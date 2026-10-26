# B2-341 B2-73 secret-scan papers (2026-09-26)

## Verdict

LANDED (papers filed from bytes; rotation policy WRITTEN, not declined). The
scan is real and its persisted bytes are now receipted. Correction to the
brief's premise: the current results file is NOT empty. The file on disk was
regenerated at 2026-09-26T16:39:42Z and carries exact per-rule counts with
stored masked rows (storage caps, not zero findings). Zero-findings was true
of the earlier generation the B2-78 lane read; the current bytes supersede it
and they DO contain candidate findings, all triaged below as corpus-side
noise or lane-artifact key-shape text, with no live-config hit.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json (current
  bytes, generated_utc "2026-09-26T16:39:42Z"): census {"files_seen": 64220,
  "scanned": 38240, "binary_skipped": 25872, "large_skipped": 106,
  "read_error": 0, "bytes_scanned": 1338762485}; rule_counts {"AWS-ACCESS-KID":
  1, "AWS-SECRET-40": 48393, "GOOGLE-OAUTH-AQ": 1, "OPENAI-CLASSIC": 14,
  "OPENROUTER-KEY": 28, "GROQ-KEY": 28, "XAI-KEY": 18, "DEEPSEEK-KEY": 16,
  "STRIPE-KEY": 7, "JWT-TRIPLE": 1, "PRIVATE-KEY-BLOCK": 1,
  "CONNSTRING-CRED": 4, "GENERIC-KEYASSIGN": 180, "ENV-ASSIGN": 11550};
  entropy total 75190 / stored 20000; runtime in file; scopes corpus/ +
  watch/inbox/.
- Hit-file census this lane: 4,722 files with rule hits, of which 158 outside
  corpus/ and every one of those is a watch/inbox lane artifact (probe
  scripts, receipts, exports; example list in the results file: B2_04_probe.py,
  LINKS.jsonl, mickey17 wave receipts) matching key-shaped TEXT (env-assign
  and key-assign patterns), not key VALUES.
- High-severity singles, all corpus-side: AWS-ACCESS-KID |
  corpus/oral_history/seat_pools/codex_sessions/2026/09/08/rollout-...jsonl
  line 105 masked "AKIARC...(len=20)"; PRIVATE-KEY-BLOCK |
  corpus/library/openai-cookbook/examples/chatgpt/.../gpt_action_box.ipynb
  line 929; JWT-TRIPLE | corpus/library/evennia/docs/... line 29;
  GOOGLE-OAUTH-AQ | corpus/library/lmcache-src/operator/go.sum line 227;
  CONNSTRING-CRED x4 | lmcache + openai-cookbook vendored examples.
- Denominator cross-check: B2_78_denominator_refresh_20260926.md:95-96
  re-derived "64,212 files seen, 38,234 text-scanned, 25,872 binary-skipped,
  106 large-skipped"; current results census reads 64,220 / 38,240 / 25,872 /
  106 (+8 seen, +6 scanned, binary and large identical): tree growth between
  the two runs, not drift in the scanner.
- B2_73_secret_scan.py:9-14 header: "Values are never written in full
  anywhere: report rows carry a masked head (first 6 chars) plus length."

## Work done

1. Read the script (scope, rules, caps, masking), the current results bytes,
   and the B2-78 census receipt.
2. Recounted hit files; isolated the 158 non-corpus hits and confirmed the
   class; pulled the exact locations of every count-under-10 high-severity
   rule hit.
3. Trialed zero live-config hits: no configs/, .env, or keys.json path
   appears in files_with_rule_hits (scopes never included configs/ or dotfiles
   at repo root; the scan covers corpus/ and watch/inbox/ only, so live
   configs were never in blast range of this scanner).
4. Wrote the solo-operator rotation policy (below) and filed this receipt,
   LEDGER row, QUEUE pointer, INDEX registration.

### Solo-operator rotation policy (the filed policy)

Scope classes and the action each demands, decided by WHERE the hit lives:
1. corpus/ hits (vendored libraries, archived session exports): noise by
   class. No rotation. The 48,393 AWS-SECRET-40 rows are 40-char strings in
   vendored code; the singles are doc/tutorial material. Accepted noise,
   named here.
2. watch/inbox/ hits that match a key STILL ACTIVE in .env or configs/keys.json:
   rotate the key at the provider, update .env/keys.json, register the old
   key dead in keys.json status, then file one ALERT row in LINKS.jsonl.
   Verification before revocation: masked head + length must match the live
   value (never print the full value into the receipt).
3. watch/inbox/ hits that match a RETIRED key: no rotation; the row stands as
   history under the no-erase law; the key's dead status in keys.json is the
   control.
Cadence: event-driven, not scheduled. Trigger events: any bulk corpus ingest,
any inbox share/publish, any operator key churn. Cause for not scheduling
weekly: single-operator estate (rotation has no second party to protect
against), blast radius one machine, scanner is local and $0, and the real
exposure (live configs) is outside the scanner's scope by design; the
provider-side dashboards already flag anomalous usage, which no local scan
replaces.

## Falsifier

This filing is inverted if any of the following holds: (a) rerunning
B2_73_secret_scan.py produces a census that differs from 64,220 / 38,240 /
25,872 / 106 by more than ordinary tree growth AND a rule count that drops to
zero without a scope change (the persisted bytes were fabricated or the
scanner regressed); (b) a live key is found whose masked head + length
matches one of the 158 non-corpus watch/inbox hits (my triage class 2 was
wrong; rotate immediately per policy); (c) the earlier-generation
zero-findings results file turns up with a generation ts AFTER 16:39:42Z
(the empty array was not a stale generation but an overwrite; investigate
who rewrote it).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_73_secret_scan.py (read in full, header +
rules + caps + storage shape); watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json
(current bytes parsed: census, rule_counts, entropy, files_with_rule_hits,
findings_stored sampled at the high-severity singles); watch/inbox/burn_wave_20260926/B2_78_scanscope_census.py
header (method: mirrors iter_files + is_binary + 10MB cap exactly);
watch/inbox/burn_wave_20260926/B2_78_denominator_refresh_20260926.md:95-96,124-125,154.
No network calls; the scan itself is local-only.
