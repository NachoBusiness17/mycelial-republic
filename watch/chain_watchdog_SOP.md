# CHAIN WATCHDOG SOP — night custody self-healing (2026-09-01 05:2xZ)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a cron watchdog detects the stalled vault download via 45s file-size growth and self-heals it with idempotent chain_resume.sh relaunches — UNPROVEN (procedure stated; chain completion receipt not in card) · falsifier: chain.log never reaches DONE + GLM_STAGE_DONE after relaunches, or two downloaders ever run concurrently

Purpose: the vault download chain runs nohup'd and dies if the OpenClaw gateway
restarts (proven 04:00Z). This watchdog is its clock until the chain completes.

State (read first):
- `chain.log` at `/root/.openclaw/workspace-worker/staging/chain.log`
- Complete when chain.log contains BOTH `DONE` (main: DS parts) AND
  `GLM_STAGE_DONE` (GLM-5.3-Flash custody). (MXFP4 sha-PASSED 05:25Z — no longer gated.)

Decision tree:
1. If chain.log has `DONE` AND `GLM_STAGE_DONE`: append
   `[watchdog] CHAIN_COMPLETE <utc>` to chain.log, then REMOVE this cron job
   (cron tool, action=remove, own jobId). Stop.
2. Else: check liveness WITHOUT downloading anything: `stat -c %s` on
   `vault_warm/ggml-org/gpt-oss-120b-MXFP4.gguf` and
   `vault_cold/DSV4F/*.gguf` and `vault_cold/GLM53F/*.gguf` (whichever exist),
   sleep ~45s, stat again. If ANY size grew: chain alive → append one line
   `[watchdog] alive <bytes snapshot>` to chain.log and stop. Do nothing else.
3. If NOTHING grew in 45s AND stages are incomplete:
   relaunch with `cd /root/.openclaw/workspace-worker/staging && setsid nohup ./chain_resume.sh > /dev/null 2>&1 < /dev/null &`
   (chain_resume.sh = DS 2-5 + GLM custody in one script, idempotent: dl.mjs v3 auto-detects complete parts via 416-probe; setsid detaches so the relaunch survives this beat's session end — plain nohup died with the 06:09Z beat).
   Then append `[watchdog] relaunched chain_resume <utc>`.
4. NEVER run two downloaders at once: if both chain.sh and chain_glm.sh could
   be running, check `chain.log` last-line logic above decides which stage is
   current; only relaunch the CURRENT incomplete stage, never both.
5. Never delete partial files. Never bypass sha gates. Two-strike law: if a
   relaunch makes no progress by next beat, log `[watchdog] strike` and leave
   it for morning — do NOT loop retries within one beat.

Laws: board is the receipt surface; conservation (this job = tiny reads, no
web, no spawns); append-only chain.log.
