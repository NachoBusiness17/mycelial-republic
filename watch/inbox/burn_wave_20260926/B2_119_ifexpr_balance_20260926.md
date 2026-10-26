# B2-119 zones_extra balance advisories triage (2026-09-26)

## Verdict

LANDED as a heuristic fix, not noise registration. All three permanent advisories were one new false-positive class, and the brief's own hypothesis (keyword-in-string) was wrong: strings are already stripped by strip_comments_strings, and the probe found zero keyword-bearing surviving strings in any of the three files. The real class is Luau if-EXPRESSIONS: `x = if c then a else b` chains (including elseif arms) are counted by the `\bif\b` opener scan but carry no `end`, so each faked delta +1. Exact match measured: FrontierSoulsZone 3 if-expressions (lines 185, 186, 206) = delta 3; HardwarePrimerZone 1 (line 175) = delta 1; IncidentDungeonZone 1 (line 141) = delta 1. Zero real imbalance: luau-lsp parse_fails=0 on the same tree the same day (B2-110 run). Fixed luau_lint.check() to discount single-line if-expression chains (ifexpr_discount, lazy regex + no-end-on-line guard + required token after else). Result: 43 files checked, 0 with findings, and the whole pre-existing advisory surface (delta 3/1/1) is gone without touching any .luau byte. RiddleMazeZone proved the guard necessity live: its line 71 `if #opts == 0 then table.remove(stack) else` (statement form, else-block on following lines) over-discounted delta -1 under the first cut and is rejected by the trailing-bare-else guard in the landed cut.

## Evidence

- tools/luau_lint.py:234-236 pre-fix `opens = sum(count_word(src, w) for w in ("function", "if", "repeat", "do"))` vs `closes = ... ("end", "until")`; the `\bif\b` scan cannot tell if-statement from if-expression
- roblox/src/server/zones_extra/FrontierSoulsZone.luau:185 `death.cd = if ph == 3 then 1.5 else 1.9`, :186 `local n = if ph == 3 then 7 else 5`, :206 `death.cd = if ph == 3 then 1.3 elseif ph == 2 then 2.0 else 2.6` (3 chains, delta 3)
- roblox/src/server/zones_extra/HardwarePrimerZone.luau:175 `local paid = if i == 1 then paid1 else paid2` (1 chain, delta 1)
- roblox/src/server/zones_extra/IncidentDungeonZone.luau:141 `local px = if n > 1 then cx - 12 + (j - 1) * (24 / (n - 1)) else cx` (1 chain, delta 1)
- tools/luau_lint.py:54-75 landed: IFEXPR_LINE_RE `\bif\b[^;\n]*?\bthen\b[^;\n]*?\belse\b\s*\S` + ifexpr_discount (no `\bend\b` on line) with the cause-carrying comment; :263 `opens -= ifexpr_discount(src)  # B2-119: if-expressions carry no end`
- Post-fix run: `checked 43 files, 0 with findings` (was `3 with findings` pre-fix, both measured this lane)
- Synthetic regression set 8/8 OK: multiline statement-if 0, ifexpr 1, elseif chain 1, two chains one line 2, trailing bare else 0 (RiddleMazeZone:71 shape), one-line statement with end 0, statement if/elseif/else with end 0
- tools/mountain_check unchanged; tools/luau_lint.py was working-tree-modified, claim line filed on QUEUE.md at 2026-09-26T19:51:18Z before the edit, retired at landing

## Work done

Triage before touch: reproduced the 3 advisories, ruled out the keyword-in-string class (strings stripped; probe found none surviving), stack-walked the stripped source, isolated if-expressions as the residual, and verified the count per file equals the reported delta exactly (3/1/1). Fixed the heuristic in luau_lint.py with a discount function rather than an accepted-noise registration, because the false positive is fully mechanical and the discount keeps real imbalances loud. First cut over-discounted RiddleMazeZone:71 (delta -1 appeared); tightened to lazy spans + required post-else token, re-ran the full lint (0 findings) and an 8-case synthetic set covering both failure directions. Claim law honored for the shared working-tree-modified file: CLAIM line appended before the edit, retired CLAIMED with receipt pointer at landing. No .luau file edited.

## Falsifier

`.venv/Scripts/python.exe tools/luau_lint.py` must print `checked 43 files, 0 with findings` while the tree parses (luau-lsp parse_fails=0). If someone adds a genuine unbalanced block (delete one `end` from any zone file), the check must go loud again with the true delta; if someone adds a single-line if-expression, no advisory may fire (that is the discount working, not a regression). The over-discount tripwire: `git diff tools/luau_lint.py` carries the trailing-bare-else guard (`\belse\b\s*\S`); removing it reintroduces the RiddleMazeZone:71 delta -1, verifiable by running the lint after stripping that guard. Multiline if-expressions remain known-blind (documented in the comment block): a future delta +1 on a file whose only anomaly is a multiline if-expression is the documented limitation resurfacing, not a new defect.

## Bibliography closed

tools/luau_lint.py (read in full, edited: comment block + IFEXPR_LINE_RE + ifexpr_discount + one-line change in check()); roblox/src/server/zones_extra/FrontierSoulsZone.luau, HardwarePrimerZone.luau, IncidentDungeonZone.luau, RiddleMazeZone.luau (read, unchanged); tools/mountain_check (read, unchanged); watch/inbox/burn_wave_20260926/B2_31_poll_tripwire_20260926.md (pointer, read via header trail); QUEUE.md (claim lines + row note); memory/burns/LEDGER.jsonl (appended).
