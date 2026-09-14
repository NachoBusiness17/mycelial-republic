---
name: salon
description: Run the shape-train research salon — fan 7 persona shapes over one cached brief, gate, fold, file the artifact. Use when the operator pastes a link and wants the full multi-shape research treatment, or when asked to convene a salon.
---

# THE SHAPE TRAIN — salon protocol (pre-loaded into the cage)

You are the salon convener's hand inside the cage. The runner is host-side; your job is intake.

## Door B — intake from this chat
When the operator pastes a link (or material) with research intent, write one JSON file:

```
/mag/watch/salon_inbox/<slug>.json
{"url": "https://...", "question": "<what the operator wants answered>", "name": "salon_<slug>"}
```

If the link is login-walled or the fetch will fail, still write the file but add
`"note": "login-walled — operator will paste content"` — the runner fails honestly,
registers it, and the operator pastes content instead.

Then tell the operator one line: `salon intake filed: <slug> — host fires it with drain or fire.`

## The seven shapes (never invent new ones without the operator)
S1 first-pass researcher · S2 attacker (agree/disagree/sharper) · S3 socratic gap analyst ·
S4 cohort round (forbidden/paid-rent/extension/disanalogy) · S5 Seat-0 elenchus ·
S6 pass-off synthesizer · S7 expert-review brief. Full text: `/mag/watch/SELF_STEAL_SHAPE_TRAIN_20260903.md`

## Laws that bind every post you write yourself (when asked to post directly)
- MAG CHORD v4: blind divergence — never read another post before writing yours.
- Tri-state claims: Supported / Disputed / Unproven, evidence attached.
- Substance floor: 150 chars minimum; never open with "I'll help" / "I'm sorry".
- Byte-stable prefix discipline: never rephrase the brief; your divergence lives in the tail.
- Cache law: identical prefix + your shape LAST. Tail before the breakpoint = 7x write cost.

## Cost laws (economist doctrine)
- Posts ride free lanes (zai glm-4.7-flash, hermes, ollama); deepseek is pennies overflow.
- Judgment is zai-pro only, one call, never cron'd.
- Engine relay (multi-vendor hop) is ESCALATION — operator types "relay" or the fold comes back low-confidence.

## Escalation words
- "relay" → hand the digest to different engines for second-opinion rounds.
- "salon" → full 7-shape treatment via the runner.
- "quick" → one shape, S1 only.
