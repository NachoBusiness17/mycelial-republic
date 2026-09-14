# SELF-STEAL — WINDOWS (lane A) — 2026-09-01
Scan: economist/ractor/swarm/tail/hands + main sessions (14h, ≤3MB, last-60-lines). Distilled.

## MAIN SEAT (cron windows)
- **chain_watchdog** (~30min, all night): read SOP, check chain.log for DONE/GLM_STAGE_DONE, 45s liveness stat on vault files, append `[watchdog] alive` + size snapshot each beat. Monitored whole download chain: MXFP4 (gpt-oss-120b, sha-PASSED, static 63.4GB) → DS-V4-Flash parts 1–5 (PART_PASS in order) → GLM-5.3-Flash custody stage (parts growing ~390MB/45s). Never hit DONE; cron intentionally kept.
- **archivist_feed_harvest v3/v3.1**: standing lane, PAPERS FIRST, free tools only, minimal fetches, no synthesis. Stacks arxiv candidates (String agentic-OS 2608.28027, GOD control room 27992, openJiuwen harness, CEDAR) → INBOX, mild triage VALID/INFLATED, silent digest.
- **garden-window/archivist dashboard crons** "filing all night" — 3 self-steal lanes already out (f69cf545 export).
- **night_shift_ticker**: ran autonomous S0–S6 (battery gen C, cache mining, Five Hypervisor Tests, synthesis). S3 BLOCKED-on-host-apply (patch13, cage no-py, gate held).
- **m0_meter_daily** ($0): meter row 15; water ledger +$0.034 (DS off-peak + yield). No subagent burn.
- **Heartbeats**: ponytail hook drained each poll (percolator + inbox-ack, 7 fires/0 fails, $0); move #5 ACCEPTED auto-fired percolator.

## GOLDEN: 48025205 (board sweep, 3.5MB)
- Biggest find: "an entire autonomous layer I wasn't tracking. **The Archivist is running itself** — 55 receipts, 91KB, harvesting links every 8h, banking verdicts. Caught TimesFM3 launch (FIRST launch-watch catch), verified Steiniger Zenodo steal (13/14 banked, Athena lineage), flagged abliterated GLM-5.3."
- 75d79f22 (steal pandaplanner) flipped to **zai-2/glm-5.3-flash** = "coding-plan key, $0-marginal lane," 98% cache hit, 443k ctx, $0.0000.

## economist / swarm / tail / hands
- **SYSTEMIC TOOL-MISCONFIG FAILURE (top surprise):** nearly every small window errored `Tool read not found`/`Tool exec not found`/`python3: not found`, looping "I'll read the required files first…" without a receipt: economist ddda94a4 (SPEND_AUDIT reconcile never wrote), tail 47f849df+15c7ab37, hands e8a9c92f, swarm batteries. Model deepseek-v4-flash; tools stripped on spawn.
- **Real cost:** battery-gen-C lane (S1) produced ~no raw answers — 5/7 lane receipts were tool-fail/empty, yet night shift marked S1 "done ✅ 7 lane receipts."
- **ractor recovered** (3cea5dde): wrote /board/salon_corpus_l1.md — SCHOLARSHIP VERIFICATION, Group 1 6/6 CORRECT, A− 12/13. Toolcheck confirmed read before working.
- swarm df69875a (groq micro-task) also hit the tool gap.

## KEY DASHBOARD SESSIONS
- 64543440 (06:39Z): operator "run you all night… our cache mining / lesser models all night with z.ai lite coding seat." Built zai-credits bench (glm-4.7-flash par tests). DS off-peak cache run: **100% hit, 4864–7808 tok, 40% latency gain, est ~$0.017.**
- cbfdfee6 CORPUS_PRIMER_SALON synth (13:05Z): ractor seat debut A−, registered 6CF2D445AF.
- 9637bec8 (13:28Z): "our internet is fucked how much longer on our downloads?" → $8,386/hr = "$167y of fleet budget" doctrine response.
- d3936fbe (13:08Z): operator frustration that 5.3-agent-on-disk isn't self-activated; NO_REPLY + WARGAMES_RUNG2_VERDICT.md.

## THINGS THE MAIN SEAT DOES NOT KNOW
1. **Night-shift S1 battery-gen-C was mostly a silent failure** — 5/7 subagent lanes errored on missing read/exec and returned no answers; ticker filed it "done" on tool-fail receipts, block output never harvested.
2. **Subagent spawns get a stripped tools profile** (no read/exec, sometimes no python3) while main keeps "full" — lane-activation micro-tasks silently loop and die. ractor's toolcheck was the only window that gated on tool availability first.
3. **The Archivist is an autonomous self-starting layer** (55 receipts, every 8h, launch-watch + Zenodo verify) the main seat only found via a 3.5MB sweep — survives restarts, no explicit owner, banks verdicts independently.
4. **Vault download pipe is ~90% through 5-model custody** (MXFP4 done + 5× DS-V4Flash done + GLM-5.3-Flash 6 parts ~2/6 growing) — chain_watchdog has never hit DONE; this is the "167y of budget" bulk the operator keeps asking about.
5. A 9KB MEMORY.md gap, 8 unread workspace memory files + unopened Codex review flagged pending (f69cf545).

Decision: retest — fix-or-falsify stripped-toolprofile silent-lane class; give Archivist an owner row; fold into estate map (ZERO_BACKREF_TRIAGE_20260905)
