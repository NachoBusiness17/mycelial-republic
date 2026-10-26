# THE MOCAP BUILD SPEC - NUANCE PASS (2026-10-04, flash rail)

Provenance: replay of `memory/plans/hermes_burn_playground_20261003/MOCAP_BUILD_spec/ask.json`.
Evidence read in full this session: `watch/inbox/mocap_pipeline_spec_20261004.md`,
`roblox/src/server/AbilitySlots.luau`, `roblox/src/client/init.client.luau`,
`configs/kabuki_cast.json`, `tools/dungeon.py`,
`watch/inbox/dd_dogfood/games-audit.md`,
`watch/inbox/replay_deepseek_thinking/MOCAP_BUILD_spec.md`.

Disclosure the contract needs first: the broad-strokes draft at
`watch/inbox/replay_deepseek_thinking/MOCAP_BUILD_spec.md` is 0 bytes
(`wc -c` = 0, mtime 2026-10-04 06:50). There is no draft text to deepen or
correct. The standing broad-strokes surface is the flash seat's own filing,
`watch/inbox/mocap_pipeline_spec_20261004.md`; this nuance pass cites that
file as "the flash spec" and corrects it where it waves. Nothing is copied
from either.

Grounding law: every file:line below was opened this session. Every number
is (a) quoted from an evidence file, (b) arithmetic shown inline, or (c)
tagged UNVERIFIED. No em-dashes.

---

## 0. GREENFIELD CENSUS (what does not exist, byte-checked)

- `tools/mocap_capture.py` does not exist (ls exit 2). This spec authors it.
- Zero animation infrastructure in the roblox tree: grep for
  Animation/Animator/AnimationTrack/Motor6D over `roblox/src/` returns
  nothing. `roblox/src/shared/ProceduralBody.luau:1-10` is DF wisp creature
  assembly (blocky primitives welded to a core ball), not a humanoid rig.
  R15 rig bootstrapping is in scope and spec'd at 1.5.
- The four dance faces (Ilse, Greta, Pell, Oswin) exist only in the flash
  spec (`watch/inbox/mocap_pipeline_spec_20261004.md:30-34`). They are not
  in the Mountain's head registry (`roblox/src/shared/Lore.luau:117-123`:
  elder, bard, economist, builder, research, ghost, janitor) and not in the
  kabuki cast (`configs/kabuki_cast.json:7`: ARAGOTO, WAKA, ONSEI,
  TACHIYAKU, ONNAGATA, HANA-GUMO). The grep hit on "Pell" in
  `mag/fermat_ractor.py:156` is the Pell equation (number theory), not a
  face; do not cite it as one.
- `roblox/default.project.json` carries no animation assets (grep anim: 0).

---

## 1. THE PIPELINE SPEC: tools/mocap_capture.py, function by function

Module contract: stdlib-only (json, subprocess, hashlib, math, pathlib,
argparse) so it runs under the repo venv and the sandbox venv alike, and so
tests collect into the census cleanly (4,156 collected / 497 files,
2026-10-02 census carrier, AGENTS.md). Quaternion math is local (~40 lines:
mul, conj, normalize, slerp). CLI:
`python tools/mocap_capture.py <stage> --clip <path> --sandbox <dir>
[--blender <exe>]`. One stage per invocation; every stage writes a JSON
receipt next to its output.

### 1.1 ingest_video

```
def ingest_video(src: Path, work: Path) -> dict
```
Inputs: source clip path. Outputs: `work/ingest.json` {path, sha256, width,
height, fps, duration_s, nframes}. Mechanism: ffprobe
(`ffprobe -v error -select_streams v:0 -show_entries
stream=width,height,r_frame_rate,duration -of json <clip>`); ffprobe
presence on this Windows host UNVERIFIED (sandbox G1 installs it).
Failure modes: ffprobe missing (exit 127 -> raise with install pointer);
clip unreadable/0 frames; fps parse "30000/1001" fractional form (parse the
ratio, do not float-truncate); duration under 1.0s (too short for a loop);
sha256 mismatch on re-run (source mutated, refuse).
Verifies before returning: json parses, all six keys present and positive,
sha256 recorded. Return value is the receipt dict, reused by every later
stage's receipt.

### 1.2 run_blendcap

```
def run_blendcap(clip: Path, out: Path, blender: Path,
                 timeout_s: int = 1800) -> dict
```
Inputs: clip, output tracks path, Blender executable path, timeout.
Outputs: `out/tracks.json` + `work/blendcap.log`. Subprocess contract (real
Blender flags, one line):

```
blender --background --factory-startup --python blendcap_driver.py -- --in <clip> --out <tracks.json>
```

`--background` is headless; `--factory-startup` ignores the user profile
(deterministic runs); `--python <script>` names the driver; everything after
`--` goes to the driver via sys.argv. The driver enables the addon itself
(`bpy.ops.preferences.addon_enable(module=<blendcap module id>)`), then
drives its extraction API. UNVERIFIED until sandbox G2: BlendCap's module
id, operator names, whether its tracker needs a GPU/EGL context that
`--background` does not provide (mitigation if so: a 1x1 offscreen window
driver pattern), and the output schema it actually emits (this spec's
`{fps, frames, joints: {name: [{t, pos[3], quat[4]}]}}` is the target
schema; the driver adapts BlendCap's real output to it, and the adapter is
the only BlendCap-specific code in the tree).
Failure modes: returncode != 0 (Blender crash or addon error; log tail goes
into the receipt); timeout (subprocess.run timeout, kill and fail - no
retry loop, a hung tracker is a sandbox problem, not a transient);
tracks.json missing or unparsable; frame count outside 5% of
duration x fps (tracker dropped the tail); nondeterminism probe: same clip
twice must hash equal after canonicalization (sorted keys, rounded to 6
decimals); if it does not, bank the delta and pin the second run's output.
Verifies before returning: file exists, parses, fps matches ingest.json
within rounding, every joint list is non-empty.

### 1.3 extract_tracks

```
def extract_tracks(tracks_json: Path) -> list[JointTrack]
```
JointTrack = {name, fps, nframes, pos: list[[x,y,z]], quat:
list[[w,x,y,z]]}. Inputs: BlendCap output. Outputs: normalized in-memory
tracks + `work/extract.json` receipt. Failure modes: quaternion norm outside
1-1e-3 (renormalize; outside 1-1e-2, fail - the tracker is broken, not
imprecise); duplicate timestamps (resample grid in 1.4 fixes); joints that
disappear mid-clip (gap-marked, never interpolated across a gap > 5
frames - a vanished wrist is a tracking failure to log, not data to
invent); source skeleton naming unknown (fail with the observed names so
the mapping table in 1.5 gets the new alias added deliberately).
Verifies before returning: every quat normalized, every track contiguous
modulo marked gaps, joint set matches the mapping table's source column.

### 1.4 clean_tracks

```
def clean_tracks(tracks: list[JointTrack], noise_deg: float = 0.5,
                 snap_deg_s: float = 45.0, fps_target: int = 30) -> list[JointTrack]
```
Inputs: raw tracks + style parameters. Outputs: cleaned, resampled tracks +
`work/clean.json` with before/after jitter metrics. Mechanism, two passes:
(1) resample every track onto a fixed 1/fps_target grid by quaternion slerp
and position lerp (Roblox keyframe snapping is conventionally 1/30s,
UNVERIFIED, confirmed at G6); (2) noise-gated smoothing: a frame is noise
when its angular delta from the previous frame is under noise_deg AND local
angular acceleration alternates sign; noise frames get a window-3 moving
average; any frame whose angular velocity exceeds snap_deg_s is preserved
byte-exact (the chain-punch snap is the move; smoothing it kills it).
Failure modes: over-smoothing a stillness style (Oswin's real motion lives
near the noise floor - his style pass lowers noise_deg to 0.2 and disables
snap preservation, and its receipt must show jitter retained, not removed);
smoothing across a marked gap (forbidden, pass 2 skips gap frames); resample
drift (grid length must equal round(duration x fps_target), asserted).
Verifies before returning: no NaN/inf, track lengths match the grid, jitter
metric computed and banked in the receipt.

### 1.5 retarget_r15

```
def retarget_r15(tracks: list[JointTrack]) -> dict[str, list[tuple[int, float, float, float, float]]]
```
Output: per-R15-joint rotation keyframe lists (frame, qx, qy, qz, qw).

RIG BOOTSTRAP (greenfield, the part the flash spec waves at). Roblox R15 is
15 parts joined by Motor6Ds: Root (HumanoidRootPart-LowerTorso), Waist,
Neck, and per side Shoulder/Elbow/Wrist (upper arm, lower arm, hand off
UpperTorso) and Hip/Knee/Ankle (upper leg, lower leg, foot off LowerTorso).
The standard rig has NO finger joints and NO face joints: Head and each Hand
are single parts. Consequences stated plainly: (a) BlendCap hand data has no
R15 destination except the wrist joint - tan sau and bong sau read as
forearm rotations in v1, hand shapes are lost without custom meshes; (b)
the flash spec's facial-track ambition needs Roblox dynamic-head meshes and
is out of scope v1 (the flash spec's own honesty ledger already flags
facial FBX as UNVERIFIED, `watch/inbox/mocap_pipeline_spec_20261004.md:41-42`).

MAPPING TABLE (source column holds common capture-skeleton aliases;
BlendCap's real names UNVERIFIED, G2 aliases them in):

| source joints | R15 Motor6D | drives |
|---|---|---|
| hips, pelvis | Root, Waist | LowerTorso |
| spine, chest | Waist | UpperTorso |
| neck, head | Neck | Head |
| LeftArm/LeftShoulder, LeftForeArm, LeftHand | LeftShoulder, LeftElbow, LeftWrist | arm parts |
| RightArm/RightShoulder, RightForeArm, RightHand | RightShoulder, RightElbow, RightWrist | arm parts |
| LeftUpLeg, LeftLeg, LeftFoot | LeftHip, LeftKnee, LeftAnkle | leg parts |
| RightUpLeg, RightLeg, RightFoot | RightHip, RightKnee, RightAnkle | leg parts |

THE RETARGET TRANSFORM. For joint j, parent p(j), frame f, with quaternions
as world rotations from the cleaned tracks:

```
q_r15_local(f, j) = conj(q_src_world(f, p(j))) * M_j * q_src_world(f, j)
```

M_j is a constant per-joint correction computed ONCE from the two rest
skeletons: source rest pose (capture rigs are conventionally T-pose,
UNVERIFIED for BlendCap) to R15 rest pose (standard rig arms hang down).
M_j = q_r15_rest_world(j) * conj(q_src_rest_world(j)). The first clean
frame's pose determines q_src_rest_world; a T-vs-A-pose mismatch shows up
as a constant shoulder offset in Studio and is fixed by editing M_j, never
by bending the data. Exact R15 rest angles UNVERIFIED until G5 measures a
rig in Studio.

SCALE. Working constant: R15 character stands about 5 studs; Roblox metric
1 stud = 0.28 m, so the export rig is built 1.4 m tall in Blender
(5 x 0.28). UNVERIFIED until the G5 calibration clip lands next to a
5-stud wall in Studio. The key greenfield simplification: we ship ROTATION
tracks onto the stock R15 Motor6D joints. We never import skinned meshes,
so the skin-weight problem the flash spec gestures at does not exist in
v1: Roblox's own R15 meshes carry their weights. "Weights" reduce to M_j
correctness, verifiable by forward kinematics.

Failure modes: parent joint missing from the track set (fail, do not
assume identity); gimbal-flip stalls in the slerp (detect as > 180 deg/frame
jumps, resample with the short-arc slerp and re-check); FK round-trip outside
tolerance (see verify below).
Verifies before returning: forward-kinematics round-trip - apply the local
rotations down the R15 hierarchy and compare reconstructed world joint
positions to the source positions; mean error under 2% of rig height,
else fail with the per-joint error table. All-identity input must produce
the R15 rest pose (a static T-pose clip is the calibration fixture).

### 1.6 export_fbx

```
def export_fbx(poses: dict, out: Path, blender: Path) -> Path
```
Mechanism: a second headless Blender job builds a minimal armature (15
bones named for the R15 Motor6Ds, rest pose = R15 rest), bakes the
keyframes, exports `blender --background <setup.blend> --python
export_fbx.py -- --out <path>` with Blender's FBX exporter defaults
(bake_anim on, `bake_anim_use_nla_strips=False`). The .blend setup file is
generated once by the driver and checked into the sandbox, not the repo.
Failure modes: Blender FBX addon missing in --factory-startup (driver
enables `io_scene_fbx` explicitly); scale mismatch on import (verify in
Blender by re-importing and diffing bone count and a probe frame's
rotations within 0.01 rad); Studio-side import behavior (roblox .fbx to
Animation Editor, keyframe fidelity, units) UNVERIFIED - that check is the
human-eyes half of G6.
Verifies before returning: re-import round-trip in the same Blender equals
the baked track; file size non-trivial; header string "FBX" present.

Tests: `tests/test_mocap_capture.py` (new) - synthetic 2-joint fixture for
the quaternion math, the 1.5 mapping table as data, a rest-pose
round-trip case, noise-gate cases (snap preserved, jitter removed), and
ingest receipt schema. Stdlib-only keeps collection clean.

---

## 2. THE DOGFOOD MAP (organs, file:line; new organs carry reasons)

| organ | wires at | what it banks |
|---|---|---|
| chan board | `mag/chan.py:211` `post(slug, text, seat=...)` onto `watch/room.jsonl` (`mag/chan.py:21`) | one capture receipt per clip: sha256, stage receipts G1-G7, timing, failures. Thread slug "mocap" is NEW (primer threads are the tuple at `mag/chan.py:40`: keep, physics, water, energy, organism, congestion, primer-feed). Reason for new: capture receipts are watch-facing play content and room.jsonl is the durable watch surface; they are not primer doctrine and not inbox files (the inbox holds the spec, the board holds the play-by-play). |
| season ledger | `mag/gwap_payload.py:681-684` `SessionLedger` (append-only, verify-before-extend) | one chain row per AnimationTrack asset: {asset_id, clip_sha256, move, face, gates_passed, ts}. Banked via the `tools/arena_gwap.py:171` `bank()` pattern; the season save-row shape it extends is `watch/inbox/replay_flash/SEASON_design.md:87-101` (row_type season_state). A "mocap-capture" session file is NEW but reuses the verified-chain class unchanged; nothing new is invented except the row's fields. |
| kabuki cast | `configs/kabuki_cast.json:7` actors array | per-face movement vocabulary field (style, loop asset id, status). Note kept honest: these actors are Hermes salon seats, not Mountain rigs; the field is the styling registry so a salon face and its dance loop stay keyed in one file. |
| route_chat | `mag/route_chat.py:121` `route_chat(...)`, dispatcher `:163`, exception-path banking inside route_chat | any LLM-assisted retarget cleanup (alias resolution, gap reasonableness review) rides the mechanical depth lane; every call banks a row, including failures, per the everything-banks law the front door enforces. Pricing source: `tools/hermes_burn.py` PRICING, imported and applied in `tools/dungeon.py:38` and `tools/dungeon.py:219-224`. |
| gap register | `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:15` (amend, never rewrite) and `:26` (rank = severity x fill-ease) | pipeline failures that outlive the session: BlendCap price/offline claim, FBX facial-track support, latency measurement, R15 rest angles, keyframe snap behavior. |
| NPC head registry | `roblox/src/shared/Lore.luau:117-123` `Lore.Heads` + `tools/roblox_npc_gateway.py:125` `PERSONAS` | where the dance faces attach when they become rigs (see part 4); the gateway is the NPC=SEAT bridge (`roblox/src/server/NpcGateway.luau:3-7`). |
| dungeon carrier | `tools/dungeon.py:38` hermes_burn import, `tools/dungeon.py:222-224` `_bank` | the banking precedent this pipeline's receipts copy (id embeds a per-session tag, ok reflects real content, not API success). |

---

## 3. THE WING CHUN BINDING (exact wiring, ids, frame budget)

What exists (byte-read this session):

- Server truth: `roblox/src/server/AbilitySlots.luau:22` -
  `{ name = "WingChunRedirect", attribute = "Abil_Redirect", window = 1.5, cooldown = 8 }`.
  Validation and cooldown clock: `AbilitySlots.luau:32-54`; the Carrying
  gate `:39-41`; the attribute flip true then false after the window
  `:47-52`.
- Client input: `roblox/src/client/init.client.luau:41` - Redirect on C,
  fires server name "WingChunRedirect" inside the InputBegan loop
  `:339-344`; mobile touch spot `:386` bound `:389-393`.
- Attribute consumers (the parry is already mechanical): the roll in
  `roblox/src/server/zones_extra/FrontierSoulsZone.luau:127`, the roll in
  `roblox/src/server/zones_extra/ToyBoxZone.luau:135`, the boss read in
  `roblox/src/server/TheAnswerBoss.luau:117`.
- Config anchor: `roblox/src/shared/Config.luau:69-76` Controls block
  already maps `C = "WingChunRedirect"` (`:73`); modules require path is
  `ReplicatedStorage.Modules` (`roblox/src/server/NpcGateway.luau:10-11`).

What gets added (v1, three seams, no new surface):

1. `roblox/src/shared/Config.luau:77` (just before `return Config` at
   `:78`): `Config.Animations = { redirect = "rbxassetid://<id>",
   dance = { ilse = ..., greta = ..., pell = ..., oswin = ... } }`. Asset
   ids UNVERIFIED until the first track uploads.
2. `roblox/src/client/init.client.luau`, new block patterned on the chip
   clock's attribute hook `:101-107`: on
   `player:GetAttributeChangedSignal("Abil_Redirect")` true, play the
   redirect track on the local character's Animator (`charHum()` helper
   already at `:296-299` for the Humanoid; Animator via
   humanoid:FindFirstChildOfClass("Animator")), track loaded once per
   character and cached, `track:Play(0.05)`,
   `track.Priority = Enum.AnimationPriority.Action`, clip trimmed to
   1.4s so it lands inside the 1.5s window (`AbilitySlots.luau:22`).
3. Nothing changes in AbilitySlots: it is server validation, and the
   animation is a client look. The flash spec's step 4 implies the
   animation rides existing wiring; correction: the wiring that reads the
   attribute for visuals exists only for the chips; the animation hook is
   new client code in the courier's own file, which is where looks live.

INPUT-TO-LATENCY BUDGET, in frames at 60 fps (1 frame = 16.7 ms):

| leg | frames | basis |
|---|---|---|
| InputBegan dispatch | 0-1 | same-frame input handling, bounded 1 |
| FireServer uplink | RTT/2 | Roblox replication, RTT UNVERIFIED on target hardware |
| server handler `:33-53` | 0-1 | sub-ms os.clock + attribute set, same heartbeat |
| attribute replication down | RTT/2 | same RTT |
| AttributeChangedSignal -> Play -> next RenderStepped | 1-2 | init.client hook pattern `:101-107` |

Honest arithmetic the flash spec skipped: with the attribute-flip trigger,
at a 100 ms RTT the budget reads 1 + 3 + 1 + 3 + 2 = ~10 frames = ~167 ms,
which is perceptible and fails the falsifier. Mitigation ladder, in order:
(1) playtest on low-RTT Studio/local play first (at 25 ms RTT: ~6 frames,
~100 ms, borderline); (2) if it reads late, switch the trigger to
optimistic local play inside the InputBegan branch `:339-344` (0-1 frames,
~16-33 ms) with the server attribute remaining the truth that cancels the
play if the fire is refused - the chip clock stays attribute-driven
(`:100-107`) and the server keeps every ounce of validation, so the
courier law (`init.client.luau:16-17`) is intact: prediction is a look,
not a verdict. The measured number, whatever it is, banks in the chan
receipt.

---

## 4. THE DANCE LIBRARY (capture manifest, sources, binding)

The four vocabularies from the flash spec `:30-34`, made concrete. The
faces are NEW relative to every registry (section 0); written reason: the
flash spec names them as the Mountain's cast, and the Mountain's head
registry `Lore.Heads` is the only in-world persona surface, so landing them
means four new Lore.Heads rows + four PERSONAS entries
(`roblox/src/shared/Lore.luau:117-123`,
`tools/roblox_npc_gateway.py:125`) plus placed rigs. v1 ships the motion
library first (AnimationTrack assets) and the rig landing second; a
vocabulary nobody can play is still banked work.

| face | style | capture protocol | idle/emote binding |
|---|---|---|---|
| Ilse | waltz glide (box step + travel, upright frame) | 16-24s loop, static camera at chest height, full body in frame, plain wall; 2 takes minimum | idle_loop = the glide at 0.5 speed, Looped; emote_one = a single full box step |
| Greta | military march (high knees, stamp, fixed cadence) | 12-16s loop, metronome at 100 bpm in the room (audio discarded, cadence kept); 2 takes | idle_loop = attention-still with weight shifts; emote_one = 8-count march in place |
| Pell | loose bounce (capoeira-adjacent ginga) | 12-20s loop; the bounce never stops - cleaning pass must preserve the 2-4 Hz rhythm as signal, not noise; 3 takes (rhythm drift is the failure mode) | idle_loop = ginga, Looped; emote_one = one esquisa lateral |
| Oswin | stillness (slow tai chi frame) | 20-30s loop, near-static; style params per 1.4 (noise_deg 0.2, snap preservation off); the receipt must show jitter RETAINED | idle_loop = the slow frame itself; emote_one = one cloud-hands cycle |

Sources: estate-owned recordings preferred; open-licensed (CC0/CC-BY)
otherwise; nothing scraped (flash spec `:42-44`). No specific source clips
are selected yet: every source line is UNVERIFIED until a clip with its URL
or provenance note rides the capture receipt. The operator's own phone
recording of the operator performing the Wing Chun drill is estate-owned by
construction and is the sanctioned first source.

Kabuki binding: `configs/kabuki_cast.json` actors gain a `movement` object
{style, loop_asset_id, status}. Reason this file and not a new one: it is
the only per-persona registry in the estate keyed by stage name, and the
contract names the kabuki cast as the carrier. The Mountain-side playback
for placed NPC rigs: one shared server script reads
`Config.Animations.dance`, loads per-face idle_loop through the rig's
Animator with `track.Looped = true`, swaps to emote_one on a
ProximityPrompt or a `MudBasecamp.say` event (the chat remote already
exists at `roblox/src/client/init.client.luau:30`). Player-character dance
emotes via the Roblox emote system are a follow-on, not v1.

---

## 5. THE SANDBOX PLAN

Location: `C:\Users\foste\Documents\projects\mocap_sandbox\` - a sibling of
the repo, outside the key tree entirely. Layout: `blender/` (portable zip
unzip), `venv/` (its own `python -m venv`; Blender bundles its own Python,
the venv is for ffprobe-adjacent tooling and the driver's stdlib needs),
`blendcap/` (the addon), `clips/` (estate-owned sources), `out/` (stage
outputs + logs). The repo touches the sandbox only through
`tools/mocap_capture.py --sandbox <dir> --blender <exe>` arguments: no
Blender path is ever hardcoded in the repo, and the Mag venv never learns
about Blender.

Verification loop (each gate proves before the next is built; a failed gate
banks its receipt to the chan board and, if the failure outlives the
session, a row in the gap register):

- G1 ingest: ffprobe reads a 10s probe clip; receipt complete. Builds 1.1.
- G2 blendcap: headless driver extracts the probe clip; schema adapter
  emits the target tracks.json; determinism probe passes; TIMING BANKED
  (the cost model's compute line). Builds 1.2/1.3. Blocked until the
  BlendCap price is an operator fact (see part 6).
- G3 extract + clean: jitter metrics before/after banked; snap frames
  preserved on the punch fixture. Builds 1.4.
- G4 retarget: FK round-trip under 2% on the probe clip; rest-pose
  calibration clip (static T-pose) validates M_j. Builds 1.5.
- G5 export: Blender round-trip re-import byte-consistent. Builds 1.6.
- G6 Studio: human-eyes import via the Animation Editor; scale checked
  against a 5-stud wall; keyframe snap confirmed. First operator call.
- G7 bind: the real falsifier, part 6.

First capture: one redirect drill (bong sau deflect) from an estate-owned
clip, walked G1-G7 to one AnimationTrack on the Mountain's redirect input.

---

## 6. THE COST MODEL + FALSIFIER

| line | value | source/status |
|---|---|---|
| Blender | $0 | confirmed, flash spec `:38` |
| BlendCap license | PRICE UNVERIFIED | flagged per contract; flash spec `:39-40` names the listing and the unverified offline claim. G2 is blocked until the operator prices it. Placeholder budget $0-50 is a design placeholder, not evidence. |
| Compute | 10 min/clip working number, UNVERIFIED | flash spec `:45` claims CPU/GPU minutes, not hours; G2 banks the real number |
| Clip census | 11 minimum | 5 Wing Chun moves (flash spec `:21-25`: tan sau entry, bong sau deflect, gaan sau sweep, chain punches, chi geuk stepping) + 4 dance loops (part 4) + 1 rest-pose calibration + 1 redirect falsifier clip |
| LLM cleanup | capped $1.00 per full set | design choice; priced through tools/hermes_burn.py PRICING (`tools/dungeon.py:38`, `:219-224`), routed through `mag/route_chat.py:121`, mechanical depth only |
| Seat time | 30-60 min/clip | estimate, named as an estimate; the honest dominant cost |

THE FALSIFIER (flash spec `:47-54`, sharpened): one captured redirect
AnimationTrack bound to the C key plays in-Studio. Pass requires all
three: (a) the input fires and the track plays (wiring part 3);
(b) an operator watching at 3 m reads it as a deflection, not a twitch;
(c) measured latency is imperceptible: record the playtest at 60 fps, count
frames between the keypress cue (the chip glow flipping on,
`roblox/src/client/init.client.luau:125-128`, is the visible keypress
marker) and the first motion frame; 6 frames (100 ms) or fewer passes,
7+ fails and triggers the mitigation ladder in part 3 before any verdict.
If the track cannot bind to the existing wiring, or latency stays
perceptible after mitigation, the pipeline dies and hand-keyed frames win
(Roblox Animation Editor: slower, still real, per flash spec `:52-54`).
That kill is real: the fallback needs no sandbox, no addon, and no
unverified license, so the pipeline must beat it on reads, not on
existence.

---

## 7. COMPLIANCE

Spec-before-behavior: this document is the spec; no code exists to orphan.
Fix comments carry receipts: every UNVERIFIED above names its gate. No
timeouts papering over sync problems: 1.2's timeout kills, it does not
retry. Pre-push gates apply when code lands: violation ratchet
(`tools/violation_ratchet.py`) over tools/, citation lint over this file's
citations (every file:line opened this session). The broad-strokes draft is
cited as demanded and is empty; this pass therefore deepens the flash spec
(`watch/inbox/mocap_pipeline_spec_20261004.md`) and corrects it in three
places: AbilitySlots carries no animation code (the look is new client
code), the attribute-round-trip latency math likely breaks the 100 ms
budget at live RTT (mitigation ladder spec'd), and facial/hand tracks have
no standard R15 destination (out of scope v1, stated not waved).
