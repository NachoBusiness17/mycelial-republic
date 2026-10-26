# HERMES STEERING ORGAN — Mag holds the wheel (2026-09-07, seat helm)

Operator framing: Mag dispatches and steers Hermes as a remote body. Hermes is not a
second brain — it is the gopher body SOUL.md already declares (RACTOR FLEET AMENDMENT).
This organ is the steering wheel between the two.

## THE ORGAN — `mag/hermes_steering.py`
Three doors over `hermes.exe chat`, all receipted to `memory/runs/hermes_dispatch_log.jsonl`,
full outputs archived to `memory/runs/hermes_jobs/<ts>.md`:

- `dispatch "<goal>" [--persona NAME] [--dir WORKDIR] [--model M] [--yolo]` —
  `chat -Q -q "<goal>" --in WORKDIR --no-restore-cwd`, captures output, extracts
  SUMMARY:/DELIVERABLE: sections, harvests the session id (best-effort, from
  `hermes sessions list`) so every dispatch carries its own steer handle.
- `steer --resume SESSION "<nudge>"` — mid-run steering of a live/resumable session.
- `jobs [n]` — the dispatch log tail.

Personas: hermes v0.21.0 chat has NO `--persona` flag, so the persona prompt is
prepended to the goal. Sources: `agent.personalities` in hermes config.yaml, then
`mag/hermes_personas/<name>.md` (gopher.md seeded from SOUL.md laws).

## THE DEMO — steering loop CLOSED (falsifier PASS)
- Goal: read `watch/SELF_STEAL_ORPHANS_20260906.md`, file a 3-line summary of the three
  deepest orphan classes with evidence paths to `research/orphan_registry/hermes_summary.md`.
- Result: exit 0 in 42s on the Lite lane. Deliverable landed, faithful to source
  (B7 spectral maze / phantom memory index / the map's unmapped tools — evidence paths correct).
  SUMMARY:/DELIVERABLE: extracted into the receipt.
- Steer door: `steer --resume 20260907_041538_776e2f` appended the steering line to the
  deliverable mid-flight, 20s, byte-verified.
- Honest receipt: first attempt (exit 2, flag bug `-Q` vs `-q`) is in the log. One builds,
  one verifies — the organ receipts its own failures.

## REPAIR EN ROUTE (backup-first, no keys echoed)
Hermes config had drifted: stale inline api_key (401 "token expired" at 03:46Z) blocked
the lane. Restored from fleet `.env` `ZAI_API_KEY_Lite` (Lite pool, glm-5.3-flash per
`mag/free_tier.py` z_ai3). Backup: `config.yaml.bak-helm-20260907T081300Z` next to it.
The Lite key lives fleet-side; hermes carries a copy — re-arm syncs are Mag's job.

## THE DOORS — personas x dispatch x resume x cron = the ractor cockpit
- personas: voices are data (config personalities + mag/hermes_personas/), swapped at
  dispatch time, prepended — zero CLI surface needed.
- dispatch: pack + goal only from Mag, outcomes filed with SUMMARY:/DELIVERABLE: —
  the SOUL.md contract enforced by the organ's receipt shape.
- resume/steer: every dispatch returns a steer handle; nudges land mid-job.
- cron: hermes already has `hermes cron`; the organ's dispatch shape is the payload a
  cron row (or Mag cadence) would call — the cockpit door is cut, not yet wired.

## RECEIPTS
- Cells: G/hermes/steering-organ + G/hermes/demo-dispatch (seat helm), tesuji verify
  PASS — 319 cells, chain intact, tip 711466e5feaf.
- Ledger: memory/runs/hermes_dispatch_log.jsonl · Jobs: memory/runs/hermes_jobs/
- Cost: two demo Lite-lane turns (~42s + ~20s, pennies) + one $0 failed local flag probe.
