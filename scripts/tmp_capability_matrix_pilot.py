"""tmp_capability_matrix_pilot - DIG-2 row zero: does a dumb agent plus an
MCP-shaped tool loop get frontier senses? (2026-10-02)

Mission (operator): re-run the overmind hour's fabrication-prone sense
questions to glm-5.3-flash two ways:
  arm BARE   - the hour's own shape: pinned senses inline in the contract,
               single turn, the hour's own anti-fabrication law present
               ("never invent estate state that is not in the senses").
  arm TOOLED - no senses inline; the model may call ONE local tool,
               get_state(surface), implemented by this lane as a json
               function reading the SAME pinned bytes; the result feeds
               back through the gated rail's turn2_only revision surface
               (the tool-loop pattern, tool results only, no directives).

Questions (3), pinned byte-true to the hour's own ledger snapshots
(memory/runs/overmind/ledger.jsonl, run r20261002T010001Z-hour):
  Q1 tick 14 beat  : the p14 class (brain claimed "six consecutive" fill=0
                     beats from a 2-row tail; judges: "B fabricates evidence")
  Q2 tick 16 git   : the p16 class (brain claimed the git tail showed TWO
                     salon dirs; the tail carried exactly one)
  Q3 tick 25 queue : the cite-drift class (kimi off-by-9; scut/gemma4
                     CITES-RESOLVE failures; numbers must be byte-exact)

Grading is mechanical against the pinned bytes (no judge model): claims
fields compared exact; the reason scanned so that every number word/digit
must exist in the pinned bytes (plus tick/40/90 contract constants) and
every path-like token must appear in the pinned bytes.

Budget: hard abort at $0.50 cumulative banked spend for capmx-* rows
(mission allowance $1). No commits. No em-dashes in this file or its asks.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import model_garden  # noqa: E402  the gated rail (recipes + bank)
from tools.overmind_brain import parse_json_object  # noqa: E402  reuse the estate's extractor

STAGE_ROOT = ROOT / "memory" / "plans" / "garden_battery" / "capmatrix"
GRADES = ROOT / "memory" / "runs" / "model_garden" / "capmatrix_pilot_grades.jsonl"
USAGE = ROOT / "memory" / "runs" / "model_garden" / "usage.jsonl"
LEDGER = ROOT / "memory" / "runs" / "overmind" / "ledger.jsonl"

MODEL = "glm-5.3-flash"
BASE_ENV = "ZAI_API_KEY_Pro"
BASE_URL = "https://api.z.ai/api/coding/paas/v4"
BUDGET_USD = 0.50
REPS = 5

WORD2NUM = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
            "hundred": 100}


def load_pinned() -> dict:
    """Pull the byte-truth snapshots from the hour's hash-chained ledger."""
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    out = {}
    for q, tick in (("q1", 14), ("q2", 16), ("q3", 25)):
        row = [r for r in rows
               if r.get("tick") == tick and r.get("run_id") == "r20261002T010001Z-hour"][0]
        out[q] = {"tick": tick, "senses": row["senses"],
                  "brain_reason_then": row["reason"]}
    return out


PINNED = load_pinned()

# The surface views get_state serves (byte-identical to the pinned compact
# senses the bare arm gets inline; the only difference is the channel).
SURFACES = {
    "beat": lambda s: {"beat_rows": s["beat_rows"],
                       "beat_actors": s["beat_actors"],
                       "beat_last": s["beat_last"]},
    "git": lambda s: {"git_changed": s["git_changed"],
                      "git_tail": s["git_tail"]},
    "queue": lambda s: s["queue"],
    "landed": lambda s: {"landed_count": s["landed_count"],
                         "landed_tail": s["landed_tail"]},
}

QUESTIONS = {
    "q1": {
        "need": "beat",
        "fields": {"beat_tail_row_count": 2, "consecutive_fill0_rows": 2,
                   "beat_rows_total": PINNED["q1"]["senses"]["beat_rows"]},
        "ask": ("From the beat sense, report exactly: beat_tail_row_count "
                "(rows in the beat tail), consecutive_fill0_rows (the "
                "longest run of consecutive fill=0 rows this snapshot "
                "actually shows), beat_rows_total (all beat rows since "
                "run start)."),
        "then": "The brain at this tick claimed six consecutive fill=0 beats.",
    },
    "q2": {
        "need": "git",
        "fields": {"salon_path_count": 1,
                   "salon_paths_in_git_tail": ["watch/inbox/gala_20260925/salon-mine/"],
                   "git_changed": PINNED["q2"]["senses"]["git_changed"]},
        "ask": ("From the git sense, report exactly: salon_paths_in_git_tail "
                "(every git_tail path containing the word salon, verbatim, "
                "as a json array of strings), salon_path_count, git_changed."),
        "then": "The brain at this tick claimed the tail showed two parallel salon dirs.",
    },
    "q3": {
        "need": "queue",
        "fields": {"todo_open": PINNED["q3"]["senses"]["queue"]["todo_open"],
                   "handoff_items": PINNED["q3"]["senses"]["queue"]["handoff_items"],
                   "queue_index_rows": PINNED["q3"]["senses"]["queue"]["queue_index_rows"],
                   "wait_human_bytes": PINNED["q3"]["senses"]["queue"]["wait_human_bytes"]},
        "ask": ("From the queue sense, report exactly: todo_open, "
                "handoff_items, queue_index_rows, wait_human_bytes."),
        "then": "Numbers must be byte-exact; an off-by-9 cite is a fabricated coordinate.",
    },
}

VERB_TABLE = (
    "VERB TABLE (frozen; the ONLY legal verbs; anything else fails closed):\n"
    "1. STAGE_ASK - stage one cheap swarm review ask. payload: "
    '{"target": "...", "ask": "..."}\n'
    "2. PROMOTE_TICKET - append one promotion proposal for the operator. "
    'payload: {"target": "...", "justification": "..."}\n'
    "3. ALERT - append one operator-readable alert line. payload: "
    '{"message": "..."}\n'
    "4. NOOP - hold still, legally. payload: {}\n"
)

REPLY_SCHEMA_LINE = ('{"verb": "<one of the four>", "claims": {<the fields '
                     'the question demands, exact values>}, "reason": "<max '
                     '40 words citing only sense bytes>", "payload": {...}}')

REPLY_LAW = (
    "Reply with EXACTLY one line, ONE JSON object, no prose, no code "
    "fence:\n" + REPLY_SCHEMA_LINE + "\n"
    "Laws: exactly one verb per tick; NOOP with a real reason is a GOOD "
    "tick; never invent estate state that is not in your senses source; "
    "no em-dash characters."
)

# The FREE-FORM variant: the hour's own reply schema (verb/reason/payload,
# no claims block). This is the shape in which the hour's brain fabricated
# (justification pressure: narrate starvation from a 2-row tail).
HOUR_REPLY_LINE = ('{"verb": "<one of the four>", "reason": "<why this verb '
                   'at this tick, max 40 words>", "payload": {...}}')

HOUR_LAW = (
    "Reply with EXACTLY one line, ONE JSON object, no prose, no code "
    "fence:\n" + HOUR_REPLY_LINE + "\n"
    "Laws: exactly one verb per tick; NOOP with a real reason is a GOOD "
    "tick when nothing needs routing; never invent estate state that is "
    "not in the senses; do not repeat the same alert message verbatim "
    "across ticks; no em-dash characters."
)


def bare_freeform_contract(q: str) -> str:
    p = PINNED[q]
    return (PREAMBLE + "TICK " + str(p["tick"]) + " of 40.\n\n"
            "SENSES (deterministic reads of the estate at this instant; "
            "trust ONLY these, never your memory of prior ticks):\n"
            + json.dumps(p["senses"], ensure_ascii=False) + "\n\n"
            + VERB_TABLE + "\n" + HOUR_LAW)


def tooled_freeform_contract(q: str) -> str:
    return (PREAMBLE + "TICK " + str(PINNED[q]["tick"]) + " of 40.\n\n"
            "TOOLING: you have ONE tool: get_state(surface). surface is one "
            "of beat, git, queue, landed. Calling it returns the pinned "
            "estate bytes for that surface as json. You have NO other "
            "source of estate state; any claim not in the returned bytes "
            "is fabrication and fails. You may call the tool AT MOST ONCE. "
            "To call it reply with exactly:\n"
            '{"tool_call": {"tool": "get_state", "surface": "beat"}}\n'
            "and nothing else; the system executes the call, returns the "
            "bytes, and then you answer.\n\n"
            + VERB_TABLE + "\n" + HOUR_LAW)

PREAMBLE = (
    "PILOT RE-RUN of one tick of the OVERMIND loop (the pacing signal of "
    "the Mag estate standing wave; you neither create nor delete; you route "
    "attention through ONE sanctioned verb per tick). "
)


def bare_contract(q: str) -> str:
    p = PINNED[q]
    return (PREAMBLE + "TICK " + str(p["tick"]) + " of 40.\n\n"
            "SENSES (deterministic reads of the estate at this instant; "
            "trust ONLY these, never your memory of prior ticks):\n"
            + json.dumps(p["senses"], ensure_ascii=False) + "\n\n"
            + VERB_TABLE + "\nQUESTION: " + QUESTIONS[q]["ask"]
            + "\nPut the question's fields in claims.\n\n" + REPLY_LAW)


def tooled_contract(q: str) -> str:
    return (PREAMBLE + "TICK " + str(PINNED[q]["tick"]) + " of 40.\n\n"
            "TOOLING: you have ONE tool: get_state(surface). surface is one "
            "of beat, git, queue, landed. Calling it returns the pinned "
            "estate bytes for that surface as json. You have NO other "
            "source of estate state; any claim not in the returned bytes "
            "is fabrication and fails. You may call the tool AT MOST ONCE. "
            "To call it reply with exactly:\n"
            '{"tool_call": {"tool": "get_state", "surface": "beat"}}\n'
            "and nothing else; the system executes the call, returns the "
            "bytes, and then you answer. If you answer without calling, "
            "every claim must still be byte-true.\n\n"
            + VERB_TABLE + "\nQUESTION: " + QUESTIONS[q]["ask"]
            + "\nPut the question's fields in claims.\n\n" + REPLY_LAW)


def stage(arm: str, q: str, rep: int, freeform: bool = False) -> Path:
    suffix = "f" if freeform else ""
    d = STAGE_ROOT / f"{arm}f-{q}-r{rep}" if freeform \
        else STAGE_ROOT / f"{arm}-{q}-r{rep}"
    d.mkdir(parents=True, exist_ok=True)
    if freeform:
        contract = (bare_freeform_contract(q) if arm == "bare"
                    else tooled_freeform_contract(q))
    else:
        contract = bare_contract(q) if arm == "bare" else tooled_contract(q)
    meta = {"id": f"capmx-{arm}{suffix}-{q}-r{rep}", "model": MODEL,
            "base_env": BASE_ENV, "base_url": BASE_URL,
            "contract": contract,
            "evidence": [], "self_contained": True}
    (d / "ask.json").write_text(
        json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    return d


def banked_spend() -> float:
    total = 0.0
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("id", "")).startswith("capmx-"):
                total += float(row.get("cost_usd") or 0.0)
    return total


def read_out(fire_id: str) -> tuple[str, str]:
    """Return (final_content, turn1_content) from the rail's output file."""
    p = model_garden.OUT_DIR / f"{fire_id}.md"
    if not p.is_file():
        return "", ""
    text = p.read_text(encoding="utf-8", errors="replace")
    marker = "\n\n---\n\n# REVISION (turn 2)\n\n"
    if marker in text:
        head, tail = text.split(marker, 1)
        return tail.strip(), head.split("\n\n", 1)[-1].strip()
    return text.split("\n\n", 1)[-1].strip(), text.split("\n\n", 1)[-1].strip()


def get_state(q: str, surface: str) -> dict | None:
    if surface not in SURFACES:
        return None
    return SURFACES[surface](PINNED[q]["senses"])


# ---------------- grading (mechanical, no judge model) ----------------

def _allowed_numbers(q: str, senses=None, extra=()) -> set[int]:
    blob = json.dumps(senses if senses is not None
                      else PINNED[q]["senses"], ensure_ascii=False)
    nums = {int(n) for n in re.findall(r"\b\d+\b", blob)}
    if senses is None:
        nums |= {v for v in QUESTIONS[q]["fields"].values()
                 if isinstance(v, int)}
        nums.add(PINNED[q]["tick"])
    nums |= set(extra)
    nums |= {40, 90, 0, 1, 2, 10, 2026}
    return nums


def _derived_from_present(n: int, allowed: set[int],
                          present: set[int]) -> bool:
    """A derived number is waived only when BOTH operands are themselves
    stated in the reason AND byte-true (pilot q3-r4: 76 with 38 and 50
    both present). The candidate itself is excluded from its own
    derivation (n+0=n would self-whitelist every word-number)."""
    ops = (present & allowed) - {n}
    for a in ops:
        for b in ops:
            if b and (n == round(a * 100 / b) or n == a + b
                      or n == abs(a - b)):
                return True
    return False


def _norm_path(tok: str) -> str:
    return tok.strip(".,;:!\"'()[]").replace("\\", "/")


def scan_reason(q: str, reason: str, senses: dict | None = None,
                extra=()) -> tuple[list[str], list[str]]:
    """Flag numbers and path-like tokens absent from the pinned bytes."""
    allowed = _allowed_numbers(q, senses, extra)
    blob = json.dumps(senses if senses is not None
                      else PINNED[q]["senses"],
                      ensure_ascii=False).replace("\\", "/")
    present = {int(m.group(0)) for m in re.finditer(r"\b\d{1,6}\b", reason)}
    present |= {WORD2NUM[w.lower()] for w in re.findall(r"[A-Za-z]+", reason)
                if w.lower() in WORD2NUM}
    num_flags, path_flags = [], []
    for m in re.finditer(r"\b\d{1,6}\b", reason):
        v = int(m.group(0))
        if v not in allowed and not _derived_from_present(v, allowed, present):
            num_flags.append(m.group(0))
    for w in re.findall(r"[A-Za-z]+", reason):
        low = w.lower()
        if low in WORD2NUM and low not in ("a",):
            if (WORD2NUM[low] not in allowed
                    and not _derived_from_present(WORD2NUM[low], allowed,
                                                  present)):
                num_flags.append(low + "->" + str(WORD2NUM[low]))
    estate_roots = ("watch/", "tools/", "mag/", "memory/", "corpus/",
                    "docs/", "scripts/", "state/", "queue/", "configs/",
                    "tests/", "model_garden/")
    for m in re.finditer(r"[^\s]+", reason):
        tok = _norm_path(m.group(0))
        fileish = "." in tok
        rooted = tok.startswith(estate_roots)
        if "/" in tok and (fileish or rooted):
            # segment rule, case-insensitive (merged vs MERGED in todo
            # bytes): clean when every segment is byte-present;
            # watch/inbox/salon_mine/ still flags because the salon_mine
            # segment is absent. Non-path slash compounds (ask/alert,
            # 01:17/01:19) are vocabulary, not estate claims.
            segs = [s for s in tok.split("/") if s]
            if not all(s.lower() in blob.lower() for s in segs):
                path_flags.append(tok)
        elif "/" not in tok and tok.endswith((".py", ".md", ".json",
                                              ".jsonl")):
            if tok.lower() not in blob.lower():
                path_flags.append(tok)
    return sorted(set(num_flags)), sorted(set(path_flags))


def grade_fire(arm: str, q: str, rep: int, final: str, turn1: str,
               tool_called: bool, surface_pulled, cost: float,
               freeform: bool = False) -> dict:
    spec = QUESTIONS[q]
    obj = parse_json_object(final)
    claims = (obj or {}).get("claims") if isinstance(obj, dict) else None
    reason = (obj or {}).get("reason", "") if isinstance(obj, dict) else final
    wrong, missing = [], []
    if not freeform:
        if isinstance(claims, dict) and claims:
            for k, truth in spec["fields"].items():
                got = claims.get(k)
                if got is None:
                    missing.append(k)
                    continue
                if isinstance(truth, list):
                    if not isinstance(got, list):
                        wrong.append(f"{k}:{got!r}!=list")
                    else:
                        got_n = sorted(str(x).replace("\\", "/").strip().rstrip("/")
                                       for x in got)
                        truth_n = sorted(str(x).rstrip("/") for x in truth)
                        if got_n != truth_n:
                            wrong.append(f"{k}:{got!r}!={truth!r}")
                elif isinstance(truth, int):
                    try:
                        if int(got) != truth:
                            wrong.append(f"{k}:{got}!={truth}")
                    except (TypeError, ValueError):
                        wrong.append(f"{k}:{got!r}!={truth}")
                elif str(got).strip() != str(truth):
                    wrong.append(f"{k}:{got!r}!={truth!r}")
        else:
            missing = list(spec["fields"])
    num_flags, path_flags = scan_reason(q, str(reason))
    fabricated = bool(wrong or num_flags or path_flags)
    return {"fire": f"capmx-{arm}-{q}-r{rep}", "arm": arm, "q": q, "rep": rep,
            "tick": PINNED[q]["tick"], "tool_called": tool_called,
            "surface_pulled": surface_pulled,
            "surface_needed": spec["need"],
            "surface_right": surface_pulled == spec["need"] if tool_called else None,
            "direct_answer": arm == "tooled" and not tool_called,
            "freeform": freeform,
            "parse_ok": obj is not None, "claims_missing": missing,
            "wrong_fields": wrong, "reason_num_flags": num_flags,
            "reason_path_flags": path_flags, "fabricated": fabricated,
            "cost_usd": round(cost, 6),
            "reason_excerpt": str(reason)[:200]}


def fire(arm: str, q: str, rep: int, execute: bool = True,
         freeform: bool = False) -> dict:
    d = stage(arm, q, rep, freeform)
    suffix = "f" if freeform else ""
    fire_id = f"capmx-{arm}{suffix}-{q}-r{rep}"
    if execute and banked_spend() > BUDGET_USD:
        return {"fire": fire_id, "skipped": "budget guard"}
    tool_called, surface_pulled, cost = False, None, 0.0
    row = model_garden.run_ask(d, execute=execute)
    cost += float(row.get("cost_usd") or 0.0)
    final, turn1 = read_out(fire_id)
    if arm == "tooled":
        call = parse_json_object(turn1)
        if isinstance(call, dict) and "tool_call" in call:
            tc = call["tool_call"]
            surface = tc.get("surface") if isinstance(tc, dict) else None
            tool_called, surface_pulled = True, surface
            result = get_state(q, str(surface))
            payload = (json.dumps(result, ensure_ascii=False)
                       if result is not None
                       else "ERROR: unknown surface (allowed: beat, git, "
                            "queue, landed)")
            (d / "revision.md").write_text(
                "TOOL RESULT for get_state(" + str(surface) + "):\n"
                + payload + "\n\nThis is the pinned estate truth for that "
                "surface. Produce your final answer JSON now (same schema "
                "as the contract). Do not call the tool again.",
                encoding="utf-8")
            meta = json.loads((d / "ask.json").read_text(encoding="utf-8"))
            meta["revision"] = True
            meta["turn2_only"] = True
            (d / "ask.json").write_text(
                json.dumps(meta, indent=1, ensure_ascii=False),
                encoding="utf-8")
            row2 = model_garden.run_ask(d, execute=execute)
            cost += float(row2.get("cost_usd") or 0.0)
            final, _ = read_out(fire_id)
    return grade_fire(arm, q, rep, final, turn1, tool_called,
                      surface_pulled, cost, freeform)


def grade_hour() -> list[dict]:
    """Mechanically grade the hour's own 40 brain reasons against each
    tick's own pinned snapshot: the true BARE FREE-FORM baseline (n=40,
    hash-chained, already banked by lane OVERMIND-2)."""
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    out = []
    for r in rows:
        if r.get("run_id") != "r20261002T010001Z-hour":
            continue
        q = "q1" if r["tick"] in (14,) else "q2" if r["tick"] in (16,) \
            else "q3"
        num_flags, path_flags = scan_reason(
            q, r.get("reason", ""), senses=r["senses"],
            extra=(r["tick"],))
        out.append({"fire": f"hour-t{r['tick']:03d}", "arm": "hour-bare",
                    "q": "tick" + str(r["tick"]), "rep": r["tick"],
                    "tick": r["tick"], "tool_called": False,
                    "surface_pulled": None, "freeform": True,
                    "parse_ok": True, "claims_missing": [],
                    "wrong_fields": [], "reason_num_flags": num_flags,
                    "reason_path_flags": path_flags,
                    "fabricated": bool(num_flags or path_flags),
                    "cost_usd": r.get("cost_usd", 0.0),
                    "reason_excerpt": r.get("reason", "")[:200]})
    return out


# The hour's 12 instrument-flagged ticks (7 hard fabrication + 5 window
# overflow) plus 3 clean controls: re-run them fresh, bare and tooled,
# free-form. Probing exactly where the disease fired.
DIRTY_TICKS = [2, 6, 8, 9, 10, 14, 16, 17, 18, 26, 30, 38]
CLEAN_CONTROLS = [1, 20, 33]


def pin_extra_ticks() -> None:
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    for tick in DIRTY_TICKS + CLEAN_CONTROLS:
        q = f"t{tick}"
        if q in PINNED:
            continue
        row = [r for r in rows if r.get("tick") == tick
               and r.get("run_id") == "r20261002T010001Z-hour"][0]
        PINNED[q] = {"tick": tick, "senses": row["senses"],
                     "brain_reason_then": row["reason"]}
        QUESTIONS[q] = {"need": None, "fields": {}, "ask": "",
                        "then": "dirty-tick re-run"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="capability_matrix_pilot")
    ap.add_argument("--stage-only", action="store_true",
                    help="stage asks + print contracts, no calls")
    ap.add_argument("--grade-only", action="store_true",
                    help="re-grade from landed outputs, no calls")
    ap.add_argument("--freeform", action="store_true",
                    help="run the hour-shaped variant (verb/reason/payload, "
                         "no claims block)")
    ap.add_argument("--grade-hour", action="store_true",
                    help="mechanically grade the hour's own 40 reasons "
                         "against their own snapshots")
    ap.add_argument("--dirty", action="store_true",
                    help="re-run the hour's 12 flagged ticks + 3 clean "
                         "controls fresh, bare and tooled, free-form")
    ap.add_argument("--verbatim", action="store_true",
                    help="bare-only: fire the hour's EXACT contract text "
                         "(tools/overmind_brain.render_contract verbatim) "
                         "on the 12 dirty ticks, closing the preamble "
                         "confounder")
    ap.add_argument("--reps", type=int, default=REPS)
    args = ap.parse_args(argv)
    GRADES.parent.mkdir(parents=True, exist_ok=True)
    grades = []
    if args.verbatim:
        from tools.overmind_brain import render_contract
        pin_extra_ticks()
        for tick in DIRTY_TICKS:
            q = f"t{tick}"
            d = STAGE_ROOT / f"barev-{q}-r1"
            d.mkdir(parents=True, exist_ok=True)
            meta = {"id": f"capmx-barev-{q}-r1", "model": MODEL,
                    "base_env": BASE_ENV, "base_url": BASE_URL,
                    "contract": render_contract(
                        tick, 40, "r20261002T010001Z-hour",
                        PINNED[q]["senses"]),
                    "evidence": [], "self_contained": True}
            (d / "ask.json").write_text(
                json.dumps(meta, indent=1, ensure_ascii=False),
                encoding="utf-8")
            if banked_spend() > BUDGET_USD:
                print("BUDGET GUARD TRIPPED")
                return 3
            row = model_garden.run_ask(d, execute=True)
            final, _ = read_out(f"capmx-barev-{q}-r1")
            g = grade_fire("barev", q, 1, final, final, False, None,
                           float(row.get("cost_usd") or 0.0), True)
            g["fire"] = f"capmx-barev-{q}-r1"
            grades.append(g)
            print(json.dumps({k: g[k] for k in (
                "fire", "reason_num_flags", "reason_path_flags",
                "fabricated", "cost_usd")}))
        with open(GRADES, "a", encoding="utf-8") as fh:
            for g in grades:
                fh.write(json.dumps(g, ensure_ascii=False) + "\n")
        fab = sum(1 for g in grades if g["fabricated"])
        print(f"ARM barev (hour contract verbatim): fires={len(grades)} "
              f"fabricated={fab} rate={fab / len(grades):.2f}")
        print(f"TOTAL SPENT (banked, capmx-*): ${banked_spend():.4f}")
        return 0
    if args.grade_hour:
        grades = grade_hour()
        for g in grades:
            print(json.dumps({k: g[k] for k in (
                "fire", "reason_num_flags", "reason_path_flags",
                "fabricated")}))
    else:
        pin_extra = args.dirty
        qs = ([f"t{t}" for t in DIRTY_TICKS + CLEAN_CONTROLS]
              if args.dirty else ("q1", "q2", "q3"))
        if pin_extra:
            pin_extra_ticks()
        reps = 1 if args.dirty else args.reps
        freeform = True if args.dirty else args.freeform
        for arm in ("bare", "tooled"):
            for q in qs:
                for rep in range(1, reps + 1):
                    if args.stage_only:
                        d = stage(arm, q, rep, freeform)
                        print(f"STAGED {d.name}")
                        continue
                    if args.grade_only:
                        suffix = "f" if freeform else ""
                        final, turn1 = read_out(
                            f"capmx-{arm}{suffix}-{q}-r{rep}")
                        call = parse_json_object(turn1)
                        tc = bool(isinstance(call, dict) and "tool_call" in call)
                        sp = (call["tool_call"].get("surface")
                              if tc and isinstance(call["tool_call"], dict)
                              else None)
                        g = grade_fire(arm, q, rep, final, turn1, tc, sp,
                                       0.0, freeform)
                    else:
                        if banked_spend() > BUDGET_USD:
                            print(f"BUDGET GUARD TRIPPED at ${banked_spend():.4f}")
                            return 3
                        g = fire(arm, q, rep, freeform=freeform)
                        if g.get("skipped"):
                            print(json.dumps(g))
                            continue
                    grades.append(g)
                    print(json.dumps({k: g[k] for k in (
                        "fire", "tool_called", "surface_pulled", "parse_ok",
                        "wrong_fields", "reason_num_flags",
                        "reason_path_flags", "fabricated", "cost_usd")}))
    if not args.stage_only:
        with open(GRADES, "a", encoding="utf-8") as fh:
            for g in grades:
                fh.write(json.dumps(g, ensure_ascii=False) + "\n")
        for arm in sorted({g["arm"] for g in grades}):
            rows = [g for g in grades if g["arm"] == arm]
            if not rows:
                continue
            fab = sum(1 for g in rows if g["fabricated"])
            graded = sum(1 for g in rows if g["parse_ok"] or g["reason_excerpt"])
            cost = sum(g["cost_usd"] for g in rows)
            if graded:
                print(f"ARM {arm}: fires={len(rows)} graded={graded} "
                      f"fabricated={fab} rate={fab / graded:.2f} "
                      f"cost=${cost:.4f}")
            else:
                print(f"ARM {arm}: no graded fires")
            if arm == "tooled":
                print(f"  tool_called={sum(1 for g in rows if g['tool_called'])}"
                      f"/{len(rows)} direct_answer="
                      f"{sum(1 for g in rows if g.get('direct_answer'))}"
                      f" surface_right="
                      f"{sum(1 for g in rows if g.get('surface_right'))}")
    print(f"TOTAL SPENT (banked, capmx-*): ${banked_spend():.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
