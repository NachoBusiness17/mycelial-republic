# PRIMER_capture_spec (anthropic/claude-opus-5.5, turn 1, channel: content)

# PRIMER CAPTURE FLOW: deep spec for `tools/primer_capture.py`

## Citation convention and standing conditions

**Citation keys.** The evidence ships without line numbers, so every citation is a quoted byte-run with "line UNVERIFIED".
- `MB` = `watch/inbox/hermes_burn/MOUNTAIN_build.md`
- `AV2` = `watch/inbox/ARENA_V2_DESIGN_20261004.md`

**Run state.** Nothing here has been run. `primer_capture.py` does not exist yet. The Roblox modules it feeds are also unlanded specs: MB says "Nothing in this pack has been run."

**Premise correction.** The CONTRACT says Primer v0 "named a webcam-captured physical page". The visible MB bytes show a different input path. The operator sends a typed code: "A player (the operator, in v0) sends a page code `Pnn-cc`." The MB evidence is truncated mid-Zone-4, so a webcam clause in the tail is **UNVERIFIED**.

**Design consequence.** The capture tool's only output is that same `Pnn-cc` string. It adds no new Roblox protocol and inherits the existing checksum, rate limit, and unlock chain unchanged.

**Deliverable.** One landable spec: `tools/primer_capture.py` plus its table file and one optional Luau bridge. Its falsifier is Part 6.

---

## 1. THE CAPTURE PIPELINE (`tools/primer_capture.py`)

### Dependencies

All three are **UNVERIFIED** as installed in the estate Python:
- Python 3
- `opencv-python`
- `numpy`

### Data types

```python
@dataclass(frozen=True)
class Frame:      bgr: np.ndarray; t_mono: float; t_utc: str; source_id: str
@dataclass(frozen=True)
class PageQuad:   corners: np.ndarray  # 4x2 float32, ordered TL,TR,BR,BL, portrait
                  rectified: np.ndarray  # 724x512 uint8 gray (H x W, A4 ratio 1.414)
@dataclass(frozen=True)
class Digest:     h0: int; h180: int; page_sha256: str  # sha256 of rectified raw bytes
@dataclass(frozen=True)
class Match:      row: dict; hamming: int; margin: int; rot: int  # rot in {0,180}
@dataclass(frozen=True)
class Reject:     reason: str; best: int | None; margin: int | None
```

### 1.1 `grab_frame(source: str | int, timeout_s: float = 2.0) -> Frame`

**Inputs.** `source` takes one of three forms:
- An `int` camera index, which uses `cv2.VideoCapture`.
- An image file path (still tier).
- A directory path (watch mode, newest file).

**Output.** One BGR frame with monotonic and UTC timestamps.

**Failure modes (raised, never swallowed):**

| Exception | Trigger |
|---|---|
| `NoDevice` | `VideoCapture.isOpened()` is false |
| `Timeout` | No frame within `timeout_s` |
| `BlankFrame` | Mean luminance < 8 or stddev < 4. This catches a lens cap or a dead sensor. |
| `FileUnreadable` | `cv2.imread` returns None |

- **Positive:** `grab_frame(0)` on a live webcam returns a 1280x720 frame.
- **Negative:** `grab_frame(0)` with the lens covered raises `BlankFrame`. It does not pass a black frame downstream, where it would later "match" nothing and look like a quiet success.

### 1.2 `detect_page(frame: Frame) -> PageQuad | Reject`

This function holds the geometric half of the tolerance mechanism.

**Steps:**
1. Convert to gray. Apply `GaussianBlur(5x5)`.
2. Run `Canny(50,150)` and `dilate(3x3, 1 iter)`.
3. Run `findContours(RETR_EXTERNAL)`.
4. For each contour, apply `approxPolyDP(eps = 0.02 * perimeter)`.
5. Keep convex 4-gons that pass every geometric tolerance:
   - Area >= 0.15 of the frame area (page fills enough of the view).
   - Every interior angle in [60, 120] degrees (tilt up to about 30 degrees survives).
   - Long/short side ratio in [1.15, 1.70] (A4 is 1.414, widened for perspective).
   - No corner within 4 px of the frame edge (page fully in view).
6. Take the largest survivor.
7. Order corners by the sum/diff method. If the quad is landscape, rotate the order 90 degrees so the page is portrait.
8. Run `warpPerspective` to 512x724 gray.

**Output.** `PageQuad` with ordered corners and the rectified image.

**Failure reasons:** `NoQuad`, `TooSmall`, `Skewed` (angle or ratio out of band), `Partial` (corner at the edge).

- **Positive:** a hand-held page tilted 20 degrees is rectified to an upright 512x724 image.
- **Negative:** the page is held so one corner leaves the frame. Result: `Reject("Partial")`, not a warped guess.

### 1.3 `digest(page: PageQuad) -> Digest | Reject`

This function holds the photometric half of the tolerance mechanism.

**Steps:**
1. Crop the inner 80% of the rectified image. This drops margins and the holding thumb.
2. Apply `equalizeHist`, which absorbs lighting and gamma.
3. Resize with `INTER_AREA` to 9x8.
4. Compute dHash: bit `i = px[r][c] > px[r][c+1]`, 64 bits row-major, stored big-endian as 16 hex chars.
5. Compute `h0` on the crop and `h180` on the crop rotated 180 degrees. This resolves upside-down presentation, the one ambiguity left after portrait ordering.
6. Set `page_sha256 = sha256(rectified.tobytes())`, the exact observation bytes, for the dice-law commit.

**Failure reason:** `LowContrast` when the post-crop stddev is < 10. This catches blank paper.

- **Positive:** the same drawn page under a desk lamp and under ceiling light gives digests within a few bits of each other.
- **Negative:** a blank sheet is rejected `LowContrast` before lookup, so it can never become a nearest-neighbor accident.

### 1.4 `lookup(d: Digest, table: list[dict], T: int = 8, M: int = 6) -> Match | Reject`

This function holds the decision half of the tolerance mechanism.

**Steps:**
1. For each row, compute the distance:
   `dist = min(popcount(d.h0 ^ row_digest), popcount(d.h180 ^ row_digest))`
2. Let `b` be the best distance and `s` the second best.
3. Accept iff `b <= T` and `(s - b) >= M`.

**Table invariant, checked at load.** The minimum pairwise row distance `D_min` (rotation-aware) must satisfy `D_min >= 2T + M` (22 at the defaults). Under that invariant, any frame within `T` of page A is at least `D_min - T` from every other page. Its margin is therefore `>= D_min - 2T >= M`. In other words, the invariant makes "ambiguous" impossible for a genuine page and confines errors to "too far".

**Failure reasons:**
- `TooFar` (`b > T`)
- `Ambiguous` (margin < M; should only fire on decoys)
- `EmptyTable`
- `InvariantBroken`, raised at load, never at query time

- **Positive:** P01 shown, `b = 3`, `s = 27`. Result: Match with margin 24.
- **Negative:** a decoy drawn with P01's border but a different glyph gives `b = 14`. Result: `Reject("TooFar")`.

### 1.5 `vote(history: deque[Match | Reject], k: int = 5, n: int = 7, cooldown_s: float = 2.0) -> str | None`

This function holds the temporal half of the tolerance mechanism.

**Rules:**
- Emit `page_id` when the same page wins `k` of the last `n` frames.
- After emitting, suppress that page until it has been absent (no accepted match) for `cooldown_s`.

**Rationale.** Holding a page up files one event, not thirty. A deliberate re-show files a second event, which matches MB's smoke: "Showing page 1 twice files 2 rows."

- **Positive:** 7 frames of P02 with one motion-blur `TooFar` give 6/7 and one emit.
- **Negative:** frames alternating P01/P02 never reach 5/7, so nothing is emitted.

### 1.6 `enroll(page_id: str, frames: list[Frame], max_spread: int = 4) -> str`

**Steps:**
1. Run `detect_page` and `digest` on 9 frames.
2. Take the bitwise majority of `h0` values to get the row digest.
3. Raise `EnrollUnstable` if any frame is more than `max_spread` bits from the majority.

The table is written only through this function. Digests are never typed by hand.

### 1.7 `commit_event(m: Match, d: Digest, votes: tuple[int,int], session: str) -> dict`

Builds the dice-law preimage (Part 4) using the adapter `read_tip() -> (tip_hex, index)`. The adapter is **UNVERIFIED**: AV2 names a "verkle tip" and a "party_subchain tip" but quotes no read API.

**Output:** the event dict plus `commit = sha256(preimage)`.

**Failure modes:**
- `TipUnavailable`: the event is journaled with `commit: null` and flagged. It is never committed against a stale tip.

### 1.8 `emit(event: dict, transport: str) -> str`

**Ordering.** The event is first appended to `watch/inbox/primer_capture/events.jsonl` (journal-before-send). The rectified PNG is saved alongside it as `<page_sha256>.png`.

**Transports:**
- `T0` (operator relay, default): prints `event["code"]` in large text on the capture host. The operator types it into the lectern.
- `T1` (relay): writes the code to an HTTP relay polled by `PrimerBridge.luau` (Part 3).

**Failure modes:**
- `TransportDown`: the event stays in the journal with `sent: false`. The next run's drain step retries. Events are never dropped silently.

---

## 2. THE MAPPING TABLE FORMAT

### File and format

- **File:** `tools/primer_capture_table.jsonl`, one row per page.
- **Loader checks, all fatal:**
  1. Schema validity.
  2. `D_min >= 2T+M`.
  3. Every `code` occurs verbatim in the bytes of `roblox/src/shared/PrimerPages.luau`. That file is an MB-specified path, so the check is grep-able once it lands.

### Schema

| field | type | rule |
|---|---|---|
| `page_id` | str | `^P\d\d$` |
| `code` | str | Copied verbatim from `PrimerPages.luau`. The checksum algorithm `cc` is **UNVERIFIED** (not in the visible MB bytes), so the tool never computes it. |
| `digest_hex` | str | 16 hex chars. Written only by `enroll()`. |
| `enroll_n`, `enroll_spread` | int | Receipt of enrollment quality. |
| `region` | str or null | CathedralMap region key. |
| `coord_ref` | str | How the world coordinate is derived. This is the authority. |
| `coord_pinned` | [x,y,z] or null | Cache only. The smoke recomputes it from `coord_ref` and fails on a mismatch above 1e-6. It stays null until a recompute fills it, because MB says "the page table never stores eigen numbers (no second truth)". |
| `zone` | str or null | Zone module name. |
| `unlock_attr` | str or null | Mirrors MB's "`PrimerUnlock_<ZoneModuleName> = true`". |
| `payload_ptr` | str | `roblox/src/shared/PrimerPages.luau#<page_id>`. The Luau entry is the unlock payload. This table only points to it. |

### Coordinate facts available today

- **The one measured coordinate.** The plate entry is `(-258.6, 8.0, 387.2)` (MB, citing FINAL). Conditions: instrument `tools/eigenmap_two_smoke.py`, moment final run 2026-09-27, context headless stub env under `tools/bin/luau/luau.exe`.
- **Lectern (derived).** MB says "A lectern stands 8 studs south (+Z) of `CathedralPlate.entry()`". Therefore lectern = `(-258.6, 8.0, 395.2)`.
- **Water (bounded, not measured).** MB says the stair runs "along the line `entry -> toWorld(water)`" and "slab Z strictly decreases with k". Therefore water's world Z < 387.2.
- **Fractal (relative only).** MB says fractal "is the southmost region (max ey), so it sits at +Z". Therefore fractal Z > water Z. Absolute numbers are **UNVERIFIED**.

### Worked rows

```jsonl
{"page_id":"P00","code":"<verbatim from PrimerPages.luau>","digest_hex":"<enroll()>","enroll_n":9,"enroll_spread":null,"region":null,"coord_ref":"CathedralPlate.entry() + (0,0,8)","coord_pinned":[-258.6,8.0,395.2],"zone":null,"unlock_attr":null,"payload_ptr":"roblox/src/shared/PrimerPages.luau#P00"}
{"page_id":"P01","code":"<verbatim from PrimerPages.luau>","digest_hex":"<enroll()>","enroll_n":9,"enroll_spread":null,"region":"water","coord_ref":"CathedralMap.toWorld(water centroid) + (0,12,0)","coord_pinned":null,"zone":"TideStairZone","unlock_attr":"PrimerUnlock_TideStairZone","payload_ptr":"roblox/src/shared/PrimerPages.luau#P01"}
{"page_id":"P02","code":"<verbatim from PrimerPages.luau>","digest_hex":"<enroll()>","enroll_n":9,"enroll_spread":null,"region":"fractal","coord_ref":"CathedralMap.toWorld(fractal centroid) + (0,12,0)","coord_pinned":null,"zone":"FractalDescentZone","unlock_attr":"PrimerUnlock_FractalDescentZone","payload_ptr":"roblox/src/shared/PrimerPages.luau#P02"}
```

**Row-by-row grounding:**
- **P00.** MB: "draws `CathedralMap.pairwise()` as a billboard and unlocks nothing". The billboard location is not in MB. Anchoring it at the lectern is this spec's choice, marked as such. The coordinate is derived from the one measured point.
- **P01.** MB: "`P01-xx` valid -> marker at the water centroid, row filed, `PrimerUnlock_TideStairZone` set". The +12 offset comes from MB: "Spawn a marker Part 12 studs above that coordinate". `coord_pinned` stays null until a recompute; the known bound is Z < 387.2.
- **P02.** MB: "Depths 4-5 require `PrimerUnlock_FractalDescentZone` (page P02)". `coord_pinned` stays null.
- **Placeholders.** Digest and code placeholders are deliberate. A hex value written before enrollment would be a fabrication.

**Negative row (loader must reject):** `{"page_id":"P01","code":"P01-00",...}` hand-typed with a guessed checksum. Result: a fatal "code not found in PrimerPages.luau bytes" error.

---

## 3. THE IN-WORLD UNLOCK

### Signal path for page N

```
[capture host]
grab_frame -> detect_page -> digest -> lookup -> vote -> commit_event -> emit
        |                                                   |
        |                                    events.jsonl (journal first)
        v
  code "Pnn-cc"
        |
   T0: operator types code at lectern TextBox
        -> RemoteEvent PrimerShow            (created by ScriptoriumZone.build())
   T1: PrimerBridge.luau polls relay (HttpService)
        -> calls ScriptoriumZone.show(operatorPlayer, code) server-side
        |
        v
[roblox/src/server/ScriptoriumZone.luau] show(player, code)
   1 validate vs roblox/src/shared/PrimerPages.luau  (checksum, page, lockout)
   2 region key (or KSpace.nearest for @walker pages)
   3 roblox/src/shared/CathedralMap.luau  toWorld(region centroid)
   4 marker Part +12 studs, BillboardGui caption        <- the visible render
   5 deps.file(player, "primer_page", {page, region, walker eigen, dist, bearing})
        -> roblox/src/server/ShadowLedger.luau row
   6 player:SetAttribute("PrimerUnlock_<Zone>", true)
        |
        v
[roblox/src/server/TideStairZone.luau]  slabs 6-9 onStep: attribute -> allowed
[roblox/src/server/FractalDescentZone.luau]  depths 4-5: attribute -> allowed
[roblox/src/server/CathedralPlate.luau]  entry() anchors the lectern (+Z 8)
```

**Sources for each step:**
- Steps 1 to 6 come from MB's six-step list under "`show(player, code)` does the following".
- "Slabs 6-9 require `PrimerUnlock_TideStairZone` (page P01)" comes from MB.
- The module paths come from MB: "`roblox/src/shared/CathedralMap.luau`, `roblox/src/server/CathedralPlate.luau`".

### What CathedralPlate actually renders

Honest scoping of the "CathedralPlate render" step:
- The evidenced CathedralPlate surface is only `build()` and `entry()` (MB). The marker for page N is spawned by ScriptoriumZone in plate world coordinates, not by a CathedralPlate function.
- Parenting the marker under the plate's model is **UNVERIFIED**, because the plate's model name is not quoted.
- No HUD change is specified. Whether `CathedralMapHud.client.luau` reacts to the attribute is **UNVERIFIED**, and this spec adds nothing there.

### What appears per page

| Page | Visible in scene | Gameplay change |
|---|---|---|
| P00 | Pairwise billboard at the lectern | None |
| P01 | Marker 12 studs above the water centroid with caption | Tide Stair slabs 6-9 pass |
| P02 | Marker above the fractal centroid | Fractal Descent depths 4-5 open |

All unlocks are session-scoped. MB: "An unlock does not survive a rejoin; the page is shown again."

### `roblox/src/server/PrimerBridge.luau` (new, T1 only)

- **Polling.** `build(deps)` per MB's DI rule ("Every zone is `build(deps)`"). It polls `deps.relayUrl` every 2 s via `HttpService:GetAsync`.
- **Calls.** It calls `deps.Scriptorium.show(deps.operatorPlayer(), code)`.
- **Trust surface.** It never touches the RemoteEvent, so it adds no client-spoof path. MB's lockout ("5 bad codes inside 10 s locks that player out for 30 s") still applies, because the call goes through `show`.

**UNVERIFIED items for T1:**
- That `show` is exported as a module function. MB specs it but has not landed it.
- HttpService reachability of a localhost relay, in both Studio and live servers. A live server needs a publicly reachable relay.

**Landing order.** `ScriptoriumZone` and `PrimerPages` must land first. T0 then works with zero Luau changes, which is why T0 is the default.

- **Positive:** P01 shown, T0 code entered, marker appears, slab 6 allows.
- **Negative:** the capture tool emits nothing, because the decoy was rejected. The operator types the decoy's guess anyway, the bad checksum is rejected by `show`, and there is no marker, no row, and no attribute.

---

## 4. THE DICE-LAW CLAUSE

AV2 trait 1: "DICE LAW (carrier-owned, chain-tipped, golden-vector pinned)". The arena's actual roll preimage bytes are not in evidence (**UNVERIFIED**). This format is self-contained. If the arena format is later found and differs in separators or field order, align this one to it and re-pin the golden vector.

**Carrier.** The capture host owns the commit, mirroring the arena carrier owning the dice. The "roll" is the observation: exact rectified bytes plus the digest.

### Preimage

UTF-8, LF line endings, fixed field order, no trailing whitespace, a final LF after `ts`:

```
primer-page-v1
tip=<64 lowercase hex, chain tip at commit time>
index=<chain index, decimal, no leading zeros>
page=<Pnn>
code=<Pnn-cc verbatim from table>
digest=<16 lowercase hex, h0 of this observation>
rot=<0|180>
hamming=<int>
margin=<int>
votes=<k>/<n>
page_sha256=<64 lowercase hex, sha256 of rectified 512x724 raw bytes>
table_sha256=<64 lowercase hex, sha256 of primer_capture_table.jsonl bytes>
session=<session id>
ts=<UTC, YYYY-MM-DDTHH:MM:SSZ>
```

`commit = sha256(preimage).hexdigest()`

### Why each binding field exists

- **`tip`** proves the event happened after that chain state.
- **`page_sha256`** plus the saved PNG let a cold seat run `digest()` on the PNG and recompute `hamming` against `table_sha256`'s row. The verdict is replayable, not reported.
- **`table_sha256`** pins which tolerance table judged the observation.

### Golden vector

- **Fixture:** `tip = "0"*64`, `index = 0`, all other fields fixed literals in `tools/primer_capture_golden.json`.
- **Pinning.** The expected hex is generated by the landing seat and pinned. It is not given here, because a hash written without running the hash would be fabricated.
- **Smoke:** recompute with `hashlib` and assert equality. Mutate any one byte (for example `votes=5/7` to `votes=6/7`) and assert inequality.

**Negative:** committing with the tip read at enrollment time instead of commit time. This is caught because `commit_event` calls `read_tip()` per event, and the smoke asserts two events across a tip advance carry different `tip=` lines.

---

## 5. THE HARDWARE HONESTY

| Need | Status | Fallback |
|---|---|---|
| USB webcam on the capture host | **UNVERIFIED** (no evidence byte mentions a camera) | Still tier: `grab_frame(path)` |
| Any still camera (phone) | **UNVERIFIED** | Synthetic tier (below) |
| Printer | **UNVERIFIED** | Hand-drawn pages, thick marker, one large distinct glyph per page |
| `opencv-python`, `numpy` | **UNVERIFIED** installed | `pip install` (software, no purchase) |
| Steady lighting | **UNVERIFIED** | `equalizeHist` plus a lamp/no-lamp test |
| Public HTTP relay for T1 | **UNVERIFIED** | T0 operator relay needs none |
| Webcam price | **UNVERIFIED** (no price evidence) | None |

### Cheapest experiment that justifies buying a webcam

Run the still tier offline, with no purchase:

1. Hand-draw P00, P01, P02 and one decoy (P01's border with a different glyph).
2. Take 10 photos of each with whatever camera exists. Vary tilt 0 to 30 degrees, lamp on/off, and a thumb on one corner.
3. Take 10 photos of negatives: blank sheet, hand, magazine page, decoy.
4. Run `detect_page -> digest -> lookup` over the folder.

**Buy decision:**
- **Buy** if there is zero cross-page mis-ID, zero accepted negatives, and >= 9/10 accepted per page. The live tier only adds motion blur and latency, and `vote()` exists for those.
- **Do not buy** if the still tier fails. A webcam will not fix it.

**If no camera exists at all.** Run the synthetic tier:
- Render the pages to PNG.
- Apply a random homography (tilt up to 30 degrees), Gaussian blur sigma 0 to 2, gamma 0.6 to 1.6, JPEG quality 40 to 90, and noise sigma 0 to 8.
- Use 200 samples per page.

This tests only the tolerance arithmetic, not optics. A pass justifies borrowing or buying a camera. A fail kills the dHash design before any spend, and the replacement is printed fiducials.

---

## 6. THE FALSIFIER

**Script:** `tools/primer_capture_falsifier.py`, run in one sitting. The tier is set by today's hardware: live if a webcam exists, still if only a phone, synthetic if neither.

### Protocol

1. **Enroll.** Enroll P00, P01, P02 with 9 frames each via `enroll()`. Assert `enroll_spread <= 4`.
2. **Separation check.** Check `D_min >= 22`.
   - If the check fails, redraw the offending page. Three failed redraws kill dHash for this purpose; switch to fiducials.
3. **Positive shows.** 20 shows per page with varied tilt, distance, lighting, and a corner thumb.
4. **Negative shows.** 20 total: 5 decoy, 5 blank, 5 hand, 5 magazine.
5. **Per-show log:**
   - Emitted or not.
   - Which page.
   - Latency from page-in-view to journal write (live tier only; operator keypress marks page-in-view).
   - `commit` hex.
6. **Cold replay.** For 5 random events, a second process recomputes `digest()` from the saved PNG and `commit` from the preimage, and both must match the journal.
7. **End-to-end (only if ScriptoriumZone and TideStairZone have landed).** One P01 emit is entered via T0 in Studio. The marker must appear and slab 6 must allow. Otherwise the Luau half rests on MB's `wave2_scriptorium_smoke.luau` 8/8 and is reported as not exercised.

### Verdicts

**PROVES** only if all of the following hold:
- 0/60 cross-page mis-IDs.
- 0/20 negatives emitted.
- >= 18/20 accepted per page.
- Live-tier median latency <= 2.0 s.
- 5/5 cold replays match.

**KILLS** on any of the following:
- Any cross-page mis-ID. P01 shown emitting P02 corrupts unlocks, so this is not tunable.
- Any emitted negative.
- < 14/20 on any page after one retune of `T`/`M` within `D_min >= 2T+M`.
- Any cold-replay mismatch.

**RETUNE ONCE** for 14 to 17 out of 20. A second miss in that band kills.

### Receipt

Written to `watch/inbox/primer_capture/falsifier-<UTC>.txt`. It must name its conditions:
- **Instrument:** camera model and resolution/fps, or the still/synthetic tier.
- **Software:** OpenCV and Python versions, plus `T`, `M`, `k`, `n`.
- **Moment:** UTC start and end, plus the chain tip and index at start.
- **Context:** lighting description, page set `table_sha256`, and transport.

It closes with `VERDICT: PROVES | KILLS | RETUNE` and the failure counts, in the style of MB's "`VERDICT: PASS (0 failure(s))`".

### Falsifier of this spec

This spec is wrong if either of the following happens:
- A genuine page passes `lookup()` but is rejected `Ambiguous`. The `D_min >= 2T+M` invariant proves that cannot happen for a correct implementation, so seeing it means the implementation or the invariant is broken.
- The still tier passes while the live tier on the same pages fails cross-ID. That would mean `vote()` is not the right temporal tolerance.
