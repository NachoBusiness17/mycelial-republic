#!/usr/bin/env python3
"""B2-94 board close, one pass on fresh bytes each step (claim law):
1. flip the leading CLAIM token to CLAIMED with -> receipt on this lane's two claim lines,
2. append the landing annotation to the pre-checked B2-94 row (earns the check per B2-238),
3. append 3 self-fed briefs UNCHECKED under Open at highest+1 (B2-441..443, B2-167 law),
4. append the LEDGER row via json.dumps.
Idempotent-guarded: each step is skipped if its target text is already present.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QUEUE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_94_mimosa_tail_20260926.md"

CLAIMS = [
    ("- CLAIM B2-94 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T18:31:20Z",
     "- CLAIMED B2-94 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T18:31:20Z"),
    ("- CLAIM B2-94 configs/violation_baseline.json 2026-09-26T18:31:20Z",
     "- CLAIMED B2-94 configs/violation_baseline.json 2026-09-26T18:31:20Z"),
]
ROW_MARK = "never touch the watch/inbox mimosa claims."
ROW_LANDING = (
    " Landed 2026-09-26 (row sat pre-checked [x] with no landing note, the B2-238 "
    "disease; this landing earns the check): bytes say 19 occurrences / 13 distinct "
    "findingIds / 13 (file, publicClass) pairs across the same 10 files, the brief's "
    "14 (tools/ 9) undercounted pupeteer_gauntlet (3 not 2) and dropped the tier_probe "
    "and wandr_selfeval CWE-95 code-injection findings; 1 FIXED tools/wandr_selfeval.py "
    "ssrf :128 (fetch_url fetched a model-authored submission URL to any host; probe PRE "
    "fetched a loopback canary 200 with listener hit 1, POST refuses non-public resolved "
    "addresses with 0 hits, file:// gold path intact 22985 bytes, selftest PASS, spec line "
    "landed in the fetch_url docstring first; pre sha256 dbb8803ce973268f, post "
    "6b8a0146acfdcc56, 680 to 703 lines, file-too-long already registered); 12 REGISTERED "
    "as named mimosa-* claims (mimosa-ssrf/path-traversal/code-injection/command-injection, "
    "scanner-impossible rules so prune keeps them per B2-95) via B2_94_baseline_update.py on "
    "fresh bytes rebased past the concurrent B2-96 landing, register 920 to 932, 0 collisions; "
    "watch/inbox 25 mimosa claims untouched (still under B2-11's by-field); models/ verdict "
    "false-positive/by-config: providers.py urls build from configs/providers.yaml base_url "
    "plus the DESIGNED base_url_env override with 30+ mag/ importers passing provider ids "
    "never URLs, probe.py target is a hardcoded literal; ratchet check --changed PASS NEW=0; "
    "CONFIG-SEAL update by name + verify PASS 49/49; receipt "
    + RECEIPT + "; self-fed B2-441, B2-442, B2-443 UNCHECKED."
)
BRIEFS = [
    "- [ ] B2-441 Pin the fetch_url public-host guard fixture-first: (self-fed by B2-94) the "
    "B2-94 guard (_assert_public_http_host in tools/wandr_selfeval.py) landed probe-proven "
    "(watch/inbox/burn_wave_20260926/B2_94_falsifier_probe.py) but has no pytest pins, so a "
    "future edit can drop the guard call or widen the scheme gate with zero red; add a test "
    "file pinning: loopback refusal as an error row not a crash, 169.254.169.254 link-local "
    "refusal, ::ffff:127.0.0.1 mapped-form refusal, file:// pass-through, nonexistent-host "
    "error row, and that fetch_url still calls the guard (sentinel via monkeypatch); "
    "falsifier: delete the _assert_public_http_host call inside fetch_url and no test goes "
    "red; pointers tools/wandr_selfeval.py (_assert_public_http_host, fetch_url), "
    "watch/inbox/burn_wave_20260926/B2_94_mimosa_tail_20260926.md Falsifier section.",
    "- [ ] B2-442 Spec the providers base_url surface: (self-fed by B2-94) 4 of the 12 "
    "registered mimosa tail claims ride models/providers.py url = f\"{base}/chat/completions\" "
    "where base = provider_base_url (configs/providers.yaml base_url plus the designed "
    "base_url_env override, models/providers.py:154-161), and the B2-94 registration accepted "
    "them on the reason that the source is operator-owned config with no untrusted input and "
    "a host allowlist would break the designed env-override feature, but no spec owns that "
    "surface, so the next feature that lets a caller pass a URL-shaped provider id or a new "
    "env override re-opens the class with no policy to point at; write the spec (doc block in "
    "models/providers.py or the configs/providers.yaml header: allowed base_url sources, "
    "scheme policy, whether non-loopback http is a declared non-goal) and pin it or register "
    "the policy decision by name; falsifier: a providers.yaml row with base_url "
    "\"http://127.0.0.1:9\" flows into url today and no doc, gate or row names the policy; "
    "pointers models/providers.py provider_base_url, configs/providers.yaml, "
    "watch/inbox/burn_wave_20260926/B2_94_mimosa_tail_20260926.md.",
    "- [ ] B2-443 Resolve the B2-95 receipt citation: (self-fed by B2-94) "
    "tools/violation_ratchet.py:16 cites watch/inbox/burn_wave_20260926/B2_95_prune_gap_20260926.md "
    "as the B2-95 receipt, which did not resolve on disk at 18:40Z 2026-09-26 while B2-95's "
    "board claims were still active CLAIM; if B2-95 lands, retire this row as covered; if "
    "B2-95 dies, the citation is a ghost per the B2-337 law and gets reconstructed from the "
    "ratchet docstring + baseline rows or retired; falsifier: the receipt pointer in the "
    "ratchet docstring resolves after this row closes; pointers tools/violation_ratchet.py:16, "
    "watch/inbox/burn_wave_20260926/QUEUE.md B2-95 rows, "
    "watch/inbox/burn_wave_20260926/B2_337_ghost_resolve_20260926.md.",
]

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# step 1+2+3: board, fresh read each replacement
q = QUEUE.read_text(encoding="utf-8")
for pre, post in CLAIMS:
    if pre in q:
        line_end = q.index("\n", q.index(pre))
        line = q[q.index(pre):line_end]
        if "->" not in line:
            q = q[:q.index(pre)] + line + " -> " + RECEIPT + q[line_end:]
            print("CLAIMED flip:", post.split(" ", 2)[2][:40])
    elif post in q:
        print("already CLAIMED:", post[:50])
row_key = ROW_MARK
if ROW_LANDING.strip()[:40] not in q:
    idx = q.index(row_key)
    q = q[:idx + len(row_key)] + ROW_LANDING + q[idx + len(row_key):]
    print("B2-94 row annotated")
else:
    print("B2-94 row already annotated")
tail_add = ""
for b in BRIEFS:
    if b[:30] not in q:
        tail_add += b + "\n"
if tail_add:
    if not q.endswith("\n"):
        q += "\n"
    q += tail_add
    print("self-fed briefs appended:", len(BRIEFS))
QUEUE.write_text(q, encoding="utf-8")

# step 4: LEDGER row via json.dumps
row = {
    "ts": now,
    "slug": "B2-94-mimosa-live-tail-triage",
    "verdict": "LANDED",
    "landing": RECEIPT,
    "one_line": (
        "B2-94 mimosa live tail: brief said 14 (tools/ 9 in 8 files + models/ 5), seal bytes "
        "hold 19 occurrences / 13 findingIds / 13 (file, publicClass) pairs across the same 10 "
        "files (brief dropped pupeteer ssrf :84 and the tier_probe/wandr CWE-95 findings); 1 "
        "FIXED tools/wandr_selfeval.py ssrf :128, fetch_url re-fetched model-authored submission "
        "URLs to any host, _assert_public_http_host (getaddrinfo + ipaddress.is_global, refused "
        "as error rows, TOCTOU window named) added spec-line-first in the fetch_url docstring, "
        "probe both directions on real bytes: PRE loopback canary fetched 200 listener hit 1, "
        "POST refused 0 hits, file:// gold intact 22985 bytes, dead host error row, selftest "
        "PASS, pre sha dbb8803ce973268f post 6b8a0146acfdcc56, 680 to 703 lines; 12 REGISTERED "
        "as mimosa-* accepted claims (scanner-impossible rules, prune-proof per B2-95) with "
        "per-file triage reasons vs real callers (providers.py config+designed env override 30+ "
        "mag/ importers, probe/ghost/steer hardcoded literals, pupeteer _E_CMDS constants, "
        "tier_probe by-design exec-of-candidate-code, projects_index v5 constant mouths, "
        "compaction_eval operator CLI arg, fold_mickey17 constant join, wandr code-injection "
        "false positive on the filename, no eval/exec in file), register 920 to 932 fresh-bytes "
        "rebased past concurrent B2-96, 0 collisions; watch/inbox 25 mimosa claims untouched; "
        "ratchet check --changed PASS NEW=0; CONFIG-SEAL update by name verify PASS 49/49; "
        "self-fed B2-441 to B2-443 unchecked"
),
    "lane": "B2-94",
}
with open(LEDGER, "a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("LEDGER row appended at", now)
sys.exit(0)
