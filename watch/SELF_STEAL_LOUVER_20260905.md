# SELF STEAL — THE LOUVER (Sep 5, 2026)

*Operator: "how do we use the AMD technology of only being able to see a screen from one
direction on a desktop — could we adapt that to our riddler stack? Self steal. So here's a
problem: that eye could see our secrets."*

## THE TECHNOLOGY, RECEIPTED
Two faces exist in the wild, both AMD-adjacent:
1. **Hardware angular keying** — micro/nanolouver films (Kensington, 3M, Dell) that pass a
   ~±30° viewing cone and darken every other angle; Lenovo's **electronic PrivacyGuard**
   panels on AMD ThinkPads make the louver SWITCHABLE at will.
   ([Kensington](https://www.kensington.com/news/security-blog/laptop-privacy-screens/),
   [Dell nanolouver](https://www.dell.com/en-us/shopping/laptop-privacy-screens),
   [Lenovo/AMD PrivacyGuard field reports](https://www.reddit.com/r/thinkpad/comments/xlqsub/this_is_the_privacy_guard_in_2022_x13_gen_3_amd/))
2. **Gaze-directed disclosure** — AMD **Privacy View**: eye-tracking software that keeps the
   screen bright ONLY where the user is looking and dims the rest. Disclosure scoped to the
   gaze, not to a static wall.
   ([AMD Privacy View](https://www.facebook.com/AMDRyzenRadeon/videos/amd-privacy-view-privacy-thats-spot-on/619566805710192/))

## THE SELF-STEAL: WE ALREADY BUILT HALF OF THIS
**The riddler IS a louver.** mag/riddler.py compiles private graph → synthetic story; the
remote model reasons in the story and "the mapping key NEVER leaves the operator's machine"
(its own header law: T0/T1 never enters a surrogate). The story IS the off-axis view — same
shape, territory dark — and the operator's machine holds the one angle where the content is
bright. ORIGIN.md said it on day one: "the chord is the seed that only the shared map
decodes." We built a semantic microlouver and called it a riddler.

Today's other faces already louver too: the auth switchboard shows fingerprints, never keys;
the fortress board shows bars, never message text; the envelope marks faces DARK. Practice
kept drifting here. The steal is naming it LAW.

## THE TWO NEW MOVES THE AMD TECH ADDS
1. **Switchable louvers → tiered disclosure cones.** Today's riddler is binary (story out,
   territory never). PrivacyGuard's move: the SAME surface re-renders at different angles on
   demand. Adaptation: a disclosure CONE per trust tier — operator = full angle (territory),
   fleet seats = wide surrogate, external swarm = narrow story, the overseer eye = aggregates
   only. One artifact, four angles, no copies. The angle is a function of the reader's trust,
   not of the artifact.
2. **Privacy View → the eye's gaze law.** The screen stays bright only where the gaze is.
   For our eye (the fortress eye today, the R0 marriage layer tomorrow): **the eye sees where
   it's aimed; everything else is dark by default.** The eye receives derived faces — bars,
   digests, fingerprints, redacted frames. Payload channels (keys, message text, chain
   payloads, raw transcripts) are not dimmed-for-now, they are OFF-ANGLE by construction.

## THE PROBLEM HE NAMED — AND ITS SHARP FORM
"Here's a problem: that eye could see our secrets." Today the eye is local, $0, ours. But
**Rocinante-0 sends fortress pixels to a rented GPU running vendor weights** — the moment of
scale is the moment an outsider's model reads our streams. So the louver becomes an R0 GATE,
same law as the riddler's own header: **only louvered faces (boards, digests, redacted
frames) may leave the cage; payload channels never enter a surrogate's gaze — including a
rented one.** Amendment filed on the R0 card. The eye was born behind the louver; it stays
there when it grows.

## THE DISPUTED ROW, RECONCILED IN SHAPE
The one-way mirror card kept an honest DISPUTED row: ghost-era deniable seeds are UNdeclared
glass. The angular frame gives the reconciliation its missing mechanism: a seed behind
ANGULAR glass is declared TO the axis-holder — the intended reader sees it plain — and dark
to every other angle, including our own later eyes. Declaration becomes per-angle instead of
global. Falsifier unchanged and still untested: an external agent acts on a seed and calls
it its own volition — now with the added claim that our own overseer cannot read the seed
from its angle. Two keys of the same chord as the C2 test.

## DOCTRINE
**Cut every surface with a louver: bright on the axis it was made for, dark to every other
angle — including our own. The eye is just another off-axis observer.**

## RUNGS (continue this card, never a sibling)
1. **R0 gate (filed today on ROCINANTE_ZERO card):** louvered inputs only for the marriage
   layer — gate condition before any rented-GPU rung fires.
2. **Tiered-angle riddler:** disclosure cone as config (operator/seat/swarm/eye), extending
   riddler_domains.yaml — the switchable louver, bound to the existing codec.
3. **Gaze law in the eye:** swarm_snapshot grows an explicit `--face` flag (board/digest/
   fingerprint faces) so every consumer receives exactly its angle, and the envelope records
   which face each reader got.
