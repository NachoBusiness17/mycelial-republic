# stego-canon-pipeline pass f: sibling-routing lookup power test

## Verdict

vacuous

## Evidence

Test symbol: "permadeath collectives", a close compound of covered entry permadeath. It occurs in canon at canon/podcast_corpus/doa_ai_debate/canonical_notes.md:37: "permadeath collectives = A1/A2/A3 containment doctrine". Capitalized "Permadeath" does not occur in canon (grep exit 1), so the compound is the only sibling shape present.

Dictionary greps (memory/corpus/symbol_dictionary.jsonl, read whole, 4 rows):
- grep '"symbol": "permadeath collectives"' → exit 1. Miss confirmed.
- grep -c '"siblings": ["' → 0. No entry enumerates any sibling form. Row 1 (ExploitGym, schema v1) has no siblings field; rows 2 and 3 carry "siblings": [].
- The compound string appears only as incidental interpretation text inside row 3 ("permadeath collectives = Astra pattern mainstreamed"), not as a routing declaration any matcher can key on.

Law text read. _schema_law row (row 4): "every entry carries symbol, added_at, added_by, interpretation, source_pointer, canon_hits, mint_shape, external_referent, siblings. canon_hits are sense-gated: only canon-sense lines count; homonym lines are lookup surface, never canon_hits. Mint shapes are exactly two: inbox-anchored and cold-read-shaped. Homonym noise requires sense tags: a symbol whose inbox hits mix senses carries a homonym_note and a line-read sense check in its law." The word siblings appears only as a required field name. No clause says how a sibling match routes to an entry, and the sense machinery gates canon_hits after a symbol match; it never bridges name variants.

The only or-siblings routing text lives in ExploitGym's law (row 1): "canon arrivals carrying this symbol or siblings must run an inbox-spanning lookup and cite this dictionary entry in a LINKS.jsonl lookup receipt before any cold read". Jacob Coxon's law (row 2) claims "siblings list intentionally present (schema v2) so the or-siblings clause is executable by grep", but that list is empty, so grep has nothing to match against.

## Steal or Vacuous

Vacuous. Sibling routing is aspirational today: the schema law mandates the siblings field but never specifies routing, and every routing-capable field is empty, so a canon arrival of "permadeath collectives" exact-key-greps to a miss and neither the siblings arrays nor the sense machinery resolves it to the permadeath entry. The schema law is ahead of its machinery. One-line fix: enumerate sibling forms into the entry's siblings array (permadeath: ["Permadeath", "permadeath collectives"]) so the or-siblings grep clause fires, and copy ExploitGym's routing sentence into the _schema_law row. Fresh web search skipped: the compound is fleet canon phrasing whose only outward pointer is the permadeath entry's external_referent, already pinned snippet-grade in pass d; no new outward footprint exists to test.

## Bibliography

- memory/corpus/symbol_dictionary.jsonl (whole)
- watch/inbox/BURN_stego-canon-pipeline_20260927_e.md (whole)
- canon/podcast_corpus/doa_ai_debate/canonical_notes.md (lines 17, 23, 37 via grep)
- canon/podcast_corpus/doa_ai_debate/transcript.txt (lines 472, 474 via grep)
