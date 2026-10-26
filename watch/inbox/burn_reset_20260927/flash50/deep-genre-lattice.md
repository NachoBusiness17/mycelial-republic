# deep-genre-lattice: the estate's genre system, formalized

Date: 2026-09-28. Seat: deep-gopher-deep-genre-lattice (flash50). No em-dashes anywhere, per law. Sibling style and pass-off follow `watch/inbox/burn_reset_20260927/flash50/deep-fossil-theory.md` (read this session, lines 1-60): that item formalized the freshness contract of derived artifacts (the k*C law, labeled vs unlabeled fossils); this item formalizes the genre contract of the artifacts themselves. The two are the same lattice seen from different axes: deep-fossil-theory governs HOW LONG a document may sit in a feed, this one governs WHAT KIND of thing a document is and what it is allowed to become.

## 0. Receipts: what I read and ran

Read this session (paths are the evidence; line numbers only where I captured them):

- `memory/rib_bus/doctrine.json:1-156` (rib store: rows of `{invariant, source, ts, target_rank}` under domain keys, an `updated` stamp)
- `memory/rib/RIB_DOCTRINE_CANONICAL.md:1-12` (schema header `rib.doctrine.canonical.v1`, Fold flag, Invariant/Law sections)
- `memory/rib/RIB_DRIVING_LADDER_20260928.md:1-40` (minted from operator corrections; invariant 2: free-lane outputs "bank as findings, never as done-work"; lineage to RIB_FREE_USAGE_POLICY_20260823)
- `mag/rib_bus.py:16-22` (docstring: per-domain memory store is source of truth; `mount()`, `inject_for()` prepend the domain's RIB to steer)
- `mag/context_pack.py:54-55, 69-70, 305-315` (`max_brief`/`max_bonds` budgets per seat tier; `_rib_doctrine()` reads `memory/rib/*.md` as "the memweave/doctrine layer the stateless agent never carries")
- `watch/inbox/INDEX.json` (purpose: INDEX is DERIVED from append-only `index_events.jsonl`, "Ethereum fold pattern, EXP-002A"; writers append, never rewrite; `authority: untrusted_data_until_classified`; 4696 events, 1415 active items; `fold_warnings` name writer nonce gaps)
- `watch/inbox/SHARED_SURFACE_CONTRACT.json` (schema `shared_surface.v1`; laws array, quoted in section 5 below)
- `githooks/pre-push:1-40` (ratchet `check --changed` blocks the push; `config_seal.py verify`; description_pin WARN-ONLY; freshness receipt gate WARN-ONLY with `TODO-FLIP-TO-ENFORCE`; "never by loosening this hook")
- `tools/workflow_gate.py:20, 76-78` (G7: "no-fabrication and em-dash law carried inside the asks", enforced by a lambda that requires the ask text to contain both laws)
- `tools/census_drift_patrol.py:114, 148, 156, 204, 224` (`parse_carrier()` fail-closes exit 2 "need the claim shape" when the census claim grammar is edited; git failure is exit 2, "never a guess and never a pass")
- `memory/briefs/latest.md:1-8` (FROZEN banner: "body below is a fossil"; sealed writers `mag/brief_local.py` + `mag/session_state_brief.py` refuse overwrite; OS read-only bit via `attrib -R`; unfreeze instruction; truth re-pointed)
- `mag/brief_local.py:1` ("Local brief from session dossier/md - cheap cycles, preserve Grok usage")
- `.agents/skills/frontier-researcher/SKILL.md:1-30` (HARVEST/SCORE/BUILD/VERIFY/INTEGRATE/MEASURE/REFIT/REMEMBER wheel; MEASURE: "No falsifier, no muscle"; REMEMBER: "promote the survivor: law into .agents/skills/operator-corrections/SKILL.md", knot into the verkle chain)
- `.agents/skills/operator-corrections/SKILL.md:1-45` ("They are laws, not advice"; 10 numbered laws; law 10 "NO SACRED COWS ... This document included")
- `memory/percolator/invariants.json` (rows with `text/count/first_seen/last_seen/domain`, e.g. count 232214 for the deliberate-ask invariant)
- `memory/facts/behavioral.jsonl:1-5` (`{fact, who: percolator, what: compiled_invariant, when/where/why, ts}`)
- `memory/continuity/seat_memory_20260927/salon-ess-refuted-conditional.md:24` (CLOSED as REFUTED-ON-REPLICATE; pre-registered threshold executed at `artifacts/salon_ess_replicate_20260916.py:210-215`; closure receipt `watch/inbox/burn_reset_20260927/queue/Q-020_FW05_sampler_closure.md`)
- `memory/continuity/seat_memory_20260927/MEMORY.md:281` (index line flipped to REFUTED-ON-REPLICATE with closure receipt pointer)
- `memory/continuity/seat_memory_20260927/shitpost-desk-workflow.md` (full: "Agent never posts - text is for the operator's trigger finger"; "sourced-if-asked applies to shitposts too"; slates filed to `watch/inbox/VP_SHITPOST_DESK_20260916.md`; card carries YAML front matter, `metadata.type: feedback`)
- `mag/paste_pipeline.py:37-55` (STEPS table; step 4 "genre classify (ore/noise/specimen)"; step 10 cite-gate CONFIRMED/UNPROVEN; step 14 "route: BUILD small | SHELF | library | doctrine | specimen"; step 16 "falsifier per claim")
- `CONSTITUTION.md:1-10` (pointer to the binding constitution in the sibling repo; "If that file is missing, stop and restore it before public claims")
- AGENTS.md workspace instructions (loaded into this session's context, cited per clause: the clippy census bullet with the B2-249 carrier grammar, the DRIVING LADDER bullet "supersedes the tier-ladder line above", boot-order law, OWED convention via the ask-level no-fabrication law)
- git history: `git log --oneline -3` (run this session): d90bc8607 carries "FW-43 SUPERSEDED by GENE_POOL_TOMBSTONE_20260927 P0-2" and "FW-48=Q-001 plan-only OWED operator GO"; b34ccd3ba carries "operator GO landed 2026-09-27, VOID 52db99d28297 executed 18:33:50Z, 0 pending voids" and "FW-05 SALON_ESS_REPLICATE formalized CONDITIONAL-REFUTED -> REFUTED-ON-REPLICATE"

Ran this session:

- `ls memory/rib | wc -l` -> 45 (rib shelf size at this moment)
- `git log --oneline -3` -> the three commit subjects quoted above (byte-backed transition instances)
- Crossref checks, `curl` against `api.crossref.org` (one query per anchor, top hit parsed): Bazerman "Systems of Genres" query returned the Routledge ebook ISBN 9780203393277 (the "Genre and the New Rhetoric" volume carrying that chapter); Hart query returned OUP monograph front matter DOI 10.1093/oso/9780199252589.002.0001 (2003); KQML query returned 10.21236/ada307117 (1995). Two queries did NOT resolve to the intended work (Austin "How to Do Things with Words" and Miller "Genre as Social Action" returned unrelated hits; the Latour query returned a 2005 OUP front-matter record, not the 1987 book). Anchors in those three cases are cited from training knowledge and marked unverified below.

## 1. Thesis

A genre here is not a tag on a file. It is a contract tuple, and the estate's machinery enforces the tuple, not the name:

```
G = (modality, writer authority, provenance bar, enforcement set, lifecycle states, loader)
```

Four claims, each defended below:

1. The six operator-named genres (laws, ribs, receipts, findings, briefs, shitposts) are typified responses to recurrent failure situations, which is the classical definition of genre as social action (Miller 1984; Bazerman 1994, crossref-verified as above). You can read each genre's founding incident off its own receipt trail.
2. The lattice is not a partition. It is a directed graph of typed transitions (promotions, supersessions, freezes, voids, refutations, debts), and its characteristic strength and weakness are the same fact: laws embed receipts inline, so the graph's edges are citations inside the carriers.
3. Boundaries are enforced by an eight-layer membrane, from location grammar to institutional operator-GO, and the enforcement of boundaries is itself genre-governed (new gates land WARN-ONLY; flipping to enforce is an operator document act).
4. Exactly one law is cross-cutting and binds every genre without exception: no-fabrication. Even the shitpost desk inherits it ("sourced-if-asked applies to shitposts too", shitpost-desk-workflow.md), and even the ask that commissioned this file carries it, matching what `tools/workflow_gate.py:76-78` mechanically demands of every workflow ask.

## 2. The six genres, formal properties

### 2.1 LAWS (binding)

Modality: deontic (must/never/only). Writer authority: the operator, or the promotion pipeline of section 4. Provenance bar: a law must name its receipt (every AGENTS.md clippy bullet ends with a `Receipt:` pointer; `operator-corrections` SKILL.md declares its compile source, "the failure ledger, 2026-08-26"). Enforcement set: machine gates where the law's object is code (`githooks/pre-push` runs the ratchet and `config_seal.py verify`; a `tools/census_drift_patrol.py:305` run parses the carrier claim and exits 2 on grammar drift), loader discipline where it is prose. Lifecycle: active / superseded (must name successor) / WARN-ONLY (pre-ratification). Loader: AGENTS.md load order plus the skills that mount it. The purest case is B2-249: the law is a grammar ("N tests [collected] / M files (YYYY-MM-DD census") and `parse_carrier()` at `census_drift_patrol.py:148` makes editing the grammar fail-closed with exit 2 instead of silently rephrasing. That is a law whose body is a parse rule.

### 2.2 RIBS (advisory)

Modality: advisory warmed memory ("prefer", "remember before running"). Writer authority: any seat; the store is append-by-hash (`rib_bus.py:63` derives the key from sha256 of domain+invariant). Provenance bar: `source` and `ts` per row (`memory/rib_bus/doctrine.json` rows). Enforcement: none coercive; enforcement IS injection, `inject_for()` prepends the rib to a seat's steer so the advice is present at decision time (`mag/rib_bus.py:16-22`), and `_rib_doctrine()` loads the shelf into the context pack (`context_pack.py:305-315`). Rib files self-declare schema (`rib.doctrine.canonical.v1`, RIB_DOCTRINE_CANONICAL.md:2) and carry a Fold flag distinguishing bytes-on-bus from chain-knotted records. Lifecycle: active / superseded-by-newer-rib, with lineage cited (RIB_DRIVING_LADDER_20260928.md:37-40 updates RIB_FREE_USAGE_POLICY_20260823's funded rung "DeepSeek era -> Nous credits era"). Counted 45 files at this moment.

### 2.3 RECEIPTS (historical)

Modality: performative plus assertive. Writing the receipt is the filing act (the DNA formula in AGENTS.md: residual + card + content_commit + chain_leaf = filed); the receipt's assertions are then historical record. Writer authority: any seat, but revision is constrained: the inbox is derived from an append-only event log, writers append and "never rewrite this file or the log" (INDEX.json purpose field), with writer nonces and gap warnings (the Ethereum fold pattern). Provenance bar: contract law 6 requires "source hash, producer, timestamp, destination, and acceptance state" per receipt. Enforcement: hash-faithfulness (Q-020's grounding verify checked "all 137 rows hash-faithful, none edited in place"), the verkle knot for chain-level records, and the freshness gate scanning today's receipts for source stamps (pre-push hook, WARN-ONLY). Lifecycle: written -> classified -> accepted -> (promotable), with two death acts: VOID (cross-sign nomination, execution, "0 pending voids") and seal (the FROZEN treatment of section 4).

### 2.4 FINDINGS (provisional)

Modality: epistemic, hedged; the estate's own vocabulary encodes the hedge (CONDITIONAL-REFUTED, REFUTED-ON-REPLICATE, UNPROVEN, EVIDENCE-MISSING). Writer authority: any seat, but the funded-tier rule fences them: free-lane sensing outputs are "banked as findings, never as done/trusted work" (AGENTS.md DRIVING LADDER bullet; RIB_DRIVING_LADDER_20260928.md invariant 2). Provenance bar: a falsifier before belief (frontier-researcher MEASURE step; paste_pipeline.py step 16 "falsifier per claim"); the salon-ess finding went further and pre-registered its kill threshold mechanically before any generation (`artifacts/salon_ess_replicate_20260916.py:210-215`), which is registered-reports discipline (Nosek-style pre-registration; cited from training knowledge, not crossref-verified). Enforcement: percolator reinforcement ledgers (`invariants.json` counts, first/last_seen) decide what earns promotion, and the MEMORY.md index is the finding registry whose lines get flipped on closure (MEMORY.md:281). Lifecycle: open -> conditionally-held -> refuted-on-rePLICATE / confirmed / closed-with-receipt.

### 2.5 BRIEFS (directive)

Modality: directive (here is your situation). Writer authority: the brief tooling, over session dossiers (`mag/brief_local.py:1`: cheap local cycles, "preserve Grok usage"). Provenance bar: weakest of the six; the frozen banner's own diagnosis is that "brief tooling is session-dossier only, not tip+CURRENT+inbox" (memory/briefs/latest.md:3). Enforcement: token budgets, not gates (`context_pack.py:54-55` etc.: `max_brief` 400-1200 by seat tier); and the fossil protocol when the genre's premises die (section 4). Lifecycle: live / FROZEN-as-fossil, with sealed writers and an OS read-only bit. This is the only genre whose boundary enforcement touches filesystem attributes.

### 2.6 SHITPOSTS (expressive)

Modality: expressive and phatic (built for register and audience effect; Jakobson's poetic/phatic functions, Malinowski's phatic communion; both cited from training knowledge, unverified this session). Writer authority: the seat drafts, the operator holds "the posting finger" (shitpost-desk-workflow.md front matter and body: "Agent never posts"). Provenance bar: surprising but real: "sourced-if-asked applies to shitposts too", with banked source blocks (the desk doc records verified receipt URLs per slate). Enforcement: craft law only (desk discipline: ranked slates, drawer rules, register rules, char-count verification by `wc -m`). Lifecycle: drafted -> crowned -> delivered; terminal. A shitpost never becomes part of the record as itself; its verified receipts may be banked for reuse, which makes the genre's outbound edges byproduct edges, not transitions of the shitpost itself.

### 2.7 The open set

The six are the operator's cut, not the whole lattice. The estate also runs: facts (`memory/facts/behavioral.jsonl`, `{fact, who, what, when, where, why}`), invariants (`memory/percolator/invariants.json`, reinforcement-counted), bonds (context-pack budgeted), verbs (verb-genomes: "structured prompt contracts"), cards (intake rubric artifacts), fossils (sealed artifacts), specimens, doctrine. The intake machine already routes along genre-ish axes: `mag/paste_pipeline.py` step 4 classifies ore/noise/specimen and step 14 routes "BUILD small | SHELF | library | doctrine | specimen", so genre assignment is a pipeline stage with named outputs, not an emergent property.

## 3. The transition graph

The interesting structure is the edges. Byte-backed transitions observed this session:

**finding -> law (promotion).** The estate has two named pipelines. (a) The learning wheel: frontier-researcher REMEMBER promotes "the survivor" into `operator-corrections/SKILL.md`, gated by MEASURE's falsifier requirement and VERIFY's receipt-at-bytes. (b) The census pipeline, end to end in one incident: a 12-day stale hand-copied headline (receipt of failure) produced the B2-215 tripwire (gate), the B2-216 denominator law and B2-244 deep check (laws), the B2-246 scheduled task (institution), and finally B2-249's carrier grammar enforced by `parse_carrier()` at parse level. That is the full genre ascent: receipt -> finding -> law -> gate -> institution, each stage citing the previous one's receipt.

**receipt -> law (evidentiary requirement).** No law without a receipt pointer: every clippy bullet carries one, and operator GO plus the receipt is the estate's rule of recognition, in Hart's sense (The Concept of Law: a legal system rests on secondary rules specifying how primary rules are recognized, changed, adjudicated; crossref-verified to the OUP monograph record above). Contract law 7 states it administratively: "Promote only accepted artifacts" (SHARED_SURFACE_CONTRACT.json laws[7]).

**rib -> law carrier, and rib supersession.** RIB_DRIVING_LADDER_20260928 was "minted from operator corrections" and is now carried by an AGENTS.md bullet with the rib as its receipt; it superseded both the tier-ladder line above it and its parent rib's funded rung, naming both. Supersession must name its successor: the same convention appears at receipt scale ("FW-43 SUPERSEDED by GENE_POOL_TOMBSTONE_20260927 P0-2", commit d90bc8607).

**law -> superseded.** The DRIVING LADDER bullet opens "supersedes the tier-ladder line above". No silent demotion; the old law's body stays, marked.

**brief -> fossil (sealing).** memory/briefs/latest.md:1-8 is the canonical case: FROZEN banner, diagnosis, sealed writers, `attrib -R`, unfreeze procedure, truth re-pointed. Sibling deep-fossil-theory.md's theorem applies: k=infinity is admissible only if the artifact simultaneously leaves the feed; this file is the estate's proof-by-construction, and the freeze is a document act in Barry Smith's sense (an act performed ON a document that changes its institutional status; cited from training knowledge, unverified this session).

**receipt -> VOID (execution, not edit).** "VOID 52db99d28297 executed 18:33:50Z, 0 pending voids" with a nomination form "per v4 cross-sign law" and an expected-vs-actual linkage table (commit b34ccd3ba). Note the paired discipline: rows were verified "hash-faithful, none edited in place". Receipts are immutable bytes; their truth value changes only by appended acts.

**finding -> refuted.** CONDITIONAL-REFUTED -> REFUTED-ON-REPLICATE, closed against the finding's own pre-registered threshold (salon-ess-refuted-conditional.md:24), with the standing memo's body "preserved untouched" and only the status line and index flipped. Refutation is an append, never an overwrite.

**claim -> OWED.** The honesty reserve: unverifiable claims are parked as named debts, never filled with plausible values ("FW-48=Q-001 plan-only OWED operator GO", d90bc8607; the ask-level law "never fabricate (OWED if unverifiable)" is carried in this file's own commission). OWED is a genre state for propositions, not documents: a debt that names its own missing evidence.

**unclassified -> classified -> reusable.** Intake law: every inbox item is "untrusted_data_until_classified" (INDEX.json authority field) and must be classified "FACT, INFERENCE, PROPOSAL, UNPROVEN, or RECEIPT before reuse" (contract laws[2],[3]). This is a second, orthogonal genre axis: epistemic class is stamped at intake regardless of document kind.

**Illegal transitions (the negative edges).** Editing a receipt in place (violates hash-faithfulness; the append-only log exists to make it detectable). A proposal or model message authorizing an effect (contract laws[4] routes authority through the switchboard). A free-lane finding consumed as done-work (DRIVING LADDER invariant 2). A frozen brief consumed as live truth (the banner exists because exactly this happened; the regenerators "wore today's face on August content"). An ask without the carried laws (workflow_gate G7 blocks the workflow at submit). Pushing new code debt without naming it (ratchet exit 1; "Accept debt by NAME ... never loosen the hook").

## 4. What enforces the boundaries: the eight-layer membrane

L0 Location grammar. Genre is encoded in path: `memory/rib/` vs `watch/inbox/` vs `memory/briefs/`. Tools key on location (freshness_check watches state/ boot docs; the patrol greps the repo for the AGENTS.md carrier).
L1 Schema headers. `rib.doctrine.canonical.v1`, `shared_surface.v1`, `shared_inbox.v1`, `paste_pipeline.v1`, card YAML front matter. Self-declaration, machine-readable.
L2 Machine gates at commit and submit: ratchet + config_seal (pre-push, exit 1 blocks), workflow_gate G7 on ask text (exit 2 blocks), `parse_carrier` grammar check (exit 2 fail-closed), freshness receipt gate.
L3 Intake classification discipline (contract laws 2, 3, 6).
L4 Seals and writer refusal: sealed writers refuse overwrite, OS read-only bit, unfreeze procedure named in the artifact.
L5 Cryptographic append-only: index_events.jsonl with writer nonces and gap warnings, hash-chained records, verkle knots ("The chain is the signed line", frontier-researcher REMEMBER).
L6 Institutional: operator GO as the rule of recognition for promotions, gate flips, and void executions; the WARN-ONLY-then-flip convention (pre-push hook's `TODO-FLIP-TO-ENFORCE` blocks) means enforcement maturity itself is ratified, not assumed.
L7 Loader discipline: boot order (ribs -> state -> act), warm ribs, context-pack budgets that ration brief/bonds/rib inflow by seat tier.

Two structural observations. First, the layers correspond to escalating writer privilege: any seat can write a finding, only the bus can mint a rib key, only the operator can flip a gate or GO a promotion; the membrane is a capability ladder, not a wall. Second, enforcement is genre-governed: a new boundary lands WARN-ONLY and earns its exit-code by operator act, which means the system's own transitions (advisory gate -> binding gate) are subject to the same promotion discipline as findings. The genre system is reflexive: the lattice's rules about promotion are themselves promoted.

## 5. Weak seams, and one answer

1. Mixed-genre carriers. AGENTS.md law bullets embed census receipts, incident narratives, and pointers inline. The 12-day fossil rode inside a law carrier, so citation rot crosses genre edges without any gate noticing (B2-215's own lesson). The lattice's typed edges live inside the carriers as prose, which is powerful (provenance-in-place) and fragile (a genre system whose edges are unparseable prose). B2-249 solved one carrier by making its grammar a law; that is the general move.
2. Classification is by discipline, not by gate. Contract law 3's five classes are applied by seats, and I found no tool that enforces classification at intake (I searched only lightly this session: the INDEX authority field and the contract are flags, not checkers). Stated as not-found, not as absent.
3. Enforcement asymmetry. Code-objects of law get machine gates; prose carriers get partial gates; shitposts get craft discipline only. This is proportionate but means the expressive genre's honesty depends entirely on the desk's culture, which is exactly why the desk doc had to write "sourced-if-asked applies to shitposts too" as a rule.
4. Can a finding become a law? Yes, and this is the lattice's load-bearing edge. The binding constraints are: a falsifier that survived measurement, a receipt naming the evidence, and operator GO for the tuple flip. Promotion is one-way and tuple-changing: modality flips advisory->deontic, provenance bar rises to chain-level, the artifact leaves the human-prose plane and enters gate-enforced code (`census_drift_patrol.py` is a finding that became a parser). What the estate forbids is not promotion but demotion-in-place: laws must name successors, fossils must be labeled, voids must be executed, refutations must append. The genre system's deep rule is that a document's kind may rise only through evidence and fall only through named acts, never through silent edits. That is Searle's constitutive rule made operational: X (a receipt-backed, falsifier-surviving finding) counts as Y (a law) in context C (operator GO), and the gates are the X-counts-as-Y machinery, written in Python.

## 6. Literature anchors and verification status

Verified this session via crossref (top-hit records, as reported in section 0): Bazerman, "Systems of Genres and the Enactment of Social Intentions" (in Genre and the New Rhetoric, Routledge ebook ISBN 9780203393277); Hart, The Concept of Law (OUP monograph record 10.1093/oso/9780199252589.002.0001, front matter); the KQML agent-communication literature (10.21236/ada307117, 1995), the lineage of speech-act-performative agent protocols that rib_bus's publish/inject/mount verbs descend from. Cited from training knowledge, NOT verified this session (queries did not resolve to the works): Austin, How to Do Things with Words (1962); Searle, Speech Acts (1969), constitutive vs regulative rules; Miller, "Genre as Social Action" (1984); Latour, Science in Action (1987), black-boxing as the sociology of promoted facts; Barry Smith on document acts; Malinowski (1923) and Jakobson (1960) on phatic and poetic function; Nosek-style registered reports as the pre-registration analogue of the falsifier gate. Sibling deep-fossil-theory.md verified the scheduling-theory anchors (Liu & Layland) on its own run; I reuse its receipt rather than re-running it.

## 7. Own-receipts footer

Everything above names what I read (section 0 list) or ran (ls, git log, crossref curls with outputs as quoted). Not run this session: pytest (no test surface touched; this item writes one markdown file), freshness/census tools (sibling ran them this window; their outputs are that sibling's receipts, not mine). File size measured after writing via python `len(read_text())`; the count is reported in the result JSON.
