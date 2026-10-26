"""Claim drift patrol tests (GENETIC BURN G1 lane i03-patrol-tests, 2026-10-18).

*** BINDS I02 INTERFACE *** (TDD-first: this battery is the executable spec for
tools/claim_drift_patrol.py, which sibling lane i02 builds in this same volley;
design source lanes/g06-patrol-design.md sections 1-6, test plan
lanes/g17-tests-map.md Organ 1). Until i02 lands, the module import below
soft-skips the whole file so the ledger never gains a collection error; once
it lands, every test binds. The bound surface, exactly as g06 designs it:

  import tools.claim_drift_patrol as cdp   (module import, never from-import:
    the tests/test_census_drift_patrol.py:32-36 law)
  cdp.PatrolError            cannot-verify exception; main() maps it to exit 2
  cdp.load_ledger(path: Path) -> list[dict]
                             raises PatrolError naming "<ledger path>:<N>" with
                             a 1-based line number on every fail-closed case
                             (g06 section 1 load laws)
  cdp.claim_patrol(moment: date, today: date, stale_days: int,
                   carrier_touched: bool, text_differs: bool)
                             -> {"ok", "verdict", "exit", "reason", ...}; the
                             tier-1 pure verdict core (g06 section 3)
  cdp.verify_patrol(claimed, real, value_kind="int", tolerance=20)
                             -> same dict shape; the tier-2 pure verdict core
                             (g06 section 3 tier 2)
  cdp.fingerprint(rule: str, claim_id: str, detail: str) -> str
                             sha256(f"{rule}\0{id}\0{detail}")[:16] (g06 section 4)
  cdp.main(argv: list[str]) -> int

CLI contract, exercised through real subprocesses on synthetic tmp estates:
  python tools/claim_drift_patrol.py [--root PATH] [--ledger PATH]
      (--check default | --collect | --baseline-update --by WHO [--note NOTE]
       | --prune) [--id ID ...] [--stale-days N] [--baseline PATH]
      [--collect-tolerance N]

B2-338 corrigenda (founding-bytes gate): the commissioning prompt paraphrased
the first-line law as "a green run's stdout starts 'claim_drift_patrol: ok'";
the founding bytes disagree. g06 section 3 pins the exact green prefix
"CLAIM-PATROL: ok" and g17 Organ 1 row 8 pins "the exact bytes CLAIM-PATROL:
ok", both following the ancestor convention (CENSUS-PATROL: ok, CITATION-LINT:
ok). This battery binds the genes, not the paraphrase.

Frozen-vector law (B2-274 carried over): every fixture is a synthetic tmp
ledger plus a synthetic tmp carrier; no test reads or writes the live
watch/claims.jsonl, the live AGENTS.md census bullet, or
configs/claim_drift_baseline.json. Baseline tests always pass --baseline
pointing into tmp_path so the default-baseline lookup can never touch the
live repo even if a real baseline file appears there mid-volley.

Exit ladder under test (g06 section 5, verbatim):
  0 = every checked row green; first line starts "CLAIM-PATROL: ok"
  1 = STALE or CONTRADICTED on at least one row (hook WARN arm)
  2 = cannot verify: missing/malformed ledger, bad row, duplicate id, regex
      non-match (carrier reworded past its frozen grammar), regex compile
      failure, future moment, missing carrier, verifier crash/timeout/
      unparsable, git failure, unknown --id. Fail-closed, never a guess;
      blind differs from stale (B2-277) and every exit-2 path names the row
      id (g06 falsifier F4).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

cdp = pytest.importorskip(
    "tools.claim_drift_patrol",
    reason="tools/claim_drift_patrol.py not landed yet "
           "(sibling lane i02 builds it in this volley; binds i02 interface)",
)

TOOL = Path(__file__).resolve().parents[1] / "tools" / "claim_drift_patrol.py"
REPO = TOOL.parents[1]

WINFLAGS = (
    {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)}
    if sys.platform == "win32"
    else {}
)

# The g06 section 1 seed row's frozen claim grammar, byte-identical to the
# ancestor CENSUS_CLAIM_RE (tools/census_drift_patrol.py:117-119). Frozen
# vector: update only with a named receipt (B2-274).
CENSUS_CLAIM_SRC = (
    r"(\d[\d,]*)\s+tests\b(?:\s+collected)?\s*/\s*(\d[\d,]*)\s+files\b"
    r"\s*\(\s*(\d{4}-\d{2}-\d{2})\s+census\b"
)

CLAIM_PATROL_OK_PREFIX = "CLAIM-PATROL: ok"  # the B2-338 hook case-arm bytes


# --- fixtures and estate builders --------------------------------------------

def _git_init_and_commit(root: Path, message: str = "init") -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True,
                   **WINFLAGS)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True,
                   **WINFLAGS)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com",
         "commit", "-q", "-m", message],
        cwd=root, check=True, capture_output=True, **WINFLAGS,
    )


def _carrier_line(collected: str = "22", files: str = "3", day: str | None = None) -> str:
    day = day or date.today().isoformat()
    return (f"- **Tests:** {collected} tests collected / {files} files ({day} census, "
            f"`pytest --collect-only -q`). Trust bytes, not reports.")


def _matched_claim(text: str) -> str:
    m = re.search(CENSUS_CLAIM_SRC, text)
    assert m is not None, "fixture carrier line must match the frozen grammar"
    return m.group(0)


def _row_and_line(day: str | None = None, collected: str = "22", files: str = "3",
                  **over) -> tuple[dict, str]:
    """A default ledger row plus the carrier line it was registered against.

    moment and the carrier's census day move together (the g06 refresh
    protocol: carrier and row move in the same commit), so a fresh row with
    a today commit is green by the strictly-after rule.
    """
    day = day or date.today().isoformat()
    line = _carrier_line(collected=collected, files=files, day=day)
    row = {
        "id": "census-headline",
        "claim_text": _matched_claim(line),
        "carrier_path": "AGENTS.md",
        "claim_regex": CENSUS_CLAIM_SRC,
        "claim_group": 1,
        "moment": day,
        "owner": "mag-census-patrol",
        "verifier": [sys.executable, "-c", f"print({collected.replace(',', '')})"],
        "value_kind": "int",
        "tolerance": 20,
        "stale_days": 7,
        "receipt": "memory/runs/genetic_burn/20261018/G1/lanes/i03-patrol-tests.md",
    }
    row.update(over)
    return row, line


def _write_estate(root: Path, rows: list[dict], carrier_text: str | None,
                  commit: bool = True) -> Path:
    (root / "watch").mkdir(parents=True, exist_ok=True)
    ledger = root / "watch" / "claims.jsonl"
    ledger.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
    )
    if carrier_text is not None:
        (root / "AGENTS.md").write_text(carrier_text + "\n", encoding="utf-8")
    if commit:
        _git_init_and_commit(root)
    return ledger


def _empty_baseline(root: Path) -> Path:
    bl = root / "baseline.json"
    bl.write_text(json.dumps({"version": 1, "updated": None, "accepted": {}}),
                  encoding="utf-8")
    return bl


def _run(root: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root), *flags],
        capture_output=True, text=True, timeout=120, **WINFLAGS,
    )


# ===========================================================================
# BAND 1: fail-closed (B2-277) - ledger load laws and the exit-2 band, first
# per the mission and per g17 NEXT TASK ("TDD-first: ledger load fail-closed
# band before any patrol code exists").
# ===========================================================================

def _raw_ledger(tmp_path: Path, text: str) -> Path:
    (tmp_path / "watch").mkdir(parents=True, exist_ok=True)
    ledger = tmp_path / "watch" / "claims.jsonl"
    ledger.write_text(text, encoding="utf-8")
    return ledger


def test_load_malformed_json_line_naming_ledger_line(tmp_path):
    # g06 section 1: malformed JSON on any line is exit 2 naming
    # "watch/claims.jsonl:N", 1-based. A silently skipped row is the 12-day
    # fossil in miniature - never skip.
    row, _ = _row_and_line()
    ledger = _raw_ledger(tmp_path, json.dumps(row) + "\n{not json\n")
    with pytest.raises(cdp.PatrolError) as ei:
        cdp.load_ledger(ledger)
    assert "claims.jsonl:2" in str(ei.value)


def test_load_missing_required_key_is_patrol_error(tmp_path):
    row, _ = _row_and_line()
    del row["owner"]  # owner is a required key: no receipt-no-row law's sibling
    ledger = _raw_ledger(tmp_path, json.dumps(row) + "\n")
    with pytest.raises(cdp.PatrolError) as ei:
        cdp.load_ledger(ledger)
    assert "claims.jsonl" in str(ei.value)


def test_load_noncompiling_regex_is_patrol_error(tmp_path):
    row, _ = _row_and_line(claim_regex="(unbalanced")
    ledger = _raw_ledger(tmp_path, json.dumps(row) + "\n")
    with pytest.raises(cdp.PatrolError):
        cdp.load_ledger(ledger)


def test_load_duplicate_id_is_patrol_error(tmp_path):
    # g06 section 1: first row wins is not enough - a later duplicate id
    # poisons baselines, so it is exit 2, not a silent dedupe.
    row_a, _ = _row_and_line()
    row_b, _ = _row_and_line(day="2026-09-01")
    ledger = _raw_ledger(tmp_path, json.dumps(row_a) + "\n" + json.dumps(row_b) + "\n")
    with pytest.raises(cdp.PatrolError):
        cdp.load_ledger(ledger)


def test_load_unparseable_moment_is_patrol_error(tmp_path):
    row, _ = _row_and_line(moment="not-a-date")
    ledger = _raw_ledger(tmp_path, json.dumps(row) + "\n")
    with pytest.raises(cdp.PatrolError):
        cdp.load_ledger(ledger)


def test_load_valid_ledger_returns_rows_in_order(tmp_path):
    row_a, _ = _row_and_line()
    row_b, _ = _row_and_line(day="2026-09-01")
    row_b["id"] = "seats-worker"
    ledger = _raw_ledger(tmp_path, json.dumps(row_a) + "\n" + json.dumps(row_b) + "\n")
    rows = cdp.load_ledger(ledger)
    assert isinstance(rows, list) and len(rows) == 2
    assert [r["id"] for r in rows] == ["census-headline", "seats-worker"]
    assert rows[0]["claim_text"] == row_a["claim_text"]


def test_cli_missing_ledger_exits_2(tmp_path):
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert "ledger" in out.stdout


def test_cli_malformed_row_exits_2_naming_line(tmp_path):
    row, line = _row_and_line()
    _write_estate(tmp_path, [], line, commit=False)
    ledger = tmp_path / "watch" / "claims.jsonl"
    ledger.write_text(json.dumps(row) + "\n{not json\n", encoding="utf-8")
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert "claims.jsonl:2" in out.stdout


def test_cli_duplicate_id_exits_2(tmp_path):
    row_a, line = _row_and_line()
    row_b, _ = _row_and_line(day="2026-09-01")
    _write_estate(tmp_path, [row_a, row_b], line, commit=False)
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr


def test_cli_future_moment_exits_2(tmp_path):
    # Freshness-gate convention: a moment in the future is a fabrication
    # smell, cannot-verify, never a pass.
    row, line = _row_and_line(day="2999-01-01")
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert "future" in out.stdout


def test_cli_missing_carrier_exits_2_naming_row(tmp_path):
    # g06 falsifier F4: an exit-2 path must name the row id; blind without
    # evidence is the B2-277 disease.
    row, _ = _row_and_line()
    row["carrier_path"] = "GHOST.md"
    _write_estate(tmp_path, [row], None, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert "GHOST.md" in out.stdout
    assert row["id"] in out.stdout


def test_cli_regex_nonmatch_is_blind_exit_2(tmp_path):
    # The carrier was reworded past its frozen grammar: BLIND, and blind
    # differs from stale (B2-277). Exit 2 naming the row, never exit 0.
    row, _ = _row_and_line(day="2026-09-01")
    reworded = "- **Tests:** the big suite, trust bytes.\n"
    _write_estate(tmp_path, [row], reworded, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert row["id"] in out.stdout


def test_cli_unknown_id_exits_2(tmp_path):
    row, line = _row_and_line()
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--id", "no-such-claim")
    assert out.returncode == 2, out.stdout + out.stderr


# ===========================================================================
# BAND 2: STALE math on the pure tier-1 verdict core (g06 section 3 verdicts;
# the two-signal shape of the ancestor patrol()).
# ===========================================================================

def test_age_at_bar_with_a_signal_passes():
    # Boundary: STALE needs age strictly beyond the bar (ancestor
    # test_boundary_age_at_bar_passes_with_growth shape).
    v = cdp.claim_patrol(moment=date.today() - timedelta(days=7), today=date.today(),
                         stale_days=7, carrier_touched=True, text_differs=False)
    assert v["ok"] is True
    assert v["exit"] == 0


def test_age_bar_plus_one_with_touch_is_stale_exit_1():
    v = cdp.claim_patrol(moment=date.today() - timedelta(days=8), today=date.today(),
                         stale_days=7, carrier_touched=True, text_differs=False)
    assert v["verdict"] == "STALE"
    assert v["exit"] == 1


def test_age_bar_plus_one_without_signals_is_ok():
    # Age alone is not the disease: the world must have moved under the
    # claim (the snapshot-tolerance doctrine).
    v = cdp.claim_patrol(moment=date.today() - timedelta(days=8), today=date.today(),
                         stale_days=7, carrier_touched=False, text_differs=False)
    assert v["ok"] is True
    assert v["exit"] == 0


def test_text_differs_alone_is_stale():
    # text_differs is the only DISK-provable drift direction; it needs no
    # git signal to convict an over-bar claim.
    v = cdp.claim_patrol(moment=date.today() - timedelta(days=8), today=date.today(),
                         stale_days=7, carrier_touched=False, text_differs=True)
    assert v["verdict"] == "STALE"
    assert v["exit"] == 1


def test_per_row_stale_days_is_honored():
    v = cdp.claim_patrol(moment=date.today() - timedelta(days=6), today=date.today(),
                         stale_days=5, carrier_touched=True, text_differs=False)
    assert v["verdict"] == "STALE"
    assert v["exit"] == 1


def test_future_moment_is_unverifiable_exit_2():
    v = cdp.claim_patrol(moment=date.today() + timedelta(days=1), today=date.today(),
                         stale_days=7, carrier_touched=False, text_differs=False)
    assert v["verdict"] == "UNVERIFIABLE"
    assert v["exit"] == 2


def test_stale_reason_names_age_and_bar():
    v = cdp.claim_patrol(moment=date.today() - timedelta(days=8), today=date.today(),
                         stale_days=7, carrier_touched=True, text_differs=False)
    assert "8" in v["reason"]
    assert "7" in v["reason"]


# ===========================================================================
# BAND 3: B2-338 first-line law - the FIRST output line is the contract the
# hook case-matches; green opens with the exact lowercase prefix bytes,
# red verdicts keep uppercase tokens and must never open with the ok prefix.
# ===========================================================================

def test_cli_green_first_line_is_the_ok_prefix(tmp_path):
    row, line = _row_and_line()
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--check")
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.startswith(CLAIM_PATROL_OK_PREFIX), repr(out.stdout.splitlines()[:1])
    assert row["id"] in out.stdout  # the per-row evidence names the claim


def test_cli_stale_never_opens_with_the_ok_prefix(tmp_path):
    # moment 2026-09-01, carrier committed today: carrier_touched fires and
    # the age is far past the 7d bar.
    row, line = _row_and_line(day="2026-09-01", collected="1,341", files="264")
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 1, out.stdout + out.stderr
    assert out.stdout.startswith("CLAIM-PATROL: STALE"), repr(out.stdout.splitlines()[:1])
    assert not out.stdout.startswith(CLAIM_PATROL_OK_PREFIX)


def test_cli_blind_opens_unverifiable(tmp_path):
    row, _ = _row_and_line()
    row["carrier_path"] = "GHOST.md"
    _write_estate(tmp_path, [row], None, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert out.stdout.startswith("CLAIM-PATROL: UNVERIFIABLE"), repr(out.stdout.splitlines()[:1])


# ===========================================================================
# BAND 4: accept-by-name baseline + the GROWTH law (g06 section 4; ratchet
# fingerprint/accept/prune bones, violation_ratchet.py:84-86, 241-281).
# ===========================================================================

def test_fingerprint_is_sha256_of_rule_id_detail_16():
    fp = cdp.fingerprint("stale", "census-headline", "claim lags carrier")
    assert fp == hashlib.sha256(
        b"stale\0census-headline\0claim lags carrier").hexdigest()[:16]
    assert len(fp) == 16


def test_fingerprint_rules_and_ids_differ():
    a = cdp.fingerprint("stale", "x", "claim lags carrier")
    b = cdp.fingerprint("contradicted", "x", "verifier contradicts claim")
    c = cdp.fingerprint("stale", "y", "claim lags carrier")
    assert a != b and a != c


def test_baseline_update_accepts_and_check_suppresses(tmp_path):
    root = tmp_path / "e"
    root.mkdir()
    row, line = _row_and_line(day="2026-09-01")
    _write_estate(root, [row], line, commit=True)
    bl = _empty_baseline(root)
    red = _run(root, "--baseline", str(bl))
    assert red.returncode == 1, red.stdout + red.stderr  # red before acceptance
    upd = _run(root, "--baseline", str(bl), "--baseline-update",
               "--by", "lane-i03", "--note", "genetic burn G1 acceptance")
    assert upd.returncode == 0, upd.stdout + upd.stderr
    data = json.loads(bl.read_text(encoding="utf-8"))
    assert len(data["accepted"]) == 1
    green = _run(root, "--baseline", str(bl))
    assert green.returncode == 0, green.stdout + green.stderr


def test_growth_line_fires_when_claim_text_churns_after_acceptance(tmp_path):
    # The B2-273 GROWTH law generalized: acceptance freezes what the world
    # looked like; a carrier refresh under an accepted claim must print the
    # GROWTH line (non-blocking, always visible). The fingerprint stays
    # stable across the churn because the detail is line-free and
    # carrier-free - the same register entry still suppresses the exit.
    root = tmp_path / "e"
    root.mkdir()
    row, line = _row_and_line(day="2026-09-01")
    _write_estate(root, [row], line, commit=True)
    bl = _empty_baseline(root)
    upd = _run(root, "--baseline", str(bl), "--baseline-update",
               "--by", "lane-i03", "--note", "accept while stale")
    assert upd.returncode == 0, upd.stdout + upd.stderr
    # Reword the carrier to fresh counts without touching the row: the row
    # is still stale (old moment, text_differs now), the fp is unchanged,
    # so the exit stays suppressed but the growth must be named.
    reworded = _carrier_line(collected="1,900", files="305", day="2026-09-26")
    (root / "AGENTS.md").write_text(reworded + "\n", encoding="utf-8")
    out = _run(root, "--baseline", str(bl))
    assert out.returncode == 0, out.stdout + out.stderr
    assert "GROWTH" in out.stdout


def test_expired_acceptance_reviolates(tmp_path):
    root = tmp_path / "e"
    root.mkdir()
    row, line = _row_and_line(day="2026-09-01")
    _write_estate(root, [row], line, commit=True)
    bl = _empty_baseline(root)
    upd = _run(root, "--baseline", str(bl), "--baseline-update",
               "--by", "lane-i03", "--note", "temp acceptance")
    assert upd.returncode == 0, upd.stdout + upd.stderr
    data = json.loads(bl.read_text(encoding="utf-8"))
    for entry in data["accepted"].values():
        entry["expires"] = (date.today() - timedelta(days=1)).isoformat()
    bl.write_text(json.dumps(data), encoding="utf-8")
    out = _run(root, "--baseline", str(bl))
    assert out.returncode == 1, out.stdout + out.stderr


def test_prune_reaps_cured_claim(tmp_path):
    root = tmp_path / "e"
    root.mkdir()
    row, line = _row_and_line(day="2026-09-01")
    _write_estate(root, [row], line, commit=True)
    bl = _empty_baseline(root)
    upd = _run(root, "--baseline", str(bl), "--baseline-update",
               "--by", "lane-i03", "--note", "accept while stale")
    assert upd.returncode == 0, upd.stdout + upd.stderr
    assert json.loads(bl.read_text(encoding="utf-8"))["accepted"]
    # Cure: refresh carrier and row together (the g06 refresh protocol),
    # moment = today, claim_text = the current match. The commit is
    # same-day, so the strictly-after rule keeps carrier_touched false.
    cured_row, cured_line = _row_and_line(day=date.today().isoformat())
    _write_estate(root, [cured_row], cured_line, commit=False)
    prune = _run(root, "--baseline", str(bl), "--prune")
    assert prune.returncode == 0, prune.stdout + prune.stderr
    assert not json.loads(bl.read_text(encoding="utf-8"))["accepted"]


# ===========================================================================
# BAND 5: frozen seed-row grammar vectors ([COPY] of the ancestor parser
# vectors; census_patrol_selftest.py:40-94 numbers 1,837/301 and 1,341/264).
# Pure re against the frozen g06 section 1 claim_regex - no patrol code.
# ===========================================================================

LIVE_SHAPE = (
    "- **Tests:** 1,837 tests collected / 301 files (2026-09-26 census, "
    "`pytest --collect-only -q`, receipt `watch/inbox/x.md`; retired 1,341). "
    "**Trust bytes, not reports.**"
)
FOSSIL_SHAPE = (
    "- **Tests:** 1,341 tests / 264 files (2026-09-14 census: 1305 passed / 34 failed / "
    "9 skipped, ~12 min). Run `pytest -q` before claiming done. **Trust bytes, not reports.**"
)


def test_seed_grammar_parses_live_canonical_shape():
    m = re.search(CENSUS_CLAIM_SRC, LIVE_SHAPE)
    assert m is not None
    assert m.groups() == ("1,837", "301", "2026-09-26")


def test_seed_grammar_parses_fossil_shape():
    # The retired hand-copied form must still parse, so the patrol keeps
    # catching it if it ever comes back.
    m = re.search(CENSUS_CLAIM_SRC, FOSSIL_SHAPE)
    assert m is not None
    assert m.groups() == ("1,341", "264", "2026-09-14")


def test_prose_numbers_before_claim_cannot_form_the_parse():
    # B2-245 vector class: tripwire prose ("retired 1,341", "31 files
    # grown") ahead of the claim must never become the parse; only a full
    # census-clause match counts, and prose-only text has no match at all.
    poisoned_prose_only = (
        "- **Tests:** Census-carrier tripwire (B2-215, 2026-09-14): the retired 1,341 headline "
        "rode 12 days stale with 31 files grown and no gate noticed. Trust bytes, not reports."
    )
    assert re.search(CENSUS_CLAIM_SRC, poisoned_prose_only) is None
    poisoned_with_live = (
        "- **Tests:** Census-carrier tripwire (B2-215, 2026-09-26): the retired 1,341 headline "
        "rode 12 days stale with 31 files grown and no gate noticed. Live: 1,837 tests collected "
        "/ 301 files (2026-09-26 census, pytest --collect-only -q). Trust bytes, not reports."
    )
    m = re.search(CENSUS_CLAIM_SRC, poisoned_with_live)
    assert m is not None
    assert m.groups() == ("1,837", "301", "2026-09-26")


def test_noncanonical_line_is_no_match():
    # Fail-closed: counts and a date without the census clause shape no
    # match, which is exit 2 upstream - never a guess.
    assert re.search(
        CENSUS_CLAIM_SRC, "- **Tests:** 31 files grown since 2026-09-14, trust bytes."
    ) is None


# ===========================================================================
# BAND 6: tier-2 deep-check symmetry on the pure verdict core (g06 section 3
# tier 2; under-claim is the B2-244 disease, over-claim is worse).
# ===========================================================================

def test_verify_underclaim_at_bar_is_contradicted():
    v = cdp.verify_patrol(2, 22, value_kind="int", tolerance=20)
    assert v["verdict"] == "CONTRADICTED"
    assert v["exit"] == 1


def test_verify_overclaim_at_bar_is_contradicted():
    # Symmetric on purpose: a number invented is worse than a number stale.
    v = cdp.verify_patrol(42, 22, value_kind="int", tolerance=20)
    assert v["verdict"] == "CONTRADICTED"
    assert v["exit"] == 1


def test_verify_below_bar_is_ok():
    v = cdp.verify_patrol(10, 22, value_kind="int", tolerance=20)
    assert v["ok"] is True
    assert v["exit"] == 0


def test_verify_text_inequality_is_contradicted_and_equality_ok():
    v = cdp.verify_patrol("gemma4", "qwen2.5-coder:7b", value_kind="text")
    assert v["verdict"] == "CONTRADICTED"
    assert v["exit"] == 1
    ok = cdp.verify_patrol("gemma4", "gemma4", value_kind="text")
    assert ok["ok"] is True


def test_verify_unclaimable_is_exit_2():
    v = cdp.verify_patrol(None, 22, value_kind="int", tolerance=20)
    assert v["verdict"] == "UNVERIFIABLE"
    assert v["exit"] == 2


# ===========================================================================
# BAND 7: tier-2 through the real CLI - verifier argv run cwd=root, real
# exit codes on synthetic estates ([COPY] of the ancestor --collect band).
# ===========================================================================

def test_cli_collect_green_exits_0(tmp_path):
    row, line = _row_and_line()  # verifier prints 22, claim_group 1 says 22
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--collect")
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.startswith(CLAIM_PATROL_OK_PREFIX)


def test_cli_falsifier_green_gate_then_collect_contradicted(tmp_path):
    # The pre-registered falsifier shape: tier 1 green (fresh moment, no
    # git growth, claim_text matches), then --collect proves the claim 20+
    # off the verifier truth: the deep check raises the verdict to
    # CONTRADICTED exit 1.
    # Carrier claims 2, the row's verifier measures 22: delta 20 hits the
    # tolerance bar from below-the-claim (the under-claim direction).
    row, line = _row_and_line(collected="2")
    row["verifier"] = [sys.executable, "-c", "print(22)"]
    _write_estate(tmp_path, [row], line, commit=True)
    base = _run(tmp_path, "--check")
    assert base.returncode == 0, base.stdout + base.stderr
    deep = _run(tmp_path, "--collect")
    assert deep.returncode == 1, deep.stdout + deep.stderr
    assert "CONTRADICTED" in deep.stdout


def test_cli_collect_unparsable_verifier_exits_2(tmp_path):
    row, line = _row_and_line()
    row["verifier"] = [sys.executable, "-c", "print('no number here')"]
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--collect")
    assert out.returncode == 2, out.stdout + out.stderr
    assert row["id"] in out.stdout


def test_cli_collect_crashed_verifier_exits_2(tmp_path):
    row, line = _row_and_line()
    row["verifier"] = [sys.executable, "-c", "import sys; sys.exit(3)"]
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--collect")
    assert out.returncode == 2, out.stdout + out.stderr
    assert row["id"] in out.stdout


def test_cli_collect_row_without_verifier_exits_2(tmp_path):
    # A row with no deep check is UNVERIFIABLE under --collect, naming the
    # row - never a silent pass.
    row, line = _row_and_line()
    del row["verifier"]
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--collect")
    assert out.returncode == 2, out.stdout + out.stderr
    assert row["id"] in out.stdout


def test_cli_collect_claim_group_out_of_range_exits_2(tmp_path):
    row, line = _row_and_line(claim_group=5)  # the frozen grammar has 3 groups
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--collect")
    assert out.returncode == 2, out.stdout + out.stderr


def test_cli_collect_text_kind_inequality_contradicted(tmp_path):
    # text mode: the verifier's last non-empty line must EQUAL the
    # claim_group capture; any inequality is CONTRADICTED exit 1.
    line = "worker: gemma4 (SEATS matrix, 2026-10-18)"
    regex = r"worker:\s+(\S+)"
    row = {
        "id": "seats-worker",
        "claim_text": "worker: gemma4",
        "carrier_path": "AGENTS.md",
        "claim_regex": regex,
        "claim_group": 1,
        "moment": date.today().isoformat(),
        "owner": "seats-curator",
        "verifier": [sys.executable, "-c", "print('qwen2.5-coder:7b')"],
        "value_kind": "text",
        "stale_days": 7,
        "receipt": "memory/runs/genetic_burn/20261018/G1/lanes/i03-patrol-tests.md",
    }
    _write_estate(tmp_path, [row], line, commit=True)
    out = _run(tmp_path, "--collect")
    assert out.returncode == 1, out.stdout + out.stderr
    assert "CONTRADICTED" in out.stdout
    assert "qwen2.5-coder:7b" in out.stdout and "gemma4" in out.stdout


def test_cli_git_failure_is_exit_2(tmp_path):
    # The carrier_touched collector is a git call; git failure is
    # cannot-verify (PatrolError), never a guess. GIT_DIR pointed at a
    # nonexistent repo makes the child's git log fail while the disk
    # fixture itself is a perfectly green estate.
    row, line = _row_and_line()
    _write_estate(tmp_path, [row], line, commit=True)
    child_env = dict(os.environ)
    child_env["GIT_DIR"] = str(tmp_path / "nowhere.git")
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)],
        capture_output=True, text=True, timeout=120, env=child_env,
        **WINFLAGS,
    )
    assert out.returncode == 2, out.stdout + out.stderr


# ===========================================================================
# BAND 8: aggregation and skipped rows (g06 section 3 aggregation laws).
# ===========================================================================

def test_unverifiable_dominates_stale(tmp_path):
    # Exit = 2 if any row is UNVERIFIABLE, even when another row is STALE:
    # blind beats stale in the exit ladder, and both are named.
    stale_row, line = _row_and_line(day="2026-09-01")
    blind_row, _ = _row_and_line(day=date.today().isoformat())
    blind_row["id"] = "ghost-claim"
    blind_row["carrier_path"] = "GHOST.md"
    _write_estate(tmp_path, [stale_row, blind_row], line, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 2, out.stdout + out.stderr
    assert blind_row["id"] in out.stdout


def test_disabled_row_is_skipped_and_exit_unaffected(tmp_path):
    # enabled=false rows print a SKIPPED line naming the id every run (the
    # FORGOTTEN_REGISTER law: a skipped surface is never silent) and do not
    # affect the exit - even when their carrier is missing entirely.
    green_row, line = _row_and_line()
    off_row, _ = _row_and_line(day="2026-09-01")
    off_row["id"] = "parked-claim"
    off_row["carrier_path"] = "GHOST.md"
    off_row["enabled"] = False
    _write_estate(tmp_path, [green_row, off_row], line, commit=True)
    out = _run(tmp_path)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "SKIPPED" in out.stdout
    assert "parked-claim" in out.stdout


# ===========================================================================
# BAND 9: B2-338 hook pairing ([COPY] of the ancestor sh case-arm replay).
# The ok-arm PATTERN is read from the real githooks/pre-push bytes at test
# time; the claim-patrol block is wired by another lane (i03 wires nothing),
# so the replay skips until the block exists and binds byte-true after.
# ===========================================================================

@pytest.mark.skipif(shutil.which("sh") is None, reason="sh not on PATH")
def test_hook_claim_case_arm_replay_green_ok_arm_stale_warn_arm(tmp_path):
    hook_text = (REPO / "githooks" / "pre-push").read_text(encoding="utf-8")
    match = re.search(r'\n\s*("(?:CLAIM-PATROL: ok)"\*)\) : ;;', hook_text)
    if match is None:
        pytest.skip("claim-patrol case arm not in githooks/pre-push yet "
                    "(hook wiring is not lane i03's)")
    pattern = match.group(1)

    green_root = tmp_path / "green"
    green_root.mkdir()
    green_row, green_line = _row_and_line()
    _write_estate(green_root, [green_row], green_line, commit=True)
    green = _run(green_root)
    assert green.returncode == 0, green.stdout + green.stderr

    stale_root = tmp_path / "stale"
    stale_root.mkdir()
    stale_row, stale_line = _row_and_line(day="2026-09-01", collected="1,341", files="264")
    _write_estate(stale_root, [stale_row], stale_line, commit=True)
    stale = _run(stale_root)
    assert stale.returncode == 1, stale.stdout + stale.stderr

    replay = 'case "$1" in ' + pattern + ') echo OK_ARM ;; *) echo WARN_ARM ;; esac'
    green_arm = subprocess.run(["sh", "-c", replay, "sh", green.stdout],
                               capture_output=True, text=True, timeout=60, **WINFLAGS)
    stale_arm = subprocess.run(["sh", "-c", replay, "sh", stale.stdout],
                               capture_output=True, text=True, timeout=60, **WINFLAGS)
    assert green_arm.stdout.strip() == "OK_ARM", green_arm.stdout + green_arm.stderr
    assert stale_arm.stdout.strip() == "WARN_ARM", stale_arm.stdout + stale_arm.stderr
