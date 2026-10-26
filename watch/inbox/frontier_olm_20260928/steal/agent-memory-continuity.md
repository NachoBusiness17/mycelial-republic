# steal card: agent-memory-continuity (round 2, 2026-09-29)

Seat: steal-agent-memory-continuity. Round 2 supersedes the round-1 card at this path.
Round-1 sealed bytes are preserved: two autoseals one minute apart, 14,244 bytes sha256
4a65bc67b87e8316a0956f407f8710a500baeadafb15f870b76b69ae03f4dcfb
(watch/inbox/index_events.jsonl:6403-6404, 11:40:46Z) then 14,366 bytes sha256
55e2dd451f45cd7c516348760454cdc1a0330a3c4c1d6ecb62407678fcf74063
(index_events.jsonl:6407-6408, 11:41:23Z; hash re-verified by sha256sum this ask before
overwrite; working copy kept at %TEMP%\amc_round1_sealed.md). The round-1 in-file scan
receipt claimed "14,244 chars at scan time" while the sealed file was 14,366 bytes: real
defect, cause was ~122 receipt bytes appended after the scan. Round-2 rule: this file is
scanned once, after its last edit, and never edited again; the sealed-byte sha256, char
count and dash/non-ASCII counts live in the round-2 StealCard JSON, not in this file, so
no in-file claim can drift from sealed bytes.

Auditor verdict on round 1 (recorded): provenance real, primary attack REPRODUCED by the
auditor under their own hands (A1 content forgery -> (True, 'chain consistent (8362
leaves)'), A2 deletion forge -> (True, 'chain consistent (8361 leaves)'), victim row
4,181 memlang-three-layers-06431932498 in the len//2 slot, chain grown 8,358 -> 8,362
since my run). Four defects blocked approval; all four are fixed in this round, each
with fresh byte evidence. Auditor re-bank audit, recorded verbatim in substance: S1 not
re-banked (new measured fact, reproduced); S2 PARTIALLY re-banked by its own admission
(workflow gate + G-cards + ratchet already exist; the new content is only the RIB
acceptance rule); S3 not re-banked (biography.py is summarization; no memory-hygiene
eval exists anywhere grepped); S4 not re-banked (nothing witnesses the head outside the
writer; warm boot only READS the tip, mag/hermes_warm_boot.py:39-54; the bridge's
estate_chain_verify wraps the same Python, so an independent-language verifier is
genuinely new).

Inputs: the same 4 confirmed finds from the frontier OLM sweep (parent method per the
ask: export.arxiv.org Atom API 6 queries, arxiv.org/abs 7 fetches, arxiv.org/html 5
full texts, plus the estate's daily mirror state/arxiv/2026-*/digest.jsonl 3,941
in-window rows; find 4 from HN). Everything below is (a) quoted from the ask's finds,
(b) verified against estate bytes with path:line citations, or (c) run live with the
exact command and output. Unverifiable items are marked OWED. No fabrication. No em/en
dashes. All probe work on temp copies; live chain and live dbs read only.

---

## S1 (PRIMARY) LLM agents tamper with their own traces -> chain writes must sit outside the seat

- Find: "LLM Agents Can Easily Tamper With Their Own Traces", arXiv 2609.30266
  (2026-09-24), confidence 0.95. Quote verbatim, byte-verified against the estate's
  own mirror pull: "We advise practitioners to ensure trace logging happens through an
  independent interception mechanism outside of the agent's control, preserving trace
  integrity even in cases of full host compromise." state/arxiv/2026-09-25/2609.30266v1.txt:6.

### CORRECTED (round-2 defect 1): the broker has an effect SLOT, not a chain writer

Round 1 claimed "a broker-side write path already exists but is opt-in". Wrong. The
measured truth:

- mag/effect_broker.py:234-251 `_broker_verkle_link` shells out to
  `python -m mag.verkle_lance link --event <id>` (:236).
- mag/verkle_lance.py is a READ-ONLY temporal mapper over the chain, verified this ask
  by reading the entire 457-line file: its only filesystem operations are reads
  (`_read_json` :54-58, `_load_chain` :61-77 reading CHAIN at :66); `link(event)`
  (:148-190) matches an event to a knot and RETURNS knot metadata plus the root at
  that point; there is no write_text, write_bytes, os.open-with-write or subprocess
  anywhere in the file. The authority/budget/receipt wiring around the slot is real
  (effect_broker.py:205-219, :369-434), but behind it there is no chain writer.
- Therefore the port is NEW writer code: a broker-side effect that performs the
  append (the paper's independent interception mechanism), not a flag flip. The slot
  shape, gate and receipt chain are the reusable parts.

Separation requirement (also round-2): broker-in-the-same-process-tree does NOT meet
the paper's bar, because the bar is "outside of the agent's control, even in cases of
full host compromise", and any in-tree code can call mag.verkle_knot directly - this
card's probe did exactly that (imported the module, pointed its globals at copies,
forged). If the interception writer runs inside the seat's process tree, the seat can
bypass or impersonate it, so the guarantee is procedural, not mechanical. The broker
writer must be a distinct principal: separate OS process at minimum, and the honest
endgame is a separate service account or remote loopback service (the estate's gateway
pattern, mag/mcp_http.py on 127.0.0.1) holding the only write path.

### Measured attack surface (three independent reproductions)

The chain gate cannot see forgery by anyone holding the writer's code, which per the
paper's threat model is the agent itself:

- Gate mechanics: `_verify_chain_consistent` (mag/verkle_knot.py:536-556) recomputes
  the merkle root from the STORED `leaf_hash` strings (:544) and checks only the last
  row's root and the tip (:548-553). Leaf hashes are derived only at leaf-build time
  (:303) and inside prove() when the caller passes the leaf object (:458); the gate
  never re-derives content -> hash. Rows carry a POINTER (`filename`) plus derived
  fields, not leaf content (measured 17-key row set below).
- Reproduction ledger, all on temp copies, live files untouched:
  1. My round-1 run-2 (chain at 8,358 rows): A1 content edit (row 1 session
     mag-agent-orc-te7d866161c, note -> " TAMPERED", stale hashes) ->
     (True, 'chain consistent (8358 leaves)'); A2 deletion forge (deleted row 4,179
     memlang-deep-scifi-invariants-06, recomputed every committed root with the
     writer's own functions exactly as tools/chain_repair.py:62-72 does, refreshed
     tip) -> (True, 'chain consistent (8357 leaves)').
  2. Auditor reproduction (chain at 8,362 rows): A1 -> (True, '...(8362 leaves)');
     A2 -> (True, '...(8361 leaves)'), victim row 4,181
     memlang-three-layers-06431932498.
  3. My round-2 run, 2026-09-29T12:09:42Z to 12:13:00Z, chain at 8,370 rows at run
     time (wc -l receipt this ask): A1 -> (True, 'chain consistent (8370 leaves)');
     A2 deleted row 4,185 memlang-attractor_tools-06453083, 8,369 rows remain ->
     (True, 'chain consistent (8369 leaves)'). Command:
     `.venv\Scripts\python.exe -u -X utf8 %TEMP%\steal_amc_probe.py` (runs 1-2 plus
     this re-run; script on file). The chain is live and growing, so all probe numbers
     are pinned to their run moment, never compared across moments.
- Measured 17-key row shape (printed by the probe, row 1): amended, dominant_theme,
  dossier_commit, end_minute, evidence_lost, filename, index, leaf_hash, n_leaves,
  note, parent_verkle_root, session_id, start_minute, tension_index,
  theme_vector_normalized, ts, verkle_root.
- Byproduct (unchanged from round 1, confirmed by the auditor):
  `find_bad_tail_index` (tools/chain_repair.py:39-46) is quadratic (per-row
  `_merkle_root` over a growing prefix); measured stall over 45 s on 8,358 rows,
  faulthandler stack chain_repair.py:44 inside verkle_knot.py:156 `_merkle_root`.
  Note mag/verkle_knot.py:82-84 records that `_rewrite_chain` already uses an
  incremental O(n log n) prefix-root calculation, so the fix is to reuse that path in
  the repair verb.

### CORRECTED (round-2 defect 2): verify-time re-derivation needs a knot-file policy or it freezes the loop

Round 1 said "harden the gate to re-derive leaf hashes from row content". As stated,
unworkable: the row stores a pointer (`filename`) plus derived fields; `leaf_hash` is
computed from the knot-file leaf object at build time (verkle_knot.py:303), so
verify-time re-derivation means loading each row's knot file. The estate's own
forensics block records why that cannot be a hard gate: "1,044 chain rows referenced
knot files that no longer existed" (mag/verkle_knot.py:71; cause :72-74, amend unlinks
the old knot file then rewrites the whole chain and a concurrent append clobbered the
rewrite, which is why the single-writer lock exists at :89-100). A strict re-derivation
gate would fail-closed every append on those 1,044 historical knot-less rows and
freeze the biography loop.

Policy the port must state (proposal, choice is an operator call):
- Rows WITH a live knot file: gate re-derives leaf_hash from the knot leaf before any
  extension; mismatch = refuse to extend (the existing "never build on a lie" intent,
  verkle_knot.py:537-540).
- Rows WITHOUT a knot file (the 1,044): the gate accepts the stored hash and SAYS SO -
  a documented trust boundary carried as a row field (for example hash_basis: "stored"
  vs "rederived"), so verification is honest about where it is weak instead of
  silently passing or failing closed.
- Writers that migrate behind the broker writer: the census this ask found 48 files
  referencing `append_verkle_knot` (grep -rln over mag/ tools/ main.py; command and
  count in Provenance; definition at mag/verkle_knot.py:813), including agent_knot,
  agent_os_loop, breakthrough_loop, castle_foundation, chord_circuit, doctor_rightsize,
  fact_bus, feedback, ghost. Warm boot is NOT a writer (verified read-only:
  mag/hermes_warm_boot.py:39-54 reads the last chain line only; CHAIN constant :30).
  Migration is phased: broker writer first, appenders re-pointed one organ at a time.
- Broker-down policy: fail-closed = no trace written while the broker is down. That is
  the paper's own recommendation taken literally (no trace is better than tamperable
  trace), but it trades continuity for integrity and must be stated as a chosen cost;
  a local spool-and-forward buffer is the alternative and reintroduces a seat-side
  tamper window, so if adopted it must be flagged as such in the design doc.

## S2 doctrine compiles to enforceable artifacts (with negative tests) or it is prose

- Find: arXiv 2609.24036 (2026-09-21), confidence 0.95; quote from the ask: "a 50.3%
  end-to-end policy correctness rate, compared with 15.3% for the baseline"; method
  per the ask: detection, extraction, schema validation, linting, positive AND
  negative tests.
- Estate landing: the percolator / law mill. Existing compiler-shaped parts verified:
  workflow gate check (tools/workflow_gate.py), seven scenario cards G1-G7 plus
  fixtures (configs/workflow_gate_scenarios/, listed round 1), ratchet debt-by-name
  (AGENTS.md build discipline). memory/rib/ is prose-only (.md files; round-1 ls), so
  the implements-edge gap is real.
- Auditor re-bank note, accepted: round 1 was PARTIALLY re-banked - the gate, cards
  and ratchet already exist; the genuinely new content is only the RIB acceptance
  rule: a RIB lands in memory/rib/ only with (1) its compiled checker module, (2) one
  positive and one negative scenario card in the G-card grammar, (3) a registry row.
- Probe precondition added (auditor): the 5 ladder-02 operator corrections
  (11:50 / 15:11 / 16:27 / 16:34 / 18:58, per the ladder-02 commit message) must first
  exist as machine-readable artifacts - commit-message timestamps are not compilable
  inputs. Step 1 of the probe is minting 5 structured correction rows (what, artifact
  path, evidence pointer), THEN compiling each into a gate check and testing
  fired-on-violating-artifact plus silent-on-20-clean-controls. Falsifier: fewer than
  4/5 fire, or any false fire on controls, and the law stays human-gated prose.

## S3 memory hygiene is scored by hidden executable oracles, not judges

- Find: DreamBench-SWE, arXiv 2608.20664 (2026-08-21), confidence 0.95; quote from the
  ask: "later software tasks depend on non-inferable evidence from earlier sessions
  and are scored by executable hidden oracles"; anti-summarization datapoint: verbatim
  event memory 82/180 vs no-memory 21/180.
- Estate landing: context pack + biography organs (mag/organ_map.py:81-90,
  :91-101). Substrate: corpus/oral_history/, fingerprint sha256:25871258ba12, 3,872
  files / 270M, PRIVACY LAW ENFORCED header (structure, paths, dates only;
  research/corpus_triangulation/R4_oral_history.md:2).
- Census (measured, this ask and round 1, identical): the two conversation-blobs.db
  stores expose one table each (`blobs`); counts 1,232 (part3) + 13,522 (part5) =
  14,754 rows, read-only URI mode, counts only. OWED stands: the ask said 14,858; the
  104-row gap is unreconciled (may sit in part4/6/7 store.db or uncheckpointed WAL;
  not counted, not asserted).
- Auditor re-bank note, accepted: S3 is NOT re-banked - biography.py is
  summarization; no memory-hygiene eval exists anywhere. The port is a new harness.
- Design honesty added (auditor): non-inferability is a CONSTRUCTION-TIME property
  with no operational test in this design - the oracle author asserts the answer is
  absent from all summaries/pointers, and that assertion is human-adjudicated at
  build time. It is not verified at eval runtime. Stated as a known limit; a runtime
  non-inferability re-check is future work, not a claim of this card.
- Probe (named, not run): 20 structure-only oracles (paths, dates, row ids; privacy
  law respected), three conditions (no-memory, context-pack summary memory, verbatim
  row-pointer memory), n=20 tasks. Falsifier: if verbatim pointers do not clearly beat
  no-memory (paper: 45.6% vs 11.7%), the anti-summarization law does not transfer and
  the biography stays summarized.

## S4 Kepil: witness the chain head outside the writer; verify in another language

- Find: github.com/oleg-vdv/kepil, confidence 0.92 (HN). Quote from the ask: "Proof
  that only its own author can check is not proof." All five README claims re-verified
  live via WebFetch in round 1 and by the auditor: hash-chained append-only JSONL;
  content-blind rows ("Values never enter the journal - only types, counts and
  hashes"); head witness leaves the writer ("the card now carries the current chain
  head", "the one artifact produced outside the writer"); independent verifier ("The
  verifier is a separate implementation in another language", npm
  proofbyte-agent-trace verify); honest limit verbatim: "Records written after the
  last witnessed head stay unprotected. That is where the guarantee stops, and it
  says so."
- CORRECTED (round-2 defect 3a): round 1 claimed estate rows "already lean this way"
  content-blind. Contradicted by the measured 17-key row set (listed in S1): rows
  carry dominant_theme, note, tension_index, theme_vector_normalized, evidence_lost.
  Content-blindness is entirely UNDONE in the estate chain, not partially done. The
  graft therefore means stripping or hashing those fields on any EXTERNAL surface
  (bridge rows), not claiming an existing property.
- CORRECTED (round-2 defect 3b): witness scope. A same-host witness (a scheduled task
  copying the tip root to another local file) does NOT meet the paper's
  full-host-compromise threat model: the same compromised seat rewrites both files.
  What it DOES catch: writer-bug forgery and the A2 deletion-forge shape from a
  non-compromised-but-buggy writer (the 09-27 race class), which is worth having and
  is the cheap first step. For the paper's bar the witness must leave the machine;
  candidate mechanisms, named as design options, none wired today: remote push to a
  store the estate already operates (the Vercel deploy surface exists as a constant,
  mag/hermes_warm_boot.py:31, but witness push is not built), a second seat's
  ack channel, or the bridge loopback service holding an append-only witness file.
- Graft 3 with owner named (auditor): independent verifier in another language.
  Proposal: TypeScript, mirroring Kepil's own npm-verifier precedent
  (proofbyte-agent-trace), reading verkle_chain.jsonl + the witness and implementing
  the S1 gate rules including the knot-less-row policy; location tools/verifier-ts/;
  maintenance owner: the seat that lands it, registered as a new organ_map entry so
  the GHOST-to-VERIFIED ladder applies. Marked as a proposal; nothing exists yet.
  The estate's current "verifier" surfaces all wrap the same Python (mcp-bridge
  estate_chain_verify wraps tools/chain_repair repair(dry=True),
  watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md:128-140), so this graft is
  genuinely new (auditor confirmed).
- Probe (named; extends the three green forgeries): write today's tip root to an
  out-of-band witness, reproduce the A2 forge, show a witness-comparing verifier
  FAILS it. Falsifier: the witness verifier passing the A2 forge. Honest limit to
  adopt verbatim, Kepil-style: records appended after the last witness stay
  unprotected; the witness cadence IS the guarantee window.

## Estate map (organs fed)

| Steal | Organ | Concrete port |
|---|---|---|
| S1 trace tampering | verkle knot + effect broker (+ mcp-bridge R1) | NEW broker-side chain writer effect (slot exists, writer does not) as a distinct principal; verify gate re-derives where knot files live, documents stored-hash basis where they do not; repair stays seat-internal |
| S2 law-to-module | percolator / law mill (+ workflow gate) | RIB acceptance rule: compiled checker + positive/negative G-card + registry row; corrections minted as machine-readable rows first |
| S3 hidden oracles | context pack + biography / context checkpoint | new memory-hygiene harness: non-inferability at construction (stated build-time limit), executable oracles, 3 memory conditions on corpus/oral_history |
| S4 Kepil grafts | verkle knot + manifest | off-machine head witness (option named), content-blind EXTERNAL rows (estate rows are not content-blind), independent TypeScript verifier with named owner |

## Provenance

- Reads this ask: mag/verkle_lance.py full 457-line read (read-only verdict);
  mag/verkle_knot.py:57-106 (session_pointer_v2, the 1,044-row forensic :71, cause
  :72-74, incremental prefix-root note :82-84, lock :89-100);
  mag/hermes_warm_boot.py:30-54 (read-only tip read); watch/inbox/index_events.jsonl
  :6400-6408 (seal records); round-1 citations unchanged and re-checked where the
  auditor contested them (all landed).
- Commands run this ask (exact): `grep -rn "append_verkle_knot" mag/ tools/ main.py
  --include="*.py"` (writer call sites; `grep -rln ... | wc -l` = 48 files);
  `wc -l memory/biography/verkle_chain.jsonl` = 8,370;
  `sha256sum watch/inbox/frontier_olm_20260928/steal/agent-memory-continuity.md` =
  55e2dd45...f74063 (round-1 sealed bytes, verified before overwrite);
  `date -u` bracketed probe run 12:09:42Z / 12:13:00Z; probe re-run
  `.venv\Scripts\python.exe -u -X utf8 C:\Users\foste\AppData\Local\Temp\steal_amc_probe.py`
  with outputs quoted in S1.
- Reproductions of this card's S3 count: 1,232 + 13,522 = 14,754 (round 1 by me,
  round 2 by the auditor, exact match).
- OWED (unchanged plus new): the 14,858 figure (measured 14,754 across part3+part5
  blobs); DreamBench-SWE and the Rego paper read only via the ask's finds; the
  knot-less-row policy options are proposals pending operator choice; the TypeScript
  verifier and off-machine witness are unwired proposals; find_bad_tail_index cost
  benchmarked only by the observed 45 s stall + stack, not a benchmark harness.
- Seal: this file is scanned once after its final edit and never edited again; the
  sealed-byte sha256, char count and em/en-dash and non-ASCII counts are recorded in
  the round-2 StealCard JSON accompanying this card (not in this file, per the
  round-2 rule at the top).
