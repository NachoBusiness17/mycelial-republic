"""riddler_veil - the code-as-law organ for the Riddler Protocol.

Lessig's architecture modality, estate edition: the protocol card
(watch/inbox/riddler_protocol_20261012/CARD.md) is the norm; this tool is the
architecture that makes the norm self-enforcing. A parable that fails the veil
cannot land.

What it checks (mechanical, byte-backed, no vibes):
  1. NO-DOX: no term from the machine-local parties registry appears in the
     parable (word-boundary match, case-insensitive). The registry lives under
     state/riddler/ which is gitignored - the parties list itself never
     publishes.
  2. COPY-THROUGH: if source documents are supplied, no 8-gram (normalized) of
     the parable may appear in any source. Reusing the raw thread's own
     sentences is the classic leak; the transform must be a rewrite.
  3. SAME-STANDS (mechanical half): the parable must declare the stands it
     carries via a `stands:` header line, and every named stand must exist in
     state/riddler/stands.json. The semantic half (does the prose actually
     deliver the stand) is the consensus leg.

Truth grading: the verdict states its own grade. `--grade sensing` runs the
mechanical checks only and says so. `--grade certified` additionally requires a
banked consensus receipt (--consensus-file) from the funded tier certifying
(a) no re-identification and (b) stands recoverable; without one it fails loud.
A sensing-grade verdict is never allowed to print as certified.

Usage:
  python tools/riddler_veil.py init
  python tools/riddler_veil.py check --parable P.md [--sources S1 S2]
                                   [--grade sensing|certified]
                                   [--consensus-file F]
Exit 0 = VEIL-PASS, exit 2 = VEIL-FAIL, exit 3 = setup error.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RIDDLER_DIR = ROOT / "state" / "riddler"
PARTIES = RIDDLER_DIR / "parties.json"
STANDS = RIDDLER_DIR / "stands.json"

N = 8  # copy-through n-gram size


def _load(path: Path, kind: str) -> dict:
    if not path.is_file():
        raise SystemExit(f"setup error: {kind} missing at {path}; run `init` first (exit 3)")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"setup error: {kind} malformed: {exc} (exit 3)")


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower()).strip()


def _ngrams(text: str, n: int = N) -> set[str]:
    words = _norm(text).split()
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def _party_terms(parties: dict) -> list[tuple[str, str]]:
    terms: list[tuple[str, str]] = []
    for party in parties.get("parties", []):
        pid = party.get("id", "?")
        for field in ("names", "handles", "orgs"):
            for term in party.get(field, []):
                t = term.strip()
                if t:
                    terms.append((pid, t))
    return terms


def check_parable(parable_path: Path, source_paths: list[Path],
                  parties: dict, stands: dict) -> tuple[list[str], list[str]]:
    """Returns (violations, notes). Empty violations = mechanical pass."""
    violations: list[str] = []
    notes: list[str] = []
    text = parable_path.read_text(encoding="utf-8", errors="replace")

    # 1. NO-DOX scan
    for pid, term in _party_terms(parties):
        pattern = re.compile(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)",
                             re.IGNORECASE)
        if pattern.search(text):
            violations.append(f"NO-DOX: party term '{term}' (party {pid}) appears in parable")

    # 2. COPY-THROUGH scan
    if source_paths:
        parable_grams = _ngrams(text)
        for src in source_paths:
            if not src.is_file():
                notes.append(f"source missing, skipped: {src}")
                continue
            overlap = parable_grams & _ngrams(src.read_text(encoding="utf-8", errors="replace"))
            for gram in sorted(overlap)[:5]:
                violations.append(f"COPY-THROUGH: 8-gram from {src.name}: '{gram}'")
            if overlap:
                notes.append(f"{len(overlap)} overlapping 8-grams vs {src.name}")

    # 3. SAME-STANDS mechanical half
    m = re.search(r"(?im)^stands:\s*(.+)$", text)
    if not m:
        violations.append("SAME-STANDS: no 'stands:' header line declared")
    else:
        named = [s.strip() for s in m.group(1).split(",") if s.strip()]
        known = {s.get("id") for s in stands.get("stands", [])}
        if not named:
            violations.append("SAME-STANDS: empty stands declaration")
        for sid in named:
            if sid not in known:
                violations.append(f"SAME-STANDS: declared stand '{sid}' not in stands registry")
    return violations, notes


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] == "init":
        RIDDLER_DIR.mkdir(parents=True, exist_ok=True)
        if not PARTIES.is_file():
            PARTIES.write_text(json.dumps({
                "version": 1,
                "note": "machine-local only; state/ is gitignored; never commit",
                "parties": [],
            }, indent=1) + "\n", encoding="utf-8")
        if not STANDS.is_file():
            STANDS.write_text(json.dumps({
                "version": 1,
                "note": "stands a parable may declare; ids only here, text is public-safe",
                "stands": [],
            }, indent=1) + "\n", encoding="utf-8")
        print(f"riddler_veil: initialized {RIDDLER_DIR} (gitignored)")
        return 0

    grade = "sensing"
    parable: Path | None = None
    sources: list[Path] = []
    consensus_file: Path | None = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "check":
            pass
        elif a == "--parable":
            i += 1; parable = Path(argv[i])
        elif a == "--sources":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                sources.append(Path(argv[i])); i += 1
            continue
        elif a == "--grade":
            i += 1; grade = argv[i]
        elif a == "--consensus-file":
            i += 1; consensus_file = Path(argv[i])
        else:
            raise SystemExit(f"unknown arg: {a} (exit 3)")
        i += 1
    if parable is None:
        raise SystemExit("setup error: --parable required (exit 3)")
    if grade not in ("sensing", "certified"):
        raise SystemExit(f"setup error: grade must be sensing|certified, got {grade} (exit 3)")

    parties = _load(PARTIES, "parties registry")
    stands = _load(STANDS, "stands registry")
    violations, notes = check_parable(parable, sources, parties, stands)

    consensus_note = "not run (mechanical grade)"
    if grade == "certified":
        if consensus_file is None or not consensus_file.is_file():
            violations.append(
                "TRUTH: certified grade requires a banked consensus receipt (--consensus-file); "
                "funded-tier certification cannot be claimed from nothing")
        else:
            rows = [json.loads(l) for l in consensus_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            ok = [r for r in rows if r.get("ok_material")]
            consensus_note = f"consensus receipt banked: {len(ok)}/{len(rows)} rows material-ok"
            if not ok:
                violations.append("TRUTH: consensus receipt carries no material-ok rows")

    print(f"RIDDLER-VEIL: grade={grade} parable={parable.name} "
          f"violations={len(violations)} notes={len(notes)} consensus={consensus_note}")
    for v in violations:
        print(f"  FAIL {v}")
    for n in notes:
        print(f"  note {n}")
    if violations:
        print("VERDICT: VEIL-FAIL")
        return 2
    print("VERDICT: VEIL-PASS"
          + ("" if grade == "certified" else " (sensing grade: mechanical checks only)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
