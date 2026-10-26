"""secret_gate_scan - scanning core for the secret gate (file/tree/history).

Moved from tools/secret_gate.py 2026-09-27 (ratchet split) and since amended
by the GATE_DEFECT_ASSIGNMENT_BYPASS fix (per-rule blockable eval; receipt in
watch/inbox/audit_20260926/). Rules: tools.secret_gate_rules; CLI: secret_gate.py.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
import subprocess
import sys

from tools.secret_gate_rules import (
    ALLOW_RE,
    BLOCKABLE_RES,
    BLOCKABLE_RULES,
    COMBINED,
    ENTROPY_MIN,
    ENT_LEN_MIN,
    FAST_PASS_RE,
    GITLEAKS_ALLOW,
    GateError,
    MAX_BLOCKING_STORED,
    MAX_ENT_STORED,
    MAX_FILE_BYTES,
    MAX_FINDINGS_PER_RULE,
    NO_PREFILTER,
    REPO,
    RULE_NAMES,
    RULE_SEV,
    SEV_RANK,
    SELF_SKIP_RELPATHS,
    SNIFF_BYTES,
    SKIP_DIR_PARTS,
)




def _run(cmd, **kw):
    # HEADLESS law (spawn_sites_no_window): every spawn is windowless.
    # Fix 2026-09-28 (drift patrol): this body called `_run` recursively (the
    # name had been rebound away from subprocess.run), so every spawn died
    # with RecursionError and the gate fail-closed ALL pushes since the
    # secret-gate go-live (e60b4e801). cmd is always an argv list —
    # subprocess.run(list, shell=False), no shell, no string interpolation.
    kw.setdefault("shell", False)
    kw.setdefault("creationflags", getattr(subprocess, "CREATE_NO_WINDOW",
                  0x08000000) if sys.platform == "win32" else 0)
    return subprocess.run(cmd, **kw)

def shannon(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def is_binary(chunk):
    if b"\x00" in chunk:
        return True
    if not chunk:
        return True
    textish = sum(1 for b in chunk if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return textish / len(chunk) < 0.85


def mask(tok):
    head = tok[:6]
    return head + "..." + "(len=%d)" % len(tok)


def rel_of(path):
    # Cause of the guard: the tree carries literal "nul" files (Windows
    # reserved device names, stray "> nul" redirect debris at repo root,
    # corpus/library/lmcache-src and memory/runs/the50, found 2026-09-27
    # when the first --full run died on them); relpath -> abspath resolves
    # those to the \\.\nul device mount and raises ValueError. Evidence:
    # first whole-tree run exited 2 with "path is on mount '\\\\.\\nul'";
    # the completing rerun is captured in
    # watch/inbox/SECRET_GATE_BUILD_20260927.md.
    try:
        rel = os.path.relpath(path, REPO)
    except (ValueError, OSError):
        return path.replace("\\", "/")
    if rel.startswith(".." + os.sep) or rel.startswith(".."):
        # outside the repo (ad-hoc scan scope): absolute path reads better
        # than a long ../../../ walk-up.
        return path.replace("\\", "/")
    return rel.replace("\\", "/")


def iter_tree_files():
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def iter_scope_files(scope_paths):
    for sp in scope_paths:
        if os.path.isdir(sp):
            for dirpath, dirnames, filenames in os.walk(sp):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS]
                for fn in filenames:
                    yield os.path.join(dirpath, fn)
        elif os.path.isfile(sp):
            yield sp
        else:
            raise GateError("scan path not found: %s" % sp)


def git_z(cmd):
    p = _run(["git", "-C", REPO] + cmd,
                       capture_output=True)
    if p.returncode != 0:
        raise GateError("git failed (%s): %s"
                        % (" ".join(cmd), p.stderr.decode("utf-8", "replace").strip()))
    return [os.path.join(REPO, f) for f in p.stdout.decode("utf-8", "replace").split("\0") if f]


def changed_files():
    """Files changed vs upstream, plus worktree and untracked.

    With an upstream: @{u}..HEAD diff (what a push would send) plus staged,
    unstaged and untracked paths (defense in depth before the commit happens).
    Without an upstream (current branch state: none configured): staged,
    unstaged and untracked only, and the row records upstream=null so the
    narrowing is visible instead of silently widening.
    """
    upstream = None
    p = _run(["git", "-C", REPO, "rev-parse", "--verify", "--quiet",
                        "@{upstream}"], capture_output=True)
    if p.returncode == 0:
        upstream = p.stdout.decode("utf-8", "replace").strip()
    seen = {}
    if upstream:
        for f in git_z(["diff", "--name-only", "-z", upstream, "HEAD"]):
            seen[f] = "upstream_diff"
    for f in git_z(["diff", "--name-only", "-z"]):
        seen[f] = "worktree"
    for f in git_z(["diff", "--name-only", "-z", "--cached"]):
        seen[f] = "staged"
    for f in git_z(["ls-files", "--others", "--exclude-standard", "-z"]):
        seen[f] = "untracked"
    return upstream, sorted(f for f in seen if os.path.isfile(f))


def line_fingerprint(line):
    return hashlib.sha256(line.strip().encode("utf-8", "ignore")).hexdigest()[:16]


def scan(files, baseline, path_rules, threshold):
    census = {
        "files_seen": 0, "scanned": 0, "binary_skipped": 0, "large_skipped": 0,
        "read_error": 0, "bytes_scanned": 0,
    }
    findings = []           # capped rows
    rule_counts = {rid: 0 for rid in RULE_NAMES}
    sev_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    ent_counts = {"total": 0, "stored": 0}
    files_with_hits = set()
    ent_files = set()
    blocking = []
    blocking_count = 0
    accepted_count = 0
    s3 = {"aws_secret_entropy_filtered": 0}

    thr_rank = SEV_RANK[threshold]

    def _emit(kind, tok, rel, i, line):
        # count + row-build + blocking decision, shared by both passes (2026-09-27)
        nonlocal blocking_count, accepted_count
        rule_counts[kind] += 1
        sev_counts[RULE_SEV[kind]] += 1
        files_with_hits.add(rel)
        row = {
            "kind": kind, "severity": RULE_SEV[kind],
            "file": rel, "line": i, "masked": mask(tok),
        }
        bkey = "%s|%s|%s" % (kind, rel, line_fingerprint(line))
        accepted = bkey in baseline or any(
            pr["rule"] == kind and pr["re"].search(rel) for pr in path_rules
        )
        if accepted:
            accepted_count += 1
        elif (kind in BLOCKABLE_RULES
                and SEV_RANK[RULE_SEV[kind]] >= thr_rank):
            blocking_count += 1
            row["blocking"] = True
            if len(blocking) < MAX_BLOCKING_STORED:
                blocking.append(row)
        else:
            row["blocking"] = False
        if accepted:
            row["accepted"] = True
        if rule_counts[kind] <= MAX_FINDINGS_PER_RULE:
            findings.append(row)

    for path in files:
        census["files_seen"] += 1
        rel = rel_of(path)
        if rel in SELF_SKIP_RELPATHS:
            continue
        try:
            size = os.path.getsize(path)
        except OSError:
            census["read_error"] += 1
            continue
        if size > MAX_FILE_BYTES:
            census["large_skipped"] += 1
            continue
        try:
            with open(path, "rb") as fh:
                chunk = fh.read(SNIFF_BYTES)
                if is_binary(chunk):
                    census["binary_skipped"] += 1
                    continue
                fh.seek(0)
                data = fh.read(MAX_FILE_BYTES)
        except OSError:
            census["read_error"] += 1
            continue
        census["scanned"] += 1
        census["bytes_scanned"] += len(data)
        text = data.decode("utf-8", errors="ignore")
        for i, line in enumerate(text.splitlines(), 1):
            if not line or len(line) > 4000:
                continue
            if GITLEAKS_ALLOW in line:
                continue
            if not NO_PREFILTER and not FAST_PASS_RE.search(line):
                continue
            # GATE_DEFECT_ASSIGNMENT_BYPASS fix (2026-09-27; receipt
            # watch/inbox/audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_
            # 20260927.md): blockable provider rules evaluate PER-RULE
            # first, so a NAME=value assignment cannot be swallowed whole
            # by the generic tail alternatives of COMBINED (finditer is
            # non-overlapping; XAI_API_KEY=xai-... landed low, not high).
            # COMBINED stays for the report tier; overlapping matches are
            # skipped so the provider rule wins exactly once.
            blockable_spans = []
            for rid, rex in BLOCKABLE_RES:
                for m in rex.finditer(line):
                    tok = m.group()
                    if ALLOW_RE.search(tok) or ALLOW_RE.search(line[:120]):
                        continue
                    blockable_spans.append((m.start(), m.end()))
                    _emit(rid, tok, rel, i, line)
            for m in COMBINED.finditer(line):
                idx = m.lastindex
                if idx is None:
                    continue
                if any(m.start() < e and s < m.end()
                       for s, e in blockable_spans):
                    continue
                if idx > len(RULE_NAMES):
                    kind = "ENT"
                else:
                    kind = RULE_NAMES[idx - 1]
                tok = m.group()
                if kind == "ENT":
                    if len(tok) >= ENT_LEN_MIN:
                        h = shannon(tok)
                        if h >= ENTROPY_MIN:
                            ent_counts["total"] += 1
                            if ALLOW_RE.search(tok):
                                continue
                            ent_files.add(rel)
                            if ent_counts["stored"] < MAX_ENT_STORED:
                                ent_counts["stored"] += 1
                                findings.append({
                                    "kind": "entropy", "file": rel, "line": i,
                                    "entropy": round(h, 2), "masked": mask(tok),
                                })
                    continue
                if ALLOW_RE.search(tok) or ALLOW_RE.search(line[:120]):
                    continue
                if kind == "AWS-SECRET-40":
                    # S3: the entropy floor the scanner already computed for
                    # the ENT branch, now used as a filter. Evidence: 48,427
                    # raw hits in the 2026-09-26 run, 80% of all findings,
                    # mostly git OIDs and hex blobs under 4.3 bits/char.
                    if shannon(tok) < ENTROPY_MIN:
                        s3["aws_secret_entropy_filtered"] += 1
                        continue
                _emit(kind, tok, rel, i, line)

    return {
        "census": census,
        "rule_counts": {k: v for k, v in rule_counts.items() if v},
        "severity_counts": sev_counts,
        "files_with_rule_hits_count": len(files_with_hits),  # S4: count, never the list
        "entropy": ent_counts,
        "entropy_files_count": len(ent_files),
        "findings_stored": findings,
        "blocking": blocking,
        "blocking_count": blocking_count,
        "accepted_count": accepted_count,
        "s3": s3,
    }


def history_scan(baseline, path_rules, threshold):
    """Steal 4 (gitleaks git mode): every ADDED line across git history
    through the same rule engine, deduped by (rule, path, line fingerprint).
    Output is the purge target list for the operator-gated filter-repo step:
    which paths carry which committed secret shapes and the first commit that
    introduced each. Slow, manual, never wired into the push hook. Paths
    parsed from git output are LABELS ONLY (regex match + JSON report); this
    function never opens a filesystem path from git output, and traversal-
    shaped or NUL-carrying paths are dropped outright.
    """
    thr_rank = SEV_RANK[threshold]
    proc = subprocess.Popen(
        ["git", "log", "-p", "--no-color", "-U0", "--all"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
        errors="replace", cwd=REPO)
    seen = {}
    path = None
    lineno = 0
    commit = "?"
    rule_counts = {}
    for raw in proc.stdout:
        line = raw.rstrip("\n")
        if line.startswith("commit "):
            commit = line.split()[1][:12]
            continue
        if line.startswith("+++ b/"):
            cand = line[6:].strip().replace("\\", "/")
            if ".." in cand or "\x00" in cand or not cand:
                path = None
                continue
            path = cand
            continue
        if line.startswith("@@"):
            m2 = re.search(r"\+(\d+)", line)
            lineno = int(m2.group(1)) - 1 if m2 else 0
            continue
        if path is None or not line.startswith("+") or line.startswith("+++"):
            continue
        lineno += 1
        content = line[1:]
        if not content or len(content) > 4000:
            continue
        if GITLEAKS_ALLOW in content:
            continue
        if not NO_PREFILTER and not FAST_PASS_RE.search(content):
            continue
        # GATE_DEFECT_ASSIGNMENT_BYPASS fix (2026-09-27), history leg: the
        # blockable set evaluates per-rule first so assignment-form secrets
        # in history block under the provider rule, not the generic tail.
        def _note(kind, tok):
            fp = line_fingerprint(content)
            key = (kind, path, fp)
            if key in seen:
                seen[key]["commits"].add(commit)
                return
            accepted = ("%s|%s|%s" % (kind, path, fp)) in baseline or any(
                pr["rule"] == kind and pr["re"].search(path) for pr in path_rules)
            seen[key] = {
                "rule": kind, "file": path, "line": lineno,
                "masked": mask(tok), "first_commit": commit,
                "commits": {commit}, "severity": RULE_SEV[kind],
                "blocking": (kind in BLOCKABLE_RULES
                             and SEV_RANK[RULE_SEV[kind]] >= thr_rank
                             and not accepted),
            }
            rule_counts[kind] = rule_counts.get(kind, 0) + 1

        blockable_spans = []
        for rid, rex in BLOCKABLE_RES:
            for m in rex.finditer(content):
                tok = m.group()
                if ALLOW_RE.search(tok) or ALLOW_RE.search(content[:120]):
                    continue
                blockable_spans.append((m.start(), m.end()))
                _note(rid, tok)
        for m in COMBINED.finditer(content):
            idx = m.lastindex
            if idx is None:
                continue
            if any(m.start() < e and s < m.end()
                   for s, e in blockable_spans):
                continue
            kind = "ENT" if idx > len(RULE_NAMES) else RULE_NAMES[idx - 1]
            if kind == "ENT":
                continue
            tok = m.group()
            if ALLOW_RE.search(tok) or ALLOW_RE.search(content[:120]):
                continue
            _note(kind, tok)
    proc.wait()
    rows = list(seen.values())
    for r in rows:
        r["commit_count"] = len(r["commits"])
        del r["commits"]
    purge = {}
    for r in rows:
        purge.setdefault(r["file"], {})
        purge[r["file"]][r["rule"]] = purge[r["file"]].get(r["rule"], 0) + 1
    blocking_count = sum(1 for r in rows if r["blocking"])
    return {
        "findings": rows, "purge_targets": purge,
        "rule_counts": rule_counts, "blocking_count": blocking_count,
        "unique_findings": len(rows),
    }
