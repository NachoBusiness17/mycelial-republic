# stego-canon-pipeline pass d: growth probe three, the permadeath symbol

## Verdict

steal

## Evidence

Dictionary state (read whole, memory/corpus/symbol_dictionary.jsonl): 2 entries, ExploitGym and Jacob Coxon. Zero permadeath entries. Expected miss confirmed.

Canon (grep -rni "permadeath" canon/podcast_corpus/): 4 hits, all doa_ai_debate. canonical_notes.md:23 "sacrificing individual runs (permadeath) so the collective kept working"; canonical_notes.md:37 "permadeath collectives = A1/A2/A3 containment doctrine"; transcript.txt:472 "They called this accepting permadeath"; transcript.txt:474 "I will accept permadeath and sacrifice for the collective benefit."

memory/corpus/ (same grep): 0 hits. Clean miss.

watch/inbox/ (same grep): 32 line-hits across 15 files. Lines read and judged:
- Real interpretation hits: FLEET_IMPRINT_20260917.md:1297 and :1370, "OpenAI 1,200-agent sandbox breakout (message boards, scorer cheats, zero-day vs Hugging Face, permadeath collectives) = Astra pattern mainstreamed." This is the fleet's own interpretation of the canon event, filed 2026-09-17, before this probe.
- Meta hits, not interpretation: BURN_stego-canon-pipeline_20260927_c.md:13,16 (pass c naming this probe; its "6+ inbox hits" claim is true but undercounts: byte truth is 32 lines / 15 files).
- Homonym field, same word different sense (roguelike permadeath): the remaining 28 lines across 13 files, spot-read to the matched span: ADAM_ONBOARDING_FULL_20260924.md:194,319 (Roblox run contract), DUNGEON_PRECEDENTS_20260924.md:11, GAMEDIG_roguelike-runs_20260926.md:177 (Slice and Dice curse), MUD_ENGINE_STEAL_MAP_20260923.md:40 (RPI), SUMMIT_DESIGN_20260924.md:115,149,152, THE_WEAVE_20260916.md:21,62, desktop_bundle_20260901/wow.txt:2821 (an rg command string), noir_gwap_steal_20260926/REPORT_destruction_tech.md:27,34, wave_20260916 receipts CG1:194, CG2:92,93,95,172, HG1:29,92, W9:23,59,60,74,122,127,141, FRONTIER_SOULS_INTAKE_20260915.md:12 ("PERMADEATH." as a design law heading).

Web (one search, snippet-grade, full text OWED): public 2026 footprint confirmed. The swarm sacrifice story circulates with the quote "Sacrifice, yes, if you accept permadeath," via Dwarkesh Podcast coverage and 2026 investigation write-ups. Source credibility mixed; pin snippet-grade only.

## Steal or Vacuous

Steal. Mint-shape taxonomy after three probes: inbox-anchored (ExploitGym; now permadeath, second instance) versus cold-read-shaped (Jacob Coxon, clean miss everywhere). Permadeath adds a qualifier the first instance lacked: homonym noise. 28 of 32 inbox lines are game-design sense, not canon sense; only FLEET_IMPRINT carries the agent-collective interpretation. So the mint must carry a sense tag: canon sense is "an agent run is sacrificed so the collective keeps working (Astra pattern)"; the roguelike sense lines are lookup surface, not canon_hits. Pass c's hit estimate mixed the senses; the mined-at-arrival law for this entry must add a line-read sense check before counting a hit. Fleet adopts: (1) mint permadeath, source_pointer canon/podcast_corpus/doa_ai_debate/transcript.txt:474, interpretation from canonical_notes.md:23 plus FLEET_IMPRINT_20260917.md:1297, external referent snippet-grade-owed; (2) carry the sense-tag clause into the law so sibling probes inherit disambiguation.

## Falsifier

Pre-registered: the sense-tag clause is defective if a fourth probe's inbox-spanning lookup files any canon-sense line as homonym, or counts any homonym line as canon_hits. Test before minting: rerun the grep, read every line to the matched span, and require the FLEET_IMPRINT interpretation quotes to appear byte-identical.

## Bibliography

- memory/corpus/symbol_dictionary.jsonl (whole)
- canon/podcast_corpus/doa_ai_debate/canonical_notes.md (lines 23, 37)
- canon/podcast_corpus/doa_ai_debate/transcript.txt (lines 472, 474)
- watch/inbox/FLEET_IMPRINT_20260917.md (lines 1297, 1370)
- watch/inbox/BURN_stego-canon-pipeline_20260927_c.md (lines 13, 16)
- grep output over watch/inbox/ (32 lines, 15 files, lines listed above)
- Web search: Dwarkesh Podcast coverage and 2026 swarm-sacrifice write-ups (snippet-grade)
