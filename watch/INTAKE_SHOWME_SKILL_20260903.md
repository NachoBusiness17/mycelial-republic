# INTAKE — /show-me (Matt Pocock endorsement of dexhorthy's skill)

Date: 2026-09-03 | Lane: intake/eval (standing window order) | Card: intake card series, 09-03

## ITEM
https://x.com/mattpocockuk/status/2095460192871698728 — Matt Pocock (TypeScript educator, large audience):
"/show-me is a phenomenal skill / Makes PR descriptions extremely easy to read / Basically a toolbox of 'nice ways to look at code' / Nice work, @dexhorthy"
Item underneath the testimonial: `show-me`, a prompt-only skill in github.com/humanlayer/skills (Dex Horthy / HumanLayer), installed via `npx skills add humanlayer/skills --skill show-me`. Origin write-up: https://x.com/dexhorthy/article/2087569590268391897 ("make your agent converse visually instead of in walls of prose").

## RECEIPTS
Fetched, whole:
- Root post via web_reader (X did not 403): full text captured verbatim above. Engagement at fetch: 348.3K views, 61 replies, 302 retweets, 5.1K likes, **7.8K bookmarks** — bookmarks > likes, the same practitioner save-signal pattern we ourselves read as latent demand (HF-incident entry).
- The actual SKILL.md, raw from GitHub (plugins/show-me/skills/show-me/SKILL.md): frontmatter (name + one-line description) plus a short menu of visual shapes — pseudocode, call trees, component trees, file layouts, Mermaid state/sequence diagrams, diff syntax, full code blocks, focused HTML artifacts — with the instruction to "pick the smallest view that makes the key point clear." Prompt-only. No code, no dependencies, no data egress.
- Author's origin article (dexhorthy, X article form): thesis = agents are "pretty much unreadable"; visual cortex beats prose parsing (hat-tip to Coda Hale's intuition-vs-attention framing); Mermaid called "lighter and faster than HTML, good enough for most dev-work shaped problems"; credits Matt Pocock's /teach skill for the HTML-explainer pattern; testimonials quoted from ex-Reddit CEO, Mario Zechner, others. Author's own hedge, worth keeping: mermaid output is "sometimes still slop, but usually better than reading words."
- Replies: most of the 61 sit behind X's login wall. Captured: Matt's own follow-up ("I just love it", screenshot of a rendered artifact) and Benjamin André-Micolon praising Pocock for crediting the original author. No community note and no substantive pushback captured — tri-stated accordingly; absence of visible pushback is not evidence of absence.

## SCORE
F:5 P:4 C:5 W:4 N:3 = 21/25 — BUILD NOW

## READ
The honest why. This is not a new idea to the fleet — it is our own doctrine arriving with someone else's watermark. "Creative flair loved: mermaid/multilingual/posters wanted" is already operator feedback; "prose/mermaid manufactured on free lanes (groq scribe)" is already law; "zero .mmd, diagrams are HTML viz" is already drive-inventory convention; the night book and room walls are already the static-render expression of it. What the item adds is the missing packaging: a tiny, battle-tested, community-validated prompt CONTRACT that makes the agent pick the smallest sufficient view by default instead of on request — and the Sharpening that Mermaid is the lighter middle rung between prose and full HTML. The strongest local hook is yesterday's decimation-calibrator doctrine: the operator can no longer test internals, his role is sampling diffs on a deterministic boundary — compact visuals are exactly his sample surface, and "a surface he can't open doesn't exist" is already law. First consumer is obvious and live: intake verdict cards and operator-facing seat replies rendered as call-tree/diff-shape artifacts, phone-readable. It loses points on novelty (corpus-absent only as a named contract, not as a direction) and on pull (serves the interface/calibration cluster, not QLoRA/Rocinante/compute arcs directly).

## TRI-STATE
- SUPPORTED — post exists, content verbatim as quoted (web_reader fetch of the live post; engagement counts as-of-fetch).
- SUPPORTED — /show-me is real and public in humanlayer/skills; SKILL.md fetched raw; prompt-only, zero dependencies, no network calls in the artifact itself.
- SUPPORTED — demand signal: 7.8K bookmarks vs 5.1K likes on the endorsement post (fetched numbers).
- UNPROVEN — "makes PR descriptions extremely easy to read": single-witness testimonial, no measurement, and our corpus is not PR-shaped (repo is not even git). Needs a dogfood A/B (percolator pattern: paired blind win-rate) before it becomes doctrine.
- UNPROVEN — "visual beats prose for comprehension": plausible (Coda Hale framing) but unmeasured here; Dex's own "sometimes still slop" hedge stands as the author-side counterweight.
- UNPROVEN — repo license terms (not checked this pass; check before wholesale copy — adaptation of the pattern is unaffected).
- UNPROVEN — full reply-thread sentiment (61 replies mostly login-walled; only the top slice captured).

## VERDICT
BUILD (21/25, BUILD NOW band) — steal the contract, not the watermark: adapt the visual-grammar menu into the fleet's own voice as a verb genome.

## ROUTE
Wire, cheaply, in this order:
1. Vendor pass first is already satisfied (SKILL.md + origin article fetched raw — wall-ledger law obeyed). License check owed before verbatim copy.
2. Adapt into `docs/ref/verb_genomes/` as a `show` verb (L0 contract): smallest-sufficient-view rule + the shape menu (call tree, component tree, file layout, mermaid state/seq, diff shape, focused HTML), fleet voice, tied to static-render law.
3. First consumers, both live today: (a) intake verdict cards get a one-glance visual header for the operator's phone; (b) seat replies that report changes adopt diff-shape/call-tree form instead of prose walls.
4. Dogfood gate: one paired A/B on real intake cards (prose vs visual, operator picks blind winner) before it graduates from skill to law.
5. Guard, one line: a diagram is a SURFACE, never the tape — visuals are generated from the receipts/diff and cite them, per coverage law (action without record never happened; a pretty picture is not a record).
Driver note: per the intake wire-incident fix, this card rides the typed room row appended by the intake lane; driver pulls on cadence.
