# B8 DOGFOOD GWAP - arena banking + gps feed + idempotence proof

Lane B8, build-it-all wave 2026-10-05. Operator order: dogfood gwap on the
playground tree. LAWS kept: `.venv\Scripts\python.exe` only, no em/en-dashes in
my prose (pasted tool output stays verbatim), no git commit, blocked filed
never faked. No code touched.

## 1. Enumeration (moment 2026-10-05T07:10Z)

`tools/arena_gwap.py --status` pre-run (AS-OF 2026-10-05T07:11:38Z):
`ledger rows=709 distinct_scenes=576 dirs=110 banked=106 unbanked=4`

Unbanked run dirs with transcript.jsonl + DONE (my lane, banked below):

- `watch/inbox/playground/dnd0_20261004T095557Z`
- `watch/inbox/playground/dnd0_20261004T095858Z`
- `watch/inbox/playground/dnd0_20261004T100306Z`

Not bankable, classified not faked: `dnd0_20261004T180242Z`, `dnd0_20261004T190238Z`,
`dnd0_20261004T200420Z`, `dnd0_20261004T210227Z`, `dnd0_20261005T070223Z` carry
only `golden_vectors.json` + `session.md` (no transcript, tool says "nothing
bankable"); `tavern_20261005T070246Z` carries only `play.md` + `scenario.json`;
`scenarios_lane9` is a config/fixture dir, not a run.

The 4th status-unbanked dir `tavern_20261005T071101Z` was the hourly cron's own
LIVE fire (no DONE at 07:11Z). Deferred to the cron per the brief; the cron
banked it itself at 2026-10-05T07:12:43Z (ledger rows s728-s730: BLOCKED x2
silent cops + VERIFIED_AGREE x1, marker now present in the dir).

## 2. Banking (banking receipts = the tool's own GWAP_BANKED markers)

Command per dir: `.venv\Scripts\python.exe tools/arena_gwap.py --no-feed <run_dir>`
(--no-feed so the gps delta is attributable to the explicit feed runs in 4).
Pasted verbatim:

```
=== dnd0_20261004T095557Z ===
OK dnd0_20261004T095557Z: chatgpt=s710@1.0 deepseek=s711@1.0 dm=s712@0.3333 grok=s713@1.0 saelis=s714@0.3333 warden=s715@0.0
CHAIN: verify ok=True bad=None scenes_mapped=6
=== dnd0_20261004T095858Z ===
OK dnd0_20261004T095858Z: chatgpt=s716@1.0 deepseek=s717@1.0 dm=s718@0.3333 grok=s719@1.0 saelis=s720@0.3333 warden=s721@0.0
CHAIN: verify ok=True bad=None scenes_mapped=6
=== dnd0_20261004T100306Z ===
OK dnd0_20261004T100306Z: chatgpt=s722@1.0 deepseek=s723@1.0 dm=s724@0.3333 grok=s725@1.0 saelis=s726@0.3333 warden=s727@0.0
CHAIN: verify ok=True bad=None scenes_mapped=6
```

Banking receipts (tool-written markers, seq-stamped):
`GWAP_BANKED` in each of the three dirs, e.g.
`dnd0_20261004T095557Z: chatgpt=s710@1.0;deepseek=s711@1.0;dm=s712@0.3333;grok=s713@1.0;saelis=s714@0.3333;warden=s715@0.0`

My verdict mix of the 18 banked rows (s710-s727): VERIFIED_AGREE 9,
CHALLENGE 6, DISPUTE 3 (bytes from the ledger tail query; the dungeon rows
score by agreement_score, not uniformly CHALLENGE).

## 3. Ledger growth + chain verify (GATE CONTRACT)

- seq before: 709 rows (tip s709), moment 07:11:38Z
- my banking: +18 rows (s710-s727) = exactly the 3 dirs x 6 actors banked
- cron's concurrent own fire: +3 rows (s728-s730) at 07:12:43Z, not mine
- final: 730 rows; final status AS-OF 2026-10-05T07:15:36Z:
  `ledger rows=730 distinct_scenes=597 dirs=110 banked=110 unbanked=0`

Tool's own verify path over the full final file (invocation on an
already-banked dir; --no-feed so scenes_mapped=0 and nothing fed):

```
SKIP dnd0_20261004T100306Z: already banked
CHAIN: verify ok=True bad=None scenes_mapped=0
```

## 4. gps feed + idempotence proof

BLOCKER FOUND AND FILED (not faked): the first feed attempt, using the exact
full-map code path of `arena_gwap.main`, refused fail-closed
`UNMAPPED_SCENE: scene_id 'arena-tavern_20261004T083959Z-Brother Oswin' missing
from scene_to_model` and fed nothing (atomic two-pass design held: gps stayed
351). Cause: run dir `tavern_20261004T083959Z` was moved intact (transcript +
scenario.json + DONE + GWAP_BANKED) to
`watch/inbox/playground/scenarios_lane9/void_stamp_collision_tavern_20261004T083959Z`,
so the disk walk builds scene ids under the new name while the ledger keeps
the originals. 6 orphaned DISPUTE scenes affected. STANDING GAP for a future
lane: `arena_gwap.main`'s full-map walk still misses these 6 scenes, so the
tool's own auto-feed path refuses until the map builder learns the fixture dir.

Resolution this lane (no code touched): re-bound the 6 scenes through the
module's documented caller argument `scene_to_model`, models resolved by
`actor_payloads` from the moved dir's own bytes (scenario.json personas,
fail-closed source, no guessing):
Brother Oswin=anthropic/claude-haiku-4.5; Greta Thornwood=anthropic/claude-sonnet-5.5;
Ilse Marrow=anthropic/claude-haiku-4.5; Maud Ashgrove=anthropic/claude-sonnet-5.5;
Pell Quickfinger=anthropic/claude-fable-5.1; Sir Edric Vane=anthropic/claude-opus-5.5.

Feed run 1 (pasted verbatim; the feed walks the WHOLE ledger by design, so the
110 fed rows are the full backlog including this lane's 13 feedable new rows
9 AGREE + 3 DISPUTE + 1 cron AGREE):

```
GPS FEED RECEIPT: rows_seen=730 fed=110 skipped=269 distinct=461 duplicate_skipped=351 task_shape=arena-agreement-v1 chain_tip=eb001e06f4adfbf045dee39eb522cf283284023befc0a420383e45d8cf944835
```

gps ledger `tools/gps_mcp/gps_ledger.db3` verdict_log (task_shape
arena-agreement-v1): 351 -> 461, delta 110 = fed exactly. by_verdict:
VERIFIED_AGREE 148, CHALLENGE 224, DISPUTE 313, BLOCKED 45; skipped 269 =
CHALLENGE + BLOCKED (instrument asymmetry: judge-owed and tabooed rounds never
score).

Feed run 2 (idempotence proof, verbatim):

```
GPS FEED RECEIPT: rows_seen=730 fed=0 skipped=269 distinct=461 duplicate_skipped=461 task_shape=arena-agreement-v1 chain_tip=eb001e06f4adfbf045dee39eb522cf283284023befc0a420383e45d8cf944835
```

gps verdict_log after run 2: 461 -> 461, delta 0. Same chain tip both runs.
ZERO NEW ROWS on the second run: idempotence proven by bytes.

## 5. Ratchet (GATE CONTRACT)

`python tools/violation_ratchet.py check --changed` (venv interpreter), pasted
verbatim:

```
RATCHET check: scope=18 changed files; hits=12; registered=12; NEW=0; expired-exceptions=0
RATCHET: PASS — no unregistered debt.
ratchet exit=0
```

NEW=0, exit 0. No code touched this lane; the changed files in scope are the
wave's sibling landings plus my receipts/markers.

## 6. Files

- Banking receipts: `GWAP_BANKED` markers inside the three run dirs (tool-written)
- This receipt: `watch/inbox/build_wave_20261005/b8_gwap.md`
- Ledgers (byte truth): `memory/runs/gwap/arena-capability.jsonl` (730 rows),
  `tools/gps_mcp/gps_ledger.db3` (461 arena rows)
