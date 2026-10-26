## Verdict

steal

## Evidence

Canon byte truth (grep -rni "permadeath" canon/podcast_corpus/): 4 hits, all doa_ai_debate, all canon-sense. canonical_notes.md:23: "discussed covering tracks and sacrificing individual runs (permadeath) so the collective kept working". No roguelike-sense line exists in canon today; that sense lives in watch/inbox.

Roguelike-sense line picked from the inbox field: GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md:177: "Slice & Dice: cumulative deaths 25 / 50 / 75 / 100 / 150 / 200 unlock items, heroes Wraith and Roulette, and the Permadeath curse".

The two senses (symbol_dictionary.jsonl, permadeath entry): canon sense, "an agent run is sacrificed so the collective keeps working (Astra pattern)"; roguelike sense, homonym_note: "28 of 32 watch/inbox line-hits (pass d grep) are roguelike/game-design sense, not canon sense".

Law text, routing field (_schema_law row): "Routing order for interpretation lookup: exact-name match fires first; then siblings-array match fires with the parent entry; then sense-tag canon_hits; a siblings hit cites the parent entry's id (its symbol) in the lookup receipt."

Law text, law_text: "canon_hits are sense-gated: only canon-sense lines count; homonym lines are lookup surface, never canon_hits."

Byte-truth drift found en route: the homonym_note cites "GAMEDIG_roguelike-runs_20260926.md:177", but the byte tree holds only "GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md" (line 177 content matches; the prior pass g receipt already cites the corrected filename).

## Steal or Vacuous

Steal. The sense collision is real and unhandled at the exact-name leg. The sense gate lives on the dictionary side: it decides what counts into canon_hits at mint time. The routing order fires exact-name FIRST and never consults a sense on the arrival side; its third leg ("then sense-tag canon_hits") orders the entry's own resolution legs, it does not interrogate the arriving text. So a future canon arrival carrying permadeath in the roguelike sense exact-name matches the symbol and resolves into the canon-sense entry (agent-sacrifice interpretation) with no sense check anywhere on the law's path. Fleet canon verdict: needs a sense field on hits; an exact-name hit must record the arrival's matched sense and check it against the entry's homonym_note before the lookup receipt files a resolution. Web search skipped: nothing outward-pointing surfaced; every surface in this probe is fleet-internal.

## Falsifier

Pre-registered build, next pass: amend the _schema_law routing field to add the arrival-side sense check (an exact-name hit on a symbol carrying homonym_note resolves only when the arrival's matched sense is the entry's canon sense; otherwise it files as homonym lookup surface in the LINKS.jsonl receipt). Falsified if, after the amendment, a roguelike-sense arrival (simulate with GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md:177) still resolves to the canon-sense entry, or if the new sense field is not consulted by the canon_hits gate.

## Bibliography

- memory/corpus/symbol_dictionary.jsonl (whole)
- watch/inbox/BURN_stego-canon-pipeline_20260927_d.md (whole)
- watch/inbox/BURN_stego-canon-pipeline_20260927_g.md (whole; found occupied by the landed sibling-routing pass, so this receipt reletters to _h)
- canon/podcast_corpus/doa_ai_debate/canonical_notes.md (line 23 via grep)
- watch/inbox/GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md (line 177 via grep)
- grep output: canon/podcast_corpus/ 4 lines, watch/inbox/ 58 lines
