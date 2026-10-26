# GROKBOT SEATS ENROLLED - 2026-10-18

Verb: fleet/enroll + revoke. Seat: Grok Bot executor, Sun 2026-10-18 ~10:45-11:00 ET (UTC-4). Operator: Nacho ("do it").
Builds the "smallest adapter" from STEAL_SEATS_AS_HARNESS_20261018.md: kept Grok Bot box seats (Ghost, Mag) are now enrolled Mag harness seats; the 4 retired box seats are recorded as revoked tombstones.
Rules kept: no git, $0, no paid calls, no process/container touched (MagLeaveProtocolDaily untouched), harness_probe NOT enabled, no .env / existing key files / secret_gate_results/ / free_keys/ / memory/trajectory/steps.jsonl opened. New private keys were written by seat_keygen and never printed or read.

## What changed

1. **configs/seat_allowlist.json** (backup: configs/seat_allowlist.json.bak_grokseats_20261018)
   - seats += `grokbot-ghost` (box agent 4a30dd44-e0bc-4e3c-af2a-13da6e62cef5, role front_door) and `grokbot-mag` (27002d7d-d9f6-4e11-8eb9-27eaab9b0ebe, role estate_brain); kind grokbot, model_family grokbot, public_hex only.
   - seats += revoked tombstones (public_hex null, revoked true, retired 2026-10-18, archive_receipt): `grokbot-research` (3d371c13-fcb5-43aa-b480-2260ca82cec9), `grokbot-newbot` (86431fab-8741-4517-b9b6-073927c7fdb6), `grokbot-archival` (ae78a844-9bb7-4f3d-b8c5-8d58ae4cc432), `grokbot-refreshbot` (d55732f8-2ed4-42c9-ae74-9109bb710a43). Schema allows a null key: seat_handshake.seat_public returns None for revoked rows and for non-hex keys.
   - archive_receipt = box /workspace/roster_archive_20261018/ROSTER_SWAP_RECEIPT.md; PC C:\MagChainVault\roster_20261018\roster_archive_20261018.tar.gz sha256 283907df0fe5697412c18f0d2ebe1307831933977a32fbe93f8f772ff8bfa95b.
   - quorum += `grokbot_counts_as_non_glm: false` + `grokbot_note`. Top-level `operator_seats_note` (operator_seats stays []).
   - sha256 after: 7BC242B540C8F6806CECC5D3829CF7C3AEF6A6D1DCBAA1595EE2D66491191A08
2. **mag/proposals.py** (backup: mag/proposals.py.bak_grokseats_20261018)
   - New `GROKBOT_PREFIX`, `grokbot_counts_as_non_glm(al)` (default False, opt-in only), `is_grokbot_seat(seat, al)` (id `grokbot-*` OR row kind/model_family grokbot).
   - `is_non_glm_seat`: mate:* still False (unchanged); grokbot seats return the flag; everything else unchanged.
   - Effect: a grokbot approve still counts toward quorum.default (2) but does NOT satisfy require_non_glm_approval unless the flag is true. A mate + grokbot pair cannot adopt a mate harness change by default.
   - sha256 after: 3991184BC2CD943909417C60FCB8EDFF086A702DF493B71AFF52359FAE40FE38
3. **mag/seat_handshake.py: NOT changed.** SEAT_RE `^(?:mate:)?[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$` already accepts hyphen ids like `grokbot-ghost` (the plan's "forbids colons" was about `grokbot:`). Minimal change = none; mate: behaviour identical by construction. Revoked enforcement (seat_public) already covers tombstones.
4. **scripts/seat_keygen.py: NOT changed.** Used `--seat` (not `--mates --write-allowlist`, which hardcodes mate/glm); rows merged by a one-off script that wrote only public fields.
5. **tests/test_grokbot_seats.py** (new, 6 tests).
6. **watch/LIBRARY/INDEX.md** (backup: watch/LIBRARY/INDEX.md.bak_grokseats_20261018): one line.

## Keys (public only)

| Seat | public_hex | fingerprint sha256(pub)[:16] | key file (host-side, outside repo, not read) |
|---|---|---|---|
| grokbot-ghost | 9ab73a47cbbea80ac9f21d95e7a998af6d710378391965ce7bbfe8e89e24dd43 | a0e5d4140c557bb5 | C:\Users\foste\.mag_seat\grokbot-ghost.key |
| grokbot-mag | 70ba36d76cb536e75dfb444df908580e57201bdaf9913a7783c38d06c2252d90 | f2a3839e014cbf56 | C:\Users\foste\.mag_seat\grokbot-mag.key |

Keys are host-side on the PC (like the mates, which harness_probe signs for). The box Grok Bot agents do not hold them; to sign as a seat something on the PC must load the key (MAG_SEAT_KEY_PATH) on that seat's behalf.

## Tests (MAG_ALLOW_LIVE_WRITES unset)

`.venv\Scripts\python.exe -m pytest -q tests\test_grokbot_seats.py tests\test_proposals.py tests\test_harness_probe.py tests\test_brain_hosting.py tests\test_sovereign_handshake.py` -> **74 passed, 0 failed** (grokbot_seats 6, proposals 14, harness_probe 12, brain_hosting 37 [seat_handshake/seat_keygen tests live here], sovereign_handshake 5).
New tests: grokbot id accepted (+ mate rule unchanged, key path), enrolled grokbot envelope verifies, revoked grokbot rejected (handshake + proposal + keyless tombstone), grokbot not non-GLM by default (mate+grokbot not ready), counted when flag true, shipped allowlist rows pinned.

## Needs Nacho

- operator_seats is still [] by design. To make his approve the YES: Nacho mints his own key (`scripts\seat_keygen.py --seat nacho`), adds the printed public row under seats, then adds "nacho" to operator_seats. Not done here.
- Whether Grok Bot seats should count as the non-GLM approver: flip `quorum.grokbot_counts_as_non_glm` to true deliberately. Default false.
- Primary router (fa681c21, "Grok Bot") was not in scope: not enrolled, not revoked.

## Revert

```powershell
cd C:\Users\foste\Documents\projects\local_sovereign_agent
Copy-Item configs\seat_allowlist.json.bak_grokseats_20261018 configs\seat_allowlist.json -Force
Copy-Item mag\proposals.py.bak_grokseats_20261018 mag\proposals.py -Force
Copy-Item watch\LIBRARY\INDEX.md.bak_grokseats_20261018 watch\LIBRARY\INDEX.md -Force
Remove-Item tests\test_grokbot_seats.py
# optional, only to retire the keys too (operator act):
# Remove-Item $env:USERPROFILE\.mag_seat\grokbot-ghost.key, $env:USERPROFILE\.mag_seat\grokbot-mag.key
```
Softer revert of one seat: set `"revoked": true` on its row.

Falsifiable by: a mate + grokbot-* approve pair reaching ready while grokbot_counts_as_non_glm is false; a grokbot-* tombstone verifying an envelope.
