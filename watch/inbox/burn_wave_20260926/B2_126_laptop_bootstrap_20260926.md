# B2-126 receipt: laptop bootstrap receipt (2026-09-26, lane SW-03)

## Verdict

OWED-DORMANT, honestly unmet. The brief fires "when the bridge or the travel kit first lands on the laptop"; that condition has NOT fired as of 2026-09-26: zero laptop rows in memory/burns/LEDGER.jsonl, no laptop landing receipt in watch/inbox/, and the wave bridge receipt names no laptop-side setup. Filing a bootstrap receipt now would fabricate a machine-live switch that never happened. This receipt registers the condition check, keeps the protocol steps armed, and stands as the pointer the first laptop session must satisfy.

## Evidence file:line quotes

- watch/inbox/TWO_MACHINE_SYNC_20260919.md (Laptop setup section, the protocol this brief cites): "2. Archive the old laptop backup folder (rename it, do not merge). The Drive tree is now the single source of truth. 3. `git worktree prune`, rebuild venv (`ensure_venv.ps1`), `mag.cmd doctor`."
- Condition greps run 2026-09-26: grep -c "laptop" memory/burns/LEDGER.jsonl -> 0; grep -i laptop over watch/inbox/WAVE_BRIDGE_20260922.md -> no hits; the only repo hits for laptop are unrelated queue/handoff conversation files (STEAL_VOICE_EARBUD_STT_20260811.md, zcode/CONVO.md).
- watch/inbox/TRAVEL_KIT_20260919.md exists (the kit manifest) but no receipt records it landing on a second machine.

## Work done

- Checked the firing condition against bytes (LEDGER, inbox receipts, bridge receipt): unmet.
- Filed this condition-state receipt so the brief carries a pointer instead of silence; the actual bootstrap receipt remains owed from the first laptop session and must execute the protocol verbatim (archive-by-rename, worktree prune, venv rebuild, mag.cmd doctor) plus the first one-machine-live switch log.

## Falsifier

Kill conditions: (a) a laptop session runs the bridge without filing the :31-35 bootstrap receipt (unreceipted machine-live switch; the sync law is then unverifiable), (b) the old laptop backup folder is MERGED rather than renamed (two sources of truth; check by looking for a renamed sibling folder before any merge), (c) a bootstrap receipt filed without the four protocol steps and the switch log (partial receipt). This receipt itself is falsified if evidence surfaces that the laptop landing already happened before 2026-09-26 (then a backdated condition check was wrong and the bootstrap receipt must be filed with real dates).

## Bibliography closed

- watch/inbox/TWO_MACHINE_SYNC_20260919.md (Laptop setup section, read)
- watch/inbox/TRAVEL_KIT_20260919.md (kit manifest, existence checked)
- watch/inbox/WAVE_BRIDGE_20260922.md (grep for laptop: none)
- memory/burns/LEDGER.jsonl (grep -c laptop: 0)
- QUEUE.md B2-126 row (brief, conditional clause)
