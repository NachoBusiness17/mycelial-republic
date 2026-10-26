#!/usr/bin/env python3
"""B2-94 mimosa tail: register the live-code tools/+models/ mimosa findings as
accepted debt in configs/violation_baseline.json, BY NAME, with date+reason.

Scope: exactly the 19 occurrences (13 distinct findingIds, 13 (file, class)
pairs) the sealed scan scan-2026-09-26T04-10-04.918Z-41fc75fa84c4 reports for
the 10 brief-named files. One pair is FIXED by this lane, not registered:
tools/wandr_selfeval.py ssrf :128 (fetch_url now refuses non-public hosts,
receipt watch/inbox/burn_wave_20260926/B2_94_mimosa_tail_20260926.md). The
other 12 pairs register here. The brief said "9 findings in 8 files" +
"models/ 5" = 14; the seal bytes hold 19 occurrences / 13 findingIds; bytes win.

Fingerprints reuse tools/violation_ratchet.py's fingerprint(rule, file, detail)
scheme with namespaced rules (mimosa-ssrf / mimosa-path-traversal /
mimosa-code-injection / mimosa-command-injection) that the scanner can never
emit, so prune keeps them (B2-95 scanner_domain contract).

Rebase: the file carries an active foreign CLAIM (B2-95 2026-09-26T18:25:53Z);
this script re-reads fresh bytes immediately before its single read-modify-
write and records pre/post sha256 in its output.
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = Path(r"C:\Users\foste\.mimosa\security-scans"
                r"\project-8af8c49a6c1b0282e16b1e73"
                r"\scan-2026-09-26T04-10-04.918Z-41fc75fa84c4\findings.json")
BASELINE = ROOT / "configs" / "violation_baseline.json"
SCAN_ID = "scan-2026-09-26T04-10-04.918Z-41fc75fa84c4"
BY = "agent:B2-94 flash-lane burn 2026-09-26 (mimosa live tail triage)"
TODAY = "2026-09-26"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_94_mimosa_tail_20260926.md"

RULE_NAME = {
    "ssrf": "mimosa-ssrf",
    "path-traversal": "mimosa-path-traversal",
    "code-injection": "mimosa-code-injection",
    "command-injection": "mimosa-command-injection",
}
FIXED = {("tools/wandr_selfeval.py", "ssrf")}

SCOPE = {
    "models/providers.py", "models/probe.py", "tools/ghost_tournament.py",
    "tools/steer_compare.py", "tools/pupeteer_gauntlet.py",
    "tools/tier_probe.py", "tools/wandr_selfeval.py",
    "tools/index/projects_index.py", "tools/compaction_eval.py",
    "tools/fold_mickey17.py",
}

NOTES = {
    "models/providers.py":
        "live estate provider client, imported across mag/ (chat_provider, "
        "chat_messages, chat_routed, api_gateway, doctor); url built at :387/:679/:822 "
        "from provider_base_url = configs/providers.yaml base_url plus the DESIGNED "
        "base_url_env override (e.g. VAST_OPENAI_BASE_URL); callers pass provider ids, "
        "no untrusted input reaches the URL, so the SSRF class does not apply to an "
        "operator-owned config source; registered not fixed: a host allowlist would "
        "break the designed env-override feature with no spec asking for it",
    "models/probe.py":
        "false positive: urlopen target is the hardcoded literal "
        "https://openrouter.ai/api/v1/chat/completions, zero dynamic URL component, "
        "key from env; operator-run probe CLI, nothing imports it",
    "tools/ghost_tournament.py":
        "false positive: urlopen target is the hardcoded literal "
        "http://localhost:11434/api/chat (local ollama); operator-run eval one-shot",
    "tools/steer_compare.py":
        "false positive: urlopen target is the hardcoded literal "
        "http://localhost:11434/api/chat (local ollama); operator-run eval one-shot",
    "tools/pupeteer_gauntlet.py|ssrf":
        "false positive: _base() resolves config.ollama_base() (operator config, "
        "local ollama) for the /api/tags liveness probe; operator-run gauntlet",
    "tools/pupeteer_gauntlet.py|command-injection":
        "by-design: subprocess.run(shell=True) executes only module-constant "
        "_E_CMDS values (3 hardcoded pytest/pip commands) via _E_CMDS.get(cc); "
        "no model-authored or external string reaches cmd; the ratchet's own "
        "shell-true claim c2a40c35650136c1 already covers this site, this row "
        "names the mimosa finding on it",
    "tools/tier_probe.py|code-injection":
        "by-design: exec(compile(ast.parse(...))) runs candidate parse_ts code "
        "against a hidden unit test, which IS the tier probe's scoring contract; "
        "operator-run eval of model output (executing candidate code is the "
        "measured behavior), AST-gated, no eval-of-raw-string; registered not "
        "fixed: sandboxing is a redesign out of this lane's scope",
    "tools/tier_probe.py|ssrf":
        "same class as models/providers.py: url built from provider_base_url("
        "get_provider('deepseek')) config source; operator CLI, no untrusted input",
    "tools/wandr_selfeval.py|code-injection":
        "false positive on the filename: the flagged line 2 is the module "
        "docstring; byte-verified 2026-09-26 that no eval(/exec( call exists "
        "anywhere in the file",
    "tools/index/projects_index.py":
        "false positive, stale against the v5 design: all three opens write "
        "compile-time constants (MASTER/ROLLUP/LAST_RUN, header 'fixed mouths' "
        "note); walked paths enter only as JSON content, never as a path",
    "tools/compaction_eval.py":
        "operator CLI arg: open(os.path.join(args.out, 'eval_20260920.json')) "
        "where --out is the operator's own flag on a local one-shot; no "
        "untrusted input path",
    "tools/fold_mickey17.py":
        "false positive: RUNS is a module-constant path join and the filename "
        "is the constant 'MASTER_INDEX_20260920.md'",
}


def fingerprint(rule: str, file: str, detail: str) -> str:
    return hashlib.sha256(f"{rule}\0{file}\0{detail}".encode("utf-8")).hexdigest()[:16]


def main() -> int:
    data = json.loads(FINDINGS.read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    for f in data["findings"]:
        p = f["location"]["path"]
        cls = f.get("identity", {}).get("publicClass")
        if p in SCOPE and cls in RULE_NAME and (p, cls) not in FIXED:
            grouped[(p, cls)].append((f["location"]["line"],
                                      f["findingId"].replace("finding:", "")[:12]))

    pre = BASELINE.read_bytes()
    pre_sha = hashlib.sha256(pre).hexdigest()
    baseline = json.loads(pre.decode("utf-8"))
    accepted = baseline.setdefault("accepted", {})

    added, skipped = [], []
    for (path, cls), occ in sorted(grouped.items()):
        occ_lines = sorted({ln for ln, _ in occ})
        ids = sorted({fid for _, fid in occ})
        detail = (f"{len(occ)} occurrence(s) at lines "
                  f"{', '.join(map(str, occ_lines))}; findingIds {', '.join(ids)}; {SCAN_ID}")
        note_key = f"{path}|{cls}" if f"{path}|{cls}" in NOTES else path
        note = (NOTES[note_key] + "; triaged against real callers 2026-09-26 by B2-94, "
                "mimosa-sourced claim under a rule the scanner cannot emit so prune "
                "keeps it (B2-95 scanner_domain), re-triage from " + RECEIPT)
        fp = fingerprint(RULE_NAME[cls], path, detail)
        if fp in accepted:
            skipped.append(fp)
            continue
        accepted[fp] = {
            "accepted": TODAY, "by": BY, "detail": detail,
            "file": path, "note": note, "rule": RULE_NAME[cls],
        }
        added.append((fp, RULE_NAME[cls], path, len(occ)))

    out = json.dumps(baseline, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    BASELINE.write_text(out, encoding="utf-8")
    post_sha = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
    print(json.dumps({
        "pre_sha256": pre_sha, "post_sha256": post_sha,
        "added": [{"fp": fp, "rule": r, "file": p, "occurrences": n} for fp, r, p, n in added],
        "already_registered": skipped,
        "total_registered_after": len(accepted),
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
