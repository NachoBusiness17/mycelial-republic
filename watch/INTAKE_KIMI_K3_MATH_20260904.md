# INTAKE CARD — 0xERONN "FROM 13,000 NUMBERS TO KIMI K3" (item, 2026-09-04)

## ITEM
Operator tasking (verbatim): https://x.com/0xEronn/status/2093610808945115624?s=20 —
X post by "0xEronn" (hex-prefixed handle, unknown content at hand-off). Turned out to
be a LONG-FORM X ARTICLE, not a thread: **"From 13,000 Numbers to Kimi K3. The LLM
Math That Changes How You See AI."** (@0xEronn, Eron, published Aug 29 2026, 130.7K
views / 3 replies / 6 quotes / 46 RT / 74 likes). Pedagogy piece walking one unbroken
line: Hinton 1986 backprop → 13,002-weight MNIST digit net ("a geometry," edges
emerge in early layers) → OpenAI Jan-2020 scaling power laws → GPT-4 predicted by
extrapolation → entropy floor of language (claims DeepMind estimated 1.69 bits,
"no model can beat") → chain-of-thought as tree search (AlphaGo Move 37) → RL on
reasoning → Kimi K3 spec walkthrough (MoE, KDA linear attention, MXFP4/MXFP8,
long-horizon agentic RL).

[SOCRATIC] Assumption attacked: "a 130K-view explainer contains buildable signal for
a fleet that already RUNS this math." Instrument: byte-check of the post's spec
section against the primary source (HF model card). Survives: the spec section
(exact match) + one fact the post omitted (custom license). Dies: the thesis that
this "changes how you see AI" — for THIS reader, we operate the machinery daily;
the marginal information is ~1 spec table + 1 license fact + 1 craft pattern.

## RECEIPTS (consult-first, this turn)
- Root article fetched whole via web_reader + WebFetch (X wall did NOT block):
  full pedagogy arc captured verbatim-range; engagement census above (likes < views
  by ~1800x = broad-layperson reach, not practitioner signal; bookmarks not shown).
- Conversation (3 replies, likely complete given count=3):
  1. @BGnowX (Sep 2) — regulator/"can we still print money" joke about Moonshot.
  2. @THE LIVING WEAVE (Sep 1) — "shared math ≠ shared physics," asks how influence
     travels in these systems (a soft emergence question; no technical content).
  3. **@LilithDatura (Aug 29, 362 likes, top reply)** — quotes the scaling-law and
     chain-of-thought passages approvingly. MESH SIGNAL: LilithDatura is the corpus's
     FIRST inbound referrer (sent @ARIKAHENRY to the operator, 08-27, memory index).
     Our audience and this post's audience overlap in named persons — threads-are-
     signal law pays again.
- WebSearch sweep (web_search_prime 429'd twice before landing — rate-limit noted):
  article also lives at x.com/0xEronn/article/2091805709868425238; independent
  coverage exists: r/kimi math-reasoning thread, HF "moonshotai/Kimi-K3 · Keep an
  eye out" (incl. community claim "run locally under $5K"), Substack "Scaling Still
  Works," Towards AI "8 Secrets Every Developer Needs," HN self-hosting thread.
- **FALSIFIER RUN (MEASURE step, $0): WebFetch huggingface.co/moonshotai/Kimi-K3.**
  Primary source receipt, spec section verified against bytes:
  - Total params **2.8T** (safetensors metadata: 2,779,931,837,184) — MATCH.
  - Activated **104B/token** — MATCH.
  - **896 routed experts, 16 selected** + **2 SHARED experts** (post omitted shared) —
    MATCH with omission.
  - Context **1,048,576** — MATCH.
  - 93 layers (1 dense): **69 Kimi Delta Attention (linear) + 24 Gated MLA (full)**,
    96 heads — MATCH (post said 69/93 linear + 24 full).
  - **QAT: MXFP4 weights / MXFP8 activations from SFT onward**; released safetensors
    mostly U8 — MATCH on training precision; NOTE: released artifact is ~multi-TB
    8-bit-ish, so the community "under $5K local" claim implies aggressive requant/
    offload — Unproven, thread not read.
  - Release: benchmarks "as of July 23 2026," collection updated Jul 29 — MATCH
    (post said July 2026).
  - **License: "Kimi K3 License" (custom, tagged other) for code AND weights** —
    OMITTED by the post. Not a clean open release (K2 was Modified-MIT era). This is
    the post's one materially load-bearing gap for fleet routing.

## SCORE — F:3 P:3 C:4 W:3 N:2 = **15/25 → BUILD WINDOWED** (mid-band)

## READ (the honest why)
This is a **genre exemplar wearing a spec delivery vehicle**, and the falsifier is
what makes it scorable: one $0 HF fetch converted the post's spec table from
Unproven-viral-claim to Supported-by-primary-source, which is why it clears the
build floor at all. FIT 3: it feeds exactly two live arcs — the OWED
cache-portability probe (memory: "Kimi 3 ratio/TTL Unproven → cache_watch A/B probe
at Moonshot endpoint"; K3 is now the concrete target, WITH a license constraint the
probe must read first) and Rocinante sizing (104B-active MoE, U8-ish multi-TB
release, HF community claims <$5K local — this is the frontier-sizing datum next to
the uzu card's Qwen lane, and it belongs in the Oct 27 ledger BEFORE hardware day).
PULL 3: pulls a $0 probe re-fire and a sizing row; nothing on this week's critical
path (GLM campaign runs on cloud lanes). COST 4: consume is $0, both consumers are
$0. WINDOW 3: K3 is 5-6 weeks old, community tooling visibly blooming, sizing math
date-gated by Oct 27. NOVELTY 2: 80% is re-find — backprop/scaling-laws sit deeper
in this corpus than in the post (we BUILT the fields it describes); genuinely new
to corpus = KDA linear-attention hybrid as a named datum, the 1.69-bit entropy-floor
claim (Unproven), the license terms, and one craft steal (below). What saves it from
REMEMBER-only: per intake genre rules, math items BUILD only with "wireable
transform + owed consumer" — the K3 spec table IS a wireable transform (cache-ratio
probe + VRAM/sizing math) and the owed consumer already exists in memory.

## DOGFOOD
1. **INVARIANT PASS**: receipts-before-build honored — falsifier ran BEFORE scoring
   (wall-ledger law applied to a social post, not just vendor docs). Tri-state per
   claim. Custody clean (public content). **Two counters — FORBIDS**: routing any
   fleet volume to Moonshot endpoints before the cache_watch A/B reads K3's cache
   ratio/TTL AND the Kimi K3 License text (custom license = gstd-style landmine
   class; "open weights" framing in the post is unlicensed-for-us until read);
   also forbids re-quoting the 1.69-bit number as fact in any public post.
   **PAID RENT**: the intake measure-step muscle — spec table now primary-sourced;
   plus the LilithDatura convergence sharpens threads-are-signal (second deployment
   of that payoff class).
2. **STOCKFISH PASS**: placement = **ROUTER opcode** (the hosted-frontier-with-cache
   leg of the decision table) + **SUBSTRATE ledger** (Rocinante sizing row, Oct 27
   lane). Placement succeeds — both consumers were already standing organs with open
   questions; this card answers one (specs) and opens one (license). Failure mode
   avoided: filing as "nice explainer" with no consumer.

## TRI-STATE
- K3 spec section (2.8T/104B, 896+2 experts/16 routed, 1,048,576 ctx, 69 KDA + 24
  MLA of 93 layers, MXFP4/MXFP8 QAT, July 2026) — **Supported** (HF card
  moonshotai/Kimi-K3, fetched this turn; post omitted 2 shared experts).
- Released weights carry a custom "Kimi K3 License" — **Supported** (HF card tag
  "other"); license TEXT unread, so permitted-use scope — **Unproven**.
- DeepMind estimated natural language's irreducible cross-entropy at 1.69 bits,
  unbeatable — **Unproven** (single-source; attribution unverified; search
  rate-limited this turn). KILL CONDITION for the next seat: locate the DeepMind
  estimate; if the published number differs by >0.1 bits, or no DeepMind
  attribution exists, mark Disputed and strike the number from any reuse. Note the
  stronger theoretical objection: a corpus-dependent log-loss floor is not a
  physical bound — "no model can beat" is category error unless pinned to a
  corpus+tokenizer.
- Backprop (Hinton 1986) / scaling power laws (OpenAI Jan 2020) / GPT-4 predicted
  by extrapolation — **Supported** as standard published history.
- "CoT = tree search + RL made reasoning frontier" — **Supported** directionally
  (AlphaGo MCTS lineage), compressed past the point the fleet's own WHALE receipt
  contradicts at the margin: harness/weights interleaving beat stagewise scaling
  5-9pts — the post's scaling math is not where the 2026 frontier marginal lives.
- "Run K3 locally under $5K" (HF community) — **Unproven** (thread title via search
  snippet only; multi-TB U8 release implies requant/offload not yet receipted).
- Post reaches 130.7K layperson viewers with one unbroken toy→frontier line —
  **Supported** (engagement census) and REMEMBERED as craft: this is the method-post
  shape (receipt-first arc's chapter-two: teach one unbroken line, every step
  load-bearing) — public-arc guild owes a look at WHY it pulled (likes<views
  ~1800x = reach without resonance, or resonance without accounts).

## VERDICT
**BUILD** (windowed) — 15/25. Small, $0, two wires: (1) cache_watch A/B probe at the
Moonshot endpoint re-armed with K3 as target — first read the Kimi K3 License text,
then measure cache ratio/TTL vs our deepseek/z.ai receipts (the probe was already
owed; this names the model and adds the license gate); (2) one sizing row into the
Rocinante/Oct 27 ledger: "K3-class frontier = 104B-active MoE, multi-TB U8 release,
community claims <$5K local (Unproven)" — falsify-or-keep alongside the uzu card's
~63→110-125 tok/s probe before hardware day. Zero code, zero new organs. Craft
pattern (one-unbroken-line pedagogy) rides free as a REMEMBER-grade note for the
operator's method-post arc.

## ROUTE
Wire: yes, two pointers — (1) cache-portability-kimi memory card gains the K3 row
(specs receipted + license gate + probe re-arm), main-seat fold; (2) Oct 27 package
builder / Rocinante manifest gets the sizing row (docked next to INTAKE_UZU card).
No driver interrupt; no build touches this week's campaign lanes. LilithDatura
convergence (her top-reply here, her inbound referral 08-27) noted for the public-arc
seat — the bucket-polish audience map should hold her name. Typed room.jsonl row
left to the main thread per Amendment 1 (path not handed to this spawn).

## THE CROP
Not seen this pass: the 6 quote-tweets (quote layer unexamined); the 1.69-bit
DeepMind attribution (search rate-limited — kill condition above is executable
cold); the Kimi K3 License text (the card's one open gate before any Moonshot
routing); the HF community "<$5K" thread body; whether the K3 API exposes cache
accounting compatible with our cache-mining doctrine (endpoint probe answers).
Next lens/chair: the **economist seat** (sizing row + license constraint fit its
per-op envelope audit) or a free-lane fetch pass on license text + quote layer.
