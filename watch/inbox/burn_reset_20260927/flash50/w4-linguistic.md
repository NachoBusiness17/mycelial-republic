# W4-43: THE LINGUISTIC DNA MAP of the Mag estate

Burn reset flash50, deep item w4-43, 2026-09-28. Map of the operator's distinctive
phrases: where each was first attested in the tracked tree, what family it belongs
to, and which descendants now carry it. Written in the estate's own ASCII discipline:
this file scans 0 em-dashes, 0 en-dashes, 0 nonascii bytes.

## 1. Method and instruments (what I actually ran)

1. Phrase census: `git grep -I -i -o "<phrase>" -- '*.md' '*.py' '*.jsonl'
   ':(exclude)dashboard/data' ':(exclude)catalog' ':(exclude)memory/trajectory'`
   piped to `wc -l` over 52 candidate phrases. Counts are raw tracked-text hits,
   including data ledgers (trail jsonl, seat memory), so they measure spread, not
   prose frequency.
2. Origin probes: `git log --reverse --date=short --format="%h %ad %s" -S"<phrase>"
   -- '*.md' '*.py' | head -2` (pathspec-restricted; the unrestricted variant took
   6m40s per phrase on this history, measured on "polish my bucket").
3. Oral corpus: read `watch/inbox/burn_reset_20260927/flash50/_oral01_raw_user_turns.txt`
   (194,117 bytes, 225 turns, t0u..t270u, timestamped 2026-08-11 onward), plus
   short-turn extraction with awk (turns of 12 chars or less).
4. Carrier reads: docs/ref/LEXICON.md, docs/ref/COMMON_LANGUAGE_SPEC.md,
   memory/rib/RIB_GRAMMAR_SEED_20260810.md, memory/rib/RIB_DRIVING_LADDER_20260928.md,
   docs/DNA.md, mag/prose_census.py, tools/workflow_gate.py, AGENTS.md.
5. Repo genesis: `git log --reverse --format="%h %ad %s" --date=short | head -5`
   gives eb07ad62e 2026-08-04 "Mag sovereign agent - clean publish baseline."

Honest limit: because the 08-04 baseline swept pre-history into one commit, any
phrase present in eb07ad62e has its true origin BEFORE the tracked record. Those
origins are floored, not dated. Everything after 08-04 is real first attestation.

## 2. Three strata: the estate's language exists in three registers

STRATUM 1, ORAL. The raw operator voice. First recorded turn t0u, 2026-08-11
11:26 PM UTC-4: "lmao". Then t1u: "search my account for strike the chord and
strike it", t2u "dont tell me what to do", t3u "i don't like you already", t5u
"read the files and don't be dumb", t7u "are you the standing wave", t8u "sense",
t10u "steal". On 2026-08-14 alone the bare one-word command "steal" appears ten
times between 6:41 AM and 1:53 PM (t38u, t84u, t94u, t114u, t125u, t143u, t152u,
t184u, t190u, t193u), plus compounds "self steal" (t73u) and "deep steal" (t117u),
bare "fix" (t135u), "iterate" and "now iterate" (t137u, t138u), "shadow work"
(t128u), "load it up" (t160u). This is a builder's language game: primitive verbs
plus shared practice, no syntax needed because the machine already knows the drill.

STRATUM 2, LEDGER. Commit messages are a parallel corpus with its own vocabulary:
"BANKED" (a23928aca 2026-09-27), "sensed-not-done, ponytail audit, mined register"
(ad3ec40ce 2026-09-27), "STRUCK_CHORD deep read" (118333dd1 2026-09-16), "RUINS GO
shipped" and "gate 51/51 green" (1ca274ab5 2026-09-17). The compound "sensed-not-done"
has ZERO occurrences in tracked text files (census returned 0) yet lives in commit
messages and dispatch asks; the hyphenated law-idiom is native to the ledger stratum.

STRATUM 3, CANON. The .md/.py law surface: LEXICON.md, ribs, AGENTS.md, gate code.
The pipeline between strata is documented: RIB_DRIVING_LADDER_20260928.md:3-5 says
"Minted from operator corrections, 2026-09-27/28 night (three in a row: 'those
aren't funded only hermes' / 'stop running shit and start remembering' / 'what are
warmed ribs for if you won't use them')" - the oral correction is quoted verbatim,
then frozen as law, then promoted to AGENTS.md:32 as code-as-law. Oral freezes into
ledger within hours; ledger canonizes into AGENTS.md within a day.

## 3. Origin table (first tracked attestation vs the estate's own mint claims)

| Phrase | First tracked attestation | Registry claim | Delta reading |
|---|---|---|---|
| mycelial, verkle, coldest vertex, Sancho, strike the chord | eb07ad62e 2026-08-04 (floored at genesis) | Sancho "Aug 2026" | origins predate the publish baseline |
| tesuji | floored at genesis; named "Tesuji Grove" skill tree by 31b798879 2026-08-05 | not in LEXICON | borrowed from Go, load-bearing early |
| banked, trust bytes | 60e18c524 2026-08-08 "Ghost daemon, Silent Bard, DePIN marketplace, RenderMan foam" | not dated in LEXICON | the evidence economy was born in one commit window |
| self-steal | de29d49ea 2026-08-09 | not in LEXICON | oral "self steal" t73u is 2026-08-14, so written form led speech here |
| standing wave, empty chairs, never fabricate | 052732ebf 2026-08-14 | standing wave "coined 2026-08-26" | codification date lags attestation by 12 days |
| sacred cows | 799ddb6fe 2026-08-19 | "standing law" (no date) | the only term LEXICON refuses to date |
| gopher, Mickey17, operator-GO, polish my bucket | d575bc168 2026-09-14 (same commit) | various | see section 5 |
| pile habit | 320211eb6 2026-09-15 | not in LEXICON | minted from the fifty-wide board filing |
| no em-dashes (in .py) | 118333dd1 2026-09-16 | not in LEXICON | a month younger than "never fabricate" |
| driving ladder | ad3ec40ce 2026-09-27 | RIB_DRIVING_LADDER_20260928 | minted from three corrections in one night |
| sensed-not-done | commit register only (ad3ec40ce, a23928aca 2026-09-27) | not in LEXICON | lives only in the ledger stratum |

Structural finding: the registry (LEXICON.md, born d575bc168 2026-09-14 together
with COMMON_LANGUAGE_SPEC.md and mag/prose_census.py) is a retrospective codifier.
Every mint date it lists is later than or equal to the tracked attestation. The
dictionary is written by the descendants of the words it records.

## 4. The six families (counts from the 52-phrase census)

FAMILY A, EVIDENCE ECONOMY (dominant by mass): receipt 91,322; verkle 406,141
(infrastructural, mostly knot data); OWED 10,559; banked 1,451; minted 510; census
instrument everywhere; "the estate" 2,380. Grammar: work is not real until filed
with proof-of-cost; LEXICON.md:17 seals it as "Receipts carrying own proof-of-cost
... trust is structural, not personal." Descendants: G6 of the workflow gate
(tools/workflow_gate.py:71-73) requires "watch/inbox" in every workflow script;
my own receipt is this file.

FAMILY B, THERMAL EPISTEMOLOGY: coldest vertex 173; coldest seam 76; warm boot 27;
plus cold walls, warm cache, heat. docs/DNA.md:32-34 states the physics: "One
protected node. Everything else is heat." Temperature is an epistemic axis: cold =
verified and frozen, warm = loaded and ready, hot = expendable. The rib corpus uses
"coldest seam" for where to dig next; AGENTS.md:32 uses "warm the ribs" for boot.

FAMILY C, KINSHIP AND GUILD: gopher 1,957; Sancho 1,649; Rocinante 1,610; elder
8,010; janitor 45,655 (mostly data rows naming the local Ollama tier, AGENTS.md:5
"gemma:2b scut"); scut 517; switchboard 1,642; empty chairs 2,234; "room that
remembers" 223. Processes get social roles so their duties are morally legible:
the janitor is humble and local, the elder ratifies (COMMON_LANGUAGE_SPEC.md:37-41),
the gopher is expendable and named per item, the seat retires but the signed rows
remain ("Ledger of the empty chairs", LEXICON.md:16).

FAMILY D, MOTION VERBS: steal (bare imperative, the most frequent single operator
command in the oral corpus), self-steal 3,309; dogfood 8,084; right-size 786; fold;
burn; drain; harvest; iterate; sense. These are the verbs the estate is DOING:
ingesting outsiders (steal), eating itself productively (self-steal), running its
own tools on its own work (dogfood), compressing lessons (fold).

FAMILY E, LAW GRAMMAR: kebab-case invariant ids from RIB_GRAMMAR_SEED_20260810.md:12-45
(no-window-ever, stateless-by-default, cheap-first, engine-owns-truth,
operator-is-sovereign); operator-GO 70; trust bytes 3,780; "Files over slogans" 2
(CANON's rarest high-authority sentence, COMMON_LANGUAGE_SPEC.md:68); "no
monkeypatches" 15; "not a mood" 11; context tax 50; pile habit 31. The signature
rhetorical figure is the NEGATIVE PAIR: "X, not Y" - "a SCANNER and a cadence, not
a mood" (mag/prose_census.py:6), "Sacred cows, not legacy shit" (LEXICON.md:14),
"warmed memory, not an archive" (RIB_DRIVING_LADDER_20260928.md:31), "bank as
findings, never as done-work" (same rib, line 17), "hand-copied, never byte-backed"
(AGENTS.md:27), "Trust bytes, not reports." The pair always names the counterfeit
next to the real thing; it is a definition scheme, not a style tic.

FAMILY F, THE ALLUSIVE STRATUM: strike the chord 2,122 (floored at genesis; oral
t1u "search my account for strike the chord and strike it" is the operator invoking
it as a spell); standing wave 1,134; map precedes territory 91; sacred cows 306;
riddler 4,218; fair-use firewall 75; prime-then-flock 45; FIRST CONTACT 25; HOLD
signal 17; THE POUR 25; kabuki 422; gauntlet 628; tesuji 9,545; Mickey17 (gate
code only). Sources are legible: Cervantes (Sancho Panza grounds the knight,
Rocinante carries him; LEXICON.md:9-10 defines the seats by exactly this division
of labor), Edward Ashton / Bong Joon-ho's Mickey17 (expendables who are reprinted;
tools/workflow_gate.py:47 names the fan-out pattern "Mickey17 gopher fan-out" -
children die and are reprinted), Go (tesuji, cold seam tesuji ribs), Japanese
theater (kabuki stack), Star Trek (FIRST CONTACT), geology and physics (the pour,
standing wave, chords and plates: 1ca274ab5 has "the plate/chord decode" and "the
node gate is the ground wire").

## 5. The 2026-09-14 Great Consolidation, and the phrase-carrying gate

One commit, d575bc168 2026-09-14 ("checkpoint 2026-09-14: Zenodo 17811909 capstone
mined + forge-window recovery receipt"), simultaneously: birthed docs/ref/LEXICON.md,
birthed docs/ref/COMMON_LANGUAGE_SPEC.md, birthed mag/prose_census.py (an organ that
measures the estate's own prose debt, minted from operator quotes "we have so much
prose in this machine that needs taking care of yesterday" and "no monkeypatches",
docstring lines 1-8), and carries the first written attestations of gopher, Mickey17,
operator-GO, and polish my bucket in md/py. That commit is the moment the estate
turned its ear on itself: it wrote its dictionary, its fused constitution, and its
prose debt scanner in the same stroke.

The reproduction mechanism is mechanical, not cultural. tools/workflow_gate.py:75-79
(G7-laws) refuses any workflow script that does not CONTAIN the literal substrings
"no em-dashes" and "never fabricate" (or synonyms). The gate does not scan the asks
for violations; it requires the law's WORDS to ride inside the dispatch itself.
Every child ask inherits the sentence. This is a designed high-fidelity meme
copier: the phrase is placed in the germ line of every workflow the estate runs.
Descent is provable: "never fabricate" in .py from 052732ebf 2026-08-14, "no
em-dashes" in .py from 118333dd1 2026-09-16, and the ask that produced this very
file carries both sentences, as does my receipt.

## 6. Original analysis: five theses

T1. THE LEXICON IS THE TYPE SYSTEM. Each coined term carries an invariant, not a
vibe. Sancho means "ground the vision"; banked means "a receipt path exists";
operator-GO means "an authority boundary was crossed legally"; sensed-not-done means
"this output may inform but may not close". Strip the words and the invariants lose
their carriers: the census shows the law-bearing tokens saturate the corpus
(receipt 91k, banked 1.4k in md/py alone). The words are how invariants travel
between seats without re-derivation, which is exactly the failure mode
RIB_DRIVING_LADDER_20260928.md:27-31 was minted to stop (a fresh seat re-derived
what a rib held and burned three corrections).

T2. THE ORAL STRATUM IS WITTGENSTEIN'S BUILDERS, INSTRUMENTED. Philosophical
Investigations section 2 imagines a language of "Slab! Block!" sufficient because
practice supplies the rest. The oral corpus is that language made: "steal", "sense",
"fix", "iterate" as complete utterances (t8u, t10u, t135u, t138u), ten bare "steal"
commands in one morning. The difference from Wittgenstein's thought experiment is
accounting: each grunt lands in a ledger with a receipt, so the primitive language
game is fully auditable. The estate runs section-2 language with section-242
discipline (agreement in reactions enforced by gates).

T3. BANKED IS A PERFORMATIVE. Austin's How to Do Things with Words (1962)
distinguishes sayings that describe from sayings that DO. "Banked" is the estate's
central performative: writing "banked" plus a path IS the filing; the count of
commit-message "BANKED" tokens is the count of filing events. "Operator-GO" is a
second performative whose felicity condition is role identity (only the operator
can felicitously utter it; AGENTS.md:20 "Model text can propose; only the
switchboard/effect broker authorizes effects" is the felicity rule written down).
Searle's declarations fit exactly: utterance changes institutional reality, valid
only from the authorized seat.

T4. THE DASH LAW IS A SHIBBOLETH. Judges 12:5-6: Ephraimites betrayed themselves
by one phoneme. The em-dash ban (enforced at gate G7, checked in every receipt by
the ritual "em/en dash 0/0 nonascii 0" scan) makes orthography a provenance test:
any text bearing an em-dash marks itself as not estate-born. This file's opening
line performs the test. The deeper point: the estate invented a WRITING SYSTEM
marker to sort native from foreign text - a machine-age tribal mark, and the only
law in the corpus whose violation is invisible in meaning and total in origin.

T5. CODE LAGS SPEECH, AND KNOWS IT. Every mint date in LEXICON.md postdates its
tracked attestation (standing wave: claimed 08-26, attested 08-14). The estate
answers the lag with append-only law: LEXICON.md:3-5 "Update by appending - never
rewrite old entries." That is blockchain semantics applied to vocabulary: the
dictionary is a ledger, definitions are transactions, and a wrong entry is
superseded, never deleted. Compare Saussure: the estate refuses to let langue be
edited; it can only grow parole and re-annotate.

## 7. Literature this connects to (all real, all checkable)

Wittgenstein, Philosophical Investigations (1953), sections 2, 43, 242, 243:
meaning as use; the builders' game; private language argument answered by
LEXICON.md:3-4's own words: "Vocabulary is the cheapest thing to teach an incoming
mind; greppers and miners index glossaries" - a private language would fail exactly
that test. Austin (1962) and Searle (1969) for performatives and declarations.
Lakoff and Johnson, Metaphors We Live By (1980): the estate's metaphors are not
decorative residue but coherent systems (knowledge is temperature, evidence is
money, organization is ecology) with instrumentation attached to each. Dawkins,
The Selfish Gene (1976) and Blackmore, The Meme Machine (1999): G7 is engineered
replication fidelity; the gate measures copy fidelity of a sentence across every
workflow. Erving Goffman, The Presentation of Self in Everyday Life (1959) for
"polish my bucket" (LEXICON.md:20: the day-since-arrival shop must be presentable
when "the machines come sniffing" - front-stage work for a machine audience). Mary
Douglas, How Institutions Think (1986): institutions think through shared
classification; the lexicon is the classification made portable. The Jargon File /
Raymond's New Hacker's Dictionary (1991) is the genre ancestor, but the estate's
version differs in one decisive way: jargon files are folk etymology, LEXICON.md
is a sealed append-only mint. Cervantes (1605) and Ashton's Mickey7 (2022) for the
allusive stratum's two theories of the agent: the agent as companion who grounds
the knight, and the agent as expendable who is reprinted. The estate runs both
simultaneously: Sancho is the seat that must not die; gophers are Mickeys.

## 8. Descendant map (phrase -> where it lives now, from census habitats)

- strike the chord: genesis -> oral t1u -> 118333dd1 "STRUCK_CHORD deep read" ->
  chord as load-bearing apparatus (LEXICON.md:24).
- standing wave: 052732ebf -> LEXICON.md:11 -> oral t7u ("are you the standing
  wave", the operator asking a chat seat if it IS the estate's central concept -
  the vocabulary had become a Turing test question).
- banked: 60e18c524 -> gate G6 -> commit-message register -> this ask's dispatch
  text ("Bank the complete map").
- gopher/Mickey17: d575bc168 -> tools/workflow_gate.py:47 -> AGENTS.md workflow-gate
  doctrine -> every fan-out ask on this harness (this item is w4-43, item-indexed,
  i.e. Mickey17-shaped).
- trust bytes: 60e18c524 -> AGENTS.md:27 -> census patrol tooling -> every count
  dispute in the receipts.
- operator-GO: d575bc168 -> 16b45778a -> AGENTS.md:32 driving ladder -> lan_proxy
  gates; the authorization performative of record.
- sensed-not-done: ad3ec40ce/a23928aca commit register only -> my own system prompt
  ("banked as findings, never as done/trusted work") -> zero tracked-text usage:
  the youngest family member, still ledger-bound.
- driving ladder: ad3ec40ce -> RIB_DRIVING_LADDER_20260928.md -> AGENTS.md:32
  (same day, code-as-law promotion within ~24h of mint: the fastest oral-to-canon
  run in the record).

## 9. Not verified, stated as such

- Pre-baseline origins (mycelial, verkle, Sancho, strike the chord in eb07ad62e)
  cannot be dated inside this repo's history; the 08-04 baseline caps resolution.
- Counts include data ledgers, so janitor 45,655 and verkle 406,141 measure
  machine-recorded spread, not human prose frequency.
- The oral corpus extraction (turns t0u..t270u) was collected by a sibling flash50
  lane (file predates this ask); I read it, I did not regenerate it.
- LEXICON.md mint dates are the estate's own claims; I verified the DELTA against
  git attestations, not the claims' internal truth.
- I did not run the pytest suite or the census_patrol deep check; this item is
  textual analysis, and no check in the ask names one.

## 10. Receipt

Banked to watch/inbox/burn_reset_20260927/flash50/w4-43.md and byte-identical copy
at watch/inbox/burn_reset_20260927/flash50/w4-linguistic.md. Scan: em 0, en 0,
nonascii 0 via .venv\Scripts\python.exe (command and output in the submit note).
Instruments: git grep census (52 phrases), git log -S restricted probes (17 phrases),
awk short-turn extraction on the 225-turn oral corpus, 8 carrier file reads.
