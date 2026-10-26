# B2-199: drift-patrol-cron adopts the living hash law (2026-09-26)

## Verdict

LANDED. The patrol is not a repo script: it is ZCode automation
`automation-a7c71ad1-f43f-403d-8677-105f5176df2b` (cron `0 8 * * *`, enabled,
workspace local_sovereign_agent), a prompt row in
`C:/Users/foste/.zcode/v2/tasks-index.sqlite`, table `automations`. That
prompt predated the living law and its step 4 drove the daily whole-file hash
refreshes the law forbids. The prompt now (1) reads
`scripts/index_fold_host.mjs verify` and counts living-ok and living-open as
PASS, never a re-register reason; (2) forbids whole-file refreshes of living
rows; (3) routes genuine living re-seals through `add --living`
(append-only originals) or `--living-open` (edit-shaped boards); (4) treats
LIVING PREFIX MISMATCH / LIVING TRUNCATED as tampering: report and file as
owed, never auto-refresh; (5) registers the patrol receipt through the fold
host, retiring hand-appended seq=epoch-ms events (the B2-157 phantom source).
DB readback verified: all clauses present, zero em-dash.

## Evidence with file:line quotes

- `watch/inbox/index_events.jsonl:3054`: `"ts": "2026-09-26T12:03:24+00:00",
  "op": "register", "file": "/board/inbox/LINKS.jsonl"` ... `"purpose":
  "hash refresh: gala-night writes evolved after registration", "writer":
  "drift-patrol-cron"` - whole-file, no living key. The patrol's last
  register, predating the 13:30:57.884Z law migration.
- 4 hash-refresh registers in 2h: `index_events.jsonl:2904` (11:35:54.086Z),
  `:3058` (12:40:34Z), `:3059` (12:47:37Z), `:3088` (13:21:20.489Z, purpose
  names "drift-patrol refreshes daily"). Law migration at `:3091`:
  `"living":true,"size":219904`.
- `watch/inbox/LIVING_HASH_LAW_20260926.md:73-75`: "the drift patrol must
  stop daily whole-file refreshes of living rows and may use this law
  instead."
- `scripts/index_fold_host.mjs:426`: "verify: ${ok} hash-clean, ${livingOk}
  living-ok, ${livingOpen} living-open, ...". Law section 6 names this
  output as the patrol's replacement gate.
- Behavior receipt: `watch/inbox/DRIFT_PATROL_20260926.md:10`, surface
  integrity row: "29 gala-night post-edit drifts ... all hash-refreshed".
- Live verify from `watch/inbox` 09-26: "973 hash-clean, 2 living-ok,
  1 living-open, 2 mismatched, 0 missing" - LINKS.jsonl and
  phone_relay_log.jsonl already PASS; the 2 mismatches are static rows.
- Writer-to-automation tie: `DRIFT_PATROL_20260915.md` header "writer:
  drift-patrol-cron, automation: automation-a7c71ad1 (daily 08:00)".

## Work done

1. Located the cron via sqlite (schtasks has no MagDriftPatrol row);
   answered B2-211's location question: the writer has no on-disk source,
   it is the automation prompt.
2. Wrote and ran `watch/inbox/burn_wave_20260926/B2_199_update_prompt.py`
   (.venv python, sqlite UPDATE, readback assert, em-dash assert refusing
   to write). Spec first: the owning spec is LIVING_HASH_LAW section 6,
   landed 09-26 before this change.
3. Tests: `pytest tests/test_index_fold_host.py -q` = 18 passed (7 living:
   growth passes, prefix mutation fails, truncation fails, open-shape
   insertion passes, plain re-add drops the flag).
4. Registered this receipt through the fold host from `watch/inbox` with
   `INDEX_WRITER=zcode-b2-199-patrol-living node
   ../../scripts/index_fold_host.mjs add ...` - the exact command form the
   amended prompt prescribes, proven to land inbox-relative.
5. Filed ledger row + 3 self-feed briefs (B2-214/215/216).

## Falsifier

The amendment is falsified if any future index_events.jsonl register with
writer `drift-patrol-cron` names LINKS.jsonl, QUEUE.md or
phone_relay_log.jsonl without a `living` flag, or any drift-patrol
hand-appended seq=epoch-ms event appears again. Check after the next 3 daily
08:00 runs. Secondary falsifier: the sqlite prompt row reverting (harness
rebuild or DB reset loses the amendment; there is no repo-side copy yet,
that exposure is filed as B2-215).

## Bibliography closed

Read whole or in relevant part: watch/inbox/LIVING_HASH_LAW_20260926.md;
scripts/index_fold_host.mjs; mag/shared_surface.py (items loop 190-309);
tests/test_index_fold_host.py (living tests); watch/inbox/index_events.jsonl
(LINKS.jsonl event history); DRIFT_PATROL_20260915.md, _20260926.md;
watch/inbox/burn_wave_20260926/QUEUE.md; memory/burns/LEDGER.jsonl;
memory/trajectory/steps.jsonl (patrol authoring steps);
C:/Users/foste/.zcode/v2/tasks-index.sqlite (automations table).
