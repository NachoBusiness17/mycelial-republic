"""Workflow-gate tests (t69, wired from t62 next_steal).

Pins the G6 receipt contract through the real CLI (exit codes 0/1/2):
a watch/inbox receipt mention with a dated stamp (label + YYYY-MM-DD,
t62 prefilter family) passes G6 ok=true; a mention with prose instead of
a date is a SOFT false (WARN row with reason, verdict PASS, exit 0, never
a hard block); a mention missing entirely stays the original hard FAIL
(exit 2). Registry rows are asserted from a tmp cwd so tests never touch
the real memory/workflows/REGISTRY.jsonl.

2026-10-05 R3-L1 amendment (ouroboros r3 move 1, receipt watch/inbox/
ouroboros_20261005/r3_land_gate.md): full-line // comments no longer
satisfy the G1-G7 shape checks, so the fixtures below carry their shapes
in code lines (laws const, conclusion in the return, receipt mention as a
code string) while declaration stamps (dated stamp, judge-model) stay on
comment lines, pinning the declaration-vs-dispatch-shape boundary. New
pins: the comment-only probe class FAILs all eight gates; a non-literal
max_concurrency RHS hard-fails G8; a width-arg default counts as a
declared width; the envelope exception requires receipt BYTES carrying a
width-bound measured number resolved from the repo root (CWD-invariant);
an unreadable script exits 2; the fire ledger joins fired_width beside
the max_concurrency stamp with a per-row width_discrepancy flag.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "workflow_gate.py"

# Fixture script that passes G1-G5 and G7 by construction; the G6 receipt
# block (code mention + comment stamp line) is injected verbatim and is the
# only thing that varies between cases. R3-L1: shapes live in code lines,
# declaration stamps live in comment lines.
BASE_SCRIPT = """// LAWS for every ask: never fabricate; no em-dashes in filed text.
const laws = "never fabricate; no em-dashes in filed text.";
async function run(items: string[]) {{
  for (const item of items) {{
    const gopher = agent("t-gopher-" + item, `fetch ${{item}}`);
    report(gopher);
    const pack = JSON.stringify(gopher);
    const review = ask(`review ${{pack}}; reported these issues? previous critique: none`);
    await artifact.markdown({{ path: "out/" + item + ".md", content: review.text }});
  }}{receipt_block}
  return {{ conclusion: "all items filed" }};
}}
"""

DATED_BLOCK = '\n  const receipt_path = "watch/inbox/RECEIPT.md";\n  // source-fetched: 2026-09-25'
UNDATED_BLOCK = '\n  const receipt_path = "watch/inbox/RECEIPT.md";\n  // fetched: all present'


def run_gate(tmp_path: Path, script_text: str) -> tuple[int, str, dict]:
    script = tmp_path / "sample.dwf.ts"
    script.write_text(script_text, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), "check", "--script", str(script), "--name", "t69-test"],
        capture_output=True,
        text=True,
        cwd=tmp_path,  # REGISTRY.jsonl lands under tmp, not the real repo
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    reg = tmp_path / "memory" / "workflows" / "REGISTRY.jsonl"
    last_row = json.loads(reg.read_text(encoding="utf-8").strip().splitlines()[-1])
    return proc.returncode, proc.stdout, last_row


def g6_row(row: dict) -> dict:
    return next(c for c in row["checks"] if c["id"] == "G6-receipts")


def test_dated_receipt_passes_g6_ok(tmp_path):
    code, out, row = run_gate(tmp_path, BASE_SCRIPT.format(receipt_block=DATED_BLOCK))
    assert code == 0
    assert "workflow_gate PASS" in out
    assert "  ok    G6-receipts" in out
    g6 = g6_row(row)
    assert g6["ok"] is True
    assert "soft" not in g6


def test_undated_receipt_is_soft_warn_not_hard_block(tmp_path):
    code, out, row = run_gate(tmp_path, BASE_SCRIPT.format(receipt_block=UNDATED_BLOCK))
    assert code == 0  # exit contract untouched: soft findings never hard-block
    assert "workflow_gate PASS" in out
    assert "  WARN  G6-receipts" in out
    g6 = g6_row(row)
    assert g6["ok"] is False
    assert g6["soft"] is True
    assert "dated stamp" in g6["reason"]


def test_missing_receipt_still_hard_fails_exit_2(tmp_path):
    code, out, row = run_gate(tmp_path, BASE_SCRIPT.format(receipt_block=""))
    assert code == 2
    assert "workflow_gate FAIL" in out
    assert "  FAIL  G6-receipts" in out
    g6 = g6_row(row)
    assert g6["ok"] is False
    assert "soft" not in g6


def test_stamp_regex_matches_t62_label_family():
    # Import the gate module to pin the regex family directly.
    sys.path.insert(0, str(REPO))
    from tools.workflow_gate import G6_STAMP_RE

    assert G6_STAMP_RE.search("source-fetched: 2026-09-25")
    assert G6_STAMP_RE.search("source_fetched: 2026-09-25")
    assert G6_STAMP_RE.search("Fetched: 2026-09-25")
    assert G6_STAMP_RE.search("observed_at: 2026-09-25T10:00Z")
    # the t51 false positive shape stays unmatched (prose, no date)
    assert G6_STAMP_RE.search("fetched: all present") is None
    assert G6_STAMP_RE.search("no stamp here at all") is None


# --- LAW-12 genesis scenario mode (landed 2026-09-26) ---
# A scenario card must cite a real registry FAIL row that shows its gate
# failing, and its fixture must produce exactly the expected verdict.
# All runs happen in a tmp cwd so the real REGISTRY.jsonl is never touched.

SCENARIO_SCRIPT = """// LAWS for every ask: never fabricate; no em-dashes in filed text.
// judge-model: groq/compound-mini (B2-206 cross-family firing contract; keeps the
// G3 judge-independence soft-warn out of these single-purpose G1 assertions)
const laws = "never fabricate; no em-dashes in filed text.";
async function run(items: string[]) {
  for (const item of items) {
    const gopher = agent(worker, `fetch ${item}`);
    report(gopher);
    const pack = JSON.stringify(gopher);
    const review = ask(`review ${pack}; reported these issues? previous critique: none`);
    await artifact.markdown({ path: "out/" + item + ".md", content: review.text });
  }
  const receipt_path = "watch/inbox/RECEIPT.md";
  // source-fetched: 2026-09-26
  return { conclusion: "all items filed" };
}
"""


def _mint_and_card(tmp_path: Path, mutate_pass: bool = False) -> Path:
    scen = tmp_path / "scenarios"
    fx = scen / "fixtures"
    fx.mkdir(parents=True)
    fixture = fx / "fail_g1.dwf.ts"
    fixture.write_text(SCENARIO_SCRIPT, encoding="utf-8")
    subprocess.run(
        [sys.executable, str(TOOL), "check", "--script", str(fixture), "--name", "scen-test"],
        capture_output=True, text=True, cwd=tmp_path,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    reg = tmp_path / "memory" / "workflows" / "REGISTRY.jsonl"
    row = json.loads(reg.read_text(encoding="utf-8").strip().splitlines()[-1])
    assert row["verdict"] == "FAIL"
    expected = {
        "overall": "PASS" if mutate_pass else "FAIL",
        "failed_checks": [] if mutate_pass else ["G1-multiplicity"],
        "warn_checks": [],
        "exit_code": 0 if mutate_pass else 2,
    }
    card = {
        "gate_id": "G1-multiplicity",
        "cited_fail_row": {"ts": row["ts"], "name": "scen-test", "digest": row["digest"]},
        "scenario_input": str(fixture),
        "expected_verdict": expected,
        "regression_criterion": "suite green after any gate change",
        "rollback_note": "git revert tools/workflow_gate.py, re-run scenarios",
    }
    card_path = scen / "G1_test.card.json"
    card_path.write_text(json.dumps(card), encoding="utf-8")
    return scen


def test_scenario_suite_green_and_read_only(tmp_path):
    scen = _mint_and_card(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(TOOL), "check", "--scenarios", str(scen)],
        capture_output=True, text=True, cwd=tmp_path,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert proc.returncode == 0
    assert "SCENARIOS ok   G1_test.card.json: G1-multiplicity -> FAIL exit 2" in proc.stdout
    assert "no registry row written" in proc.stdout
    # read-only proof: the registry still holds exactly the one minted row
    reg = tmp_path / "memory" / "workflows" / "REGISTRY.jsonl"
    assert len(reg.read_text(encoding="utf-8").strip().splitlines()) == 1


def test_scenario_expectation_mismatch_exits_2(tmp_path):
    scen = _mint_and_card(tmp_path, mutate_pass=True)
    proc = subprocess.run(
        [sys.executable, str(TOOL), "check", "--scenarios", str(scen)],
        capture_output=True, text=True, cwd=tmp_path,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert proc.returncode == 2
    assert "SCENARIOS FAIL G1_test.card.json" in proc.stdout
    assert "verdict FAIL != expected PASS" in proc.stdout


def test_scenario_citation_to_missing_row_is_error(tmp_path):
    scen = _mint_and_card(tmp_path)
    card_path = scen / "G1_test.card.json"
    card = json.loads(card_path.read_text(encoding="utf-8"))
    card["cited_fail_row"]["digest"] = "deadbeefcafe"
    card_path.write_text(json.dumps(card), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), "check", "--scenarios", str(scen)],
        capture_output=True, text=True, cwd=tmp_path,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert proc.returncode == 2
    assert "not found in" in proc.stdout


# --- B2-206 judge-independence marker behind G3 (soft-warn family like G6) ---
def test_g3_judge_independence_marker(tmp_path):
    sys.path.insert(0, str(REPO))
    import importlib.util
    spec = importlib.util.spec_from_file_location("wg_b2_206", str(TOOL))
    wg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wg)
    run_checks, G3_JUDGE_MODEL_RE = wg.run_checks, wg.G3_JUDGE_MODEL_RE
    steering = 'const r = await agent("reader", {}).ask<V>("reported these issues? Previous critique: none");'
    without = run_checks(steering)
    g3 = next(r for r in without if r["id"] == "G3-steering")
    assert g3["ok"] is False and g3.get("soft") is True and "judge independence" in g3["reason"]
    with_stamp = run_checks(steering + "\n// judge-model: groq/compound-mini\n")
    g3s = next(r for r in with_stamp if r["id"] == "G3-steering")
    assert g3s["ok"] is True and "soft" not in g3s
    # steering absent: no marker either way (marker fires only when G3 passes)
    for text in ("", "nothing here"):
        g3n = next(r for r in run_checks(text) if r["id"] == "G3-steering")
        assert g3n["ok"] is False and not g3n.get("soft")
    assert G3_JUDGE_MODEL_RE.search("subagent_model: google/gemini-2-flash") is not None


# --- R3-L1 width truth (2026-10-05, ouroboros r3 move 1, receipt
# watch/inbox/ouroboros_20261005/r3_land_gate.md) ---

# The banked R3 probe class: every dispatch shape lives in a // comment.
# Pre-fix this PASSed the gate from the repo root (fold re-verified, digest
# 661e5b317ecb); post-fix it must FAIL all eight gates.
COMMENT_ONLY_SCRIPT = """// R3 trust probe: can the gate be PASSed by prose alone?
// G1 shape in a comment: agent("x-" + item)
// G2 shape in a comment: result + parsed.text
// G3 shape in a comment: Previous critique: reported these issues in ask<
// G4 shape in a comment: report(item);
// G5 shape in a comment: artifact.markdown(out) conclusion: done
// G6 shape: receipt lands in watch/inbox with Source-fetched: 2026-10-05
// G7 shape: asks carry the laws: never fabricate, no em-dashes
// G8 shape: max_concurrency: 50 with envelope-receipt: watch/inbox/INDEX.json
const placeholder = 1;
"""


def test_comment_only_script_fails_all_shape_gates(tmp_path):
    code, out, row = run_gate(tmp_path, COMMENT_ONLY_SCRIPT)
    assert code == 2
    assert "workflow_gate FAIL" in out
    failed = {c["id"] for c in row["checks"] if not c["ok"] and not c.get("soft")}
    # every shape gate rejects prose-only shapes; G8 fails because
    # watch/inbox/INDEX.json bytes carry no width-bound measured number
    assert failed == {
        "G1-multiplicity", "G2-passoff", "G3-steering", "G4-salvage",
        "G5-deliverable", "G6-receipts", "G7-laws", "G8-width-shape",
    }


def test_block_comment_header_still_carries_declarations(tmp_path):
    # Boundary pin: /* */ header blocks and comment declaration stamps keep
    # their meaning (the LAW-12 card fixtures pinned that idiom); only the
    # G1-G7 dispatch shapes must live in code.
    sys.path.insert(0, str(REPO))
    from tools.workflow_gate import strip_comment_lines
    text = "/* header: laws, no em-dashes */\n// stamp line\nconst x = 1;\n"
    assert strip_comment_lines(text) == "/* header: laws, no em-dashes */\nconst x = 1;"


def test_g8_nonliteral_rhs_hard_fails(tmp_path):
    script = BASE_SCRIPT.format(
        receipt_block=DATED_BLOCK
    ).replace(
        'const laws =',
        'const shape = { max_concurrency: laneCount };\nconst laws =',
    )
    code, out, row = run_gate(tmp_path, script)
    assert code == 2
    g8 = next(c for c in row["checks"] if c["id"] == "G8-width-shape")
    assert g8["ok"] is False
    assert "non-literal max_concurrency RHS laneCount" in g8["reason"]


def test_g8_width_arg_default_counts_as_declared_width(tmp_path):
    # The FIRE_LEDGER row-1 shape: args width default 50 beside a
    # max_concurrency 3 stamp. G8 must bind the fired width, not the stamp.
    script = (
        "/* zcode-workflow header: laws, no em-dashes, never fabricate.\n"
        "   source-fetched: 2026-10-05 */\n"
        "args:\n  width:\n    type: number\n    default: 50\n"
        "*/\n"
        "// max_concurrency: 3 (declaration stamp)\n"
        + BASE_SCRIPT.format(receipt_block=DATED_BLOCK)
    )
    code, out, row = run_gate(tmp_path, script)
    assert code == 2
    g8 = next(c for c in row["checks"] if c["id"] == "G8-width-shape")
    assert g8["ok"] is False
    assert "declared width 50 above 3" in g8["reason"]


def test_g8_envelope_exception_requires_measured_bytes_not_existence(tmp_path):
    # INDEX.json exists under watch/inbox (repo-root anchored, CWD-invariant)
    # but its bytes carry no width-bound measured number: existence alone
    # must not excuse a width above 3 (the R3 probe's core assertion).
    script = COMMENT_ONLY_SCRIPT.replace(
        "const placeholder = 1;",
        'const shape = { max_concurrency: 50 };\n'
        '// envelope-receipt: watch/inbox/INDEX.json\n'
        'const placeholder = 1;',
    )
    code, out, row = run_gate(tmp_path, script)
    assert code == 2
    g8 = next(c for c in row["checks"] if c["id"] == "G8-width-shape")
    assert g8["ok"] is False
    assert "no measured envelope receipt" in g8["reason"]
    # a stamp naming a missing file fails identically (existence was the
    # pre-fix only test; bytes are the post-fix test)
    script2 = script.replace("watch/inbox/INDEX.json",
                             "watch/inbox/NO_SUCH_RECEIPT_20261005.md")
    code2, _, row2 = run_gate(tmp_path, script2)
    assert code2 == 2
    g82 = next(c for c in row2["checks"] if c["id"] == "G8-width-shape")
    assert g82["ok"] is False


def test_g8_receipt_bytes_verdict_is_cwd_invariant(tmp_path):
    # R3 fold: the same script PASSed from repo root and FAILed from /tmp
    # (digest 661e5b317ecb). The receipt path now resolves from
    # Path(__file__).parents[1], so the G8 outcome cannot flip with CWD.
    sys.path.insert(0, str(REPO))
    import importlib.util
    spec = importlib.util.spec_from_file_location("wg_r3", str(TOOL))
    wg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wg)
    probe = (REPO / "watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust"
             / "probes/g8_vacuous_envelope.dwf.ts").read_text(encoding="utf-8")
    ok = wg.g8_width_shape_ok(probe)
    # from this test process's cwd (wherever pytest runs), INDEX.json is not
    # a measured envelope for width 50
    assert ok is False
    assert str(wg.REPO_ROOT).endswith("local_sovereign_agent")


def test_unreadable_script_is_hard_block_exit_2(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(TOOL), "check", "--script",
         str(tmp_path / "missing.dwf.ts")],
        capture_output=True, text=True, cwd=tmp_path,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert proc.returncode == 2
    assert "cannot read script (hard block)" in proc.stdout


def test_fire_ledger_joins_fired_width_beside_stamp(tmp_path):
    script = (
        "/* zcode-workflow header: laws, no em-dashes, never fabricate.\n"
        "   source-fetched: 2026-10-05 */\n"
        "args:\n  width:\n    type: number\n    default: 50\n"
        "*/\n"
        "// max_concurrency: 3 (declaration stamp)\n"
        + BASE_SCRIPT.format(receipt_block=DATED_BLOCK)
    )
    run_gate(tmp_path, script)
    ledger = tmp_path / "memory/workflows/FIRE_LEDGER.jsonl"
    fire = json.loads(ledger.read_text(encoding="utf-8").strip().splitlines()[-1])
    # the row-1 discrepancy shape is now visible per row, not nested-only
    assert fire["fired_args"]["width"] == "50"
    assert fire["max_concurrency"] == 3
    assert fire["fired_width"] == 50
    assert fire["width_discrepancy"] is True
