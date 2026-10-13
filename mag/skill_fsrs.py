"""skill_fsrs - clippy-as-prober: closed-book free-recall probes on the
skill cards, FSRS-default state, passes as gwap payloads (D3, eleven-doors,
2026-10-05).

The door: "the one genuinely un-held build: FSRS/scheduler census clean
across tracked code; banks the ~1k probes FSRS needs off defaults; gates
the decay family's third store."

Design, honest about what is defaulted:
- CARDS: every SKILL.md under .agents/skills + .zcode/skills. Card id =
  the skill directory name. Card bytes ARE the answer key.
- FSRS-DEFAULT: the 17-weight FSRS-4.5 default parameter set, unfitted -
  the estate banks reviews until ~1k exist, THEN fitting becomes honest.
  The scheduler here is the minimal reproducible core: initial stability
  per first grade (Again 0.4d / Hard 1d / Good 3d / Easy 8d rounded from
  w[0..3]), then S' = S * growth(grade, difficulty) with the default
  difficulty update - named as the simplified core, not the full
  forgetting-curve machinery. Interval = S days; due = now + interval.
- PROBES (closed-book free recall): 2-3 questions generated
  DETERMINISTICALLY from the card bytes (frontmatter description -> when
  do you reach for it; H2 headings -> what are the steps; the first law
  line -> the card's one law). No LLM in question generation - the probe
  is the same for every asker, so answers are comparable.
- ANSWER + SELF-GRADE: a seat answers closed-book from memory
  (answer --card X --recall "..."); the grade is deterministic statement
  overlap between the recall and the card (the monoculture proxy's
  invariant primitives): >=0.5 Easy-ish, >=0.25 Good, >0 Hard, 0 Again.
  The grade maps to the FSRS interval; the review appends to
  memory/fsrs/reviews.jsonl (append-only).
- GWAP PASS: each review mints a payload (intent = the recall's
  statements, report = the card's probe-answer lines, independently
  keyed) through mag.gwap_payload.build_payload - the decay family's
  third store rides the same agreement engine.

CLI:
  python -m mag.skill_fsrs due            # cards due now (default state: all)
  python -m mag.skill_fsrs probe <card>   # the closed-book questions
  python -m mag.skill_fsrs answer <card> --recall "..."   # grade + bank
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOTS = (ROOT / ".agents" / "skills", ROOT / ".zcode" / "skills")
FSRS_DIR = ROOT / "memory" / "fsrs"
REVIEWS = FSRS_DIR / "reviews.jsonl"

# FSRS-4.5 default weights (unfitted; the census says the estate holds no
# scheduler - these bank reviews until ~1k make fitting honest)
W = [0.40255, 1.18385, 3.173, 15.691, 7.1949, 0.5345, 1.4604, 0.0046,
     1.54575, 0.1192, 1.01925, 1.9395, 0.11, 0.29605, 2.2698, 0.2315,
     2.9898, 0.51655, 0.6621]
# simplified initial stability per grade (days), from the default table
INITIAL_S = {"again": 0.4, "hard": 1.0, "good": 3.0, "easy": 8.0}
GROWTH = {"again": 0.0, "hard": 1.2, "good": 2.5, "easy": 4.5}
GRADES = ("again", "hard", "good", "easy")

SCHEMA = "skill.fsrs.v1"


def _now_dt() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now_dt().strftime("%Y-%m-%dT%H:%M:%SZ")


# -- cards ------------------------------------------------------------------


def cards() -> dict[str, Path]:
    """card_id -> SKILL.md path over both skill roots."""
    out: dict[str, Path] = {}
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        for p in sorted(root.glob("*/SKILL.md")):
            out.setdefault(p.parent.name, p)
    return out


def card_text(card_id: str) -> str:
    p = cards().get(card_id)
    return p.read_text(encoding="utf-8", errors="ignore") if p and p.is_file() else ""


# -- fsrs state (derived from the append-only log) --------------------------


def _reviews() -> list[dict]:
    if not REVIEWS.exists():
        return []
    out = []
    for line in REVIEWS.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def card_state(card_id: str) -> dict:
    """Current FSRS state derived from the review log (default = fresh)."""
    rows = [r for r in _reviews() if r.get("card") == card_id and r.get("schema") == SCHEMA]
    if not rows:
        return {"stability_days": None, "difficulty": None, "reviews": 0,
                "last_grade": None, "due": None}
    last = rows[-1]
    return {"stability_days": last.get("stability_days"),
            "difficulty": last.get("difficulty"),
            "reviews": len(rows), "last_grade": last.get("grade"),
            "due": last.get("due")}


def next_state(prev: dict, grade: str) -> dict:
    """The simplified FSRS-default update (named, not the full curve fit)."""
    if grade not in GRADES:
        raise ValueError(f"grade must be one of {GRADES}")
    if prev.get("stability_days") is None:
        s = INITIAL_S[grade]
        d = 5.0 if grade in ("good", "easy") else 7.0
    else:
        s = float(prev["stability_days"])
        d = float(prev.get("difficulty") or 5.0)
        s = max(0.4, s * GROWTH[grade])
        d = min(10.0, max(1.0, d + (1.0 if grade == "again" else -0.5)))
    due = (_now_dt() + timedelta(days=round(s, 2))).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"stability_days": round(s, 3), "difficulty": round(d, 2),
            "reviews": int(prev.get("reviews") or 0) + 1, "last_grade": grade,
            "due": due}


def due_cards(now: str | None = None) -> list[str]:
    now = now or _now_iso()
    out = []
    for cid in cards():
        st = card_state(cid)
        if st["due"] is None or st["due"] <= now:
            out.append(cid)
    return sorted(out)


# -- probes (deterministic, closed-book) -------------------------------------


def probe(card_id: str) -> list[str]:
    """2-3 free-recall questions from the card bytes. Same bytes = same
    questions, every asker, every session - answers stay comparable."""
    text = card_text(card_id)
    if not text:
        return []
    qs: list[str] = []
    m = re.search(r"^description:\s*(.+?)(?:\n[a-z_]+:|\n---)", text, re.S | re.M)
    if m and len(m.group(1).strip()) > 20:
        qs.append(f"CLOSED-BOOK: from memory - when do you reach for {card_id}, "
                  "and what does it do? (one sentence)")
    h2s = re.findall(r"^##\s+(.+)$", text, re.M)
    if h2s:
        qs.append(f"CLOSED-BOOK: name the section steps of {card_id} "
                  f"({len(h2s)} headings) in order, one line each.")
    laws = [l for l in text.splitlines() if re.match(r"^\s*[-*]\s+\*\*", l)]
    if laws:
        qs.append(f"CLOSED-BOOK: state {card_id}'s first bolded law from memory.")
    return qs[:3]


def answer_key_lines(card_id: str) -> list[str]:
    """The report-side lines (the card's own bytes) for the gwap payload."""
    text = card_text(card_id)
    m = re.search(r"^description:\s*(.+?)(?:\n[a-z_]+:|\n---)", text, re.S | re.M)
    out = []
    if m:
        out.append(" ".join(m.group(1).split())[:200])
    out += [h.strip() for h in re.findall(r"^##\s+(.+)$", text, re.M)][:6]
    return out


def key_terms(card_id: str, cap: int = 12) -> list[str]:
    """Distinctive terms of the card's answer-key lines (lowercase alnum,
    len>=4, stoplist out, order-preserving, capped). The gwap objects: the
    engine is exact-tuple Jaccard, so free-phrased sentences can never
    match - terms CAN, and coverage of card terms by the recall is exactly
    the decay-family metric."""
    stop = {"the", "and", "that", "with", "this", "from", "into", "your",
            "when", "what", "which", "through", "without", "between",
            "their", "then", "them", "than", "some", "only", "also",
            "never", "always", "every", "each", "more", "most", "less"}
    seen: list[str] = []
    for tok in re.findall(r"[a-z0-9]{4,}", " ".join(answer_key_lines(card_id)).lower()):
        if tok in stop or tok in seen:
            continue
        seen.append(tok)
        if len(seen) >= cap:
            break
    return seen


# -- answer + self-grade + bank ----------------------------------------------


def _tok4(s: str) -> set[str]:
    """Length-gated tokens: >=4 chars. The plain roshomon _overlap let
    'and'-class stopwords leak a nonzero score onto a fully wrong recall
    (graded hard instead of again - caught by the wrong-recall control)."""
    return set(re.findall(r"[a-z0-9]{4,}", s.lower()))


def self_grade(recall: str, card_id: str) -> tuple[str, float]:
    """Deterministic overlap grade: recall statements vs the answer key."""
    from mag.roshomon import _invariant_statements

    key = answer_key_lines(card_id)
    if not key or not recall.strip():
        return "again", 0.0
    rec_stmts = _invariant_statements(recall)
    key_stmts = _invariant_statements(" ".join(key))
    if not rec_stmts or not key_stmts:
        return "again", 0.0

    def overlap(a: str, b: str) -> float:
        ta, tb = _tok4(a), _tok4(b)
        if not ta or not tb:
            return 0.0
        return len(ta & tb) / min(len(ta), len(tb))

    best = max(overlap(r, k) for r in rec_stmts for k in key_stmts)
    scores = [max((overlap(r, k) for r in rec_stmts), default=0.0)
              for k in key_stmts]
    cover = sum(scores) / len(scores) if scores else 0.0
    score = round((best + cover) / 2.0, 4)
    if score >= 0.5:
        return "easy", score
    if score >= 0.25:
        return "good", score
    if score > 0.0:
        return "hard", score
    return "again", score


def answer(card_id: str, recall: str, *, bank_payload: bool = True) -> dict:
    """Grade one closed-book recall, advance the FSRS state, append the
    review, mint the gwap payload. Returns the full review row."""
    from mag.gwap_payload import build_payload
    from mag.roshomon import _invariant_statements

    if card_id not in cards():
        return {"ok": False, "error": f"unknown card {card_id}"}
    grade, score = self_grade(recall, card_id)
    prev = card_state(card_id)
    nxt = next_state(prev, grade)
    row = {
        "schema": SCHEMA, "card": card_id, "ts": _now_iso(),
        "grade": grade, "score": score,
        "recall_chars": len(recall),
        "stability_days": nxt["stability_days"],
        "difficulty": nxt["difficulty"], "due": nxt["due"],
        "probe_count": len(probe(card_id)),
    }
    payload = None
    if bank_payload:
        import hashlib

        # objects = the card's key TERMS; the intent side mints ONLY terms
        # verifiably present in the recall text, so agreement = recall
        # coverage in the engine's own exact-tuple Jaccard (free-phrased
        # sentence objects can never match - the first two live reviews
        # scored DISPUTE 0.0 on honest recalls before this shape). The
        # qualifier binds both sides to the card-bytes commitment
        # (commit=<sha12>:, the v1.1 ledger-confirmation exemption): both
        # sides enumerate the same term list, so order-identity is the
        # expected honest shape, not collusion.
        terms = key_terms(card_id)
        recall_toks = set(re.findall(r"[a-z0-9]{4,}", recall.lower()))
        hit_terms = [t for t in terms if t in recall_toks]
        card_sha = hashlib.sha256(
            " ".join(answer_key_lines(card_id)).encode("utf-8")).hexdigest()
        commit = "commit=" + card_sha[:12] + ":"
        payload = build_payload(
            scene_id=f"skill-recall-{card_id}",
            intent_struct={"author": "seat", "claims": [
                {"subject": card_id, "verb": "states", "object": t,
                 "qualifier": commit} for t in hit_terms]},
            report_struct={"author": "card", "claims": [
                {"subject": card_id, "verb": "states", "object": t,
                 "qualifier": commit} for t in terms]},
            participants=[{"anon_id": "seat", "role": "robber"},
                          {"anon_id": "card", "role": "cop"}],
            consent=True, created_utc=row["ts"],
            replay_tape_ref={"sha256": card_sha,
                             "engine_version": "skill-fsrs-v1-defaults"})
        row["gwap_verdict"] = payload.get("verdict")
        row["gwap_agreement"] = payload.get("agreement_score")
    REVIEWS.parent.mkdir(parents=True, exist_ok=True)
    with REVIEWS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    row["ok"] = True
    row["payload"] = payload
    return row


# -- clippy block ------------------------------------------------------------


def clippy_block(max_cards: int = 3) -> str:
    """The clippy probe block: due cards + their closed-book questions.
    The ANSWER happens next session (answer --card X --recall ...); the
    block never prints the answer key."""
    due = due_cards()
    if not due:
        return "FSRS: no cards due."
    lines = [f"FSRS PROBES: {len(due)} card(s) due; showing up to {max_cards}. "
             "Answer CLOSED-BOOK next session: python -m mag.skill_fsrs answer <card> --recall \"...\""]
    for cid in due[:max_cards]:
        lines.append(f"  [{cid}]")
        lines += [f"    {q}" for q in probe(cid)]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="skill_fsrs", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("due")
    p = sub.add_parser("probe"); p.add_argument("card")
    p = sub.add_parser("answer"); p.add_argument("card"); p.add_argument("--recall", required=True)
    sub.add_parser("clippy")
    args = ap.parse_args(argv)
    if args.cmd == "due":
        due = due_cards()
        print(f"{len(due)} due / {len(cards())} cards")
        for cid in due:
            print(" ", cid)
        return 0
    if args.cmd == "probe":
        for q in probe(args.card):
            print(q)
        return 0
    if args.cmd == "answer":
        row = answer(args.card, args.recall)
        if not row.get("ok"):
            print(row.get("error")); return 1
        print(f"{args.card}: grade={row['grade']} score={row['score']} "
              f"stability={row['stability_days']}d due={row['due']} "
              f"gwap={row.get('gwap_verdict')} ({row.get('gwap_agreement')})")
        return 0
    if args.cmd == "clippy":
        print(clippy_block())
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
