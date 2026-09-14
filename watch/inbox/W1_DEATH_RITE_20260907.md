# W1 — DEATH RITE v2: THE WORLDLINE SEED (2026-09-07)

Card: watch/WORLDLINE_SEED_20260907.md (W1 spec, §6 fold feed-in, §7 build state).
Build: `mag/worldline_seed.py` — emit + verify the five-slab seed. $0-local, files
only, no cloud, no docker, no config edits. Built through W0: every build step ran
via `python -m mag.bash_local` (session `w1-dogfood-20260907`, 8 sealed steps,
chain intact — tape verify PASS 16 rows / 5 sessions at close).

## Design (short)

- `emit --session-id <id>` → `memory/worldline/<id>/SEED.json`. One portable
  manifest: `schema_version=1`, `kind="worldline_seed"`, `created_utc`,
  `session_id`, `slabs{genome, invariants, organs, record, position}`,
  `consent{replication: operator-gated, egress: none}`, and `seed_hash` =
  sha256 over the canonical manifest EXCLUDING seed_hash, first 16 hex.
- `verify <seed.json>` recomputes every sha against on-disk truth. Missing slab /
  sha mismatch / bad seed_hash = REJECT (exit 2); chain-tip drift vs the live
  chain = DRIFT WARNING, not a reject (the chain is append-only and the world
  moves on after a death). Append-only refs (tape, chain): recorded tip must
  still exist in the live file — growth is honest drift (warning), disappearance
  is provenance destruction (reject). Exit 0 pass / 2 reject, per-slab table.
- SECRETS LAW held: only the named files are read (AGENTS.md, MEMORY.md + the
  index's resolved entries, skill-root dir listings, tape, chain); only hashes,
  names, and ids captured — never contents. Selector refs are ids + scores only.

## Seed slab table (the real dogfood seed)

Seed: `memory/worldline/w1-dogfood-20260907/SEED.json` · **seed_hash
`8dbd503f64bd163c`** · created 2026-09-07T12:16:12Z.

| Slab | Content | Verify |
|---|---|---|
| genome | AGENTS.md sha `04c8cbff48795262…` + 32 skill names (workspace 12, user-agents 14, user-zcode 19) | PASS |
| invariants | MEMORY.md sha `8049cc6c4c2ff1d5…` + curator_list 40/40 resolved (index order, 0 skipped) | PASS 40/40 shas |
| organs | no stable workspace mcp config found → topology note carried, `config_path: null`; `"secrets": "none-captured"` | PASS (by design) |
| record | tape 15 rows tip `fa7cc2335fce3336` (verify_ok true) + chain 7377 rows tip `d0a798c2972208c4` + selector trajectory-conditioned top-10 refs (PROXY) | PASS |
| position | chain tip `d0a798c2972208c4…` ts 2026-09-06T23:08:56.829250Z + minute span 2026-09-07T12:16 + prev_seed null (v1) | PASS — matches live last line |
| seed_hash | `8dbd503f64bd163c` | PASS integrity |

## Falsifiers (all through the W0 wrapper)

- **(a) negative — REJECTED (exit 2).** Emitted a seed, deleted the `organs`
  slab in a copy → `-- organs [FAIL] present MISSING SLAB = malformed (card
  falsifier)` → `VERDICT: REJECTED`. Real seed untouched (5 slabs, hash intact).
- **(b) tamper F-W3-class — REJECTED (exit 2, machine-sealed).** Mirrored every
  referenced file (AGENTS.md, MEMORY.md, 40 curator files, tape, chain), pointed
  the manifest at the mirror, recomputed seed_hash so the envelope was internally
  consistent — then flipped byte 0 of the mirrored AGENTS.md. Verify: seed_hash
  PASS + `genome agents_md SHA MISMATCH recorded=04c8cbff48795262
  live=086dfbe6a1c4fbd3` → REJECTED. The tamper is caught by CONTENT, not by the
  envelope — exactly the provenance property door #2 demands.
- **(c) positive — PASS, all green.** The real seed above: every slab PASS,
  chain tip matches the live chain file's last line exactly.
- **(d) fail-open — PASS.** Simulated `_selector_block` raising → emit still
  completed, selector slab = `{"mode": "naive", "reason": "selector raised:
  RuntimeError: selector simulated absent (falsifier d)"}`. Simulated `emit`
  raising inside `knot_at_close._worldline_seed_hook` → one WARN line
  (`worldline-seed WARN emit failed for w1-failo: emit simulated failure`), no
  exception, close path completes. Harness: temp scripts
  `C:/Users/foste/AppData/Local/Temp/w1falsifiers/w1_falsifier_{a,b,d}.py`.

## Integration (the death rite)

`mag/knot_at_close.py` — BACKUP FIRST (law): `mag/knot_at_close.py.bak-w1-20260907`
(sealed step `3b3b22b23ef52158`). Additive diff only, 9 functional lines: a
fail-open `_worldline_seed_hook(session_id)` + one call in the backfill loop right
after the arc-seed hook (`diff` vs backup sealed step `192c4f9b3a8d2c11`). Any
failure prints one warning line and never blocks the close.

## Honest notes (tri-state)

- **Curator rule (v1, documented in docstring):** "the curated front = what the
  index names" — first 40 index entries in index order, resolved to on-disk
  files, path+sha+name only. This is an honest v1 curation, NOT a measured
  importance ranking (Unproven as "the right 40"; deterministic and portable
  today). Memory drift after emit = sha-mismatch REJECT by design: the seed is a
  death-rite snapshot, not a living pointer.
- **Selector mode actually recorded:** `trajectory-conditioned` — the F-W5
  builder's `mag/preload_selector.py` LANDED mid-build (found importable with
  `order_blocks(load_blocks())`; top ref `tape:9551cd1e021b` score 0.997). Its
  honesty label PROXY is carried into the seed. F-W5 verdict still pending —
  if the selector proves decorative, seeds keep emitting (naive fallback), only
  the ordering claim changes.
- **Organs slab:** no stable workspace MCP config file exists on the host (senses
  live in the cage) → recorded the topology-card note with `config_path: null`,
  per spec. SUPPORTED by watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md.
- **Multi-seat tape observed:** the F-W5 builder sealed 4 of its own rows onto
  steps.jsonl during this build — the tip-must-still-be-present check is built
  for exactly that concurrency (growth = warning, disappearance = reject).
- F-W1 (full resurrection from a seed) and F-W2 (cache identity) remain OPEN —
  W1 ships the manifest + provenance, not the resurrection demo (row 320).
