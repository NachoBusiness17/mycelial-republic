# BREAK-SECURITY (hostile second pass): the singing network lens, 2026-10-10

Seat: break-security. Job: byte-check the lens's evidence, attack its falsifiers,
find what it dropped. Laws kept: no fabrication, no em-dashes, every claim cited,
quantifier law enforced (every count below names its instrument and moment).

## Instruments run this sitting (all by this seat, 2026-10-10)

- `ollama list` (live): 15 rows, output banked in the session transcript.
- `rg -n "verifyQuorum|SettleTaskWithProof" reference/gstdcoin/contracts/` -> exit 1,
  zero hits, full tree, untruncated.
- `rg -n "verifyQuorum|SettleTaskWithProof" reference/gstdcoin/gstdbot/src/` -> 6
  matching lines across 5 files (p2p/node.ts:128, p2p/identity.ts:11,
  p2p/attestation.ts:3, :34, :80, swarm/agent.ts:694).
- `rg --files -g "*consensus*"` (repo, node_modules/.git excluded) -> 11 files,
  plus `stat -c "%y %n"` on each.
- Reads (byte-level, this sitting): watch/inbox/gstd_perimeter_design_20261010/CARD.md
  (whole), watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md (whole),
  ROUTER_VOCAB_LANDED.md (whole), watch/inbox/ractor50/mcp.md:125-164,
  reference/gstdcoin/gstdbot/src/wallet/wallet.ts:30-64, src/p2p/identity.ts:1-64,
  src/p2p/attestation.ts via rg cites, src/blockchain/token.ts:384-401,
  src/gateway/server.ts:3301-3306, reference/gstdcoin/contracts/SettlementMaster.tact:100-139,
  tools/seed_mcp.py (whole), watch/inbox/mcp_layer_status_20261010.md (whole),
  dead_salmon_airllm_drop_20261010/CARD.md (whole), unisub_drop_20261010/CARD.md (whole),
  gstd_gb_pitch_20261010/CARD.md (whole), garage_wizard_network_20261010/CARD.md (whole),
  memory/facts/ox_artifact.jsonl:348-354, mag/consensus_gate.py head, mag/_consensus_witness.py head.

## VERDICTS

### F1 (A2 rides a two-family garden; label-shuffle cannot catch correlated lineage error): CONFIRMED, census corrected, concentration WORSE than claimed

Byte-checks:
- CARD.md:19-20 confirmed: the A2 control names only the label-shuffled baseline.
- ROUTER_VOCAB_LANDED.md row 7 confirmed (deepseek-r1:1.5b is qwen2 arch r1 distill);
  row 14 confirmed (Ternary-Bonsai-2-27B "quality UNPROVEN ... zero verdicts anywhere").
- Census DISPUTE: my `ollama list` this sitting reads 15 models; vocab row 15 says
  nomic-embed-text "cannot serve /chat/completions at all", so 14 are chat-capable,
  not 13. The lens's 13 (6 qwen2 + 6 gemma + bonsai) silently includes athena-class
  in the gemma count (correct per vocab row 13: athena-class:latest is gemma4 30.7B)
  and drops qwen2.5vl:3b (vocab row 6, qwen25vl arch, served on the chat router).
  Corrected: 13 of 14 chat-capable models are qwen/gemma lineage (6 strict qwen2-arch
  + deepseek + qwen2.5vl = 7 qwen lineage; 6 gemma lineage incl. athena-class); only
  the bonsai is out-of-family. The quantifier law bites the lens's "13 chat-capable"
  (its instrument moment is not named), but the error is in the direction that
  STRENGTHENS the finding: the garden is more concentrated than the lens sold.
- The analytic core (label-shuffle breaks input-output alignment but preserves each
  model's marginal error distribution, so family-correlated errors survive it) is
  sound and is CONVERGENT with estate-banked law this lens did not cite:
  mag/consensus_gate.py:4-8 and memory/facts/ox_artifact.jsonl:350 ("Majority/confidence
  aggregation implicitly assumes votes are conditionally independent draws around the
  truth. They are not: agents share pretraining corpora, fine-tuning teachers, RLHF
  preference sources"), LAW-CONS-ILLI-001, banked 2026-08-24. Duplication is emphasis:
  F1 outranks a novel finding for this reason.
- Falsifier attack: the lens's falsifier (3+ family set agreeing at same-family rates
  => publish the null) is falsifiable and survives. One gap: with 14 local models and
  only 1 out-of-family, the falsifier is UNTESTABLE on local iron alone; the move's
  API-tier out-of-familyanimals leg is load-bearing, not optional. Keep it mandatory.

### F2 (A1 verifies the theater's counter; the signed lane targets phantom methods): CONFIRMED, two cite corrections, falsifier needs one sharpening

Byte-checks (all re-run by this seat, not ridden on the audit):
- `rg "verifyQuorum|SettleTaskWithProof" reference/gstdcoin/contracts/` -> exit 1,
  zero hits, full contracts tree. CONVERGENT with GSTD_TOKENOMICS_AUDIT.md:52 and the
  lens's own greps.
- All five gstdbot reference sites byte-verified: p2p/attestation.ts:3, :34, :80;
  p2p/identity.ts:11; swarm/agent.ts:694 (and p2p/node.ts:128, which the audit had and
  the lens dropped).
- Fabrication sites byte-read: src/blockchain/token.ts:387 recordEarning, :391
  `hash: 'tx_' + randomBytes(16).toString('hex')`, :398 `status: 'confirmed'`.
  CITE CORRECTION 1: the audit/lens span "token.ts:387-396" contains the hash but the
  'confirmed' status lands at :398, two lines past the span. Substance intact.
- CITE CORRECTION 2: the fabricated claim txHash is at src/gateway/server.ts:3304, not
  ":3305" as the audit (line 21) and lens cited; and the cite should name the directory
  (two server.ts files exist: gateway and dashboard).
- CARD.md:13-14 confirmed verbatim: A1 asserts "the paying node's balance/ledger delta"
  and claims it "closes our audit's settlement-theater finding on a staging rail".
- SettlementMaster.tact:128-135 byte-read this sitting: SettleTask requires
  owner-or-gateway sender (:129), replay-guards taskId only (:134); 85/10/5 split at
  :106-108, baseRate at :110. The trusted-fields chain the audit alleged is real.
- Audit cite spot-checks: :6-7 (platform unobservable), :19-22 (fabrication),
  :47-53 (phantom method), :95-98 (91% gateway emissions) all match my reads.
- Falsifier sharpening (the one hole): the proposed on-chain read arm fires "chain
  shows nothing" on day one if the staging rail is counter-based BY DESIGN. The audit
  (lines 17-19) established live payouts ride D1 counters and per-payout minting is
  unobservable. A falsifier that cannot fail clean is not a falsifier. The arm must
  first pin WHERE staging settles (GB's docs or his answer); if staging is counter-only,
  A1's honest scope is counter-integrity-plus-reconciliation, and CARD.md:14's "closes
  the settlement-theater finding" must be reworded, because a staging counter cannot
  close a mainnet-theater finding either way.

### F3 (vast arm puts wallet seeds under lessor-readable keys): CONFIRMED, and UNDERSTATED

Byte-checks:
- wallet.ts:42-52 byte-read: deriveKey() reads /etc/machine-id (:46), falls back to a
  homedir string (:48), sha256s it into the AES-256-CBC key for wallet_seed.enc (:51,
  :54-60). The lens cite ":43-51" holds.
- CARD.md:34-36 (tailnet perimeter places rented hosts inside the mesh) and :37-39
  (identity pinning = persistent volumes = longer seed-at-rest dwell) confirmed.
- The analytic chain (host root reads machine-id and the seed file together; AES under
  a co-located secret is obfuscation, not custody) is sound. The homedir-string
  fallback is weaker still (a knowable string, no host secret at all).
- Why understated: see ADDITION A2. The wallet seed is the SECOND key at risk; the
  attestor seed is plaintext.

### F4 (seed MCP breaches never-cross rule 4; cap is caller-raisable): CONFIRMED

Byte-checks:
- tools/seed_mcp.py:112 `def tool_rebuild_subtree(self, into: str, ...)`, :114
  `root = Path(into)`, :130 `target.write_bytes(raw)`. No allowlist or void-check on
  `into` anywhere in the function; is_void at :122 guards only the seed's entry rel
  paths. Confirmed: caller-supplied write root, exactly the class never-cross rule 4
  pins (watch/inbox/ractor50/mcp.md:147-150, byte-read: "Caller-supplied write paths.
  The writer is pinned").
- :187 `cap = max_bytes or self.fetch_cap` confirmed; --max-fetch feeds fetch_cap via
  the constructor (:356-357, :363), and any caller max_bytes above it wins. The
  docstring at :12-14 promises the cap. Confirmed: a gate that tests itself.
- is_void def at :52-53 confirmed (entry paths only).
- Sibling instances the lens did not list: rebuild_subtree also takes a caller
  `source` root (:139, pointer-check reads from a caller-chosen tree) and verify_hash
  takes a caller `root` (:162, arbitrary-path hash oracle). Same doctrine class, lower
  severity; fold into the same fix.
- Falsifier attack: the lens's post-fix falsifier ("any test that still raises the
  served cap above --max-fetch or lands bytes outside the pinned root") is runnable
  and correct. Survives. Note the fix must use min(max_bytes, self.fetch_cap) and
  must ALSO decide the max_bytes=0 edge (`or` currently treats 0 as absent).

## BLIND-SPOT AUDIT (the lens's six, verdict by verdict)

1. "GB's staging platform code is unobservable": STANDS (audit :6-7; nothing on disk
   contradicts it).
2. "No vast.ai rental made live; pricing is estimate-class": STANDS (CARD.md:6-9
   self-labels ESTIMATE-CLASS; no rental receipt exists in any card read this sitting).
3. "The consensus harness does not exist yet; find *consensus* newer than the thesis:
   zero hits": WEAKENED. My census (`rg --files -g "*consensus*"`, this sitting) reads
   11 files; ONE is newer than the thesis:
   watch/inbox/babelfish_selfmine_20261010/RIB_TRANSLATED_rib_mindsweave_eval_consensus_illusion_2.md
   (mtime 2026-10-10 00:29:48 vs thesis mtime 2026-10-08 23:05:18, stat -c). The
   substantive claim (no GSTD perimeter harness exists) still holds, that file is a
   rib translation. But the deeper miss: the estate ALREADY OWNS consensus
   instruments a filename grep hides: mag/consensus_gate.py (2026-10-05),
   mag/_consensus_witness.py (2026-08-25), tests/test_consensus_degeneracy_20261005.py,
   handoff/OX_MEGA_consensus_illusion_detection.json (2026-08-22). The descent
   protocol leg 1 (prior-art sweep by SUBJECT, not filename) was the missing instrument.
4. "Papers known via drop cards, not read first-hand": PARTIALLY CLOSED BY THIS SEAT.
   dead_salmon CARD.md:3 claims "Both fetched first-hand (grok verbatim + arXiv
   abstract + GitHub)"; unisub CARD.md:4-5 claims "read first-hand at abs page +
   toshi2k2.github.io/unisub project site". The arXiv ids (2512.18792, 2512.05117)
   remain card-backed; I did not refetch arXiv this sitting, so they stay OWED at my
   layer, not asserted.
5. "Tailscale/WireGuard ACL semantics not lab-tested": STANDS (no test artifact found;
   spec demand only).
6. "Tact line-cites ride the 2026-10-09 audit": MOSTLY CLOSED BY THIS SEAT. Re-verified
   independently: the contracts grep (zero hits) and SettlementMaster.tact:106-135.
   Still ridden: GSTDJetton.tact cites (:107, :111, :120, :123) were not re-read.

## ADDITIONS (what the lens missed)

A1. A2 HAS NO GROUND-TRUTH ARM, and the estate's own banked law says majority-of-
correlated-samples is the wrong estimator. The perimeter measures agreement; unanimous
wrong answers beat the label-shuffle control trivially (mode collapse), and the estate
has a MEASURED calibration ladder saying small-model unanimity is barely above chance
or an anti-signal (mag/consensus_gate.py:9-17: 1.5B AUROC 0.58, 7B 0.71, 27B 0.89,
120B 0.09; the garden is 1.8B-8B plus two unproven big locals). A tested failure
already exists: the babelfish rib (mtime 2026-10-10 00:29) records flock consensus
returning the WRONG answer at strength 0.67 while single-local and strong-remote were
both right. The fix organ exists: consensus_gate.verdict() (n>=2 floor, refusal
stripping, scale weighting) plus the dogfood task bank's mechanical graders
(ROUTER_VOCAB_LANDED.md:100-102, pace_run.py grades shapes against ground truth).
MOVE (~45 min): A2 aggregator gains a ground-truth-anchored correctness column and a
verdict()-weighted consensus score; assert consensus-beats-shuffle AND correctness-
vs-ground per shape; import, never re-derive. FALSIFIER: any task shape where consensus
strength is high while ground-truth correctness sits at or below chance proves the
aggregator is measuring echo; the babelfish row is the fixture.

A2. THE ATTESTOR KEY IS PLAINTEXT ON DISK, worse than the wallet seed F3 flagged.
reference/gstdcoin/gstdbot/src/p2p/identity.ts:42-46 writes the Ed25519 seed as raw
seedHex JSON to ~/.config/gstdbot/attestor-identity.json; the comment at :45 claims
"same posture as wallet.json" but wallet seeds get AES (wallet.ts:54-60): the comment
is a lie in code. On a pinned vast volume the lessor clones the signing identity and
can FORGE SettleTaskWithProof attestations, poisoning the signed lane A1/A2 ride,
which is worse than stealing test funds. MOVE (~15 min): fold into the lens's KEY
CUSTODY law (disposable attestor identities per rental too) and file the
comment-vs-code delta upstream (it is GB's repo). FALSIFIER: any rented-host build
whose attestor-identity.json contents cannot forge a valid attestation on another
host means the key is not plaintext-stealable; the file's seedHex field is the
counterexample already on disk.

A3. THE PERIMETER CARD MISQUOTES THE UNISUB PAPER by dropping its own qualifier.
CARD.md:22-23 sells A2 as "the behavioral analog of today's unisub paper claim
(disjoint models converge)" and the GB addendum (:84-87) as "the behavioral version
of the convergence paper", but the estate's first-hand read of the paper carries the
abstract's own qualifier: convergence is WITHIN shared architectures, "do not
overclaim cross-architecture" (unisub_drop_20261010/CARD.md:14, caveats at :51-55).
The garden is two architectures; F1 shows the "different models" are mostly same-
architecture siblings. As written, the beauty line sold to GB is the paper's within-
architecture effect in a cross-model costume: a lie waiting to be caught by the first
person who reads the paper. MOVE (~10 min): amend CARD.md:22-23 and the addendum to
carry the qualifier, or make A2 span 3+ architectures so the analogy is honest.
FALSIFIER: if A2's consensus sets span 3+ architectures and still converge at rates
matching the paper's within-architecture bands, the analogy upgrade is earned; if the
card keeps the unqualified line, the catch is owed to the first external reader.

A4. THE DEAD-SALMON LAW AS LANDED PRESCRIBES TWO CONTROL ARMS; A2 NAMES ONE.
dead_salmon_airllm_drop_20261010/CARD.md:19-20 states the falsifier law as "survives
a random model check, a label shuffle, an intervention test", and its protocol
amendment (:21-24) makes the negative-control arm "(random-weights model,
label-shuffled run)" MANDATORY for probe lanes. The perimeter CARD.md:19-20 implements
only the label-shuffle arm, so the harness is under-controlled by the estate's own
freshly-minted law, two cards over. MOVE (~20 min): add the random/degenerate-model
arm to the A2 control section (a fixed garbage responder or a randomly-initialized
small model is enough; the control needs a floor, not realism) and an intervention
leg (re-ask with a corrupted task input; true consensus should track the change).
FALSIFIER: if the added arms never change any verdict the label-shuffle arm already
issues, the extra arms are decoration and the original one-arm design was sufficient;
publish that null instead of carrying unearned machinery.

A5. THE GPS LEDGER FEED CAN POISON THE NETWORK'S MEMORY (the self-learning law's
instrument). CARD.md:79-80: the aggregator "Feeds the GPS capability ledger as
consensus-contrib rows", and the ledger drives real routing (ROUTER_VOCAB_LANDED.md:
19-24: routes on pass-rate from the SQLite capability ledger). If consensus-contrib
rows bank "pass" from family-correlated agreement (F1) or consensus illusion (A1),
the network learns the echo: the router will PREFER echo models, and the thing that
"should learn on its own as it grows" learns theater. record_verdict's Q28 gate
re-hashes cited bytes (ROUTER_VOCAB_LANDED.md:23-24), which proves the bytes exist,
not that the votes were independent. MOVE (~30 min): consensus-contrib rows require
family-partition and ground-truth columns plus the control delta; land the schema
field before Phase 2, not after the first sweep. FALSIFIER: a ledger read showing
consensus-contrib rows whose pass-rates diverge from ground-truth-anchored
correctness for the same model+shape is the poisoning caught in the act.

A6. PHASE 3'S HEADLINE NUMBER WOULD BE MEASURED ON A RAIL GB WILL NEVER SHIP.
CARD.md:40-43 names whitelisting the perimeter IP range on the staging platform as
"the real fix" for the rate bucket, and Phase 3 (:71-73) runs the ~1000-node
launch-scale reward test through that perimeter. Payout-holds-at-1000 measured on a
whitelisted rail does not transfer to launch conditions (no whitelist at launch; the
bucket math is ~1 req per 10-15s per IP, gstd_gb_pitch_20261010/CARD.md:17-20).
MOVE (~10 min): Phase 3 goes dual-rail (whitelisted core for A1/A2 depth plus an
unwhitelisted burst sample sized to the bucket math), or the claim is re-scoped to
"payout under whitelist" in the GB reply. FALSIFIER: if unwhitelisted and whitelisted
rails show the same payout-per-task at the same node count, the whitelist concern was
decoration; if they diverge, the single-rail number was the caught lie.

A7. THE PERIMETER SPENDS THE GUILD'S NAME AGAINST THE GUILD'S OWN LAW, and the bench
leg names no wallet. garage_wizard_network_20261010/CARD.md:40-42 (v1 law: "Growth-
without-need = the monster class") and :101-102 ("no platform is built before the
guild ritual shows demand") sit against perimeter CARD.md:59-61 and :71-73 (the blade
as "the Garage Guild's first shared asset", benches hosting perimeter boxes, a Phase 3
guild fleet). Also "the guild's collective test fleet earns GSTD" names no wallet or
split: on other people's benches that is either the declared supporter-toggle pattern
(distribution thesis, gb_pitch CARD.md:43-45: "user's-own-wallet default, loud opt-in
supporter toggle, never silent founder-mining") or silent operator mining by another
name, the exact 91%-gateway pattern the audit condemned (GSTD_TOKENOMICS_AUDIT.md:95-98).
MOVE (~10 min): gate Phase 3's guild leg on the guild card's own falsifier (ritual
alive at month 1) and add one wallet-posture line to the perimeter CARD (whose wallet,
what split, declared). FALSIFIER: if the guild ritual is alive and the wallet posture
is declared before any bench joins, the conflict was sequencing only; if benches run
before either, the monster-class law was broken in the guild's name.

## CONVERGENCE FLAGS

- F1 is CONVERGENT with LAW-CONS-ILLI-001 (ox_artifact.jsonl:348-354, banked
  2026-08-24) and mag/consensus_gate.py (2026-10-05): two independent derivations
  (the lens from lineage arithmetic, the estate from measured AUROC) of the same
  law. Per the duplication-is-emphasis rule, F1 outranks any novel single-source
  finding in this pass.
- F2 is CONVERGENT with GSTD_TOKENOMICS_AUDIT.md:49-53 (phantom methods) and :19-22
  (fabrication): the lens's greps and mine agree across two sittings.

## OWED (not asserted)

- arXiv ids 2512.18792 and 2512.05117: card-backed first-hand claims, not re-fetched
  by this seat.
- GSTDJetton.tact cite lines (:107, :111, :120, :123): still riding the audit.
- Staging platform internals: unobservable, unchanged.
- Tailscale ACL enforcement: untested, spec demand only.
