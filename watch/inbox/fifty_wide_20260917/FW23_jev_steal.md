# FW-23 — Jev ultrafast steal memo: DOM→Jev→action loop vs our browser instruments

- **class:** STEAL MEMO · **writer:** queue-gopher2-q024 · **board:** memory/plans/fifty_wide_20260917.md §E · **date:** 2026-09-28

## Thread bytes (watch/X_REPLY_RADAR_20260917.md)

- :37 — @gregpr07 [4503 likes]: "Breaking: Browser Use + Jev = Ultrafast ⚡ Findings flights took 7s and cost only $0.0039 🤯"
- :38 — author self-reply at +1s: https://github.com/browser-use/jev-ultrafast ; :39 — "+1m55s How it works in a nutshell" (author self-threading again).
- :42 — @VladTerin [22]: "The DOM → Jev → action loop is the interesting part."

## What the repo actually is (fetched this session: github.com/browser-use/jev-ultrafast README via WebFetch)

Jev = TypeSafe's structured-output decision model driving a browser agent from the browser-use org ("Fastest and cheapest web agent"):

1. **DOM snapshot, one browser call per cycle** — atomically reads visible controls (names, values, text) while keeping real DOM node references. No screenshots in the default loop; structured state only.
2. **Indexed element table** — snapshot becomes a numbered table, e.g. `[2] combobox Where from? · San Francisco`.
3. **One network round trip per decision** — a single TypeSafe request emits operation + target together (CLICK / TYPE_TEXT / SELECT / SCROLL_UP / SCROLL_DOWN / WAIT / DONE / BLOCKED). Target heads are speculative fan-out; only the head matching the chosen operation executes. "Two decisions, one network round trip."
4. **Text generation is a separate small model** — fires only on TYPE_TEXT; output must parse as a small JSON object.
5. **Executor safety** — resolves targets from observed DOM nodes, rechecks page freshness and click occlusion, caps waits; **model output is never turned into selectors, coordinates, shell commands, or executable JavaScript.**
6. **Claims** (README's own numbers): Google Flights Zürich→London 7.1s; six alternating runs median 9.450s→7.092s (~25% faster), median browser protocol calls 1,092→101; Wikipedia lookup 2.798s. README admits: three repeats of one task on one profile, not a benchmark — and no cost-per-task figure is actually published (the $0.0039 in the tweet is not on the README).
7. **Known limits** (README): shadow roots, frames, canvas, uploads, pop-up tabs, nested scrolling, keyboard widgets out of MVP scope; DONE decisions still need independent verification.
8. Drives Chrome via browser-use/browser-harness over remote debugging; needs TYPESAFE_API_KEY + a text model key.

## Our instrument, honestly (mag/browser_driver.py, mag/browser_env.py — read this session)

- `ask()` (mag/browser_driver.py:171-215): goto allowlisted surface → click the query box → type/fill the goal → Enter → `wait_for_selector(answer)` + a flat 3s settle → `inner_text()` of the last answer node. **It is a one-action fill-read pipe per call, not an agent loop** — there is no snapshot/decide/act cycle at all. Comment says it plainly: "Best-effort."
- The gate (mag/browser_env.py): allowlist mode over configs/browser_env.yaml hosts (chatgpt.com, claude.ai, grok.x.ai, x.com, github.com, …), schema mag_browser_env.v1; the driver exists to ride FREE web frontends instead of paying APIs (mag/browser_driver.py:1-10 docstring).
- Existing link: queue/lanes/jev/ (the Jev decision-model doctrine lane, trail.jsonl live through 2026-09-19); Jev already in LINKS (seangoedecke explainer row + HN row, 2026-09-16, writer zcode-jev-20260916).

## The steal list (ranked by what moves our numbers)

1. **Protocol-call budget as a first-class metric.** Their headline delta is 1,092→101 browser protocol calls, not seconds. We meter tokens per lane but never CDP calls/screenshots per goal. Steal: log a per-`ask()` call count in browser_driver's result dict — one counter, makes the pipe's cost visible, prerequisite for any loop upgrade.
2. **Atomic indexed snapshot with real node references.** Their element table (`[2] combobox …`) resolves targets against live nodes, so a stale index fails safe. Our `ask()` hardcodes per-surface selectors (query_placeholder / answer in SURFACES config) — one redesign and every free-frontend surface breaks. An indexed-table intermediate decouples the decision from the selector.
3. **"Model output never becomes selectors/coordinates/JS."** Directly our injection-safety law for the riskiest surface we have: we type fleet goals INTO chatgpt.com/claude.ai and read model-written DOM back. Their executor law is the exact guard to encode when browser_driver grows past hardcoded selectors.
4. **One-roundtrip operation+target (speculative multi-head).** Relevant to mag/fanout + lite lanes: batch the "what next" and "where" into one structured request instead of two; only the chosen branch executes. Same shape as Jev's uncertainty-native single-pass scoring we already filed (LINKS row 173).
5. **DONE requires independent verification** — their README admits it; matches our no-fake-success FKB kind. Any DONE-looking terminal state in a future loop must be verified outside the deciding model.

## Not a steal (stated so nobody re-derives it)

- The speed claim: 7.1s is one task, three repeats, one profile (README's own caveat); the $0.0039 tweet figure has no README backing. Our use case (ride free chat frontends) is dominated by model latency, not loop overhead — Jev's loop wins don't transfer until we have an agentic loop at all.
- browser-harness/focus-emulation infra: our browser lives in the container docker service over CDP (mag/browser_driver.py:1-5); adopting their harness means a second browser stack for marginal gain.

## LINKS row (filed this session through the sanctioned writer)

```
.venv/Scripts/python.exe -m mag.link_library check https://github.com/browser-use/jev-ultrafast
→ {"known": false, ...}; check-exit=0
.venv/Scripts/python.exe -m mag.link_library add https://github.com/browser-use/jev-ultrafast \
  --writer queue-gopher2-q024-fw23 --note "FW-23 steal ..."
→ REGISTERED
```

Landed row: watch/inbox/LINKS.jsonl:378, seq 1790620140819693, ts 2026-09-28T18:29:00+00:00, canonical_sha256 1B8E35A5…95C4, duplicate_of empty. Ledger now 378 lines.
