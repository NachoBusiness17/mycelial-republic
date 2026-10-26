# GAP_REGISTER.md - the 09-30/10-01 burst, every gap in one ranked table

Written 2026-10-01 by lane a15-rollup of the gap-analysis burn
(memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/).
This file is the lane table for the NEXT 100M-token job: it tells that job
what to fire, in what order, at what cost, and who owns it.

## Provenance and coverage honesty

- Inputs: 8 sibling lane audits, read in full this session: a01-olm-day2,
  a02-olm-day1, a03-music, a04-vonnegut, a05-ractor50, a06-spiking,
  a07-localfirst, a08-48h-synth (lanes dir poll 2026-10-01 ~18:30Z).
- Lane slots a09-a14 produced NO files in the lanes dir at poll time. This
  register merges 8 siblings, not the full ask's set; if a09-a14 land later,
  they amend this register, they do not rewrite it.
- No prior gap register existed anywhere (grep GAP_REGISTER|gap_register over
  corpus/steal, memory/research_polished, watch/inbox/*.md = 0 hits, exit 1).
  This is the first. watch/inbox/gap_analysis_20261001/ did not exist and was
  created for this file.
- Five load-bearing sibling quotes were byte-checked with grep -cF before
  reuse (1 exact hit each); everything else in the table is adopted as
  lane-reported with the lane pointer as its citation.

## Ranking law

Rank = severity x fill-ease, cheapest-cure-first inside a severity band.

Severity:
- S1 CRITICAL: corrupts a record other seats will consume, breaks a live
  trust/safety gate, or a falsifier clock kills an asset within ~48h.
- S2 HIGH: a whole window or program's findings are uncitable/unreachable,
  or an enforcement gap repeats by construction.
- S3 MEDIUM: single stale label, missing pointer, undelivered one-line action.
- S4 LOW: bookkeeping and polish.

Fill cost:
- ONE-SITTING: one seat, one window, no approvals, no shared-host risk.
- ONE-WAVE: multi-step, needs a build+test cycle, a download, or another fill.
- OPERATOR: touches the shared janitor host, keys or mode flips, hardware
  placement, or spend. Only the operator can pull these.

## The four meta-gaps (the pattern behind the table)

1. MINED-NEVER-SCHEDULED (dominant class). Findings banked but on zero
   execution surfaces: a06's 3 synthesis moves, a05's 20-of-30 prose-only
   laws and 0-of-18 skill verdicts executed, a07's 3 unticketed top steals,
   a08's 0-of-5 autonomous fires, a02's percolator zero-ingestion, a01's 11
   owed-unowned probes. The burst dug brilliantly and scheduled almost
   nothing. The next 100M-token job is a schedule-and-fire pass.
2. CORPUS-FOLD NEVER RUN. corpus/steal and memory/research_polished received
   nothing from the music, localfirst, spiking, olm-day-1, ractor50-polished
   and 48h-owed programs (zero-hit greps in a03, a07, a06, a02-r9, a05, a08-r5;
   reproduced by this lane). Every wave's findings live only inside
   watch/inbox windows where the next seat will not grep.
3. PHANTOM-CITATION CLASS. Byte-failing numbers and unresolvable anchors are
   riding in consumed records: STORY.md:240's 191.8M (its named source has
   zero '191' hits, re-grepped by this lane), a01's phantom heal commit
   1a1efc67b and unbanked tweet id, a05's 213-vs-438-vs-167 census wound and
   2 anchor-drifted cites, a03's STORY.md-section-3 citation path drift,
   a06's mislabeled paper title and wrong-GPU line, a07's letta line pointer.
   The estate already owns census_drift_patrol for counts; the citation
   cousin (a05's citation_lint spec) has never been built.
4. GATES LIVE BUT UNARMED. steer_seal.py runs in warn-default with no keyfile
   and no mode sentinel (a07, ls of ~/.mag confirms), verify_seal.py is
   PAM-class by construction (hashes only, one trust domain), EstateWalkDaily
   failed with both alarm channels silent (a08), and SAELIS rides an
   unmeasured q8_0 KV default (a01). Enforcement exists; enforcement teeth
   were never installed.

## THE RANKED REGISTER

| rank | gap | lane | sev | fill cost | owner |
|---|---|---|---|---|---|
| 1 | EstateWalkDaily bake fired red (result 1, 10-01 09:15:15), END line AND attention alarm both silent; repeats 10-02 09:15 with the same relative-path defect | a08-r3 | S1 | one-sitting | any seat w/ Task Scheduler |
| 2 | elder-lens salvage lens unbanked while the card's own falsifier clock closes ~10-02 (queue/lanes/elder/inbox.jsonl = 0 bytes, mtime Sep 4, re-confirmed) >> FILLED 2026-10-02 by fillball-1001 before the clock closed: receipt watch/inbox/fillball/elder-salvage.md, inbox.jsonl now 2,024 B on disk (byte-checked 2026-10-04, queue-truth-a14) | a05-r3 | S1 | one-sitting | any seat |
| 3 | tools/citation_lint.py absent from the whole estate (re-confirmed); its spec is written and it closes meta-gap 3 at pre-push >> FILLED 2026-10-01 by fillball-1001: receipt watch/inbox/fillball/citation-lint.md, tools/citation_lint.py on disk 13,447 B (byte-checked 2026-10-04, queue-truth-a14) | a05-r2 | S1 | one-sitting | any builder seat |
| 4 | 191.8M-token headline in STORY.md:240 fails a byte check against its named source (re-confirmed: 0 '191' hits in frontier_olm_20260928/DIGEST.md) >> FILLED 2026-10-01 by fillball-1001: receipt watch/inbox/fillball/errata.md, the erratum itself at watch/inbox/48h_synth/ERRATA.md (on disk 5,983 B, byte-checked 2026-10-04, queue-truth-a14) | a08-r2 | S1 | one-sitting | any seat |
| 5 | steer_seal gate live UNARMED (~/.mag holds only steer_seal_seen/, re-confirmed) and no forge drill exists against the PAM-class verify_seal | a07-r1/r2/r4 | S1 | one-sitting + operator flip | seat + operator |
| 6 | Percolator zero-ingestion: no candidates row from 09-28 or 10-01 ever reached invariants.json; no --candidates flag exists (0 consumers in mag/tools/scripts, re-confirmed) >> FILLED 2026-10-02 by fillball-1001: receipt watch/inbox/fillball/percolator-candidates.md, --candidates flag live in mag/percolator.py:23 (byte-checked 2026-10-04, queue-truth-a14) | a02-r2 | S2 | one-sitting | any seat |
| 7 | Day-1 window uncitable: frontier_olm_2026-09-30 has no DIGEST/register/percolator (fold step missing, not misplaced; 6 cards + 32 sweeps on disk) >> FILLED 2026-10-02 by fillball-1001: receipt watch/inbox/fillball/day1-digest.md, DIGEST.md + register.jsonl + percolator_candidates.jsonl now on disk under watch/inbox/frontier_olm_2026-09-30/ (dir-listed 2026-10-04, queue-truth-a14) | a02-r1 | S2 | one-sitting | any seat |
| 8 | Day-2's own headline outputs unindexed: 13 files incl DIGEST/register/candidates/RECEIPT + 5th card are NOT-INDEXED; fold writes last, indexes never again | a02-r8 | S2 | one-sitting | any seat (sanctioned writer) |
| 9 | KVarN one-liner undelivered (0 hits in ARXIV_REGISTER.json, mtime Sep 29, re-confirmed) + theneurondaily fetch receipt owed (FETCHED AND CONFIRMED by a15, receipt below) | a01/a02-r7 | S3 | one-sitting | any seat |
| 10 | Day-1 unconfirmed trio dropped by day-2 dedupe: U2 r/LocalLLaMA 1sy7srk KV table (load-bearing for the KV ladder) and U3 arXiv 2609.21341 serving confound; zero mentions anywhere | a01-dedupe | S3 | one-sitting (2 archive fetches) | any seat |
| 11 | SS-1 seed-seal Ed25519 port, CP-1 depends_on cascade, R2-1 memory-on-MCP verbs: none ticketed anywhere (TICKET_LEDGER row zero covers other sources; estate_corpus_search = 0 in mag/tools, re-confirmed) | a07-r3 | S2 | one-sitting (3 named tickets) | any seat |
| 12 | Spiking synthesis MOVE 1 ($0 R0 Vulkan gate probe) scheduled nowhere; fire it and name the zero-mapped trio (Mamba-3, LFM2, Falcon-H1) as candidates | a06-r4/r5 | S2 | one-sitting ($0) | seat on the RX 5600 XT box |

## TOP 12 ONE-SITTING FILL SPECS

1. BAKE CHANNELS (a08-r3). Before 10-02 09:15: edit scripts/estate_walk_daily.ps1
   to absolute paths or Push-Location the repo root at the top; run it by hand;
   prove BOTH channels fire (log END line + attention.md alarm) on an injected
   failure; land the receipt beside watch/inbox/48h_synth/. Cost: minutes.
2. ELDER LENS SALVAGE (a05-r3). Bank one lens mined from
   watch/inbox/48h_synth/STORY.md into queue/lanes/elder/inbox.jsonl before
   ~10-02; the card resurrects by its own terms. Cost: a 20-minute write.
3. CITATION LINT (a05-r2). Build tools/citation_lint.py exactly to the
   accuracy.md spec (path exists + line range non-empty + claim-token match),
   wire one line into githooks/pre-push after the ratchet, run it once over
   ractor50's 12 spot-checked cites to prove it catches the 2 known drifts
   (mag/mcp_server.py:338-340, mag/biography.py:526). Cost: one sitting.
4. ERRATA FOR 191.8M (a08-r2). Write watch/inbox/48h_synth/ERRATA.md striking
   or journal-binding the 191.8M in STORY.md:240 (the run journal is a
   compiled payload with no token totals; bind to workflow REGISTRY rows or
   cut the number). Cost: 15 minutes.
5. ARM THE SEAL GATES (a07-r1/r2/r4). Seat: write tests/test_seal_forge_drill.py
   running pam.check.txt section-4's drill against seed/verify_seal.py and
   assert refusal; land mag/seed_seal.py to the pam.md spec (Ed25519 over
   seed+chain bytes, .seal sidecar, key in state/keys/, verify-at-consume
   fail-closed). Operator: mag/steer_seal.py write_keyfile() then flip
   ~/.mag/steer_seal_mode to enforce; prove a forged permit word is refused.
6. PERCOLATOR INTAKE (a02-r2). Add --candidates <file> to mag/percolator.py
   (percolate each row's claim, source=<source_url>); run once over
   frontier_olm_20260928/percolator_candidates.jsonl and
   frontier_olm_2026-10-01/percolator_candidates.jsonl; file invariant and
   explore receipts. Cost: one sitting.
7. DAY-1 FOLD BACKFILL (a02-r1). Produce DIGEST.md + register.jsonl +
   percolator_candidates.jsonl for watch/inbox/frontier_olm_2026-09-30/ from
   the on-disk 6 cards and 32 sweeps, then index them (see 8). Cost: one
   sitting; makes the 09-30 window citable like 09-28 and 10-01.
8. INDEX-LAST LAW (a02-r8). Rerun the sanctioned shared-surface writer once
   after the fold's last write so day-2's 13 unindexed files (DIGEST,
   register, candidates, RECEIPT, quantization-compression.md, sweep/xml)
   enter INDEX.json; amend olm-mine.dwf.ts with "index last, write first".
9. KVARN LINE + FETCH RECEIPT (a01/a02-r7). Append arXiv 2606.03458
   (huawei-csl/KVarN) to memory/runs/corpus_gap_research/ARXIV_REGISTER.json
   (one line). The theneurondaily fetch is DONE by a15 this session: raw
   fxtwitter bytes (203,655 bytes) carry the sentence byte-exact; append the
   receipt beside sweep/inference-efficiency-x.md and relabel 0.55 to
   primary-confirmed.
10. TRIO CARRY-FORWARD (a01-dedupe). Fetch r/LocalLLaMA 1sy7srk via
    pullpush/arctic-shift for the f16-vs-q8_0-vs-turbo KV table and append it
    (confirmed or still-owed) to steal/quantization-compression.md's OWED
    ledger; re-cite arXiv 2609.21341 into the C1 card as serving-stack prior.
11. MINT THE THREE TICKETS (a07-r3). Add SS-1 (seed-seal Ed25519 port),
    CP-1 (depends_on column + BFS cascade on invariants.json, currently 639
    rows with zero dependency keys), R2-1 (estate_corpus_search +
    estate_bonds_read on the house MCP bridge) to
    watch/inbox/hermes_burn/TICKET_LEDGER.md. Cost: 3 ticket rows.
12. FIRE MOVE 1 (a06-r4/r5). On the RX 5600 XT box with the proven
    llama-server Vulkan path (queue/todo.md Stone 7): load one 7B Q4 GGUF,
    time tok/s at 8k context, land the receipt beside watch/inbox/spiking_wide/,
    and name Mamba-3, LFM2 and Falcon-H1 as scored candidates against the
    SWA+4-sinks R0 incumbent.

## ONE-WAVE QUEUE (next band)

- E3b runtime-parity leg (a01-3): same Q4_K_M bytes via Ollama Modelfile vs
  transformers, 40-prompt pairs, >=38/40 pass; gated on the abliterate v2
  amendment (a01-2) which is itself one-sitting; 2.74 GB download + 1 pip
  install; needs the shared-env caretaker's nod.
- A1-A5 autonomous fires in one batch (a08-r4): git tag recovery-pack/...,
  probe dir, whale-patrol task, attention_feedback rows, suite task; A1 alone
  is 5 minutes. Also: F7's meter must learn to watch the Claude descent lane
  (236 rows it never counted).
- KV degradation ladder on gemma:2b + SAELIS q8_0 review ticket (a01-5): one
  afternoon, $0; the review ticket is one-sitting and can go early.
- Abliterate probe schema v2 (a01-2): one-sitting technically; queued here
  because it gates E3b and wants a test pass.
- Day-2 card hygiene batch (a01 register-row-1 relabel; a02-r3 prior-card
  check sections; a02-r5 lattice_loop num_ctx fix + git-add
  tools/olm_tokenizer_probe.py; a02-r6 kv_cache_compaction.md refresh): one
  wave, four files.
- Label-fix batch (a06-r1 MetaX/H100 line 25; a06-r2 2601.22076 retitle to
  "Where Do the Joules Go?"; a07-r5 letta line 23 to 21 + PAM register row;
  a05-r1 census erratum in B2-216 grammar; a05-r5 resolve-at-line pass):
  one wave, all byte-edits with receipts.
- Music program repair wave (a03): strong-conf rule (bpm_conf >= 3.0, n=45)
  into STYLE_SPEC + delete/implement the phantom parabolic-refine clause;
  per-cut acceptance bands derived from each cut's own DNA (CUT 1 at 107
  folded and CUT 3 at 112 are off-band by the spec's own gate); audio-dna-v2
  second recipe pass over all 110 files (vocal-band share, stereo
  correlation, per-file crest/low-ratio/acf completion of the 80); paste the
  stranger falsifier and riddle-provenance caveat into vonnegut-final HOUSE
  LAWS; restate render targets at ~3:00.
- Vonnegut wave (a04): re-pin the gate's hook band to the canon 1-4 or write
  the supersession note; strip or waive the 4 attribution tags; add
  abstraction words to the BANNED scan and rewrite the 3 doctrine-in-disguise
  lines; tier-2 entailment regrade on rows 2-5; fold the dropped workover
  material into the annotations.

## OPERATOR-GATED QUEUE (only the operator can pull)

- Ollama 0.34.3 to 0.35 quiet-window upgrade + step-0 /v1/systemone
  conformance + 3-arm bake-off (a01-4): touches the shared janitor host,
  ~2h, book a quiet window.
- Janitor-host hardening after the 3-line ticket lands (a01-8): bind
  assertion daily check, state-restore-free surface, prompt-lifetime
  guarantee; plus one netstat check.
- steer_seal enforce flip (the operator half of fill 5).
- Offsite medium choice + restic install + key journal (a08-r5): spend and
  placement decisions; A1's git tag needs no operator and should not wait.
- KVarN-adjacent: Ollama 0.35 13-dataset accuracy figures chase,
  nimble/tev1 + Qwen license texts, ExLlamaV3 CUDA feasibility (a01-10).
- llama.cpp/Ollama server-flag inventory + 2B collapse battery (a01-9):
  shared-host benchmark time.

## BELOW-CUT LEDGER (every remaining sibling gap, none lost)

- a01: reach-ratio meter probe (minutes, no owner); below-cut confirmation
  debt (doug.sh prefix-cache, MemCodex pointer-vs-inline, TAGGRAPH-vs-BM25,
  mem0 49/128, the five judge-block items, the three flock items); the
  244-to-24 adjudication criterion was never published.
- a02: day-1 finds never revisited (2609.31540, HN 43905942, four reddit
  finds, P1 knowledge_graph invariant-id truncation still live); day-1
  corpus fold map; the positive control (sweep-layer dedupe works) is the
  pattern to copy into the card layer.
- a03: artist-count definitional drift (60 raw vs 51 parsed, unnamed);
  STORY.md citation-path drift; punctuation normalization passed off
  near-verbatim.
- a04: 4-of-6 packs over the canon hook band; 4 attribution tags; 3
  doctrine-in-disguise lines; dropped workover material; tier-1 4-no
  verdicts.
- a05: 5 skipped gala slugs (spiking-wide 8, localfirst 7, music-ractor 6,
  lyric-workover 3, vonnegut-final 1 = 25 lane JSONs unmined); 2
  anchor-drifted citations; 20-of-30 prose-only law list stands as the
  enforcement backlog; MCP-2 and ractor50 absent from research_polished.
- a06: MIT Tech Review + KTH thesis primary fetches for the 2 unconfirmed
  energy rows; the ask's own named input spiking_adjacent_signals.jsonl
  does not exist in the repo (premise drift, first-class negative).
- a07: register carries no PAM row (the wave's top finding is receipt-only);
  ownmem 23-vs-21 extras.
- a08: Cairncross duplicate row; CHECK 7 REVISE correction applied nowhere;
  tapestry receipt; offsite/key-journal owed set; the bake falsifier needs a
  third failure shape named (red AND silent).

## Byte-checked quotes this register rides on (grep -cF = 1 each)

- "scheduled on zero surfaces" (a06-spiking.json)
- "a third shape the falsifier battery did not name" (a08-48h-synth.json)
- "it is the synthesis' one number that fails a byte check" (a08-48h-synth.json)
- "zero-hit grep is a finding: the wave never folded to corpus/steal" (a07-localfirst.json)
- "ZERO OF THE 18 SKILL VERDICTS' CONCRETE ACTIONS WERE EXECUTED" (a05-ractor50.json)
- "RunAnywhere says hosted GLM-5.3 Flash reaches 380 tokens/second, GLM-5.3 Max 790, Qwen3.8-27B 485, and DeepSeek-V4.1 Flash 615" (raw fxtwitter JSON, fetched and curl-verified by a15 this session)

## Negative findings, first-class

- Lanes a09-a14 did not land; 8 siblings merged. This is coverage, reported.
- The ask's "fires LAST ... poll the lanes dir" was honored: one poll at
  ~18:30Z and one at rollup start; no late landings appeared.
- No prior gap register existed; zero-hit grep, exit 1 (a finding, not silence).
- The theneurondaily 0.55-confidence number is now primary-confirmed; the
  10-01 sweep's "fxtwitter /i/article door is down (HTTP 404)" no longer held
  at 18:37Z - the door served the article body through the status endpoint.
  The sweep's door-status claim was true at its moment, false at mine.
- Nothing in this register is a fill claim except fill 9's fetch half, which
  was executed in-lane with raw-byte verification; everything else is specced,
  not done.
