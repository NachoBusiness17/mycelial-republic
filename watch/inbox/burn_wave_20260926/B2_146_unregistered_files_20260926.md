# B2-146 receipt: unregistered inbox files (2026-09-26)

## Verdict

steal

## Evidence

- Fold of watch/inbox/index_events.jsonl (3,065 rows) before this lane: all five targets had zero prior events, zero history rows. INDEX.md shows register at log line 927 then invalidate at line 1381, SHARED_SURFACE_CONTRACT.json register at line 4 then invalidate at line 1379, both "retire: self-referential derived file, meta-files must never be hash-registered (patrol law 20260922)", writer drift-patrol-cron. Left retired as ordered.
- watch/inbox/EVENTS.jsonl read in full (51 event.v1 rows, 35,730 bytes): writers free-resource-scout 25, zcode-seat 6, endpoint-news 9, x-intel-dig 11, spanning 2026-09-20 to 09-26. Every row byte-matches its origin pointer in watch/inbox/LINKS.jsonl lines 275 to 331: 0 mismatches on id+title per row.
- ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc: 22,120,192 bytes, sha256 ADA2F62926F432ED4EA01FDCE867BC572860BFA181F5C59D35B958F8AB587C87, prefix-matching memory/trajectory/steps.jsonl:22168 whose command is the creator: "find memory/vault ... | tar ... | openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:configs/secrets/pack_key.txt -out $OUT ... cp $OUT /c/Users/foste/OneDrive/". OneDrive copy re-hashed this lane: byte-identical. Contents stay unverified by design: the key lives outside the machine (ESSENTIALS_RESTORE.md:9-10).
- Receipt claims re-verified live today: arxiv.org/abs/2606.26479 title, Narisetty et al., 2026-06-25, and all four quoted sentences match BURN_doctrine-owed-chase_20260926_b.md:11; sefaria.org/api/texts/Kol_HaTor.4 returns exactly "Kol HaTor ends at Chapter 3." as claimed at BURN_doctrine-owed-chase_20260926_b.md:9; inference-docs.cerebras.ai/support/rate-limits card-gate sentence and Free Trial table (5 / 30K / 90K / 1M / 1M on exactly gpt-oss-120b and qwen-3.8-27b) match BURN_free-resource-landscape_20260926_e.md:7. All three receipts land as memory/burns/LEDGER.jsonl lines 69, 70, 71 (ts 2026-09-26T12:14:31Z, exact landing filenames).

## Work done

Registered all five via scripts/index_fold_host.mjs add (INDEX_WRITER=b2-146-unregistered-files-20260926, seqs 1789823567015749390 to 394, INDEX.json refolded, 974 active items): EVENTS.jsonl class DATA, vault pack class artifact, three BURN receipts class RECEIPT. Every purpose line grounded in bytes read this lane; nothing synthesized. All five verify sha256_match=True in mag.shared_surface validate; remaining errors are other items' pre-existing drift (REJECTION_TAXONOMY_20260917.md, BURN_JUDGE_LANE_BUILD_20260925.md, phone_relay_log.jsonl, LINKS.jsonl, QUEUE.md); index_events.jsonl itself reads unindexed by the validator, a pre-existing condition. Because this lane's QUEUE.md edit staled QUEUE.md's own registration, applied the established hash-refresh pattern (precedent: event 3056): re-registered QUEUE.md at seq 1789823567015749397. LEDGER row appended (slug unregistered-files, ts 2026-09-26T13:18:21Z, ledger then 98 rows). Self-feed: B2-160 (C8 check overdue: ledger 92 rows at count vs pinned row 85) and B2-161 (EVENTS.jsonl drift policy: frozen projection vs refresh owner).

## Falsifier

Any of the five paths showing a pre-existing register event dated before 2026-09-26, or a shared_surface sha256_match=False on them, or the two retired meta-files reappearing as active items, falsifies this receipt. The EVENTS.jsonl projection claim breaks if any row diverges from its LINKS.jsonl origin line.

## Bibliography

- watch/inbox/index_events.jsonl (3,065 rows folded; lines 4, 94-96, 927, 1379, 1381, 3021, 3056 read in place)
- watch/inbox/EVENTS.jsonl (full read, 51 rows); watch/inbox/LINKS.jsonl (lines 275, 331 spot-checked, full per-row programmatic compare)
- watch/inbox/ESSENTIALS_RESTORE.md; memory/trajectory/steps.jsonl line 22168; configs/secrets/pack_key.txt (existence only)
- watch/inbox/BURN_doctrine-owed-chase_20260926_b.md; BURN_free-resource-landscape_20260926_e.md; BURN_judge-lane-spec_20260926_e.md (full reads)
- memory/burns/LEDGER.jsonl (92 rows at count, 98 after append; lines 69-71 read)
- Fetched 2026-09-26: arxiv.org/abs/2606.26479; sefaria.org/api/texts/Kol_HaTor.4; inference-docs.cerebras.ai/support/rate-limits
- Tooling: scripts/index_fold_host.mjs; probe watch/inbox/burn_wave_20260926/B2_146_regcheck.py; append watch/inbox/burn_wave_20260926/B2_146_append.py
