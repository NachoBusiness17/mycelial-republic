---
name: corrections-research
description: SWEEP the operator's research links to primary sources - mechanisms out, slop framing dropped, bibliography row landed (law 18). Use whenever the operator posts research links, papers, or slop posts for the desk.
when_to_use: Every research intake from an operator-posted link.
argument-hint: <url-or-post-ref> [subsystem]
---

# SWEEP - research intake, primary sources only (law 18, standing)

When the operator posts research links, NEVER return the slop post's own
framing. Extract the MECHANISMS described and sweep the academic literature -
arXiv papers, primary sources, adjacent research - and return that instead.
Clickbait is an input, never an output. If `$0` (the link) is missing, ask
for the source URL before sweeping.

Every desk intake gets a DEEPSEEK PAD-OUT (adjacent-literature scaffold,
routed through the CHEAP lane per the routing law) acting as its
bibliography, and every paper lands on `docs/ref/BIBLIOGRAPHY_MAP.md` -
paper -> subsystem -> status - so when a system is upgraded we know which
research it instantiates and where the new piece connects.

GATES: the pad-out rides the cheap lane (deepseek/local $); the premium lane
only on operator word. TEETH: any desk reply that summarizes a post without
a mechanism-level academic sweep is a repeated failure; any build that
touches a subsystem without consulting its bibliography rows is a repeated
failure.

## Commands

```bash
# before building on a subsystem, consult its rows
grep -in "<subsystem>" docs/ref/BIBLIOGRAPHY_MAP.md
# after the sweep, land the new rows (one per paper: ref, subsystem, what it gives, status, where used)
```

Final response: the mechanisms extracted (not the post's framing), the
primary-source list with the pad-out receipt path, the BIBLIOGRAPHY_MAP rows
added, and any subsystem-build consult that the sweep flagged as owed.
