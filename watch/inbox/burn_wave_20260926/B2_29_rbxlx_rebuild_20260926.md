# B2-29 rbxlx rebuild + verify (2026-09-26)

## Verdict
P0 REBUILD GATE PASSED. `roblox/the_mountain.rbxlx` was stale (mtime 01:10,
src edited to 01:20, prereg-proven missing t74 + t72). This lane ran
`bash tools/mountain_check`, got "GATE PASS: the_mountain.rbxlx rebuilt" with
0 parse-level failures, and re-proved the fix landed on the new build bytes:
"UpdateAsync" now 2 hits (was 0), "GetAsync(key)" 0 hits (was 1), t72
"annotation exactness" 8 hits (was 0). The B2-10 prereg P0 falsifier
conditions are both cleared. Build bytes are no longer stale. Not committed;
left in the working tree for the operator's Sep-29 playtest gate.

## Evidence
- Stale proven before rebuild (bytes, not mtimes): `grep -c UpdateAsync
  roblox/the_mountain.rbxlx` = 0; `grep -c "GetAsync(key)"` = 1. HEAD build
  carries the old two-call shape: `store:GetAsync(key` (git show HEAD grep).
- Live src carried the fix: `roblox/src/server/ShadowLedger.luau:59`
  `store:UpdateAsync(key, function(old)`, copy-then-append transform :60-65
  (`local rows = {}` ... `rows[#rows + 1] = entry` `return rows`), t74
  receipt comment :43-57 naming the lost-update cause and the docs fetch.
- Live src carried t72: `roblox/src/server/zones_extra/GalleryZone.luau:41`
  and `:56` both carry "annotation exactness" comments; `:57`
  `local function mk(...): Part` with `:58 Instance.new("Part")`.
- Gate run: lint advisory 3 block-balance notes (known false positives per
  tool header), sourcemap created, analyze "parse-level failures: 0",
  "unique findings: 9" (all accepted noise classes: 8 LocalUnused, 1
  external-type TypeError MudBasecamp(220,19)), then "Built project to
  the_mountain.rbxlx" and "== GATE PASS: the_mountain.rbxlx rebuilt ==".
- Post-rebuild bytes: UpdateAsync 2 (the :59 call plus the t74 comment text),
  GetAsync(key) 0, annotation exactness 8, Gate_ 11 (t46 held), Sole Summit_
  writer 1 (t56 held). mtime 2026-09-26 08:28:15 -0400, 383,204 bytes.
  git diff --stat: 140 insertions, 65 deletions in the rbxlx only.
- This lane modified no src: `git status --short -- roblox/src
  roblox/sourcemap.json` is empty.

## Work done
Verified both prereg claims against src bytes before building, ran the gate
once, ran all five greps on the rebuilt bytes, diffed against HEAD, filed
this receipt, appended the LEDGER row, self-fed 3 briefs (B2-108..110).

## Falsifier
This receipt dies if: (a) the rbxlx on disk at Sep-29 does not contain
`store:UpdateAsync(key, function(old)` (grep it fresh), or (b) the live src
ShadowLedger.luau:59 is reverted to GetAsync+SetAsync without a new receipt.
Playtest P3 (ledger race, two clients) is the runtime check this static gate
cannot substitute for: t74 is still "NOT verified against a live DataStore".

## Bibliography closed
roblox/the_mountain.rbxlx (pre + post bytes); roblox/src/server/ShadowLedger.luau;
roblox/src/server/zones_extra/GalleryZone.luau; tools/mountain_check;
watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md;
git HEAD 790145ab1 roblox tree; memory/burns/LEDGER.jsonl tail;
watch/inbox/burn_wave_20260926/QUEUE.md.
