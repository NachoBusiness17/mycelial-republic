# BREAK PASS: moonshot-2 (hostile second lens, 2026-10-10)

Instrument: every cite re-read or re-run this sitting against the estate; the
ask's JSON payload arrived truncated mid-finding-3 (findings 4 and 5 cut off),
so the full five-finding report was recovered from the on-disk original
(watch/inbox/ractor_engine/2026-10-10-singing-network/moonshot-2.md, read
whole this sitting) and all five are verdicted. Bash on this host runs through
git-bash; python ran as .venv/Scripts/python.exe; no subprocess spawned beyond
the interpreter itself.

## Verdicts

### F1 (A1 verifies the theater's bookkeeping): CONFIRMED

Every byte re-derived first-hand this sitting, no cite failed:

- CARD.md:13-14 verbatim (A1 = ledger delta, "closes our audit's
  settlement-theater finding") and CARD.md:15-20 (A2 + dead-salmon) both read.
- watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md:20-23 and 47-54
  read; the audit's own line-number for the token.ts block is 387-396 where
  moonshot-2 says 388-398; both windows cover the same recordEarning body.
- reference/gstdcoin/gstdbot/src/blockchain/token.ts:388-398 read: hash
  'tx_' + randomBytes(16), status 'confirmed'. Exact.
- reference/gstdcoin/contracts/SettlementMaster.tact:128-135 read: SettleTask
  gated only on sender==owner||gateway (:129), zero-address worker (:131),
  taskId replay latch (:134-135). Exact.
- Phantom-method census RE-RUN UNTRUNCATED over the whole contracts tree
  (.venv/Scripts/python.exe pathlib rglob, all files): 0 hits for
  verifyQuorum|SettleTaskWithProof. The lens scoped its grep to
  SettlementMaster.tact and got 0; the full tree also gives 0, so the claim
  survives the quantifier law with room to spare.
- Node-side targets: attestation.ts:3 and swarm/agent.ts:694 both byte-match;
  my census also surfaced attestation.ts:34, attestation.ts:80, identity.ts:11,
  p2p/node.ts:128 (the lens cited 3 of the 6; under-cite, not over-cite).
- Genesis-seal cite (audit 42-44) read: "supply grows only with verified work",
  no enforcement site. Exact.

Falsifier (TON testnet wallet pull after an A1 pass) is named, honestly
unrun (no testnet, no staging, platform Workers code not public). CONVERGENT
beyond the lens's own flag: siblings lineage.md F1 (marked CONVERGENT),
dogfood.md finding 2, operations.md, economics.md:69, communication.md:39,
moonshot-1.md:33 all re-derive the same A1-theater conviction. See Addition 3
for a cheaper tonight-runnable variant of its falsifier.

### F2 (dead-salmon blind to family correlation; ~3 lineages): CONFIRMED, census corrected, one defect in the proposed move

Confirmed bytes: CARD.md:15-20 and 22-23 read; unisub_drop CARD.md:9-14 read
("within shared architectures - the abstract's own qualifier" is verbatim at
13-14); dead_salmon_airllm_drop CARD.md:19,24 read (the control IS a
label-shuffle; a shuffle permutes the key, never the model-correlation
structure). The logical core stands and the falsifier (family-blocked K-sets,
within-minus-between gap) is the right instrument.

Corrections from my re-census (.venv/Scripts/python.exe over
tools/gps_mcp/config.gstd.json + config.json):

- 20 providers total: CORRECT.
- Test doubles: 6, not 5. tools/gps_mcp/config.json (the shipped config,
  read this sitting) holds exactly 6 providers: yesno-tiny, gemma2:2b,
  gemma4-short-worker, vendor/flash-cheap, vendor/flash-fast, opus-class.
  ROUTER_VOCAB_LANDED.md:57-58 says "the 6 shipped test-double providers PLUS
  14 gstd-tier provider rows". The lens's 5 came from counting the shipped
  double gemma4-short-worker (which it renamed "gemma-worker-4b") as a garden
  gemma.
- Garden partition: gemma-line 6, not 7 (gemma:2b, gemma2:2b-instruct-q5_K_M,
  gemma4, gemma4-desk, gemma4-hermes, athena-class), qwen-line 7 (incl
  deepseek-r1:1.5b), ternary-bonsai 1. 6+7+1 = 14 real rows. Siblings
  independently landed the same 6 (moonshot-1.md:57-58 "~6 gemma-derived",
  security.md:29-31 "6 gemma-lineage"); moonshot-2's 7 was the outlier.
- Net effect STRENGTHENS the finding: 2 proven lineages + 1 zero-verdict
  experiment (ROUTER_VOCAB:49: ternary "quality UNPROVEN... zero verdicts
  anywhere"), i.e. the fleet is MORE concentrated than the lens claimed.
- Cite defect: the deepseek-r1:1.5b qwen2-arch mapping lives at
  ROUTER_VOCAB_LANDED.md:42 (table row 7), not :49-50 (which point at the
  ternary and nomic-embed rows). Fact right, anchor wrong.

Defect in the MOVE, not the finding: the K-set rule ">=4 distinct vendor
lineages" measures VENDOR, but the unisub echo prediction is
architecture-scoped (their own qualifier). deepseek-r1:1.5b is DeepSeek
vendor on qwen2 arch: it passes a vendor-diversity rule while being an
architecture sibling. A sweep of 4 vendors all serving qwen2-arch models
would satisfy the rule as written and still be lineage echo. Fix is one
word: stratify on architecture family; count vendor diversity separately.

### F3 (self-learning bar has no instrument; divergence curriculum): CONFIRMED

- CARD.md:18 verbatim ("divergence cases banked as receipts" is the loop's
  last step).
- mag_magatama_primer CARD.md:72-74 verbatim ("means it is a pile, not a
  Mag").
- tools/gps_mcp/ledger.py read end to end this sitting: every named property
  byte-verifies (append-only verdict_log, INSERT-only, no UPDATE/DELETE
  anywhere; Q28 evidence gate at :509-562; a04 dedupe SELECT at :387-413 with
  the partial UNIQUE index at :32-34; momentum at :623-681; capability PK
  (model_id, task_shape) at :13, and no pairwise/agreement table exists in
  SCHEMA_SQL, so "cannot hold a pairwise agreement matrix" is structural).
- Live census RE-RUN: capability 34, verdict_log 707, evidence_resolved=1:
  213. Exact match.
- arena_gwap.py:58 is exactly TASK_SHAPE = "arena-agreement-v1";
  arena_gwap.py:7-27 docstring read: the independent-cop pattern
  (cop parses the post-roll record independently, claimed-but-unruled scores
  as disagreement, silent cop = BLOCKED) is verbatim there. Live rows
  re-queried: 4 models, verdict counts 71/107/135/148, pass rates
  0.0467-0.5430. Exact.

Missed prior art that SUPPORTS the finding: see Additions 1 and 2. Falsifier
(replay the task bank after a month; zero divergence-provenance tasks +
unchanged routing = executed-not-learned) is checkable and correctly framed
as the acceptance bar's instrument. Partial convergence: operations.md:50
(divergence as curriculum-grade signal), communication.md:158-159
(SONG_DIGEST top-3 divergence cases per sweep).

### F4 (never-silent founder-mining has no byte instrument): CONFIRMED

- gstd_distribution_thesis_20260109.md:21-33 read: default wallet user's own,
  supporter toggle default OFF, "cannot silently mine for the founder"
  verbatim.
- gstd_gb_pitch_20261010/CARD.md:44-45 (never silent founder-mining) and :53
  (toggle "should carry his blessing") read.
- Perimeter CARD.md read whole: no wallet, toggle, or split appears anywhere;
  the harness asserts only "payout delta asserted" (CARD.md:78). Confirmed
  absence, instrument = full-file read this sitting.
- GSTD_TOKENOMICS_AUDIT.md:95-99 read: 51.4735 of 56.6955 visible GSTD = 91%
  to the operator's own gateway/node address. The lens's honest scoping
  ("their bytes, their network, pre-return") stands.

Falsifier (undeclared destination set, or split pct not summing to the delta,
caught by bytes) is the right shape. Partial convergence:
communication.md:121, moonshot-1.md:26.

### F5 (model identity self-reported; seed second consumer): CONFIRMED

- CARD.md:37-39 (identity pinning, ghost rows) and :78 (model id among
  asserted fields) read.
- mcp_layer_status_20261010.md:71-74 (law MCP-2 verbatim) and :113-116
  (second-consumer open item verbatim) read.
- ractor50/mcp.md:189-195 read: the law's origin block, exact.
- SEED_RIB_FORMAT_v0_20260926.md:96-99 read: falsifier (b) "a pointer entry
  gets synthetic content instead of a named stub" is the never-invented-bytes
  law the lens invokes.
- tools/mcp_parity.py exists on disk (19,006 bytes, read its presence).
- The ollama-digest mechanism is general knowledge, unfired: spec-class, as
  the lens itself scopes.

Multi-way convergent: lineage.md F3 (CONVERGENT flag on the same fold),
dogfood.md finding 4, economics.md:139-140. Falsifier (swap served model,
expect quarantine; cold container fails join = seed stays proved-once) is
honest in both directions.

## Additions (what moonshot-2 missed)

1. The estate already owns a MEASURED consensus-illusion law with a size-tier
   calibration ladder, and neither the CARD's A2 nor moonshot-2's
   family-stratification fix names it: mag/consensus_gate.py (read :1-40 this
   sitting), LAW-CONS-ILLU-001, memory/facts/ox_artifact.jsonl:348-354:
   agreement among correlated samples is an ANTI-SIGNAL, AUROC 0.58@1.5B,
   0.71@7B, 0.89@27B, 0.09@120B (unanimity at 120B = Confident Mode
   Collapse). The garden fleet is mostly 1.8B-8B (deepseek-r1 1.8B, gemma:2b
   2.6B, gemma2:2b 2.6B, qwen2.5:3b, qwen2.5:7b, gemma4 8B per
   ROUTER_VOCAB_LANDED rows 7-13), so even family-stratified consensus from
   this fleet rides the bottom of the ladder. Third axis the whole singing
   network frame missed: SIZE TIER, with the organ already written (verdict()
   importable, refusal-stripping and n>=2 floor already cured per the
   2026-10-05 ouroboros note in the module). Falsifier: an all-sub-7B K-set
   returning unanimous consensus must route UNVERIFIED by the estate's own
   law; a harness receipt that CONFIRMS it contradicts measured law, and if
   tier-gated consensus shows no monotone relation to the AUROC ladder across
   sweeps, the ladder does not transfer to this fleet and that itself is a
   bankable finding. Move: 30 min, add the tier-aware gate call plus a
   size-tier-mix column to the A2 spec.

2. The estate already computed cross-model pairwise agreement once and left
   it in exactly the pile F3 convicts: tools/gauntlet_grade.py:259-278 (read
   this sitting) banks ONE register row for a 3-free-seat group with model
   "3 free seats" and note "pairwise overlap ... (AUROC-ladder tier wiring
   next pass)"; GAUNTLET_REGISTER.jsonl grep = 4 gauntlet:consensus rows,
   latest 2026-10-07, overlaps 0.45/0.44/0.35, wiring still not landed. This
   is (a) receipts-only prior art for F3's sibling-table decision (the
   register row shape already answers "receipts-only" and no gps_ledger
   surgery is needed to start), and (b) a live specimen of banked-not-
   consumed: the number exists since 10-07 and nothing reads it. Falsifier:
   a consumer of "gauntlet:consensus" rows outside gauntlet_grade itself
   would void the pile reading; grep found none. Move: 15 min, fold the
   register-row shape into F3's spec as the receipts-only default and name
   the wiring debt so the consensus harness does not mint a second pile.

3. F1's theater is detectable TONIGHT at $0 without TON testnet, by hash
   shape alone: the fabricated hash is 'tx_' + 32 lowercase hex
   (token.ts:391, byte-read this sitting; the audit's server.ts:3305
   'tx_'+sha256 form is card-cited, not re-read), while real TON transaction
   ids are 44-character base64-style strings over 32 bytes, never
   tx_-prefixed hex. A regex assert (^tx_[0-9a-f]{32}$ = theater by
   construction) converts F1's wait-for-testnet falsifier into a Phase-1
   kill-test the desktop rig can run before any spend. Falsifier: a genuine
   TON tx whose id matches the tx_-hex grammar (encoding-wise implausible,
   which is why the shape is evidence), or a staging that emits well-formed
   non-tx_ hashes that still resolve to nothing on-chain, in which case the
   regex is necessary-but-insufficient and the chain pull stays required.
   Move: 10 min, one assert line plus both accepted hash grammars named in
   the A1 spec.

4. Between-family agreement has NEVER been measured anywhere in the estate:
   the only prior art, arena-agreement-v1, is 4 anthropic models (live query
   this sitting: claude-sonnet-5.5, opus-5.5, fable-5.1, haiku-4.5), i.e.
   single-family. F2's between-family arm therefore has no baseline number
   anywhere on disk; its first sweep produces the estate's first cross-family
   measurement. Falsifier: any estate byte holding a cross-family agreement
   measurement (ledger shape or register row keyed on two different-family
   models) voids this; none found. Move: 0 min, but the first between-family
   row should be labeled first-of-its-kind in the receipt header, not
   compared against a phantom baseline.

5. Census corrections owed to the record (detail in F2 above): 6 shipped
   test doubles not 5; garden gemma-line 6 not 7; the deepseek-r1 mapping
   anchor is ROUTER_VOCAB_LANDED.md:42, not :49-50. Two sibling lenses
   (moonshot-1, security) independently census 6+6, so the corrected
   partition is itself convergent. Move: 5 min wherever F2 gets promoted.

## Hostile-pass summary

No finding died; no finding even weakened in substance. The one move-level
defect found (vendor vs architecture axis in F2's K-set rule) and five cite-
or-count corrections are all cheap and none reverse a conclusion. The lens's
honesty structure holds up under byte fire: its blind-spot list accurately
named what it had not done, and its CONVERGENT flag (vs the 10-09 audit) is
now multiply-confirmed by six sibling lenses. The two real misses are the
consensus_gate law (Addition 1, the only existing estate organ that already
ENFORCES distrust of correlated consensus, with measured numbers) and the
gauntlet pairwise-agreement pile (Addition 2, which is F3's disease caught
in the act on a sibling organ). Both cuts strengthen the lens's own thesis:
the singing network's instruments exist in pieces, and the pieces are
already demonstrating the failure modes the lens predicts.
