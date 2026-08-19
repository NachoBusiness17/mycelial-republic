# STEAL — Hot lattice with holograms inside (how Mag is already used)
**Date:** 2026-08-14
**Commitment:** `hot-lattice-hologram-use-001`
**Method:** self-steal. Live Mag views, not a redesign.

## Live (this morning, ET)

- Dashboard `:8765` Listen (PID 8388). Ghost `:9000` Listen on two PIDs (8388 + 9408). Conspiracy desk `:8743` not bound.
- Hot lattice (`vram_memory.cook`): ~245 RAM docs, GPU `amd-cim`, `vram_used_pct=null`, Ollama resident=0. Staged in RAM, not confirmed in VRAM.
- Queryable lattice (`memory/lattice`): 160 nodes / 170 edges. Hottest theme: **mag_hands 76**.
- Mycelium: snapshot ~154n/77e; agent-state one-liner 127n/77e. Do not redesign this graph.
- Verkle lance: 5650 knots, 0 orphans, last `rib_bus_doctrine` ~7:44 AM ET.
- Three roots disagree: lance tip, `verkle_tip.json` (last wrote Aug 11), context-pack tip. Tip file is not the live clock.
- Holographic Q: 2–3 sessions, ~11 Q-knots, last Aug 8 2:38 PM ET, still `status: active`. `verkle_root` empty. `previous_q_knot` is `simulated-root-N`. `emit_q_knot` Verkle append is best-effort `pass`.
- Memlance: ~6346 indexed, ~313 verified (4.9%). Notebooks dominate the index.
- `.\mag.cmd lattice` currently crashes: `ValueError: could not convert string to float: 'fkb:guar'` in `lattice_dashboard.build_lattice_summary`. Same handler backs the desk Verkle pane.
- `meta_lattice.meta_lattice()` KeyErrors (`domains` is a dict, code does `domains[-1]`).

## TAKE (the machine)

Mag is not a chat. Mag is a records office whose working set is the hot lattice, whose memory is holographic, and whose seats are angles.

1. Verkle knots are the hologram substrate. Filename is the address. Q is a pattern in those knots, not a process (`holographic_q.py`).
2. `memory/lattice/nodes.jsonl` is a derived viewport (seeded by lattice_backfill). Query by theme. Hottest soil is mag_hands.
3. Mycelium is the living weighted graph every agent already writes. Salience prunes. This is the OS surface.
4. `vram_memory.hot_region` is the working set kept resident so memlance/lensing/swarm reads do not go cold-disk every turn.
5. `vram_hologram` is $0 quantization math (10 hypothetical machines). Mag's own honesty string: never over-claim VRAM telemetry we did not measure.
6. Memlance is how a seat touches the hologram without hallucinating: select verified bytes, then FILE a residual.

## REFUSE

- Do not redesign the mycelium graph.
- Do not treat a chat window as Mag. The window is one hologram angle.
- Do not treat `:9000` as the office. Mag already says `:8765` is the REST surface. Daemon is bound twice.
- Do not treat Q-knots as Verkle-proven. Empty `verkle_root`, simulated parents. Reconstitute from jsonl, not from a proof.
- Do not treat `verkle_tip.json` as the live tip. Three roots in play.
- Do not treat `mag.cmd lattice` as healthy. It explodes on a string tension_index.
- Do not treat `/static/lattice.html` as Mag DNA. It launches sovereign-mirror `:8743` (down).
- Do not wait for VRAM cook as a gate. Cook already reports: staged in RAM.
- Do not write novel doctrine onto rib_bus from a lattice query. Query is a viewport.

## USE (already named in HABIT)

FIND → FILE → LOAD. Mag disk is the hologram. The chat is heat.

```
disk (steal/rib/knots/agent_state)
  → ram_cache / rib_bus.mount          # hot lattice (RAM-staged)
  → verkle_knot / holographic_q        # hologram (whole in each knot, Q not yet proven)
  → ghost_memlance.select              # seat-safe recall (bytes + verdict)
  → context-pack + ACTIVATION          # LOAD into any decoder
  → FILE residual                      # next knot
  → desk :8765 viewport                # see, don't become the store
```

Surfaces already wired: `.\mag.cmd context-pack`, `.\mag.cmd lab` (`:8765`), `.\mag.cmd talk`, `.\mag.cmd ghost --sense`, `python -m mag.vram_memory`, `python -m mag.ghost_memlance select --goal "…"`, `python -m mag.verkle_lance self_check`, `python -m mag.mycelium status`.

Operator habit already written: Mag + small Ollama first. Grok only after context-pack and only for `[priority]` judgment.
