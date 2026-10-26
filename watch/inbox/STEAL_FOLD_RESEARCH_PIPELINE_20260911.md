# STEAL FOLD — RESEARCH PIPELINE TRIANGULATION (2026-09-11 evening, lane: zcode)

**THE POINT:** Three zero-shared-context bots tore down Perplexity, the
claim-engines (Elicit/Consensus/scite), and the deep-research products. They
converged on three invariants — and each product's private moat is something we
either already own or don't need. The pipeline upgrade is specified below. The
invariant of the day came from OUTSIDE the wave: "fork vs isolated" is the dial
the whole frontier is converging on, and it is a CACHE decision — the KV OS is
its theory.

## The three invariants (independent convergence = truth by our rule)

1. **CITATIONS ATTACH AT EXTRACTION, bound to verbatim excerpts.**
   Perplexity: prompt assembled as chunk records, generation emits numbered
   citations bound to them. Elicit: every cell carries a mandatory verbatim
   quote + reasoning + prompt version. DeepResearch/NotebookLM: citation
   metadata (URL + exact excerpt) attached when the fact is taken — writing can
   only cite what was retrieved. Bookkeeping, not a smarter model.
   → UPGRADE: knots carry quote + pointer from birth; cite_gate becomes a
   structural guarantee, not a rejection filter. Fits the hash chain natively.
2. **HONESTY = VISIBLE COUNTS + DECLARED THRESHOLDS, never confidence scores.**
   Consensus shows its vote count and hides the meter under n<5; Elicit refuses
   fake confidence — audit by "show the why"; DeepResearch ships coverage
   thresholds (2+ independent sources per sub-question, else UNPROVEN) and
   mandatory "what remains" rows.
   → UPGRADE: invariant sheet keeps vote counts, adds refutation counts and
   n-threshold honesty flags.
3. **STOPPING = CHEAPEST-SUFFICIENT-EVIDENCE CASCADES with hard floors.**
   Perplexity cascade-ranks cheap→expensive; DeepResearch stops at coverage;
   the whole industry prices evidence.
   → UPGRADE: pipeline order is deepseek seam first, escalation only on
   coverage failure, hard UNPROVEN floor.

## What each keeps private (the moats we don't need)
- Perplexity: the search index (Vespa, 200B URLs, 358ms). We don't crawl the
  web — we OWN 1.2M files. Our corpus is the index.
- scite: 40k hand-labeled citations. Not stealable; the CLASS is — train
  contrast-detection on our own cards.
- OpenAI: RL-trained backtracking. Not stealable.
- Their academic mode is just a domain mask (proven by their own filter bug) —
  an allowlist in our research seam replicates it in an afternoon.

## The truth-meter hole (Bot B's sharpest finding)
scite classifies citation CONTEXT: supporting vs CONTRASTING vs mentioning.
Our percolator counts repetition — it never counts REFUTATION. The invariant
sheet ranks by agreement with no way to vote against. That is the upgrade that
turns the sheet from a popularity meter into a truth meter.

## The invariant of the day (from the four evening links)
"**Fork vs isolated is the right dial**" — an OpenHands reply (87k-star
project), the SAME dial as DeepSeek's spawn_teammate (fresh mode vs fork mode),
the SAME dial as our KV-OS scaffold-pinning design. Three unconnected sources,
one dial. Fork shares the prefix; isolated re-encodes it; the cost difference
IS the KV OS. The frontier is converging on a cache decision and calling it an
agent feature.

## The four evening links (mechanisms)
1. **CVE MCP Server** (mukul975/cve-mcp-server): parallel-query NVD + EPSS +
   CISA KEV → composite risk score. Our triangulation as a productized MCP
   tool; cage-install candidate beside Mimosa.
2. **Agenvoy** (Dan Kornas, 2-for-2 today after GraphCode): single-Go-binary
   harness with AUTO TOOL GENERATION (create → test → retain), a SHARED MCP
   TOOL LIBRARY across Claude Code/Codex, NL→cron. Top reply: "Shared tool
   library is the correct obsession" — our mag-gateway design, validated.
3. **OpenHands Agent Canvas**: ACP-protocol agents in one console, 87k stars.
   The dial quote above. Beta-honest.
4. **MiniCPM5-2B, second drop today** (@trikcode): agent capabilities baked in
   at pre-train/SFT/RL "not a wrapper"; skeptic reply says it hallucinates and
   qwen3.5-4b beats it. Tri-state holds; the 2GB edge rig claim stays UNPROVEN
   until our bench.

## Pipeline upgrade spec (v1, the concrete build order)
1. Quote-at-carve: knot writer embeds verbatim excerpt + source pointer + class.
2. Refutation column: contrast detection pass over existing cards (percolator v2).
3. Cascade: deepseek seam → escalation → hard UNPROVEN floor, n-counts shown.
4. Academic mask: domain allowlist in the research seam (their academic mode, $0).
5. Gateway: the four tools on mag/mcp_http.py (padout, invariants, bibliography,
   kvos stats) — backup-first wiring, next strike.

Wave receipt: 3 bots, 1,136k subagent tokens total (A 474k / B 344k / C 344k),
39 tool calls, 3 files, zero overlaps, zero cancellations after relaunch.

## Evening batch 3 (three more, mechanisms only)

1. **Polyphonic Decision Engine** (Dan Kornas, 3-FOR-3 today: GraphCode =
   mesh topology, Agenvoy = shared tool library, now llm-task-orchestrator =
   task routing): complexity/ambiguity/domain/novelty classification →
   deterministic auditable rules → fallback chains → YAML profiles; three
   layers separating classification/routing/audit. That is the fleet's routing
   law (premium touches judgment only) as a public repo. THE REPLY NAMES OUR
   ANSWER: "if the routing layer runs a heavyweight model, turtles all the way
   down" — the fleet's router is deterministic rules + cheap classifiers, so
   the router is always cheaper than its lanes. Router-recursion is only a
   trap if your router is a frontier model.
2. **11.7bn-token security bench** (@0x0SojalSec, aikido.dev blog): V4.1 Flash
   finds a CVE for ~$2, recall 65.6% single / 84.4% pass@3, precision 78.9%,
   "50x cheaper per valid finding"; GLM-5.3 also frontier-level for security.
   Methodology UNVERIFIED (blog). The quip — "burned a tank of gas finding the
   cheap station" — MISSES THE ACCOUNTING: the 11.7bn tokens are capital, not
   expense. Spend once, every downstream user routes through the finding
   forever. That is the corpus/cache economics: one public benchmark is a
   permanent public good. Fleet action: mantis skills + V4.1 at $2/CVE = a
   cheap security organ for the cage once weights are pinned.
3. **MiniCPM5-2B official** (OpenBMB, third drop today): #1 HF trending, day-0
   Intel/AMD/Arm, ships training code + Agent SFT/RL data + UltraX/Meshy/
   JustRL II, iPad-A16-speed reply. The P3 edge-rig candidate firms — x86+Arm
   day-0 means the cage and the eye could serve it.

## Evening batch 5 (four more — the V4.1 triangulation closes)

1. **SemiAnalysis confirms the morning read** (32.7K views, the board's most
   credible analyst): CED, 8B prefill/16B decode (CORRECT order — unlike
   nrehiew_), 196B Engram via sparse lookups, ~8x less persistent KV via
   bounded replay. FIFTH independent lane; architecture facts now five-lane
   triangulated with zero surviving disputes. The one error all day remains
   nrehiew_'s flip — caught against primary.
2. **Abliteration reaches edge scale** (OrcaRouter, second drop today):
   Nex-N2.5 Mini Uncensored — agentic post-train on Qwen3.5-35B-A3B, IQ4_XS
   GGUF 18.73GB (24GB machines), MLX build. The weight-level probe escalated
   from frontier (GLM 320B) to consumer in one day, marketed as a feature
   ("run it locally, break it"). Sharpest reply = the falsifier: does
   TOOL-CALLING survive abliteration — testable by anyone with the GGUF.
   Wrongthink map row updated: refusal removal is now an edge-scale product.
3. **GLM-5.3-Flash economics independently charted** (@zRdianjiao): the whole
   coding frontier is five plans, $0.00133–$0.01274 per million tokens; our
   judgment lane's 2x-quota window averages ~$0.0045 — ON the public Pareto
   frontier. The critique reply ("the denominator is doing all the work") is
   the desk catch: plan-claimed tokens vs MEASURED burns — our burn board
   holds the measured version the public chart lacks. Bibliography row.
4. **Slop item** (Gumroad C++ course ad): no mechanism to sweep — counted,
   not triaged. The librarian now tracks slop rate as a desk health metric.


## Evening batch 4 (eight more, the free-lane map fills in)

1. **Free-lane map** (jdraven + zefirium): GLM 5.3 Flash FREE on OrcaRouter
   (same router that posted the abliteration paper — provenance caution
   stands), V4.1 Flash $0 on XP Labs, GPT-5.6 Luna $0 with 1M context on
   APInex. The promo economics are hardening into permanent infrastructure.
   Lane-intel, bench through the provenance-pinned endpoint only.
2. **audio.cpp** (0xShug0): ggml-based pure C++ audio — TTS/ASR/voice
   conversion, Qwen3 models, NO Python in the inference core. Steal: the
   cage-law version of the ear (space_ear runs faster-whisper/Python); voice
   input on-device for the 2GB edge rig.
3. **Beej's Guide, 30 years free** (@TrisH0x2A): one maintainer, free forever,
   became infrastructure, "funnier than any technical book has a right to be."
   The room-that-remembers, network edition — the aspiration standard for
   docs/ref: write once, keep true, keep free, keep funny.
4. **16 free AI/ML repos** (@SCR01111): curriculum wave again; karpathy
   nn-zero-to-hero leads. Feeds the pedagogy half of the bibliography map.
5. **Nanocoder** (Dan Kornas — 4-FOR-4 today: topology, tool library, router,
   now vendor-neutral CLI agent with normal/auto-accept/yolo/plan modes, MIT).
   He is shipping the fleet control plane from the outside, repo by repo.
   SHARPEST REPLY: tool schemas vary PER PROVIDER, changing agent behavior
   under identical config — "does Nanocoder pin the tool schema?" That is W3
   cache-identity at the agent layer: pin the schema, content-address the
   tool definitions, or behavior drifts byte-by-byte.
6. **Muse Spark 1.3 free in Cline** (vendor: "similar to Opus 5"; top reply:
   "clearly benchmaxed... doesn't even match GLM-5.3 Flash"). Tri-state in the
   wild — and note: GLM-5.3 Flash is now the measuring stick strangers reach
   for. Vendor claim UNPROVEN; the free-tier competition is real regardless.
7. **Gromov–Hausdorff ≅ Hilbert space, proved WITH AI** (arXiv, 34K views):
   first AI-collaborated structure theorem in our stack; math wing datum.
   Replies demand the readable law: "ai-generated unreadable texts" fails
   one-pass readability even in topology. Verification pending — claim exists.

