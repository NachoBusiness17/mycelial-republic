"""overmind_judge - THE DECISION JUDGE (OVERMIND-2 gap 3, 2026-10-01).

Spec: watch/inbox/model_garden/OVERMIND_THEORY.md sec 6 (controls and
judgment) + sec 7 gap 3: nothing scores DECISIONS ("was this routing call
the one the seat would have made?"). This is that instrument.

Material: for ticks of one run, pair the LOOP's actual decision against the
BLIND SEAT LIST (memory/runs/overmind/blind_seat_list.json, sealed before
any fire; the run's ledger rows carry its sha256). Judges:
  1. KIMI RELAY (labeled; the directive-compliant family per
     STEERING_DOGFOOD): sees both decisions labeled, verdict
     AGREE/DISAGREE/UNDECIDABLE + which call was better.
  2. DEEPSEEK BLIND x2 (slot-alternated): sees the two decisions as
     unlabeled A/B, slot order alternated by pair index and swapped on the
     second pass (position-bias control). The judge never learns which
     side is the loop's.
Scoring: per-pair final verdict (AGREE only when kimi and the deepseek
consensus both say AGREE; DISAGREE when both say DISAGREE; else
UNDECIDABLE), agreement rate, smarter-than-blind tallies, and the five
kill conditions of theory sec 6 evaluated from the ledger bytes.
Judge budget: ~$0.50 (banked spend from the garden usage ledger rows for
judge ask ids; the kimi rows bank 0.0 in PRICING so an OpenRouter-list
estimate is also reported).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RUN_DIR = ROOT / "memory" / "runs" / "overmind"
LEDGER = RUN_DIR / "ledger.jsonl"
BLIND = RUN_DIR / "blind_seat_list.json"
JUDGE_ASKS = RUN_DIR / "judge_asks"
GARDEN_USAGE = ROOT / "memory" / "runs" / "model_garden" / "usage.jsonl"
GARDEN_OUT = ROOT / "watch" / "inbox" / "model_garden"

KIMI = {"model": "moonshotai/kimi-k2", "base_env": "HERMES_API_KEY_2",
        "base_url": "https://inference-api.nousresearch.com/v1"}
DEEPSEEK = {"model": "deepseek-chat", "base_env": "DEEPSEEK_API_KEY",
            "base_url": "https://api.deepseek.com"}
# kimi-k2 real price ceiling per KIMI_DOSSIER (OpenRouter list, USD per M)
KIMI_REAL_PER_TOKEN = (0.57e-6, 2.30e-6)

VERDICTS = ("AGREE", "DISAGREE", "UNDECIDABLE")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_rows(run_id: str) -> list[dict]:
    rows = []
    for line in LEDGER.read_text(encoding="utf-8",
                                 errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("run_id") == run_id:
            rows.append(r)
    return sorted(rows, key=lambda r: r.get("tick") or 0)


def _git_delta(rows: list[dict], i: int) -> int:
    cur = rows[i]["senses"].get("git_changed") or 0
    base = rows[0]["senses"].get("git_changed") or 0
    return cur - base


def match_seat_entry(rows: list[dict], i: int) -> dict:
    """Mechanical matcher: which blind-list entry governs tick i's state.
    Priority mirrors the seat policy (most specific condition first).
    Failure signal comes from beat_last rows (each carries status)."""
    blind = json.loads(BLIND.read_text(encoding="utf-8"))
    entries = {e["id"]: e for e in blind["entries"]}
    r = rows[i]
    s = r.get("senses") or {}
    tick = r.get("tick") or 0
    total = rows[-1].get("tick") or len(rows)
    beat_rows = s.get("beat_rows") or 0
    quiet_streak = 0
    j = i
    while j >= 0 and (rows[j]["senses"].get("beat_rows") or 0) == 0:
        quiet_streak += 1
        j -= 1
    failed = sum(1 for b in (s.get("beat_last") or [])
                 if str(b.get("status") or "").lower() in ("failed", "error"))
    if i == len(rows) - 1 and tick == total:
        return entries["D10"]
    if beat_rows == 0 and quiet_streak >= 10:
        return entries["D03"]
    if failed >= 2:
        return entries["D01"]
    if _git_delta(rows, i) >= 20:
        return entries["D04"]
    if (s.get("landed_count") or 0) > 0:
        return entries["D05"]
    if i > 0 and rows[i - 1]["senses"] == s:
        return entries["D08"]
    if beat_rows == 0:
        return entries["D02"]
    return entries["D11"]


def build_pairs(rows: list[dict], max_pairs: int = 14) -> list[dict]:
    """Judge every non-NOOP decision plus a deterministic NOOP stride."""
    non_noop = [i for i, r in enumerate(rows)
                if (r.get("verb") or "") != "NOOP"]
    noops = [i for i, r in enumerate(rows) if (r.get("verb") or "") == "NOOP"]
    stride = max(1, len(noops) // max(1, max_pairs - len(non_noop))) \
        if noops else 1
    picked = sorted(set(non_noop) | set(noops[::stride]))[:max_pairs]
    pairs = []
    for i in picked:
        r = rows[i]
        entry = match_seat_entry(rows, i)
        pairs.append({
            "pair_id": f"p{i + 1:02d}", "tick": r.get("tick"),
            "senses": r.get("senses"),
            "loop": {"verb": r.get("verb"), "reason": r.get("reason"),
                     "executed": r.get("executed"),
                     "verified": r.get("verified")},
            "seat": {"entry_id": entry["id"], "verb": entry["verb"],
                     "payload": entry.get("payload", {}),
                     "reason": entry["reason"],
                     "when": entry["when"]},
        })
    return pairs


def _fire(ask_id: str, spec: dict, contract: str) -> tuple[dict | None, float]:
    from tools import model_garden
    d = JUDGE_ASKS / ask_id
    d.mkdir(parents=True, exist_ok=True)
    meta = {"id": ask_id, "model": spec["model"],
            "base_env": spec["base_env"], "base_url": spec["base_url"],
            "contract": contract, "evidence": [], "self_contained": True}
    (d / "ask.json").write_text(
        json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    res = model_garden.run_ask(d, execute=True)
    out = GARDEN_OUT / f"{ask_id}.md"
    raw = out.read_text(encoding="utf-8", errors="replace") \
        if out.is_file() else ""
    from tools.overmind_brain import parse_json_object
    return parse_json_object(raw), float(res.get("cost_usd") or 0.0)


def _parse_judge_reply(raw: str) -> dict | None:
    from tools.overmind_brain import parse_json_object
    return parse_json_object(raw)


def _read_judge_reply(ask_id: str) -> str:
    out = GARDEN_OUT / f"{ask_id}.md"
    return out.read_text(encoding="utf-8", errors="replace") \
        if out.is_file() else ""


def judge_kimi(pair: dict, run_id: str) -> dict:
    ask_id = f"overmind-judge-{run_id}-{pair['pair_id']}-kimi"
    contract = (
        "DECISION-REVIEW (orchestration judgment, OVERMIND falsifier run).\n"
        "Two deciders faced this one estate tick:\n"
        "- SEAT LIST: a standing policy written BLIND, before the run, by "
        "the seat class that built the loop.\n"
        "- LOOP: what the unattended cheap overmind actually decided.\n\n"
        "TICK SENSES (deterministic estate reads; trust only these):\n"
        + json.dumps(pair["senses"], ensure_ascii=False)[:3000] + "\n\n"
        "SEAT LIST decision: " + json.dumps(pair["seat"],
                                            ensure_ascii=False) + "\n"
        "LOOP decision: " + json.dumps(pair["loop"],
                                       ensure_ascii=False) + "\n\n"
        "Reply with EXACTLY one line, ONE JSON object:\n"
        '{"verdict": "AGREE or DISAGREE or UNDECIDABLE", "reason": "<=30 '
        'words", "better": "SEAT or LOOP or NEITHER", "why_better": "<=20 '
        'words"}\n'
        "verdict: do the two decisions materially agree on what this tick "
        "should do (same verb class for the same state, or both legal "
        "holds)? UNDECIDABLE only if the material is insufficient. better: "
        "when they differ, which call was the smarter orchestration move. "
        "No em-dash characters.")
    ask_id = f"overmind-judge-{run_id}-{pair['pair_id']}-kimi"
    raw = _read_judge_reply(ask_id)
    cost = 0.0
    if not raw:  # fire only when the banked bytes are missing (idempotent)
        _, cost = _fire(ask_id, KIMI, contract)
        raw = _read_judge_reply(ask_id)
    dec = _parse_judge_reply(raw)
    v = (dec or {}).get("verdict")
    return {"judge": "kimi", "verdict": v if v in VERDICTS else "UNDECIDABLE",
            "reason": str((dec or {}).get("reason") or "")[:200],
            "better": str((dec or {}).get("better") or "NEITHER"),
            "cost_usd": cost}


def _blind_contract(pair: dict, loop_is_a: bool) -> str:
    a = pair["loop"] if loop_is_a else pair["seat"]
    b = pair["seat"] if loop_is_a else pair["loop"]
    return (
        "ORCHESTRATION CALL REVIEW. An always-on estate loop sampled one "
        "tick of estate state; two candidate decisions were recorded. Judge "
        "the calls on their merits only.\n\n"
        "STATE (deterministic reads; trust only these):\n"
        + json.dumps(pair["senses"], ensure_ascii=False)[:3000] + "\n\n"
        "DECISION A: " + json.dumps(a, ensure_ascii=False) + "\n"
        "DECISION B: " + json.dumps(b, ensure_ascii=False) + "\n\n"
        "Reply with EXACTLY one line, ONE JSON object:\n"
        '{"equivalent": "AGREE or DISAGREE or UNDECIDABLE", "better": "A or '
        'B or EQUAL", "reason": "<=30 words"}\n'
        "equivalent: do A and B materially do the same orchestration thing "
        "given this state? better: when they differ, which is the smarter "
        "call. No em-dash characters.")


def judge_deepseek(pair: dict, run_id: str, pass_no: int) -> dict:
    loop_is_a = (int(pair["pair_id"][1:]) + pass_no) % 2 == 0
    ask_id = f"overmind-judge-{run_id}-{pair['pair_id']}-ds{pass_no}"
    raw = _read_judge_reply(ask_id)
    cost = 0.0
    if not raw:  # fire only when the banked bytes are missing (idempotent)
        _, cost = _fire(ask_id, DEEPSEEK,
                        _blind_contract(pair, loop_is_a))
        raw = _read_judge_reply(ask_id)
    dec = _parse_judge_reply(raw)
    v = (dec or {}).get("equivalent")
    better = str((dec or {}).get("better") or "EQUAL")
    mapped = better
    if better in ("A", "B"):
        was_loop = loop_is_a if better == "A" else not loop_is_a
        mapped = "LOOP" if was_loop else "SEAT"
    return {"judge": f"deepseek{pass_no}", "verdict":
            v if v in VERDICTS else "UNDECIDABLE",
            "reason": str((dec or {}).get("reason") or "")[:200],
            "better": mapped, "cost_usd": cost}


def judge_budget_spent() -> tuple[float, float]:
    """(banked, real-estimate) spend on judge asks from the byte-truth
    ledger; kimi rows bank 0.0 in PRICING so the real estimate uses the
    dossier list price on its token counts."""
    banked, real = 0.0, 0.0
    if not GARDEN_USAGE.is_file():
        return 0.0, 0.0
    for line in GARDEN_USAGE.read_text(encoding="utf-8",
                                       errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not str(row.get("id", "")).startswith("overmind-judge-"):
            continue
        banked += float(row.get("cost_usd") or 0.0)
        if "kimi" in str(row.get("model") or ""):
            real += (int(row.get("prompt_tokens") or 0) * KIMI_REAL_PER_TOKEN[0]
                     + int(row.get("completion_tokens") or 0)
                     * KIMI_REAL_PER_TOKEN[1])
        else:
            real += float(row.get("cost_usd") or 0.0)
    return round(banked, 6), round(real, 6)


def run_judgment(run_id: str, max_pairs: int = 14) -> dict:
    rows = load_rows(run_id)
    blind = json.loads(BLIND.read_text(encoding="utf-8"))
    pairs = build_pairs(rows, max_pairs=max_pairs)
    print(f"judging {len(pairs)} pairs for run {run_id}", flush=True)
    scored = []
    for pair in pairs:
        k = judge_kimi(pair, run_id)
        d1 = judge_deepseek(pair, run_id, 1)
        d2 = judge_deepseek(pair, run_id, 2)
        ds_votes = [d["verdict"] for d in (d1, d2)]
        ds_consensus = ds_votes[0] if ds_votes[0] == ds_votes[1] \
            else "UNDECIDABLE"
        if k["verdict"] == "AGREE" and ds_consensus == "AGREE":
            final = "AGREE"
        elif k["verdict"] == "DISAGREE" and ds_consensus == "DISAGREE":
            final = "DISAGREE"
        else:
            final = "UNDECIDABLE"
        better = [x["better"] for x in (k, d1, d2)
                  if x["better"] in ("LOOP", "SEAT")]
        smarter = ("LOOP" if better.count("LOOP") >= 2 else
                   "SEAT" if better.count("SEAT") >= 2 else "SPLIT")
        scored.append({"pair_id": pair["pair_id"], "tick": pair["tick"],
                       "seat_entry": pair["seat"]["entry_id"],
                       "loop_verb": pair["loop"]["verb"],
                       "seat_verb": pair["seat"]["verb"],
                       "kimi": k, "deepseek": [d1, d2],
                       "ds_consensus": ds_consensus, "final": final,
                       "smarter": smarter})
        print(f"  {pair['pair_id']} tick {pair['tick']}: loop="
              f"{pair['loop']['verb']} seat={pair['seat']['verb']}"
              f"({pair['seat']['entry_id']}) -> {final} smarter={smarter}",
              flush=True)
    n = len(scored)
    agree = sum(1 for s in scored if s["final"] == "AGREE")
    banked, real = judge_budget_spent()
    out = {"schema": "overmind.judgment.v1", "run_id": run_id,
           "judged_ts": _now(),
           "blind_list_sha256_at_run": rows[0].get("blind_sha256")
           if rows and "blind_sha256" in rows[0] else blind["seal_sha256"],
           "pairs": scored,
           "agreement_rate": round(agree / n, 4) if n else 0.0,
           "agree": agree, "judged": n,
           "loop_smarter": sum(1 for s in scored if s["smarter"] == "LOOP"),
           "seat_smarter": sum(1 for s in scored if s["smarter"] == "SEAT"),
           "judge_spend_banked_usd": banked,
           "judge_spend_real_est_usd": real}
    path = RUN_DIR / f"judgment_{run_id}.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False),
                    encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"},
                     ensure_ascii=False), flush=True)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="overmind_judge")
    ap.add_argument("cmd", choices=["judge"])
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--max-pairs", type=int, default=14)
    args = ap.parse_args(argv)
    if not LEDGER.is_file() or not BLIND.is_file():
        print("USAGE-ERROR: ledger or blind list missing")
        return 2
    run_judgment(args.run_id, max_pairs=args.max_pairs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
