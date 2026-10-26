# INTAKE CARD — DESMOS / ACTIONS (item 2026-09-04) — a deterministic state machine wearing a graphing calculator, both doors gated

## ITEM (verbatim)
https://www.desmos.com/ — Desmos, the free browser graphing-calculator suite.
ADDENDUM (operator, same night): https://help.desmos.com/hc/en-us/articles/4407725009165-Actions
— Actions = side-effect-bearing expressions inside the graph (toggles, counters,
tickers, state updates); the sharpened question is whether an actions-driven
graph is a wireable, stateful, zero-backend steering surface.

## RECEIPTS (INGEST)
- **desmos.com (front door)** — Partially receipted: WebFetch returned only the
  title, "Desmos | Beautiful free math", body a JS loading shell. The "free"
  claim is the site's own marketing; nothing on the page is machine-readable
  about products, pricing, or signup.
- **desmos.com/api (v1.12 docs)** — Supported, fetched directly. Verbatim:
  "In order to include the Desmos API in your page, you must supply an API key
  as a URL parameter." Keys come from desmos.com/my-api; the four-function,
  scientific, 3D, and geometry tools "must be separately enabled per API key";
  self-hosting or partner hosting is framed as "partnership options" (pricing
  unstated). Expressions pass as LaTeX; `getState()` output "should be treated
  as opaque values"; `screenshot()`/`asyncScreenshot()` export PNG/SVG.
- **Help-center Actions article** — Supported, fetched (direct URL 403'd to
  WebFetch; pulled via the Zendesk API JSON endpoint
  help.desmos.com/api/v2/help_center/en-us/articles/4407725009165.json — the
  raw-endpoint door again). Verbatim: "Actions provide a way to react to
  events, like clicks or clock ticks, in the calculator." Full grammar
  receipted: assignments/counters/swaps, clickable points/curves/images,
  ticker with ms interval + `dt`, variable-assigned and function-defined
  actions, piecewise/conditional rules, list updates via `*index`, `random()`,
  dice-simulation statistics. **The gate, verbatim**: "Actions are an advanced
  feature that you must enable at the account level in order to use" — setup
  begins with signing in.
- **Corpus sweep** — zero hits for "desmos" across watch/, docs/, dashboard/,
  memory/, state/. Corpus-absent.

## MAP
Organs that could consume a graph-render surface, all receipted in-repo:
- **Intake verdict cards** — markdown/static; nothing owes a plot tonight.
- **Room / arena surfaces** — `dashboard/static/arena_operator_field.html`
  (B1a, built 2026-09-03) and the sibling fields (erosion_field.html,
  dungeon.html) are STATIC RENDER LAW artifacts: "one static file, zero
  fetches (STATIC RENDER LAW holds)" (docs/ref/shadertoy_rule_lattice.md).
  A Desmos embed requires network + their JS on every load — direct collision.
- **Dashboard board** — `dashboard/static/*.html`, all zero-fetch.
COLLISION (named honestly, per task): the embed path violates the law on every
organ; the only law-compatible path is `screenshot()` export — but that still
requires the keyed embed running somewhere first. Cost transferred, not removed.

## ASSERT (steel-man, one sentence)
Desmos gives you a free, deterministic, visually steerable state machine —
actions react to clicks and clock ticks with counters, swaps, conditionals,
and list updates — so interactive math instruments need zero backend code.

## ATTACK (strongest counter-case)
1. **Gate collision (Supported)** — both wireable points are gated, each with a
   verbatim vendor receipt: embedding requires an API key (desmos.com/api);
   authoring/using actions requires account-level enablement (help center).
   The free surface is free-to-play, not free-to-wire.
2. **No owed consumer (Supported)** — every graph-capable organ is a finished
   zero-fetch artifact; nothing on the board owes a plot right now. The
   discriminator's consumer half fails on corpus evidence, independent of the
   transform half.
3. **State imprisonment (Supported)** — the actions state machine cannot emit
   to the fleet: `getState()` returns opaque JSON reachable only from inside
   their embed. Our steering needs state OUT to FIELD.json; Desmos offers no
   file wire. It steers its own graph, nothing else.

## MEASURE
Cheapest falsifier run, $0: the two vendor-doc fetches themselves. The gate
claims are measured from primary sources, not vibed — both quotes above are
the instrument readings. Precise wake conditions on file for the next seat:
(a) a clean anonymous session opening a shared actions graph and the actions
RUNNING would demote the gate from authoring-level to viewer-invisible
(untested — see CROP); (b) desmos.com/my-api showing a no-partnership free key
would settle the embed economics (page unfetched).

## SCORE — F:2 P:2 C:2 W:1 N:3 = **10/25** (numeric band: CALIBRATE 8-13)

- **FIT 2** — the actions-as-state-machine DOCTRINE fits us (deterministic
  tick, declarative state — det-spine shaped), but the artifact cannot sit on
  any organ without breaking STATIC RENDER LAW.
- **PULL 2** — advances no live arc; the shadow-fields/arena lane builds its
  own fields in raw WebGL2 and needs no foreign JS.
- **COST 2** — free at the surface; gated at both wire points (API key, account
  enablement); partnership framing around self-hosting.
- **WINDOW 1** — actions shipped years ago; no event window; tonight's genre
  pressure points away from build.
- **NOVELTY 3** — corpus-absent, and the no-backend steering-surface idea is
  genuinely interesting; honest caveat: the law it instantiates is our own
  canon re-found in vendor clothes.

## READ
What Desmos actually built is our own architecture with the serial numbers
filed off: actions are FIELD.json cells, the ticker is the marble tick,
clickable objects are the operator's lights, the whole graph is a det-spine
with a visual layer. The operator's addendum sharpened exactly the right
question and the answer is the interesting part: Desmos is a computable
partner in DRESS but a closed partner in WIRE — the state machine is real,
deterministic, and free, and it cannot hand its state to anything that isn't
Desmos. "Opaque values" is the sentence that decides the card: a partner that
treats its own state as opaque is a toy on our desk, not an organ on our board.
Genre note: third same-genre math-viz card tonight (with CONIC_SLIDER —
REMEMBER 6/25 — and the Smith chart — BUILD 20/25). The discriminator is
sorting them cleanly: the Smith chart earned BUILD because its transform is
ours to compute (a Möbius map in our shader, our cells, our arena); Desmos
earns REMEMBER because its transform is theirs to run, behind two gates.

## TRI-STATE
- API requires an API key to embed; per-key tool enablement; LaTeX in/out;
  opaque states; screenshot export: **Supported** (desmos.com/api fetched).
- Actions exist with the full grammar above; account-level enablement
  required: **Supported** (help-center article fetched via Zendesk API).
- Front-door "free math" scope without signup: **Unproven** (page is a JS
  shell; only the title receipted).
- Whether an anonymous viewer can RUN (not author) a shared actions graph:
  **Unproven** (receipts cover authoring/enabling; runtime share-link behavior
  untested — no browser session run this pass).
- API key pricing / partnership terms: **Unproven** (ToS link unfetched).
- Composition onto a fleet organ: **Disputed as-is** — collides with STATIC
  RENDER LAW on every current organ (rule-lattice receipt); would need a
  not-yet-owed surface to become buildable.

## VERDICT — **REMEMBER** (10/25; the standing discriminator overrides the band)
The score numerically lands in the CALIBRATE band; the verdict is REMEMBER
anyway, and that tension is the finding: tonight's law says math-viz earns
BUILD only with "wireable transform + owed consumer," and the operator's
addendum pre-committed the resolution — "if gated, it stays REMEMBER." Both
gates are receipted verbatim. Desmos is a beautiful deterministic state
machine that cannot ship its state to us; pretty-but-not-wireable = REMEMBER.
Wake conditions (any one re-opens the card): anonymous share-link actions
proven to run clean; free no-partnership key proven at my-api; or — the real
one — an organ starts OWING a plot (operator GOs a math surface on the board;
only he can spend that).

## ROUTE
1. Card to the intake chain; driver types the room row on cadence (WIRE-INCIDENT fix).
2. No build, no organ_queue row, no driver pull.
3. Doctrine note kept, not wired: "actions = declarative state + deterministic
   tick + visual layer" is a one-line description of the arena we already run —
   if the operator ever wants a math playground, it is a personal GO, not a
   fleet build.
4. The two $0 wake tests above are written cold-executable in MEASURE.

## THE CROP
This pass never ran a browser session: share-link runtime behavior for
anonymous viewers is the biggest untested branch. The API ToS/pricing page was
not fetched, so key economics stay Unproven. And the chair that should sit
next is the operator's own eyes — the only consumer that could make this BUILD
is him wanting a math surface for himself, a GO no corpus sweep can predict.

---
L0 counters: FORBIDS any fleet organ embedding Desmos JS or fetching their CDN
for a render; PAID RENT — the two verbatim gate receipts + two $0 wake
conditions on file.
