"""secret_gate - repo secret-scan gate (PACK_SECRET_GATE_20260926 section 4).

Detector ONLY: it reports and blocks, it fixes nothing, it edits nothing.

Borrowed, verbatim, per pack section 2 (do not rewrite, do not improve):
  - the rule table, ALLOW_RE exemption, combined matcher and its self-checks
    come from watch/inbox/burn_wave_20260926/B2_73_secret_scan.py (the table
    sits at lines 28-60 of that file and holds 31 rules; the pack's "28 rules
    at lines 28-57" is a miscount, the table bytes are what count);
  - the redaction shape-exemption concept (a human-redacted token is not a
    finding) comes from scripts/sanitize_dossiers.py KEY_PATTERNS; the
    borrowed ALLOW_RE already carries that concept (REDACTED, MASKED, ...),
    so the exemption lives inline here and nothing is imported from the
    redactor. A change to the redactor cannot silently disarm this gate.

S3 (pack section 3): AWS-SECRET-40 is entropy-gated. Cause: the regex is
"any 40-char base64-ish run", so git OIDs and hex blobs matched; the one
real run (2026-09-26, watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json)
counted 48,427 hits = 80% of all findings, which buried the one critical.
Fix: a hit below the entropy floor the scanner already computes (shannon
< 4.3, the ENT branch threshold) is dropped before counting. Hex SHAs sit
near 3.9 bits/char and cannot pass; real 40-char base64 AWS secrets pass.

S4 (pack section 3): machine rows carry COUNTS plus a results-file path,
never the per-file list. Cause: the 2026-09-26 beat row embedded a 4,812
entry files_with_rule_hits list and weighed 641,924 bytes for ONE run
(watch/inbox/SECRET_SCAN_BEAT.jsonl, verified by reading the row).

Blocking tier (pack section 4, ruling 3): only specific provider shapes can
block, and only at or above --severity (default high). AWS-SECRET-40,
GENERIC-KEYASSIGN, ENV-ASSIGN, JWT-TRIPLE and GENERIC-BEARER NEVER block.

Day one baseline is ZERO (pack section 4, ruling 4): no baseline file ships
with this tool and no debts are imported from configs/violation_baseline.json.
--baseline accepts a named-acceptance file in that B3 shape only.

Secret values are never printed: every row is path:line:rule:severity plus
at most a masked head (first 6 chars) and the token length.

Exit codes:
  0  clean, or only report-tier findings
  1  BLOCKING finding at or above the --severity threshold
  2  scanner error (git failure, unreadable baseline, internal error, or
     not running on the repo venv). Callers must treat 2 as "detector
     blind", never as success.

Run: .venv/Scripts/python.exe tools/secret_gate.py --full
     .venv/Scripts/python.exe tools/secret_gate.py --changed
Optional positional paths narrow the scan to those files/dirs (testability
and ad-hoc scans); the pack flags keep their exact meaning.

SPLIT 2026-09-27 (ratchet file-too-long fix): the rule table, thresholds,
block sets, GateError and baseline acceptance (load_baseline) moved to
tools/secret_gate_rules.py; the scanning core to tools/secret_gate_scan.py;
this file keeps the CLI. A pure code move with two
documented equivalences (len(RULES) -> len(RULE_NAMES), identical by
construction; the routing self-check probe now concatenated so no key-shaped
run sits in source, runtime string byte-identical). Split falsifier:
state/fuel/sg_split_ref/ — pre/post counts on a fixed scope with prefilter
on and off must match exactly. CLI, exit codes and hook contract unchanged.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import argparse  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402

from tools.secret_gate_rules import (  # noqa: E402,F401
    ALLOW_RE,
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
    RESULTS_DIR,
    RULE_NAMES,
    RULE_SEV,
    SEV_RANK,
    SELF_SKIP_RELPATHS,
    SNIFF_BYTES,
    SKIP_DIR_PARTS,
    load_baseline,
)
from tools.secret_gate_scan import (  # noqa: E402
    changed_files,
    history_scan,
    iter_scope_files,
    iter_tree_files,
    scan,
)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="secret_gate",
        description="Secret-scan gate. Exit 0 clean/report-tier only, "
                    "1 blocking finding, 2 scanner error (never silently 0).")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--changed", action="store_true",
                      help="scan files changed vs upstream plus staged, "
                           "unstaged and untracked (fast path, for pre-push)")
    mode.add_argument("--full", action="store_true",
                      help="whole-tree scan (offline / scheduled)")
    mode.add_argument("--history", action="store_true",
                      help="scan every ADDED line across git history (steal 4, "
                           "gitleaks git mode): the purge target list for the "
                           "filter-repo step. Slow; manual; never in the hook.")
    ap.add_argument("--severity", choices=["critical", "high", "medium", "low"],
                    default="high",
                    help="block at or above this tier (default high: "
                         "critical,high block; medium,low report only). "
                         "Generic-shape rules never block at any tier.")
    ap.add_argument("--baseline", metavar="PATH", default=None,
                    help="named acceptance file, B3 shape "
                         "{\"accepted\": {fp: {...}}}; day one is zero "
                         "baseline and none ships with this tool")
    ap.add_argument("--json", action="store_true",
                    help="machine output for the beat row (one compact line)")
    ap.add_argument("paths", nargs="*", metavar="PATH",
                    help="optional: narrow the scan to these files/dirs "
                         "(ad-hoc scans and acceptance tests)")
    args = ap.parse_args(argv)

    # Fail closed on environment: this tool must run on the repo venv. If the
    # venv were missing its interpreter could not run at all, so any foreign
    # interpreter here means the environment is not the sanctioned one.
    exe_dir = os.path.normcase(os.path.dirname(os.path.abspath(sys.executable)))
    venv_dir = os.path.normcase(os.path.join(REPO, ".venv"))
    if not exe_dir.startswith(venv_dir + os.sep) and exe_dir != venv_dir:
        print("secret_gate: not running on the repo venv (%s); "
              "use .venv/Scripts/python.exe" % sys.executable, file=sys.stderr)
        return 2

    baseline = {}
    path_rules = []
    if args.baseline:
        baseline, path_rules = load_baseline(args.baseline)

    if args.history:
        t0 = time.time()
        res = history_scan(baseline, path_rules, args.severity)
        runtime = round(time.time() - t0, 1)
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_rel = "watch/inbox/secret_gate_results/history_%s.json" % ts
        with open(os.path.join(REPO, results_rel), "w", encoding="utf-8",
                  newline="\n") as out:
            json.dump({
                "tool": "tools/secret_gate.py", "mode": "history",
                "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "runtime_sec": runtime,
                "unique_findings": res["unique_findings"],
                "blocking_count": res["blocking_count"],
                "rule_counts": res["rule_counts"],
                "purge_targets": res["purge_targets"],
                "findings": res["findings"],
            }, out, indent=1)
        print("mode=history runtime_sec=%s unique_findings=%d blocking=%d"
              % (runtime, res["unique_findings"], res["blocking_count"]))
        for rid, n in sorted(res["rule_counts"].items(),
                             key=lambda kv: -kv[1])[:15]:
            print("  history %-22s %d" % (rid, n))
        for p in sorted(res["purge_targets"],
                        key=lambda p: -sum(res["purge_targets"][p].values()))[:15]:
            print("  purge-target %s : %s" % (p, res["purge_targets"][p]))
        print("results: %s" % results_rel)
        print("operator response: this is the filter-repo purge list; "
              "rotate anything live BEFORE stripping history")
        return 1 if res["blocking_count"] else 0

    t0 = time.time()
    mode_name = "changed" if args.changed else "full"
    if args.paths:
        scope_paths = [os.path.abspath(p) for p in args.paths]
        files = list(iter_scope_files(scope_paths))
        upstream = "n/a"
        basis = "explicit"
    elif args.changed:
        upstream, files = changed_files()
        basis = ("upstream..HEAD+worktree+untracked" if upstream
                 else "worktree+untracked (no upstream configured)")
    else:
        upstream = "n/a"
        basis = "tree"
        files = list(iter_tree_files())

    res = scan(files, baseline, path_rules, args.severity)
    runtime = round(time.time() - t0, 1)

    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    results_rel = None
    n_findings = (sum(res["rule_counts"].values())
                  + res["entropy"]["stored"])
    if (args.full and not args.paths) or res["blocking_count"] or n_findings:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_rel = "watch/inbox/secret_gate_results/%s_%s.json" % (mode_name, ts)
        with open(os.path.join(REPO, results_rel), "w", encoding="utf-8",
                  newline="\n") as out:
            json.dump({
                "tool": "tools/secret_gate.py", "mode": mode_name,
                "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "scope_basis": basis,
                "severity_threshold": args.severity,
                "census": res["census"],
                "rule_counts": res["rule_counts"],
                "severity_counts": res["severity_counts"],
                "blocking_count": res["blocking_count"],
                "blocking": res["blocking"],
                "accepted_count": res["accepted_count"],
                "files_with_rule_hits_count": res["files_with_rule_hits_count"],
                "entropy": res["entropy"],
                "entropy_files_count": res["entropy_files_count"],
                "s3": res["s3"],
                "thresholds": {"entropy_min": ENTROPY_MIN,
                               "ent_len_min": ENT_LEN_MIN,
                               "max_file_bytes": MAX_FILE_BYTES},
                "findings_stored": res["findings_stored"],
            }, out, indent=1)

    row = {
        "tool": "tools/secret_gate.py",
        "schema": "secret_gate_beat.v1",       # S4 shape: counts + results path
        "mode": mode_name,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scope_basis": basis,
        "severity_threshold": args.severity,
        "census": res["census"],
        "severity_counts": res["severity_counts"],
        "rule_counts": res["rule_counts"],
        "blocking_count": res["blocking_count"],
        "accepted_count": res["accepted_count"],
        "files_with_rule_hits_count": res["files_with_rule_hits_count"],
        "entropy_total": res["entropy"]["total"],
        "s3_aws_secret_entropy_filtered": res["s3"]["aws_secret_entropy_filtered"],
        "blocking_sample": [
            {"file": b["file"], "line": b["line"], "rule": b["kind"],
             "severity": b["severity"], "masked": b["masked"]}
            for b in res["blocking"][:10]
        ],
        "results_file": results_rel,           # S4: path, never the file list
        "runtime_sec": runtime,
    }

    exit_code = 1 if res["blocking_count"] else 0

    if args.json:
        print(json.dumps(row, separators=(",", ":")))
    else:
        print("mode=%s scope=%s files_scanned=%d runtime_sec=%s"
              % (mode_name, basis, res["census"]["scanned"], runtime))
        sc = res["severity_counts"]
        print("severity: critical=%d high=%d medium=%d low=%d"
              % (sc["critical"], sc["high"], sc["medium"], sc["low"]))
        print("s3: aws_secret_entropy_filtered=%d"
              % res["s3"]["aws_secret_entropy_filtered"])
        print("blocking=%d (threshold=%s, provider shapes only)"
              % (res["blocking_count"], args.severity))
        for b in res["blocking"][:50]:
            print("  %s:%d:%s:%s masked=%s"
                  % (b["file"], b["line"], b["kind"], b["severity"], b["masked"]))
        if res["blocking_count"] > len(res["blocking"]):
            print("  ... and %d more (see results file)" %
                  (res["blocking_count"] - len(res["blocking"])))
        if results_rel:
            print("results: %s" % results_rel)
        if exit_code == 1:
            print("operator response: excise or rotate the value, or accept THAT "
                  "finding by name in configs/secret_gate_baseline.json "
                  "(accepted_by + reason, or a paths entry); never loosen the hook")
        print("exit=%d %s" % (exit_code,
              "BLOCKING findings present" if exit_code == 1 else "clean or report-tier only"))
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GateError as e:
        print("secret_gate: scanner error: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # fail closed on any internal error
        print("secret_gate: internal error: %s: %s" % (type(e).__name__, e),
              file=sys.stderr)
        sys.exit(2)
