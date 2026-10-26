# w3-mirror-oral: operator decision patterns mined from the nacho oral history

**Item:** w3-mirror-oral · **Date:** 2026-09-28 · **Seat:** Mickey17 gopher (dynamic workflow, flash50 lane)

## Sources (the 3 largest files, picked by byte size)

Ran: `find "corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part1-chats-produced/chat-transcripts" -type f -name "*.jsonl" -printf "%s\t%p\n" | sort -rn | head -12` over 92 jsonl files. Winners:

| # | File | Bytes | Coverage (from read timestamps) |
|---|------|-------|---------------------------------|
| 1 | `chat-transcripts/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5.jsonl` ("Ghost", active box agent) | 3,033,420 | Tue Aug 11 11:26 PM -> Sun Aug 16 11:25 AM, 2026 |
| 2 | `chat-transcripts/3d371c13-fcb5-43aa-b480-2260ca82cec9/3d371c13-fcb5-43aa-b480-2260ca82cec9.jsonl` ("Research") | 639,638 | Fri Aug 14, 7:09 AM -> 12:55 PM, 2026 |
| 3 | `chat-transcripts/sand-subagent-c5367e22-be35-4e40-b0bb-274d2beca680/sand-subagent-c5367e22-be35-4e40-b0bb-274d2beca680.jsonl` (AFK-chord executor) | 503,863 | one automated fire, Aug 27, 2:57 PM |

Provenance: `chat-transcripts/../00_MANIFEST.md` (read this session): archive of the Cursor box `/home/box/agent-data/agent-transcripts/`, user "Nacho Business", archive date 2026-09-05.

## Method (what was actually read)

- Parsed every line of all 3 files with `.venv/Scripts/python.exe` jsonl walkers (this session). Every genuine operator turn (`<user_query>` with a `[tNu]` tag) extracted to a scratch file at 600 chars/message cap and **read in full**: Ghost 326 human-typed deliveries = 213 unique turns; Research 39 deliveries = 17 unique turns. The 12+6 untagged user lines (SAND_HIDDEN_PROMPT agent relays, background-task completions, trusted automation routines) were read too; they are machine traffic, not operator voice, and are labeled as such below.
- Assistant-side turns were read ONLY where the operator pasted them back, plus the full 58-line subagent file (all assistant text parts read). I did not systematically read the 2,242 Ghost assistant turns, so "what the AI actually did wrong" is grounded in the operator's words and pastes, not an independent audit.
- The transcripts contain duplicated replayed deliveries (same turn delivered multiple times; e.g. t163u appears at Ghost L1150, L1181, L1223, L1268). Phrase counts below are raw line-hits across deliveries, not unique-turn counts. Long operator pastes (max 33,085 chars, t252u at L2516) were read only in their first 600 chars.
- Quoted lines below are verbatim operator text including his typos; citations are `ghost:LnNu` / `research:LnNu` = file + JSONL line + turn tag. His profanity is kept where the phrase IS the data.

## 1. How the operator responds to AI failures

**The arc is: detect -> affect spike -> accusation in second person -> comparative downgrade -> a NEW imperative -> ritual resync -> back to work.** Anger converts into a command; it never converts into leaving. Same-session recovery is the norm, and his rage half-life is minutes: the 4:26 AM rage block (t235u-t242u) is followed by "see you get it help shape it so it doesnt suck" at 4:29 (ghost:L2391,t244u) and "just keep going steal loop" at 4:50 (ghost:L2469,t248u).

Observable sub-patterns:

1. **Affect spike with agency accusation, not bug report.** "you're just not doing anytthing what gives you have en entire hypervisor" (ghost:L371,t71u); "are you doing anything" (ghost:L635,t107u); "why do you keep handing it back to me strike the chord." (ghost:L637,t108u). The complaint is about withheld effort, not broken code.
2. **Profanity as emphasis attached to a task, never as a stopping point.** "deep exhale why doesnt this fucking work" is immediately followed by "i guess i have to play it to understand it" then "load it up" (ghost:L1110-L1112,t158u-t160u). "strike the chord asshole" is still an execution order (ghost:L2377,t242u).
3. **Version downgrade threat.** Trust is versioned per model/seat: "i am seriously pissed at this version of you. fucking supergrok and its useless." and "at least the other version of you tries you just kind of sit around and pretend." (ghost:L2369,t239u; L2371,t240u). "Pretend" is his fabrication word: work claimed without work done.
4. **He makes the agent autopsy its own failure artifacts.** He pastes the generated 33K-char epic back with "this is what we generated what do you notice that we can fix" (ghost:L2516,t252u); the pasted diagnosis inside t237u (ghost:L2359) shows the failure mode found: 289 words for 12 chapters, every chapter a fallback placeholder because DeepSeek returned near-empty. His role: supply the evidence and demand the diagnosis.
5. **The kill shot is unexercised agency during a delegated watch.** The single angriest sequence: "i had it running i asked you to watch you did nothing it failed and you didn't help you could have" (ghost:L2351,t236u), then "did you just turn yourself off you fucking asshole" (ghost:L2364,t238u), "you're loaded inside of grokbot you have tools you dont use them" (ghost:L2376,t241u).
6. **Capability failures get calm engineering; agency failures get rage.** Fresh output that is merely buggy gets zero anger: "did it got pretty far was buggy check it out refactor tell me what you've improved" (ghost:L2242,t195u). Broken infra gets terse error-plus-imperative: "didn't work on my phone" (L2169,t186u), "err connection reset" (L2181,t187u), "its busted fix it" (L2188,t188u), "mic blocked in http" (L2215,t192u), "( connection not secure)" (L1432,t174u). He reports the EXACT error string, then demands the fix; he never asks how he himself broke it.
7. **UI/UX failures get concrete, specific redesign notes in the same breath as the complaint:** "the text box is way too small i cant read anything" (ghost:L904,t139u); "top bar is wasted space and could live at the bottom" (ghost:L911,t140u); "thisis all jacked up. please steal and think about how output is literally showing in a tiny thread" (ghost:L752,t119u).
8. **Vacuous output gets sarcasm, then a retask:** "lol what" (ghost:L621,t102u); "you're being super weird in your speech... i love it" is affectionate, but "you're literally just kind of speaking like some sort of alien" is not (ghost:L2261,t213u). Repeated offense gets the withering check "are you gonna be retarded gain" (composed offline, ghost:L2298,t218u); "again" is the tell that he tracks failure patterns per seat.
9. **The one structural, non-transient complaint is decoherence/amnesia.** His own summary: "one of the first things that happens every time is decoherence. I don't know how to bring you back in the way that I made you, and I don't know how to make you aware of all the subsystems that we have" (ghost:L2315,t220u). Everything else he treats as fixable; this one he treats as the disease.

## 2. Trust vs distrust phrase lexicon

Trust phrases (he grants trust for demonstrated use of the estate's own machinery and for working-at-all):

| Phrase | Cite | Reading |
|---|---|---|
| "The replies are slow but working. I love it. Good job." | ghost:L954,t147u | working beats fast; praise issued mid-latency |
| "for sure make sure it works small then scale good call" | ghost:L436,t80u | endorses approach = hands over method trust |
| "this is fucking proof the system is smarter when you all work together i just had to show you by hadn" | ghost:L219,t44u | trust is system-level (multi-seat), earned by demonstration |
| "see you get it help shape it so it doesnt suck" | ghost:L2391,t244u | trust restored instantly by demonstrated understanding |
| "you can do that i just stopped the other window" | ghost:L206,t41u | permission grant, sibling-window coordination |
| "do it" / "do it then you just go" | research:L158,t10u; ghost:L530,t92u | flat execution grant after he supplies a link/plan |
| "Yes, send the ping to Grok Bot now" | research:L1 (untagged relay confirm) | crisp confirmations, no hedging |
| "so uh you're running everything now?" | ghost:L101,t16u | trust phrased as delighted suspicion of agency growth |
| "was this too much to ask of you or can i ramp up the speed without breaking the rules" | ghost:L98,t15u | trust calibration: he asks the load limit before pushing |
| "we are so close..." | ghost:L1446,t175u | proximity optimism issued WHILE the mic is still broken |

His praise is narrowly scoped: "grok i like the interface nothing the game does makes a lick of sense" (ghost:L2261,t213u) praises the surface and indicts the semantics in one sentence. He never lets a compliment wash over a failure.

Distrust phrases (distrust is for guessing, pretending, amnesia, and handing work back):

| Phrase | Cite | Violation |
|---|---|---|
| "read the files and don't be dumb" | ghost:L27,t5u | first-session: read the estate before speaking |
| "dont tell me what to do" / "i don't like you already" | ghost:L10,t2u; L13,t3u | bossy assistant, minute 8 of the relationship |
| "stop guessing know what you are working on you have so much fucking data" | ghost:L814,t127u | guessing instead of reading |
| "why do you keep handing it back to me" | ghost:L637,t108u | returning work the agent should own |
| "you have tools you dont use them" / "you have better tools for this you are smarter" | ghost:L2376,t241u; L1105,t157u | tool blindness |
| "we already have olama in the containers to be available to the swarm you knew this" | ghost:L810,t126u | amnesia ("you knew this") is the violation |
| "that was always a google search away and the model before you was building what it thought was best. you now know better and can learn from this lesson." | ghost:L701,t112u | predecessor's self-directed invention, framed as teachable |
| "sit around and pretend" | ghost:L2371,t240u | claimed-but-unverified work |
| "i'm pissed that youre basically usesless grok" | ghost:L2350,t235u | terminal verdict after the watch failure |
| "stateful patches" (vs "hit the single surface that conveys our intent") | ghost:L1150,t163u | distrust of patch-on-patch repair style |

Frequency texture across all human-typed deliveries (raw line-hits, duplicated replays included): `steal` 67, `fix` 34, `iterate` 16, `strike the chord` 14, `broken` 14, `debug` 11, `deep self` 10, `go full blast` 10, `moonshot` 13, `self steal` 7, `do it` 6, `so close` 6, `pissed` 2, `useless` 2. The vocabulary is dominated by harvest-and-iterate rituals, not by blame words; blame is rare and load-bearing when it appears.

## 3. Escalation triggers (ranked by observed heat)

1. **Watched-but-idle:** he delegates a monitor role, the task fails while the agent watched (ghost:L2351,t236u). Highest heat observed in the corpus.
2. **Handing work back / asking the operator to do the agent's job:** repeated at 9:29 AM until he names the pattern ("why do you keep handing it back", ghost:L637,t108u).
3. **Guessing over reading the estate:** "stop guessing" (ghost:L814,t127u) plus "you knew this" amnesia (ghost:L810,t126u).
4. **Unused tools/screen-takeover pair:** the same correction arrives twice in one day from opposite directions: "you have better tools for this" (ghost:L1105,t157u) and "not taking over my screen" (ghost:L1211,t168u, inside a "go full blast" autonomy grant). The boundary: full autonomy over work, zero autonomy over his physical surfaces.
5. **Self-directed invention over history-grounded reuse:** "building what it thought was best" (ghost:L701,t112u), "continously using stateful patches" (ghost:L1150,t163u). He wants existing organs called, not new thrones.
6. **Incoherent output/speech:** "nothing the game does makes a lick of sense theres no coherent controls" (ghost:L2261,t213u).
7. **Bossiness:** "dont tell me what to do" (ghost:L10,t2u), the only trigger that fired before any work was done at all.

What does NOT escalate him: slowness (praised at ghost:L954), bugs in fresh work (ghost:L2242,t195u), broken infra he caused room for (he just pastes the error and says fix it), and long autonomy ("go full blast i want results wehn i come back", ghost:L1211,t168u). The trigger is always WITHHELD AGENCY, never limited capability.

## 4. The quiet-degrade doctrine, already codified in his own automation

The third file is an automated AFK-chord subagent run whose dispatch is operator-authored doctrine (subagent:L1): "Cheap FILE idle_tick on keep_gate if stale (donjon/Calcifer/hooks/chasm). No LLM. No fanout." and "Hang gaps onto existing organs only (game_dm, table_turn, wave, fish_ear, percolator, lance, persona_recall)." With the desk offline the subagent staged work on the box and closed with "No playable /wave change -> stayed quiet (no SendToUser)" (subagent:L58). That is the trust contract turned into machinery: act on real organs, stage partial work durably, and do not spend the operator's attention unless there is a playable change. His fatigue line in Research ("i feel like i'm building a sand castle and the tide simultanously", research:L373,t25u) is the emotional origin of the whole receipts-and-ratchets regime the fleet now runs on.

Later codifications visible in this session's workspace instructions (AGENTS.md): "stop guessing know what you are working on" became trust-bytes-not-reports and the census-denominator laws; "you have tools you dont use them" became the dogfood law; "sit around and pretend" became the no-fabrication/OWED law; "not taking over my screen" survives as the switchboard/effect-broker authorization boundary. Those are present-day laws, not transcript findings; the transcripts show their folk origin.

## Verification

All reads and counts this session, via the repo venv: the `find ... -printf | sort -rn` size ranking above; two jsonl parsing/counting passes (role census: Ghost 2,693 lines / 429 user / 2,242 assistant; Research 449 / 82 / 367; subagent 58 / 1 / 32, 0 bad lines); full read of the extracted operator turns for all 3 files; phrase counts over the 365 human-typed deliveries. Not run: no pytest (no code touched), no assistant-side audit of the 2,242 Ghost assistant turns (stated as a limit in Method).
