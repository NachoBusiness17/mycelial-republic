# INTAKE — book-to-skill (2026-09-04)

NAME — OSS distiller: turns any book/PDF/folder into a lazy-loading agent skill (SKILL.md index + per-chapter files + glossary + decision tables); agent reads only the chapter it needs. github.com/virgiliojr94/book-to-skill (28.5K stars, MIT, Python, Agent Skills open standard; works in Claude Code/Copilot CLI/Amp/Hermes). Source: @\_guillecasaus tweet 2095836781627261350 (ES), repo link hunted via GitHub search — tweet said "in comments".

SCORE — F:5 P:4 C:5 W:3 N:3 = 20/25 BUILD NOW
- FIT 5: pure composition of parts we run — skills shelf, files-not-processes, local CLI, no new vendor/account.
- PULL 4: mining arc (distill sources -> executable skills — PhiCookBook/ZAI reference already live this pattern by hand); token thrift directly eases the key-saturation throttle during the Sep 3-20 promo wall. Not on the Rocinante/maze-keeper critical path.
- COST 5: free, local, zero operator minutes beyond one install.
- WINDOW 3: useful tonight (cheaper premium-lane context), but nothing is blocked on it.
- NOVELTY 3: new tool, known pattern — the fleet hand-rolls chapter-index distillation; this industrializes it. No prior card on watch/ (3-min box, no full corpus sweep).

VERDICT — BUILD (install + run on one fleet reference doc as falsifier) | tri-state: Supported — tool exists, measured claim "24x-51x fewer tokens vs full-context dump" is the repo's own receipts (docs/performance.md, "discovery loop tax"); tweet's "reduces hallucinations" claim Unproven (vendor marketing, no falsifier shown).

DOGFOOD — Test 4 (Stockfish): it sits on our lattice as a distillation opcode on the mining aisle — same opcode as transcript-mining, different input codec (books vs sessions). Placement succeeded. Test 1 (invariants): reinforces files-not-processes + route-bulk-to-free-lanes (distill once on free lane, save premium tokens forever); contradicts nothing.

LAUNCH WIRE (Amendment 5, same-turn): builder = one free-lane run: `/book-to-skill` on docs/ref/ZAI_API_EXPERT_REFERENCE.md (or PhiCookBook), diff token cost vs current full-file read, file receipt. ~15 min, $0.

FILED — watch/INTAKE_book_to_skill_20260904.md + room.jsonl thread "intake"
