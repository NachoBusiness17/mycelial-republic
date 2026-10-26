# FOLD GATE LANDED - 2026-10-05 (cross-run fold mutex)

## The disease (operator ask: "the fold steps on the workflows were running into
## each other and erroring out - make it so they don't hold each other up")
Concurrent workflows all end in a FOLD phase (frontier mines, the
mickey17-burn R-series consolidations). When two folds overlap: same-day
output folders collide, shared-surface appends race, and two giant-prompt
fold dispatches hit the one account together - so folds error into retry
loops (the day-5 mine's fold published without its receipt at 19:52 ET while
R4 landed in parallel; fold total ~11 min including the retry).

## The cure
`tools/fold_gate.py` - a cross-run fold mutex, stdlib only, Windows-safe.
Lock core stolen from `tools/ledger_lock.py` (O_CREAT|O_EXCL atomic acquire,
mtime stale-break, JSONL audit trail) with ONE deliberate divergence:
identity is the caller's --holder STRING, not a pid, because acquire and
release run in different short-lived processes (separate world.run bash
calls / agent tool-calls) - a pid-bound release could never succeed.

Never-block law (the actual ask): a second fold WAITS (default 900s), never
errors; a lock older than 45 min (above a fold + two repair loops) is
stale-broken (the reboot-dead-holder species); on the pathological wait
timeout acquire exits 4, LOGS it, and the caller proceeds unlocked with
shared appends routed through tools/ledger_lock.py append. Release refuses
mismatched holders (exit 5) unless --force (logged).

Locks + audit: `memory/runs/fold_locks/<name>.lock` + `.lock.log`
(events: acquire, stale-break, wait-timeout, release, release-refused,
force-release).

## Wiring (fleet-wide sweep, follow-up ask "what about other workflows")
Deterministic world.run wiring (acquire before the fold, release after,
holder "<workflow>:<slug>"):
- .zcode/workflows/mickey17-burn.dwf.ts (R-series consolidation skeleton)
- .zcode/workflows/mickey17-v2.dwf.ts - CRITICAL catch: its master fold path
  is FIXED (corpus/steal/MASTER_MICKEY17_V2.md), so two concurrent runs
  clobber the same file; the gate is the only serializer it has
- .zcode/workflows/gap-analysis.dwf.ts - same FIXED master path, same cure
- .zcode/workflows/the-gala.dwf.ts
- .zcode/workflows/wide-dig.dwf.ts, fill-ball, drop-dig, salon-mine,
  librarian-expedition (gala-lineage clones; the "fold_gate.sh" already in
  them is their per-run COUNTING gate, a different instrument - the mutex
  is new)

Prompt-law wiring (agent-driven folds; acquire first / release last per ask,
'FOLDGATE acquired|timeout' reply suffix journaled):
- .zcode/workflows/olm-mine.dwf.ts (the SAVED copy the daily cron fires -
  distinct from the draft) + .zcode/workflow-drafts/olm-mine-2.dwf.ts (the
  generation that ran today)
- .zcode/workflows/ractor-engine.dwf.ts (synthesis voice + its repair asks)

Left ungated, deliberately (episodic, agent-driven folds into slug-isolated
folders, no shared write surface, no fixed paths): music-cut, the-50,
tree-doctrine-dig, game-dig-* (5 vein clones). Any future amendment of these
should add the same gate law per the memory note; new fold-bearing skeletons
acquire the gate by the same law.

One-off historical drafts (OLM-mine-daily-burn-*, ouroboros-round-*, etc.)
left alone: superseded by the wired skeletons; ouroboros R5 should fire as a
mickey17-burn amendment (which carries the gate) per the fork-and-forget
consolidation.

## Proof
- tests/test_fold_gate.py: 6/6 green (acquire/status/release cycle; the
  cure species - second acquire WAITS while holder lives then proceeds after
  release; wait-timeout exits 4 WITHOUT stealing the lock; stale-break takes
  a dead holder; wrong-holder release refused then --force works; release on
  free lock is success). Instrument: `.venv/Scripts/python.exe -m pytest
  tests/test_fold_gate.py -q`, 6 passed in 7.27s, 2026-10-05 20:42 ET.
- Live CLI cycle in the real lock dir (memory/runs/fold_locks):
  acquire -> HELD, status -> HELD holder=boot-proof, release -> RELEASED,
  status -> FREE; audit log carries the acquire + release pair.

## Limits
- Prompt-law wiring (the mine) is soft: a folder agent that skips the gate
  is caught by the missing FOLDGATE journal line, not prevented.
- 45-min stale window: two folds CAN overlap if a holder died silently and
  45 min passed; tradeoff documented in the tool docstring.
- Live runs already dispatched (R4 successor) run the old script; the gate
  arms on the NEXT submission of either skeleton.
