## Verdict

steal

## Evidence

Pre-edit drift (memory/corpus/symbol_dictionary.jsonl, permadeath homonym_note): "GAMEDIG_roguelike-runs_20260926.md:177". Byte truth (ls watch/inbox/GAMEDIG_roguelike*): only "GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md" exists; no bare "GAMEDIG_roguelike-runs_20260926.md" on disk. Line 177 content matches the cited span (pass h quote: "Slice & Dice: ... and the Permadeath curse").

Post-edit: homonym_note now cites "GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md:177".

Sense-collision precondition check: pass h (BURN_stego-canon-pipeline_20260927_h.md) verdict: "a future canon arrival carrying permadeath in the roguelike sense exact-name matches the symbol and resolves into the canon-sense entry ... with no sense check anywhere on the law's path." The routing field still opens "exact-name match fires first" and was NOT edited this pass: an arrival-side sense check in prose has no carrier (canon_hits carry no sense field; lookup receipts record no matched sense), so an early edit would write a rule nothing consults, the exact failure pass h's falsifier names ("if the new sense field is not consulted by the canon_hits gate").

Post-edit _schema_law row carries a new field, "open_risks": ["sense-collision at the exact-name leg: routing is sense-blind at lookup; a same-name-different-sense arrival (roguelike-sense permadeath, watch/inbox/GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md:177) would exact-name match and resolve into the canon-sense entry with no arrival-side sense check anywhere on the path; the fix needs the pre-registered falsifier build first (sense field on hits, BURN_stego-canon-pipeline_20260927_h.md), so the routing text stays unamended until that build lands"]. The law_text meta-row clause was touched minimally to stay byte-true: "is a meta-row carrying symbol, law_text, the routing field, and open_risks by design (open_risks landed pass i 2026-09-27)".

Verification: repo venv python json load passes, 4 entries intact (ExploitGym, Jacob Coxon, permadeath, _schema_law), routing field byte-unchanged.

## Steal or Vacuous

Steal. The fleet adopts: (1) the byte-true homonym_note citation; (2) the open_risks convention on the _schema_law meta-row: a risk the falsifier has named but no build yet carries gets one line in open_risks, never prose in routing that nothing consults. The routing law stays sense-blind at the exact-name leg by recorded choice until the sense-field build lands; that choice is now on the ledger, not latent. Web search skipped: nothing outward-pointing surfaced; every surface in this pass is fleet-internal.

## Falsifier

Standing pre-registration (pass h) unchanged and now anchored: amend routing with the arrival-side sense check only when a sense field on hits exists to carry it. Falsified if routing prose gains sense-check wording before any hits-side sense field exists (the premature state this pass refused), or if a roguelike-sense arrival (simulate: GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md:177) still resolves to the canon-sense entry after the build.

## Bibliography

- memory/corpus/symbol_dictionary.jsonl (whole, pre-edit and post-edit)
- watch/inbox/BURN_stego-canon-pipeline_20260927_h.md (whole)
- ls watch/inbox/GAMEDIG_roguelike* (filename byte truth)
