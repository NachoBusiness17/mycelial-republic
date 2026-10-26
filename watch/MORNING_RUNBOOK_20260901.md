# MORNING RUNBOOK — 2026-09-01 (written 05:20Z, operator asleep)

## Night chain (auto-runs, no action needed)
1. STATUS 07:00Z: MXFP4 SHA-PASSED 05:25Z (custody verified). DS part 1 PASS. Part 2 hit HF/Xet 416-on-open-ended-range stall (041-200 attempts wasted); downloader patched to v3 (explicit-end + 416-probe/backoff), chain_resume.sh relaunched 07:02Z — part 2 confirmed growing.
2. Remaining: DS parts 2-5 (~140GiB) then GLM-5.3-Flash UD-Q4_K_XL 6 parts + mmproj (186GiB) — ETA ~12:30Z combined.
3. All artifacts sha-gated vs upstream oids in `glm_parts.txt`/`ds_parts.txt`; receipts append to `chain.log`
4. **Self-healing active:** `chain_watchdog` cron (id 6259dd35, every 20min, isolated DS-Flash) beats per `/board/chain_watchdog_SOP.md` (updated: relaunch = chain_resume.sh via setsid) — removes itself when CHAIN_COMPLETE.
5. **Verification on wake:** `tail -30 /root/.openclaw/workspace-worker/staging/chain.log` — expect MXFP4_SHA_PASS, DS_PART_PASS x5, PART_PASS x6 (GLM); any *_FAIL line = two-strike law applies, do NOT retry blind
6. Disk check after: `df -h /` — expect ~460GB free (620GB filled tonight)

## Operator decision queue (morning coffee, in order)
1. **RAM math correction (05:26Z):** 128GB DDR4 ≈ $600, not $150 — I lowballed from
   mixed-era pricing; my error, receipted. Feasibility table unchanged; the $600
   question is: local GLM-5.3-Flash at 2-6 t/s CPU vs ~$0.25/call API lane vs
   GPU path (FreeToken, still needs hardware check). Custody needs NO ram; serving
   economics need the spreadsheet before any buy. No RAM purchase recommended yet.
2. **steer_bus SPEC v0.1 -> /patches:** designed (closed-enum, quorum-2, target
   consent, governor-sole-executor), needs a JSON patch for mag host. Say the word.
3. **Procurement threshold note:** at $600/RAM the vault ladder re-ranks: drive
   (Phase 3, ~$600 for 20TB) and RAM are now equal-cost levers with different payoffs
   (archive vs serving). Recommendation lands after GPU check (RUNG 0.5, still pending).
4. **rnd_advisor_steering** first scheduled pass 10:15Z (already mid-run once tonight)
5. **procurement_hunter** next run 17:19Z (delivery bug fixed 04:48Z)

## Parked (unchanged)
- FreeToken install: gated on host GPU/VRAM check (operator-side, RUNG 0.5)
- steer s-001-ea54 (BABYSTEPS) still UNREAD — steer-edit affordance open question
- Phase 5 GLM lineage mapping: datasets banked per checkpoint; starts after custody verifies
- abliterated quarantine siblings (Huihui DS-V4-Flash MIT etc.): after Tier A close

## Estate state at 05:20Z
- 103 links stacked, 26/26 INDEX sha-verified, steer-001 closed 12/12 receipts
- Tonight's receipts: glm53flash_quant_menu (05:09Z), chain restart (04:41Z), procurement fix (04:48Z)
- Session lane: zai-2/glm-5.3-flash coding plan, $0.0000 billed
