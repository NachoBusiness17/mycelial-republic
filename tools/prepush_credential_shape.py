#!/usr/bin/env python3
"""prepush_credential_shape.py - credential-SHAPE scan over changed content.

Lane row (cause + evidence): memory/runs/mickey17_v2/runs/run-0/lanes/
a11-commits.json row index 4, key dd44a33dcafe (the leak-audit row). That lane
grepped both full diffs of the campaign commits with a fixed shape set
(sk- 16+, xai-, AIza, gsk_, Bearer 15+, api_key=val, password=, BEGIN PRIVATE
KEY) and got zero hits because keys are env-resolved at runtime; the same row
found a NEW leak class the shape set missed: the operator home path under
C:/Users/<name> embedded 3 times in a committed receipt
(watch/inbox/hermes_burn/SUBSTANCE_48h_synthesis.md). The row's own steal
names the landing spot: "extend the pre-push leak pass with an
operator-home-path grep (the operator's C:-Users literal, spelled in the
OPERATOR-HOME-PATH rule below, over the pushed range) alongside the
credential-shape regexes; landing: githooks/pre-push next edit". This tool is
that landing; the grep lives in the OPERATOR-HOME-PATH rule (a regex over
C: + separator + Users + separator + the operator name), so this docstring
cites the steal without re-planting the literal it catches - the first
landing's verbatim quote tripped the tool on its own bytes (receipt
watch/inbox/go_wave_20261004/prepush_instruments.md), which is the masking
discipline in miniature.

Scope: changed/staged content only, the secret_gate fast path (upstream..HEAD
diff when an upstream is configured, plus staged, unstaged and untracked
worktree files) - a full-tree scan in pre-push is a gate nobody keeps (pack
section 9, watch/inbox/PACK_SECRET_GATE_20260926.md).

Masking law (secret_gate convention): findings print a masked value head only,
never the full token.

Value-shape gates: the row's literal greps (xai-, AIza, api_key=val) were
diff-scoped, but this scan covers prose files too, so each prefix rule below
requires a plausible value length after it; a prose mention of the pattern
name ("api_key=val") with no value-sized token stays out of the WARN channel.
Deviations from the row's literal greps are named per-rule below.

Zero baseline day one (citation_lint precedent): configs/
prepush_credential_baseline.json starts absent; a finding may be accepted by
NAME (fingerprint) into it after triage, never mass-imported.

WARN-ONLY first landing per the t40/B2-215 house pattern: the hook prints this
tool's output as a WARN and never blocks a push; flip to enforce is an
operator call.

Exit codes: 0 = no unaccepted findings; 1 = findings (the WARN payload);
2 = cannot verify (git failure).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
# Anchored to ESTATE_ROOT (violation_ratchet cwd-relative-path class, first
# landing: the bare Path("configs/...") literal sat at module scope and the
# ratchet named it; a push hook runs from the repo root but the tool must not
# depend on that). main() still re-resolves a RELATIVE --baseline against
# --root so tmp-root tests keep working.
DEFAULT_BASELINE = ESTATE_ROOT / "configs/prepush_credential_baseline.json"
MAX_FILE_BYTES = 2_000_000  # per-file cap; bigger files are skipped and counted
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

# One (name, compiled shape, note) per row grep. The note names the row's
# literal grep and any deviation.
SHAPES: list[tuple[str, "re.Pattern[str]", str]] = [
    ("OPENAI-SK", re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
     "row grep sk-[16+]; unchanged"),
    ("XAI-KEY", re.compile(r"\bxai-[A-Za-z0-9_-]{12,}"),
     "row grep xai-; +12-char value gate for prose scope"),
    ("GOOGLE-AIZA", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}"),
     "row grep AIza; +30-char value gate (real keys are 39 chars)"),
    ("GROQ-GSK", re.compile(r"\bgsk_[A-Za-z0-9]{20,}"),
     "row grep gsk_; +20-char value gate"),
    ("BEARER-TOKEN", re.compile(r"[Bb]earer[ \t]+[A-Za-z0-9._~+/=-]{15,}"),
     "row grep Bearer+15; unchanged"),
    ("KV-ASSIGN", re.compile(
        r"\b(api[_-]?key|password)[\"']?[ \t]*[:=][ \t]*[\"']?[^\s\"']{8,}",
        re.IGNORECASE),
     "row greps api_key=val, password=; +8-char value gate, underscore/hyphen "
     "spelling added"),
    ("PRIVATE-KEY-BLOCK", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
     "row grep BEGIN PRIVATE KEY; widened to RSA/EC/OPENSSH headers"),
    ("GITHUB-PAT", re.compile(r"\bghp_[A-Za-z0-9]{30,}"),
     "ouroboros R3 move 6 (2026-10-05): the GitHub PAT family scanned clean "
     "(ghp_ + 30-char value gate; classic PATs carry 36)"),
    ("AWS-AKIA", re.compile(r"\bAKIA[0-9A-Z]{16}(?![0-9A-Z])"),
     "ouroboros R3 move 6 (2026-10-05): the AWS access-key family scanned "
     "clean (AKIA + 16 uppercase alnum, the exact key-id shape)"),
    ("BARE-JWT", re.compile(
        r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}(?:\.[A-Za-z0-9_-]{5,})?"),
     "ouroboros R3 move 6 (2026-10-05): a JWT without a Bearer prefix scanned "
     "clean (eyJ header + payload segments; signature optional for alg:none)"),
    ("OPERATOR-HOME-PATH",
     re.compile(r"C:[/\\]+Users[/\\]+foste", re.IGNORECASE),
     "the row's own steal: the leak class the shape set missed (3 committed "
     "hits in watch/inbox/hermes_burn/SUBSTANCE_48h_synthesis.md at HEAD); "
     "R3 move 6: repeated separators (JSON-escaped doubled backslashes) now "
     "trip too, single separator matched only one"),
]


def fingerprint(name: str, rel: str, masked: str) -> str:
    """Accept-by-NAME identity: shape + file + masked value head. Line numbers
    are excluded on purpose so a one-line shift does not resurrect accepted
    debt; editing the value changes the mask and re-opens triage."""
    raw = f"{name}|{rel}|{masked}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def mask_value(value: str) -> str:
    head = value[:4]
    return f"{head}****(len {len(value)})"


def scan_text(text: str, rel: str) -> list[dict]:
    """Pure scan core: one row per (shape, line, hit) match, masked value only.

    finditer, not search (ouroboros R3 move 6, 2026-10-05): a line carrying
    TWO distinct secrets reported exactly one finding before, so the second
    token rode the push unreported."""
    out: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, rx, _note in SHAPES:
            for m in rx.finditer(line):
                value = m.group(0)
                out.append({"name": name, "file": rel, "line": lineno,
                            "masked": mask_value(value), "fp": None})
    for row in out:
        row["fp"] = fingerprint(row["name"], row["file"], row["masked"])
    return out


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, timeout=60, creationflags=HEADLESS)


def changed_files(root: Path) -> tuple[list[str], str | None]:
    """The secret_gate fast path: upstream..HEAD plus staged, unstaged,
    untracked. Returns (files, error)."""
    files: list[str] = []
    up = git(root, "rev-parse", "--abbrev-ref", "@{upstream}")
    if up.returncode == 0 and up.stdout.strip():
        r = git(root, "diff", "--name-only", "-z", up.stdout.strip(), "HEAD")
        if r.returncode != 0:
            return [], f"git diff upstream failed: {(r.stderr or '').strip()[:160]}"
        files += [f for f in r.stdout.split("\0") if f]
    r = git(root, "diff", "--name-only", "-z", "HEAD")
    if r.returncode != 0:
        return [], f"git diff HEAD failed: {(r.stderr or '').strip()[:160]}"
    files += [f for f in r.stdout.split("\0") if f]
    r = git(root, "ls-files", "-z", "--others", "--exclude-standard")
    if r.returncode != 0:
        return [], f"git ls-files failed: {(r.stderr or '').strip()[:160]}"
    files += [f for f in r.stdout.split("\0") if f]
    seen: set[str] = set()
    ordered = [f for f in files if not (f in seen or seen.add(f))]
    return ordered, None


def load_baseline(path: Path) -> dict:
    if not path.is_file():
        return {"accepted": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"accepted": {}}
    return data if isinstance(data, dict) and "accepted" in data else {"accepted": {}}


def run(root: Path, baseline_path: Path) -> int:
    files, err = changed_files(root)
    if err is not None:
        print(f"CRED-SHAPE: cannot verify, {err}")
        return 2
    baseline = load_baseline(baseline_path)
    accepted = baseline.get("accepted", {})
    findings: list[dict] = []
    scanned = 0
    skipped_binary = 0
    skipped_big = 0
    for rel in files:
        path = root / rel
        if not path.is_file():
            continue  # deleted in the range
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        if b"\0" in blob[:8192]:
            skipped_binary += 1
            continue
        if len(blob) > MAX_FILE_BYTES:
            skipped_big += 1
            continue
        scanned += 1
        findings.extend(scan_text(blob.decode("utf-8", errors="replace"), rel))
    fresh = [f for f in findings if f["fp"] not in accepted]
    head = (f"scanned {scanned} changed file(s), {len(findings)} finding(s) "
            f"({len(findings) - len(fresh)} accepted by name), "
            f"skipped {skipped_binary} binary / {skipped_big} >{MAX_FILE_BYTES // 1_000_000}MB")
    if not findings:
        print(f"CRED-SHAPE: ok - {head}")
        return 0
    if not fresh:
        print(f"CRED-SHAPE: ok - {head}")
        for f in findings:
            print(f"  accepted: {f['name']} {f['file']}:{f['line']} value={f['masked']}")
        return 0
    print(f"CRED-SHAPE: WARN - {head}")
    for f in fresh:
        mark = "" if f["fp"] not in accepted else " (accepted)"
        print(f"  {f['name']} {f['file']}:{f['line']} value={f['masked']}{mark}")
    print("  fix: excise or rotate the value, or accept THIS finding by name: "
          f"{DEFAULT_BASELINE.as_posix()} fingerprint(s) printed above; "
          "never loosen the hook")
    for f in fresh:
        print(f"  fp: {f['fp']}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="credential-shape scan over changed content (a11-commits row 4)")
    ap.add_argument("--changed", action="store_true",
                    help="scan the secret_gate fast path (default when no files given)")
    ap.add_argument("--root", type=Path, default=ESTATE_ROOT)
    ap.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    ap.add_argument("files", nargs="*", help="explicit files (tests); bypasses --changed")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    baseline = args.baseline
    if not baseline.is_absolute():
        baseline = root / baseline
    if args.files:
        findings: list[dict] = []
        for rel in args.files:
            path = Path(rel)
            if not path.is_absolute():
                path = root / rel
            if not path.is_file():
                print(f"CRED-SHAPE: cannot verify, missing file {rel}")
                return 2
            blob = path.read_bytes()
            if b"\0" in blob[:8192]:
                print(f"CRED-SHAPE: skip binary {rel}")
                continue
            rel_disp = path.relative_to(root).as_posix() if path.is_relative_to(root) else rel
            findings.extend(scan_text(blob.decode("utf-8", errors="replace"), rel_disp))
        fresh = [f for f in findings if f["fp"] not in load_baseline(baseline).get("accepted", {})]
        if not fresh:
            print(f"CRED-SHAPE: ok - scanned {len(args.files)} file(s), "
                  f"{len(findings)} finding(s), all accepted or none")
            return 0
        print(f"CRED-SHAPE: WARN - scanned {len(args.files)} file(s), {len(fresh)} finding(s)")
        for f in fresh:
            print(f"  {f['name']} {f['file']}:{f['line']} value={f['masked']}")
            print(f"  fp: {f['fp']}")
        return 1
    return run(root, baseline)


if __name__ == "__main__":
    sys.exit(main())
