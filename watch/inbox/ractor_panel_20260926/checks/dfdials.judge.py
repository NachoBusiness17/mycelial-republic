# dfdials judge verification script, 2026-09-26
# Verifies byte claims both candidates hang the card kill condition on:
# "a debt row that fits two tiers with no tiebreak rule, or a dial with no
#  retirement receipt condition"
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
sys.path.insert(0, str(ROOT))
from tools.violation_ratchet import SCANNER_RULES, scanner_domain, fingerprint  # noqa: E402

print("== SECTION 1: baseline census (configs/violation_baseline.json) ==")
b = json.loads((ROOT / "configs" / "violation_baseline.json").read_text(encoding="utf-8"))
accepted = b.get("accepted", {})
print(f"total claims: {len(accepted)}")
by_rule = Counter(e.get("rule", "?") for e in accepted.values())
for rule, n in sorted(by_rule.items(), key=lambda kv: (-kv[1], kv[0])):
    print(f"  rule {rule}: {n}")
rules = set(by_rule)
print(f"distinct rules: {len(rules)}: {sorted(rules)}")
unknown = sorted(r for r in rules if r not in SCANNER_RULES and not r.startswith("mimosa-"))
print(f"rules outside SCANNER_RULES and not mimosa-* (candidate two admits this kills its tierer): {unknown}")
expires_rows = [fp for fp, e in accepted.items() if e.get("expires")]
print(f"rows using expires: {len(expires_rows)}")
ext = sum(1 for e in accepted.values() if not scanner_domain(e.get("rule", ""), e.get("file", "")))
scan_dom = len(accepted) - ext
print(f"scanner-domain claims: {scan_dom}; external claims: {ext}")

print()
print("== SECTION 2: dial partitions recomputed under each candidate mapping ==")
# candidate one: f(rule) total; unknown/namespaced -> manual-only
one = {
    "parse-error": "always-on", "unreadable": "always-on",
    "except-pass": "default-on", "bare-except": "default-on",
    "env-key-read": "default-on", "cwd-relative-path": "default-on",
    "file-too-long": "opt-in", "shell-true": "opt-in",
    "todo-undated": "manual-only",
}
def dial_one(rule):
    return one.get(rule, "manual-only")  # mimosa-* and unknown -> manual-only

# candidate two: first-match tree, least automated wins:
# manual-only (mimosa-* or by-design note) -> opt-in (except-pass, bare-except,
# env-key-read, shell-true) -> default-on (file-too-long) -> always-on (todo-undated, cwd-relative-path)
two_optin = {"except-pass", "bare-except", "env-key-read", "shell-true"}
def dial_two(rule, note):
    if rule.startswith("mimosa-") or "by design" in (note or "") or "by-design" in (note or ""):
        return "manual-only"
    if rule in two_optin:
        return "opt-in"
    if rule == "file-too-long":
        return "default-on"
    if rule in {"todo-undated", "cwd-relative-path"}:
        return "always-on"
    return "UNCLASSIFIABLE"

p1, p2 = Counter(), Counter()
unclass = []
for fp, e in accepted.items():
    p1[dial_one(e.get("rule", ""))] += 1
    d2 = dial_two(e.get("rule", ""), e.get("note", ""))
    p2[d2] += 1
    if d2 == "UNCLASSIFIABLE":
        unclass.append((fp, e.get("rule"), e.get("file")))
print(f"candidate one partition: {dict(p1)} sum={sum(p1.values())}")
print(f"candidate two partition: {dict(p2)} sum={sum(p2.values())}")
print(f"candidate two unclassifiable rows: {unclass}")

print()
print("== SECTION 3: row-level double-fit test (kill prong 1) ==")
# For candidate one the dial is a function of rule alone: a row can only fit two
# tiers if one rule mapped to two dials, which a dict table cannot express.
# Check instead that every live rule lands in exactly one branch of the table.
print(f"candidate one: dial = f(rule) total over {len(rules)} live rules; rules hitting the default branch (manual-only): "
      f"{sorted(r for r in rules if r not in one)}")
# For candidate two: which live rows satisfy MORE THAN ONE predicate of its tree?
multi = []
for fp, e in accepted.items():
    rule, note = e.get("rule", ""), e.get("note", "") or ""
    manual_pred = rule.startswith("mimosa-") or "by design" in note or "by-design" in note
    optin_pred = rule in two_optin
    default_pred = rule == "file-too-long"
    always_pred = rule in {"todo-undated", "cwd-relative-path"}
    n = sum([manual_pred, optin_pred, default_pred, always_pred])
    if n > 1:
        multi.append((fp, rule, e.get("file"), note[:60]))
print(f"candidate two: live rows matching >1 dial predicate (tiebreak must exist for these): {multi}")
by_design_scan = [(fp, e.get("rule"), e.get("file")) for fp, e in accepted.items()
                  if scanner_domain(e.get("rule", ""), e.get("file", ""))
                  and ("by design" in (e.get("note") or "") or "by-design" in (e.get("note") or ""))]
print(f"candidate two: scanner-domain rows with by-design note (the cross-tier case): {by_design_scan}")
by_design_all = [(fp, e.get("rule"), e.get("file")) for fp, e in accepted.items()
                 if "by design" in (e.get("note") or "") or "by-design" in (e.get("note") or "")]
print(f"candidate two: ALL rows with by-design note: {len(by_design_all)} -> {by_design_all}")

print()
print("== SECTION 4: mixed-dial files (file-level ambiguity) ==")
files_one = defaultdict(set)
files_two = defaultdict(set)
for fp, e in accepted.items():
    files_one[e.get("file", "?")].add(dial_one(e.get("rule", "")))
    files_two[e.get("file", "?")].add(dial_two(e.get("rule", ""), e.get("note", "")))
mixed_one = {f: sorted(d) for f, d in files_one.items() if len(d) > 1}
mixed_two = {f: sorted(d) for f, d in files_two.items() if len(d) > 1}
print(f"candidate one: files carrying >1 dial: {len(mixed_one)}")
for f in ["tools/pupeteer_gauntlet.py", "tools/wandr_selfeval.py", "tools/steer_compare.py", "tools/ghost_tournament.py"]:
    print(f"  {f}: dials={sorted(mixed_one.get(f, files_one.get(f, set())))}")
print(f"candidate two: files carrying >1 dial: {len(mixed_two)}")
print(f"  mag/knowledge_graph.py: dials={sorted(mixed_two.get('mag/knowledge_graph.py', files_two.get('mag/knowledge_graph.py', set())))}")

print()
print("== SECTION 5: named live claims ==")
for fp, e in sorted(accepted.items(), key=lambda kv: kv[1].get("file", "")):
    if e.get("file") in ("mag/icon_drop.py", "mag/max_distill.py"):
        recomputed = fingerprint(e.get("rule", ""), e.get("file", ""), e.get("detail", ""))
        print(f"  {fp} rule={e.get('rule')} file={e.get('file')} accepted={e.get('accepted')} "
              f"by={e.get('by')} note={(e.get('note') or '')[:70]!r} fp_recomputes={recomputed == fp}")

print()
print("== SECTION 6: dfhack_fixes.json mode census (corpus/df_mine/) ==")
dj = (ROOT / "corpus" / "df_mine" / "dfhack_fixes.json").read_text(encoding="utf-8")
data = json.loads(dj)
entries = data if isinstance(data, list) else data.get("fixes") or list(data.values())
print(f"top-level type: {type(data).__name__}; entries counted: {len(entries) if isinstance(entries, list) else 'n/a'}")
if isinstance(data, dict) and not isinstance(entries, list):
    for k in list(data)[:10]:
        v = data[k]
        print(f"  key {k}: {type(v).__name__} len={len(v) if hasattr(v, '__len__') else '?'}")
modes = Counter()
auto_plus_manual = 0
auto_total = 0
retired = 0
if isinstance(entries, list):
    for fx in entries:
        if not isinstance(fx, dict):
            continue
        if fx.get("retired") or fx.get("status") == "retired" or "retired" in str(fx.get("mode", "")):
            retired += 1
        m = str(fx.get("mode", ""))
        if "always" in m and "on load" in m:
            modes["always-on"] += 1
        elif "default-enabled" in m or "default-enabled" in str(fx.get("note", "")):
            modes["default-on"] += 1
        elif "NOT default" in m or "opt-in" in m:
            modes["opt-in"] += 1
        else:
            modes["manual-only(other)"] += 1
        if ("always" in m or "default-enabled" in m or "periodic" in m) and "manual" in m:
            auto_plus_manual += 1
        if "always" in m or "default-enabled" in m or "periodic" in m:
            auto_total += 1
    print(f"mode census (heuristic keyword bins): {dict(modes)}; retired-flag rows: {retired}")
    print(f"automatic-mode entries: {auto_total}; of those also carrying '+ manual': {auto_plus_manual}")
else:
    print("unexpected dfhack_fixes.json shape; keys above")
print()
print("== SECTION 7: byte-cited line spot checks (dfhack_fixes.json) ==")
lines = dj.splitlines()
for want in [108, 233, 288, 297, 460]:
    if want <= len(lines):
        print(f"  line {want}: {lines[want-1][:150]}")

print()
print("== SECTION 8: candidate two tierer log present? ==")
tl = ROOT / "watch/inbox/ractor_panel_20260926/cands/dfdials-two_tierer_check.txt"
print(f"exists: {tl.exists()} size: {tl.stat().st_size if tl.exists() else 0}")
if tl.exists():
    txt = tl.read_text(encoding="utf-8", errors="replace")
    print("--- first 40 lines of tierer log ---")
    for ln in txt.splitlines()[:40]:
        print(f"  {ln}")
    print(f"--- tierer log total lines: {len(txt.splitlines())} ---")
print()
print("JUDGE SCRIPT DONE")
