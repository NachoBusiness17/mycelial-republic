# RUN CLOSEOUT REGISTER: start-plan and provider casualties, dispositioned

- Operator order 2026-10-07: "Gather anything that timed out on the start
  plan and close it out."
- Instrument: this register (the SUPERSEDED.md pattern for runs - no run is
  deleted; each terminal-but-undispositioned stopped/errored run gets one
  row with its best-evidence disposition). Superseded chains are closed by
  definition and listed only as family counts.
- Census moment: 2026-10-07T02:20Z, 50+ runs swept, statuses
  stopped/errored/pending.

## Class 1: the start-plan quota wall (2026-10-06 23:06Z, code 1005)

Three runs died on the start-plan quota wall this sitting. ALL THREE were
re-seated to account:zai-individual-coding-plan and their successors are
live or complete - nothing owed:

- dwfrun-5de02c51 (100M dogfood burn, 81.1M tok) -> superseded by
  dwfrun-8cd5a845 (running, 112.6M tok total at last check). CLOSED.
- dwfrun-c948c345 (Stockfish ractor, 4.9M tok) -> superseded by
  dwfrun-42896305 (running). CLOSED.
- dwfrun-c21d18c2 (da Vinci lens ractor, 0 tok) -> superseded by
  dwfrun-d96545c9 (running, re-seated pre-emptively before its first ask).
  CLOSED.

## Class 2: provider-stopped, never superseded (8 runs)

| run | label | tok | disposition |
|---|---|---|---|
| bf3b90d0 | Build-it-all | 31.5M | LANDED-ELSEWHERE: the 10-03 BUILD-IT-ALL commit af9aa05f6 (arena/DD test waves, +50 collected per the AGENTS.md census lineage) is this run's work; the run stopped after landing. |
| 0dd7a6c5 | Ractor-50-wave-retro | 37.7M | LANDED-ELSEWHERE: the ractor50 receipt family (watch/inbox/ractor50/: accuracy.md, communication.md, MCP_PARITY_R20_20261001.md) carries the retro's findings; accuracy.md incident 5 is cited by the citation-lint gate. |
| 618ca877 | OLM mine daily 0930 | 131.0M | LANDED-PARTIAL then superseded-by-cadence: watch/inbox/frontier_olm_2026-09-30/ exists (the bank folder); the daily mine recovered on later dates (dwfrun-daecd119 164.5M completed 10-05; dwfrun-4c984c88 196.9M completed 10-06). |
| a5abb24e | OLM mine daily 0930 | 115.6M | same disposition as 618ca877 (its earlier half; the pair is one daily job that provider-stopped twice). |
| 38c4a19f | Flash 50 fullsend | 21.3M | SUPERSEDED-BY-MEASUREMENT: interrupted 09-28; the 10-03 flash-50wide probe re-ran the question clean (receipt watch/inbox/envelope_50w_20261003.md, 50/50 clean, zero 429/1302) and its numbers are the ones the AGENTS.md width law carries. |
| ab6970fe | Grok-estate-audit | 0 | VOID (died at dispatch, nothing banked); the question was answered by the sibling's Grokbot estate audit (10-03, ractor_engine/2026-10-03-grokbot-estate/SYNTHESIS.md). |
| e3d51dd6 | Gap-analysis-amend | 0 | VOID (died at dispatch); the gap-analysis instrument ran to completion separately (the 75-row register, 10-01, and the 10-03 receipt). |
| c13997d8 | Ractor-fleet-meta | 0 | VOID (died at dispatch); the fleet-meta question was answered by ouroboros R1 (dwfrun-270df86a, complete, the fleet synthesis). |

## Class 3: errored, never superseded (13 runs)

| run | label | tok | disposition |
|---|---|---|---|
| fde62465 | Ractor judgment panel (8 cards, 2-4-8-16 ladder) | 136.3M | PARTIAL-TAIL-LOST: no judgment fold in corpus/steal; the arena program's design work continued and landed as ARENA_V2_DESIGN (watch/inbox/ARENA_V2_DESIGN_20261004.md) + the arena day-one/three chain. Partial lane archives, if any, under memory/runs/mickey17_v2/runs/. Marked: needs no rescue - the program moved past its question. |
| aa9969b0 | Frontier OLM mine 0929 | 120.1M | LANDED-PARTIAL: the olm-mine saved workflow's own provenance line cites the 2026-09-29 run (32/32 miners, 21/24 confirmed) - the fold landed before the resume's tail errored; no frontier_olm_2026-09-29 folder found (folder-name drift), digest lineage lives in the workflow provenance + LINKS rows. |
| 279d66b4 | Frontier OLM mine 0929 (first half) | 36.3M | same job as aa9969b0; covered by that row. |
| ef372bc6 | Game dig: co-op social | 67.7M | LANDED-ELSEWHERE: the 09-27 game-dig wave closed ALL FILED (zknot 09-27 close: 5 veins); the vein's verdicts fed the wheel spec. |
| 038cd25b | Game dig: roguelike runs | 62.4M | LANDED-ELSEWHERE: same 09-27 ALL FILED wave. |
| 2663df44 | Salon-mine-20deep | 25.1M | LANDED-ELSEWHERE: the salon vault was fully mined 20/20 (10-02, laws minted incl V4-Never-Ran, ghost-citation-gate; receipts salon_mine_*). |
| ca497ba4 | Ractor-dogfood-gaps | 28.5M | LANDED-ELSEWHERE: the ractor-dogfood fed the 10-02 blind-audit verdicts (4 classes HALF THEATER banked, watch/inbox/ractor_engine/2026-10-03-surface-migration lineage). |
| 9bafb3d8 | Gap analysis: arena day one | 0 | VOID (errored at birth); the arena day-one gap analysis ran later to completion (75 rows, ACCEPT). |
| 260efe85 | Wide dig: the Grok bot ecosystem | 0 | VOID (errored at birth); covered by the 10-03 Grokbot wide dig (8/8 lanes ACCEPT, memory banked). |
| 6176a7ae | Fill-ball-amend | 0 | VOID (errored at birth); fill-ball ran 7/7 the same day (10-01). |
| dbb3f798 | Salon-vault-offpeak | 0 | VOID (errored at birth); offpeak subagents were measured DEAD for workflow work (10-02 memory) - this run was that measurement. |
| 619d47ec | Salon-mine-offpeak | 0 | VOID (same offpeak measurement class). |
| f4a8ddd6 | Burn 48 wide | 0 | VOID (errored at birth). |

## Family counts (superseded chains, closed by definition)

Game-dig supersede chains (7 generations across 5 veins), salon chain
(7128afa9 -> 1cd89983 -> 2663df44), read-estate (f008cecb -> a6bacf9c
complete), librarian (c48601ef -> 5b23d7bb), ball-20260929-dance2
(a924022d -> 23cefaa7), hitler-dig (09772510 -> 45c9dc32): 26 terminal
superseded runs. No action - the successor carries the work.

## The rule this register mints

A stopped/errored run with spent tokens gets ONE disposition row citing
where its work landed - or it stays an open wound the fleet re-reads
forever. Zero-token dispatch deaths are VOID, not failures: they are the
account's admission ticket, not lost work. Closeout cadence: this register
re-runs weekly beside the gap analysis, or after any provider event.

## Live at census close (healthy, funded account)

overnight-mesh (6a821d9c, 6 lanes executing, last progress seconds ago),
100M burn resume (8cd5a845, 112.6M), stockfish ractor (42896305), davinci
lens ractor (d96545c9). The start-plan main session recovered (daily reset)
and this seat answered on it - the subagent seats stay on the funded plan
until the operator re-points.

## Addendum 2026-10-07: dwfrun-d96545c9 disposition (lane m7-phantom-erratum, run morning-block-20261007)

The Class 1 row above still shows fire 2 running ("dwfrun-d96545c9 (running,
re-seated pre-emptively before its first ask)", :23) and the census-close list
above carries it live; both are stale. Disposition row, per the register's own
rule and the cure the lineage lens prescribed
(watch/inbox/ractor_engine/2026-10-07-davinci-lens/break-lineage.md:180-189, A2):

- dwfrun-d96545c9 (da Vinci lens ractor, fire 2, journal
  dwfrun-d96545c9-d216-4295-b3d5-d7496dceb3fe.mjs, born 2026-10-06 19:38:00,
  script mtime never moved past birth on this lane's stat): terminal. The
  coordinator-side closeout ask reports it completed; this lane could not
  re-read the harness run status itself (workflow introspection unreachable
  from the seat), so the terminal finding rides the estate's byte evidence:
  the journal carries the engine but no slug and no topic key,
  byte-consistent with an args-less refire
  (watch/inbox/ractor_engine/2026-10-07-davinci-lens/communication.md:88-92),
  i.e. an args-loss kill
  (watch/inbox/ractor_engine/2026-10-07-davinci-lens/break-lineage.md:145-154,
  BS4). It banked ~25 receipt files but no signal
  (watch/inbox/ractor_engine/2026-10-07-davinci-lens/communication.md:88-92).
  Its topic's work landed via the re-fired successor dwfrun-176a6b3b (born
  23:28:58, args intact), which folded as commit a4a34e900, DA VINCI LENS
  RACTOR FOLDED, 2026-10-07 02:05:38 -0400, receipts at
  watch/inbox/ractor_engine/2026-10-07-davinci-lens/. Disposition:
  args-loss kill, superseded by dwfrun-176a6b3b, work landed. CLOSED.
