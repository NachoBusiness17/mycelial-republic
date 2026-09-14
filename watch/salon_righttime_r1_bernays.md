# SALON RIGHT-TIME R1 — BERNAYS lens (audience, consent, presentation timing)

> Provenance: PARENT-AUTHORED fallback, honestly labeled. The Bernays lane was assigned to
> glm-4.7-flash @ z.ai and failed twice on provider overload (FailoverError, 0 tokens both
> strikes); no ollama node available. Sancho runs on the GLM family this session — same
> model family as the intended lens, so the voice is preserved but the independence is NOT.
> Flagged for the standing salon law: next host-side round should re-run this lens from a
> different family for true 3-family independence.

## 1 — Presentation timing: what the fleet should SHAPE (not gate) by clock

Gating refuses work; shaping decides when the audience sees it. Three shape rules, minimal:

1. **Digest rhythm stays human-timed:** digests land on the operator's morning, not UTC
   midnight. HOT items surface immediately (a HOT launch-watch hit is worthless 7 hours
   later); VALID batches wait for the digest. This rule is already half-true (harvest
   cadence 8h); making it explicit costs nothing.
2. **Answer delivery:** `desk_timing` already records per-speaker cadence —
   `last_by_speaker()` and `format_timing_row()` (parent-verified at
   `mycelial-republic/dashboard/rest.py:3713-3714` reading `mag.desk_timing`). Minimal
   upgrade: one new helper, `due(action) -> {deliver: "now" | "defer_to", reason}`, beside
   the existing readers — recorder becomes presenter in ~20 lines, no new organ.
3. **Ractive scene pacing:** next scene loads only after the ractor's reply ("wait is a
   season" — the water clock's own law). The freeze pack holds the scene; timing holds the
   door. No new machinery: it's a rule in the game loop, not a daemon.

## 2 — Prompts-as-games and the honesty guard (consent)

Rules-before-play changes trust because the rules become **inspectable files**: a freeze
pack is on-disk L0/L1/L2 — the operator can read the whole game board before any move.
That is the consent mechanism. The guard that must ride every shaped answer:

- **The clock tag:** anything delayed or shaped by timing carries a visible
  `[shaped: defer_to <ts>]`-class marker. No silent holds.
- **The reversal right:** one operator question — "what did you hold back?" — must always
  return the unshaped truth. Timing that hides is manipulation; timing that reveals is
  presentation. If the fleet cannot answer that question instantly from its receipts,
  the shape layer is illegal and K_T5 (meter open-loop) should fire on the audience axis.

## 3 — Q5 verdict

**Verdict: YES, with one condition.** The stew composes — rules-before-play (freeze packs)
+ ractive loop + temporal authority = teaching by dealing a game the model knows the rules
of — IF and only if every shape is reversible by the operator's single question and every
gate fires on a meter the fleet can actually read (Ellul's condition). The audience lens
adds the third leg the charter was missing: the game must be played WITH the operator,
not performed at him.

Smallest playable experiment (≤3 lines):
1. One scene: freeze a 3-prop tavern pack, one NPC, one typed RolePacket (pack's own step #5).
2. Operator plays the ractor once; the NPC's next line waits on the reply (pacing rule live).
3. PASS = the operator can name what was shaped, when, and why — from receipts, not memory.
