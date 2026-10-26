"""Tests for tools.citation_lint (a05-r2, GAP_REGISTER rank 3, 2026-10-01).

The founding law: the 191.8M phantom must FAIL the lint. The founding
fixture is the verbatim STORY.md paragraph (lines 225-243 as they stood
before the 2026-10-01 ERRATA struck the clause), embedded here and in the
tool's self-test path so the fixture survives the errata and any future
STORY edit. Both known ractor50 anchor drifts must fire:
  mag/mcp_server.py:338-340  (wiring moved to :344/:356/:358)
  mag/biography.py:526       (the write moved to :390 via evict_for_prepend)

This file also carries the tool's --selftest battery (the CLI runs it via
pytest), so fixtures live with the tests: tests/ sits outside the ratchet's
scan roots and fixtures are test material.

Receipt: watch/inbox/fillball/citation-lint.md
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "citation_lint.py"

# Package-form imports ONLY: the tool's modules import each other in package
# form when the estate root is importable (it is, under pytest), so binding
# the plain names here would patch a SECOND module instance and the fixture
# world would never touch the code under test (the live failure that forced
# this import discipline).
from tools import citation_lint as cl  # noqa: E402
from tools import citation_lint_io as cio  # noqa: E402


def _fixture_world(monkeypatch, tmp_path: Path):
    """Point the tool at a throwaway estate slice, hermetically."""
    # both layers carry ESTATE_ROOT: core's pipeline uses its own import,
    # io's resolver and rel_path use theirs
    monkeypatch.setattr(cl, "ESTATE_ROOT", tmp_path)
    monkeypatch.setattr(cio, "ESTATE_ROOT", tmp_path)
    # keep the fixture world hermetic: no real-repo basename fallback
    monkeypatch.setattr(cio, "_git_ls_files", lambda pattern: [])
    cio._LSFILES_CACHE.clear()
    cio._RESOLVE_CACHE.clear()
    cio._CONTAINS_CACHE.clear()
    cio._SOURCE_TEXT_CACHE.clear()
    return cl


def _write(tmp: Path, rel: str, text: str) -> Path:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


# The founding fixture: watch/inbox/48h_synth/STORY.md lines 225-243, verbatim
# bytes (embedded, never read live: the 2026-10-01 ERRATA struck the 191.8M
# clause from STORY.md, and this fixture must survive it). It carries one
# phantom number (191.8M vs DIGEST.md), one drifted anchor
# (mag/percolator.py:264-272, flagged in accuracy.md:175), and one clean
# anchor (mag/seed_percolator.py:6-16) as the control.
FOUNDING_PARAGRAPH = """\
The fold added its own death-and-amendment pair. The first fold pass overwrote the same-path
predecessor fold, and because the four fold outputs were untracked in git with no committed
history, the overwrite destroyed the only copy; the predecessor text is NOT recoverable, its
headline counts (18 lanes / 23 finds / 9 cards) survive only in the Supersession note and the
digest's pass-over delta (watch/inbox/frontier_olm_20260928/RECEIPT.md, "Supersession";
watch/inbox/frontier_olm_20260928/DIGEST.md lines 7 to 17). Then came the trust incident: the
operator reported RECEIPT.md missing while the seat's os.path.exists returned True and measured
the file at 26,347 bytes; instead of averaging the contradiction, the receipt records both facts
and supersedes itself with fresh measurements (RECEIPT.md header, "Write-time state"). One more
amendment rode along: an earlier grep for the workflow's registry rows used the underscore form
(frontier_olm) and silently matched none of the names, missing rows 31 to 33; the corrected
hyphenated grep found all six (RECEIPT.md, "Search note"). The mine that emerged from all of it:
32 of 32 sweep returns ok, 21 confirmed finds banked with per-row overlap corrections (the Vals
"#1 open-weight" headline REFUTED at probe time, the PolAgentBench CC0 attribution refuted as
MIT code plus CC BY 4.0 data), 3 unconfirmed items held with evidence and cited nowhere, 5 steal
cards with falsifiable probes, 191.8M tokens spent, and the two percolator code reads verified
in-session (recurrence-only promote at mag/percolator.py:264-272, the estate's own dormant
paired-blind gate at mag/seed_percolator.py:6-16) (watch/inbox/frontier_olm_20260928/DIGEST.md,
executive summary and register table; SKILL.md "Lineage").
"""


def _build_fixtures(tmp: Path) -> dict[str, Path]:
    """Build a throwaway estate slice with every finding class + controls."""
    # real span bytes: mag/seed_percolator.py:6-16 (clean control); the stub
    # keeps the real line numbering (ELDER block opens at line 6)
    seed = "\n".join(
        [
            "# seed percolator",
            "x = 1",
            "x = 2",
            "x = 3",
            "x = 4",
            "ELDER DESIGN LOCKED (memory/runs/seed_percolator_elder_advice.md):",
            "  fitness   = paired blind win-rate vs frozen baseline (judge picks better; tie=0.5)",
            "  threshold = >=55% win-rate, min 30 judged pairs PER EPOCH",
            "  promotion = >=55% in 3 CONSECUTIVE epochs on fresh task sets (total >=90 pairs)",
            "  guard     = null-variant canary: baseline copy must NOT exceed 50% wins, else judge",
            "              is biased -> loop HALTS (auto), flag raised.",
            "              Adversarial judge rotation every 10th pair (epoch 1+, not v0).",
            "",
            "v0 scope (babystep): mechanics only. No scheduler wiring;",
            "the worker container or tick can call the beat entrypoint later.",
            "x = 5",
        ]
    )
    # real span bytes: mag/percolator.py:264-272 (the drifted anchor's span)
    perc = "\n".join(
        ["# percolator"] + ["x = 1"] * 262 + [
            "                    merged = dict(seal_gens)",
            "                    if INVARIANT_REGISTRY.is_file():",
            "                        try:",
            "                            live = json.loads(INVARIANT_REGISTRY.read_text(encoding=\"utf-8\"))",
            "                            for k, v in (live.get(\"invariants\") or {}).items():",
            "                                if k in merged:",
            "                                    # Z15 (2026-09-29, S15 diagnosis \"heal-merge SUMS counts\"",
            "                                    # (triple-counting)\"): shared count merges take MAX, not SUM.",
            "                                    # MAX is IDEMPOTENT, healing N times from the same seal",
        ]
    )
    # real span shape: mag/mcp_server.py lines 336-358 at HEAD (drift 1)
    mcp = "\n".join(
        ["# mcp server"] + ["x = 1"] * 334 + [
            "    from tools.mcp_pin import DEFAULT_LEDGER  # lazy: module import stays stdlib-only",
            "",
            "    return DEFAULT_LEDGER",
            "",
            "",
            "def pin_gate_filter(",
            "    manifest: list[dict[str, Any]], ledger_path: str | Path | None",
            ") -> tuple[list[dict[str, Any]], dict[str, Any]]:",
            "    \"\"\"Connect-time rug-pull gate: run tools/mcp_pin.py check_drift, fail loud.",
            "",
            "    NEW and PINNED tools pass unchanged.",
            "    \"\"\"",
            "    if ledger_path is None:",
            "        return manifest, {\"alarm\": False, \"enabled\": False}",
            "    from tools.mcp_pin import check_drift  # lazy: module import stays stdlib-only",
            "",
            "    report = check_drift(manifest, ledger_path=Path(ledger_path))",
        ]
    )
    # real span shape: mag/biography.py lines 388-392 and 524-528 at HEAD (drift 2)
    bio = "\n".join(
        ["# biography"] + ["x = 1"] * 387 + [
            "    prev = att.read_text(encoding=\"utf-8\") if att.exists() else \"\"",
            "    att.write_text(evict_for_prepend(prev, note, 40000), encoding=\"utf-8\")",
            "    return len(note)",
            "",
            "",
        ] + ["x = 1"] * 132 + [
            "    themes_line = \"\"",
            "    for t in themes:",
            "        themes_line += t",
        ]
    )
    # the named source that must NOT contain the phantom number, plus the
    # receipt that carries the 26,347 byte measurement (so the founding
    # fixture fires exactly one phantom: the 191.8M)
    digest = (
        "# OLM MINE DAY 2 DIGEST\n\n"
        "executive summary: 32 of 32 sweep returns ok, 21 confirmed finds.\n"
        "register table follows. No token totals are compiled in this payload.\n"
    )
    receipt = (
        "# OLM MINE RECEIPT\n\n"
        "Write-time state: os.path.exists returned True and the on-disk file\n"
        "measured 26347 bytes; both facts are recorded.\n"
    )
    digest_hit = (
        "# control source\n\nThe mine spent 191.8M tokens (compiled payload).\n"
    )
    fixtures: dict[str, Path] = {}
    fixtures["perc"] = _write(tmp, "mag/percolator.py", perc)
    fixtures["seed"] = _write(tmp, "mag/seed_percolator.py", seed)
    fixtures["mcp"] = _write(tmp, "mag/mcp_server.py", mcp)
    fixtures["bio"] = _write(tmp, "mag/biography.py", bio)
    fixtures["digest"] = _write(tmp, "watch/inbox/frontier_olm_20260928/DIGEST.md", digest)
    fixtures["receipt"] = _write(tmp, "watch/inbox/frontier_olm_20260928/RECEIPT.md", receipt)
    fixtures["digest_hit"] = _write(tmp, "watch/inbox/ctrl/DIGEST.md", digest_hit)
    fixtures["story"] = _write(
        tmp, "watch/inbox/48h_synth/STORY.md",
        FOUNDING_PARAGRAPH,
    )
    fixtures["mcp_record"] = _write(
        tmp, "watch/inbox/rec/mcp_drift.md",
        "S7 check_drift caller census (wired at mag/mcp_server.py:338-340). The moved truth sits at :356/:358.\n"
        "Control: the pin doctrine docstring now lives at mag/mcp_server.py:344-349 and names check_drift.\n",
    )
    fixtures["bio_record"] = _write(
        tmp, "watch/inbox/rec/bio_drift.md",
        "The biography writer truncates with att.write_text(note + prev[:40000]) at mag/biography.py:526.\n"
        "Control: the eviction write now lives at mag/biography.py:390 with evict_for_prepend.\n",
    )
    fixtures["missing"] = _write(
        tmp, "watch/inbox/rec/missing.md",
        "The gate is documented at docs/ref/NO_SUCH_FILE_SPEC.md:12 in the doctrine.\n",
    )
    fixtures["oob"] = _write(
        tmp, "watch/inbox/rec/oob.md",
        "The span runs past EOF at mag/biography.py:99999 per the drift note.\n",
    )
    fixtures["blank"] = _write(
        tmp, "watch/inbox/rec/blank.md",
        "The vacuous anchor sits at mag/biography.py:392 in the drift note.\n",
    )
    fixtures["clean"] = _write(
        tmp, "watch/inbox/rec/clean.md",
        "The elder gate reads: fitness = paired blind win-rate vs frozen baseline at mag/seed_percolator.py:6-9.\n",
    )
    return fixtures


def test_founding_phantom_fails_lint(monkeypatch, tmp_path):
    """THE founding test: the 191.8M phantom must FAIL the lint."""
    _fixture_world(monkeypatch, tmp_path)
    fx = _build_fixtures(tmp_path)
    result = cl.run([fx["story"]], False, {})
    phantoms = [
        f for f in result.findings
        if f.rule == "PHANTOM-NUMBER" and "191.8" in f.anchor
    ]
    assert phantoms, "the 191.8M phantom did not fire"
    assert len(phantoms) == 1, "exactly one phantom: 26,347 lives in RECEIPT.md"
    assert result.blocking, "the founding fixture must FAIL the lint (blocking findings)"
    # the paragraph's clean control anchor stays silent
    assert not [f for f in result.findings if "seed_percolator" in f.anchor]
    # accuracy.md:175's second drift in the same paragraph fires (a default
    # run carries TOKEN-MISS as warn class, not blocking)
    assert any(
        f.rule == "TOKEN-MISS" and "percolator.py" in f.anchor
        and "biography" not in f.anchor
        for f in result.findings + result.warns
    )


def test_known_drifts_fire(monkeypatch, tmp_path):
    """Both GAP_REGISTER-named drifts fire as TOKEN-MISS on their records."""
    _fixture_world(monkeypatch, tmp_path)
    fx = _build_fixtures(tmp_path)
    mcp = cl.run([fx["mcp_record"]], True, {})
    assert any(
        f.rule == "TOKEN-MISS" and "mcp_server.py" in f.anchor
        and "lines 338-340" in f.detail
        for f in mcp.findings
    ), "mcp_server.py:338-340 drift did not fire"
    bio = cl.run([fx["bio_record"]], True, {})
    assert any(
        f.rule == "TOKEN-MISS" and "biography.py" in f.anchor
        and "lines 526-526" in f.detail
        for f in bio.findings
    ), "biography.py:526 drift did not fire"
    # and the moved-truth controls stay clean
    assert not any("lines 344-349" in f.detail for f in mcp.findings)
    assert not any("lines 390-390" in f.detail for f in bio.findings)


def test_deterministic_classes_block(monkeypatch, tmp_path):
    """PATH-MISSING, LINE-OOB, EMPTY-SPAN block; shorthand never blocks."""
    _fixture_world(monkeypatch, tmp_path)
    fx = _build_fixtures(tmp_path)
    assert any(
        f.rule == "PATH-MISSING" for f in cl.run([fx["missing"]], False, {}).findings
    )
    assert any(f.rule == "LINE-OOB" for f in cl.run([fx["oob"]], False, {}).findings)
    assert any(f.rule == "EMPTY-SPAN" for f in cl.run([fx["blank"]], False, {}).findings)
    short = tmp_path / "watch" / "inbox" / "rec" / "shorthand.md"
    short.parent.mkdir(parents=True, exist_ok=True)
    short.write_text(
        "The held-out reproduction gate sits at SKILL.md:26-29 per the skill table.\n",
        encoding="utf-8",
    )
    res = cl.run([short], False, {})
    assert not res.blocking
    assert any(f.rule == "SHORTHAND-UNRESOLVED" for f in res.warns)


def test_clean_record_and_phantom_control(monkeypatch, tmp_path):
    """A clean record is silent; a number present in its source passes."""
    _fixture_world(monkeypatch, tmp_path)
    fx = _build_fixtures(tmp_path)
    assert not cl.run([fx["clean"]], False, {}).findings
    ctrl = _write(
        tmp_path, "watch/inbox/ctrl/STORY_OK.md",
        "The mine spent 191.8M tokens (see watch/inbox/ctrl/DIGEST.md, executive summary).\n",
    )
    res = cl.run([ctrl], False, {})
    assert not any(f.rule == "PHANTOM-NUMBER" for f in res.findings)


def test_baseline_accepts_by_name(monkeypatch, tmp_path):
    """A baseline fingerprint suppresses exactly that finding."""
    _fixture_world(monkeypatch, tmp_path)
    fx = _build_fixtures(tmp_path)
    raw = cl.LintResult()
    cl.lint_record(fx["story"], raw, tmp_path)
    ph = [f for f in raw.findings if f.rule == "PHANTOM-NUMBER"][0]
    accepted = cl.run([fx["story"]], False, {ph.fingerprint(): {"by": "test"}})
    assert not any(f.rule == "PHANTOM-NUMBER" for f in accepted.findings)


# --- R3 move 5 (ouroboros 2026-10-05, SYNTHESIS row 5): the banked
# NO_SUCH_FILE fixture. A notable number whose sentence names only record
# paths that resolve nowhere was skipped whole (the 900M probe passed the
# engine with numbers-checked 0), so the founding 191.8M class survived one
# dead-path citation. The named path does not exist and must never be created.
DEAD_CITE_TEXT = (
    "The sweep burned 900M tokens (see watch/inbox/NO_SUCH_FILE_20261005.md).\n"
)


def test_unresolved_source_warn_tier(monkeypatch, tmp_path):
    """A dead-path aggregate is a WARN-tier UNRESOLVED-SOURCE finding, one per
    number, never blocking by default (unresolved is unverifiable, not proven
    phantom)."""
    _fixture_world(monkeypatch, tmp_path)
    rec = _write(tmp_path, "watch/inbox/rec/dead_cite.md", DEAD_CITE_TEXT)
    res = cl.run([rec], False, {})
    warns = [f for f in res.warns if f.rule == "UNRESOLVED-SOURCE"]
    assert warns, "the dead-path aggregate must not be silent"
    assert "900M" in warns[0].anchor
    assert "NO_SUCH_FILE_20261005.md" in warns[0].detail
    assert not res.blocking, "warn tier: never blocks without enforce"
    assert res.numbers == 1, "the unresolved number counts as checked"


def test_unresolved_source_partial_resolution_keeps_phantom_path(monkeypatch, tmp_path):
    """Control: a sentence naming a resolvable source PLUS a dead one keeps
    today's strong check (PHANTOM-NUMBER against the resolvable bytes); the
    warn fires only when NOTHING resolves."""
    _fixture_world(monkeypatch, tmp_path)
    fx = _build_fixtures(tmp_path)
    rec = _write(
        tmp_path, "watch/inbox/rec/mixed_cite.md",
        "The burn was 900M tokens (see watch/inbox/frontier_olm_20260928/DIGEST.md "
        "and watch/inbox/NO_SUCH_FILE_20261005.md).\n",
    )
    res = cl.run([rec], False, {})
    assert not any(f.rule == "UNRESOLVED-SOURCE" for f in res.warns + res.findings)
    assert any(
        f.rule == "PHANTOM-NUMBER" and "900M" in f.anchor for f in res.blocking
    ), "the resolvable source still gets byte-checked"


def test_unresolved_source_quiet_without_notable_number(monkeypatch, tmp_path):
    """Control: a dead path on a sentence with no notable number stays silent
    (the anchor classes own dead paths; this engine owns aggregates)."""
    _fixture_world(monkeypatch, tmp_path)
    rec = _write(
        tmp_path, "watch/inbox/rec/quiet_cite.md",
        "The old plan lives at watch/inbox/NO_SUCH_FILE_20261005.md per the note.\n",
    )
    res = cl.run([rec], False, {})
    assert res.findings == [] and res.warns == []


def test_hook_entry_wired_after_ratchet():
    """The hook carries the citation_lint line after the ratchet, enforcing."""
    hook = (REPO / "githooks" / "pre-push").read_text(encoding="utf-8")
    ratchet_at = hook.find("violation_ratchet.py check --changed")
    lint_at = hook.find("tools/citation_lint.py check --changed")
    assert ratchet_at != -1, "ratchet line missing from pre-push"
    assert lint_at != -1, "citation_lint line missing from pre-push"
    assert lint_at > ratchet_at, "citation_lint must run after the ratchet"
    assert "|| exit 1" in hook[lint_at : lint_at + 120], "enforcing tail missing"


def test_selftest_battery_green():
    """The CLI --selftest runs this file via pytest and exits 0."""
    if os.environ.get("CITATION_LINT_SELFTEST") == "1":
        pytest.skip("inner battery: the outer battery is already running")
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--selftest"],
        capture_output=True, text=True, timeout=600,
        cwd=str(REPO),
        env={**os.environ, "CITATION_LINT_SELFTEST": "1"},
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_changed_mode_first_line_contract():
    """check --changed runs on the live tree and opens with the contract token."""
    proc = subprocess.run(
        [sys.executable, str(TOOL), "check", "--changed"],
        capture_output=True, text=True, timeout=300,
        cwd=str(REPO),
    )
    assert proc.returncode in (0, 1), proc.stdout + proc.stderr
    first = proc.stdout.splitlines()[0] if proc.stdout else ""
    assert first.startswith("CITATION-LINT: "), f"contract broken: {first!r}"
