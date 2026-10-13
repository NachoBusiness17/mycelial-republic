# name_translation — Mythic-Noun Table Cell (EXTEND)

## Finding — what your cell yields

The name_translation domain is **Disputed**, not Supported. SEATS.md pins 11 seat names to provider/lane pairs, but the repo's own operating names (Quixote, Sancho, Rocinante, Mickey) appear in 30+ files outside the seat matrix — configs/spend_overlay.yaml, .agents/skills/, corpus/canon/. The "zero mythic nouns" claim holds only inside the SEATS.md table; the auditor sees a second mythic layer bleeding into routing configs. Strongest disagreement with the obvious reading: the obvious reading treats SEATS.md as *the* name registry. The audit-relevant reading is that the repo has **two name systems** — formal seat matrix and informal mythic layer — and the boundary between them is where identity/substrate coupling hides. If "Sancho" means different things in SEATS.md vs AGENTS.md vs the operator's mouth, Athena's cross-model identity transfer has no stable anchor.

## Evidence — what in the repo supports it (file/shape, no invention)

- SEATS.md lines 6–72: 11 seat names → provider/lane pairs
- grep `Quixote|Sancho|Rocinante|Mickey` hits: .agents/skills/frontier-hr/SKILL.md, configs/spend_overlay.yaml, corpus/canon/x_canon_2026_fx/fx_2088552569928867997.json, attic/kill_list_20260908/mag/mag_soul.py
- HABIT.md lines 38–56, 103–115: enforcement commands referencing SEATS.md
- audit_prep/name_translation_cell.md: existing VERIFY cell making the same "zero mythic nouns" claim

## Risk if wrong — what the audit breaks on if this is missed

Steiniger's abliteration instinct strips the mythic layer and finds the seat matrix empty of the names the system actually uses. The identity-across-substrate claim (Oct-27 Apple Silicon migration) collapses: identity must survive substrate change, but if the name "Rocinante" is a parable reference in one file and a routing label in another, the transfer has no stable anchor. The audit flags the whole doctrine as theater.

## The act — the concrete prep step (file/spec/number)

Write `audit_prep/name_translation_spec.md` (60 lines): each seat name → SEATS.md line → HABIT.md enforcement command → mythic-name boundary rule (mythic names only in parable/identity docs, never in routing configs). Include the grep falsifier command. Cheapest artifact: one markdown file, reuses existing SEATS.md + HABIT.md, no code.

## Falsifier — what would prove this wrong

```
grep -rn "Quixote\|Sancho\|Rocinante\|Mickey" configs/ mag/ dashboard/ \
  | grep -v "parable\|identity\|oral_history"
```
Any match outside parable/identity context proves mythic names leak into operational routing → Disputed.
