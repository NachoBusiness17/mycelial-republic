# R2 LANDING: FLEET LANE (rows 1-remainder and 5, the free-lane work generator)

Seat: R2-landing fleet lane, ouroboros night loop. Moment of my bytes: 2026-10-05, midday EDT. Fold read first: `watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/SYNTHESIS.md`. Files touched: `tools/free_lane_fleet.py`, `scripts/free_lane_fleet_cycle.ps1`, `.zcode/workflows/mickey17-burn.dwf.ts`, this receipt. No git commit (lane law).

## ROW 1 REMAINDER (the green-light cure, completed)

- Set-Location: already landed this morning in the cycle script (grep-verified, single hit, not re-added).
- Exit-code check: the PS1 now checks $LASTEXITCODE after the --cycle invocation and exits 1 on nonzero, logging to the fleet log and the fleet errors.log. It also rejects any cycle output that does not carry the "FREE-LANE CYCLE: fired N, banked M findings, providers healthy X/Y" success shape, same fail path. The try/catch alone cannot see a nonzero native exit; that gap is how this morning's dead fires ran green.
- Liveness tripwire: `tools/free_lane_fleet.py` gained --check-liveness, exit 1 when the ledger at `memory/runs/free_lane_fleet/ledger.jsonl` sits stale past the 90 minute limit while the hourly MagFreeLaneFleet task owed 2+ fires (the B2-465 no-START-stamp shape). The PS1 calls it after the cycle and fails loudly on its nonzero exit.
- Live proof the loop is lit: `logs/free_lane_fleet.log` carries consecutive FREE-LANE CYCLE success lines stamped 15:03, 15:33, 16:03 and 16:33Z today, each banking 8, 9 or 10 findings, and the fleet errors.log does not exist.

## ROW 5 (A1-A6 verdicts)

- A1 probe dedupe: LANDED. A _banked_probe_ids() helper reads the fleet ledger and probe selection skips every work_id already banked ok. Before the fix, 43 banked probe rows in the ledger carried one shared work_id; the refire pool now excludes all of them.
- A2 window sensing: LANDED. probe_items globs `watch/inbox/*/percolator_candidates.jsonl` newest-mtime-first, strictly read-only, alongside the master store (which keeps its freshest-tail rule). Six window files exist on disk. The gate cycle banked window-sourced probes; the sanctioned writer remains the only ingest door.
- A3 probe-key source: LANDED. falsifier and amended_metric are joined by probe as a third falsifier source, and the prompt labels the field "Probe" when the probe key is the one used. The executor's freshest store rows carry probe keys and no falsifier key, so they were skipped before.
- A4 fleet-ops corridor: LANDED. "fleet operations: schedulers, health checks, silent failure modes" appended to CORRIDOR_AREAS; the gate cycle fired it on ollama-local and banked it ok.
- A5 width declaration: LANDED. Before the edit, grep -L over `.zcode/workflows/*.dwf.ts` returned exactly mickey17-burn.dwf.ts; after adding the house-shape declaration comment, the nondeclarer list is empty.
- A6 PROVIDERS date-stamp: LANDED. The PROVIDERS table now carries the comment stamping the ALIVE-sweep moment as 2026-10-05, 7/7 healthy. Stamp only; this lane did not rerun the sweep.

## INCIDENT FOUND AND FIXED DURING LANDING (the fold's method, live)

My first A1 cut derived probe ids for rows lacking id/source keys from the output position. The 16:33Z scheduled fire ran that cut, banked three positional ids from the frontier_olm_2026-10-04 window file, and deadlocked that file's remaining pool: with nothing appended yet, every later row recomputed the first positional id, matched the done-set, and skipped. Fix landed in the same sitting: id-less rows now get a content-hash id (sha1 over claim plus falsifier, first 16 hex, prefixed probe-h-), stable across cycles and never positional. The three already-banked positional ids are orphaned, so those three rows refire once under hash ids; they are sensing rows and the cost is one cheap pass, noted honestly.

## GATES (all green)

- Cycle: the module's --cycle printed "FREE-LANE CYCLE: fired 10, banked 10 findings, providers healthy 5/7" and exited 0.
- Liveness: --check-liveness printed "LIVENESS OK: ledger mtime age 0 min (limit 90 min)" and exited 0.
- Ratchet: the pre-push gate tool over changed files reports hits 5, registered 5, NEW 0, PASS. The landing first tripped its file-too-long rule when this lane's additions grew the module to 437 lines; fixed by compacting my own additions (merged the row-source helper into probe_items, tightened comments while keeping cause and evidence) to exactly 400 lines. No baseline debt was accepted.
- PS1: PSParser tokenize over the edited script, zero errors. py_compile over the amended module: clean.

## HONEST RESIDUE

- Provider health: openrouter-free-1 sits at 6 consecutive fails and openrouter-free-2 at 5 (both crossed the skip-at-5 law, last fails 14:33Z today); the other five providers are at zero consecutive fails. Re-provisioning those keys is an operator-console call, not a code defect.
- The PS1 shape check is parse-verified, not fault-injected; no deliberate bad-exit run was made against the live scheduled task.
- The three refires from the positional-id orphan are owed by design and will appear once in the ledger, then never again.
