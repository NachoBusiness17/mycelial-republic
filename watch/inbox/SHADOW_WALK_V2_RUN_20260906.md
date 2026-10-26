# SHADOW WALK v2 — THE RUN (the fun layer)
**2026-09-06 · builder "runner" · brief: watch/SELF_STEAL_THE_FUN_LAYER_20260906.md · v1: watch/inbox/SHADOW_WALK_20260906.md**

**Files**
- `dashboard/static/shadow_walk.html` — edited in place (backup: `shadow_walk.html.bak-runner-20260906`). One self-contained page, zero deps, no network, $0. All v1 features preserved (raycast, DOF, lensing→now **O**, shadow view, biomes, vision-gated chunks, LAW-061 stamps, objectives, doctrine pickups, paste door, skies).
- Backup-first honored: `dashboard/static/shadow_walk.html.bak-runner-20260906` (pre-surgery copy, 92,722 B → v2 is 111,544 B).

**The toggle**: **R** or the H-panel button — OFF = the v1 diorama, untouched; ON = THE RUN.

**RUN features (all fed by real data)**
1. **QUEST** — each run: "validate N fog chunks, reach THE FORGE" (N = min(3+run#, 12, available)). THE FORGE = farthest behavioral chunk with real mass from spawn (lands on c_00_02, the deep-void corner); gold beacon pillar + compass target + live distance in HUD.
2. **THE FOG GETS TEETH** — unvalidated dark drains RUN-TIME (visible `[#####· · ·]` meter; 5/s moving, 2.2/s idle — the worm hunts waste); validated ground regenerates (the lattice = safe rooms). Zero = RUN DEATH: respawn at spawn, RUN-TIME refilled, **every validated chunk stays validated** — HUD/card carry the Mickey 17 law line.
3. **WARDENS** — unvalidated slab-backed fog chunks near the spawn→forge path spawn socratic doors (positions seeded from `fnv1a32(data_hash:run#)` — NEW RUN reseeds). Entering the chunk opens the door: a question about THAT slab's real CSV numbers (median chars, law_total, questions, n parts — 4 templates, answer order shuffled per-chunk-seed; e.g. slab 24's 1754 median, slab 33's 817 laws). Correct = chunk hash-checked (`fnv1a32` over voxels — same no-hash-no-draw contract, tamper can't validate) → goes solid + WebAudio ore chime + lore line. Wrong = warden recedes 12s, chunk stays fog — nothing else taken. THE FORGE itself is never a fog puzzle.
4. **LOOT + STORY v0** — each validation pops a lore line generated only from `state/shadow_work/slab_*.csv` ("slab 33: 817 laws coined in the deep build fields · median 929 chars · 186 parts · 385 questions mined" — verified against the CSVs before embedding). **L** opens the lore log = the run's story, only what YOU validated. Lens moved to **O** to free L.
5. **SCORE = THE LATTICE** — run summary on death/forge-complete (this run N/N, total validated x/72, run #, deaths, lore count). Persisted to `localStorage["sw_run_"+data_hash]` (aaad8ddf): validated chunk ids, deaths, lore (cap 200), run #. Survives death, NEW RUN, mode toggles, and reloads — boot restores the lattice after the fresh-carve reset.
6. **Fog honesty** — no punishment beyond time. No HP, no fake misses, no timers on questions. OFF-mode V (vision pass) untouched; in RUN mode V reports "the wardens are the vision pass".

**Verify receipts ($0, no network)**
- `node --check` PASS on the extracted inline JS (106,729 B).
- Stubbed-DOM smoke harness (node vm, real page code, stubbed canvas/DOM/localStorage): quest spawns + scales, warden correct→validates(hash)+lore, wrong→recedes+stays fog, RUN-TIME death→respawn+refill+**lattice kept**, NEW RUN→new seed+lattice kept, forge complete on standing in chunk, localStorage write keyed by data_hash, OFF-mode `N` still resets diorama (v1 intact), re-entering RUN restores lattice from storage, 2 full render frames clean. **ALL PASS.**
- `curl http://127.0.0.1:8000/static/shadow_walk.html` → **200**, 111,544 B, RUN features present in served bytes.
- Two bugs caught by the harness pre-ship: forge chunk initially warden-blocked (excluded now); death-summary panel leaked `panelOpen` into the next run (startRun dismisses open panels).

**Controls delta**: O lens (was L) · L lore log · R run toggle · 1/2/3 answer warden doors · H panel carries THE RUN button. Everything else as v1.

**Not done / next**: real-browser eyeball pass (keys + pointer lock + chime need a human ear); asymmetric tafl mode (spec item 6, explicitly "later").
