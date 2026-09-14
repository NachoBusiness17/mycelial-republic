# LANE6 — V4.1 CODING PACE: can deepseek-v4-flash build viz pages on our stack?

## THE POINT

Yes. We fired one deepseek-v4-flash call (tier T2, 4,000 max tokens) at a real coding
task — build a 3D force-directed graph of the fleet's 17 laws as a single-file canvas
page, same dark aesthetic as the Viz Lab. What came back is a working page: it parses,
the physics converges, it rotates, and it looks like one of ours. One shot, no retries,
3,692 output tokens, pennies. V4.1 Flash can build functional visualization pages on
our stack.

## The shot

- Lane: `models/providers.py` → `chat_provider("deepseek", tier="T2", max_tokens=4000)`
- Model: deepseek-v4-flash (thinking disabled per providers.yaml — 4K budget produces text, not reasoning)
- Prompt: the exact LANE6 prompt, with `dashboard/static/viz_gallery.html` (4.1 KB) pasted in
  as the file it was told to read (a remote API can't open paths — the paste IS the read)
- Result: ok=True on the first call. 1,388 prompt / 3,692 completion tokens. Output came
  wrapped in a markdown fence (stripped before saving). No truncation — file closes `</html>`.
- Saved: `dashboard/static/viz_lattice_test.html` (9,521 chars, 289 lines)

## Verification (all mechanical, receipts above)

| Check | Result | How verified |
|---|---|---|
| HTML parses | PASS | Python html.parser: 0 errors, 0 unclosed tags |
| JS syntax | PASS | `node --check` on the extracted script: clean |
| Single canvas | PASS | 1 `<canvas>`, 2d ctx, DPR-aware resize handler |
| Force-directed graph | PASS | Real one: pairwise Coulomb repulsion (F=k/d²), Hooke springs on 38 edges ((d−L)·k), center gravity, 0.88 velocity damping — in 3D |
| Physics converges | PASS | 600 standalone sim steps in Node: 0 NaN nodes, min pair distance 106.5 vs spring length 110 — layout settles where the springs want it |
| Rotates | PASS | angleY += 0.0018/frame, Y-rotation + fixed 0.15 X-tilt in the projection. Driven 181 frames in Node with a stubbed canvas: 181 renders, 6,878 edge strokes (38×181), 9,231 node arcs, 1,086 depth-culled labels — the loop never stalls |
| 17 law nodes | PASS | Labels I–XVII, exactly 17 nodes, 6 color groups |
| Dark aesthetic | PASS | #0a0806 background, #efe3d0 foreground, warm amber palette, radial glow, depth-fog alpha, painter's-algorithm edge sorting |
| No external libraries | PASS | Zero script src, zero imports, zero fetch — one IIFE, vanilla JS |

## Ratings (1–5)

- **Correctness: 5** — every requested behavior present and verified live, not just read.
  The one caveat is content, not code: the 17 laws' *text* is invented (the prompt never
  listed them, so it synthesized plausible fleet-flavored ones — "the fish was beautiful
  and wrong" lifted straight from the gallery footer). Given no ground truth in the
  prompt, fabrication was the only move; a production version would pass the law list in
  the prompt.
- **Aesthetics: 5** — warm amber-on-dark, node glow, depth alpha, labels only on near
  nodes. Reads as a fleet page, not a generic demo.
- **Completeness: 5** — full document, all constraints honored, no truncation at 3,692/4,000
  tokens. Note: that budget is nearly saturated — a richer page at max_tokens=4000 would
  clip; give generation tasks 8K+ or the default ceiling.
- **Self-containment: 5** — zero dependencies, one file, one canvas. Drops straight into
  `dashboard/static/` and the Viz Lab tab list.

## Verdict

V4.1 Flash (deepseek-v4-flash) CAN build functional visualization pages on our stack,
single-shot, in the pennies lane. It produces the correct architecture unprompted
(IIFE scope, DPR handling, painter's algorithm, depth-culled labels, warm-up iterations
before first paint — that last one is a real graphics-programmer habit, not pattern
completion). Limits: it invents domain content when the prompt doesn't carry it, and
4,000 max_tokens is tight for a full page. For the pyramid: bulk viz generation is a
deepseek job; judgment stays on the premium lanes.

Lane receipt: 1 deepseek call (1,388 in / 3,692 out), 1 HTML artifact, this card. Off-peak
fire (04:13 Beijing), no peak defer triggered, usage logged to the quota ledger.
