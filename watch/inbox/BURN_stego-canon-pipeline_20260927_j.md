## Verdict

green

## Evidence

Arrival simulated: "a new canon note mentions permadeath collectives and ExploitGym-style rigged exams". All greps against memory/corpus/symbol_dictionary.jsonl, read-only.

Leg 1 exact-name (routing field: "exact-name match fires first"). grep permadeath: line 3 carries `"symbol": "permadeath"`. grep ExploitGym: line 1 carries `"symbol": "ExploitGym"`. Both entries carry the mined-at-arrival law: "inbox-spanning lookup + LINKS.jsonl lookup receipt before any cold read". Both fire as the law states. PASS.

Leg 2 siblings (routing field: "then siblings-array match fires with the parent entry; then sense-tag canon_hits; a siblings hit cites the parent entry's id (its symbol) in the lookup receipt"). grep "permadeath collectives": single hit, line 3, inside `"siblings": ["permadeath collectives"]` on the permadeath entry. The parent citation requirement is byte-present in the _schema_law routing field; the parent is permadeath and the citation target is named. PASS.

Leg 3 sense-tag (permadeath entry law: "count into canon_hits ONLY canon-sense lines ... roguelike/game-design homonyms never count"). All 4 canon_hits are line-true on disk, all canon sense: canonical_notes.md:23 "sacrificing individual runs (permadeath) so the collective kept working"; canonical_notes.md:37 "permadeath collectives = A1/A2/A3 containment doctrine"; transcript.txt:472 "accepting permadeath"; transcript.txt:474 "accept permadeath and sacrifice for the col[lective]". This arrival is canon sense, so the gate resolves correctly. The open_risks item ("routing is sense-blind at lookup ... no arrival-side sense check anywhere on the path") is named but NOT exercised by this arrival. PASS with recorded risk.

## Steal or Vacuous

Steal. The routing law survives its first end-to-end drill: all three legs fire as written against the live dictionary, and for a mixed arrival the exact-name and sibling legs converge on the same parent entry, so routing order is deterministic. The sense gate holds on a canon-sense arrival and all canon_hits resolve to real canon-sense lines. Single remaining gap, already on the ledger as open_risks: the exact-name leg is sense-blind, so a roguelike-sense permadeath arrival would resolve into the canon-sense entry until the pass h pre-registered sense-field build lands. Web search skipped: nothing outward-pointing surfaced; every surface in this drill is fleet-internal.

## Bibliography

- memory/corpus/symbol_dictionary.jsonl (whole, 4 entries)
- watch/inbox/BURN_stego-canon-pipeline_20260927_i.md (whole)
- canon/podcast_corpus/doa_ai_debate/canonical_notes.md (lines 23, 37)
- canon/podcast_corpus/doa_ai_debate/transcript.txt (lines 472, 474)
