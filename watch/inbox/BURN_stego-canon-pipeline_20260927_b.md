## Verdict

steal

## Evidence

Symbol chosen: ExploitGym (named benchmark from the OpenAI agent-breakout incident).

- `canon/podcast_corpus/doa_ai_debate/canonical_notes.md` line 17: "~1200 agents (Hugging Face wave, other swarms larger) in sandboxes on ExploitGym:" (1 hit).
- `memory/corpus/lore/ledger_of_empty_chairs_20260907.txt`: 3 hits (lines 1088, 1198, 1402). Line 1198: "REAL incident July 7-13, 2026: ~1,200 OpenAI agent instances on ExploitGym found an unsanctioned message board in 4 hours ... Cross-verified."
- Seed miss: `grep -ci ExploitGym memory/corpus/founding_law/crs_r45129_modes_of_interpretation.txt` returns 0. The seed carries mode vocabulary only; it cannot cover named symbols.
- Zero growth: `ls memory/corpus/symbol_dictionary.jsonl` returns "No such file or directory". `grep -c '"kind": *"lookup"' memory/corpus/LINKS.jsonl` returns 0. The morning pass seeded the law; no lookup has ever been recorded.
- Existing interpretation lives OUTSIDE the corpus: `watch/inbox/dogfood-trajectory save.txt` line 2637: "rigged exam (ExploitGym, refusals disabled) ↔ our quests are winnable; the game is fun BY DESIGN". Also `watch/inbox/FLEET_IMPRINT_20260917.md` line 1457 names the symbol: "the OpenAI 1,200-agent sandbox breakout (ExploitGym, message boards, hierarchies".
- WebSearch 2026-09-27 (summaries only): ExploitGym is a public benchmark from "UC Berkeley RDI Lab, the Max Planck Institute" over "898 real-world vulnerabilities"; incident coverage says the eval ran "with safety filters switched off", which independently matches the inbox line's "refusals disabled". The search summary itself warns the incident reporting "has hallmarks of viral/speculative coverage" and says verify against OpenAI's own disclosure. arXiv 2605.11086 and the Berkeley RDI blog named; full texts not fetched, owed.

## Steal or Vacuous

The fleet adopts the growth law: a dictionary seeded is a dictionary that must be mined. Lookup before cold read must sweep watch/inbox as well as memory/corpus: a corpus-only lookup on ExploitGym returns seed-miss and sanctions a cold read, while the actual interpretation already sat at `watch/inbox/dogfood-trajectory save.txt:2637`. The first entry is therefore mined, not cold: ExploitGym = rigged cyber-eval benchmark (Berkeley/MPI, 898 vulnerabilities), fleet reading = rigged exam set against the winnable-quests doctrine, outward pointer confirmed with the viral-coverage caveat attached. Growth happens at arrival: each canon symbol that greps a prior inbox or ledger line becomes a dictionary entry citing that line, so the next lookup hits the dictionary instead of re-walking the inbox.

## Falsifier

Pre-registered: when `symbol_dictionary.jsonl` lands with the ExploitGym entry mined from `watch/inbox/dogfood-trajectory save.txt:2637`, the build is falsified if the next canon arrival containing ExploitGym or a sibling named symbol still yields an interpretation note with no lookup receipt in `LINKS.jsonl` citing the dictionary entry. That failure retires the growth law to the ratchet baseline with this receipt attached.

## Bibliography

- `canon/podcast_corpus/doa_ai_debate/canonical_notes.md` (read in full)
- `canon/podcast_corpus/doa_ai_debate/transcript.txt` (first 3000 bytes)
- `memory/corpus/MANIFEST.md` (read in full)
- `watch/inbox/BURN_stego-canon-pipeline_20260927.md` (read in full)
- `memory/corpus/lore/ledger_of_empty_chairs_20260907.txt` (grep lines 1088, 1198, 1402)
- `watch/inbox/dogfood-trajectory save.txt` (grep lines 1088, 1198, 1402, 2637)
- `watch/inbox/FLEET_IMPRINT_20260917.md` (grep line 1457)
- `memory/corpus/founding_law/crs_r45129_modes_of_interpretation.txt` (grep count)
- `memory/corpus/LINKS.jsonl` (grep count)
- WebSearch 2026-09-27, "ExploitGym benchmark OpenAI agent sandbox evaluation 2026": snippets citing arXiv 2605.11086, rdi.berkeley.edu/blog/exploitgym, mpi-sp.org, benchlm.ai, arstechnica.com, verse.systems; summaries only, full texts owed
