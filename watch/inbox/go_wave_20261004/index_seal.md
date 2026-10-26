# index-seal receipt (GO wave 2026-10-04, lane 5)

GO item 5 of corpus/steal/MASTER_MICKEY17_V2.md section 9 (a13-receipts-census rows #0, #2, #3):
refold INDEX.json, seal the 4 unregistered receipts, rerun the name greps.
Lane: index-seal. Moment of receipt: 2026-10-04T09:10:34Z (date -u).

## Sub-item 1: refold INDEX.json (scripts/index_fold_host.mjs)

Before-state (banked before any action; `wc -l watch/inbox/index_events.jsonl` + grep on INDEX.json):

- index_events.jsonl: 10,079 lines
- INDEX.json fold: derived_at 2026-10-03T12:09:53.009Z, event_count 9237, active_items 2700
- drift = 10,079 - 9,237 = 842 events stale (the a13 row measured 747 at its moment: 9,984 vs 9,237; +95 more events landed between that census and this lane)

Command: `node scripts/index_fold_host.mjs rebuild`

Output: `rebuild: folded 10076 events -> 2932 active items` (3 legacy malformed lines 94,95,96 skipped by the tolerant reader, reported on stderr; exit 0; the WARN lines are the fold's standing nonce-gap + malformed-line warning channel, historical, untouched by this lane)

After: derived_at 2026-10-04T09:08:52.531Z, event_count 10076, active_items 2932.

## Sub-item 2: seal the 4 unregistered receipts (tools/md_record_seal.py)

Lane 3's amendment of frontier_delta_register_20261003.json confirmed on disk before sealing
(11,797 bytes, top-level {meta, rows} shape, head shows "top-level object since 2026-10-04 (was a bare 14-row array)").
Content untouched by this lane; sealed as-is.

Command per file (4 invocations, sequential):

```
printf '{"tool_input":{"file_path":"C:/Users/foste/Documents/projects/local_sovereign_agent/<path>"}}' | .venv/Scripts/python.exe tools/md_record_seal.py seal
```

All 4 exited 0. Result: 8 events appended (register + autoseal per file); log went 10,079 -> 10,087 lines (`wc -l`).

Seal ids (register events, writer md-record-seal, class receipt; sha256 re-proven against disk bytes with sha256sum after sealing, all 4 match):

| file | seq | nonce | sha256 (register == disk) |
|---|---|---|---|
| frontier_delta_register_20261003.json | 1790901937830714513 | 2855 | 9816bd7443f0ae88f1b6968688e76430a9a19f51a47527cdee8a59f89077e98b |
| xai_grok47/GROK_PREREG_ADVERSARIAL_20261003.md | 1790901937830714514 | 2856 | 465cae95da40fb4d81020d8d19c5cf30053677c1398c8cdaf45c04312c8c5969 |
| xai_grok47/GROK_W4_RERUN_PROTOCOL_20261003.md | 1790901937830714515 | 2857 | 140ca100a76946618116f057f7b6b3257ce806766178f828abe616e0a9ece950 |
| xai_grok47/GROK_OCTOBER_FOLD_20261003.md | 1790901937830714516 | 2858 | 51cf8d3c4d9fc5e3d636368caa283442292420db3adfa60741e21914cba2af37 |

Note: the register file's sealed sha 9816bd74 differs from the a13 row's disk sha c834420b because lane 3's amendment changed the bytes after that census; the seal anchors the post-amendment bytes. GROK_OCTOBER_FOLD's sha 51cf8d3c matches the a13 row byte-for-byte (unchanged since census).

Refold after sealing (row #2's steal: "mint their register+autoseal events, then refold INDEX.json"):

Command: `node scripts/index_fold_host.mjs rebuild`
Output: `rebuild: folded 10084 events -> 2936 active items` (10,087 lines minus the same 3 legacy malformed lines; derived_at 2026-10-04T09:09:54.265Z)

## Sub-item 3: name greps (commands and counts)

Command: `grep -c <name> watch/inbox/index_events.jsonl` and `grep -c "\"path\": \".*<name" watch/inbox/INDEX.json`, per name from the a13 row's checks_run battery.

| name | events (before -> after) | INDEX items |
|---|---|---|
| parable_day_one_20261003 | 2 -> 2 | 1 |
| mag_rails_plugin_spec_20261003 | 2 -> 2 | 1 |
| envelope_50w_20261003 | 2 -> 2 | 1 |
| burn_claims_50wide_20261003 | 2 -> 2 | 1 |
| frontier_delta_steal_20261003 | 2 -> 2 | 1 |
| dd-actualplay-intel | 6 -> 6 | 1 (gala_20260925/dd-selfsteal/lanes/dd-actualplay-intel.json) |
| DND_ACTUALPLAY_INTEL | 1 -> 1 | 0 (by design: its one event autoseals corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md, a corpus/ path the inbox fold drops as outside; corpus files keep the autoseal journal line only per md_record_seal.py inbox_rel; its INDEX surface is the dd-actualplay-intel.json item above) |
| frontier_delta_register_20261003 | 0 -> 2 | 1 |
| GROK_OCTOBER_FOLD_20261003 | 0 -> 2 | 1 |
| GROK_PREREG_ADVERSARIAL_20261003 | 0 -> 2 | 1 |
| GROK_W4_RERUN_PROTOCOL_20261003 | 0 -> 2 | 1 |

All 11 receipt names are now queryable: the 4 formerly zero-event receipts are register+autoseal sealed and lifted into INDEX.json as active items.

## INDEX counts, before -> after (full arc)

- event log: 10,079 lines before -> 10,087 lines after (+8: the 4 register + 4 autoseal events)
- fold: event_count 9237 / active_items 2700 / derived_at 2026-10-03T12:09:53.009Z (stale, 842 behind)
  -> event_count 10076 / active_items 2932 / derived_at 2026-10-04T09:08:52.531Z (first refold)
  -> event_count 10084 / active_items 2936 / derived_at 2026-10-04T09:09:54.265Z (second refold, post-seal)

## Files touched

- watch/inbox/INDEX.json (fold output only; twice via scripts/index_fold_host.mjs rebuild)
- watch/inbox/index_events.jsonl (append-only; +8 events via tools/md_record_seal.py seal)
- watch/inbox/go_wave_20261004/index_seal.md (this receipt)
- No content edits to any receipt: frontier_delta_register_20261003.json and the three xai_grok47 files were sealed as-found.

## Blockers

None. Every sub-item executed as specified. Not run (out of lane scope): full `verify` sweep of all 2,936 items, no pytest, no git commit (coordinator commits).
