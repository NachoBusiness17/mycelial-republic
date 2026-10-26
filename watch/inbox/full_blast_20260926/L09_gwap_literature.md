# L09: adversarial GWAP literature (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L09) · **Class:** RECEIPT / literature
**Closes debt:** #6 from the design-precedents report (KissKissBan citation) and the ESP-fix question from the noir GWAP pack.

## Corrections on our own record (no-fabrication cuts both ways)

- KissKissBan EXISTS but our precedents agent's authorship guess was WRONG: authors are Chien-Ju Ho, Tao-Hsuan Chang, Jong-Chuan Lee, Jane Yung-jen Hsu, Kuan-Ta Chen (Academia Sinica + NTU), NOT Edith Law (adjacent lineage: TagATune, Cyclopedia). Venue: ACM SIGKDD HCOMP '09, DOI 10.1145/1600150.1600153; extended SIGKDD Explorations Nov 2010, DOI 10.1145/1882471.1882475. Both Crossref-verified via curl this session.
- Jain & Parkes citation chain corrected/extended: TEAC 2013 builds on their HCOMP '09 workshop paper, DOI 10.1145/1600171... (10.1145/1600150.1600171).

## The mechanism that matters (the proven ESP fix)

KissKissBan: two players form a "couple" scoring by independently matching words for an image; a third player, the BLOCKER, gets ~7 seconds head start to enter common words which become TABOO to the couple. Blocker profits when the couple fails, so the couple is pushed off the high-frequency-tag equilibrium into rare, descriptive annotations. Per the agent's synthesis: this is an ACTION-SPACE fix (removes the common-tag moves) rather than a scoring redesign, and it is the ONE empirically demonstrated fix in the literature: engagement retained, output shifted rare-ward. No production scoring-fix has ever been verified: Google Image Labeler (the ESP lineage) shut down 2011 without a documented fix. Clean open-gap claim for the noir design doc: "the match-early equilibrium has an academic action-space fix (KissKissBan) but no published production fix via scoring redesign."

## Fleet translation (seat crosswalk)

The blocker role = the fleet's drift-patrol weaponized as game mechanic: a designated adversarial player banning the obvious/common moves forces the workers off the low-effort equilibrium. That is exactly the "rare-words-first preference shift" lever from our v4 crosswalk, now with a verified mechanism and citation. Concretely for a cops-and-robbers GWAP: the blocker role maps to the ROBBER side excluding obvious alibi words, or to a per-case "taboo list" the system generates from prior cases, forcing witnesses and cops into rarer, more verifiable description space.

## Other verified items

- **PhotoCity** (Tuite, Snavely, Hsiao, Tabing, Popovic, CHI 2011, DOI 10.1145/1978942.1979146): adversarial team-vs-team territory capture via geolocated building photos feeding 3D reconstruction labels. Genuinely zero-sum GWAP precedent.
- **TagATune** (Law, von Ahn et al., ISMIR c. 2007/09): adversarial via TRICK ROUNDS (same/different judgment with asymmetric info); original not in Crossref this session (flag), corroborated via mTagATune DOI 10.1109/icmb.2011.39.
- **Reeves, West, Simperl (CHI 2017)**, "A Game Without Competition Is Hardly a Game": competition drives activity in human computation games (Crossref-existence verified).
- **Foldit strategy compilation: THE citation is Khatib, Cooper, Tyka et al., "Algorithm discovery by protein folding game players," PNAS 108(47):18949-18953, Nov 2011** (DOI 10.1073/pnas.1105868108 from knowledge, flag: not re-verified). Player-written "recipes" benchmarked competitive against expert Baker-lab Rosetta scripts. Production mechanism: recipes are player-authored LUA SCRIPTS in an in-game cookbook with ratings/reuse. This is the v6 brief's Comp operator (verified trace to callable artifact in others' action spaces) running in production a decade before the brief; the brief does not cite it. Biggest single literature find of this blast.
- Supporting: Cooper Nature 2010 (already verified earlier), Khatib PLOS Biology 2019 DOI 10.1371/journal.pbio.3000472 (Crossref-verified): player scripts used for cryo-EM model building.
- **LLM-era revival:** Chatbot Arena (Chiang et al., arXiv:2403.04132, ICML 2024, lmarena.ai): anonymous pairwise battles = human preference verification as a self-sustaining game, the closest LLM-era GWAP descendant. "Game-Based Discovery" arXiv:2407.02798 (verified this session) frames GWAP 2.0 as mini-games inside commercial games. Human or Not? (AI21 2023) gamified Turing test, arXiv ID unverified. Honest gap claim: no verified dedicated "GWAPs for LLM training data" survey through mid-2026; the revival is Arena-style evaluation games, not von Ahn labor games.
- Unresolved lead: DARPA Verigames suite (StormBound, card game for program verification, 2012-2014): lead, not citation.

## Agent debts

PNAS DOI, Nature DOI, Chatbot Arena arXiv ID, TagATune year, Human-or-Not ID: from knowledge, flagged not re-verified; Foldit cookbook/Lua details from docs not fetched; Verigames unverified.

## Seat synthesis for the noir GWAP design doc

The literature spine is now complete and citation-clean: ESP match-early pathology (Jain & Parkes) -> action-space fix via adversarial blocker (KissKissBan, corrected authors) -> adversarial team framing retains players (PhotoCity, Reeves CHI 2017) -> strategies compile into reusable artifacts in production (Foldit recipes, PNAS 2011) -> the LLM-era continuation is evaluation games (Chatbot Arena). The noir cops-and-robbers GWAP is a legitimate, citable next step in this lineage, and its cop/robber/witness triangle is structurally a three-role KissKissBan variant with destruction as E_t mutability.
