# AH6 — Root junk sweep, audit #11 (VERIFY-THEN-DELETE)

- **Owner:** AH6 junk-sweep seat (this file is the receipt; sole write by this sweep)
- **Date:** 2026-09-30 ~08:30 EDT
- **Scope:** repo root path-bug junk + `.git` tmp_pack garbage. Constraints honored: `.mimosa` untouched, `watch/inbox` content untouched (only this owned receipt added), tracked files untouched (after incident recovery, below).

## Deleted (freed: 442,623,459 bytes = 422.50 MiB)

| Item | Size | Verification before delete |
|---|---|---|
| `.git/objects/pack/tmp_pack_Pzg0vB` | 115,998,732 B | git `count-objects` itself labels all 4 `garbage found`; mtime Sep 29 22:44 (interrupted gc window 22:39–22:53) |
| `.git/objects/pack/tmp_pack_dhcUQj` | 162,791,436 B | same; read-only orphan, no `.idx`, unreferenced by any pack |
| `.git/objects/pack/tmp_pack_isrA9v` | 1,441,804 B | same |
| `.git/objects/pack/tmp_pack_l4Kht9` | 162,791,436 B | same (byte-identical size to dhcUQj — duplicate repack attempt) |
| `nul` (root, untracked `??`) | 51 B | 51-byte plain file (cmd `dir /x` + python `listdir`), not the device |

**Git hygiene sequence (as ordered):** `git count-objects -vH` before → `count: 12599, packs: 3, size-pack: 6.27 GiB, garbage: 4, size-garbage: 422.50 MiB`; quick `git fsck --no-dangling --connectivity-only` clean (exit 0), no `gc.pid`/`index.lock`/pack `.lock`; tmp_packs still garbage → removed; after → `garbage: 0, size-garbage: 0 bytes`, fsck re-run clean. **Full `git gc` deliberately not run:** the only garbage was the tmp_packs (3 packs healthy, `prune-packable: 0`); repacking 6.27 GiB under live multi-lane traffic (receipts landing all morning) buys nothing the mission asked for.

**nul deletion method:** plain `rm ./nul` in Git Bash worked (MSYS rm bypasses the reserved-device name mapping). The prescribed `\\?\` route failed twice first — `python os.remove(r'\\?\C:\...\nul')` → WinError 3, `cmd del \\?\...` likewise. Recorded so the next seat starts with `rm`.

## Not found (already gone before audit #11)

Root has **zero** `%`-named entries and no `CUsers*`/`C?Users*` directories: `%CD%`, `%TEMP%`, `%TEMP%balatro`, `%TEMP%dee_dig`, `%TEMP%or_models`, `CUsersfosteAppDataLocalTempfw`, `CUsersfosteAppDataLocalTempgk_deep`, and the file `%TEMP%or_models.json` — none exist. Presumed cleared by a prior audit (≤ #10). Only the mangled **file** family `UsersfosteAppDataLocalTemp*` persists (see unresolved).

## Unresolved — verified junk but LEFT IN PLACE

### (a) Tracked junk — blocked by NEVER-touch-tracked constraint (~21.9 MB)
All committed & clean against HEAD; removal requires deliberate `git rm` + commit (operator call):
- 16 × `UsersfosteAppDataLocalTemp*.{json,html,pdf,txt}` (4.2 MB) — path-bug scrape outputs (fw/gk_deep/flash50/omni/or_models/ddg/evade families)
- `.tmp_*` family — **41 tracked paths**: `.tmp_dig/` (18 files, 10.8 MB, dig scrape corpus) + 24 root `.tmp_*` files (2.4 MB, search-probe outputs)
- `scratch_cobalt/` (259 KB, 57 .wiki) · `tmp_digger_sts/` (1.4 MB) · `tmp_gopher/` (2.8 MB) · `tmp_kyn/` (1.1 MB) · `tmp_bw.html` + `tmp_inst.html` (12 KB)

### (b) ACL-locked — 20 × `.pytest-*` basetemp dirs (Aug 30)
Contents unreadable: `find` → Permission denied, `icacls` → Access denied, non-elevated `takeown` → Access denied, `cmd rd /s /q` → Access denied. Foreign owner (likely Docker/WSL-root creation during the Aug 30 burn-wave pytest runs). Untracked (pathspec-verified). Needs an **elevated** `takeown /f <dir> /r` + `icacls <dir> /reset /t /c /q` + delete pass.

### (c) Observations (not in mission list, left)
- `=17` — 0-byte root file (Sep 22), same path-bug family (`--opt=17` shell artifact); next audit should claim it.
- `.pytest_cache/` — Jul 20; underscore, not `.pytest-*` hyphen shape; standard cache, out of pattern.

## Incident + full recovery (the honest part)

- **What happened:** first tracked-check ran `git ls-files | grep -E '(^|/)(\.pytest-|tmp_|\.tmp_|UsersfosteAppDataLocalTemp|scratch_cobalt|nul$)'` and it **silently matched nothing dot-prefixed** — it cleared `.tmp_*` as untracked. `rm -rf ./.tmp_*` then deleted **41 tracked files** (~13.1 MB worktree).
- **Root cause (reproducible):** this shell's `grep` is **ugrep 7.8.4 WIN64**, not GNU grep. Its `(^|/)(alternation)` shape fails on these inputs: `printf '.tmp_sh1.json' | grep -E '(^|/)\.tmp_'` → no match (rc=1), while `grep -E '^(\.tmp_|tmp_)'` matches. Distrusting the instrument was the fix.
- **Detection:** same-session `git status --porcelain -uno` showed ` D .tmp_dig/...` rows.
- **Recovery:** `git restore -- '.tmp_*'` (pathspec scoped to exactly my deletion set — no other lane's files touched). Final `^ D` sweep: **empty**. Spot byte-check: `.tmp_sh1.json` 51 B, matches pre-incident.
- **Law echo (census denominator law):** trust the byte instrument, not the hand-rolled report. The reliable tracked-check here is `git ls-files -- '<glob>'` (pathspec), which is what exposed all 41.

## Protected surfaces

`.mimosa` — untouched. `watch/inbox` — untouched except this owned receipt. The 37 `git status` entries under `.mimosa`/`watch` observed at sweep close are the concurrent last-mile wave landing receipts (mtimes all morning), not this seat's writes.

## Net

- **Freed:** 422.50 MiB (tmp_packs 422.50 MiB + `nul` 51 B)
- **Unresolved:** ~21.9 MB tracked junk (needs `git rm` lane) + 20 ACL-locked `.pytest-*` dirs (needs elevated sweep) + `=17` (unclaimed)
