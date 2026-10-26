"""Duel harness: one ask, two model families, one cheap judge (Mickey17 W3, 2026-09-29).

Problem (wave ledger return 8, watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md):
the hermes gopher burn fired G1 (qwen) and G3 (glm-prime) on the same
adversarial-review ask and promised a cross-family diff inside the prompt,
but the diff was never computed. No scoring artifact exists.

Fix: clone the gopher driver's call pattern (watch/inbox/
game_platform_basecamp_20260929/hermes_gopher_burn_20260929.py: Nous
inference API, OpenAI-compatible; keys loaded from the hermes .env;
reasoning capped at 6000 so the answer gets written; cost metering prefers
usage.cost from the API and falls back to the published price table), fire
ONE ask to TWO models, then a THIRD cheap call (fireworks/ember-1) judges
A-vs-B against a rubric embedded in the judging ask. Every duel appends
one row to logs/duel/duels.jsonl: {ask_id, a_model, b_model, a_cost, b_cost,
judge, winner, rubric, ts, corr_id} plus judge detail (criteria table, rationale,
judge_cost). corr_id is the AH14 join field: MAG_CORR_ID from the env, else a
uuid4 hex8 minted once per series (process). Rows feed the tier ladder and the
future gps router (the
return 8 improvement clause: burn fuel becomes router training data).

Retroactive mode (--from-jsonl + --a-id/--b-id): loads two already-paid
answers from a burn output file, fires only the judge call, and banks the
verdict row with the real already-spent contender costs. This is how the
never-judged G1-vs-G3 duel gets its verdict without re-paying the
contenders.

Deliberate deviation from the gopher retry law: the driver rotated the
model on HTTP error (lane availability), a duel must NOT, because rotating
a contender corrupts the A-vs-B comparison. Retries reuse the same model
with the next key.

Judge blinding (v1.1, S5 Arena methodology audit 2026-09-29): the judge
sees contenders as A and B only. LMSYS anonymizes contenders until after
the vote because judge models are biased by model identity; v1.0 leaked
a_model/b_model inside the ANSWER_A/ANSWER_B tags, so the names are no
longer parameters of judge_prompt at all (a future edit cannot re-leak
them) and are logged in the ledger row instead. Presentation order
alternates per duel: slot A carries logical B's text whenever the ledger
already holds an odd number of rows, so position bias cancels across
duels; the banked winner and per-criterion scores are always remapped to
the logical a_model/b_model contenders. Each row also logs answer length
and markdown-header count per contender for future style-control
regression (content vs volume separation).

Usage:
    python tools/duel_harness.py --ask-id my-duel --ask "review X" \\
        --a-model qwen/qwen3.8-max-prime --b-model z-ai/glm-5.3-prime
    python tools/duel_harness.py --ask-id retro-g1-g3 \\
        --from-jsonl watch/inbox/game_platform_basecamp_20260929/GOPHER_BURN_output3_healthy_20260929.jsonl \\
        --a-id G1-adversarial-baseline-qwen --b-id G3-model-test-glm-prime \\
        --ask "adversarial review of the baseline spec" --context-file spec.md
    python tools/duel_harness.py ... --judge-rubric "coverage,severity,evidence,actionability" --dry
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERMES_DIR = Path(r"C:\Users\foste\AppData\Local\hermes")

ALLOWED_HOST = "inference-api.nousresearch.com"
BASE = "https://" + ALLOWED_HOST + "/v1/chat/completions"
KEY_ENVS = ("NOUS_SDD_API_KEY", "HERMES_API_KEY_1", "HERMES_API_KEY_2")

MODELS = ["z-ai/glm-5.3-prime", "qwen/qwen3.8-max-prime", "fireworks/ember-1"]
# Pricing per 1M tokens (USD), Nous published list, budget meter fallback
# only; real metering prefers usage.cost returned by the API.
PRICE = {
    "z-ai/glm-5.3-prime": (3.0, 15.0),
    "qwen/qwen3.8-max-prime": (3.0, 15.0),
    "fireworks/ember-1": (0.3, 1.2),
}

DEFAULT_A = "qwen/qwen3.8-max-prime"
DEFAULT_B = "z-ai/glm-5.3-prime"
DEFAULT_JUDGE = "fireworks/ember-1"
DEFAULT_RUBRIC = "section coverage, defect severity, evidence citations, actionability"

OUT_DEFAULT = ROOT / "logs" / "duel" / "duels.jsonl"

# ---------------------------------------------------------------------------
# AH14 correlation law (receipt watch/inbox/last_mile_20260930/AH14_CORR_ID.md;
# canonical definition: mag/trajectory_step.py): every provenance row —
# trajectory steps, game-flow burns, duels — carries the same optional join
# field corr_id, a uuid4 hex8 carried in the MAG_CORR_ID env var. This
# harness is stdlib-standalone by design, so the resolver is re-implemented
# here with the identical env var and hex8 shape. Duels MINT one corr_id per
# series when the env is unset: a series is one seat's process (a series
# script imports this module and fires many run_duel calls), so every duel
# banked by that process joins the same minted id; env-set ids always win.
# Old rows without the field read as null (absent = null, readers must not
# break).
# ---------------------------------------------------------------------------

CORR_ENV = "MAG_CORR_ID"
_SERIES_CORR: str | None = None


def series_corr_id() -> str:
    """MAG_CORR_ID from the env when the lane set it, else the per-series mint."""
    global _SERIES_CORR
    env = os.environ.get(CORR_ENV)
    if env:
        return env
    if _SERIES_CORR is None:
        _SERIES_CORR = uuid.uuid4().hex[:8]
    return _SERIES_CORR

REASONING_CAP = 6000  # LESSIG RAILS pattern from the driver: cap reasoning or the answer never gets written
CONTENDER_TOKENS = 16000
JUDGE_TOKENS = 6000
ANSWER_LIMIT = 20000  # chars of each answer shown to the judge, cost bound
CONTEXT_LIMIT = 9000  # chars of optional reference doc shown to the judge

WINNER_RE = re.compile(r"^winner\s*:\s*(?P<w>[AB]|TIE)\b", re.IGNORECASE)
CRIT_RE = re.compile(
    r"^crit\s*\|\s*(?P<crit>.+?)\s*\|\s*A\s*=\s*(?P<a>\d+)\s*\|\s*B\s*=\s*(?P<b>\d+)\s*\|\s*(?P<note>.*)$",
    re.IGNORECASE,
)
RATIONALE_RE = re.compile(r"^rationale\s*:\s*(?P<r>.+)$", re.IGNORECASE)

# Markdown header line (ATX, 1-6 hashes + text): the style-control signal
# logged per contender (S5 v1.1: volume vs content regression).
HEADER_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S", re.MULTILINE)


def load_dotenv(path: Path) -> None:
    # inline replacement for models.env_load (module absent in this install,
    # same as the gopher driver 2026-09-29)
    if not path.is_file():
        return
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def load_keys() -> list[str]:
    load_dotenv(HERMES_DIR / ".env")
    keys = [k for k in (os.environ.get(e) for e in KEY_ENVS) if k]
    if not keys:
        keys = [os.environ.get(e) for e in KEY_ENVS if os.environ.get(e)]
    return [k for k in keys if k]


def call(model: str, prompt: str, key: str, max_tokens: int = CONTENDER_TOKENS) -> dict:
    """One Nous inference call, byte-shape identical to the gopher driver's."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": {"max_tokens": REASONING_CAP},
    }).encode()
    req = urllib.request.Request(
        BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def fire(model: str, prompt: str, keys: list[str], tag: str,
         caller=call, max_tokens: int = CONTENDER_TOKENS) -> tuple[str, float]:
    """Fire one call with a single retry (same model, next key).

    Model rotation on retry is refused: a duel contender must stay fixed
    (see module docstring). Returns (content, cost_usd).
    """
    last_err: Exception | None = None
    for attempt in (1, 2):
        key = keys[hash((tag, attempt)) % len(keys)]
        try:
            t0 = time.time()
            resp = caller(model, prompt, key, max_tokens=max_tokens)
            usage = resp.get("usage", {})
            cost = cost_of(model, usage)
            msg = resp["choices"][0]["message"]
            content = msg.get("content") or ""
            if not content.strip():
                raise ValueError(f"{tag}: empty content from {model}")
            print(f"fire {tag} model={model} cost=${cost:.4f} "
                  f"secs={time.time() - t0:.1f} chars={len(content)}")
            return content, cost
        except urllib.error.HTTPError as e:
            last_err = e
            print(f"retry {tag} after HTTP {e.code} (same model, next key)")
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"error {tag}: {e}")
    raise RuntimeError(f"{tag}: both attempts failed: {last_err}")


def cost_of(model: str, usage: dict) -> float:
    """Real cost first (usage.cost from the API), published price fallback."""
    c = usage.get("cost") if isinstance(usage, dict) else None
    if c is not None:
        return float(c)
    pi, po = PRICE.get(model, (3.0, 15.0))
    return (usage.get("prompt_tokens", 0) / 1e6) * pi + (usage.get("completion_tokens", 0) / 1e6) * po


def judge_prompt(task: str, a_text: str, b_text: str,
                 rubric: list[str], context: str | None = None) -> str:
    """Build the blind judging ask (v1.1, S5 Arena audit).

    Contenders appear as A and B only. Model identities are deliberately
    NOT parameters of this function, so no call site can leak them into
    the judge's context; they are logged in the ledger row instead.
    a_text/b_text are the PRESENTED slot contents (already swapped by the
    caller when position-bias control flips the order).
    """
    crit_lines = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(rubric))
    ctx = ""
    if context:
        ctx = "\n<REFERENCE_DOCUMENT (what both answers were reviewing)>\n" + context[:CONTEXT_LIMIT] + "\n</REFERENCE_DOCUMENT>\n"
    return (
        "You are the judge of a two-model duel. Two anonymous models, A and B, "
        "answered the same ask. Score both against the rubric, then pick one winner.\n\n"
        f"RUBRIC (score each criterion 0-5 for A and for B):\n{crit_lines}\n\n"
        "<ASK>\n" + task + "\n</ASK>\n"
        + ctx +
        "\n<ANSWER_A>\n" + a_text[:ANSWER_LIMIT] + "\n</ANSWER_A>\n\n"
        "<ANSWER_B>\n" + b_text[:ANSWER_LIMIT] + "\n</ANSWER_B>\n\n"
        "OUTPUT CONTRACT (strict, machine-parsed):\n"
        "Line 1 exactly: WINNER: A   (or WINNER: B, or WINNER: TIE)\n"
        "Then exactly one line per rubric criterion in order:\n"
        "CRIT | <criterion> | A=<0-5> | B=<0-5> | <note under 12 words>\n"
        "Final line exactly: RATIONALE: <one line under 25 words>\n\n"
        "Laws: no em-dashes in your output. The contenders' identities are "
        "withheld (blind judging): judge only what is on the page. "
        "Depth of concrete defects beats volume of prose. No preamble."
    )


def parse_judge(text: str) -> dict:
    """Parse the strict judge contract. Returns winner/criteria/rationale/parsed.

    parsed is True only when a valid winner line AND a rationale line were
    found; a missing criterion table does not void the verdict but is
    reported by len(criteria). Unparseable output yields winner UNPARSED
    and parsed False so the caller can refuse to bank a fake verdict.
    """
    winner = "UNPARSED"
    criteria: list[dict] = []
    rationale = ""
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith("winner:") and winner == "UNPARSED":
            m = WINNER_RE.match(line)
            if m:
                w = m.group("w").upper()
                winner = "TIE" if w == "TIE" else w
        elif low.startswith("crit"):
            m = CRIT_RE.match(line)
            if m:
                criteria.append({
                    "criterion": m.group("crit").strip(),
                    "a": int(m.group("a")),
                    "b": int(m.group("b")),
                    "note": m.group("note").strip(),
                })
        elif low.startswith("rationale:") and not rationale:
            m = RATIONALE_RE.match(line)
            if m and m.group("r").strip():
                rationale = m.group("r").strip()
    parsed = winner in ("A", "B", "TIE") and bool(rationale)
    if not parsed:
        winner = "UNPARSED"
    return {"winner": winner, "criteria": criteria, "rationale": rationale, "parsed": parsed}


def count_headers(text: str) -> int:
    """Markdown ATX header lines in an answer (style-control signal, S5 v1.1)."""
    return len(HEADER_RE.findall(text or ""))


def ledger_row_count(out_path: Path) -> int:
    """Duel rows already banked in the ledger file (0 when absent)."""
    if not out_path.is_file():
        return 0
    with open(out_path, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for line in f if line.strip())


def map_winner(slot_winner: str, swap: bool) -> str:
    """Remap the judge's slot verdict to the logical contender.

    When swap is set, slot A in the prompt held logical B's text (position-
    bias control), so the judge's A means our B. TIE and UNPARSED pass
    through unchanged.
    """
    if not swap or slot_winner not in ("A", "B"):
        return slot_winner
    return "B" if slot_winner == "A" else "A"


def remap_criteria(criteria: list[dict], swap: bool) -> list[dict]:
    """Remap per-criterion slot scores to logical contenders (a/b flip)."""
    if not swap:
        return criteria
    return [dict(c, a=c["b"], b=c["a"]) for c in criteria]


def load_pair(jsonl_path: Path, a_id: str, b_id: str) -> tuple[dict, dict]:
    """Load two already-paid answer rows from a burn output jsonl."""
    found: dict[str, dict] = {}
    with open(jsonl_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("id") in (a_id, b_id):
                found[row["id"]] = row
    missing = [i for i in (a_id, b_id) if i not in found]
    if missing:
        raise KeyError(f"rows not found in {jsonl_path}: {missing}")
    if not (found[a_id].get("content") or "").strip() or not (found[b_id].get("content") or "").strip():
        raise ValueError(f"empty content in one of {a_id}/{b_id}")
    return found[a_id], found[b_id]


def run_duel(
    ask_id: str,
    task: str,
    a_model: str,
    b_model: str,
    a_text: str | None = None,
    b_text: str | None = None,
    a_cost: float | None = None,
    b_cost: float | None = None,
    judge_model: str = DEFAULT_JUDGE,
    rubric: list[str] | None = None,
    context: str | None = None,
    out_path: Path = OUT_DEFAULT,
    keys: list[str] | None = None,
    caller=call,
    mode: str = "live",
    swap: bool | None = None,
) -> dict:
    """Fire (or load) both contenders, judge blind, append one row to the ledger.

    caller is injectable so tests run the full pipeline on fake responses
    without any network or spend. swap forces (True/False) or auto-picks
    (None) the presentation order: slot A carries logical B's text whenever
    the ledger already holds an odd number of rows, so position bias
    cancels across consecutive duels (S5 Arena finding, v1.1). The banked
    winner/criteria are always in logical a_model/b_model terms.
    """
    rubric = [c.strip() for c in (rubric or DEFAULT_RUBRIC.split(",")) if c.strip()]
    keys = keys if keys is not None else load_keys()
    if not keys:
        raise SystemExit("NO KEYS - aborting without spend")

    if a_text is None or b_text is None:
        a_text, a_cost = fire(a_model, task, keys, f"{ask_id}:A", caller=caller)
        b_text, b_cost = fire(b_model, task, keys, f"{ask_id}:B", caller=caller)
    # retro mode: costs come from the burn rows (already paid there)
    assert a_cost is not None and b_cost is not None

    if swap is None:
        swap = ledger_row_count(out_path) % 2 == 1
    slot_a_text, slot_b_text = (b_text, a_text) if swap else (a_text, b_text)
    jp = judge_prompt(task, slot_a_text, slot_b_text, rubric, context)
    j_text, j_cost = fire(judge_model, jp, keys, f"{ask_id}:JUDGE",
                          caller=caller, max_tokens=JUDGE_TOKENS)
    verdict = parse_judge(j_text)

    row = {
        "ask_id": ask_id,
        "a_model": a_model,
        "b_model": b_model,
        "a_cost": round(float(a_cost), 4),
        "b_cost": round(float(b_cost), 4),
        "judge": judge_model,
        "winner": map_winner(verdict["winner"], swap),
        "rubric": rubric,
        "ts": datetime.now(timezone.utc).isoformat(),
        "corr_id": series_corr_id(),  # AH14 join field (env wins; per-series mint when unset)
        "mode": mode,
        "swap": swap,
        "judge_cost": round(float(j_cost), 4),
        "criteria": remap_criteria(verdict["criteria"], swap),
        "rationale": verdict["rationale"],
        "a_chars": len(a_text),
        "b_chars": len(b_text),
        "a_headers": count_headers(a_text),
        "b_headers": count_headers(b_text),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    print(f"DUEL {ask_id}: winner={row['winner']} swap={row['swap']} "
          f"a_cost=${row['a_cost']} b_cost=${row['b_cost']} judge_cost=${row['judge_cost']}")
    print(f"RATIONALE: {row['rationale'] or '(none parsed)'}")
    return row


def _auto_ask_id(ask: str, a_model: str, b_model: str) -> str:
    h = hashlib.sha1((ask + "|" + a_model + "|" + b_model).encode()).hexdigest()[:12]
    return "duel-" + h


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ask", help="the duel ask (live: fired at both contenders; retro: judge context only)")
    p.add_argument("--ask-id", help="stable ledger id (default: duel-<sha1 of ask+models>)")
    p.add_argument("--a-model", default=DEFAULT_A)
    p.add_argument("--b-model", default=DEFAULT_B)
    p.add_argument("--judge", default=DEFAULT_JUDGE)
    p.add_argument("--judge-rubric", default=DEFAULT_RUBRIC,
                   help="comma-separated criteria the judge scores A and B on")
    p.add_argument("--from-jsonl", type=Path, help="retro mode: burn output holding both answers")
    p.add_argument("--a-id", help="retro mode: row id of answer A in --from-jsonl")
    p.add_argument("--b-id", help="retro mode: row id of answer B in --from-jsonl")
    p.add_argument("--context-file", type=Path,
                   help="optional reference doc shown to the judge (what was reviewed)")
    p.add_argument("--out", type=Path, default=OUT_DEFAULT)
    p.add_argument("--dry", action="store_true", help="print the plan, no calls, no writes")
    args = p.parse_args(argv)

    rubric = [c.strip() for c in args.judge_rubric.split(",") if c.strip()]
    retro = bool(args.from_jsonl)
    if retro and not (args.a_id and args.b_id):
        p.error("--from-jsonl requires --a-id and --b-id")
    if not retro and not args.ask:
        p.error("live mode requires --ask")

    ask_id = args.ask_id or _auto_ask_id(args.ask or "", args.a_model, args.b_model)
    context = None
    if args.context_file:
        context = args.context_file.read_text(encoding="utf-8", errors="replace")

    if args.dry:
        plan = {
            "ask_id": ask_id, "mode": "retro" if retro else "live",
            "a_model": args.a_model, "b_model": args.b_model, "judge": args.judge,
            "rubric": rubric, "from_jsonl": str(args.from_jsonl) if retro else None,
            "context_file": str(args.context_file) if args.context_file else None,
            "out": str(args.out), "ask_preview": (args.ask or "")[:200],
        }
        print(json.dumps(plan, indent=2))
        return 0

    if retro:
        a_row, b_row = load_pair(args.from_jsonl, args.a_id, args.b_id)
        task = args.ask or (
            "Retroactive duel: both answers below responded to the same ask "
            "(the original prompt is not stored in the burn row; judge the "
            "answers as adversarial spec reviews against each other)."
        )
        row = run_duel(
            ask_id, task,
            a_row["model"], b_row["model"],
            a_text=a_row["content"], b_text=b_row["content"],
            a_cost=a_row.get("cost_usd", 0.0), b_cost=b_row.get("cost_usd", 0.0),
            judge_model=args.judge, rubric=rubric, context=context,
            out_path=args.out, mode="retro",
        )
    else:
        row = run_duel(
            ask_id, args.ask,
            args.a_model, args.b_model,
            judge_model=args.judge, rubric=rubric, context=context,
            out_path=args.out, mode="live",
        )
    return 0 if row["winner"] != "UNPARSED" else 1


if __name__ == "__main__":
    sys.exit(main())
