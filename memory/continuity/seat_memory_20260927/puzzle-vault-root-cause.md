---
name: puzzle-vault-root-cause
description: Puzzle vault was an imaginary gate — no wall carried gate:true,
  plate II unreachable in sealed pocket, zero harness lanes consumed the reward;
  all three fixed, 58/58 green
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

Puzzle vault root cause (2026-09-16, N10): the gate machinery called `walls.find(w => w.gate)`
but no wall in the world ever carried `gate: true` — the two-plate puzzle "opened" a gate that
didn't exist. Plate II sat at (1720,1000) inside the sealed south-drafts pocket (no door). Zero
harness lanes ever consumed the key→chest payout. Three levels of dead link: imaginary gate,
unreachable plate, unverified reward.

**Fix:** south band wall tagged `gate:true` (existing seal/open/collision/vision/brass-render
machinery already honored it); plate II moved to forge floor (1720,700); chest pinned inside
vault pocket. Human route: key → plate I (infirmary) → plate II (forge) → gate grinds open →
chest pays 120 souls + full heal + weapon + super orb. 7 new harness lanes (52–58), 58/58
green ×5 consecutive.

Also N12: inventory/loot loop consumed — root cause was a pure consumption gap (no driver),
wired via `makeLoot` on window.MUD + 5 new fifty-gate lanes (59–63), replay-law compliant.

Related: [[mud-replay-law-20260916]], [[wave-20260916-night]]
