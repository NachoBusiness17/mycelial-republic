# B18 - Mates pack refresh with today's laws (2026-09-30)

Seat: builder lane, file ownership `configs/mates.yaml` only (the dispatcher
needed zero changes: the mission template already renders the laws block
verbatim, so `tools/leave_dispatcher.py` is untouched).

## What landed (3 new laws in the shared `laws` block, 6 -> 9 bullets)

1. **Positive steering steers YOU too** (operator law 2026-09-30): an error
   during improvement is LOGGED, not spiraled on; and mates' ASKS never
   generate distress content when a positive-frame design answers the same
   question. Wording anchored to the operator's own law as quoted in
   LM7_POSITIVE_GPS.md.
2. **RAM gate** (shared-box law, never swap the estate): never launch a job
   needing more than free RAM minus 2 GB; if it does not fit, POLL until it
   does. Precedent wording: IMP8's free-RAM guard + auto-launcher
   (IMP8_REPLICATION_RUN.md, gate-then-poll, never launch into swap).
3. **Drop-ledger awareness** (one line on discoverability): receipts land in
   the indexed world (watch/inbox, the append-only drop ledger behind
   INDEX.json) - write them to be FOUND: descriptive filename, real search
   terms, no burying.

## Proof trail (all commands run with .venv/Scripts/python.exe)

- YAML parses: `yaml.safe_load` OK, schema mag_mates.v1 unchanged, version
  2026-09-30, 8 mates intact, 9 law bullets, zero em-dash characters in file.
- Seal: `tools/config_seal.py update --by B18-mates-refresh --note ...`
  (60 files sealed) then `verify` = PASS (sealed=60 live=60 modified=0
  missing=0 unsealed=0).
- Render: the 20260930 mission packs were stale unclaimed drafts from this
  morning's auth-dead fire (dispatcher_20260930.log ends at the 08:00:02
  START lines; zero .claim sidecars; zero receipts in
  watch/inbox/mates_leave_protocol/receipts/), so all 8 were removed and
  `tools/leave_dispatcher.py --dry` rewrote them: DRY COMPLETE, 8 packs,
  8 constant-argv invocations NOT run. All 8 packs contain the three new
  laws (grep loop, zero misses); mission_20260930_01_cartographer.md shows
  the full 9-bullet laws section plus its STEER row.
- Tomorrow 08:00 (2026-10-01) is the first REAL fire: datetime.now() rolls
  to 20261001, so fresh packs render with these laws even without today's
  stale-pack removal.

## JOURNEY

Read mates.yaml -> read leave_dispatcher.py + config_seal.py (mechanics) ->
checked missions dir (20260929 + 20260930 packs) -> dispatcher log showed
today's fire started 8 runners then died on auth, no claims/receipts left ->
chased "drop ledger" through skill_drop.py (wrong: skill breadcrumbs),
AI_DROP_FIRST_READ.md (operator drops), then landed on watch/inbox
INDEX.json purpose line: derived from append-only index_events.jsonl = the
drop ledger -> RAM-gate wording mined from IMP8 receipt -> edit, validate,
seal, dry-run render proof.
