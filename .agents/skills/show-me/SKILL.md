---
name: show-me
description: Render explanations as the smallest visual artifact instead of walls of prose — one menu of shapes (pseudocode, call/component trees, file layouts, Mermaid, diffs, focused code, single-file HTML) and one rule, pick the smallest view that makes the key point clear. Use whenever explaining code, architecture, state, or a change — especially when the reader is the Operator on a phone.
when_to_use: Before writing any multi-paragraph explanation of code, flow, architecture, or a diff — and always first when writing for the Operator.
---

# show-me — the smallest visual artifact

**Provenance:** adapted from `show-me` in dexhorthy/humanlayer (github.com/humanlayer/skills, `plugins/show-me`), the prompt-only skill popularized by Matt Pocock's public testimonial (fetched 2026-09-03; 7.8K bookmarks vs 5.1K likes on the endorsement). Fleet adaptation credited to the local_sovereign_agent build lane, 2026-09-03, operator GO. Prompt-only by the original's own design, kept: no code, no dependencies, no data egress — this file is the whole skill.

## The one rule

**Pick the smallest view that makes the key point clear.**

When explaining structure, flow, state, or change, choose a visual artifact before prose. Escalate only when the smaller view fails. The ladder, smallest first:

```
prose  <  tree / diff / pseudocode  <  Mermaid  <  single-file HTML
```

## The menu (emit the shape, don't describe it)

- **Pseudocode** — the logic without the language noise. Emit a fenced code block in fake-but-obvious syntax.
- **Call tree** — who calls whom. ASCII tree in a fenced block (`driver ──┬─ mickey-1`), one branch per path that matters.
- **Component tree** — organs and their containment/wiring. Same ASCII form; label edges with the channel (bus, queue, file).
- **File layout** — a repo or artifact at a glance. Fenced tree with one-line comments per file.
- **Mermaid state/sequence diagram** — state machines and message flows. Emit a fenced ` ```mermaid ` block; this is the lighter middle rung, good enough for most dev-shaped problems. If it comes out slop (the origin author's own hedge), drop to a tree or step up to HTML — never ship slop.
- **Diff syntax** — what changed. Fenced ` ```diff ` block, `- ` removed / `+ ` added, only the hunk that carries the point.
- **Focused code block** — the one function that IS the answer. Real code, trimmed to the load-bearing lines, path cited.
- **Single-file HTML artifact** — only when the above are too small: an interactive/annotated explainer as one self-contained HTML file the Operator can open anywhere. Static render only, no external calls.

## Fleet-shaped examples (each is one artifact, one line of intent)

- **Spawn tree:** call tree of one driver fanning out to a burst of Mickeys, each branch labeled with its lane (z_ai3 Lite, groq, cache).
- **Organ wiring:** sequence diagram of `steer_bus` → receipts → `event_stream` → chain — a GO flowing from command to signed tape.
- **Monomyth tale map:** state diagram mapping the day's room rows onto departure / initiation / return stages of the tale.
- **GO-row lifecycle:** state diagram `drafted → GO → building → verified → organ.built row → chain knot`, with the dead-end states named.

## The tiered-language law (fleet addition — the bridge)

Workers get baremetal: raw logs, raw diffs, raw commands, no decoration. The **Operator gets the visual shape**. When writing for the Operator, default to the smallest visual artifact first, prose second — his phone is the surface, a wall of prose is a surface he won't open, and a surface he can't open doesn't exist.

## The guard

A diagram is a SURFACE, never the tape. Generate visuals from the receipts and diffs and cite them; a pretty picture is not a record. Action without record never happened — the picture points at the record, it does not replace it.
