"""consumer_gate - flag NEW organ modules whose docstring declares no Consumer/Verifier (i08).

Spec chain: memory/runs/genetic_burn/20261018/G0/lanes/g05-consumer-law.md
(the CONSUMER LAW as enforceable estate text, built on
watch/inbox/ORG_SYSTEM_V2_20261018.md Organ 5) + G0/GENOME.md assignment
i08-consumer-gate. Shape follows tools/citation_lint.py (a05-r2 bones).
Scope: --changed (newly ADDED .py modules vs HEAD under mag/ tools/
scripts/, the organ belt; untracked files are not push content, the
citation_lint discipline) or --files (explicit list; every named path is
treated as in-scope, which is how the founding violations are demonstrated
without a retroactive sweep). One is required.

The one deterministic class:
  CONSUMER-MISSING   a NEW organ module whose module docstring lacks a
                     declared "Consumer:" line and/or a "Verifier:" line.
                     The CONSUMER LAW (g05 section 1): an organ without a
                     named consumer and a named verifier is a cow, not a
                     spore - bounced at review. A consumer is a named reader
                     with a trigger that acts on the organ's output; a
                     verifier is a named check that can FAIL the organ's
                     claim. This gate checks DECLARATION only (the lines
                     exist in the docstring); resolving them on disk is the
                     full organ build's job, not this lane's.

Certainty: WARN-only by default (t40 precedent: findings print, exit 0;
the flip to enforce is an operator call). --enforce makes
CONSUMER-MISSING blocking (exit 1). Malformed input is exit 2,
fail-closed (B2-277: a blind gate is worse than no gate): git failure in
--changed mode, unreadable or unparseable module, bad args.

Exit/output contract (B2-338 first-line law): green opens
"CONSUMER-GATE: ok" (WARN rows print under it), blocking opens
"CONSUMER-GATE: FAIL", cannot-verify opens "CONSUMER-GATE: ERROR";
never widen.

Founding fixtures (selftest subcommand): the three violations the law
would have caught, excerpted from the 2026-10-18 bytes and carried as
detector exemplars, never read live from the real modules and never
retroactively flagged - tools/redboard.py (board with no forced reader),
tools/palace.py (falsifier fields defined, nothing ever checks them),
mag/knot_at_close.py (the bridge, report-only by default). The same move
citation_lint made with the struck 191.8M headline.

Consumer: githooks/pre-push, one WARN-only line after the citation lint
  (gene g05 section 4 step 3; pending operator wiring - until then any
  seat runs it by hand per this receipt, which is the standing trigger).
Verifier: this module's selftest battery
  (python tools/consumer_gate.py selftest) over the three founding
  fixtures; it can FAIL and say so.

CLI:
  python tools/consumer_gate.py check --changed [--enforce]
  python tools/consumer_gate.py check --files A.py B.py [--enforce]
  python tools/consumer_gate.py selftest
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = "CONSUMER-GATE"
ESTATE_ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = ("mag", "tools", "scripts")  # the organ belt (g05 section 2)
CONSUMER_KEY = "Consumer:"
VERIFIER_KEY = "Verifier:"


class ConsumerGateError(Exception):
    """Blind-gate condition: the gate cannot verify, exit 2 (B2-277 law)."""


class Finding:
    """One CONSUMER-MISSING row: module plus which declarations are absent."""

    def __init__(self, module: str, missing: list[str]) -> None:
        self.rule = "CONSUMER-MISSING"
        self.module = module
        self.missing = missing

    def render(self) -> str:
        return f"{self.rule} {self.module}: docstring lacks declared {' and '.join(self.missing)}"


def display_path(path: Path) -> str:
    """Repo-relative posix display path when inside the estate, else posix."""
    try:
        return path.resolve().relative_to(ESTATE_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def module_docstring(path: Path) -> str | None:
    """Module docstring text or None; raises ConsumerGateError when blind."""
    try:
        source = path.read_bytes()
    except OSError as exc:
        raise ConsumerGateError(f"unreadable module {display_path(path)}: {exc}")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ConsumerGateError(
            f"unparseable module {display_path(path)}: line {exc.lineno}: {exc.msg}"
        )
    return ast.get_docstring(tree)


def check_module(path: Path) -> Finding | None:
    """CONSUMER-MISSING when the docstring lacks Consumer:/Verifier: lines."""
    doc = module_docstring(path)
    lines = doc.splitlines() if doc else []
    missing: list[str] = []
    if not any(ln.strip().startswith(CONSUMER_KEY) for ln in lines):
        missing.append("'Consumer:'")
    if not any(ln.strip().startswith(VERIFIER_KEY) for ln in lines):
        missing.append("'Verifier:'")
    if missing:
        return Finding(display_path(path), missing)
    return None


def changed_new_modules() -> list[Path] | None:
    """Newly ADDED .py modules vs HEAD under the organ belt, or None on git failure.

    `git diff --name-status HEAD` covers staged + unstaged vs HEAD. Only
    status A rows count: a pre-existing module is never a retroactive flag,
    whatever else the push touches in it (renames are not new organs).
    Untracked files are excluded - not push content (citation_lint law).
    """
    try:
        proc = subprocess.run(
            ["git", "diff", "--name-status", "HEAD"],
            cwd=str(ESTATE_ROOT), capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    modules: list[Path] = []
    for row in proc.stdout.splitlines():
        parts = row.split("\t")
        if len(parts) < 2 or not parts[0].startswith("A"):
            continue
        p = Path(parts[-1])
        if p.suffix == ".py" and len(p.parts) > 1 and p.parts[0] in SCAN_ROOTS:
            modules.append(ESTATE_ROOT / p)
    return modules


def run_gate(modules: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for m in modules:
        f = check_module(m)
        if f is not None:
            findings.append(f)
    return findings


def cmd_check(modules: list[Path], enforce: bool) -> int:
    try:
        findings = run_gate(modules)
    except ConsumerGateError as exc:
        print(f"{TOOL}: ERROR {exc}")
        return 2
    if findings and enforce:
        print(f"{TOOL}: FAIL modules={len(modules)} findings={len(findings)} enforce=True")
        for f in findings:
            print(f"  {f.render()}")
        print(
            f"{TOOL}: declare Consumer:/Verifier: in the module docstring "
            f"(g05 section 1: consumer = named reader + trigger, verifier = check that can FAIL)"
        )
        return 1
    print(f"{TOOL}: ok modules={len(modules)} findings={len(findings)} enforce={enforce}")
    for f in findings:
        print(f"  WARN {f.render()}")
    return 0


# --- founding fixtures (detector exemplars, not retroactive flags) ---------
# Excerpts of the three founding violations, verbatim from the 2026-10-18
# bytes. The knot excerpt's one em dash is normalized to a plain hyphen per
# the no-em-dash law; the detector is insensitive to it. These live here so
# the selftest never depends on the live modules staying uncured.

FIXTURE_REDBOARD = """\
tools/redboard.py - one boot-time screen of what is red, for how long, and whose fix it is.

DFHack-style named tool (verb: redboard). Change #4 of
watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md: 8 scheduled tasks red, no
action logged, and memory/attention.md drowned by one alarm class.

  state/REDBOARD.md              the board (meter line first)
  state/REDBOARD.json            same rows, machine form (--json)
  memory/runs/redboard/runs.jsonl one receipt row per run
"""

FIXTURE_PALACE = """\
palace - the operator's ideation method as an estate organ.

The operator's own words (2026-10-13): "i read all of these minds... when i
think i remember what it is i know about a person and use empathy basically
their ocean model filtered through what i know about them and their demeanor
and life to make up a plausible story that helps me understand what they might
have done. i do this around shit all the time, sort of like a memory palace.
i want you to do this as well somehow."

This is that, as machinery. A person-model is an OCEAN vector + demeanor notes +
life context + sources, stored MACHINE-LOCAL under state/palace/ (gitignored,
same discipline as state/riddler/). The plausible-story generation is a lane:
the tool formats a story-ask from a model; a sensing-grade or better judge runs
it; stories rank by consistency with the known bytes. Every model carries
confidence and a falsifier field: what byte would update it.
"""

FIXTURE_KNOT = """\
W1 finding (2026-09-06, memory/runs/batch5_20260906/ORPHAN_LEDGER_20260906.md): chain
knots index the cage stream, not the CLI session db - 51/65 24h sessions ended with no
chain row. CURRENT.md critique: "knot-at-close bridge owed." This organ IS the bridge.
"""

FIXTURE_COMPLIANT = """\
compliant_example - an organ that obeys the consumer law.

Consumer: scripts/morning_brief.ps1 renders the meter line at logon.
Verifier: tests/test_consumer_gate.py battery (exits 1 when the meter lies).
"""


def selftest() -> int:
    """Founding-fixture battery, stdlib only. 0 = all pass, 1 = any fail."""
    checks: list[tuple[str, bool]] = []

    def expect(name: str, cond: bool) -> None:
        checks.append((name, bool(cond)))

    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)

        def write(name: str, body: str) -> Path:
            p = tdir / name
            p.write_text(f'"""{body}"""\n', encoding="utf-8")
            return p

        red = write("fixture_redboard.py", FIXTURE_REDBOARD)
        pal = write("fixture_palace.py", FIXTURE_PALACE)
        knot = write("fixture_knot_at_close.py", FIXTURE_KNOT)
        comp = write("fixture_compliant.py", FIXTURE_COMPLIANT)
        half = write(
            "fixture_half_declared.py",
            "half_declared - consumer named, verifier missing.\n\n"
            "Consumer: mag/rib_boot.py VAULT_RIBS mounts it at boot.\n",
        )
        # raw invalid syntax (docstring-wrapping it would make it a valid
        # bare-string module - the 12-check failure this comment now explains)
        broken = tdir / "fixture_broken.py"
        broken.write_text("def oops(:\n", encoding="utf-8")

        for label, p in (
            ("redboard fixture flagged", red),
            ("palace fixture flagged", pal),
            ("knot_at_close fixture flagged", knot),
            ("half-declared (verifier missing) flagged", half),
        ):
            f = check_module(p)
            expect(f"{label} (CONSUMER-MISSING)", f is not None and f.rule == "CONSUMER-MISSING")
        expect("compliant fixture clean", check_module(comp) is None)

        # malformed input is the blind class: must raise -> exit 2 upstream
        try:
            check_module(broken)
            expect("unparseable module raises ConsumerGateError", False)
        except ConsumerGateError:
            expect("unparseable module raises ConsumerGateError", True)

        # exit contract: WARN-only 0, --enforce 1 on findings, clean 0
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_warn = cmd_check([red], enforce=False)
            rc_enf = cmd_check([red], enforce=True)
            rc_clean = cmd_check([comp], enforce=True)
        out = buf.getvalue().splitlines()
        expect(f"warn-only exits 0 (got {rc_warn})", rc_warn == 0)
        expect(f"enforce flips to 1 (got {rc_enf})", rc_enf == 1)
        expect(f"clean module enforces to 0 (got {rc_clean})", rc_clean == 0)
        expect("green opens 'CONSUMER-GATE: ok'", out[0].startswith(f"{TOOL}: ok"))
        expect(
            "blocking opens 'CONSUMER-GATE: FAIL'",
            any(ln.startswith(f"{TOOL}: FAIL") for ln in out),
        )
        expect("warn rows carry the WARN prefix", any(ln.startswith("  WARN CONSUMER-MISSING") for ln in out))

    failed = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'} {n}")
    if failed:
        print(f"{TOOL}: ERROR selftest failed {len(failed)}/{len(checks)} checks")
        return 1
    print(
        f"{TOOL}: ok selftest {len(checks)}/{len(checks)} checks passed "
        f"(founding fixtures: tools/redboard.py, tools/palace.py, mag/knot_at_close.py)"
    )
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="consumer_gate", description=__doc__.splitlines()[0]
    )
    sub = ap.add_subparsers(dest="cmd")
    ck = sub.add_parser("check", help="flag NEW organ modules missing Consumer:/Verifier:")
    scope = ck.add_mutually_exclusive_group(required=True)
    scope.add_argument(
        "--changed", action="store_true",
        help="newly added .py modules vs HEAD under mag/ tools/ scripts/",
    )
    scope.add_argument("--files", nargs="+", help="explicit module paths")
    ck.add_argument(
        "--enforce", action="store_true",
        help="CONSUMER-MISSING blocks (exit 1); default is WARN-only (exit 0)",
    )
    sub.add_parser("selftest", help="run the founding-fixture battery")
    args = ap.parse_args(argv[1:])

    if args.cmd == "selftest":
        return selftest()
    if args.cmd != "check":
        ap.print_help()
        return 2
    if args.changed:
        modules = changed_new_modules()
        if modules is None:
            print(f"{TOOL}: ERROR git failed, refusing to guess the changed set")
            return 2
    else:
        modules = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = (ESTATE_ROOT / f).resolve()
            if p.suffix != ".py":
                print(f"{TOOL}: ERROR not a .py module: {f}")
                return 2
            if not p.is_file():
                print(f"{TOOL}: ERROR module not found: {f}")
                return 2
            modules.append(p)
    return cmd_check(modules, args.enforce)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
