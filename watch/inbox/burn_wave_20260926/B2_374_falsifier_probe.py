"""B2-374 falsifier probe: the behavioral-events scout emission disease.

Run twice with the repo venv from the repo root:
  .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_374_falsifier_probe.py

PRE-fix (old emission): the digest fixture row quotes "tool_fail=12
collapse=3" in its detail; the scout row's detail prints those phantom
census-shaped tokens for kinds the census never counted, and one
non-dict JSON row silently drops the WHOLE behavioral row via the outer
except. POST-fix: the detail splits on " samples: ", the census section
carries exactly the counted kinds, the quoted literals live only in the
samples section, and the non-dict row is skipped while the real rows
survive. Also cross-checks the live logs/behavioral_events.jsonl tail
census against the old inline arithmetic (equality expected: the field
rule is unchanged; only the emission and the non-dict guard moved).

Constants import from tests/test_improve_behavioral_scout.py so probe
and pins cannot drift (the B2-357 probe pattern).
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tests"))

import mag.improve as improve_mod  # noqa: E402
import test_improve_behavioral_scout as pins  # noqa: E402


def behavioral_row(rows):
    return [r for r in rows if r.get("claim", "").startswith("Behavioral events log:")]


def drive(jsonl_text: str):
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        log_dir = tmp / "logs"
        log_dir.mkdir()
        (log_dir / "behavioral_events.jsonl").write_text(jsonl_text, encoding="utf-8")
        saved = improve_mod.ROOT
        improve_mod.ROOT = tmp
        try:
            return behavioral_row(improve_mod._behavioral_candidates("2026-09-26"))
        finally:
            improve_mod.ROOT = saved


def main() -> int:
    verdict = "HOLDS"
    has_census = hasattr(improve_mod, "behavioral_events_census")
    print(f"census function present: {has_census}")

    print("\n== arm 1: digest fixture row quoting counted kind literals ==")
    rows = drive(pins.QUOTED_DIGEST_ROW)
    assert len(rows) == 1, f"expected 1 behavioral row, got {len(rows)}"
    detail = rows[0]["detail"]
    print("claim:", rows[0]["claim"])
    print("detail:", detail)
    if " samples: " in detail:
        census_section = detail.split(" samples: ")[0]
        phantom_in_census = "tool_fail=12" in census_section or "collapse=3" in census_section
        print(f"phantom tokens in census section: {phantom_in_census}")
        if phantom_in_census:
            verdict = "DIES"
    else:
        phantom_everywhere = "tool_fail=12" in detail
        print(f"no samples marker (old emission); phantom token in detail: {phantom_everywhere}")
        if not phantom_everywhere:
            print("UNEXPECTED: old emission should carry the phantom token")
            verdict = "DIES"

    print("\n== arm 2: non-dict JSON row survival ==")
    rows = drive(pins.TOOL_FAIL_ROW + pins.NONDICT_ROW + pins.COLLAPSE_ROW)
    print(f"behavioral rows emitted: {len(rows)}")
    if rows:
        print("claim:", rows[0]["claim"])

    if has_census:
        print("\n== arm 3: live tail census vs old arithmetic ==")
        live = REPO / "logs" / "behavioral_events.jsonl"
        text = live.read_text(encoding="utf-8", errors="replace")
        tail = text.splitlines()[-80:]
        # old arithmetic, verbatim shape of the pre-B2-374 scout block
        old_kinds = {}
        old_dropped_block = False
        for line in tail:
            if not line.strip():
                continue
            try:
                ev = __import__("json").loads(line)
            except Exception:
                continue
            try:
                k = str(ev.get("kind") or "event")
            except AttributeError:
                old_dropped_block = True
                break
            old_kinds[k] = old_kinds.get(k, 0) + 1
        census = improve_mod.behavioral_events_census(text)
        print(f"live tail lines: {len(tail)}")
        print(f"old arithmetic events: {sum(old_kinds.values())} (block aborted: {old_dropped_block})")
        print(f"census events: {census['events']} kinds: {census['kinds']}")
        if old_dropped_block or census["events"] != sum(old_kinds.values()) or census["kinds"] != old_kinds:
            verdict = "DIES"
    else:
        print("\n== arm 3 skipped: census function absent (pre-fix run) ==")

    print(f"\nVERDICT {verdict}")
    return 0 if verdict == "HOLDS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
