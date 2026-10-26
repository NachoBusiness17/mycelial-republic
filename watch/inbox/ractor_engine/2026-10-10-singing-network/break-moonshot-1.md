# BREAK PASS: moonshot-1 (hostile second pass, 2026-10-10)

Seat: break-moonshot-1. Job: byte-check every evidence cite of the moonshot-1 lens
report against the estate, attack the falsifiers, name what it missed. No file edits
outside this receipt.

Instruments run this sitting (all commands executed from repo root):
- Read: gstd_perimeter_design_20261010/CARD.md, gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md,
  gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md, token.ts, SettlementMaster.tact,
  gateway/server.ts, revenue/engine.ts, router.py, ledger.py, metabolism.py,
  unisub_drop_20261010/CARD.md, garage_wizard_network_20261010/CARD.md,
  gstd_distribution_thesis_20260109.md, ARENA_GWAP_BACKLOG_R3_20261010.md.
- Filesystem grep `grep -rn -i -E "verifyQuorum|SettleTaskWithProof" reference/gstdcoin/contracts/
  reference/gstdcoin/gstdbot/src/` (git grep is INVALID over this tree, see trap below).
- `.venv/Scripts/python.exe -c` provider recount over tools/gps_mcp/config.gstd.json.
- `.venv/Scripts/python.exe -c` executing tools.gps_mcp.router.family_of over the 14 real ids.
- `ls tools/gps_mcp/`, `ls tools/ | grep`, `grep -rln consensus tools/` (organ census).
- NOT RUN (impossible this sitting, honest): any live TON testnet call. No staging endpoint
  exists (CARD.md:56-58 UNOBSERVABLE until GB confirms) and no resolve_claimed_tx tool exists
  on disk, so there is no claimed txHash to resolve.

## Verdict 1: A1 passes on theatrical settlement. CONFIRMED

Every cite byte-checks:
- CARD.md:13-14: A1 claims "closes our audit's settlement-theater finding on a staging rail".
  Exact bytes confirmed.
- token.ts:387-403: recordEarning builds `hash: 'tx_' + randomBytes(16).toString('hex')`,
  `status: 'confirmed'`, unshifts into a local list capped at 1000. Confirmed by direct read;
  the lens's line range is exact.
- SettlementMaster.tact:128-135: SettleTask gates only sender (owner/gateway, :129) and
  replay (taskId, :133-135); workerAddr/computeUnits/qualityScore ride as trusted message
  fields. Confirmed by direct read.
- Phantom-method grep re-derived a THIRD time, correct instrument: filesystem grep returns
  6 node-side reference hits (p2p/attestation.ts:3,34,80; p2p/identity.ts:11; p2p/node.ts:128;
  swarm/agent.ts:694) and ZERO hits inside reference/gstdcoin/contracts/. The lens's
  "ZERO hits in contracts" survives; CONVERGENT with GSTD_TOKENOMICS_AUDIT.md:49-54, now
  triple-derived (audit 2026-10-09, lens grep, this pass grep).
- The two cites the lens deferred to the audit are now closed first-hand:
  gateway/server.ts:3304 fabricates claim txHash `'tx_' + sha256(address+Date.now())`
  (audit said :3305; the line is 3304, off-by-one, content exact) and revenue/engine.ts:15
  header promises "Settled on-chain via SettlementRouter.tact (real GSTD transfer)".
- Logic holds: A1 as worded ("balance/ledger delta lands as claimed") asserts against the
  node-side ledger, which is the fabricated local list by construction, so A1 passes on
  theater. The theater-catcher (chain resolution of every claimed txHash) is the right fix.

Blind spots verified honest: no live TON probe was possible (no endpoint, no harness);
vast pricing and staging rate limits remain estimate-class/UNOBSERVABLE per CARD.md:7-9, 56-58.

## Verdict 2: "K DIFFERENT models" is ~2 base-weight lineages (family echo). CONFIRMED

- Recount executed: `.venv/Scripts/python.exe -c` over config.gstd.json reads total=20
  providers, test_double=false = 14. Exact match to the lens.
- Lineage split confirmed against ROUTER_VOCAB_LANDED.md rows: qwen-derived 7 (rows 1-5
  incl. qwen-desk row 4 "same family + arch", plus deepseek-r1:1.5b row 7 "qwen2 arch r1
  distill"), gemma-derived 6 (rows 8-12 plus athena-class row 13 "gemma4, 30.7B"), ternary
  experiment 1 (row 14, "zero verdicts anywhere"). 13 of 14 real models on 2 base lineages.
- unisub qualifier confirmed at unisub_drop_20261010/CARD.md:13-15: convergence claimed
  "within shared architectures", their own qualifier.
- Duel law confirmed at router.py:766-841: cross-family challenger (:799-807), third-family
  blind judge (:813-825), gap named not papered (:785-789, :808-812).
- family_of confirmed prefix-based at router.py:618-620.
- The lens UNDERSTATED the bug; see Addition A1 below (executed check: the cross-family
  test is vacuous over the entire local garden today, every model its own singleton family).
  This strengthens the finding, and the card's A2 (CARD.md:15) indeed never names lineage
  partitioning; the dead-salmon control at CARD.md:19-20 is in the card but lineage is not.

## Verdict 3: data organ exists, no behavior-change organ. CONFIRMED

- ledger.py:623-633 confirmed: momentum badges earned from verdict windows, "badges are
  earned, never declared".
- router.py:40 confirmed: DEFAULT_PASS_RATE_THRESHOLD = 0.85; router.py:336-344 confirmed:
  qualifying = passes_threshold, cheapest wins, momentum reasons appended.
- router.py:16-20 and ReceiptLog router.py:201-223 confirmed: append-only receipt on every
  decision ("A decision we cannot audit did not happen").
- CARD.md:79-80 confirmed: aggregator feeds the ledger as consensus-contrib rows.
- Organ census executed: `ls tools/gps_mcp/` shows coverage.py, gps_embed*.py, metabolism.py,
  ledger.py, providers.py, receipts.jsonl, router.py, seed_fixtures.py, server.py,
  test_gps_mcp.py. No learning/diff/flip organ. Hostile challenge run against the nearest
  candidate, metabolism.py: it is read-only effective-rate computation (alpha-decay,
  dispute-streak slashing, drift-patrol-keyed epoch reset, metabolism.py:1-26); it adjusts
  how rates are READ and emits no route-flip measurement. The challenge fails to kill the
  finding; nothing measures which route choices flipped.
- `grep -rln consensus tools/ --include=*.py` hits only unrelated files (behavior_cards_x,
  gauntlet_feed, gauntlet_grade, overmind_judge, reverse_map); the lens's blind spot
  "consensus harness v0 does not exist on disk" is confirmed: no dispatcher-K-compare
  organ anywhere in tools/.

## Verdict 4: divergence as product feeding GWAP adjudication. WEAKENED

Organ cites all byte-check:
- ARENA_GWAP_BACKLOG_R3_20261010.md line 1 confirmed: "census reads dirs=110 banked=110
  unbanked=0 AS-OF 2026-10-10T13:09:59Z" plus raw-check pointer. tools/arena_gwap.py exists.
- ledger.py:310 confirmed: record_verdict is the evidence-gated write path
  (evidence_hash/evidence_path/evidence_bytes).
- gstd_distribution_thesis_20260109.md:21-32 confirmed verbatim: default wallet the user's
  own, supporter toggle default OFF, "our software is the on-ramp, not the tenant".
- CARD.md:18 confirmed: "divergence cases banked as receipts" (passive banking, as charged).
- Audit cites confirmed: ~1.53 GSTD/day and "demand is" the constraint (:82-84), 2-10x net
  emission subsidy per task (:91-94), cold demand the named failure (:109-111).
- Cite drift (minor): percolator novelty ranking is named at garage_wizard_network_20260110/
  CARD.md:82; the lens cited :92-94, which is the adjacent fox-counters block (receipt-weighted
  ranking). Content real, line off by ten.

Why weakened, one leg broken against its own evidence: the "closes GB's demand gap" leg
contradicts the audit it cites. Audit :109-111 names COLD (external) demand as the failure
and states our dogfood was already "the platform's biggest demand event"; internally
generated consensus-sweep tasks are the same self-play class (and per :91-94 each task is a
2-10x net emission subsidy, so more internal tasks deepens the subsidy leak unless priced
differently). The graded-fixture leg is not merely intact, it is STRONGER than the lens
showed: ROUTER_VOCAB_LANDED.md:25-30 documents the starvation directly ("nothing anywhere
passes the 0.85 threshold, and the shapes summarize/classify/extract had NO history").
Also noted: the finding statement arrived in the report under review truncated mid-sentence
("...closes GB's demand gap by c"); this verdict covers the checkable core. Fix the claim,
keep the organ: divergence cases to GWAP adjudication as ledger fixtures stands; strike or
re-scope the demand-gap closing to "internal demand for the perimeter's own task bank",
which is real but is not GB's cold-demand cure.

## Additions (what the lens missed)

A1. The duel layer's cross-family law is VACUOUS over the entire local garden, not just
qwen-desk. Executed this sitting: family_of over the 14 real config.gstd.json model ids
returns 14 DISTINCT families, because every ollama id is slash-less so
`model_id.split("/", 1)[0]` returns the whole id (router.py:618-620). Today a duel between
qwen2.5:3b-instruct and qwen2.5:7b PASSES the cross-family check at router.py:800.
Falsifier: if the duel ledger's model_ids carry provider prefixes (e.g. "ollama/qwen2.5:3b")
the singleton effect disappears; I ran family_of on the exact config strings and they are
slash-less, so it stands until a lineage key lands. Move: the lens's lineage-key fix is
promoted from a consensus-aggregator nicety to a live duel-layer bug fix; same one sitting,
+15 min over the lens's move.

A2. Instrument law for the gstdcoin tree: reference/gstdcoin/ is gitignored (.gitignore:169;
`git ls-files reference/gstdcoin/` returns 0 tracked files), so git grep over it silently
returns zero for everything. Demonstrated: `git grep -n -i -E "verifyQuorum|SettleTaskWithProof"
-- reference/gstdcoin/` exited 1 (zero hits) while the same pattern via filesystem grep
returned 6 node-side hits. Anyone re-verifying A1 evidence or the audit with git grep will
"prove" the phantom-method references do not exist. Falsifier: if the tree becomes tracked,
git grep goes valid again. Move: 5 min, name the instrument in the perimeter harness readme
and use filesystem grep (grep/findstr) in all A1 tooling.

A3. A1's asset ambiguity: the card's wording "balance/ledger delta" (CARD.md:13) never names
WHICH balance, and the node-side ledger is theater by construction (token.ts:387-403) while
the live counter is platform D1 (audit :17-19). The lens's resolve_claimed_tx.py catches
fabricated hashes but a REAL hash of a zero-value transaction would pass hash-resolution
while paying nothing. The assert needs the on-chain jetton/TON balance delta at the worker
address around the claim, not just hash existence. Falsifier: if one staged zero-value tx
with a valid hash already fails the lens's proposed assert, the hash leg covers the balance
leg; test with exactly that fixture. Move: +10 lines to the proposed harness (balance
before/after the claim, compare against the claimed delta).

A4. learning_diff should key on the estate's existing epoch organ, not invent a second era
axis: metabolism.py already defines drift-patrol-keyed measurement eras with an explicit
reset act (metabolism.py:18-22, EPOCH_PATH metabolism_epoch.json beside the ledger), and the
raw flip material (tools/gps_mcp/receipts.jsonl) is already on disk (ls this sitting). The
lens's learning_diff.py should report route flips ACROSS epoch markers, so a flip caused by
an epoch reset (tainted-era collapse) is not miscounted as the network "learning".
Falsifier: if flips binned across epoch markers are always identical to flips across raw
time, epoch keying adds nothing and can be dropped. Move: 15 min, learning_diff joins
metabolism_epoch.json markers when binning.

## Blind-spot ledger (lens claims re-verified this sitting)

- No live TON testnet call: confirmed not run and not runnable (no endpoint, no harness).
- server.ts:3305 / engine.ts:15 deferred to audit: both now closed first-hand (gateway/
  server.ts:3304, revenue/engine.ts:15), off-by-one on the server.ts line, content exact.
- vast.ai pricing estimate-class: confirmed as card's own qualifier (CARD.md:7-9).
- Consensus harness v0 absent from disk: confirmed by tools/ census (no organ file).
- tools/arena_gwap.py named but unopened: existence confirmed; the 110/110 claim verified
  at its receipt line 1 with an AS-OF moment stamp and a raw-check pointer.

## Score

4 findings: 3 confirmed (1, 2, 3), 1 weakened (4, demand leg contradicts its own audit
evidence, fixture leg stronger than shown). 0 killed. 4 additions banked, two of them
executed checks (A1 family vacuity, A2 git-grep trap), two cheap design sharpeners (A3, A4).
The lens's evidence hygiene was strong: 20 of 21 line cites byte-exact, one off-by-ten
(garage percolator), one off-by-one (server.ts), zero fabricated cites.
