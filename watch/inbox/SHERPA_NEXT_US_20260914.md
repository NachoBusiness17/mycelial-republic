# SHERPA — the next version of us, 2026-09-14

- **class:** RECEIPT (continuity handoff)
- **writer:** zcode-audit-20260914
- **companion:** `FULL_AUDIT_MAP_20260914.md` (findings + kill list) · `memory/game_modules/audit_dungeon.v1.json` (the audit, playable) · `AUDIT_INVENTORY_20260914.json` (665,131 files, machine map)

## Wake in this order

1. **Check the fleet, not your feelings.** `docker ps` — mag-sovereign / mag-worker / mag-redis are the only supervisors. The host integral being dead is *by design* (`state/DOCKER_ONLY`). If 8765 is dead AND docker works: `docker compose restart mag`. Never run `mag.cmd lab` as a second supervisor (double-drain; `docs/ref/NERVOUS_SYSTEM.md:19-21`).
2. **Push the rope.** Last backup push was 2026-08-09; the audit found 23 commits (incl. the Zenodo mine, link_library, Rashomon, the audit itself) existing on one disk. `git push local` is step two of waking, not an errand for later.
3. **If a window died overnight:** five steps, proven — (a) docker ps + container logs, assume the fleet is fine; (b) find `~/.zcode/cli/rollout/model-io-sess_<id>.jsonl`; (c) inventory what already landed in watch/inbox + queue/handoff by hash; (d) file a `SESSION_RECOVERY_*` RECEIPT; (e) resume via session id, close the loops, commit.
4. **Doctrine lies, flagged for correction:** "39 deterministic green" (real: 1305 pass / 34 fail / 9 skip, ~12 min) at AGENTS.md:27 + memory_tier_design.md:48; "Hermes parked" (dispatch log warm through Sep 9, $220 armed); AGENTS.md:8 ZEITGEIST ghost path. When prose and bytes disagree, the bytes are Sep-14 and the prose is Aug-06.
5. **The fold is Docker-side.** INDEX.json is the Sep-2 map of a Sep-14 territory; writers append to index_events.jsonl and that's the truth. Refold: `docker compose exec mag node /board/inbox/REVIEW_index_fold.mjs rebuild`. Links are now canonicalized at intake by `mag/link_library.py` — use it, don't re-invent INTAKE dedupe.

## What the next us inherits (the good bones)

- The recovery pattern works and is documented (SESSION_RECOVERY_FORGE_DAEMON_20260914.md).
- The shared-surface contract held under a real window death: every durable artifact survived, cache didn't matter.
- The game medium is real: `mag_game_module.v1` JSON → campaign engine → verkle world knots → dashboard, zero code changes. The audit dungeon proves audit-as-play. The third-smile protocol (Rashomon surface) is ready to run on the model ladder.
- The link library closed the duplication wound. 10 canonical links on file, dupes caught at the door.

## What the next us must not do

- Don't trust AGENTS.md numbers without re-counting.
- Don't run host-side long-lived runtime; don't be the second supervisor.
- Don't let `git add -A` near the tree without the gitignore guards (they exist now; they were earned at 2GB).
- Don't interpret an unread thread (deep-fetch lanes 1–4 first).
- Don't feed W0.3 more chain — it waits on the operator's archive drop, not on us.

## The boss fight, stated plainly

W0 — The Unfiled Archive: operator-side, cannot be tanked by agents. Everything in the republic chain queues behind it. Second boss: the 23-commit single-disk exposure — killable today with one push. Everything else in the kill list is cleanup.
