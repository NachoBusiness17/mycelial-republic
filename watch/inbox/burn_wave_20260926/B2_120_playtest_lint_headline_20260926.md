# B2-120 receipt: PLAYTEST.md lint headline fossil (2026-09-26, lane SW-03)

## Verdict

DONE with one owed dependency named. The PLAYTEST.md header no longer recites "21 files clean"; it now carries the live 2026-09-26 truth measured from bytes: tools/luau_lint.py prints "checked 43 files, 3 with findings", the 3 named zones_extra block-balance advisories. The brief conditioned the refresh on "after B2-119 triage lands"; B2-119 has NOT landed (no receipt on file, QUEUE row carries no pointer), so the classification of the 3 advisories is filed as OWED to B2-119 in the refreshed header itself, not fabricated as resolved.

## Evidence file:line quotes

- roblox/docs/PLAYTEST.md:3-4 (pre-edit): "2026-09-25 · Headless pass done (tools/luau_lint.py: 21 files clean; audit fixed the Ossuary solid-rock maze bug ..."
- Live run 2026-09-26 (.venv/Scripts/python.exe tools/luau_lint.py, tail): "roblox\src\server\zones_extra\FrontierSoulsZone.luau - block balance: 39 openers vs 36 closers (delta 3) ... HardwarePrimerZone.luau - block balance: 25 openers vs 24 closers (delta 1) ... IncidentDungeonZone.luau - block balance: 26 openers vs 25 closers (delta 1) ... checked 43 files, 3 with findings"
- QUEUE.md:304 (B2-119 row, pre-execution): "classify each as real unbalanced block vs the documented keyword-in-string false-positive class ... register the noise by name in the mountain_check accepted-noise header"
- QUEUE.md row B2-120 (brief): "the 2026-09-26 tree is 43 files with 3 advisories; refresh the header to current truth after B2-119 triage lands (trust bytes, not hand-written counts)"

## Work done

- Ran tools/luau_lint.py live (the brief's law: trust bytes, not hand-written counts) and confirmed 43 files / 3 findings, matching the brief's numbers exactly.
- roblox/docs/PLAYTEST.md:3-12: replaced the stale "21 files clean" headline with the dated refresh: live count 43 files 3 findings, the 3 advisories named with their opener/closer deltas, and the classification explicitly marked owed to B2-119 triage (real imbalance vs keyword-in-string false positive).
- No linter code touched (B2-31 tripwire section left byte-identical; B2-119 owns any luau_lint/mountain_check change).

## Falsifier

Kill conditions: (a) the refreshed header still names a file count or finding count that differs from a live luau_lint run (re-run and compare; today they match at 43/3), or (b) the header implies the 3 advisories are resolved/classified before a B2-119 receipt lands (it does not; it names them open). Re-check after B2-119 lands: its classification must be folded into this header or the fossil regrows.

## Bibliography closed

- roblox/docs/PLAYTEST.md (read lines 1-26, edited 3-12)
- tools/luau_lint.py live output 2026-09-26 (run in this lane)
- watch/inbox/burn_wave_20260926/QUEUE.md B2-119 and B2-120 rows (read)
- watch/inbox/burn_wave_20260926/B2_31_poll_tripwire_20260926.md (pointer named in brief; tripwire spec section in PLAYTEST.md read)
- ls of watch/inbox/burn_wave_20260926/ (no B2_119 receipt on file at execution time; checked before writing OWED note)
