#!/usr/bin/env python3
"""genome_patrol - fail-closed read-only validator for mag_genome.v1 genomes.

Laws this tool enforces (byte-backed, nothing hand-assumed):
- Carrier grammar (B2-249, tools/census_drift_patrol.py parse_carrier idiom):
  the GENOME.md header is frozen grammar; any shape defect fail-closes exit 2.
- Named-omission law (tools/zknot.py:219-243 generalization, g19 section 4):
  every DEAD lane must carry a casualty marker with a named cause; silence is
  never a valid fold state. A fold that proposes zero, kills zero and disputes
  zero must still print the explicit mutation_scan / no-drift line.
- Accounting invariant (g19 section 1.1): PROPOSED == TRANSMITTED + DEAD +
  DISPUTED, parsed from the genome's accounting section.
- Lane manifest integrity (g19 section 1.3): every manifest sha256 is
  recomputed from disk bytes (trust bytes, not reports); manifest rows and
  lanes-dir files must match one-to-one, no silent additions or drops.
- g21 risk gates (memory/runs/genetic_burn/20261018/G0/lanes/g21-genetic-risk-pass.md):
  founding-bytes anchor, tier-gate, bounds, consumer pulse - WARN-only at this
  tier, printed as WARN lines, never failures.

Exit codes: 0 = genome valid (first line "genome_patrol: ok"), 2 = structural
defects (first line "genome_patrol: FAIL: N defect(s)"). Read-only: opens
genome, manifest and lane files for reading only; the --selftest writes its
fixtures under the system temp dir and touches nothing in the repo.

Usage:
  python tools/genome_patrol.py <path/to/GENOME.md>
  python tools/genome_patrol.py --selftest
"""

import argparse
import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path

BURN_DIR_TOKEN = "memory/runs/genetic_burn"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
TITLE_RE = re.compile(r"^#\s+GENOME\s+G(\d+)\s+-\s+(\S.*)$")
FORMAT_RE = re.compile(r"format:\s*mag_genome\.v1\b")
PARENT_RE = re.compile(r"parent:\s*([^\s;(,]+)")
MOMENT_RE = re.compile(r"moment:\s*\S+")
FOLD_MASTER_RE = re.compile(r"fold-master:\s*([^\s;(,]+)")
MANIFEST_RE = re.compile(r"manifest:\s*([^\s;(]+)(?:\s*\((\d+)\s+lanes)?")
LANES_RE = re.compile(r"lane files:\s*([^\s;]+)")
ACCOUNT_RE = re.compile(
    r"PROPOSED\s+(\d+)\s*=\s*TRANSMITTED\s+(\d+)\s*\+\s*DEAD\s+(\d+)(.*?)"
    r"\+\s*DISPUTED\s+(\d+)",
    re.S,
)
PAREN_RE = re.compile(r"\(([^)]*)\)")
MANIFEST_ROW_RE = re.compile(r"^([0-9a-f]{64})\s+\*(.+)$")
ID_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{2,}$")
PATH_TOKEN_RE = re.compile(
    r"[A-Za-z0-9_.\-/\\]+\.(?:md|py|json|jsonl|yaml|yml|txt|sqlite|sha256)"
)
CASUALTY_MARKERS = ("casualty", "tombstone", "killed", "dead", "marked")
CAUSE_TOKENS = (
    "death", "killed", "fail", "rate-limit", "ratelimit", "drift", "error",
    "abort", "crash", "missing", "timeout", "1302", "429", "empty", "refused",
    "expired", "dead", "orphan",
)
MUTATION_SCAN_RE = re.compile(r"mutation_scan|no drift detected", re.I)


class Patrol:
    """Collects defects (exit 2) and warns (exit 0) for one genome."""

    def __init__(self):
        self.defects = []
        self.warns = []
        self.notes = []

    def defect(self, msg):
        self.defects.append(msg)

    def warn(self, msg):
        self.warns.append(msg)

    def note(self, msg):
        self.notes.append(msg)


def read_text(path):
    data = Path(path).read_bytes()
    return data.decode("utf-8", errors="replace")


def find_repo_root(start):
    cur = Path(start).resolve()
    for cand in [cur] + list(cur.parents):
        if (cand / ".git").exists():
            return cand
    return None


def resolve_header_path(value, genome_dir, repo_root):
    """Resolve a header path against the genome dir first, then repo root."""
    value = str(value).strip().rstrip("/\\")
    if not value:
        return None
    cands = []
    if os.path.isabs(value):
        cands.append(Path(value))
    else:
        cands.append(Path(genome_dir) / value)
        if repo_root is not None:
            cands.append(Path(repo_root) / value)
    for c in cands:
        if c.exists():
            return c
    return None


def header_block(text):
    """Text between the '# GENOME' title line and the first '## ' heading."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if TITLE_RE.match(line):
            start = i + 1
            break
    if start is None:
        return "", None
    body = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return " ".join(body), start


def section_text(text, heading_substr):
    """Text of the first '## ' section whose heading contains the substring."""
    lines = text.splitlines()
    in_sec = False
    body = []
    for line in lines:
        if line.startswith("## "):
            if in_sec:
                break
            in_sec = heading_substr.lower() in line.lower()
            continue
        if in_sec:
            body.append(line)
    return " ".join(body)


def check_casualty_clause(clause):
    """A casualty clause must name an id, carry a marker and a cause."""
    problems = []
    segments = [s.strip() for s in clause.split(",") if s.strip()]
    if not segments or not ID_TOKEN_RE.match(segments[0]):
        problems.append("no lane/task id named")
    low = clause.lower()
    if not any(m in low for m in CASUALTY_MARKERS):
        problems.append("no casualty marker")
    if not any(c in low for c in CAUSE_TOKENS):
        problems.append("no cause named")
    return problems


def run_checks(genome_path):
    """Validate one genome file. Returns (Patrol, genome_sha256)."""
    p = Patrol()
    gp = Path(genome_path)
    if not gp.is_file():
        p.defect("genome file not found: %s" % gp)
        return p, ""
    raw = gp.read_bytes()
    genome_sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    p.note("genome: %s" % gp)
    p.note("genome sha256: %s" % genome_sha)

    # --- title line (frozen grammar: "# GENOME G<n> - <burn name>") ---
    m = None
    for line in text.splitlines():
        m = TITLE_RE.match(line)
        if m:
            break
    if m is None:
        p.defect("title: no '# GENOME G<n> - <burn name>' line found")
        generation = None
    else:
        generation = int(m.group(1))
        p.note("title: G%d - %s" % (generation, m.group(2)))

    # --- header keys ---
    head, _ = header_block(text)
    if not head:
        p.defect("header: empty or unparsable header block")
    if not FORMAT_RE.search(head):
        p.defect("header: 'format: mag_genome.v1' line missing or off-grammar")
    pm = PARENT_RE.search(head)
    parent_val = pm.group(1) if pm else None
    if pm is None:
        p.defect("header: 'parent:' key missing")
    else:
        if parent_val.lower() == "none":
            if generation is not None and generation > 0:
                p.defect(
                    "header: G%d declares parent none (orphan generation, "
                    "g19 section 2.3)" % generation
                )
            else:
                p.note("parent: none (founder)")
        elif HEX64_RE.match(parent_val.lower()):
            p.note("parent_genome_sha256: %s" % parent_val.lower())
        else:
            p.defect(
                "header: parent value %r is neither 'none' nor 64-hex sha256"
                % parent_val
            )
    mm = MOMENT_RE.search(head)
    if mm is None:
        p.defect("header: 'moment:' key missing or carries no date")
    else:
        p.note("moment: %s" % mm.group(0).split(":", 1)[1].strip())
    fm = FOLD_MASTER_RE.search(head)
    if fm is None or not fm.group(1):
        p.defect("header: 'fold-master:' key missing or empty")
    else:
        p.note("fold-master: %s" % fm.group(1))

    # --- lane manifest: parse, resolve, recompute ---
    man = MANIFEST_RE.search(head)
    man_path = None
    if man is None:
        p.defect("header: 'manifest:' key missing")
    else:
        man_val = man.group(1)
        claimed_count = int(man.group(2)) if man.group(2) else None
        repo_root = find_repo_root(gp.parent)
        man_path = resolve_header_path(man_val, gp.parent, repo_root)
        if man_path is None:
            p.defect("manifest: file not resolvable: %r" % man_val)
        else:
            lanes_val_m = LANES_RE.search(head)
            if lanes_val_m is None:
                p.defect("header: 'lane files:' key missing")
                lanes_dir = None
            else:
                lanes_dir = resolve_header_path(
                    lanes_val_m.group(1), gp.parent, repo_root
                )
                if lanes_dir is None or not lanes_dir.is_dir():
                    p.defect(
                        "header: lanes dir not resolvable: %r"
                        % lanes_val_m.group(1)
                    )
                    lanes_dir = None
            rows = []
            for lineno, line in enumerate(
                man_path.read_text(encoding="utf-8", errors="replace").splitlines(),
                1,
            ):
                line = line.strip()
                if not line:
                    continue
                rm = MANIFEST_ROW_RE.match(line)
                if rm is None:
                    p.defect(
                        "manifest: line %d off-grammar (want '<sha256> *<name>')"
                        % lineno
                    )
                    continue
                rows.append((rm.group(1), rm.group(2).strip()))
            p.note("manifest: %d rows parsed from %s" % (len(rows), man_path.name))
            if claimed_count is not None and len(rows) != claimed_count:
                p.defect(
                    "manifest: header claims %d lanes but manifest holds %d rows"
                    % (claimed_count, len(rows))
                )
            if rows and lanes_dir is not None:
                bad_name = [
                    n
                    for _, n in rows
                    if os.path.isabs(n) or ".." in Path(n).parts
                ]
                for n in bad_name:
                    p.defect("manifest: unsafe lane path escapes lanes dir: %r" % n)
                if bad_name:
                    rows = [r for r in rows if r[1] not in bad_name]
                verified = 0
                for want, name in rows:
                    lf = lanes_dir / name
                    if not lf.is_file():
                        p.defect("manifest: lane file missing on disk: %s" % name)
                        continue
                    got = hashlib.sha256(lf.read_bytes()).hexdigest()
                    if got != want.lower():
                        p.defect(
                            "manifest: sha256 mismatch %s (manifest %s, disk %s)"
                            % (name, want, got)
                        )
                    else:
                        verified += 1
                p.note(
                    "manifest: %d/%d lane hashes verified against disk bytes"
                    % (verified, len(rows))
                )
                on_disk = sorted(
                    f.name for f in lanes_dir.iterdir() if f.is_file()
                )
                listed = sorted(n for _, n in rows)
                for name in on_disk:
                    if name not in listed:
                        p.defect(
                            "manifest: lane file on disk absent from manifest "
                            "(named-omission class): %s" % name
                        )
                for name in listed:
                    if name not in on_disk:
                        # already covered by the missing-file defect above
                        pass

    # --- accounting invariant ---
    acct = section_text(text, "Accounting")
    am = ACCOUNT_RE.search(acct)
    if am is None:
        p.defect(
            "accounting: no parsable 'PROPOSED n = TRANSMITTED n + DEAD n "
            "... + DISPUTED n' line in the accounting section"
        )
    else:
        proposed = int(am.group(1))
        transmitted = int(am.group(2))
        dead = int(am.group(3))
        dead_clause = am.group(4)
        disputed = int(am.group(5))
        p.note(
            "accounting: PROPOSED %d = TRANSMITTED %d + DEAD %d + DISPUTED %d"
            % (proposed, transmitted, dead, disputed)
        )
        if proposed != transmitted + dead + disputed:
            p.defect(
                "accounting: invariant FAILS: %d != %d + %d + %d"
                % (proposed, transmitted, dead, disputed)
            )
        # named-omission law: every DEAD lane named with marker + cause
        if dead > 0:
            clauses = PAREN_RE.findall(dead_clause)
            if not clauses:
                p.defect(
                    "named-omission: DEAD %d but no casualty clause follows "
                    "(silence is never a valid fold state)" % dead
                )
            else:
                if len(clauses) != dead:
                    p.defect(
                        "named-omission: DEAD %d but %d casualty clause(s) "
                        "found; each dead lane must be named individually"
                        % (dead, len(clauses))
                    )
                for clause in clauses:
                    probs = check_casualty_clause(clause)
                    for pr in probs:
                        p.defect(
                            "named-omission: casualty clause %r: %s"
                            % (clause, pr)
                        )
        # mutation scan: the all-zero fold must still speak
        if proposed == 0 and dead == 0 and disputed == 0:
            if not MUTATION_SCAN_RE.search(text):
                p.defect(
                    "named-omission: all-zero fold without an explicit "
                    "mutation_scan / no-drift line (g19 section 4)"
                )

    # --- g21 risk gates: WARN-only ---
    found_founding = False
    for tok in PATH_TOKEN_RE.findall(text):
        norm = tok.replace("\\", "/").lower()
        if norm.startswith(BURN_DIR_TOKEN):
            continue
        # a founding cite is cross-file: needs a directory component, is not
        # the genome's own manifest, and does not resolve as a genome-sibling
        # (genome-local paths dead-end inside the fold, g21 risk 1)
        if "/" not in norm or norm.endswith(".sha256"):
            continue
        if (gp.parent / tok).exists():
            continue
        found_founding = True
        break
    if not found_founding:
        p.warn(
            "g21 R1 founding-bytes anchor: no byte path outside %s cited"
            % BURN_DIR_TOKEN
        )
    if not re.search(r"\btier", text, re.I):
        p.warn("g21 R2 tier-gate: no tier annotation mentioned anywhere")
    if not re.search(r"\bbound", text, re.I):
        p.warn("g21 R3 standing-wave bounds: no section bound mentioned")
    if not re.search(r"\bconsumer", text, re.I):
        p.warn("g21 R4 consumer pulse: no consumer mentioned")
    return p, genome_sha


def print_report(p, genome_sha):
    if p.defects:
        print("genome_patrol: FAIL: %d defect(s)" % len(p.defects))
    else:
        print("genome_patrol: ok")
    for n in p.notes:
        print("genome_patrol: %s" % n)
    for d in p.defects:
        print("genome_patrol: DEFECT: %s" % d)
    for w in p.warns:
        print("genome_patrol: WARN: %s" % w)
    return 0 if not p.defects else 2


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="fail-closed read-only validator for mag_genome.v1"
    )
    ap.add_argument("genome", nargs="?", help="path to a GENOME.md")
    ap.add_argument("--selftest", action="store_true", help="run fixture selftest")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.genome:
        ap.print_usage()
        print("genome_patrol: FAIL: a GENOME.md path or --selftest is required")
        return 2
    p, _sha = run_checks(args.genome)
    return print_report(p, _sha)


# ---------------- selftest (census-patrol frozen-grammar + fixture pattern) --

GOOD_LANE_BODY = "lane report body for selftest\n"

GOOD_TEMPLATE = """# GENOME G0 - selftest burn

format: mag_genome.v1 (per selftest); parent: none (founder); moment: 2026-10-18T00:00:00Z; fold-master: selftest-seat; manifest: manifest.sha256 (2 lanes, sha256 each); lane files: lanes/

## Accounting invariant (PROPOSED == TRANSMITTED + DEAD + DISPUTED)

{accounting}

## Falsifier status at fold

- founding anchor: watch/inbox/selftest-founding.md; tier-gate satisfied; genome sections bounded; consumer pulse named.
{extra}"""


def build_fixture(root, accounting, extra="", tamper_lane=False):
    root = Path(root)
    lanes = root / "lanes"
    lanes.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in ("l1.md", "l2.md"):
        (lanes / name).write_bytes(GOOD_LANE_BODY.encode("utf-8"))
        rows.append(
            "%s *%s" % (hashlib.sha256(GOOD_LANE_BODY.encode("utf-8")).hexdigest(), name)
        )
    (root / "manifest.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")
    if tamper_lane:
        (lanes / "l1.md").write_bytes(b"tampered bytes\n")
    genome = root / "GENOME.md"
    genome.write_text(
        GOOD_TEMPLATE.format(accounting=accounting, extra=extra), encoding="utf-8"
    )
    return genome


def selftest():
    cases = []
    base = tempfile.mkdtemp(prefix="genome_patrol_selftest_")

    g = build_fixture(os.path.join(base, "good"), "PROPOSED 2 = TRANSMITTED 2 + DEAD 0 + DISPUTED 0.")
    cases.append(("good-genome", g, 0))

    g = build_fixture(
        os.path.join(base, "tampered"),
        "PROPOSED 2 = TRANSMITTED 2 + DEAD 0 + DISPUTED 0.",
        tamper_lane=True,
    )
    cases.append(("tampered-lane-hash", g, 2))

    g = build_fixture(
        os.path.join(base, "nocause"),
        "PROPOSED 2 = TRANSMITTED 1 + DEAD 1 (g99-missing-lane) + DISPUTED 0.",
    )
    cases.append(("dead-without-marker-or-cause", g, 2))

    g = build_fixture(
        os.path.join(base, "mathbreak"),
        "PROPOSED 3 = TRANSMITTED 1 + DEAD 1 (g99-x, casualty-marked, rate-limit death) + DISPUTED 0.",
    )
    cases.append(("accounting-invariant-break", g, 2))

    g = build_fixture(
        os.path.join(base, "silentzero"),
        "PROPOSED 0 = TRANSMITTED 0 + DEAD 0 + DISPUTED 0.",
    )
    cases.append(("silent-all-zero-fold", g, 2))

    g = build_fixture(
        os.path.join(base, "zeroscan"),
        "PROPOSED 0 = TRANSMITTED 0 + DEAD 0 + DISPUTED 0.",
        extra="- mutation_scan: no drift detected (0 tasks reviewed)\n",
    )
    cases.append(("all-zero-with-mutation-scan", g, 0))

    g = build_fixture(
        os.path.join(base, "orphan"),
        "PROPOSED 2 = TRANSMITTED 2 + DEAD 0 + DISPUTED 0.",
    )
    text = g.read_text(encoding="utf-8")
    text = text.replace("parent: none (founder)", "parent: none (oops)")
    text = text.replace("# GENOME G0 -", "# GENOME G1 -")
    g.write_text(text, encoding="utf-8")
    cases.append(("g1-orphan-parent-none", g, 2))

    failures = 0
    for name, genome, want_zero in cases:
        p, _ = run_checks(genome)
        got = 0 if not p.defects else 2
        ok = got == want_zero
        if not ok:
            failures += 1
        print(
            "selftest: %s: %s (want exit %d, got %d)"
            % (name, "PASS" if ok else "FAIL", want_zero, got)
        )
        if not ok:
            for d in p.defects:
                print("  defect: %s" % d)
    print("selftest: %d/%d fixtures passed" % (len(cases) - failures, len(cases)))
    print("selftest: fixtures under %s (temp only; repo untouched)" % base)
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
