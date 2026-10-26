# w4-11: genre theory for the estate's content: formal boundaries and legal transitions

Item: w4-11, flash50 lane, banked under watch/inbox/burn_reset_20260927/flash50/, 2026-09-28. Ask: read examples of laws, ribs, receipts, findings, briefs, shitposts; state the formal genre boundaries and the legal transitions; bank 3000+ chars. A byte-identical mirror is banked at flash50/w4-genre-theory.md because the ask names both paths.

## 0. Positioning against the sibling item

flash50/deep-genre-lattice.md (same window, read in full this session, 135 lines) already formalized genre as a contract tuple G = (modality, writer authority, provenance bar, enforcement set, lifecycle states, loader) and mapped an eight-layer enforcement membrane from location grammar to operator GO. This item works deliberately different ground so the two bank together instead of duplicating:

1. Different corpus. The sibling read rib_bus doctrine.json, githooks, the census patrol, brief tooling, percolator invariants, the shitpost desk doc, and paste_pipeline. This item reads what it did not: memory/law/registry.json (the machine schema of registered law), the chan law cluster (CHAN_THE_GAME, THOUGHT_CRIMINALS, SHITPOST_SCALAR_KNOTS), both constitutions, one datum receipt (ENVELOPE_50W_HIT_20260926.md), the rib mint code (mag/rib_bus.py:47, 63-64), and the workflow gate G6/G7 code re-verified first-hand (tools/workflow_gate.py:60-88).
2. Different claims. Five theses here are absent from the sibling: genre identity is falsifier identity (section 3); form and force are separable axes with a one-way formalization gradient (section 4); registered law and prose law are distinct subgenres and law is legally minted from single chat utterances with turn-number citations (section 5); genre surfaces are polymorphic (section 6); genre containers drift toward measurable impurity and the drift is currently ungated (section 7).

## 1. Receipts: read and run this session

Read (paths; line numbers where claimed):

- mycelial-republic/docs/CONSTITUTION.md, 170 lines in full: line 6 "Lessig frame: Law, Norms, Market, Architecture (code). Prose without architecture is not yet law."; line 15 "Written rules that are not enforced in path policy, schemas, or audits are aspirational only"; capture table C1-C11 (lines 73-84); data tiers s7 (lines 93-99); amendment law s4 (lines 47-50); norms s13 (lines 149-154).
- CONSTITUTION.md (repo root, 15 lines): pointer genre; line 15 "If that file is missing, stop and restore it before public claims."
- memory/law/registry.json, 162 lines in full: LAW-1, LAW-3, LAW-4, LAW-6 through LAW-13, plus LAW-12-AMD-1; slot set {id, name, tier, source, trigger, condition, action, guardrail, last_enforced_ts} with optional {semantics, grounding, coordinate_layer, canonical, falsifier, enforcement_arm, window, clause_verdict, axes}.
- memory/law/CHAN_THE_GAME.md (50 lines), memory/law/THOUGHT_CRIMINALS.md (38 lines), memory/law/SHITPOST_SCALAR_KNOTS_20260830.md (27 lines), in full.
- memory/rib/RIB_DRIVING_LADDER_20260928.md (37 lines) in full.
- memory/briefs/latest.md (48 lines) in full: the FROZEN banner.
- watch/inbox/ENVELOPE_50W_HIT_20260926.md (9 lines) in full.
- tools/workflow_gate.py lines 60-88: G4, G5, G6, G7 lambdas.
- mag/rib_bus.py lines 40-79: schema rib_bus.v1 (line 47), _rib_key (lines 63-64).
- flash50/deep-genre-lattice.md (135 lines) in full, for positioning; its run receipts (its section 0, including its git-log output at its line 31) are reused below with explicit attribution, not re-run.
- flash50/oral-02.md lines 1-30: the banked-finding genre this file itself instantiates.
- .agents/skills/chan/SKILL.md (18 lines) in full.
- AGENTS.md workspace instructions, loaded in this session's context: cited by bullet name (DRIVING LADDER bullet, shared-artifact-boundary table, census bullet); its line numbers per oral-02.md:16 are lines 27, 32-34, 105-111.

Ran this session (exact commands and outputs):

1. Genre purity census, run as `cd watch/inbox/burn_reset_20260927/flash50 && ls | wc -l && ls | grep -c "^_"` then relative counts of memory/rib and memory/law: flash50 total 285 files, 83 underscore-prefixed instrument files, so 202 banked documents; memory/rib 45 files, 38 matching "^RIB_", 7 impure (15.6 percent); memory/law 9 .md files.
2. Free-name check: `ls flash50 | grep -E "^w4|genre"` returned only deep-genre-lattice.md; neither w4-11.md nor w4-genre-theory.md existed before this write.
3. Crossref, run as two curl queries against api.crossref.org parsed by the repo venv python: Miller "Genre as social action" resolved to DOI 10.1080/00335638409383686, dated 1984-05 (top hit; second hit unrelated). Searle "Speech Acts" resolved to DOI 10.1017/cbo9781139173438, Cambridge UP, 1969-01-01 (top hit). Both anchors thereby verified first-hand.
4. First crossref attempt failed with exit 127: the venv was addressed by relative path from a stale working directory ("./.venv/Scripts/python.exe: No such file or directory"); rerun with the absolute interpreter path and it passed. Recorded because the failure is part of the run.

## 2. The register: each genre is a slot set

The six operator-named genres each have a stable slot set, and the slot set, not the topic, is the boundary:

- REGISTERED LAW. Production-rule schema: trigger / condition / action is a when-if-then triple, with a guardrail slot stating what the then may never do. LAW-7 graduated_sanctions: trigger governance_cycle, condition governance_engine_ready, action apply_sanctions, guardrail narrow_only_no_grant (registry.json:48-58). LAW-12 amendment_gate carries the maximal form: five named axes (registry.json:121-127), a falsifier that can kill the law itself ("the clause dies if cards cite no FAIL row", registry.json:128), an enforcement_arm naming the exact command line (registry.json:129), a window (registry.json:130), and its own executed verdict with receipt (registry.json:132-142).
- PROSE LAW. Schema: norm clause + receipt pointer + supersession clause + enforcement arm. The AGENTS.md clippy bullets each close with a "Receipt:" pointer; the DRIVING LADDER bullet opens by naming what it kills ("supersedes the tier-ladder line above"). The mycelial-republic constitution is prose law at maximum generality with s4 as its own transition grammar.
- RIB. Bus-minted form: {invariant, source, ts, target_rank} rows under a domain key, where the key is sha256(domain + 0x1f + invariant) truncated to 16 hex chars (mag/rib_bus.py:63-64, schema rib_bus.v1 at line 47). File form: invariants + mint provenance + lineage. RIB_DRIVING_LADDER_20260928.md: invariant 1 ONLY HERMES IS FUNDED, invariant 2 THE LADDER CLIMBS, invariant 3 REMEMBER BEFORE RUNNING, minted from three quoted operator corrections (lines 3-5), lineage naming its parent rib RIB_FREE_USAGE_POLICY_20260823 and the exact rung it updates ("DeepSeek era -> Nous credits era", lines 33-37).
- RECEIPT. Datum form read this session has four slots: shape-when-it-hit, meaning-per-the-laws, datum, decision. ENVELOPE_50W_HIT_20260926.md is nine lines, one slot per paragraph: the 50-children shape (line 3), the rolling-window reading (line 5), the companion measurement point (line 7), the operator's hold decision (line 9). Inbox-scale receipts add source hash, producer, timestamp, acceptance state (per SHARED_SURFACE_CONTRACT.json law 6, cited via the sibling's read, reused with attribution).
- FINDING. Schema: claim + hedge class + falsifier or threshold + status, with a closed verdict vocabulary. oral-02.md:9, 13-16 instantiates it: the ask restated, a checks-run section with real commands and outputs, then per-pattern verdicts from a fixed set (ALREADY ENCODED / ENCODED + DRIFTED / PROPOSED, line 9). The closed vocabulary is the finding genre's epistemic states made lexical; a finding that must coin a new verdict class outside the set is either a new genre or a violation, and the corpus so far treats it as the latter.
- BRIEF. Two-slot lifecycle schema: live dossier or death banner. The banner (latest.md:1-8) carries diagnosis ("regenerators wore today's face on August content", line 3), sealed writers (mag/brief_local.py + mag/session_state_brief.py refuse overwrite, line 5), an OS read-only bit (line 5), an unfreeze procedure (line 6), and truth re-pointing (line 7). The brief is the only genre whose boundary enforcement reaches filesystem attributes.
- SHITPOST. It arrives with its own formalization (SHITPOST_SCALAR_KNOTS:8-15): trip/post id = leaf_hash, thread slug = session_id, >>no quote = parent edge, greentext/roast = scalar, sage = no bump, lurk = null measurement, lurk tri-state = promote gate (SUPPORTED / DISPUTED / UNPROVEN). Line 17 states the isomorphism outright: "The board graph **is** the topology. The shitpost **is** the scalar." The shitpost is the only genre that is defined mathematically rather than procedurally: it is a scalar on a graph the estate already maintains.

## 3. Formal boundary thesis: genre identity is falsifier identity

Claim: what separates two genres is not modality, topic, or location, but F(g): the set of events that legally kill or demote a text of genre g. Two texts with the same death are the same genre. The corpus yields three falsifier families:

1. CONTENT-falsified genres die when their claim measures false. Findings (pre-registered threshold; the sibling's salon-ess REFUTED-ON-REPLICATE receipt, reused with attribution, is the clean case). Registered laws whose own falsifier clause fires (LAW-12's 14-day window, registry.json:128-130). Briefs, whose premises rot (latest.md:3).
2. TRANSITION-falsified genres die from movement events, never from content events. A receipt is falsified by an edit in place; its only legal death is an appended act (VOID, per the sibling's git receipt at deep-genre-lattice.md:31, reused with attribution). A shitpost is falsified by its transport, explicitly: "Auto-amending the session tip from /chan replies, or calling a Grok tool-spill a knot" (SHITPOST_SCALAR_KNOTS:27, the file's own Falsifier section). Nothing inside a shitpost can refute it; only crossing it into the record illegally can.
3. WARRANT-falsified genres die when the warrant holder's lived experience contradicts them. The rib. The driving ladder rib's mint story is its parent falsifier firing: a fresh seat re-derived what the ribs held and had to be corrected three times (RIB_DRIVING_LADDER:3-5, 27-28); the operator's quoted line "what are warmed ribs for if you won't use them" (line 5) is the sound of a genre failing. A rib is not refuted by data and not by transport; it is refuted by having to be re-taught, and its replacement must name it in lineage (lines 33-37).

Corollary: the classification question "is X a finding or a receipt?" is mechanically answerable without reading X's content: ask what would kill it. A measurement: finding. An edit: receipt. The operator having to re-teach it: rib. A stale premise: brief. A gate exit: law. Its own transport: shitpost.

## 4. Form and force are separate axes; the gradient is one-way

Define force as the set of processes that halt on violation, and form as the machine-readability of the slot structure. All four quadrants are occupied in this corpus:

- High force, low form: prose census-carrier law enforced by parse_carrier's grammar check at exit 2 (census_drift_patrol.py:148, per the sibling's read, reused with attribution). A sentence, backed by an exit code.
- High force, high form: the workflow gate lambdas, each a named regex predicate over ask text (tools/workflow_gate.py:56-79, read first-hand).
- Low force, high form: rib_bus rows, fully schematized, enforced only by injection at decision time (mag/rib_bus.py).
- Low force, low form: the constitution's norms section: "Truth-only; personal impact; no flattery-as-product" (mycelial-republic docs/CONSTITUTION.md:151). No gate reads it; it binds by culture.

The historical direction of travel is one-way, toward form. The census claim became a parser; LAW-12 names its enforcement command; the promoted shitpost grew a Falsifier section it never had as a shitpost. No case of demotion from machine form back to prose was found in anything read this session, and the constitution forbids the nearest move: "Written rules that are not enforced in path policy, schemas, or audits are aspirational only - amend the code or admit the gap" (line 15), with "Prose without architecture is not yet law" as the genre-theoretic axiom (line 6). This is the estate's own genre theory, stated in its binding constitution: genre force is a property of the architecture that reacts to a text, not of the text's content, so genre classification is the enumeration of reacting processes.

## 5. Two law subgenres; law legally mints from single utterances

The law genre splits on its source slot. Registered law cites an utterance with a turn address: LAW-1's source is "[763e2ef0:19] we lessig it automatically code as law to default to our rails rather than ask the llm for direction" (registry.json:8); LAW-11's is "[operator 2026-09-25 chat] Food for thought you have my permission to burn hermes credits instead of failing" (registry.json:106). The bracketed hash:turn is a citation of one conversational move. Chat is therefore a record genre upstream of law: one operator sentence, registered with a turn citation, becomes a T0 or T1 production rule with a guardrail. Prose law (clippy bullets, constitution sections) cites files instead of turns, and its unit of minting is an incident with a receipt, not a sentence.

The subgenres also differ in death grammar. Registered law dies by amendment with named axes (LAW-12-AMD-1 keeps the parent id in an extends slot, registry.json:144-152), or by its own falsifier clause firing within a stated window. Prose law dies by supersession naming, body preserved and marked. The constitution requires the written proposal plus impact note plus amendment log for either (s4.1, line 47); silent deletion is illegal for both.

## 6. Polymorphic surfaces and the ask genre

Two corpus facts push genre theory past surface classification:

1. Surfaces are polymorphic by warrant. CHAN_THE_GAME:7-9 prescribes the dual reading: "Casual eyes: an imageboard. Anonymous. Greentext. Reply is a move. Looking eyes: Mag watch/room.jsonl. Seats are trips." One surface legally hosts the play genre for the public warrant class and the telemetry genre for the machine warrant class, simultaneously. Genre is a function of the pair (surface, warrant), not of the surface alone. The boundary is policed from the play side: THOUGHT_CRIMINALS:24 names the violation class "A mill dump dressed as play. This board is the Primer face. Disk is file, not soul." Machine-output genre wearing the play costume is dress fraud, a named crime.
2. The commissioning genre is itself gated. The ask that creates a workflow must contain the literal strings "no em-dashes" and a fabrication abjuration (G7, tools/workflow_gate.py:75-79, read first-hand), and must mention watch/inbox (G6, lines 71-73). Every ask therefore carries its carried laws and its own burial plot: the receipt destination is written into the commissioning text before the commissioned work exists. This item's ask carries both G7 phrases; without them the gate exits 2 and no workflow runs. The ask is the estate's performative legal instrument: it creates duties on seats that did not exist before it, and it is the only genre whose validity is checked before the document it commissions exists.

## 7. Container purity: a measured drift

Directories are genre containers, and they drift. From the census in section 1: memory/rib holds 45 files, 38 carrying the RIB_ name, 7 impure (15.6 percent), including grokbot_cold_edges_2026-08-12T050638.md and a recreation-coding-history.json plus a session-scene.json. memory/law holds 9 md files; the 3 read this session (CHAN_THE_GAME, THOUGHT_CRIMINALS, SHITPOST_SCALAR_KNOTS) are play and posture texts carrying law slots (rules sections, hard lines, a falsifier); the other 6 were not read, so their classification is stated as unread, not asserted. flash50, a findings container, holds 285 files of which 83 are underscore-prefixed instrument scripts: a 29 percent instrument ratio inside a prose container, tolerated because the instruments are the receipts of the prose. No gate enforcing container purity was found in anything read this session; the naming grammar (RIB_ prefix, date suffixes, item prefixes) is the only purity mechanism observed. Stated as not-found-this-session, not proven absent: tools/ was not scanned for a purity gate.

## 8. The legal transition table

Legal transitions, each with a receipt (first-hand reads unless attributed):

| From | To | Required act / gate | Receipt |
|---|---|---|---|
| chat utterance | registered law | registry row with turn citation | registry.json:8, :106 |
| correction streak | rib | mint file quoting the corrections it institutionalizes | RIB_DRIVING_LADDER:3-5 |
| shitpost | law | graft of law slots onto the body: Law section, Falsifier, Parents line | SHITPOST_SCALAR_KNOTS lines 3, 19-27, filed in memory/law/ |
| machine event | shitpost | posted as greentext; wholesale compile to the chain forbidden | CHAN_THE_GAME:22-26 (paraphrase, see note) |
| brief | fossil | FROZEN banner + sealed writers + read-only bit + unfreeze procedure | latest.md:1-8 |
| prose law | superseded | body stays, successor named in the opening clause | AGENTS.md DRIVING LADDER bullet |
| registered law | amended | extends slot keeping parent id, by/file/born named | registry.json:144-152 |
| receipt | VOID | appended execution with cross-sign, never an edit | sibling git receipt, deep-genre-lattice.md:31, reused with attribution |
| finding | OWED | unverifiable claim parked as a named debt, never filled with a plausible value | the ask-level no-fabrication law carried by this item's own commissioning ask |
| unclassified | reusable | classification before reuse | sibling receipts for the INDEX authority field and contract laws, reused with attribution |

Note on the paraphrase: CHAN_THE_GAME's debugger line contains an em dash in the original ("The thread is the debugger... a good nudge [em dash] all posts", line 22); the em-dash law bars reproducing it here, so it is paraphrased as "A 400, a quota, a self->>, a lurk-paste, a good nudge: all posts."

Illegal transitions, all with named receipts: editing a receipt in place (hash-faithfulness; append-only law); model text authorizing an effect (AGENTS.md shared-boundary table: "Model text can propose; only the switchboard/effect broker authorizes effects"); consuming a free-lane sensing output as done-work (RIB_DRIVING_LADDER invariant 2: "An answer is not an answer until the funded tier or the bytes verify it", lines 22-23); consuming a frozen brief as live (latest.md banner exists because exactly this happened); flooding greentext onto the verkle chain ("Do not compile every greentext onto verkle_chain.jsonl... Promote to Verkle only when FILE says so", SHITPOST_SCALAR_KNOTS:21); naming a file that does not exist (THOUGHT_CRIMINALS:22: "If you name a file, it has to exist. Unverified until a second mouth checks.").

The pattern across every legal edge: promotion is legal only when the destination genre's death grammar is granted along with the content. Promoting the shitpost into law grafted a falsifier the shitpost never carried; minting the ladder rib accepted in advance that a future rib may supersede it by name. You may not promote a text into a genre whose falsifier you are unwilling to accept. That sentence is this item's one-line theory of legal transition, and it explains why the estate's genre system has so few dead-text cleanup problems: nothing is allowed to enter a genre it cannot legally leave.

## 9. Literature anchors and verification status

Verified first-hand this session by my own crossref queries (section 1, run 3): Miller, "Genre as social action", Quarterly Journal of Speech, DOI 10.1080/00335638409383686, 1984. The genre-as-social-action frame holds here with one twist: the recurrent situations these genres typify are recurrent FAILURES, not tasks; the register is institutionalized scar tissue (the driving ladder from a correction streak, the frozen brief from a face-wearing incident, the census law from a 12-day stale headline). Searle, Speech Acts, Cambridge UP, DOI 10.1017/cbo9781139173438, 1969. Searle's constitutive formula "X counts as Y in context C" is literally the promotion gate: a receipt counts as filed in context operator GO; a shitpost counts as law in context slot graft plus falsifier grant; a prose claim counts as a census law in context the parse grammar matching.

Cited from training knowledge, NOT verified this session: Austin, How to Do Things with Words (1962), performatives; Bakhtin, Speech Genres and Other Late Essays (1986), primary vs secondary genres (receipts are primary, situated utterances; the constitution and the gate code are secondary, systematizing genres); Jakobson (1960), phatic and poetic functions, the shitpost's modality; Foucault, "The Order of Discourse" (1971), procedural control over who may speak, implemented here as the switchboard/effect-broker rule; Swales (1990), discourse community and its genre repertoire, implemented as the shared inbox contract table in AGENTS.md. Lessig needs no training citation: the constitution carries the frame itself (line 6) and the data-tier table (s7, lines 93-99) is the architecture modality written as law. The sibling verified Bazerman and Hart by crossref on its own run; those receipts are reused with attribution rather than re-run.

## 10. Not run, not found

- pytest not run: this item writes two markdown files and touches no code.
- Crossref: only the two queries recorded; anchors marked unverified in section 9 remain unverified.
- Container purity gate: not searched for in tools/; reported as not-found-in-what-was-read, not as absent.
- The 6 unread memory/law files (CONGESTION_COST, CRYPTOCOM_VAST_LOCK, GREYSWAN_BLADES, IMMORTALITY_SHARED, OBJECTS_ON_THE_BOARD, SHARE_WITHOUT_THE_SLUDGE): unread; no genre classification asserted for them.
- INDEX.json and SHARED_SURFACE_CONTRACT.json: not re-read by me; cited via the sibling's section 0 receipts with attribution.
- census_drift_patrol.py, githooks/pre-push, salon-ess artifacts: not read by me; cited via the sibling with attribution.

## 11. Own-receipts footer

Every claim above names a file read this session (section 1 list), a command run this session with its output (section 1 runs 1-4), or a sibling receipt reused with explicit attribution. Em/en dash scan and char counts: command and output recorded immediately below after the write.

## 12. Verification block

- Dash scan command (repo venv interpreter): python reads both files as utf-8 and counts U+2014 and U+2013. Result on the pre-append file: em=0, en=0 for both copies. This section is ASCII-only, so the appended file keeps em=0, en=0; the post-append scan output below is the final receipt.
- Mirror: w4-genre-theory.md is a byte-identical cp of w4-11.md (pre-append sha256 prefix 7d1ad9355f01 for both); final hashes below.
- Final char count of this file is reported in the run result JSON (a self-referential count printed here would change the count it reports).
