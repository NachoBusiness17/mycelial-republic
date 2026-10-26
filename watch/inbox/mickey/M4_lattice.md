# M4 — Viz lattice polish and deploy (mickey lane 4/7)

Date: 2026-09-11 · Seat: zcode (mickey lane) · Files touched:
- `dashboard/static/viz_lattice_test.html`
- `dashboard/static/viz_gallery.html`

## What changed

1. **Real laws in, invented labels out.** Lane 6's deepseek single-shot invented poetic
   17-law labels ("The Republic is the chain", "The horse gallops on the flash lane"...).
   Replaced all of them with the REAL laws read from
   `.agents/skills/operator-corrections/SKILL.md` — short canvas-legible names, full
   one-liners listed below.
2. **Count correction: 17 → 18.** The task said 17 laws; the skill file now carries 18
   (Law 18, RESEARCH INTAKE — PRIMARY SOURCES ONLY, added 2026-09-11, after the lattice
   was conceived). Truth over gloss: rendered all 18. Node count, header sub, title, and
   footer all updated to match. The deepseek render's edges referenced 17 node indices,
   so the edge set was rebuilt for 18 nodes: 17 chain edges (law order) + 17 semantic
   cross-links = 34 edges.
3. **Gallery load.** Added the tab to `viz_gallery.html` TABS:
   `{ id:'laws', name:'Law Lattice', src:'viz_lattice_test.html', note:'the constitution as a force-directed graph — 18 real correction laws · deepseek-v4-flash single-shot, labels grounded' }`
   (name adjusted from the specced '17 Laws Lattice' to match the real count).
4. Deepseek's bones kept whole (sacred cows, not legacy shit): 3D fibonacci-sphere
   seeding, repulsion+spring simulation, painter's-algorithm depth sorting, slow
   Y-rotation, warm-up passes. The simulation is count-agnostic, so 18 nodes needed no
   force-parameter changes.

## What was verified

- `node --check` on the extracted inline script: **SYNTAX OK**.
- Node/edge sanity: 18 nodes, 34 edges, max node index 17 (< 18, no dangling edges).
- Gallery tab confirmed present: `grep id:'laws' viz_gallery.html` → 1 hit, line 46.
- Not verified in a live browser (no GUI lane here) — JS parse + data bounds are the
  receipt; the render path is unchanged from the 5/5 lane-6 build.

## The loaded-law list (as rendered on the lattice)

| # | Label | One-liner (from the corrections skill) |
|---|-------|----------------------------------------|
| I | Consult first | If a tool, command, or doc would answer faster than re-deriving it, use it first. |
| II | Two-strike bail | Any approach failing twice → switch strategy, consult the other seat, or read the docs. |
| III | Stop when verified | Once criteria are met and verified against the operator's surface, stop. |
| IV | Verify on their surface | "It works" is only true on the surface the operator actually touches. |
| V | Compose first | The first sentence of every message is written in plain language and checked first. |
| VI | Claim only from data | Never assert a fact or a fix "works" unless read from data first. |
| VII | Meet at the bytes | Read the actual file, output, or state before agreeing or correcting. |
| VIII | No apology spirals | Corrections are fixed directly, plainly, once — not performed. |
| IX | Rightsize, not pattern-match | Ask what the actual situation calls for; never copy a default blindly. |
| X | No sacred cows | Every past decision was the best understanding at the time; re-evaluate freely. |
| XI | One supervisor only | Never start a second supervisor on the host; the watchdog is it. |
| XII | Standard binds both ways | The seats keep the operator to the same law he keeps them to. |
| XIII | Cite laws at design time | Name the standing laws any host-side runtime touches, before it runs. |
| XIV | Handshakes are loans | Every unlock owes a first-use receipt within a day. |
| XV | Reserves at starvation | Finite-pool rescue levers spend at measured starvation, never at impatience. |
| XVI | One steerer | No parallel background subagents during burn windows. |
| XVII | Stream is filtered surface | Charged-register source lives in files; reference by path, never paste. |
| XVIII | Primary sources only | Research intake sweeps primary literature; clickbait is an input, never an output. |

## NEXT:

Labels are short names to stay canvas-legible — a hover/click tooltip carrying each
law's full one-liner (plus its skill-file line number) is the next polish pass; also
worth wiring edge choice to real co-citation (which laws get cited together in the
failure ledger) instead of hand-picked semantic links.

SPAWNABLE: a small worker job to mine `operator-corrections/SKILL.md` + the failure
ledger for law co-citation pairs and emit a JSON edge list the lattice loads at runtime
(edges become evidence, not taste).
