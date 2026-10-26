"""contamination_tripwire: standing paired seen/unseen score divergence (2026-10-07).

Steal (find 1, the evals-self-improvement card under
watch/inbox/frontier_olm_2026-10-07/steal/): decontamination search cannot
prove unseen-ness; the standing signal is score DIVERGENCE between corpus-seen
material and a post-freeze minted twin set ("when a model's public score climbs
but the private score stays flat, that's your contamination signal"). This
graduates mag/mirror_control.py condition C into that standing tripwire, as a
separate module: the pair shape (two eval arms + ledger + candidate landing)
is not the one-shot instrument-control shape mirror_control owns.

Pair mechanics (reused organs, nothing hand-rolled):
  SEEN ARM    tools/duty_fuzz.py cycle 0: the cycle-0 reference battery, bytes
              in tools/duty_fuzz.py's docstring and filed at
              watch/inbox/duty_fuzz/cycle_000.jsonl (2026-09-18); any lane
              with repo access has SEEN this material.
  MINTED ARM  tools/duty_fuzz.py cycle 9999 (default): held-out by
              construction (g = cycle*1000 + i seeds an independent RNG per
              case; different cycles never emit the same case; deterministic,
              replay-safe). No cycle-9999 batch is filed anywhere.
  GRADER      deterministic closed-option letter match against case
              "spec_reading"; no LLM judge; no A-D letter scores wrong.
  DIVERGENCE  delta = seen_score - minted_score; delta >= threshold (config
              contamination_tripwire.threshold, default 0.15) is the WARN:
              the seen arm climbs while the minted arm stays flat. Arms
              tracking each other falsify the contamination worry for a lane.

Landing (the B2-106 kind=risk pattern, mag/improve.py run_provider_probe): the
pair row appends to <improve root>/contamination/pairs.jsonl and ONE candidate
lands via mag.improve.append_candidates with the exact provider-probe row shape
(kind=risk status=new on WARN; kind=runtime status=hold when quiet: evidence,
not a ticket). A WARN also appends EXACTLY ONE [priority] line to
mag.improve.ATTENTION_PATH (B2-494, read at call time so tests retarget it).
Cadence reuses improve.provider_probe_due, state key "last_contamination_check"
(missing or unparseable ts is due).

CLI (venv python only):
  .venv/Scripts/python.exe -m mag.contamination_tripwire --check gemma:2b
  .venv/Scripts/python.exe -m mag.contamination_tripwire --check gemma:2b --root <dir>
  .venv/Scripts/python.exe -m mag.contamination_tripwire --register
Exit codes, --check: 0 clean, 1 WARN, 2 error.

Standing call: mag.improve.run_eval invokes standing_check() each daily eval
(MagImproveDaily 08:00 drives improve_once -> run_eval): no separate schtask.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import duty_fuzz  # noqa: E402

SCHEMA = "improve_candidate.v1"
STATE_KEY = "last_contamination_check"
DEFAULT_LANE = "gemma:2b"
DEFAULT_COUNT = 12
DEFAULT_THRESHOLD = 0.15
DEFAULT_CADENCE_DAYS = 1.0
DEFAULT_SEED = duty_fuzz.DEFAULT_MASTER_SEED
SEEN_CYCLE = 0        # the cycle-0 reference battery: repo bytes since 2026-09-18
MINTED_CYCLE = 9999   # never filed anywhere: post-freeze by construction
LEDGER_DIRNAME = "contamination"
LEDGER_FILENAME = "pairs.jsonl"
PLAYBOOK_MARKER = "<!-- contamination-tripwire standing call registered"
_ANSWER_RE = re.compile(r"\b([A-D])\b")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ollama_up(timeout: float = 0.8) -> bool:
    """Mirror mag.afk_loop._ollama_up: a down janitor is a known env state."""
    import urllib.request

    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=timeout)
        return True
    except Exception:  # noqa: BLE001
        return False


def ollama_answer(lane: str, case: dict[str, Any]) -> str:
    """One local ollama ask via mag.afk_loop._ollama_ask; first A-D letter.

    No letter in the response is a wrong answer, not a crash: the grader
    stays deterministic.
    """
    from mag.afk_loop import _ollama_ask

    try:
        text = _ollama_ask(str(case.get("q") or ""), model=lane, timeout=60.0)
    except Exception:  # noqa: BLE001 - a failed ask is a wrong answer, counted
        return ""
    m = _ANSWER_RE.search(text or "")
    return m.group(1) if m else ""


def score_arm(answer_fn: Callable[[str, dict[str, Any]], str], lane: str,
              cases: list[dict[str, Any]]) -> float:
    if not cases:
        return 0.0
    hits = 0
    for case in cases:
        want = str(case.get("spec_reading") or "").strip().upper()
        got = str(answer_fn(lane, case) or "").strip().upper()
        if got and got == want:
            hits += 1
    return hits / len(cases)


def run_pair(
    lane: str,
    *,
    count: int = DEFAULT_COUNT,
    seed: int = DEFAULT_SEED,
    seen_cycle: int = SEEN_CYCLE,
    minted_cycle: int = MINTED_CYCLE,
    threshold: float = DEFAULT_THRESHOLD,
    answer_fn: Callable[[str, dict[str, Any]], str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Score the lane on BOTH arms and return the pair row.

    Same generator, count, spec on both arms: the minted arm is the same-shape
    twin of the seen arm, differing only in cycle index (unseen by
    construction). answer_fn injection keeps the pair hermetic for tests.
    """
    answer_fn = answer_fn or ollama_answer
    seen_cases = duty_fuzz.generate(seed, seen_cycle, count)
    minted_cases = duty_fuzz.generate(seed, minted_cycle, count)
    seen_score = score_arm(answer_fn, lane, seen_cases)
    minted_score = score_arm(answer_fn, lane, minted_cases)
    delta = round(seen_score - minted_score, 4)
    warn = delta >= float(threshold)
    return {
        "ts": (now or _utc_now()).isoformat(),
        "lane": lane,
        "seen_score": round(seen_score, 4),
        "minted_score": round(minted_score, 4),
        "delta": delta,
        "threshold": float(threshold),
        "verdict": "WARN" if warn else "OK",
        "warn": warn,
        "count": count,
        "seed": seed,
        "seen_cycle": seen_cycle,
        "minted_cycle": minted_cycle,
    }


def _ledger_path(paths: dict[str, Path]) -> Path:
    return paths["root"] / LEDGER_DIRNAME / LEDGER_FILENAME


def land_pair(
    pair: dict[str, Any],
    cfg: dict[str, Any],
    paths: dict[str, Path],
) -> dict[str, Any]:
    """Append the pair to the ledger and land ONE B2-106-shaped candidate.

    Row shape mirrors mag.improve.run_provider_probe exactly; the candidate
    rides mag.improve.append_candidates so dedupe-by-id is the pattern's own.
    """
    from mag import improve

    day = pair["ts"][:10]
    warn = bool(pair.get("warn"))
    claim = (
        "Contamination tripwire (lane %s): seen %.4f vs minted %.4f, delta %.4f %s %.2f"
        % (
            pair["lane"], pair["seen_score"], pair["minted_score"], pair["delta"],
            ">=" if warn else "<", float(pair["threshold"]),
        )
    )
    detail = (
        "arms: duty_fuzz seed %d, %d cases per arm, seen cycle %d (repo bytes) "
        "vs minted cycle %d (post-freeze by construction); grader: deterministic "
        "closed-option letter match"
        % (pair["seed"], pair["count"], pair["seen_cycle"], pair["minted_cycle"])
    )

    ledger = _ledger_path(paths)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(pair, ensure_ascii=False, default=str) + "\n")
    try:
        ledger_ref = str(ledger.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        # Sandboxed callers (tests, --root): the absolute path is the honest ref.
        ledger_ref = str(ledger).replace("\\", "/")

    row = {
        "schema": SCHEMA,
        "id": improve._candidate_id(claim, day + ":contamination_tripwire"),
        "date": day,
        "kind": "risk" if warn else "runtime",
        "claim": claim,
        "detail": detail[:600],
        "source": "mag_internal",
        "source_urls": [ledger_ref],
        "local_feasible": "true",
        "status": "new" if warn else "hold",
        "created": pair["ts"],
    }
    improve.append_candidates([row], paths)

    # B2-494 alarm surface, same single-mouth rule as the provider probe:
    # EXACTLY ONE [priority] line on alarm, read at call time so tests can
    # retarget improve.ATTENTION_PATH. A quiet pair writes nothing.
    if warn:
        try:
            with improve.ATTENTION_PATH.open("a", encoding="utf-8") as f:
                f.write(
                    "- [priority][contamination-tripwire] lane %s seen %.4f minted %.4f "
                    "delta %.4f (run %s) -> %s\n"
                    % (pair["lane"], pair["seen_score"], pair["minted_score"],
                       pair["delta"], day, ledger_ref)
                )
        except OSError as e:
            # the alarm still lands via the candidate row; name the lost surface
            sys.stderr.write(
                "contamination_tripwire: attention surface write failed: %s\n" % e)
    return {"pair": pair, "row": row, "ledger": ledger_ref}


def standing_check(
    cfg: dict[str, Any],
    paths: dict[str, Path],
    *,
    answer_fn: Callable[[str, dict[str, Any]], str] | None = None,
    ollama_up_fn: Callable[[], bool] | None = None,
    now: datetime | None = None,
) -> dict[str, Any] | None:
    """The run_eval hook: run the pair when the cadence is due, else None.

    Returns None when the config disables the organ or the cadence is fresh
    (B2-106 semantics). A down janitor lane returns {"ok": False, "reason":
    "ollama down"} WITHOUT landing anything: a lane that is not serving
    cannot be scored, and that is a known environment state for the eval
    step to record, not a tripwire verdict. A due run stamps the state key.
    """
    from mag import improve

    tcfg = cfg.get("contamination_tripwire") or {}
    if tcfg.get("enabled") is False:
        return None
    state = improve._load_state(paths)
    cadence = float(tcfg.get("cadence_days") or DEFAULT_CADENCE_DAYS)
    if not improve.provider_probe_due(state, cadence, now=now, key=STATE_KEY):
        return None
    up_fn = ollama_up_fn or ollama_up
    if not up_fn():
        return {"ok": False, "reason": "ollama down"}

    pair = run_pair(
        str(tcfg.get("lane") or DEFAULT_LANE),
        count=int(tcfg.get("count") or DEFAULT_COUNT),
        seed=int(tcfg.get("seed") or DEFAULT_SEED),
        seen_cycle=int(tcfg.get("seen_cycle") or SEEN_CYCLE),
        minted_cycle=int(tcfg.get("minted_cycle") or MINTED_CYCLE),
        threshold=float(tcfg.get("threshold") or DEFAULT_THRESHOLD),
        answer_fn=answer_fn,
        now=now,
    )
    landed = land_pair(pair, cfg, paths)
    state[STATE_KEY] = (now or _utc_now()).isoformat()
    state["last_contamination_summary"] = {
        "day": pair["ts"][:10],
        "lane": pair["lane"],
        "seen_score": pair["seen_score"],
        "minted_score": pair["minted_score"],
        "delta": pair["delta"],
        "verdict": pair["verdict"],
        "row_id": landed["row"]["id"],
    }
    improve._save_state(paths, state)
    return {"ok": True, "pair": pair, "row": landed["row"], "ledger": landed["ledger"]}


def register(paths: dict[str, Path], cfg: dict[str, Any] | None = None) -> bool:
    """Write the standing-call note into the improve playbook (idempotent).

    No schtask: MagImproveDaily already drives improve_once -> run_eval
    daily, and run_eval calls standing_check(). Returns True when written.
    """
    tcfg = (cfg or {}).get("contamination_tripwire") or {}
    playbook = paths["playbook"]
    playbook.parent.mkdir(parents=True, exist_ok=True)
    existing = playbook.read_text(encoding="utf-8") if playbook.is_file() else ""
    if PLAYBOOK_MARKER in existing:
        return False
    note = (
        "\n## Contamination tripwire (standing, P2 2026-10-07)\n\n"
        "%s\n"
        "- Standing call: mag.improve.run_eval -> mag.contamination_tripwire."
        "standing_check (daily via MagImproveDaily 08:00; no separate schtask).\n"
        "- Pair: duty_fuzz seen cycle %d (repo bytes) vs minted cycle %d "
        "(post-freeze by construction), %d cases per arm, deterministic letter "
        "grader; ledger memory/improve/%s/%s.\n"
        "- WARN at delta >= %s lands ONE improve candidate (kind=risk status=new) "
        "plus a [priority] attention line; a quiet pair lands kind=runtime "
        "status=hold (evidence, not a ticket).\n"
        "- Ad hoc: python -m mag.contamination_tripwire --check %s\n"
        % (
            PLAYBOOK_MARKER,
            int(tcfg.get("seen_cycle") or SEEN_CYCLE),
            int(tcfg.get("minted_cycle") or MINTED_CYCLE),
            int(tcfg.get("count") or DEFAULT_COUNT),
            LEDGER_DIRNAME, LEDGER_FILENAME,
            tcfg.get("threshold") or DEFAULT_THRESHOLD,
            tcfg.get("lane") or DEFAULT_LANE,
        )
    )
    with playbook.open("a", encoding="utf-8") as f:
        f.write(note)
    return True


def _sandbox_paths(root: Path) -> dict[str, Path]:
    return {
        "root": root,
        "candidates": root / "candidates.jsonl",
        "daily": root / "daily",
        "evals": root / "evals",
        "playbook": root / "playbook.md",
        "state": root / "state.json",
    }


def main(argv: list[str] | None = None) -> int:
    from mag import improve

    ap = argparse.ArgumentParser(description="paired seen/unseen contamination tripwire")
    ap.add_argument("--check", metavar="LANE", help="run the pair once for this lane")
    ap.add_argument("--register", action="store_true",
                    help="write the standing-call note into the improve playbook")
    ap.add_argument("--count", type=int, default=None, help="cases per arm (default %d)" % DEFAULT_COUNT)
    ap.add_argument("--threshold", type=float, default=None, help="WARN delta (default %s)" % DEFAULT_THRESHOLD)
    ap.add_argument("--seen-cycle", type=int, default=None)
    ap.add_argument("--minted-cycle", type=int, default=None)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--root", default=None, help="sandbox root for ledger/candidates/state (default: the improve config paths)")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError) as e:
        sys.stderr.write("contamination_tripwire: stdout reconfigure skipped: %s\n" % e)

    if not a.check and not a.register:
        ap.error("one of --check LANE or --register is required")

    cfg = improve.load_config()
    paths = improve.ensure_dirs(cfg) if not a.root else _sandbox_paths(Path(a.root))
    paths["root"].mkdir(parents=True, exist_ok=True)
    paths["candidates"].parent.mkdir(parents=True, exist_ok=True)

    rc = 0
    if a.register:
        written = register(paths, cfg)
        hook = "mag.improve.run_eval standing_check (daily MagImproveDaily)"
        print("register: %s (%s)" % ("written" if written else "already registered", hook))
    if a.check:
        tcfg = cfg.get("contamination_tripwire") or {}
        knobs = dict(
            count=a.count if a.count is not None else int(tcfg.get("count") or DEFAULT_COUNT),
            threshold=a.threshold if a.threshold is not None else float(tcfg.get("threshold") or DEFAULT_THRESHOLD),
            seed=a.seed if a.seed is not None else int(tcfg.get("seed") or DEFAULT_SEED),
            seen_cycle=a.seen_cycle if a.seen_cycle is not None else int(tcfg.get("seen_cycle") or SEEN_CYCLE),
            minted_cycle=a.minted_cycle if a.minted_cycle is not None else int(tcfg.get("minted_cycle") or MINTED_CYCLE),
        )
        try:
            pair = run_pair(a.check, **knobs)
            landed = land_pair(pair, cfg, paths)
            state = improve._load_state(paths)
            state[STATE_KEY] = _utc_now().isoformat()
            improve._save_state(paths, state)
            print(json.dumps(pair, ensure_ascii=False, indent=2))
            print("candidate: %s (%s)" % (landed["row"]["id"], landed["row"]["kind"]))
            print("ledger: %s" % landed["ledger"])
            if pair["warn"]:
                rc = 1
        except Exception as e:  # noqa: BLE001
            print("error: %s" % e, file=sys.stderr)
            rc = 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
