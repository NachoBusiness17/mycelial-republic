# THE MOCAP PIPELINE - Wing Chun + dance styles for the Mountain (2026-10-04)

Operator order: "do this to our wing chun and lets grab some dance styles."
The enabling drop: BlendCap, a 100% local offline Blender add-on extracting
full-body, hand, and facial tracking from a single video (@unity3dvfx,
2026-10-03 - proven in-thread, no studio, no cloud).

## THE PIPELINE (video in, Roblox animation out)

1. SOURCE: estate-owned or open-licensed footage - Wing Chun forms (chain
   punches, tan/bong/gaan drills, the redirect), dance styles for the cast.
2. CAPTURE: Blender + BlendCap extracts skeletal tracks (body/hands/face).
3. RETARGET: Blender rig -> Roblox R15 rig mapping -> FBX/glTF export.
4. IMPORT: Roblox Animation Editor -> AnimationTrack assets -> the Mountain's
   AbilitySlots/WingChun redirect wiring plays them on hit/parry/emote.
5. BANK: every captured move receipts into the season ledger like a session.

## THE WING CHUN APPLICATION

The Mountain already wires the Wing Chun redirect input (roblox/src/client +
AbilitySlots). What's missing is the LOOK. Capture list: tan sau entry,
bong sau deflect (the redirect - the signature), gaan sau sweep, chain
punches (linsip keun), the stepping (chi geuk). Each becomes one
AnimationTrack bound to the redirect input - the deflection animation plays
exactly when the input reads a parry. The fidelity target: readable at
Roblox scale, not film-perfect.

## THE DANCE GRAB LIST (movement vocabulary for the cast)

The kabuki faces get signature movement: Ilse's glide (waltz frame - the
widow who flatters before she cuts), Greta's stance drill (military march
frame - the mercenary), Pell's loose bounce (capoeira-adjacent - the
cutpurse), Oswin's stillness (a slow tai chi frame - the friar). Sources:
open-licensed dance footage only; every capture receipts its source URL.

## THE HONESTY LEDGER

- Blender: free, confirmed.
- BlendCap: superhivemarket listing, price UNVERIFIED, offline claim UNVERIFIED
  until run sandboxed.
- Roblox FBX import via Animation Editor: supported, UNVERIFIED for facial
  tracks (Roblox has limited facial animation support - head mesh only).
- Source footage licensing: estate-owned recordings preferred; open-licensed
  otherwise; nothing scraped.
- Hardware: the capture is CPU/GPU minutes per clip, not hours.

## THE FALSIFIER

One Wing Chun redirect captured, retargeted, and played in-Studio on the
Mountain's redirect input - the input fires, the animation reads as a
deflection, and the input-to-animation latency is imperceptible. If the
animation cannot bind to the existing redirect wiring, the pipeline dies
and the fallback is Roblox's native animation editor with hand-keyed
frames (slower, still real).

Filed by the flash seat. The next sitting: install Blender + BlendCap in
the sandbox, capture one redirect drill from an estate-owned clip, and walk
the full pipeline to one AnimationTrack on the Mountain.
