# LINGUISTIC DNA MAP (deep-linguistic-dna)

**Filed:** 2026-09-28, flash50 wave, seat deep-gopher. **Ask:** extract every distinctive operator phrase, trace its origin, map its descendants (code, receipts, behavior), and separate load-bearing from decorative.

## 0. Method (everything below was run in this session)

1. Full-history phrase archaeology: `git log --reverse --date=short --format="%h %ad %s" -S"<phrase>"` for "trust bytes", "pile habit", "context tax", "coldest vertex" over 656 commits (`git rev-list --count HEAD` = 656, pack 6.11 GiB per `git count-objects -vH`).
2. Estate text census: a Python scanner (temp script, run with `.venv/Scripts/python.exe`) over 6,378 files / 72.6 MB, case-insensitive counts of 46 phrases bucketed by layer: code (mag/, tools/, scripts/, tests/, configs/, queue/, dashboard/), doctrine (docs/ + root *.md), memory (memory/continuity + memory/rib + memory/improve + top-level memory files), receipts (watch/*.md + watch/inbox/*.md top level), corpus (corpus/steal). Per-file read cap 5 MB; canon/, catalog/, attic/ excluded from the voice analysis (they are library, not estate voice). Caveat: a full tracked-tree `git grep -i -l "trust bytes"` finds 312 files; the 93-file census figure is the scoped-scan number.
3. Commit-message census: same 46 phrases against all 656 commit messages, oldest first, to date the register.
4. Origin-commit verification: `git show --stat 8f9beb69c` and `git show --stat 6dfd35673`.
5. Machine-metadata reads: `memory/percolator/invariants.json` and `dashboard/static/lattices/invariants.json`, `tools/census_drift_patrol.py`, `mag/diary.py`, `mag/corpus_ingest.py`, `main.py`, `mag/state_snapshot.py`, `tests/test_freshness_gate.py`, `tests/test_grave_classify.py`.

## 1. The three named phrases

### 1.1 "Trust bytes, not reports" (the mechanized one)

**Origin.** First tracked entry: commit `60e18c524` 2026-08-08 ("sovereign architecture: Ghost daemon, Silent Bard, DePIN marketplace, RenderMan foam"). Machine capture: the percolator invariant `a77444ced5abc2e7`, text `[steer] Verify with git diff / actual file bytes before declaring done. Trust bytes, not reports.`, `count: 446`, `first_seen: 2026-08-31T12:34:41Z`, `last_seen: 2026-09-28T17:40:50Z` (memory/percolator/invariants.json:67-71). That is today: the phrase is a live steering vector, injected into sessions and counted 446 times.

**Descendants.** (a) Probe trail: `dashboard/static/lattices/invariants.json:78` carries the invariant plus dozens of `pro-<id> -> ok|fail` event rows (lines 86-283), i.e. the phrase has its own pass/fail telemetry. (b) Code: 76 of 127 census hits are in code (the strongest code-share of any doctrine phrase measured). (c) Doctrine: the AGENTS.md census bullet ("Trust bytes, not reports"), and "never trust a hand-written count" (3 hits). (d) Behavior: it is the stated reason every receipt names commands and outputs.

**Verdict: LOAD-BEARING, maximally mechanized.** Of the whole phrase population, it is the only one present in the percolator invariant store (grep for coldest vertex / sacred cow / parable / pile habit in that file: zero rows). It crossed from prose to invariant to probe events. In Austin's terms (How to Do Things with Words, 1962) it is a performative that has been compiled: saying it is checking it.

### 1.2 "No sacred cows" (the procedure-generating one)

**Origin.** Operator trigger, verbatim: "the september 20th date is a sacred cow you are missing aton here. make this representative self steal go deep." (memory/continuity/seat_memory_20260927/sacred-cow-audit-sep20-20260918.md:10-12). Origin commit verified: `git show 6dfd35673` = 2026-09-18 09:48 EDT, "SACRED COW AUDIT Sep-20 ... DATE PROVENANCE LAW filed", adding watch/inbox/SACRED_COW_AUDIT_SEP20_20260918.md (77 lines).

**Descendants.** 166 census hits (84 receipts, 42 memory, 33 code). The audit killed a false cliff (the Sep-20 z.ai promo expiry accreted ceremony) and minted the DATE PROVENANCE LAW: every board date is EXTERNAL, COORDINATION, or ACCRETED ("cows, milked for urgency, shot on audit"). It is now correction law #10 in `.agents/skills/operator-corrections/SKILL.md:36`: "NO SACRED COWS. Every past decision was the best understanding at the time. Re-evaluate." Commit-message layer: 2 commits carry it, both 09-18.

**Verdict: LOAD-BEARING as a procedure generator.** It has no single gate, but it demonstrably manufactures other laws (DATE PROVENANCE LAW) and audits. Its force is episodic: it exists to be invoked at moments of accretion.

### 1.3 "The crab on the magistrate's road" (the deliberately unmechanizable one)

**Origin.** Operator parable, given 2026-09-18: "The crab feels that the magistrate's road was made for its scuttle. The magistrate smiles and the mountain has forgotten more roads than the magistrate has records for." (memory/continuity/seat_memory_20260927/crab-and-magistrate-parable.md:10-13). The alignment append that banked it: `git show 8f9beb69c` = 2026-09-18 08:55 EDT, adding 47 lines to watch/inbox/STEINIGER_OPERATIONAL_STEAL_20260918.md.

**Descendants.** A three-layer decode (crab = us, magistrate = record-keepers, mountain = substrate), an operator verdict that pairs it with the estate's own Bach crab ("Bach's crab = the TEST ... the magistrate crab = the LAW", parable file lines 51-57), a week-later operator-commissioned constitutions essay (crab-magistrate-constitutions-essay-20260925.md, "Crab reading: ... the pinch is the feature"), and the rarest event in the estate's linguistic record: **transfer across the boundary.** An external reader (M.P. Steiniger) "ADOPTED THE CRAB CANON natively: reading papers as roadmap = crab behavior" (memory/corpus/LINKS.jsonl:16). The parable also spawned a self-catch class ("the wrong-crab lesson", parable file lines 45-49) and adjectival productivity ("crab logic", "crab behavior", "both crabs"). Census: crab 178 hits, magistrate 88; both first enter commit messages 2026-09-18 (`8f9beb69c`).

**Verdict: LOAD-BEARING and deliberately NOT mechanized.** The operator verdict says it outright: "humility no byte-check delivers" (parable file line 56). This is the estate's meta-law about the limits of its own favorite move (byte-trusting). Decorative by the gate criterion, load-bearing by every other one: it changed how the fleet reads papers, how it frames asks ("Ask the walker"), and how an outside physicist now describes himself.

## 2. Census: the lexicon by layer

| phrase | TOT | code | doctrine | receipts | memory |
|---|---|---|---|---|---|
| receipt | 12103 | 4033 | 425 | 6543 | 963 |
| verkle | 9415 | 3391 | 657 | 1562 | 3787 |
| owed | 3720 | 830 | 114 | 2308 | 428 |
| landed | 1528 | 385 | 22 | 653 | 449 |
| janitor | 1054 | 468 | 143 | 239 | 204 |
| mycelial | 713 | 240 | 146 | 170 | 157 |
| parable | 788 | 153 | 43 | 367 | 224 |
| pack-first | 349 | 21 | 33 | 8 | 287 |
| artifact > transcript | 275 | 8 | 6 | 1 | 260 |
| banked | 438 | 183 | 11 | 180 | 64 |
| coldest vertex | 128 | 56 | 4 | 49 | 19 |
| trust bytes | 127 | 76 | 4 | 29 | 18 |
| sacred cow | 166 | 33 | 7 | 84 | 42 |
| crab | 178 | 6 | 1 | 103 | 68 |
| seat purity | 55 | 8 | 14 | 2 | 31 |
| chat is heat | 45 | 8 | 16 | 13 | 8 |
| warm the ribs | 1+3 | 0 | 1 | 0 | 2 |

Scanned 6,378 files / 72.6 MB, 5 MB/file cap; receipts = watch/*.md + watch/inbox/*.md top level; canon/catalog/attic excluded.

The layer skew is itself a finding. "pack-first" is 287/349 memory; "artifact > transcript" is 260/275 memory. The living language concentrates in memory/continuity and receipts, not in docs/ (the doctrine column is near zero for most phrases). The official documentation tree is already a fossil layer of the estate's own language; replication happens in memory and code.

## 3. The four registers (families), with literature anchors

**Legal-accounting register** (receipt, owed, landed, banked, superseded, void, wart, proven): first appears in commit messages 2026-09-14 ("receipt": d575bc168; "landed": 99826e153), "banked" 2026-09-25. This register is only two weeks old and already dominates: "receipt" sits in 106 of 656 commit messages and 2,264 files. It is enforced semi-mechanically by the workflow gate (receipt landing in watch/inbox/ is a gate check per AGENTS.md build discipline). Literature: Lessig's code-as-law, applied literally; the estate keeps its own port at docs/ref/lessig_1_6.md (law/norm/market/architecture modalities mapped onto moves 1-6).

**Craft/style register** (no em-dashes, no not-X-but-Y tics, canon language, "moon man language", no AI tells): enforced by tests, not vibes: tests/test_freshness_gate.py:288 (`test_module_has_no_em_dash_in_filed_text`) and tests/test_grave_classify.py:142 (`assert "\u2014" not in row["justification"]`); prompt contracts carry it too (scripts/gopher_packs.py:133 "operator craft law: no em-dashes in operator-facing text"; scripts/union_fullsend_day.py:72 "No em-dashes. Do not explain the parable after telling it."). The moon-man correction (2026-09-18, memory/continuity/seat_memory_20260927/moon-man-language-correction.md) is a translation duty: external jargon must land in fleet canon first (Go board, cache mining, lens physics, moonshots) or it reads "handwavy". Literature: Orwell's "Politics and the English Language" (1946) as style-as-thought, upgraded to style-as-provenance: the style laws are anti-AI-tell watermarking (author-mask-stego-method: Made-with-AI beacon public, stego mark private). Hofstadter and Sander's Surfaces and Essences (2013) argues analogy is the core of cognition; the moon-man law mandates analogy-first as policy.

**Biology register** (mycelial 713, mycelium 578, janitor 1054, residual, DNA, rib, spore, knot): the founding metaphor family. "Janitor" (the product's actual first principle: local Ollama janitors first) has 468 code hits, the largest doctrine-to-code pipeline measured. The source genre is the mycology canon in the corpus library (primary-documents-canon-20260916 lists a mycology shelf; Sheldrake's Entangled Life and Stamets' Mycelium Running are the obvious reference points for hyphae/residual/spore vocabulary). "Warm the ribs" is the newest organ of this register.

**Physics/game register** (coldest vertex, atari, kifu, move 37 = A1, lens, the pour, closure tax, context tax): "coldest vertex" is founding vocabulary, present in the first publish baseline (`git log -S "coldest vertex"` oldest = eb07ad62e 2026-08-04 "Mag sovereign agent, clean publish baseline"), and the estate preserves its coinage utterance as code provenance: mag/corpus_ingest.py:4 quotes the operator verbatim ("those are coldest vertexes are they not...", 2026-08-12). The Go cypher anchors to AlphaGo's move 37 (2016), repurposed as "the dead-looking stone that anchors everything" (S_core = -8 at A1). "Context tax" (also first tracked 60e18c524 2026-08-08) names a real mechanism, not a mood: mag/rightsize_all.py:94 "RC cache, context tax (the big lever)", mag/session_freeze.py:5 "paying the context tax once", mag/session_maze.py:5. Lakoff and Johnson's Metaphors We Live By (1980) claims abstract reasoning is metaphor all the way down; this estate goes further and makes the metaphor the module name.

## 4. Load-bearing vs decorative: the estate's own criterion

The estate has already defined the test, from outside: Steiniger's invariant, recorded at LINKS.jsonl:16: "whatever survives transfer without losing shape was identity; whatever does not was decoration." Transfer-losslessness is the definition of identity, testable. Applying it to the lexicon, plus a teeth criterion (does a gate, test, parser, or command depend on it):

| phrase | teeth | transfer | verdict |
|---|---|---|---|
| trust bytes, not reports | invariant + probes + test-era census law | operator to seats to probes to AGENTS.md | LOAD-BEARING (mechanized) |
| census carrier grammar "N tests collected / M files (YYYY-MM-DD census" | parsed by tools/census_drift_patrol.py:118 regex; fail-closed exit 2 "need the claim shape" (B2-249) | prose grammar is a machine contract | LOAD-BEARING (parse-tight) |
| coldest vertex | mag/diary.py:212 greps docs/DNA.md for the literal lines "Fidelity lives" / "Residual is" / "Coldest vertex"; rewording the doc orphans the diary's origins line. Also prompt text in mag/autonomous_research.py:63,90,184,231 | founding vocabulary, quoted in code | LOAD-BEARING (parse-tight) |
| pile habit | main.py:4645 `pile-classify` command into tools/pile_classify; mag/state_snapshot.py:75 `capture_summary` | AGENTS.md clippy bullet | LOAD-BEARING (command surface) |
| context tax | names the cache architecture (session_freeze, session_maze, rightsize_all) | operator coinage to design principle | LOAD-BEARING (names the mechanism) |
| no king | embedded law strings: mag/operator_os.py:22, mag/republic_os.py:12 and :119 (Redlock lock docstring), mag/story.py:97 | constitution phrase inside code | LOAD-BEARING (architecture) |
| no em-dashes | two tests assert on emitted text; prompt contracts carry it | style law with test teeth | LOAD-BEARING (mechanized) |
| steal / probe / fold / verify / dispatch / sign / wash | verb genomes L0 contract is marked "byte-stable; do not reword" (docs/ref/verb_genomes/L0_contract.md); workflow gate enforces the receipt verb on runs | frozen lexicon | LOAD-BEARING (by contract) |
| receipt / owed / landed / banked | workflow gate receipt check; register in 2,264 files | operator to fleet-wide register | LOAD-BEARING (the operating dialect) |
| no sacred cows | no direct gate; mints audits and laws | correction law #10 | LOAD-BEARING (procedure-generating) |
| duplication is emphasis | no gate; actively blocks consolidation proposals (MEMORY.md doctrine) | operator teaching 09-18, verbatim preserved | LOAD-BEARING (normative) |
| parables are the spec | citation protocol: sweep the parable canon before re-deriving doctrine | operator's published X posts treated as T1 primary docs (THE_PARABLE_REGISTER, 9 spec'd) | LOAD-BEARING (normative) |
| moon man language | no test can assert "not handwavy" | craft law | LOAD-BEARING (normative, partially testable) |
| crab / magistrate / mountain | explicitly refused teeth ("humility no byte-check delivers") | crossed the boundary (Steiniger adopted it) | LOAD-BEARING (meta-law), unmechanizable by design |
| warm the ribs / warmed ribs | 1 to 4 hits, minted 09-27/28 (RIB_DRIVING_LADDER_20260928 quotes the operator: "what are warmed ribs for if you won't use them") | boot-order prose only | YOUNG: load-bearing intent, decorative instrumentation so far |
| no core-mirror throne | 5 hits, Zeitgeist tombstone guard | deletion mark | DECORATIVE but functional (a grave marker is supposed to be inert) |
| you're so close / worth the whole night | 5 hits each, quoted praise used as memory hooks | reinforcement signals | DECORATIVE (mood), reproducible |
| portrait of the operator / operating system of record | 0 hits anywhere in the estate | none | NOT ESTATE LANGUAGE (the ask's examples only; reported as found-zero) |

## 5. Original findings

**1. The language is compiled, in three depths.** The same estate runs three compiliation pipelines for phrases: full mechanization (trust bytes: prose to invariant to probe events to counted behavior, first_seen 2026-08-31, last_seen today, count 446), parse-tightness (the census carrier grammar and the DNA.md origin lines that mag/diary.py:212 and tools/census_drift_patrol.py:118 literally regex), and deliberate refusal of mechanization (the crab: "humility no byte-check delivers"). A healthy sign: the estate assigns each phrase its depth on purpose rather than by accident, and the operator verdict on the crab states the assignment explicitly.

**2. Load-bearing language is fragile, and the fragility is the feature.** B2-249 documents that editing the AGENTS.md census bullet to any other grammar "breaks the gate instead of silently rephrasing it" (tools/census_drift_patrol.py fail-closes exit 2, "need the claim shape"). Same shape in mag/diary.py:212: reword "Coldest vertex" in docs/DNA.md and the daily origins line goes blind. This is Wittgenstein's meaning-is-use (Philosophical Investigations §43) turned into a build breaker: the meaning of the sentence IS its parse. The estate knows, and rather than loosening the coupling it registered the coupling as law (carrier shape law). Consequence for maintainers: doctrine prose in parse-tight spots is code. Diff it like code.

**3. The register dates are stratigraphic.** Founding layer (2026-08-04/08): coldest vertex, context tax, trust bytes, verkle, janitor, mycelial. Legal-accounting layer (2026-09-14/25): receipt, landed, banked, owed as commit-message grammar. Parable layer (2026-09-16/18): parables are the spec, crab/magistrate, sacred cow, moon man, duplication is emphasis. Rib layer (2026-09-27/28): warm the ribs, remember before running, driving ladder. The lexicon accretes in bursts that coincide with organizational phase changes (publish baseline, factory era, operator-correction era, funding-truth era), which is Dawkins-meme evolution with a ratchet: mutations are kept only when they land in memory plus receipts, and the violation ratchet (pre-push hook) does to code debt what the receipt register does to speech debt.

**4. One-way translation is the load wall.** The moon-man law requires external jargon to be translated INTO canon (Steiniger's Dirichlet energy became "the go board"; his proper time integral became the operator's own aphorism "the road gets shorter by walking it", 8 hits, which the estate notes he uttered before reading the physics). Almost nothing translates OUT: the canon terms (pack-first, artifact > transcript) appear in receipts only 8 and 1 times respectively, while memory carries 287 and 260. The language is engineered to be sticky inward and opaque outward. That is sovereignty practice in the Lessig sense: the estate's concepts are natively expressible only in its own tongue, which makes capture by outside framings structurally harder. Cost: every new seat must be steeped (the rib system exists to pay that cost once).

**5. The two crabs compose the epistemology.** Bach's crab (the record must read the same forwards and backwards: replay determinism, byte checks) and the magistrate crab (the record is the tally, never the mountain) are respectively the estate's verification doctrine and its humility doctrine, delivered as one parable pair and confirmed live when the seat's "wrong" reach for its own crab canon was ruled "duplication is emphasis", not error (parable file lines 51-61). The linguistic DNA's deepest law is that its two halves contradict on purpose: trust bytes absolutely, and hold the bytes as maps, never as the mountain. Everything else in the lexicon is one of those two moves wearing a different coat.

**6. Watch items (owed by this map).** (a) "warm the ribs" is 5 days old with zero instrumentation; if it is real doctrine it needs a boot gate (the estate's own pattern: prose that matters gets teeth within a week, see census carrier law). (b) The census grammar lives in one bullet of one file with a single parser; a second independent consumer would make it robust rather than fragile. (c) The parable register (788 hits, 282 files) has a register file (THE_PARABLE_REGISTER, 9 spec'd) but no automated drift check that new parable-derived doctrine cites its parable; the "wrong-crab lesson" self-catch is currently manual. (d) This scan read 72.6 MB of an estate whose watch/ alone is 7.9 GB; deep-file (post-5MB) occurrences are undercounted by construction, and canon/ corpus text was excluded as library rather than voice. Both caveats bound the census, not the genealogies, which were each verified at the source file and commit level.

**Sources read this session (primary):** memory/continuity/seat_memory_20260927/{crab-and-magistrate-parable.md, sacred-cow-audit-sep20-20260918.md, duplication-is-emphasis-20260918.md, parables-are-the-spec-20260916.md, moon-man-language-correction.md, crab-magistrate-constitutions-essay-20260925.md}; memory/corpus/LINKS.jsonl:16; memory/percolator/invariants.json:67-96; dashboard/static/lattices/invariants.json:76-283; docs/DNA.md; docs/ref/OPERATOR_CARD.md; docs/ref/lessig_1_6.md; docs/ref/verb_genomes/L0_contract.md; memory/rib/RIB_DRIVING_LADDER_20260928.md; mag/{corpus_ingest.py:1-20, diary.py:200-225, clippy.py:55, rightsize_all.py:11,94, session_freeze.py:5, session_maze.py:5, operator_os.py:22, republic_os.py:12,119, story.py:97,270, autonomous_research.py:63-231, state_snapshot.py:75, fermat_ractor.py:265,473, republic.py:449}; main.py:4645-4646; tools/census_drift_patrol.py:93-208; tests/test_freshness_gate.py:288; tests/test_grave_classify.py:5,142; scripts/{gopher_packs.py:133, union_fullsend_day.py:72,92}; .agents/skills/{operator-corrections/SKILL.md:36, verb-genomes/SKILL.md}; AGENTS.md (workspace instructions). **Commands run:** the census script and greps listed in section 0, all executed 2026-09-28 in this session; nothing cited above was taken on a report's word without opening the file or running the query, except the four literature anchors (Austin 1962, Wittgenstein PI §43, Lakoff/Johnson 1980, Dawkins 1976, Hofstadter/Sander 2013, Carse 1986, Lessig 1999, Orwell 1946, Sheldrake 2020), which are cited from general knowledge as connections, not as estate claims.
