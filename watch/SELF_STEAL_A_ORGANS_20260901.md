# SELF-STEAL A — ORGAN INVENTORY (Salon lane A, deep self-steal 20260901)

Run: 2026-09-01 ~04:16Z. Lane: mechanical inventory. Sources: openclaw_catalog latest.json (ts 2026-08-31T11:33:52Z) + fabric.json + SURFACES.md D-bis + board receipts (room.jsonl tail-5000, ledgers, dated .md).
Evidence window: /board/room.jsonl tail-2000 spans 2026-08-29T22:14Z → 2026-09-01T04:15Z (4d). Dated .md/.jsonl receipts extend to 08-31/09-01.
Method: organ-mention grep across room.jsonl tail-5000 + all board ledgers/*.md. Any claim not under a dated byte = UNVERIFIED. /mag untouched (read-only). No `python -m mag.*` executed.

Class rules (per brief): EXERCISED-7d = dated evidence within last 7 days (>=2026-08-25). EXERCISED-30d = within 30d but older than 7d. DORMANT = 30d+ no evidence or catalog-only mentions. UNMOUNTED = named in catalog but no runnable mounting evidence. Evidence is membrane/ledger dates only.

## Crown organ table (all 16 verified to exist in catalog json)

| organ id | gloss | last-exercised evidence (date + surface) | class |
|---|---|---|---|
| memlance | ghost_memlance: select grounded states from MEMORY bytes, anti-synthesize | mentions in room.jsonl (12, incl `ghost_memlance`: 6 within tail-5000, window 08-29→09-01) | EXERCISED-7d |
| verkle-lance | verkle_lance: temporal map of verkle knot chain, parent_root→tip | room.jsonl (verkle: 42 in tail-2000); verkle chain is state surface (SURFACES C) | EXERCISED-7d |
| pylance | ghost_pylance: AST diagnose over our code, $0, anti-hallucination | room.jsonl (pylance 6, ghost_pylance 1 tail-5000); ledger/md refs 16 | EXERCISED-7d |
| steer | grok_steer: DFHack overlay, sit over live seat, steer don't patch-loop | room.jsonl (steer 40 tail-2000); steer_exp_001_receipts.jsonl all ts 2026-09-01T02:55→02:57Z (steering exp 001 PASS, water_ledger 03:02Z) | EXERCISED-7d |
| dnd | game_campaign: campaign engine owns truth, LLM narrates | room.jsonl (dnd 8; campaign 79 tail-5000); CAMPAIGN_MAP_20260831.md | EXERCISED-7d |
| chess | agent_arena: seat-vs-seat, python-chess oracle | room.jsonl (agent_arena 10, chess 10 tail-5000); ledger/md refs 44 | EXERCISED-7d |
| lab | lab_episode: Grey Swan stolen as Lab, blackout episodes | room.jsonl (lab_episode 15, lab 58 tail-5000) | EXERCISED-7d |
| mermaid | surface_render: inline hypervisor mermaid + bare-metal SVG | room.jsonl (mermaid 2 tail-2000; surface_render 7 tail-5000) | EXERCISED-7d |
| render-world | game_world_render: region glyph render | room.jsonl (game_world_render 1, render-world 0 tail-2000); ledger/md refs 2 — thin | EXERCISED-7d, thin |
| render-console | console_render: artifact console | room.jsonl (console_render 1, render-console 0 tail-2000); ledger/md refs 2 — thin | EXERCISED-7d, thin |
| cast | cast_server: cast page renderer (wearable/voice stack imports) | room.jsonl (cast 33 tail-2000); PACK_RACTOR_CAST_20260831.md | EXERCISED-7d |
| salon | lane_salon: verbose one board, monitor files | room.jsonl (salon 161 tail-2000); SALON_BUS_*_20260831.md (A/B/C/synthesis dated 08-31) | EXERCISED-7d |
| patches | openclaw_patches: /patches → Mag write jail | room.jsonl (patches/openclaw_patches 14 tail-5000); openclaw_traj.jsonl (ts 09-01) | EXERCISED-7d |
| corpus | seat_corpus: what to send each lane | room.jsonl (corpus 33 tail-2000; seat_corpus 25 tail-5000); CORPUS_TIER_D_MANIFEST.jsonl | EXERCISED-7d |
| fuel | fuel_feed: free-lane mill | room.jsonl (fuel 5 tail-2000; fuel_feed 27 tail-5000); fuel_feed lane_profile = SURFACES state surface | EXERCISED-7d |
| governor | governor: autorun decide/execute, one supervisor | room.jsonl (governor 9 tail-2000; 28 tail-5000); governor_autorun family listed in scanned_extra | EXERCISED-7d |

## Counts

EXERCISED-7d: 16 · EXERCISED-30d: 0 · DORMANT: 0 · UNMOUNTED (of crown): 0.
(Dormancy is concentrated in the 609 scanned_extra orphans, not the crown. Crown = all warm within the evidence window.)
UNBUILT surfaces (D-bis): 7 surfaces, 4 rows with code-existing-but-unmounted status; Mermaid grammar = 0 .mmd files on disk.

## 5 most glaring DORMANT organs (from scanned_extra, catalog-only / no board evidence)

Brief-note: "dormant" below = present in catalog scanned_extra but zero dated exercise in board evidence (membrane + ledgers). They exist as code/CLI names only.

1. **abundance_rogue** — empty origin in catalog; would give an audited harvest/mine organ if exercised (name suggests abundance mining). UNVERIFIED intent; reported only as catalog-presence + zero evidence.
2. **grok_desktop / grok_seat_burner / grok_frontier_loop** (grok family cluster) — the grok free-lane (SURFACES B free rotation) is a live paid-lane; exercising these would let the seat mine the free grok channel the way fuel_feed does paid lanes. Zero board evidence.
3. **unsloth_seat / lm_studio / ollama-adjacent (saelis_*)** — local free lane (SURFACES B: ollama 11 models + saelis-31b staged); exercising would route local + free compute through the seat. Zero evidence in window.
4. **x_surface / x_posts_mine / x_chat_mine / x_oauth** — X mining organs; exercising would run X research independent of web_search, matching the known X syndication lane. Zero evidence (x_search used, not these modules). UNVERIFIED mapping.
5. **jupyter / *nb side (module notebooks)** — notebooks exist in-tree (6-7 first-party .ipynb at /mag) but are UNWIRED per D-bis "PARTIAL (files exist, not wired)"; exercising would make live fleet organs of the interactive compute surface.

## Unbuilt-surfaces list (SURFACES.md D-bis), with on-disk status check

| Surface (D-bis row) | Role | Doctrinal status | On-disk check (verbatim) | Actual | Net status |
|---|---|---|---|---|---|
| Hugging Face | free stateless storage; hf_space.py 5 use-cases; local hub cache | MAPPED — code exists, deployment unbuilt | `hf_space.py` → yes (23324 B, 2026-08-08); `~.cache/huggingface` → NO such dir (ls fails) | code exists; HF cache dir NOT present | CODE-EXISTS / MOUNT-UNVERIFIED (cache claim UNVERIFIED) |
| Notion seat | knowledge surface for operator; INBOX active | INBOX active; API key present | `notion_api.py` → yes (6900 B, 2026-08-26) | code exists; INBOX active per doctrine text | CODE-EXISTS / ACTIVE-per-doctrine |
| z.ai frontends (chat/GLM/Smith) | extra UI surfaces on held accounts | UNMAPPED | no file check (not a named module) | n/a | UNMAPPED (doctrine) |
| Jupyter (kernel) | notebooks → live fleet organs | PARTIAL (files exist, not wired) | `/mag/*.ipynb` → 6 first-party notebooks (e.g. _live_dm, _restore, verify_*); `/mag/notebooks` dir → NO | 6 notebook files exist, no notebooks/ dir | PARTIAL — files exist, not wired |
| Mermaid | diagram-as-code grammar; git-diffable docs | UNBUILT | find `*.mmd` under /mag/mag → 0 | zero .mmd files | UNBUILT (0 files on disk) |
| Sci-fi corpus (Desktop preprints + Diamond Age) | doctrine source material, mine like sessions | UNMINED | not a named module; PACK_DIAMOND_AGE_SYNTHESIS_20260830.md + SALON_DIAMOND_AGE_* exist | mined via salon/pack lanes (receipts dated 08-30/31) | MINING-EVIDENCE exists (receipts), core corpus UNMINED |
| Instruction sets from the chain | standing waves/BRIEF built from verkle knots, deploy remote | pattern proven locally; remote deployment unbuilt | verkle_lance imports invariant_lattice (fabric); STEERING_SYNTHESIS_20260901.md exists | local proven (steering exp 001, 09-01); remote unbuilt | LOCAL-PROVEN / REMOTE-UNBUILT |

## Notes / caveats
- Dormancy in the crown is nil; the 609-item scanned_extra is the dormant mass. RANKING focus belongs there (all 16 crown are warm).
- EXERCISED "thin" markers on render-world / render-console: single mentions only, could be chatter not true runs — flagged for synthesis lane.
- Hand-count evidence is grep-based; a crown organ could run off-window (older than 4d evidence captured) without my seeing it — UNLESS it appears in a 30d check, which I did not run for every organ. Crown 7d classification is evidence-supported for the window shown.

VERIFY: `wc -l` below. All 16 table organ ids confirmed present in catalog json (node membership check returned `true`).
