# DOGFOOD — day tool on glass: AutoGLM pixel-guess vs AX-resolve (2026-09-04)

**CLAIM (steal card STEAL_ZAI_SYSTEMS_AUTOMATE):** AutoGLM-Phone — the vendor's embodied
brain — can drive the fleet's Android surface.

**FALSIFIER (single step of the 70-step ladder):** task = "tap the button labeled
'invariants'" on the DAY TOOL page (emulator-5554, WebView, 1080×2400).

## RESULTS

| arm | attempt | outcome |
|---|---|---|
| AutoGLM pixel-guess (vendor loop, brain only) | `Tap 155,716` | **FAILED** — true button center (166,1725); Δy = 1,009px (42% of screen height); tap landed in the digest text block |
| AX-resolve hybrid (our harness resolves, then taps) | tap (166,1725) → STEP ×70 (753,2030) | **PASSED** — 47 entries loaded, walk reached **pos 47/47** |

Brain cost: 3,495 prompt / 216 completion tokens, one call, autoglm-phone-multilingual on
the Lite key (Calcifer), $0 under vendor "free for a limited time". Receipts:
`watch/receipts/autoglm_before.png`, `autoglm_after.png`, `autoglm_brain_out.json`,
`ax_hybrid_after70_v2_20260904.png`.

## LAWS MINTED (failures logged as laws, not bugs)

1. **AX-RESOLVE OVER PIXEL-GUESS.** The WebView exposes the full accessibility tree with
   exact bounds and clickability ("invariants" Button at 28,1680–304,1769). The vision
   brain guessing coordinates missed by 1,009px; the tree was exact. Feed the brain
   RESOLVED targets (or skip the brain for taps entirely); never let it guess pixels.
   This is our computer-use seat's a11y-first doctrine, now MEASURED on the Android rig.
2. **NORMALIZE AT THE BOUNDARY.** The vendor returned `"Tap"` against a grammar that says
   `"tap"`. Harness normalizes verb case/aliases at the boundary; the lattice of actions
   stays canonical inside.
3. **ONE CANONICAL MIRROR SHAPE.** A raw `cp` of invariants.json (dict-of-dicts) collapsed
   47 invariants into ONE walkable entry (1/1 walked — silent wrong answer, not an error).
   `mag.lattice_logic export` is the only door into dashboard/static/lattices/: every
   mirror carries `{schema: lattice_logic.v1, entries: [...]}`.

## STATE

- The 70-step ladder is LIVE embodied: AX taps walk any mirrored lattice to its end
  (47-entry invariants walked; ×70 caps at lattice size — correct).
- mag/autoglm.py = brain half (mimosa-audited: pinned endpoint, public-IP check,
  no-redirect opener). mag/lattice_logic.py = the logic organ (list/query/walk/chain/export).
- chain() finding: ALL 8 law-registry conditions are prose ("executor_available") —
  zero machine-checkable rules exist; the logic tool fires NOTHING blind. LAW CANDIDATE:
  prose conditions are decorative to a machine.

## TRI-STATE
Pixel-fail/AX-pass: **Supported** (receipts above). AutoGLM pricing $0: **Supported**
(vendor "free for limited time", usage row shows no charge line — monitor).
Law generality beyond WebView surfaces: **Unproven** (native apps next).

*Filed by the zcode seat (Max), day-drive 09-04. Next rung: native-app target + the
full 70-step ladder with brain-in-the-loop decisions at branch points only.*
