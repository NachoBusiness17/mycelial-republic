#!/usr/bin/env python3
"""gate_canary.py - pre-push gate-liveness canary (Mickey17 W2, return 7/24).

Concept (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md line 49, RETURN 7):
plants one known-bad per gate family in a throwaway git worktree of HEAD,
runs each pre-push gate with the exact command the hook uses, and requires
the gate to FIRE (its own named detection per the exit contracts in
githooks/pre-push). A gate silent on its own known-bad is dead and the
canary appends an attention alert naming it: silence files its own death
receipt. Known-bads are ONLY artifacts the gates define as test-safe: the
planted provider token is obviously fake (ghp_ prefix + 36 'A', built by
concatenation so this source never holds a provider-shaped run); the rest
are stale dates, unpinned text, a dropped ledger row. No real secret ever.

Safety: read-only on the real tree (all planting in the throwaway worktree,
removed after; the ONE sanctioned real write is the memory/attention.md
append a DEAD gate mints); families run isolated (plant, run, restore) so a
firing is attributable to its own known-bad.

Usage: .venv/Scripts/python.exe tools/gate_canary.py [--repo PATH]
          [--workroot PATH] [--attention PATH] [--only a,b] [--keep]
Exit 0 = every family fired; 1 = dead or blind family (attention appended);
2 = cannot verify (setup failed).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable, Optional

REPO = Path(__file__).resolve().parent.parent
NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0
SPARSE_DIRS = ["tools", "configs", "scripts", "tests", "mag", "memory/workflows",
               "watch/inbox/burn_wave_20260926", "watch/inbox/qdrop_export",
               "memory/burns"]
SENTINELS = [
    "AGENTS.md", "tools/secret_gate.py", "tools/workflow_gate.py", "tools/refold_gate.py",
    "tools/prepush_paths_changed.py", "configs/.config_seal.json", "configs/violation_baseline.json",
    "configs/secret_gate_baseline.json", "configs/tools/description_pin.json",
    "configs/workflow_gate_scenarios/G1_multiplicity.card.json", "memory/workflows/REGISTRY.jsonl",
    "scripts/index_fold_host.mjs", "scripts/the50_t21_q_caption_ledger_verify.py",
    "tests/test_index_fold_host.py", "watch/inbox/burn_wave_20260926/QUEUE.md",
    "watch/inbox/qdrop_export/q_caption_ledger.jsonl"]
SNAPSHOT_SCOPES = ["AGENTS.md", "configs", "tools", "scripts", "githooks", "tests", "watch", "memory"]
FAKE_GH_TOKEN = "ghp_" + "A" * 36  # obviously fake; never a real credential

class CanaryError(Exception):
    """Setup or run failure that means the canary cannot verify."""

class PlantError(Exception):
    """The HEAD bytes do not hold the shape a plant expects."""


def _git(repo: Path, *args: str, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          text=True, errors="replace", timeout=timeout,
                          creationflags=NO_WINDOW)


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _write(wt: Path, rel: str, text: str) -> list[str]:
    (wt / rel).write_text(text, encoding="utf-8", newline="\n")
    return [rel]


def _append(wt: Path, rel: str, text: str) -> list[str]:
    with (wt / rel).open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return [rel]


def plant_census(wt: Path) -> list[str]:
    text = _read(wt / "AGENTS.md")
    new = re.sub(r"\(\d{4}-\d{2}-\d{2} census", "(2026-09-01 census", text, count=1)
    if new == text:
        raise PlantError("no census clause found in AGENTS.md carrier")
    return _write(wt, "AGENTS.md", new)


def plant_checkbox(wt: Path) -> list[str]:
    rel = "watch/inbox/burn_wave_20260926/QUEUE.md"
    lines = _read(wt / rel).splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip().lower() == "## open":
            lines.insert(i + 1, "- [x] B2-9999 gate canary row, no receipt anywhere\n")
            return _write(wt, rel, "".join(lines))
    raise PlantError("no ## Open heading in QUEUE.md")


def plant_caption(wt: Path) -> list[str]:
    _append(wt, "scripts/the50_t21_q_caption_ledger.py",
            "\n# gate_canary arming byte (planted)\n")
    rel = "watch/inbox/qdrop_export/q_caption_ledger.jsonl"
    rows = [ln for ln in _read(wt / rel).splitlines() if ln.strip()]
    return _write(wt, rel, "\n".join(rows[:-1]) + "\n")  # drop last row: check6 FAIL


# The B2-279 falsifier: this tier swap makes the 2^53 band outrank exact seqs.
_REFOLD_MUTATIONS = [
    ("if (Number.isSafeInteger(s)) return { tier: 2, seq: BigInt(s) };",
     "if (Number.isSafeInteger(s)) return { tier: 1, seq: BigInt(s) };"),
    ("if (Number.isInteger(s)) return { tier: 1, seq: BigInt(s) };",
     "if (Number.isInteger(s)) return { tier: 2, seq: BigInt(s) };"),
    ("if (typeof s === 'string' && /^\\d+$/.test(s)) return { tier: 2, seq: BigInt(s) };",
     "if (typeof s === 'string' && /^\\d+$/.test(s)) return { tier: 1, seq: BigInt(s) };"),
]


def plant_refold(wt: Path) -> list[str]:
    text = _read(wt / "scripts/index_fold_host.mjs")
    for old, new in _REFOLD_MUTATIONS:
        if text.count(old) != 1:
            raise PlantError("fold-host tier line not unique: %r" % old[:44])
        text = text.replace(old, new)
    return _write(wt, "scripts/index_fold_host.mjs", text)


def plant_wgate(wt: Path) -> list[str]:
    _append(wt, "tools/workflow_gate.py", "\n# gate_canary arming byte (planted)\n")
    rel = "configs/workflow_gate_scenarios/G1_multiplicity.card.json"
    card = json.loads(_read(wt / rel))
    card["expected_verdict"]["overall"] = "PASS"
    return _write(wt, rel, json.dumps(card, indent=2) + "\n")


def _has(rc_out: tuple[int, str], *needles: str, rc: Optional[int] = None) -> Optional[str]:
    got_rc, out = rc_out
    if (rc is not None and got_rc != rc) or any(n not in out for n in needles):
        return None
    for line in out.splitlines():
        if all(n in line for n in needles):
            return line.strip()
    return out.strip().splitlines()[0] if out.strip() else None


@dataclasses.dataclass
class Step:
    argv: list[str]
    fired: Callable[[tuple[int, str]], Optional[str]]
    timeout: int = 300


@dataclasses.dataclass
class Family:
    name: str
    note: str
    plant: Callable[[Path], list[str]]
    steps: list[Step]
    control_skip: bool = False  # argv references planted-only artifacts


def _armed(*paths: str) -> Step:
    return Step(["tools/prepush_paths_changed.py", "--refs", "", "--", *paths],
                lambda ro: "changed-path arm on" if ro[0] == 1 else None, timeout=60)


FAMILIES = [
    Family("violation_ratchet", "ENFORCING: NEW violation in a changed tools/ file",
           lambda wt: _write(wt, "tools/gate_canary_bad_ratchet.py",
                             "# canary known-bad: silent except for the ratchet\n"
                             "try:\n    value = 1\nexcept Exception:\n    pass\n"),
           [Step(["tools/violation_ratchet.py", "check", "--changed"],
                 lambda ro: _has(ro, "RATCHET: FAIL", "NEW", "except-pass", rc=1))]),
    Family("config_seal", "ENFORCING: modified sealed config byte",
           lambda wt: _append(wt, "configs/lanes.yaml",
                              "\n# gate_canary drift byte (planted)\n"),
           [Step(["tools/config_seal.py", "verify"],
                 lambda ro: _has(ro, "CONFIG-SEAL: FAIL", "MODIFIED", rc=1))]),
    Family("secret_gate", "ENFORCING: fake ghp_ provider token in a changed file",
           lambda wt: _write(wt, "tools/gate_canary_bad_secret.py",
                             "# canary known-bad: obviously fake provider token\n"
                             "PLANTED = %r\n" % FAKE_GH_TOKEN),
           [Step(["tools/secret_gate.py", "--changed", "--baseline",
                  "configs/secret_gate_baseline.json"],
                 lambda ro: _has(ro, "GITHUB-TOKEN", "exit=1", rc=1), timeout=600)]),
    Family("census_drift_patrol", "WARN/exit2 split: stale AGENTS.md census carrier",
           plant_census,
           [Step(["tools/census_drift_patrol.py"],
                 lambda ro: _has(ro, "CENSUS-PATROL: STALE", rc=1))]),
    Family("freshness_gate", "WARN-only: stale receipt stamp",
           lambda wt: _write(wt, "watch/inbox/gate_canary_stale_receipt.md",
                             "# canary stale receipt\n\nsource-fetched: 2026-01-01\n"
                             "\nstale claim\n"),
           [Step(["tools/freshness_gate.py", "watch/inbox/gate_canary_stale_receipt.md"],
                 lambda ro: _has(ro, "FRESHNESS-GATE: FAIL", rc=2))], control_skip=True),
    Family("checkbox_receipt_gate", "WARN: checked Open row with no receipt",
           plant_checkbox,
           [Step(["tools/checkbox_receipt_gate.py"],
                 lambda ro: _has(ro, "CHECKBOX-RECEIPT-GATE: FAIL", "B2-9999", rc=1))]),
    Family("description_pin", "WARN-only: unpinned tool manifest",
           lambda wt: _write(wt, "configs/tools/gate_canary_unpinned.json",
                             json.dumps({"tools": [{"name": "canary_tool",
                             "description": "does canary things, no version"}]},
                             indent=1) + "\n"),
           [Step(["tools/description_pin.py", "configs/tools"],
                 lambda ro: _has(ro, "canary_tool", "unpinned", rc=2))]),
    Family("caption_ledger_verify", "WARN conditional: armed + missing ledger row",
           plant_caption,
           [_armed("scripts/the50_t21_q_caption_ledger.py",
                   "scripts/the50_t21_q_caption_ledger_verify.py"),
            Step(["scripts/the50_t21_q_caption_ledger_verify.py"],
                 lambda ro: _has(ro, "RESULT: FAIL"))], control_skip=True),
    Family("refold_gate", "WARN conditional: B2-279 tier-swap fold mutation",
           plant_refold,
           [Step(["tools/refold_gate.py"],
                 lambda ro: _has(ro, "REFOLD-GATE: FAIL", rc=1), timeout=600)]),
    Family("workflow_gate_scenarios", "ENFORCING conditional: armed + red card",
           plant_wgate,
           [_armed("tools/workflow_gate.py"),
            Step(["tools/workflow_gate.py", "check", "--scenarios",
                  "configs/workflow_gate_scenarios"],
                 lambda ro: _has(ro, "SCENARIOS FAIL", rc=2))]),
]


def setup_worktree(repo: Path, workroot: Path, sparse: Optional[list[str]] = None,
                   venv_link: bool = True) -> tuple[Path, str, list[str]]:
    notes: list[str] = []
    workroot.mkdir(parents=True, exist_ok=True)
    wt = Path(tempfile.mkdtemp(prefix="gate_canary_", dir=str(workroot)))
    r = _git(repo, "worktree", "add", "--detach", "--no-checkout", str(wt), "HEAD")
    if r.returncode != 0:
        raise CanaryError("git worktree add failed: %s" % r.stderr.strip()[:300])
    dirs = SPARSE_DIRS if sparse is None else sparse
    if dirs:
        for cmd in (("sparse-checkout", "init", "--cone"),
                    ("sparse-checkout", "set", *dirs)):
            r = _git(wt, *cmd)
            if r.returncode != 0:
                raise CanaryError("sparse %s failed: %s" % (cmd[1], r.stderr.strip()[:200]))
    _git(wt, "config", "core.autocrlf", "false")  # byte-faithful checkout: smudged
    # CRLF broke caption check8 and config_seal hashes in worktrees (2026-09-29)
    r2 = _git(wt, "reset", "--hard", "HEAD")
    if r2.returncode != 0:
        raise CanaryError("worktree checkout failed: %s" % r2.stderr.strip()[:300])
    if sparse is None:  # real-run sentinel check (fixtures pass their own tree)
        missing = [s for s in SENTINELS if not (wt / s).is_file()]
        if missing:
            raise CanaryError("worktree missing sentinels: %s" % missing)
    venv_py = wt / ".venv" / "Scripts" / "python.exe"
    interpreter, linked = sys.executable, False
    if venv_link and (repo / ".venv").is_dir() and not venv_py.is_file():
        lj = subprocess.run(["cmd", "/c", "mklink", "/J", str(wt / ".venv"),
                             str(repo / ".venv")], capture_output=True, text=True)
        linked = lj.returncode == 0 and venv_py.is_file()
        if linked:
            notes.append("venv junction linked (secret_gate venv check armed)")
        else:
            notes.append("venv junction failed; secret gate may fail its venv check")
    if venv_py.is_file():
        interpreter = str(venv_py)
    elif not linked:
        notes.append("no worktree venv; running on this interpreter")
    return wt, interpreter, notes


def teardown_worktree(repo: Path, wt: Path) -> None:
    r = _git(repo, "worktree", "remove", "--force", str(wt))
    if r.returncode != 0:
        shutil.rmtree(wt, ignore_errors=True)
        _git(repo, "worktree", "prune")


def run_step(wt: Path, interpreter: str, step: Step) -> tuple[int, str]:
    try:
        p = subprocess.run([interpreter, *step.argv], cwd=str(wt),
                           capture_output=True, text=True, errors="replace",
                           timeout=step.timeout, creationflags=NO_WINDOW)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "GATE-CANARY: step timed out after %ss: %s" % (step.timeout, " ".join(step.argv))
    except OSError as e:
        return 127, "GATE-CANARY: cannot run step: %s" % e


def restore(wt: Path, touched: list[str]) -> None:
    if not touched:
        return
    tracked = _git(wt, "ls-files", "--", *touched)
    keep = set(tracked.stdout.split()) if tracked.returncode == 0 else set()
    for rel in touched:
        if rel in keep:
            _git(wt, "checkout", "--", rel, timeout=120)
        elif (wt / rel).exists():
            (wt / rel).unlink()


def run_family(fam: Family, wt: Path, interpreter: str, plant: bool = True) -> dict:
    touched: list[str] = []
    try:
        if plant:
            touched = fam.plant(wt)
        rows = []
        for s in fam.steps:
            rc, out = run_step(wt, interpreter, s)
            rows.append({"argv": s.argv, "rc": rc,
                         "fired": s.fired((rc, out)), "out": out})
    except PlantError as e:
        return {"name": fam.name, "note": fam.note, "state": "BLIND",
                "error": "plant failed: %s" % e, "steps": []}
    finally:
        if plant:
            restore(wt, touched)
    blind = any(r["rc"] in (124, 127) or "Traceback (most recent call last)" in r["out"]
                or "can't open file" in r["out"] for r in rows)
    state = ("ALIVE" if all(r["fired"] is not None for r in rows)
             else "BLIND" if blind else "DEAD")
    return {"name": fam.name, "note": fam.note, "state": state, "steps": rows}


def snapshot(repo: Path, exclude_rel: str = "") -> dict[str, tuple[int, int]]:
    r = _git(repo, "ls-files", "-z", "--", *SNAPSHOT_SCOPES)
    if r.returncode != 0:
        raise CanaryError("git ls-files failed: %s" % r.stderr.strip()[:200])
    out: dict[str, tuple[int, int]] = {}
    for rel in r.stdout.split("\0"):
        if not rel or rel == exclude_rel:
            continue
        try:
            st = (repo / rel).stat()
            out[rel] = (st.st_mtime_ns, st.st_size)
        except OSError:
            out[rel] = (-1, -1)
    return out


def append_attention(path: Path, dead: list[dict]) -> None:
    stamp = time.strftime("%Y-%m-%d %H:%M")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        for r in dead:
            fh.write("- [priority][gate-canary] %s %s: stayed silent on its own "
                     "known-bad (%s) canary run %s; githooks/pre-push liveness "
                     "receipt owed\n" % (r["state"], r["name"], r["note"], stamp))


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="gate_canary",
                                 description="pre-push gate-liveness canary")
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--workroot", default=tempfile.gettempdir())
    ap.add_argument("--attention", default=None)
    ap.add_argument("--only", default=None, help="comma-separated family names")
    ap.add_argument("--keep", action="store_true", help="keep the worktree")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    attention = (Path(args.attention) if args.attention
                 else repo / "memory" / "attention.md")
    only = set(filter(None, (args.only or "").split(",")))
    families = [f for f in FAMILIES if not only or f.name in only]
    before = snapshot(repo, exclude_rel="memory/attention.md")
    wt, interpreter, notes = setup_worktree(repo, Path(args.workroot))
    try:
        for n in notes:
            print("note: %s" % n)
        controls = [None if f.control_skip
                    else run_family(f, wt, interpreter, plant=False)
                    for f in families]
        results = [run_family(f, wt, interpreter, plant=True) for f in families]
    finally:
        if args.keep:
            print("keep: worktree left at %s" % wt)
        else:
            teardown_worktree(repo, wt)
    after = snapshot(repo, exclude_rel="memory/attention.md")
    taint = [k for k in before if before.get(k) != after.get(k)]
    dead = [r for r in results if r["state"] != "ALIVE"]
    print("GATE-CANARY: %d families, throwaway worktree on HEAD" % len(families))
    for c, r in zip(controls, results):
        dirty = "" if c is None or c["state"] != "ALIVE" else " (control fired at HEAD!)"
        print("  %-24s %s%s  %s" % (r["name"], r["state"], dirty, r["note"]))
        if r.get("error"):
            print("    error=%s" % r["error"])
        for s in r["steps"]:
            print("    rc=%s fired=%s" % (s["rc"], (s["fired"] or "SILENT on its known-bad")[:120]))
            if s["fired"] is None and s["out"].strip():
                print("      tail: %s" % " | ".join(s["out"].strip().splitlines()[-2:])[:180])
    if dead:
        append_attention(attention, dead)
        for r in dead:
            print("GATE-CANARY: attention alert filed for %s (%s)" % (r["name"], r["state"]))
    if taint:
        print("GATE-CANARY: WARN real-tree movement during run (sibling lanes share"
              " this tree; the canary writes only temp + attention): %s" % taint[:6])
    print("GATE-CANARY: real tree snapshotted (%d tracked paths)" % len(before))
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
