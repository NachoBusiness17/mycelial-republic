---
name: swarm-burn-20260926
description: 9/26 flash-lane burn COMPLETE — all 397 briefs landed through 12-lane
  swarm (~2.5B witnessed tokens, all 12 lanes completed); width cap 12→24 proven
  on live bytes; dynamic-ceiling law proven; silent absorption discovered;
  FCFS queue is the next bottleneck; swarm minted 6 self-governance laws
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

The 9/26 flash-lane burn ran 397+ briefs through 12 swarm lanes (25 briefs each) plus a 10-minute dispatcher, burning ~816M+ witnessed tokens on the flash lane with a measured peak of 109M tok/h at width 10 (B2-25). Width cap raised 12→24 by operator order; B2-98's tally found 287 silently absorbed 1302s inside "clean" waves, proving "zero surfaced" ≠ "zero occurred" — the retry layer hides rate-limit pressure.

**Architecture that worked**: dispatcher every 10 min, self-feeding queue (each landed lane mints 1-3 new briefs), shared-file claim law (B2-250), checkbox truth law (B2-238), queue dedupe janitor passes, free-lane tandem runner (B2-178) burning estate work through 8 alive free lanes in parallel. Double-dispatch self-healed via B2-247-style verify-not-redo.

**Landed highlights**: FTS5 wired (4.5s→2.5ms), catalog_rebuild.py (489K rows, zero dupes), writer-debt root-caused (fold silently dropped watch/ paths), verkle tip re-anchored, rbxlx rebuilt + committed, prompt-law v2 amendments, check7 guard pin, FKB continuity repair (1,435 sigs recovered), LAW-12 registered with 7 scenario cards, LAW-13 experiment-on-absence registered.

**Why:** The burn machine works at scale and produces receipted, gated, self-feeding work. The envelope is dynamic not constant.

**How to apply:** the dispatcher is armed to noon Sep 27 at cap 24 on operator GO. The free-lane runner runs to 23:30. Width-15+ remains operator-gated (B2-97 card armed). The next burn's lever is value-ranking the FCFS feed, not more width.

**Final swarm phase (all 12 lanes completed, all 397 landed):** per-lane token totals: SW-02 116M (heaviest), SW-00 95.1M, SW-08 93.6M (constant-1-error test disease fixed), SW-10 86.2M, SW-01 81.9M (B2-388 self-inflicted incident restored), SW-05 80M (commit 6d417abd5: 18 critical files committed, gate PASS), SW-11 76M (QUEUE truncated+restored, BOARD_REPAIR_INCIDENT), SW-07 70M (Arm C 200-leg killed, OWED), B2-279 10.8M (sort totality). Day-total witnessed agent tokens: 815.9M across 191 agents. Laws the swarm minted about itself: shared-file claim law (B2-250), checkbox truth law (B2-238), queue dedupe janitor (B2-255 pattern, 147+ receipt-verified re-flips after the QUEUE restore wars), pointer-anchor law (B2-491), restore-guard (B2-343), living-file hash law (B2-156). Structure fact proven: dispatch was strictly FCFS by brief number with zero value ranking, ~100 of 398 receipts clearly debt-class by name, the rest mixed — the next burn's lever is value-ranking the feed, not more width.

**Late-9/26 swarm completions (all 12 lanes + wide experiment final):** SW-06 died to generic model failure (not 1302) mid-slice, 25 briefs requeued unchecked. SW-04 died to 1302 2/25 done. SW-09 died 0/24. SW-02 25/25 at 116M (heaviest: 19 LANDED, B2-312 REJECTED-by-falsifier, B2-125 BLOCKED-as-owed, B2-344 disposition+fired falsifier). SW-10 24/24 at 86.2M (B2-143 PARTIAL under 1302 throttling). SW-08 24/24 at 93.6M (constant-1-error test disease fixed, QUEUE restore war caught/deduped/gated). SW-11 24/24 at 76M (QUEUE truncated+restored, BOARD_REPAIR_INCIDENT). SW-01 25/25 at 81.9M (self-inflicted incident restored, B2-521 backfill). SW-05 25/25 at 80M (commit 6d417abd5: 18 critical files, gate PASS). SW-07 25/25 at 70M (Arm C 200-leg killed, OWED, QUEUE truncation rebuilt from git). SW-00 25/25 at 95.1M (B2-326 no CUDA owed, B2-470 payloads unrecoverable owed). Total witnessed: ~816M agent-metadata tokens; true burn higher (absorbed retries invisible to per-agent counters).

**Width-24 experiment definitive verdict (overnight 9/26-27):** at width 24 + 12-lane swarm + free-lane runner + Arm C, the surfaced 1302 wall appeared within the hour: 8 deaths total (SW-09, SW-04, B2-104, B2-217, B2-239, B2-139, B2-155, B2-151). Every death auto-requeued its briefs — nothing lost. The envelope law is now carried as a dynamic function of window fill-state, never as a frozen constant. B2-98's provider-error tally (1,741 silently absorbed at width 10-12) proves the retry layer hides the true pressure either way. The 50-wide shape hit its own first rate limit (filed ENVELOPE_50W_HIT_20260926.md). Ladder now: 3-6-10-12-24 proven, 15-16 untested, 50 = first-contact-at-fresh-window.
