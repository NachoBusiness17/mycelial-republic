# B2-396 mag-tasks-disabled check cries wolf (SW-07, 2026-09-26)

## Verdict

LANDED. Spec-first: the operator-sanctioned task set now lives in configs/sanctioned_scheduled_tasks.yaml (13 rows, each with its register source and expected state, including the two Bounded B2-261 mimo tasks and the two Disabled retirees). scripts/lattice_check.py's whitelist loads that file instead of the hardcoded mag-docker-watchdog-only set. Post-fix live run: `[   ok   ] mag-tasks-disabled: {"violators": [], "state_drift": [], "sanctioned_count": 13}` -- the card's signal is restored, and a future Mag* task that is neither Disabled nor in the spec screams again.

## Evidence file:line quotes

- The disease, QUEUE.md row: "the lattice card diverged on it all day with violators MagCensusPatrolDaily, MagEndpointNewsDaily, MagImproveDaily, MagVisionNightly (memory/runs/lattice/latest.json 17:32:10Z run) while SANCTIONED_MAG whitelists only mag-docker-watchdog (scripts/lattice_check.py:59) even though AGENTS.md registers MagImproveDaily as the sanctioned 08:00 daily task and B2-246 landed census-patrol scheduling".
- Pre-fix bytes: `SANCTIONED_MAG = {"mag-docker-watchdog"}` with violators = every non-Disabled Mag* name.
- The spec, configs/sanctioned_scheduled_tasks.yaml header: "The operator-sanctioned set is every task a register_*.ps1 script or a landed receipt installed, named here with its source ... adding a task = add its register script + a row here."
- Host truth at spec time (schtasks CSV): mag-docker-watchdog, MagCensusPatrolDaily, MagCorpusRescanDaily, MagEndpointNewsDaily, MagFtsIndexDaily, MagImproveDaily, MagMimoWatchClose, MagMimoWatchHourly, MagQCaptionVerifyDaily, MagSecretScanWeekly, MagVisionNightly all Ready; MagLabKit8765 and MagPrivateOffice8765 Disabled; zero unlisted Mag* tasks.
- Post-fix run: divergence row above; the remaining 2 divergences (covenant-floor, one-resident) are pre-existing and unrelated to this check.
- One real defect found by the first post-fix run, receipted: ConvertTo-Json serializes the TaskState enum as numbers (Disabled=1, Ready=3), so the first version misread every state and wrongly flagged the two Disabled retirees in state_drift; fixed with the STATE_NAMES map and re-run green.

## Work done

- configs/sanctioned_scheduled_tasks.yaml: the spec (13 tasks, sources, expected states, bounded-expiry notes for the B2-261 pair with a remove-at-close instruction).
- scripts/lattice_check.py: _load_sanctioned_mag() reads the yaml (fail-loud when unreadable); check_mag_tasks now lists TaskName+State via ConvertTo-Json, maps the numeric enum, classifies violators (unsanctioned and not Disabled) and state_drift (sanctioned-but-wrong-state); claim line appended before the edit (file was working-tree-modified; rebased on fresh bytes).
- Check description string updated to name the spec home.

## Falsifier

The brief's falsifier ("--json shows mag-tasks-disabled diverged on every run while the named tasks are operator-registered") is disproven by the post-fix run quoted above. Reopen if: the yaml drifts from the host (a live task absent from the spec screams -- that is the check working, and the operator response is either delete the task or register it in the spec), or the check reverts to a hardcoded set.

## Bibliography closed

Read: scripts/lattice_check.py (whitelist block pre/post), configs/sanctioned_scheduled_tasks.yaml (this lane's spec), AGENTS.md:27 and :96 and :109 (sanctioned-task registrations), memory/runs/lattice/latest.json (pre-fix violators named in the QUEUE row; post-fix row read back), schtasks CSV query, QUEUE.md B2-396 row. No external sources.
