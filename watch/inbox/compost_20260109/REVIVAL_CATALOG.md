# REVIVAL CATALOG - copy-paste resurrection for every re-pullable kill (2026-10-09)

Companion to `COMPOST_LEDGER.jsonl` + `COMPOST_MAP.md` section 5 item 2 (the
starter-script sweep, the mangos law generalized: every re-pullable kill gets its
one-liner written while the context is fresh). The graveyard becomes a catalog.

Law held here: every command's ingredients were byte-verified this sitting
(2026-10-09): registry tags HEAD-checked (HTTP 200), HF repos HEAD-checked
(HTTP 200), modelfile receipts opened, the local blob deletions confirmed (the
banked modelfiles' FROM paths are dead - revivals below swap FROM to the
registry tag, they do not resurrect a blob). No number below is hand-copied
without a cited receipt. Disk costs are re-pull costs (what the revival puts
back on C:).

## 1. The disk-class revivals (2026-10-08/09 rotation + purge)

| # | Kill (ledger row / manifest row) | Revival command(s) | Receipt / manifest path | Disk cost |
|---|---|---|---|---|
| 1 | frob/ling-3.0-flash (ledger `ollama-ling-3-0-flash`) | `ollama pull frob/ling-3.0-flash` | watch/inbox/DISK_INVENTORY_20261008.md (RESOLUTION: "+77GB (registry re-pull by name; last used 2026-09-16)"); modelfile receipt watch/inbox/model_modelfiles_20261008/frob_ling-3.0-flash.modelfile | 77 GB |
| 2 | qwen2.5:32b (ledger `ollama-qwen25-32b`) | `ollama pull qwen2.5:32b` | same DISK_INVENTORY receipt (rotation table + RESOLUTION "+19GB"); modelfile receipt watch/inbox/model_modelfiles_20261008/qwen2.5_32b.modelfile | 19 GB (shares its base blob with row 3; the PAIR was +19GB together at kill time) |
| 3 | maze-keeper, the Modelfile variant (ledger `ollama-maze-keeper`) | two steps (the banked FROM blob sha256-eabc98a9... is deleted, verified gone from ~/.ollama/models/blobs; the base must come back first, then FROM swaps to the registry tag): (a) `ollama pull qwen2.5:32b` (b) `sed 's|^FROM C:.*|FROM qwen2.5:32b|' watch/inbox/model_modelfiles_20261008/maze-keeper.modelfile > /tmp/maze-keeper.modelfile && ollama create maze-keeper -f /tmp/maze-keeper.modelfile` | watch/inbox/model_modelfiles_20261008/maze-keeper.modelfile (15,274 bytes, the full 15KB kit per the ledger's compost note) + DISK_INVENTORY RESOLUTION | +KB on top of row 2 (variant layer only; base blob is row 2's 19 GB) |
| 4 | unsloth/gemma-4-31B-it-GGUF (HF cache purge) | `huggingface-cli download unsloth/gemma-4-31B-it-GGUF --revision c1ac76e99d5513b141e8adde7288b85c3f9c32ec` | watch/inbox/disk_audit_20261009/cleanup/HF_PURGE_MANIFEST.json (bytes 20,536,614,478, status DELETING; purge executed, cache verified empty of it) | 20.5 GB (19.1 GiB) |
| 5 | slashreboot/saelis-31b (HF cache purge) | `huggingface-cli download slashreboot/saelis-31b --revision 8aca6a7d2c96213d10c76be92250109372e9309e` | same manifest (bytes 16,908,001,107) | 16.9 GB (15.7 GiB) |
| 6 | Qwen/Qwen3-8B (HF cache purge) | `huggingface-cli download Qwen/Qwen3-8B --revision b968826d9c46dd6066d109eabc6255188de91218` | same manifest (bytes 16,397,434,674) | 16.4 GB (15.3 GiB) |
| 7 | google/tabfm-1.0.0-pytorch (HF cache purge) | `huggingface-cli download google/tabfm-1.0.0-pytorch --revision 77cb9cc1b4fd3a9c77fbb9552c218200bb4dab83` | same manifest (bytes 6,557,890,193) | 6.6 GB (6.1 GiB) |

HF rows 4-7 total: 60,399,940,452 bytes = 56.3 GiB (sum of the manifest bytes
rows; the DISK_INVENTORY relief list called it "~60GB", same number rounded).

Ingredient checks run this sitting: registry.ollama.ai HEAD 200 on
`library/qwen2.5:32b` and `frob/ling-3.0-flash:latest`; huggingface.co
`/api/models/<repo>` HEAD 200 on all four HF repos; `huggingface-cli.exe`
present in `.venv/Scripts/` (huggingface_hub 1.26.1); both dead FROM blobs
confirmed absent from `~/.ollama/models/blobs/`; `ollama list` confirms none of
the three ollama kills currently installed. Rows 4-7 are NOT yet
COMPOST_LEDGER rows (map section 6: "rows when the purge fires" - the purge
fired 2026-10-09T02:16Z per the manifest ts; they ride this catalog now, the
ledger row is owed at the next closeout).

## 2. gemma-4 seat (ledger `gemma4-seat`) - console steps, 0 disk

The seat is the OpenRouter free lane, upstream Google AI Studio; it died
PATH-DARK on 429 upstream_provider_shared_pool with the estate key valid
(receipt watch/inbox/LAND_L3_gauntlet_seat.md section 2, probe 2026-10-07,
model google/gemma-4-26b-a4b-it:free; the snapshot also carries
google/gemma-4-31b-it:free - which variant the operator meant is still the OWED
referent question). Revival is console action, not code:

1. Get a Google AI Studio key (aistudio.google.com console; the 429 metadata
   names "Google AI Studio" as the upstream provider).
2. Add it BYOK at https://openrouter.ai/settings/integrations (the remedy_hint
   URL in the banked 429 body). Alternative: provider routing per
   https://openrouter.ai/docs/features/provider-routing.
3. Re-probe the path (one curl, key never printed):
   `curl -s https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" -d '{"model":"google/gemma-4-26b-a4b-it:free","messages":[{"role":"user","content":"ping"}]}'`
4. On light: re-run the schema-door restage same day (the ledger's revival
   condition): `probe_comics_schema_restage.py --stage` then one fleet cycle
   (watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/LAND_L1_schema_door.md
   section 2 is the last run's shape).

Disk cost: 0 (remote free lane). Receipt:
watch/inbox/LAND_L3_gauntlet_seat.md + git 714e1be01.

## 3. xai SD card reissue (ledger `xai-card-reissue`) - GATED ON MONEY

**GATED: operator order 2026-10-08, verbatim "stop asking for xai reissue its
not coming until i have money i do not"** (watch/inbox/DAWN_REPORT_20261006.md
item 4, the PARKED marker). Revival condition per the ledger: the operator
states money exists and asks for the reissue unprompted. No window re-raises
this item until then.

Steps when the gate opens (the key is already wired - .env line 7
XAI_SD_API_KEY, verified present; the account is 403-unfunded, a funding state
not a capability verdict per the ledger compost):

1. Operator adds credits / a valid card to the xAI SD account at
   console.x.ai (the only human step).
2. Re-verify with the banked probe shape (grok-4.7 paid run receipt:
   watch/inbox/GROK47_LUNCHEON_INTEL_20260929.md; 13 models live-verified
   2026-09-29 on this account).
3. Judgment dispatches resume on grok-4.7 per the DRIVING LADDER with every
   paid dispatch banking usage in its receipt.

Disk cost: 0. Cost class: credits (the last measured grok-4.7 run on this key:
usage total_tokens 5365, cost_in_usd_ticks 242180000 per the luncheon intel
receipt line 3).

## 4. Other ledger rows with verified one-command revivals (no disk)

| Kill (ledger row) | Revival command | Ingredient verified | Receipt |
|---|---|---|---|
| mangos-mysqld | `scripts\start_mangos_db.cmd` | script present in scripts/ | git 2894e55ba (the starter-script law minted at death) |
| kill-list-unreferenced-0908 | copy the organ back to its original path per the per-file table | attic/kill_list_20260908/MANIFEST.md present (path/bytes/sha16/reason per file) | attic/kill_list_20260908/MANIFEST.md |
| gps-embed-substrate | `.\.venv\Scripts\python.exe -m tools.gps_mcp.gps_embed_trial` (rerun the banked trial; sidecar + instrument live) | tools/gps_mcp/gps_embed_trial.py + models/embeddinggemma-2-onnx/onnx/model.onnx present | watch/inbox/gps_embed/GPS_EMBED_TRIAL.md; gate on WHEN: the shape tripwire tools/shape_tripwire.py (this lane's deliverable 2) |
| lite-lane-mates | operator re-points the lane, then un-dormant in configs/providers.yaml and `set LITE_LANE_ACTIVE=1` | mag/lite_guard.py:229 reads the lever | watch/inbox/LITE_LANE_PULL_20261003.md |

Not re-pullable, listed for completeness so nobody hunts for a command:
athena-class (HELD for operator ruling - the FROM-blob is local-only, no known
registry source; deletion would be unreconstructible), hermes-premium-rung
(key2 top-up, a human/credits act), city-generator-v2 (a $64-$199 buy), and
every claim/idea row (their revivals are conditions, not commands).

Falsifier for this catalog: any command above that fails on a fresh shell with
its ingredients present = a fabrication; fix the row the same sitting it is
found, and re-HEAD the registry tags quarterly (registry tags rot silently -
the same death class as playhouse-dependency).
