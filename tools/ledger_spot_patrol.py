#!/usr/bin/env python3
r"""ledger_spot_patrol -- WARN-ONLY claim-vs-artifact spot checks on LANDED ledger rows.

FORCED BY adversarial-self-probes pass c (watch/inbox/BURN_adversarial-self-probes_20260927_c.md,
2026-09-27): the pass hand-verified one LANDED row's byte claims and every check held,
but a single manual probe is not an instrument. This patrol automates the probe.

Pre-registered falsifier (verbatim intent, pass c): the patrol samples 3 LANDED
rows per day and verifies every sha/byte/existence claim in one_line against
disk. If two consecutive weeks surface zero claim-artifact mismatches AND no
lane acts on a patrol warning, the patrol is vacuous overhead and reverts to
manual probes. WARN-ONLY by law: the patrol never edits the ledger, never
fails a run over a mismatch (exit 0 unless the ledger itself is unreadable),
and appends its findings to memory/burns/SPOT_PATROL.jsonl so the two-week
vacuousness clock is greppable.

Claim extraction (mechanical, honest about limits):
  * PATH claims: tokens containing "/" with a known file extension -> stat
    existence and size;
  * BARE-PATH claims (pass g): extensionless tokens under known dirs
    (githooks|scripts|tests|tools|configs|mag|docs) -> existence check only,
    fired solely when the path exists (WARN-free by construction);
  * SHA256 claims: bare 64-hex tokens -> compare against sha256 of every path
    named in the same one_line (a hex that matches nothing is UNMATCHED, a
    warn-grade finding only when the row also names exactly one path);
  * BYTE-SIZE claims: "<number> bytes" -> compare against the size of paths
    named in the same one_line when exactly one path is named.
Anything the regexes cannot bind (counts, row ids, prose) is reported as
unchecked, never guessed.

Grammar-extension probe (pass f, watch/inbox/BURN_adversarial-self-probes_20260927_f.md,
2026-09-27): psm1|ps1|log|cmd|sh|rbxlx|lua in PATH_RE plus logs/ and githooks/
in KNOWN_DIRS was built and REVERTED the same pass on pass e's pre-registered
thresholds (7 of 19 blind rows gained vs 10 required; fired fraction 48.3% vs
58% required; the extension also silenced 3 existing warns on B2-384 by
breaking the single-path sha/bytes heuristics). The measured blind tokens are
extensionless (githooks/pre-push) or dir-prefix-bare, which extension-scoped
grammar structurally cannot bind.

Known-dirs prefix probe (pass g, watch/inbox/BURN_adversarial-self-probes_20260927_g.md,
2026-09-27): BARE_PATH_RE binds the gap class pass f named -- extensionless
tokens under githooks|scripts|tests|tools|configs|mag|docs -- which
extension-scoped grammar structurally cannot reach. Three guards keep it
additive-only: a bare token binds only when its final segment carries no dot
(dotted tails stay PATH_RE's class), a token already bound by PATH_RE never
re-fires, and a bare path fires a check ONLY when it exists on disk (no warn
inflation on guesses). Bare paths never join the extension-path list, so the
single-path sha256/bytes heuristics keep their arity and no existing warn can
be silenced (the criterion that killed pass f).

Sampling: deterministic per UTC day -- the pool of LANDED rows rotates by an
integer day offset (day number * 3 mod pool size), so the same day re-verifies
the same rows and successive days walk the pool.

Usage: .venv/Scripts/python.exe tools/ledger_spot_patrol.py [--rows 3]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"
PATROL_LOG = REPO / "memory" / "burns" / "SPOT_PATROL.jsonl"

PATH_RE = re.compile(r"[\w./\\-]+\.(?:py|md|jsonl|json|txt|yaml|yml|ts|js|html|db|sqlite)")
BARE_PATH_RE = re.compile(r"\b(?:githooks|scripts|tests|tools|configs|mag|docs)/[\w.-]+")
SHA_RE = re.compile(r"\b[0-9a-f]{64}\b", re.IGNORECASE)
BYTES_RE = re.compile(r"\b(\d{2,})\s+bytes\b")
KNOWN_DIRS = ("watch/", "memory/", "corpus/", "tools/", "configs/", "tests/", "mag/", "queue/", "catalog/", "scripts/", "roblox/", "dashboard/", "backend/", "docs/")


def _now_z() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_landed() -> list[dict]:
    rows = []
    with LEDGER.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if str(r.get("verdict", "")).upper() in ("LANDED", "landed"):
                rows.append(r)
    return rows


def _sample(pool: list[dict], n: int) -> list[dict]:
    if len(pool) <= n:
        return list(pool)
    day = _dt.datetime.now(_dt.timezone.utc).timetuple().tm_yday
    start = (day * n) % len(pool)
    return [pool[(start + i) % len(pool)] for i in range(n)]


def _paths_in(one_line: str) -> list[Path]:
    out = []
    for m in PATH_RE.findall(one_line):
        p = m.replace("\\", "/")
        if p.startswith(KNOWN_DIRS):
            out.append(REPO / p)
    return out


def _bare_paths_in(one_line: str, covered: set[str]) -> list[Path]:
    """Pass g: extensionless known-dir tokens, the gap pass f named.

    Binds only dotless-tail tokens (dotted tails are PATH_RE's class or
    ambiguous), skips tokens already bound by PATH_RE (no double count), and
    returns only paths that exist on disk, so the warn count cannot inflate
    on guesses. Dot-segments (".", "..") are noise, not claims.
    """
    out = []
    for tok in BARE_PATH_RE.findall(one_line):
        segs = tok.split("/")
        if "." in segs[-1]:
            continue
        if any(s in (".", "..") for s in segs):
            continue
        if any(tok == c or tok.startswith(c + "/") or c.startswith(tok + "/")
               for c in covered):
            continue
        p = REPO / tok
        if p.is_file():
            out.append(p)
    return out


ABSENCE_MARKERS = ("absent", "retracted", "removed", "not on disk", "no longer exists",
                   "missing from disk", "deleted")


def check_row(row: dict) -> dict:
    one_line = str(row.get("one_line", ""))
    paths = _paths_in(one_line)
    claims_absence = any(m in one_line.lower() for m in ABSENCE_MARKERS)
    findings: list[dict] = []

    for p in paths:
        rel = str(p.relative_to(REPO)).replace("\\", "/")
        if p.is_file():
            findings.append({"check": "path-exists", "target": rel, "state": "ok"})
        elif claims_absence:
            # claim polarity (self-caught on B2-298, 2026-09-27): a one_line that
            # claims absence may name files because they are GONE; a missing file
            # then CONFIRMS the claim instead of warning. Reported as info, and
            # only when a presence-claiming row's file is missing does it warn.
            findings.append({"check": "path-exists", "target": rel,
                             "state": "info absence-claimed, file absent (no warn)"})
        else:
            findings.append({"check": "path-exists", "target": rel, "state": "WARN missing"})

    # pass g (watch/inbox/BURN_adversarial-self-probes_20260927_g.md): bare-path
    # claims fire existence-gated and heuristic-isolated -- they never join
    # `paths`, so the single-path sha256/bytes heuristics keep their arity and
    # no existing warn can be silenced (the criterion that killed pass f).
    for p in _bare_paths_in(one_line, {q.replace("\\", "/") for q in PATH_RE.findall(one_line)}):
        findings.append({"check": "bare-path-exists",
                         "target": str(p.relative_to(REPO)).replace("\\", "/"),
                         "state": "ok"})

    shas = SHA_RE.findall(one_line)
    if shas and paths:
        disk_hashes = {}
        for p in paths:
            if p.is_file():
                disk_hashes[hashlib.sha256(p.read_bytes()).hexdigest()] = p
        for s in shas:
            low = s.lower()
            if low in disk_hashes:
                findings.append({"check": "sha256", "target": low[:16] + "...", "state": "ok matches " + disk_hashes[low].name})
            elif len(paths) == 1:
                findings.append({"check": "sha256", "target": low[:16] + "...", "state": "WARN unmatched against the single named file"})

    bm = BYTES_RE.search(one_line)
    if bm and len(paths) == 1 and paths[0].is_file():
        claimed = int(bm.group(1))
        actual = paths[0].stat().st_size
        state = "ok" if claimed == actual else f"WARN claimed {claimed} vs actual {actual}"
        findings.append({"check": "bytes", "target": paths[0].name, "state": state})

    warns = [f for f in findings if str(f["state"]).startswith("WARN")]
    return {
        "patrol_ts": _now_z(),
        "row_ts": row.get("ts"),
        "slug": row.get("slug"),
        "verdict": row.get("verdict"),
        "checks": len(findings),
        "warns": len(warns),
        "findings": findings,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ledger_spot_patrol",
                                 description="WARN-ONLY spot checks on LANDED ledger rows")
    ap.add_argument("--rows", type=int, default=3, help="rows per patrol (default 3)")
    args = ap.parse_args(argv)

    pool = _read_landed()
    if not pool:
        print("PATROL: no LANDED rows in the ledger; nothing to check")
        return 0
    sample = _sample(pool, args.rows)

    results = [check_row(r) for r in sample]
    with PATROL_LOG.open("a", encoding="utf-8", newline="\n") as f:
        for res in results:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")

    total_checks = sum(r["checks"] for r in results)
    total_warns = sum(r["warns"] for r in results)
    for res in results:
        flag = "WARN" if res["warns"] else "ok"
        print(f"[{flag}] {res['row_ts']} {res['slug']}: {res['checks']} checks, {res['warns']} warns")
        for fnd in res["findings"]:
            if str(fnd["state"]).startswith("WARN"):
                print(f"    - {fnd['check']} {fnd['target']}: {fnd['state']}")
    print(f"PATROL: {len(sample)} rows, {total_checks} mechanical checks, "
          f"{total_warns} warns (WARN-ONLY; log {PATROL_LOG.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
