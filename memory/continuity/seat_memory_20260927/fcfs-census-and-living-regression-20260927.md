---
name: fcfs-census-and-living-regression-20260927
description: 9/27 FCFS census numbers (97 debt / 27 frontier / 274 neutral by
  filename), living-regression confirmed live (drift-patrol reverted living
  migrations), cost truth accepted unpriced as honest unknown
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

9/27 late-burn findings from the width-24 experiment batch.

**FCFS census (byte-backed):** 398 receipts landed; by filename 97 debt-class (24%), 27 frontier-class (7%), 274 neutral (69%). Structural fact confirmed: dispatch is FCFS by brief number, zero value ranking. Queue composition is a choice, not a property of the machine. The neutral majority includes real builds (FTS5 wiring, drift board, catalog rebuild) that filenames can't classify — the shallow census can't settle usefulness, only count it.

**Living regression confirmed live:** drift-patrol-cron's plain whole-file refreshes reverted B2-156's living migrations on LINKS.jsonl, phone_relay_log.jsonl, and QUEUE.md. Caught by the B2-329 pin test going red within a minute. Fixed by B2-254 re-pinning at unanimous-max seqs and patching the patrol prompt (sqlite update via B2_254_update_prompt.py). The patrol prompt lives only in the tasks-index sqlite — a harness DB rebuild reverts it (filed as B2-222).

**Cost truth repricing decision:** accepted "unpriced" as the honest unknown rather than restoring free rates or building a frozen table. 265 rows re-labeled (165 cerebras + 100 nvidia provider-exact). Option A (free rates) rejected because it would label stray post-dormancy calls as free-credits, violating "pricing a dead lane $0 is a cost lie." Historical dollars unchanged in all four windows (today 0.51, 7d 7.16, 30d 21.70, all-time 286.46) — the gate moved labels only, never dollars.

**W40 stamp verification:** aging guard verified on W40 rows — all carry referent_age_days + verdict_guard; no W40 row is ALIGNED with age < 7. T6 recovery pre-registered for W43 (flood contamination until Oct 17).

**Ask 3 source repair:** Grok packet's FlashREINFORCE/GPO/RPG/BPO sources mirrored into LINKS through the sanctioned door; packet amended to name on-disk rows and declare memory/live_from_grok.md "never a source." FlashREINFORCE arxiv id still 0 results (x-drop remains the only pointer).

**Seed-MCP cold-join falsifier survived:** cold client 10/10 pass over real stdio, strict schema consumer, negative arms held (flipped content refused, mutated source refused, void paths refused).
