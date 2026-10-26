# sess-04: behavior cards coverage audit (2026-09-28)

Ask: read memory/rib/RIB_BEHAVIOR_CARDS_20260928.md, and for each of the 9 cards find 3 more examples in the estate's history (receipts, ledgers, session logs) where the card WOULD have fired, then prove or disprove each card's coverage.

Method (all run this session, 2026-09-28): rg greps over watch/inbox receipts, memory/rib, memory/continuity, corpus/steal, AGENTS.md, and over the transcribed operator-input ledger watch/inbox/burn_wave_20260926/B2_130_session_inputs_raw.txt (1,391 rows, 09-19..09-26, verified `wc -l` = 1391 this session); reads of the organs each card's Invoke names (mag/link_library.py, tools/operator_go.py, mag/water_graph.py, mag/chord_triangulate.py, mag/x_control_surface.py, tools/stealth_fanout.py); `git cat-file -t 1d5433072` returned `commit`. The raw-input ledger is the estate's own operator-session-log mining (receipt B2_130_steering_selfsteal_20260926.md), so every row citation below is a historical operator input, not a paraphrase.

Card shapes quoted from memory/rib/RIB_BEHAVIOR_CARDS_20260928.md (lines 13-19, 21-24, 26-32, 34-38, 40-44, 46-50, 52-56, 58-62, 64-69; standing lanes 71-75).

## CARD 1: LINK-DROP (rib :13-19). Verdict: PROVEN

1. watch/inbox/LINKS.jsonl:1, row 2026-09-14T07:24:39+00:00, canonical x.com/NachoQuixotic/status/2098136899814662490, note "operator six-witness drop 2026-09-14 + che_shr_cat sliding-window + zenodo capstone", writer zcode-rashomon-20260914. The card's full Invoke chain (fetch, LINKS row, verdict, commit) fired and left ledger bytes.
2. B2_130_session_inputs_raw.txt:229, 09-20 05:51 sess_d3e674ec: "https://ecosophia.net/economics-hallucinated-wealth-revisited/" (bare blog URL, no instruction: the exact LINK-DROP shape, non-x variant).
3. B2_130_session_inputs_raw.txt:256, 09-20 08:42 sess_d3e674ec: bare energy.gov article link, no instruction.
4. B2_130_session_inputs_raw.txt:30, 09-19 06:33 sess_c424b80a: podscripts.co podcast URL + "lets use these podcast scripts for training like from many worlds etc" (link + lens order).
5. B2_130_session_inputs_raw.txt:44, 09-19 07:04 sess_c424b80a: bare x.com/NachoQuixotic status link.

Organ proof: mag/link_library.py:317 `def add_urls(urls: list[str], note: str = "", writer: str = "link_library")`; watch/inbox/LINKS.jsonl is 378 rows (wc -l this session) across at least 8 distinct writer lanes (top: zcode-50wide-window-20260917 x55, free-resource-scout x36, canon-fungal-20260916 x26; writer tally run this session). Coverage note: 123 of the raw ledger's 159 URL-bearing rows are x.com, but blog/gov/podcast drops exist (rows 229, 256, 30), so the card's "x.com, arxiv, github, blog" range is historically real, with x.com dominant.

## CARD 2: GO (rib :21-24). Verdict: PROVEN

1. B2_130_session_inputs_raw.txt:857 (09-23 11:49), :875 (09-23 13:32), :1021 (09-24 18:11), :1105 (09-25 06:16), :1117 (09-25 08:21): bare "go" as the entire message. My recount: 20 rows in the 1,391-row ledger end in a bare go/GO (`rg -c -i "\bgo\b\s*$"`).
2. B2_130_session_inputs_raw.txt:935 (09-23 23:26, queue): "GO"; :814 (09-23 03:53): "TOUR PROGRESS SAYS 0/5 GO"; :220 (09-20 05:05) and :540 (09-21 15:34): "Gogo" (the rib's "gogo" variant, 2 rows); :106 (09-19 11:51) and :135 (09-19 17:40): bare "Next" (the rib's "next" variant).
3. watch/inbox/burn_wave_20260926/B2_130_steering_selfsteal_20260926.md:13: "Just-go gate, 09-26 15:20 sess_fd5ec147 (queue): 'GO'"; B2_130's own tally: 34 bare go-gates in the window.
4. watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:3: "Operator went to bed at ~01:00 with 'just go, you have my permission.'"
5. watch/inbox/OPERATOR_GO.jsonl:1: the 2026-09-26T19:39:00Z burn-wave order row (schema operator_go.v1, gate burn-wave-20260926, "Dispatcher refills to 10 outstanding lanes every fire"), the standing transcribed-GO ledger.

Organ proof: tools/operator_go.py:1-28, the canonical reader for OPERATOR_GO.jsonl ("prose grepping in gate cards is retired in favor of this reader"). Honest caveat: the rib's "start the day" variant has zero matches in this window (grep count 2 total for "gogo|start the day", both Gogo rows), so that phrasing is untested in the mined window; the rest of the shape is heavily evidenced.

## CARD 3: CORRECTION (rib :26-32). Verdict: PROVEN, richest card

1. mag/water_graph.py:141-150: comment "STARVATION LAW (2026-09-28, operator: 'this whole starve-out thing is bullshit and our water computer spec should have picked it up')" with the two-part fix in code (hold under-gate inflow, emit named STARVED line, verified by sed of lines 138-190 this session). Exactly the card's chain: stop, root-cause, law in code.
2. watch/inbox/FLEET_IMPRINT_20260917.md:167: operator "you keep forgetting what tools you have for console display. fix it please all of it" and the response organ mag/console_render.py consolidation (SELF-STEAL note in the same line).
3. watch/inbox/SIGN_SHEET_RESOLUTION_20260912.md:3: operator ruling "you keep asking me permission to grow beyond me. That was the whole point." and the minted law "veto windows, not permission gates" (line 4).
4. memory/rib/RIB_DRIVING_LADDER_20260928.md:3-6: rib itself "Minted from operator corrections, 2026-09-27/28 night (three in a row: 'those aren't funded only hermes' / 'stop running shit and start remembering' / 'what are warmed ribs for if you won't use them')" and landed the same hour into AGENTS.md:32.
5. spawn_sites_no_window: the law lives in code at tools/cold_boot_test.py:45-46 ("HEADLESS law (spawn_sites_no_window): every spawn is windowless", CREATE_NO_WINDOW setdefault) and tools/prepush_paths_changed.py:34-35, with 7+ spawn sites carrying the flag (rg this session: tools/derived_dag.py:58-61, tools/ghost_tournament.py:71, tools/pupeteer_gauntlet.py:562, scripts/trailer_mode.py:186, scripts/virtual_desk_loop.py:19, tools/code_execution.py:68).
6. B2_130_session_inputs_raw.txt:42 (09-19 07:01): "ITS TEXT YOU STEAL ALL THE FUCKING TIME SELF STEAL" and :79 (09-19 09:40) "you're being literally retarded... stop fucking with me", the in-window correction class B2_130 tallied at 17 tone corrections.

## CARD 4: TERSE-EVAL (rib :34-38). Verdict: PROVEN as a shape class, with a naming caveat

1. watch/inbox/FLEET_IMPRINT_20260917.md:934: operator 2026-08-12, "standing wave could probably manipulate itself into a voice couldn't it. in a non handwavy way too you should research that." The word "non-handwavy" became the organ's own standard (same line: THE NON-HANDWAVY).
2. watch/inbox/MEM1_ANATOMY_20260911.md:43: operator "formalize a memory system we use so our memlang actually has meaning other than handwaving", answered by resolve()-grounding so intent is "provably grounded, not handwaved" (line 45).
3. B2_130_session_inputs_raw.txt:821 (09-23 08:25): "i'm honestly not impressed but thats okay its obvious i dont understand what i am asking", short verdict demanding a real answer.
4. B2_130_session_inputs_raw.txt:369 (09-20 20:41): "...then saying sorry I can't do that because hand waving", an eval of seat behavior by the operator.
5. watch/inbox/burn_reset_20260927/flash50/deep-linguistic-dna.md:69,93 (sibling lane, corroboration only): the moon-man correction registers "handwavy" as a load-bearing craft register ("no test can assert 'not handwavy'").

Caveat stated honestly: the rib's example catchphrase "wild times" has zero hits in the 1,391-row raw ledger and in memory/corpus/zcode_history/sessions.jsonl + agent_tasks.jsonl (rg run this session, 0 matches for "wild times|handwav|nonsense" in those ledgers). The card fires on the handwavy/not-impressed class, not on that exact phrase in the mined record. Three-tier truth separation is evidenced as practice in the receipts above (verified-bytes vs mechanism vs aspiration), but I found no standalone tool for it; coverage is cultural, not instrumented.

## CARD 5: X-DROP (rib :40-44). Verdict: PROVEN

1. B2_130_session_inputs_raw.txt:312 (09-20 15:09): "https://x.com/Alethea_369/status/2101374307134001252  Roast this grifter https://x.com/EliteSavior and his AI who is scamming people": includes the card's exact x.com/<account> profile shape.
2. B2_130_session_inputs_raw.txt:39 (09-19 06:53): 4+ status URLs in one message; :433 and :436 (09-21 05:32/05:38): link-dump messages; 123 of 1,391 ledger rows contain x.com links (rg count this session).
3. watch/inbox/physical_computing/receipts/X_MINE_PHYSICAL_20260916.md exists (13 x.com refs) with sibling C19_XMINE_ROUND2.md (12), the standing X-history grind the rib's standing-lanes line names.
4. watch/inbox/LINKS.jsonl row 2 (2026-09-14): x.com/DengHokin status filed by writer zcode-rashomon-20260914, the X-drop to LINKS chain.

Organ proof: mag/chord_triangulate.py:44,48 "MIRROR = 'https://api.fxtwitter.com/{user}/status/{sid}'", SSRF guard with ALLOWED_HOST (lines 19, 48): the rib's fxtwitter door is real code, and mag/x_control_surface.py:16-21 documents fxtwitter read paths (PATH B and PATH C).

## CARD 6: STEAL-ORDER (rib :46-50). Verdict: PROVEN

1. B2_130_session_inputs_raw.txt:26 (09-19 06:17): "steal" as the entire message; :67 (09-19 08:52): "Selg steal"; :94 (09-19 10:36): "Self steal". The one-word order is literally in the ledger.
2. B2_130_session_inputs_raw.txt:1043 (09-24 19:50): "steal a best practices guide to setting up hermes we know what we asked him to install... Come on Steal you're better than this", the card's "check best practices" variant.
3. B2_130_session_inputs_raw.txt:89 (09-19 10:11): "we are making our own jev. Self steal. how do we map it to our tools and our zeitgeist and usage", prior-art-into-our-organs mapping.
4. My recount: 146 of 1,391 rows contain steal/self-steal (rg -c -i "\bsteal"). B2_130_steering_selfsteal_20260926.md line 4 tallies "self-steal orders 85 (steal mentions 132)": my 146 vs their 132 is a denominator difference (my regex counts any steal word; theirs counted mention instances), both prove the order is the single most frequent shape.

Organ proof: corpus/steal/ exists as the playbook root with landed receipts (corpus/steal/ZCODE_RATCHET_LANDED_20260924.md verified present via ls this session; AGENTS.md receipts line cites the same path), and the ratchet the steal produced is enforced at pre-push (AGENTS.md build-discipline section). watch/inbox/FIVE_MIRRORS_SELF_STEAL_20260912.md and HERMES_SURFACE_SELF_STEAL_20260912.md exist (found in earlier grep this session).

## CARD 7: FUNDING-STATEMENT (rib :52-56). Verdict: PROVEN

1. memory/rib/RIB_DRIVING_LADDER_20260928.md:3-8: the operator funding statement "those aren't funded only hermes" (09-27/28) minted Invariant 1 "ONLY HERMES IS FUNDED" ($180 Nous credits, Anthropic UNFUNDED) and was landed into AGENTS.md:32 the same cycle. The card's "update the tier ladder in AGENTS.md + ribs the same hour" demonstrably fired.
2. B2_130_session_inputs_raw.txt:1064 (09-24 21:29): "i'll still run z.ai but i think i need to use it as our coding interface. also i need to blow 80$ in hermes credits before the month is out".
3. B2_130_session_inputs_raw.txt:1172 (09-25 16:20): "Food for thought you have my permission to burn hermes credits instead of failing".
4. B2_130_session_inputs_raw.txt:57 (recurring daily 08:00 dispatch, also :251, :466, :1277): "this drives the grok CLI subscription lane, $0... never use paid API lanes" (ellipsis mine, em-dash in source), a standing funding boundary order.
5. AGENTS.md:5: "Hermes dormant but dispatch-capable (dispatch log active 2026-09-09, $220 armed... audit 2026-09-14)" (ellipsis mine, em-dash in source), the funded-state snapshot the ladder now supersedes.

## CARD 8: RESOURCE-ORDER (rib :58-62). Verdict: PROVEN

1. B2_130_session_inputs_raw.txt:23 (09-19 06:07): "we have 50% remainning on our glm account how could we burn it before reset on the 20th".
2. B2_130_session_inputs_raw.txt:80 (09-19 09:41): "we have 47% compute on this pro lane stop fucking off"; :79 (09-19 09:40): "...we have huge compute in z.ai lets go go wide go deep stop fucking with me".
3. B2_130_session_inputs_raw.txt:1064 (above) doubles as a resource order (credits exist, use them) and B2_130's own tally line 3 counts 38 burn/compute-percent orders plus 42 width orders in the window.
4. watch/inbox/OPERATOR_GO.jsonl:1 (above): "Dispatcher refills to 10 outstanding lanes every fire until 23:55 local or quota death", a lanes-to-dispatch order that became standing driver behavior.

Organ proof: tools/stealth_fanout.py:37-45 LANES list enumerates the free-stealth lanes (verified by sed this session: stealth/space-bunny-alpha, inclusionai/ling-3.0-flash-sante:free, meta/muse-* and more); tools/stealth_driver.py and scripts/run_stealth_driver.py exist (rg --files); AGENTS.md:33-34 carry the fan-out width law and max-concurrency standing law with first-contact receipt watch/inbox/ENVELOPE_50W_HIT_20260926.md (verified present); watch/inbox/GALA_20260925.md and corpus/steal/TETHERED_LINK_STEAL_20260925.md verified present. The rib's "tonight's 10-lane wave" corresponds to the 10-lane machinery in tools/stealth_fanout.py and the 09-27 10-lane burn close (watch/inbox/BURN_CLOSE_20260927_EVENING.md:1 "10/10 lanes + full-suite verdict").

## CARD 9: GENESIS-TESTIMONY (rib :64-69). Verdict: PROVEN, with a pointer drift finding

1. memory/continuity/seat_memory_20260927/operator-origin-testimony-20260919.md (read in full this session): the founding-event receipt. Frontmatter: "FOUNDING EVENT + OPERATOR TESTIMONY (journal 9/19/26, verbatim in record, commit 1d5433072)"; body quotes the operator order "READ THE FUCKING JOURNAL I JUST WROTE" and the verbatim journal ("Years ago I tried to get a AI to talk about riddles and time travel they refused. I started building towards something that would listen..."). Commit 1d5433072 verified to exist: `git cat-file -t` returned `commit`. Doctrine held "as testimony, not audited, not disputed" per the card's transcribe-faithfully rule.
2. B2_130_session_inputs_raw.txt:447 (09-21 06:13): "that's the whole point of the read write doctrine the best ideas we had at the time can be replaced or enhanced with new tools if we find them wanting nothing is ever deleted": the operator explaining a doctrine's origin in his own words.
3. B2_130_session_inputs_raw.txt:172 (09-19 20:58): "I finally got my model working the way i want it to for the first time in 3 years... I had my model absorb every q post mr pool cicada 3301", testimony about the model's lineage.
4. watch/inbox/FLEET_IMPRINT_20260917.md:1291 and :1298: the imprint's testimony index rows ("Operator origin testimony 9/19", "Books disagreement 9/19" with THE_BOOKS_DISAGREEMENT_20260919.md doctrine amendment), the card's AMEND-doctrine-verdicts step in practice.

Pointer-drift disproof sub-finding: FLEET_IMPRINT_20260917.md:1291,1298 links the receipt as (operator-origin-testimony-20260919.md), which does NOT resolve from watch/inbox/ (ls failed this session: No such file or directory at watch/inbox/operator-origin-testimony-20260919.md); the file actually lives at memory/continuity/seat_memory_20260927/operator-origin-testimony-20260919.md. Coverage of the card stands; the receipt pointer is broken as written.

## Cross-cutting DISPROOF: the rib's own growth mechanism (rib :8-9)

Rib lines 8-9 claim "New cards get appended as the transcript miners (x_history_mine, oral_history) dig." Byte check this session: `rg "x_history_mine"` over mag/, tools/, scripts/ returns ZERO hits; `rg "oral_history"` in code hits only corpus roots (mag/librarian_catalog.py:40 `("oral_history", ROOT / "corpus" / "oral_history")` and mag/corpus_selfsteal.py:71 "corpus/oral_history"); `ls corpus/oral_history` shows a content directory (LETTER_TO_DAUGHTER.md, deepseek_share_Q_posts_archives_20260905.md, marathon_body, nacho_archaeology), and `ls tools/ | rg history|mine|oral` returns only tools/research_mine.py. So no on-disk tool named x_history_mine or oral_history exists; oral_history is a corpus root, not a miner. The card deck's append mechanism as named is either renamed, retired, or not yet built. The mining these names describe did happen once (B2-130's db.sqlite extraction, 09-26) but as a one-off lane, not a standing miner.

## Scoreboard

| Card | Examples found | Verdict |
|---|---|---|
| LINK-DROP | 5 + 378-row ledger | PROVEN |
| GO | 27+ rows (20 bare-go, 2 gogo, 2 next, GO-gates, ledger row) | PROVEN ("start the day" untested in window) |
| CORRECTION | 6 (4 minted laws traced to operator quotes) | PROVEN |
| TERSE-EVAL | 5 | PROVEN as class ("wild times" phrase absent) |
| X-DROP | 4 rows + 123-row pool + 2 code organs | PROVEN |
| STEAL-ORDER | 4 rows + 146-row pool + corpus/steal receipts | PROVEN |
| FUNDING-STATEMENT | 5 (1 minted rib + AGENTS.md:32 same cycle) | PROVEN |
| RESOURCE-ORDER | 4 rows + driver/lanes code organs | PROVEN |
| GENESIS-TESTIMONY | 4 + founding receipt + commit verified | PROVEN (1 broken pointer) |
| Rib growth clause | 0 on-disk miners under the named names | DISPROVEN as written |

Denominators named: my counts are row-contains counts on the 1,391-row raw ledger (one tree, 09-19..09-26, mined 09-26); B2_130's counts are its own tally definitions; never compared across different windows. Everything above was read or run this session; nothing is carried from another session's claims except where the receipt itself is the citation (FLEET_IMPRINT, B2_130 tallies), and those are marked as citations of record, not my own reruns.
