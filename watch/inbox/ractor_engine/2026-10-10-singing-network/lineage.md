# LINEAGE lens: THE SINGING NETWORK (GSTD closed perimeter + heterogeneous consensus + MCP toggle layer) - 2026-10-10

ERRATUM (2026-10-10, hostile second pass accepted, re-verified this sitting): F2's
min_support cite was ROUTER_VOCAB_LANDED.md:18 (grep: exactly one hit), not :30-31,
and the lineage DIRECTION was reversed - router.py landed 91acc5bdf 2026-09-29 BEFORE
gps_router_v0.py's min_support arrived 9bac820a1 2026-10-07, and `git log -S
min_support -- tools/gps_mcp/router.py` returns zero commits (never existed there):
the floor was invented LATER in the sibling instrument and never ported back, not
dropped. F5's shuffle-within-task instrument was unbuildable (verdict_log has no task
key; 461 rows carry 461 distinct evidence_hash, zero multi-verdict groups) and its
comparison arms were path-mismatched (LM7 clamp holds opus at 0.5430 vs raw 0.5333,
fable 0.3369 vs raw 0.3239). Both findings below carry the corrected forms.

Lens frame: Lessig's four modalities, operator's "lessig ponytail" order - law (Tact
contracts), norms (receipt culture), markets (GSTD rewards), architecture (MCP +
consensus). Linage jacket: what prior ractors asked that was never delivered, and what
this wave dropped between generations. Every claim below cites bytes I read or a command
I ran THIS sitting; anything unverified is named OWED. No em-dashes.

The beauty call first: the network's memory is ALREADY WARM and its boot path is
ALREADY PROVED. The estate has 461 heterogeneous-agreement verdict rows banked
(arena-agreement-v1) and a 7-step cold-join protocol that passed its falsifier once.
A perimeter built on those two organs does not start empty; it starts mid-song. What
would make it sing is the loop: nodes boot from the seed, earn verdict rows, the rows
steer routing, routing steers the next sweep. What is a lie waiting to be caught is
named per finding below.

## F1 (LAW): A1 as instrumented does not close the settlement-theater finding; the phantom contract method is the unnamed first Tact deliverable. CONVERGENT (audit 10-09 + this sitting's re-census).

The perimeter CARD claims A1 REWARD "closes our audit's settlement-theater finding on a
staging rail" (watch/inbox/gstd_perimeter_design_20261010/CARD.md:13-14). But the
theater finding was that payouts ride a platform D1 counter while node code FABRICATES
tx hashes: gstd_earned is "a platform D1 counter... not an observable chain balance",
token.ts:387-396 fabricates 'tx_'+randomBytes with status 'confirmed', and the revenue
engine contains zero chain-call code
(watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md:17-24). The estate's only
end-to-end paycheck receipt was itself read from that same counter: "Platform nodes
API: tasks_completed 1 -> 2, gstd_earned 0.027056 ->" (DOGFOOD_DATA.md:105). If the
harness asserts the balance delta from the platform's own API, it asserts the theater's
own scoreboard and calls the finding closed. That is the lie waiting to be caught.

The deeper law-side drop: the audit found the signed lane targets phantom methods -
attestation.ts:3 says signatures "MUST exactly match SettlementMaster.tact's
verifyQuorum()", agent.ts:694 and p2p/node.ts:128 reference SettleTaskWithProof, "grep
of contracts/ for either name returns ZERO hits (2026-10-09)" (AUDIT:48-54). I re-ran
the census THIS sitting: `grep -rn "verifyQuorum|SettleTaskWithProof"
reference/gstdcoin/contracts/` returns zero hit lines, while the node source still
references them at reference/gstdcoin/gstdbot/src/p2p/attestation.ts:3, :34, :80,
swarm/agent.ts:694, p2p/node.ts:128; SettlementMaster.tact carries only
`receive(msg: SettleTask)` at :128 (the trusted-gateway-field path, AUDIT:128-135) and
no WithProof receiver anywhere in the file (grep of the file's receive/message surface,
this sitting). GB's need list includes "TON/Tact contract work" - and the estate
already scoped the exact first job (AUDIT:132-134: "Top unmet need:
settlement-grade verifiable work-minting - the one thing the seal promises and nothing
enforces") - yet the perimeter CARD never names it. The lineage debt: two days old,
one generation old, still undelivered.

MOVE (30 min, spec amendment): split A1 into A1a (platform counter delta, trivially
true, names itself as the D1 read) and A1b (chain-visible settlement delta on TON
testnet, read from a TON explorer/API, NOT the platform; requires one banked question
to GB: does the staging platform settle on-chain at all?) and add "implement
verifyQuorum + SettleTaskWithProof in SettlementMaster.tact so the signed lane has a
real target" as the perimeter's named Tact deliverable. FALSIFIER: if GB's staging
settles on-chain and the harness reads the chain (not the D1 counter) and deltas still
land, A1b is honestly closed; if the harness ships reading /api/v1/nodes gstd_earned,
A1 is settlement theater with a receipt on it.

## F2 (ARCHITECTURE): the network's memory has no sample-size floor; 6 rows at rate 1.0 with n<=2 are routing-eligible today, and min_support=5 was invented then dropped between generations.

The self-learning law names the GPS capability ledger as the network's memory. I read
the routing gate: `passes_threshold = pass_rate >= constraints.pass_rate_threshold`
(tools/gps_mcp/router.py:252-253, DEFAULT 0.85 at :40) - sample_size is CARRIED in the
Candidate (router.py:106) but never GATES anything. The sibling instrument learned the
law and the live router never received it, in this order (git, re-run this sitting):
router.py first landed 91acc5bdf 2026-09-29 ("gps-mcp v0 LANDED"); min_support=5
entered gps_router_v0.py at 9bac820a1 2026-10-07 (commit message: "evidence gate >=5
rows per shape"), EIGHT DAYS LATER, and `git log -S min_support --
tools/gps_mcp/router.py` returns zero commits - the floor never existed in the live
organ. ROUTER_VOCAB_LANDED.md:18 names min_support=5 as the generated artifact's
evidence gate (grep: exactly one hit in that file). So the true lineage shape is not a
drop between generations but a FAILED FORWARD-PROPAGATION: the estate learned the
n-floor law in one organ (the ml3 lane's table generator) and the organ actual traffic
rides never got the lesson - which is verbatim the living-weights rib's own falsifier
1, "a session where the estate failed to carry a lesson forward"
(memory/rib/RIB_LIVING_WEIGHTS_BY_NATURE.md:17). The self-learning law fails at
estate scale exactly the way the singing network would: learning logged in one place,
routing decisions made in another. Live census THIS sitting
(.venv/Scripts/python.exe over tools/gps_mcp/gps_ledger.db3): capability holds 34
rows; 12 have sample_size<=2; 6 of those claim pass_rate 1.0 - and ROUTER_VOCAB_LANDED
itself appended rows "all four pairs at rate 1.0, n=1" (ROUTER_VOCAB_LANDED.md:96-97),
including a classify row the same receipt honestly downgraded (strict per-line pairing
was 3 of 5, ROUTER_VOCAB_LANDED.md:117-124). At perimeter scale (50 to 1000 nodes
x consensus sweeps x many models) this class multiplies: a thousand n=1 "perfect"
rows is a network that logs, not learns - and "cheapest wins" (router.py:341) will
park traffic on the cheapest lucky-once model. The instrument that makes learning
measurable is an n-floor in the gate, not just the column.

MOVE (45-60 min): add `min_sample_size` to Constraints (default 5, caller-overridable)
and gate in `_evaluate` (sample_size below floor = exploration-class candidate, never
"cheapest wins"), plus one test pinning a rate-1.0 n=1 row to the exploration arm; run
tools/gps_mcp/test_gps_mcp.py. FALSIFIER: after the floor lands, a routing decision
that cites a sub-floor row as "passes constraints and pass-rate threshold; cheapest
wins" is the fake-learning catch - the receipt line itself convicts.

## F3 (ARCHITECTURE + NORMS): the perimeter specifies identity pinning but no boot path; seed-rib MCP cold join is the proved-once instrument that both fills the hole and earns its second-consumer proof. CONVERGENT (mcp_layer_status open item 4 + ractor50 missing-tools freeze + CARD silence).

The perimeter CARD spends its architectural care on identity pinning, rate buckets,
tailnet (CARD.md:37-43) - and says nothing about how a node BOOTS into the fleet. The
estate already built that organ: tools/seed_mcp.py serves seed://current,
seed://law-registry, bounded sealed pointers capped at --max-fetch (seed_mcp.py:8-13),
and join_protocol returns a 7-step boot ladder ending "leave a receipt naming
seed_sha256 and the join outcome... the fleet can audit the join from the receipt
alone" (seed_mcp.py:204-232, steps at :210-231). It passed its falsifier once: a cold
session rebuilt a working subtree from MCP alone, 10/10 cold-join checks,
hash-verified (watch/inbox/mcp_layer_status_20261010.md:19-22). The MCP status file
names the exact open item: "a SECOND, different-client cold boot... would upgrade it
from proved-once to proved-portable" (mcp_layer_status:114-116). The perimeter's
nodes ARE that second consumer class, and the guild benches the third. Same story one
layer up: ractor50's missing-tools list (ractor50/mcp.md:214-247) froze items 2-7
behind "demand precedes organ" (mcp_layer_status:109-111) - the singing network IS
the demand event: nodes fetching law needs seed_fetch (item 3), consensus dispatch
wants estate_gps_ask/cascade wired (item 6), and the loop-closure organ already
landed (estate_receipt_append live at tools/__init__.py:65, mag/estate_bridge.py:122,
verified by grep this sitting) so a node can file its own receipts. The frozen list
unfreezes on exactly this perimeter; that is the between-generations drop: the freeze
law was written without naming what would count as the demand.

MOVE (30 min spec clause + Phase 1 amendment): write the cold-boot clause into the
spec - every perimeter node joins via seed MCP join_protocol (7 steps), never via
hand-copied env; Phase 1's 3-5 docker nodes each file a join receipt via
estate_receipt_append. That single dogfood fires the second-consumer proof and the
audit-the-join-from-the-receipt norm in one sitting. FALSIFIER: if a Phase 1 node
boots by hand-copied config files instead of join_protocol, the toggle layer is
decoration and seed MCP stays proved-once forever; if the join receipt cannot be
audited without the node's cooperation, step 7's check is false.

## F4 (MARKETS): the guild blade creates a shared-asset earnings class with no wallet law; the distribution thesis covers installs only, and silence defaults to silent mining.

The perimeter CARD's Arm 2 guild play: "the blade is the Garage Guild's first shared
asset. Benches host perimeter boxes; the guild's collective test fleet earns GSTD
doing GB's verification" (CARD.md:59-61). Whose wallet do a shared asset's rewards
flow to? The estate banked the law for INSTALLS only: "DEFAULT WALLET = THE USER'S
OWN, loud opt-in, plain disclosure... The sovereignty product cannot silently mine
for the founder" (watch/inbox/gstd_distribution_thesis_20260109.md:22-28). A guild
blade is neither the user's own seat nor the founder's - it is a third class, and no
clause covers it. The garage guild founding card repeats the exposure: "each garage
node = supply AND demand" with receipts as the only stated currency of trust
(watch/inbox/garage_wizard_network_20261010/CARD.md:33-36, 91-96). Unwritten defaults
resolve to whoever runs the setup script - which is precisely the silent-mining class
the thesis outlawed, now wearing a guild flag. This is the markets modality's lie
waiting to be caught: a collective that banks receipts for truth but not for money.

MOVE (20 min, before any guild box boots): one clause in the spec - every shared
guild asset declares a written revenue split at registration time (asset host /
guild treasury / optional project-support toggle mirroring the supporter toggle),
receipt-banked in the asset's registration row; undeclared wallet = asset does not
join the perimeter. FALSIFIER: a guild asset whose first payout lands in a wallet no
registration row names is the exact silent-mining catch; the cure is enforcement
(asset ejected), not an apology.

## F5 (NORMS + the acceptance bar, CORRECTED): the estate's consensus memory is real but STRUCTURALLY cannot express mutual consensus, and its stored rates carry a clamp that poisons a naive control; the zero-spend move is a same-path permutation control plus a task-key schema amendment.

The CARD says "the GPS capability ledger already holds the per-model half (dogfood
matrix); consensus is the new aggregation view" (CARD.md:24-25). Live census THIS
sitting: verdict_log holds 461 arena-agreement-v1 rows (the GWAP feed,
watch/inbox/build_wave_20261005/b8_gwap.md:99-103) with per-model agreement rates at
real n: claude-sonnet-5.5 0.324 at n=148, claude-opus-5.5 0.543 at n=135,
claude-haiku-4.5 0.047 at n=107, claude-fable-5.1 0.337 at n=71. But three limits,
each verified this sitting, keep that from being the warm consensus memory it looks
like. (1) NOT MUTUAL CONSENSUS: the schema is ts/model_id/task_shape/verdict/
evidence_hash/evidence_resolved/evidence_source/evidence_bytes (pragma table_info) -
there is NO task/round key, so the 461 rows are 461 distinct evidence_hash with ZERO
multi-verdict groups (census: groups with >1 verdict = 0). These are per-model
agreement-with-arena rates; the K-model agreement matrix A2 wants is UNCOMPUTABLE
from this table today - there is nothing to join on. (2) THE STORED RATES ARE
CLAMPED: the LM7 positive floor (ledger.py docstring at :359-373, "operator
positive-steering law 2026-09-30") means a fail during a rising momentum window
cannot sink pass_rate below the window-start rate; recomputing raw rates from
verdict_log: opus raw 72/135 = 0.5333 vs stored 0.5430 (+0.0097), fable raw 23/71 =
0.3239 vs stored 0.3369 (+0.0129), while sonnet 48/148 = 0.3243 and haiku 5/107 =
0.0467 match stored exactly (unclamped pairs). A control that compares raw-shuffled
against stored-measured inherits that manufactured margin as fake signal. (3) The
original move's "shuffle labels within task" was unbuildable - consequence of (1).

What survives, honestly: Phase 1 still has a zero-spend first falsifier, but it is a
FLAT permutation control on the same path - recompute RAW rates from verdict_log,
shuffle verdict labels across the whole arena-agreement-v1 population per model,
compare raw-measured to raw-shuffled (both arms raw, or both arms replayed through
record_verdict; never mixed). And the schema amendment becomes part of the finding:
the perimeter harness's consensus rows need a task_id/round key from row one, or A2's
agreement matrix is uncomputable FOREVER, exactly as it is today. The unisub tie
survives weakened: the garage measures behavioral convergence where the paper
measured spectral (CARD.md:22-25; unisub CARD.md:44-49) - but the estate's fossil
record is per-model-only until the key lands.

MOVE (60-90 min, $0): (a) a same-path permutation script over verdict_log - raw
recompute, B shuffles per model, empirical p per model, receipt to watch/inbox/;
(b) one-line schema amendment in the harness spec: every consensus verdict row
carries task_id (the join key the arena never had). FALSIFIER: (a) if a model's raw
agreement rate does not beat its own shuffled null (sonnet 0.3243 vs null ~0.33),
the arena signal was dead salmon and A2's bar rises before the perimeter spends;
(b) if after the task_id lands, replaying the same rows through record_verdict
changes ANY unclamped model's stored rate, the two arms diverge by more than the
clamp margin, and the control design - not the signal - is what broke.

## What is decoration (no sacred cows)

The vast.ai price sizing (CARD.md:44-48) is estimate-class by its own admission and
is fine as sizing; it would be decoration only if a phase gate keyed on it. The
truth bar the design must not decorate: A1b (chain-read), the n-floor, the join
receipt, the declared wallet, the shuffled baseline. Those five are the difference
between a network that learns and a network that performs learning.

## Blind spots (honest)

- GB's staging platform behavior is UNOBSERVABLE to me: whether staging settles
  on-chain (testnet) or on a D1 counter is the single fact F1's A1b hinges on, and
  only GB can answer it. I banked it as the question, not a guess.
- The perimeter harness does not exist on disk yet; all Phase 1 claims are plan
  review, not test runs. My ledger/router/contract checks are real runs; the
  harness's future behavior is unfalsified by construction.
- My census ran only the capability and verdict_log tables of gps_ledger.db3 and the
  two named greps over reference/gstdcoin; I did not audit the full gstdbot codebase
  or TON testnet state.
- I did not reread every prior ractor dir (ractor_engine has 25+); I worked from the
  ask's named primary sources plus the gps_mcp and seed_mcp organs. Prior lenses of
  THIS wave (siblings in 2026-10-10-singing-network) were not on disk when I wrote,
  so no cross-lens dedup was possible from their bytes.
- vast.ai pricing (dynamically loaded page) not re-fetched; the CARD's
  estimate-class marking stands as-is.

## Checks run this sitting (instrument, moment 2026-10-10)

1. grep census: verifyQuorum|SettleTaskWithProof in reference/gstdcoin/contracts/ -
   zero hit lines; referenced in gstdbot/src at attestation.ts:3,:34,:80,
   agent.ts:694, node.ts:128 (bash grep, this sitting).
2. SettlementMaster.tact receive/message surface grep - SettleTask at :128, no
   WithProof receiver.
3. .venv/Scripts/python.exe sqlite census of tools/gps_mcp/gps_ledger.db3:
   capability 34 rows, 12 at n<=2, 6 at rate 1.0 n<=2; verdict_log 461
   arena-agreement-v1 rows.
4. Code reads: router.py:40,:106,:252-253,:341; gps_router_v0.py:237,:261;
   seed_mcp.py:204-232; tools/__init__.py:65; mag/estate_bridge.py:122.
5. Doc reads: all 13 primary sources named in the ask (CARDs, mcp doctrine, seed
   format, tokenomics audit, router vocab, distribution thesis, living-weights rib,
   state/CURRENT.md).

Second-pass re-verification (same sitting, post-verdict):
6. grep min_support ROUTER_VOCAB_LANDED.md - exactly one hit at :18.
7. git log --follow router.py (first: 91acc5bdf 2026-09-29) vs gps_router_v0.py
   (first: 9bac820a1 2026-10-07); git log -S min_support -- router.py = zero commits.
8. pragma table_info(verdict_log): no task key; arena rows 461, distinct
   evidence_hash 461, groups with >1 verdict = 0.
9. Raw recompute: opus 72/135=0.5333 (stored 0.5430, +0.0097), fable 23/71=0.3239
   (stored 0.3369, +0.0129), sonnet 48/148 and haiku 5/107 match stored exactly;
   LM7 docstring read at ledger.py:359-373.
