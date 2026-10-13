#!/usr/bin/env python3
"""violation_ratchet.py — fingerprint-ratcheted violation gate over estate code.

Recreated from the zai-org/ZCode architecture gate's shapes (Picasso law: our own
hand, our own rules — no imported code). Law: debt that exists today is a REGISTERED
CLAIM in the baseline; only NEW violations fail. The register can only grow by a
human/agent running baseline-update, never silently. Debt that gets fixed leaves via
prune, so the register trends down.

Prune only reaps claims inside the scanner's own domain (rule in SCANNER_RULES and
file under a scan root). Claims registered from other surfaces under namespaced
rules the scanner cannot emit (e.g. the mimosa-* claims over watch/inbox/, a tree
the scanner never scans) are underivable by construction and are kept by every
prune; external debt leaves the register only by explicit re-triage, never by a
silent reap. B2-95 closed this after a routine prune reaped all 25 mimosa claims
B2-11 had registered (receipts: watch/inbox/burn_wave_20260926/B2_11_mimosa_close_20260926.md
falsifier, watch/inbox/burn_wave_20260926/B2_95_prune_gap_20260926.md).

Fingerprints are sha256(rule NUL file NUL detail), first 16 hex. Detail is
deliberately line-free so unrelated edits don't churn the register; one fingerprint
per (rule, file) — the ratchet's teeth are "no NEW file acquires this disease".

Usage:
  python tools/violation_ratchet.py check [--changed]
  python tools/violation_ratchet.py baseline-update [--by WHO] [--note NOTE]
  python tools/violation_ratchet.py prune

Exit codes: 0 = pass (no new violations), 1 = new violations found, 2 = gate itself broken.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ESTATE_ROOT / "configs" / "violation_baseline.json"
DEFAULT_ROOTS = ["mag", "tools"]
FILE_LINE_CAP = 400

# Rules the scanner itself can emit (violations_in below). An accepted claim
# whose rule is outside this set, or whose file sits outside DEFAULT_ROOTS, can
# never be re-derived by a scan, so prune treats it as externally sourced and
# keeps it (B2-95, 2026-09-26): external debt leaves the register only by
# explicit re-triage, never by a silent reap.
SCANNER_RULES = {
    "unreadable",
    "file-too-long",
    "parse-error",
    "bare-except",
    "except-pass",
    "shell-true",
    "env-key-read",
    "cwd-relative-path",
    "todo-undated",
}


def scanner_domain(rule: str, file: str) -> bool:
    """True when a full scan could re-derive a claim with this (rule, file)."""
    if rule not in SCANNER_RULES:
        return False
    return any(file.startswith(root + "/") for root in DEFAULT_ROOTS)

# An accepted entry with "expires": "YYYY-MM-DD" counts as a violation once the
# date passes — exceptions rot into violations instead of silently living forever.
#
# B2-273 (2026-09-26), the growth law: a file-too-long claim's detail is
# line-free, so after acceptance the claim silently absorbs unbounded growth
# (the observed 427-to-453 same-day drift). Law chosen: baseline-update stamps
# the accepted size (accepted_lines) into the claim, and check prints a GROWTH
# line whenever a scanned accepted file-too-long claim now measures more lines
# than it was accepted at. Growth stays non-blocking (the accepted claim still
# passes the ratchet) but is always a visible ledger fact, and the cure is a
# named re-acceptance or a split.
TODAY = date.today().isoformat()


def fingerprint(rule: str, file: str, detail: str) -> str:
    return hashlib.sha256(f"{rule}\0{file}\0{detail}".encode("utf-8")).hexdigest()[:16]


def iter_py_files(roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        base = ESTATE_ROOT / root
        if not base.is_dir():
            continue
        # rglob, not glob: the full scan must see subdirectory files too, or
        # subdir debt (tools/gps_mcp/*) can never register and check --changed
        # stays permanently red for it - caught at the fix-everything fold
        # 2026-10-01 (full-tree PASS while --changed flagged gps_mcp rows).
        files.extend(sorted(p for p in base.rglob("*.py") if p.is_file()))
    return files


def changed_files() -> list[Path] | None:
    """Files modified vs HEAD plus untracked, filtered to scan roots. None = git broke."""
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ESTATE_ROOT, capture_output=True, text=True, timeout=60,
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=ESTATE_ROOT, capture_output=True, text=True, timeout=60,
        )
        if diff.returncode != 0 or untracked.returncode != 0:
            return None
    except (OSError, subprocess.TimeoutExpired):
        return None
    roots = set(DEFAULT_ROOTS)
    out = []
    for line in diff.stdout.splitlines() + untracked.stdout.splitlines():
        rel = line.strip().replace("\\", "/")
        if rel.endswith(".py") and rel.split("/")[0] in roots:
            out.append(ESTATE_ROOT / rel)
    return sorted(set(out))


ENV_EXEMPT_FILES = {"mag/key_law.py", "models/env_load.py"}
ENV_KEY_NAME = re.compile(r"[A-Z_]*(API|TOKEN|SECRET|_KEY|KEY_)[A-Z_]*")


def _is_os_environ(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "os"
        and node.attr == "environ"
    )


def violations_in(path: Path) -> list[dict]:
    """All rule hits in one file. detail is line-free for register stability."""
    rel = path.relative_to(ESTATE_ROOT).as_posix()
    found: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [{"rule": "unreadable", "file": rel, "detail": f"oserror: {type(e).__name__}", "line": 0}]
    n_lines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
    if n_lines > FILE_LINE_CAP:
        found.append({"rule": "file-too-long", "file": rel, "detail": f">{FILE_LINE_CAP} lines", "line": n_lines})
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        found.append({"rule": "parse-error", "file": rel, "detail": f"ast: {e.msg}", "line": e.lineno or 0})
        return found
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                found.append({"rule": "bare-except", "file": rel, "detail": "silent except:", "line": node.lineno})
            elif len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                found.append({"rule": "except-pass", "file": rel, "detail": "silent except ...: pass", "line": node.lineno})
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    found.append({"rule": "shell-true", "file": rel, "detail": "subprocess shell=True", "line": node.lineno})
            # env-key-read: os.getenv("..."), os.environ.get("...")
            fname = node.func
            key_arg = None
            if isinstance(fname, ast.Attribute) and fname.attr == "getenv" \
                    and isinstance(fname.value, ast.Name) and fname.value.id == "os" \
                    and node.args and isinstance(node.args[0], ast.Constant):
                key_arg = node.args[0].value
            elif isinstance(fname, ast.Attribute) and fname.attr == "get" and _is_os_environ(fname.value) \
                    and node.args and isinstance(node.args[0], ast.Constant):
                key_arg = node.args[0].value
            if isinstance(key_arg, str) and ENV_KEY_NAME.search(key_arg) and rel not in ENV_EXEMPT_FILES:
                found.append({"rule": "env-key-read", "file": rel, "detail": f"direct env read: {key_arg}", "line": node.lineno})
        if isinstance(node, ast.Subscript) and _is_os_environ(node.value):
            # env-key-read: os.environ["..."]
            sl = node.slice
            if isinstance(sl, ast.Constant) and isinstance(sl.value, str) \
                    and ENV_KEY_NAME.search(sl.value) and rel not in ENV_EXEMPT_FILES:
                found.append({"rule": "env-key-read", "file": rel, "detail": f"direct env read: {sl.value}", "line": node.lineno})
    # cwd-relative-path: module-level NAME = Path("relative/literal")
    for stmt in tree.body:
        targets: list[ast.AST] = []
        value = None
        if isinstance(stmt, ast.Assign):
            targets, value = stmt.targets, stmt.value
        elif isinstance(stmt, ast.AnnAssign):
            targets, value = [stmt.target], stmt.value
        if value is None or not (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "Path"):
            continue
        if value.args and isinstance(value.args[0], ast.Constant) and isinstance(value.args[0].value, str):
            lit = value.args[0].value
            if lit and not Path(lit).is_absolute() and not lit.startswith(("/", "\\\\")) and not re.match(r"^[A-Za-z]:", lit):
                found.append({"rule": "cwd-relative-path", "file": rel, "detail": f"module-level Path({lit!r}) is cwd-dependent", "line": stmt.lineno})
    for i, line in enumerate(text.splitlines(), 1):
        head = line.split("#", 1)
        if len(head) == 2 and re.search(r"\b(TODO|FIXME)\b", head[1]) and not re.search(r"\d{4}", head[1]):
            found.append({"rule": "todo-undated", "file": rel, "detail": "TODO/FIXME without a year", "line": i})
    return found


def all_violations(paths: list[Path] | None = None) -> list[dict]:
    files = paths if paths is not None else iter_py_files(DEFAULT_ROOTS)
    hits: list[dict] = []
    for p in files:
        hits.extend(violations_in(p))
    # one fingerprint per (rule, file): collapse to the first occurrence
    seen: set[tuple[str, str]] = set()
    unique: list[dict] = []
    for v in hits:
        key = (v["rule"], v["file"])
        if key not in seen:
            seen.add(key)
            unique.append(v)
    return unique


def load_baseline() -> dict:
    if not BASELINE_PATH.exists():
        return {"version": 1, "updated": None, "accepted": {}}
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def save_baseline(b: dict) -> None:
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    b["updated"] = datetime.now().isoformat(timespec="seconds")
    BASELINE_PATH.write_text(json.dumps(b, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def expired_fps(baseline: dict) -> dict[str, dict]:
    out = {}
    for fp, entry in baseline.get("accepted", {}).items():
        exp = entry.get("expires")
        if exp and exp < TODAY:
            out[fp] = entry
    return out


def cmd_check(changed_only: bool) -> int:
    paths = None
    if changed_only:
        paths = changed_files()
        if paths is None:
            print("RATCHET check: git failed — refusing to guess the changed set (exit 2)")
            return 2
    viols = all_violations(paths)
    baseline = load_baseline()
    accepted = baseline.get("accepted", {})
    new = [v for v in viols if fingerprint(v["rule"], v["file"], v["detail"]) not in accepted]
    expired = list(expired_fps(baseline).values())
    registered = len(viols) - len(new)
    scope = f"{len(paths)} changed files" if changed_only else f"{len(iter_py_files(DEFAULT_ROOTS))} files (all)"
    print(
        f"RATCHET check: scope={scope}; hits={len(viols)}; registered={registered}; "
        f"NEW={len(new)}; expired-exceptions={len(expired)}"
    )
    for v in new:
        fp = fingerprint(v["rule"], v["file"], v["detail"])
        print(f"  NEW {fp} {v['rule']}: {v['file']}:{v['line']} — {v['detail']}")
    for e in expired:
        print(f"  EXPIRED exception: {e.get('file','?')} — {e.get('detail','?')} (was accepted, expired {e.get('expires')})")
    # B2-273 growth law: accepted file-too-long claims that now measure more
    # lines than at acceptance are a visible ledger fact (never silent).
    for v in viols:
        if v["rule"] != "file-too-long":
            continue
        fp = fingerprint(v["rule"], v["file"], v["detail"])
        entry = accepted.get(fp)
        if not isinstance(entry, dict):
            continue
        base_lines = entry.get("accepted_lines")
        if isinstance(base_lines, int) and isinstance(v.get("line"), int) and v["line"] > base_lines:
            print(f"  GROWTH claim {fp}: {v['file']} accepted at {base_lines} lines, "
                  f"now {v['line']} (+{v['line'] - base_lines}) — re-audit or re-accept by name")
    if new or expired:
        print(f"RATCHET: FAIL — run 'baseline-update' ONLY after a human/agent accepts the debt by name.")
        return 1
    print("RATCHET: PASS — no unregistered debt.")
    return 0


def cmd_baseline_update(by: str, note: str) -> int:
    viols = all_violations()
    baseline = load_baseline()
    accepted = baseline.setdefault("accepted", {})
    added = 0
    for v in viols:
        fp = fingerprint(v["rule"], v["file"], v["detail"])
        if fp not in accepted:
            entry = {
                "rule": v["rule"], "file": v["file"], "detail": v["detail"],
                "accepted": TODAY, "by": by, "note": note,
            }
            if v["rule"] == "file-too-long" and isinstance(v.get("line"), int):
                # B2-273 growth law: freeze the accepted size so later growth
                # is a visible ledger fact (check prints the GROWTH line).
                entry["accepted_lines"] = v["line"]
            accepted[fp] = entry
            added += 1
    save_baseline(baseline)
    print(f"RATCHET baseline-update: hits={len(viols)}; already-registered={len(viols)-added}; ADDED={added}")
    # Cause (ball3 driver-meter 2026-09-29): this print called
    # BASELINE_PATH.relative_to(ESTATE_ROOT) and raised ValueError when the
    # baseline sat outside the estate (the wave5 suite-burn run used an
    # out-of-repo pytest basetemp:
    # watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt,
    # test_baseline_update_stamps_accepted_lines). Print-only line; with the
    # default in-repo baseline the output is byte-identical.
    try:
        shown = BASELINE_PATH.relative_to(ESTATE_ROOT).as_posix()
    except ValueError:
        shown = BASELINE_PATH.as_posix()
    print(f"  register now holds {len(accepted)} claims → {shown}")
    return 0


def cmd_prune() -> int:
    baseline = load_baseline()
    live = {fingerprint(v["rule"], v["file"], v["detail"]) for v in all_violations()}
    accepted = baseline.get("accepted", {})
    before = len(accepted)
    # B2-95 (2026-09-26): prune used to delete any accepted claim its fingerprint
    # could not re-derive. Externally sourced claims (namespaced rules like the
    # mimosa-* set B2-11 registered over watch/inbox/, a tree the scanner never
    # scans) are underivable by construction, so every prune reaped them; the
    # B2-11 falsifier named this reap in advance and a same-day prune took all
    # 25. Only scanner-domain debt leaves via prune now.
    external = sum(
        1 for entry in accepted.values()
        if not scanner_domain(entry.get("rule", ""), entry.get("file", ""))
    )
    dead = [
        fp for fp, entry in accepted.items()
        if scanner_domain(entry.get("rule", ""), entry.get("file", "")) and fp not in live
    ]
    for fp in dead:
        del accepted[fp]
    save_baseline(baseline)
    print(
        f"RATCHET prune: register={before}; fixed-debt-removed={len(dead)}; "
        f"external-kept={external}; register now {len(accepted)}"
    )
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"check", "baseline-update", "prune"}:
        print(__doc__)
        return 2
    if argv[1] == "check":
        return cmd_check("--changed" in argv)
    if argv[1] == "baseline-update":
        by = "operator"
        note = ""
        if "--by" in argv:
            by = argv[argv.index("--by") + 1]
        if "--note" in argv:
            note = argv[argv.index("--note") + 1]
        return cmd_baseline_update(by, note)
    return cmd_prune()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
