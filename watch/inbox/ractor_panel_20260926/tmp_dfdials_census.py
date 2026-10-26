"""dfdials revision census: dial partition of the register + mixed-dial file census.

Run: .venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/tmp_dfdials_census.py
Reads configs/violation_baseline.json (never writes it).
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import violation_ratchet as vr  # noqa: E402

DIAL_BY_RULE = {
    "parse-error": "always-on",
    "unreadable": "always-on",
    "except-pass": "default-on",
    "bare-except": "default-on",
    "env-key-read": "default-on",
    "cwd-relative-path": "default-on",
    "file-too-long": "opt-in",
    "shell-true": "opt-in",
    "todo-undated": "manual-only",
    "mimosa-ssrf": "manual-only",
    "mimosa-path-traversal": "manual-only",
    "mimosa-code-injection": "manual-only",
    "mimosa-command-injection": "manual-only",
}


def dial_of(rule: str) -> str:
    # tiebreak clause (a): unknown/namespaced future rules -> manual-only
    return DIAL_BY_RULE.get(rule, "manual-only")


def main() -> None:
    baseline = json.loads((ROOT / "configs" / "violation_baseline.json").read_text(encoding="utf-8"))
    accepted = baseline.get("accepted", {})
    print(f"total claims: {len(accepted)}")

    # partition
    dial_counts = Counter(dial_of(e.get("rule", "")) for e in accepted.values())
    rule_counts = Counter(e.get("rule", "") for e in accepted.values())
    print("rule counts:", dict(sorted(rule_counts.items())))
    print("dial counts:", dict(sorted(dial_counts.items())))
    print("dial sum:", sum(dial_counts.values()))
    unstampable = [fp for fp, e in accepted.items() if e.get("rule", "") not in DIAL_BY_RULE]
    print(f"rows outside named rule table (fall to manual-only by clause a): {len(unstampable)}")

    # per-dial registered counts restricted to scanner-domain live claims? The
    # card's 678/197/58/0 partition counts REGISTER rows, not live hits.
    for d in ("always-on", "default-on", "opt-in", "manual-only"):
        rows = [fp for fp, e in accepted.items() if dial_of(e.get("rule", "")) == d]
        print(f"  {d}: {len(rows)} rows")

    # mixed-dial file census (live REGISTER claims, the mapping's own domain)
    by_file = defaultdict(set)
    for fp, e in accepted.items():
        by_file[e.get("file", "")].add(dial_of(e.get("rule", "")))
    mixed = {f: dials for f, dials in by_file.items() if len(dials) > 1}
    print(f"files with more than one dial among registered claims: {len(mixed)}")
    dial_pair_counts = Counter(tuple(sorted(d)) for d in mixed.values())
    print("mixed-dial composition:", dict(sorted(dial_pair_counts.items())))
    for name in ("tools/pupeteer_gauntlet.py", "tools/wandr_selfeval.py",
                 "tools/steer_compare.py", "tools/ghost_tournament.py"):
        dials = by_file.get(name, set())
        print(f"  {name}: {len(dials)} dials -> {sorted(dials)}")

    # always-on zero-hit proof: full scan, count hits by rule for the two rules
    hits = vr.all_violations()
    rule_hits = Counter(v["rule"] for v in hits)
    print(f"full-scope scan hits: {len(hits)} files_scanned={len(vr.iter_py_files(vr.DEFAULT_ROOTS))}")
    print(f"parse-error hits: {rule_hits.get('parse-error', 0)}; unreadable hits: {rule_hits.get('unreadable', 0)}")
    # NEW rows by rule/file for the sequencing bullet
    new = [v for v in hits if vr.fingerprint(v["rule"], v["file"], v["detail"]) not in accepted]
    print(f"NEW rows now: {len(new)}")
    for v in new:
        print(f"  NEW {vr.fingerprint(v['rule'], v['file'], v['detail'])} {v['rule']}: {v['file']}:{v['line']}")


if __name__ == "__main__":
    main()
