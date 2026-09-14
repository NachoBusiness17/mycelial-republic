# PURPLE HARVEST B5 — BAD APPLE FIELD receipt (2026-09-06)

Builder: zcode B5 lane · card: `watch/PURPLE_HARVEST_TRIAGE_02_20260906.md` TRIAGE 06
(@linguinelabs "Bad Apple but it's playing on a fly's brain", 31,398❤ — the genre proof).
**Port of the genre to OUR substrate:** the video is rendered BY the fleet's behavioral
record, not ON it.

**Honesty line (the one the card demands):** the fly-brain demo ran on a connectome;
ours runs on the fleet's behavioral record; weights-volume tier is a later door. This
is the fleet's signed record as a display substrate — NOT inference on model weights.

## Shipped

- **Surface:** `dashboard/static/bad_apple_field.html` (NEW, 281KB single file, self-
  contained, no network). House conventions: dark field, errbanner fixture wired to
  `window.onerror` + `unhandledrejection`, nav.js include, canvas ImageData scaled
  pixelated, rAF loop with 30fps pacing, preallocated ImageData + typed arrays (zero
  per-frame allocs), keyboard controls (SPACE play/pause · R re-seed mapping · F
  raw-vs-field A/B · ←/→ seek ±1s), live falsifier strip, append-only ledger strip.
- **Nav:** one LINKS entry `["/static/bad_apple_field.html", "Bad Apple Field"]` in the
  game cluster (right after Shadow Walk). Backup `nav.js.bak-b5-20260906`; `node --check`
  clean; diff vs backup is exactly that one line.
- **Video source:** segment 0:00–0:40 (1200 frames) of the Bad Apple!! shadow video,
  96x72 1-bit, bit-RLE + consecutive-dedup (1200 → 1145 unique frames, 181,766 RLE
  bytes, ~248KB embedded JSON). Embedded, so the surface runs from file:// with no
  network — same doctrine as shadow_walk's embedded world.
- **Receipt:** this file.

## Substrate mapping (chunk stat → pixel effect)

Substrate = `state/shadow_work/chunk_manifest.json` (schema chunk_manifest/v1,
data_hash `aaad8ddf`, fnv1a32, "no hash no draw; ghost until vision_validated:true").
Grid 288x64, 16px chunks → 18x4 = 72 chunks; the 480x360 canvas maps every pixel into
the chunk grid (chunkOf[] precomputed). Each chunk's REAL stats precompute integer
render params at seed time; the frame is then transformed per-pixel:

| Chunk stat | Effect | Formula |
|---|---|---|
| `mean_law` | **EAT** — law-dark chunks eat the silhouette | `gain = 0.18 + 0.82·ln(1+mean)/ln(1+30.46)` (multiplied into lit value) |
| `max_law` | **BLOOM** — high-law chunks burn brighter | `bloom = 255·(0.30 + 0.70·ln(1+max)/ln(1+149))` (lit value) |
| `cells` | **DITHER** — thin/void chunks dissolve to Bayer dots | `dith = 16·min(1, 1.55·cells/161)`; pixel kept iff `bayer4[x,y] < dith` |
| `questions` | **WATER** — question-dense chunks wash cyan | lit color mixed toward (96,208,224) at strength `nQ·140/256` |
| `biome=weights` | **GOLD** — the weights annex gilds + sinks bg | lit mixed toward (232,201,106) @115/256; `bg += 8` |
| `cells→0` | **VOID** — empty chunks sink toward black-blue | `bg = 22·cells/161` (per-chunk background) |
| `vision_validated:false` | **GHOST** — the fog contract | lit value dimmed 216/256 on an 8px stripe keyed by `content_hash^seed`; all 72 chunks are ghosts today (0/72 validated) and render in ghost grade — the contract is honored, the code path for validated=true is live |
| `content_hash` | **PHASE** — per-chunk dither matrix + offsets | Bayer variant `(hash^seed)&3`, phase from hash bits; no RNG anywhere |

**NO random textures, NO passthrough:** every non-raw pixel value is an integer
function of (manifest stats, content_hash, seed, frame bit). **R (re-seed)** rebuilds
params from `mulberry32(seed)`: dither variant/phase and ghost stripes re-phase; the
stat→role table above is canonical and never permuted (documented on-page).

**CHAIN LAW AS RENDER PIPELINE:** every drawn frame is hashed with fnv1a32 over the
full 691,200-byte ImageData and chained — `head = fnv1a32(head_hex + ':' + frame_hash)`
— appended to the ledger (in-memory log unbounded, DOM strip capped at last 8 rows +
running total). Same frame + same seed + same view → byte-identical render → same
hash. Playback appends one row per video frame; pause appends nothing; seeks/reseeds
append exactly one row each; rows are never spliced or renumbered.

## Falsifiers — PASS (measured by the harness on the shipped code, not asserted)

Harness: `watch/PURPLE_HARVEST_B5_harness_20260906.mjs` — stubs the DOM, evaluates the
FULL shipped page script, drives the real loop and real keydown handlers (B1/B2 style:
the tested code IS the shipped code). Numbers from the run:

| Falsifier | Result | Numbers |
|---|---|---|
| Decode integrity | PASS | RLE stream consumed exactly: 181,766/181,766 bytes; 1200 frames, 1145 unique |
| Provenance (extra) | PASS | embedded bits == ffmpeg gray source, 48,384/48,384 pixels on 7 sample frames, 0 mismatches |
| (1) DETERMINISM | PASS | 23 frames sampled (stride 53), render twice: byte-identical AND fnv-equal, 0 mismatches |
| (2a) SUBSTRATE ≠ PASSTHROUGH | PASS | mean |raw−field| = **92.26** (threshold > 8), min 7.47 (the all-black title frames), over ALL 1200 frames |
| (2b) identity mode | PASS | field pipeline with neutral params == raw **exactly** (max diff = 0.0, all 1200 frames) |
| (3) PERF | PASS | render hot path median **1.00 ms/frame**, p95 1.19ms, max 1.77ms on the full 1200-frame segment (budget 8ms; Node 22 JIT — browser pending, see below) |
| (4) LEDGER | PASS | 600-tick play → 299 appends (30fps pacing exact); pause 40 ticks → delta 0; each seek → exactly +1 row (SEEK+1s/SEEK−1s); R and F → +1 row each; resume 240 ticks → 120 appends; row ids contiguous 1..424 throughout — append-only, never spliced, chain head 0x6f6c54dc at end of drive |
| (5) On-page strip | PASS | boot selftest prints 3 PASS markers (determinism / substrate / identity), 0 FAIL; live rolling median in HUD |

## Source provenance + license (honest)

- GitHub searched FIRST per house law: found `github.com/Felixoofed/badapple-frames`
  (community frame-dump repo: `frames.zip` 15.8MB pre-extracted PNGs + source
  `badapple.mp4`). Took the repo's mp4 (9,820,855 bytes, 480x360@30, 219s; verified by
  ffprobe) and extracted our segment locally with ffmpeg 8.1.2 (`scale=96:72`, gray,
  threshold 128). Source preserved at `watch/inbox/bad_apple/badapple.mp4` + extractor
  (`pack_frames.mjs`) + intermediate (`seg.raw`) + `PROVENANCE.md`.
- **License status:** the repo has NO LICENSE file (fan-distribution, offered "for all
  kind of your bad apple projects"); the video itself is the famous Niconico shadow PV
  of Alstroemeria Records' "Bad Apple!!" — freely distributed by its creators, THE
  canonical genre video, but **no formal open license**. Our use: non-commercial,
  local, attributed on-surface. Recorded honestly: fan-use under the genre's norms,
  not an open license.

## Birth defect caught (failure voice, one row)

First harness run FAILED (2a) at 7.47 with a suspiciously frame-independent number:
the render loops hashed `packed[row+…]` and never added the per-frame base offset —
every frame rendered frame 0 (the black title card). Fixed (`packed[pk+row+…]` in both
branches); the substrate number went 7.47 → 92.26. This is exactly what falsifier 2a
exists to catch. Second harness hang was a HARNESS stub defect (no `firstChild` on the
fake ledger element → the display-cap trim loop span), not shipped code — the real DOM
has firstChild.

## What was verified vs not (honest tape)

- **VERIFIED (Node 22 harness on the exact shipped file):** everything in the table
  above — decode, provenance vs the ffmpeg source bytes, determinism, transform
  magnitude, identity exactness, hot-path timing, ledger append-only semantics through
  the real key handlers, and the on-page selftest output text.
- **NOT VERIFIED (no browser run on this seat):** actual on-screen pixels, 60fps under
  a real compositor, keyboard feel, and the visual read of the field (gold annex,
  water wash, dithered voids). The harness executed every frame()-reachable code path
  with canvas stubs — logic verified, pixels not. The errbanner fixture is in place;
  if the browser path lies, it will speak.
- **UNPROVEN (marked, not asserted):** that this counts as "the room playing the
  video" in the genre's full sense — the fly demo's substrate LEARNED nothing either;
  what ours proves is legibility: the signed record can carry a signal without being
  passthrough (92.26 mean abs diff says the room is IN the image).

## Files

- `dashboard/static/bad_apple_field.html` (new, single file, 281KB incl. embedded frames + manifest)
- `dashboard/static/nav.js` (one LINKS line; backup `nav.js.bak-b5-20260906`)
- `watch/PURPLE_HARVEST_B5_harness_20260906.mjs` (falsifier harness)
- `watch/inbox/bad_apple/` (source mp4 + PROVENANCE.md + packer + seg.raw + frames_embed.txt)
- `watch/PURPLE_HARVEST_B5_BAD_APPLE_20260906.md` (this receipt)

Console access: `window.__BADAPPLE` exposes {FIELD, LEDGER, head(), draw(), selftest(),
time()} for on-surface poking.

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran the shipped harness fresh: EXIT=0, ALL FALSIFIERS PASS, every number
reproduces — decode exact (181,766 px, 1,200 frames), provenance 48,384/48,384
sampled pixels vs the ffmpeg source, determinism 23/23 byte-identical, substrate
mean 92.26 with identity mode exactly 0.0, hot path median ~1.0ms (budget 8),
ledger 424 rows contiguous through pause/seek/reseed/view-toggle, on-page selftest
3/3. Nav wired at nav.js:60, backup present. The caught birth defect (missing
per-frame base offset → every frame was frame 0, substrate 7.47 → 92.26 when
fixed) is exactly what falsifier 2a exists for — the doctor worked. License
honesty confirmed: fan-use under genre norms, recorded as such, attributed
on-surface. VERDICT: PASS. Pixels remain the open eye, same as B1/B2 — first
human load: errbanner silent, F-toggle showing the room IN the image.
