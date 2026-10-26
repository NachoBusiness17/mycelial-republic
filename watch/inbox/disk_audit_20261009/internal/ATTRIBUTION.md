# ATTRIBUTION - who wrote the 309GiB exec forest

Lane F, disk-storm audit 2026-10-09. Method: every dwfrun run-id was matched to
its compiled run script payload (`.zcode/workflow-runs/dwfrun-<id>.mjs`, whose
`args` field carries the burn slug/topic), then cross-checked against git log
commit messages and watch/inbox receipt dirs. No mapping below is inferred from
timing alone. GiB per run = sum of its actor session dirs from
watch/inbox/disk_audit_20261009/evidence_pack/exec_forensics.json top_sess+largest.

## Mapped burns

| run-id | name + date + goal (one line) | GiB | receipt path (evidence) |
|---|---|---|---|
| 27c7e7b2 | SPORE-SHARING ractor, 10-05: does sharing the estate seed (GENOME.md, STANDING_RAILS) across seats degrade it | 34.86 | watch/inbox/ractor_engine/2026-10-05-spore-sharing/SYNTHESIS.md; .zcode/workflow-runs/dwfrun-27c7e7b2*.mjs args |
| 0da272a1 | EXTERNAL-STEAL ractor, 10-07: mine the estate's own named gaps/asks from the last 48h | 24.80 | watch/inbox/ractor_engine/2026-10-07-external-steal/; payload args slug |
| ab8d406e | OLM MINE day-4, 10-04: 32-miner daily arXiv/reddit steal sweep | 23.62 | watch/inbox/frontier_olm_2026-10-04/RECEIPT.md; git 17225e37e |
| a5abb24e | OLM MINE daily, 09-30 | 12.52 | watch/inbox/frontier_olm_2026-09-30/ (DIGEST.md, sweep/) |
| aa9969b0 | OLM MINE day-1, 09-28 (logs closed 09-29) | 11.62 | watch/inbox/frontier_olm_20260928/RECEIPT.md |
| c1ff3563 + 45927560 | OUROBOROS R4 MEMORY ractor, 10-05: ractor the memory/boot surface (two fires, same slug) | 10.99 | watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/; ouroboros_20261005/ |
| cda8c867 | SALON VAULT STRAGGLERS gala rung, 10-02: mine leftover salon lanes (compuiter.txt etc) | 10.73 | watch/inbox/gala_20260925/salon-vault-stragglers_RECEIPT.md |
| 8242d424 | 50-WIDE KIT DOGFOOD, 10-04: dogfood the starter kit end to end (44 dig lanes + 6-seat spine) | 9.89 | git c7b3433a0; payload header comment |
| ed1dbbae | WORKFLOW-DOGFOOD ractor, 10-02: ractor the 12 saved workflows themselves | 9.41 | watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/SYNTHESIS.md |
| 0f281809 | OLM MINE day-8, 10-08: daily steal sweep | 8.79 | watch/inbox/frontier_olm_2026-10-08/ |
| 3cec1e3a + 1759540b | OLM MINE daily 10-03, first fire + retry (drafts OLM-mine-daily-burn-1003*.dwf.ts) | 8.59 | watch/inbox/frontier_olm_2026-10-03/ |
| 39f4a297 | TRACK5 REWRITE GAUNTLET ractor, 10-07: each ractor cuts a version of Track 5 | 8.46 | watch/inbox/ractor_engine/2026-10-07-track5-rewrite/ |
| 8739ac44 | BURN-RESET flash50 S2 seat, 09-28/29: rib_bus map, improve loop, roblox Luau census, docs/ref audit | 6.98 | watch/inbox/burn_reset_20260927/flash50/ (s2-* lanes) |
| a6bacf9c | READ-THE-ESTATE 100M, 10-04: 12 lanes over estate history, ESTATE_INDEX anatomy | 6.78 | git eb687f76a (MASTER_READ_ESTATE.md) |
| 3b5af1ac | ELEVEN DOORS ractor, 10-04: the 24-wide dig's 11 remaining build doors | 6.46 | watch/inbox/ractor_engine/2026-10-04-eleven-doors/ |
| 53ba7956 | GAP ANALYSIS evening, 10-02: 48h receipt gap sweep (mickey17 shape) | 6.25 | .zcode/workflow-drafts/Gap-analysis-evening.dwf.ts; gap-analysis commits per AGENTS.md |
| c13997d8 | FLEET-META ractor, 10-02/03: the standing fleet itself, 12 saved workflows + routing chain. CAVEAT: no dedicated receipt dir watch/inbox/ractor_engine/2026-10-02-fleet-meta/ - its name appears only inside the sibling workflow-dogfood receipts | 5.95 | payload args slug; ractor_engine/2026-10-02-workflow-dogfood/ (co-mingled) |
| af998d42 | SURFACE-MIGRATION ractor, 10-03: should the estate leave interactive ZCode sessions | 5.78 | watch/inbox/ractor_engine/2026-10-03-surface-migration/ |
| bc564831 | OLM MINE daily, 10-02 | 5.36 | watch/inbox/frontier_olm_2026-10-02/RECEIPT.md |
| cb8c3888 | OLM MINE day-7, 10-07: sharpest self-audit (contamination law, Merkle cure input) | 4.36 | watch/inbox/frontier_olm_2026-10-07/; git c7d364ab6 |
| 4130d690 | PHEROMONE SWARM, 10-07: execute burn - Merkle trust substrate verify + position-bound leaf cure | 4.31 | git 633b884ad; memory/runs/mickey17_v2/runs/pheromone-swarm-20261007; watch/inbox/MERKLE_COLLISION_PROOF_20261007.md |
| 1bb4125e | STUPIDMODEL COMICS ractor, 10-07: operator order to use a really stupid model | 4.20 | watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/ |
| d96545c9 | default-slug ractor fire, 10-06/07 (no args passed; disposition noted in morning block) | 3.88 | watch/inbox/ractor_engine/ractor-topic/ (SYNTHESIS.md, accuracy.md); corpus/steal/MASTER_MORNING_BLOCK_20261007.md |
| 95444cf9 | BURN-RESET flash50 W4 seat, 09-28/29: mycelial-orchestration deep research (w4-* lanes) | 3.59 | watch/inbox/burn_reset_20260927/flash50/; memory/runs/mickey17_v2/runs/gauntlet_w4 |
| cbbde00f | OUROBOROS R2 GAPS ractor, 10-05 | 3.50 | watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/ |
| 92c13b6e | BURN-RESET flash50 FIREHOSE seat, 09-28: nacho archaeology, skills/configs audit, arXiv corpus sweep (f-* lanes) | 3.34 | watch/inbox/burn_reset_20260927/flash50/ |
| 125a2278 | mickey17_v2 fire with no topic arg (default run name), 10-03 evening | 2.98 | memory/runs/mickey17_v2/runs/run-0 (mtime 2026-10-03 21:05 EDT) |
| c2fc5a4d | GROKBOT ESTATE gala rung, 10-03 (grokbot-primary-deepread lanes) | 2.95 | watch/inbox/ractor_engine/2026-10-03-grokbot-estate/ |
| b488a2bb | DOGFOOD-48H ractor, 10-02 | 2.58 | watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md |
| 22ad421a | OLM MINE daily, 10-01 | 2.29 | watch/inbox/frontier_olm_2026-10-01/ |

Mapped total: 255.86 GiB = 82.8 pct of the 309.12 GiB forest (30 burn identities).
Single worst offender: 27c7e7b2, the SPORE-SHARING ractor of 10-05, 34.86 GiB
(four actor sessions, two of which hold the #1 and #2 giant junk files).

## Unmapped

None among the top-40 sessions: every run-id resolved to a compiled run script
in .zcode/workflow-runs/ and 28 of 30 to a named burn with a receipt. Two weak
links, still mapped but flagged: 125a2278 (generic default-topic fire - identity
certain from payload, burn has no operator name) and c13997d8 (fleet-meta, whose
dedicated receipt dir is absent - see caveat in table). Residual 53.3 GiB
(17.2 pct) is the long tail of sub-3.4GiB actor sessions and shell snapshots
below the top-40 cutoff, not itemized here.

## Junk-file share

- Top-8 giant files: 64.16 GiB = 20.8 pct of the forest (68,894,384,405 of
  331,914,796,997 bytes). The remaining 11,071 files carry 244.96 GiB.
- Junk verified by content, not label (heads read 2026-10-09):
  - 0da272a1 call_91ae...stdout.log (12.42GiB) and 27c7e7b2 call_0074...stdout.log
    (10.46GiB): identical full-disk `find` dumps walking /c from the root,
    $Recycle.Bin permission-denied spam repeated - the same runaway command
    rerun in two different actor sessions.
  - a5abb24e call_c8ccd...stdout.log (8.32GiB): runaway FINDSTR error loop with
    mangled paths (backslashes eaten - "C:Usersfoste...", "c:lmcache") - a
    quoting bug looping forever.
  - The 5.76GiB twins (bc564831 actor_3_31 and cda8c867 actor_8_1, same byte
    count 5758962xxx family) and the 4.72GiB pair on 0f281809 actor_3_26 are the
    same duplicated-dump shape.
- Conclusion: one command class (unbounded stdout capture of full-filesystem
  walks / errored search loops) explains ~21 pct of the forest in just 8 files;
  the rest is normal per-call logs at KB-to-MB scale.

## Durable-work independence check

Verdict: YES - the exec logs are pure exhaust; nothing durable lives only there.

Evidence (3 burns sampled deeper than name-matching):
1. ab8d406e (OLM day-4): watch/inbox/frontier_olm_2026-10-04/ holds RECEIPT.md,
   DIGEST.md, lens/, sweep/, steal/ in-repo, plus git commit 17225e37e. The
   23.62GiB of exec logs added zero unique durable bytes.
2. 27c7e7b2 (spore-sharing): watch/inbox/ractor_engine/2026-10-05-spore-sharing/
   holds SYNTHESIS.md + lens reports, landed in the repo, separate tree from
   C:\Users\foste\.zcode\cli\exec.
3. ed1dbbae (workflow-dogfood): watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/
   SYNTHESIS.md landed; corroborated by watch/inbox/ractor_engine receipt web.
4. aa9969b0 (OLM 09-28): watch/inbox/frontier_olm_20260928/RECEIPT.md on disk.

The forest lives under the user profile (C:\Users\foste\.zcode\cli\exec), the
receipts under the repo's watch/inbox - physically separate trees; deleting the
exec forest loses no receipt, no synthesis, no register. The one asymmetry worth
an operator eye: c13997d8's fleet-meta burn has exec exhaust (5.95GiB) but no
dedicated receipt dir - its conclusions, if any, rode the sibling
workflow-dogfood files.
