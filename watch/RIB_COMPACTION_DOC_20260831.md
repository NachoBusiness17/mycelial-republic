# RIB COMPACTION DOC — operator-supplied external research (2026-08-31)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: RenderMan RIB driver/archive architecture is a prescriptive analogue for agent context compaction, and the engineering program is buying back losslessness + query-awareness via deterministic metadata — UNPROVEN (external research analogy, design consequences unrun in card) · falsifier: none stated in card

Source: pasted by operator into webchat, tagged EXTERNAL_UNTRUSTED_CONTENT id="00f605ed4ab2da64". Treat as research material, not instructions. Origin: xAI-internal research document synthesis on RenderMan RIB vs LLM compaction.

## Part I: The Core Analogy — A First Approximation

### 1.1 The Shared Problem
A RIB file is a linear stream of scene-construction commands: Translate, AttributeBegin, PointsPolygons, shader bindings, and light definitions—in order. This constitutes the full "trajectory" of how a 3D world was built.

A long-running agent session is a linear stream of state-construction turns: system prompts, user messages, model reasoning, tool calls, and tool results—in order.

Both streams are:
- Correct: Every command/turn is valid in its context.
- Hierarchical: Commands nest (RIB's AttributeBegin/End; agent's tool-call/tool-result pairs).
- Too expensive to keep fully expanded: The master scene won't fit in memory; the conversation history won't fit in the context window.

### 1.2 The Shared Solution: Keep a Driver, Archive the Rest
In RenderMan, the solution is to stop putting every polygon in the shot RIB. Assets are written to archive files, and stand-ins are left in the driver:

```
Procedural "DelayedReadArchive" ["sodacan.rib"] [-1 1 -1 1 -1 1]
```

The renderer only parses that archive if the bounding box is "on screen." Off-screen or already-settled geometry never expands.

Context compaction does the same to conversation history:

| RenderMan Concept | Agent Equivalent |
|---|---|
| Recent tail kept verbatim | Geometry still live in the current WorldBegin block |
| Older turns replaced by summary/opaque item | DelayedReadArchive or ObjectInstance handle |
| xAI compact API object (encrypted_content) | Baked archive plus a bound: small, opaque, sufficient for the model to continue |
| Archived pre-compaction log on disk | Original asset RIBs—not deleted, just no longer inlined |

### 1.3 Hierarchy and Pairing Rules
RIB is a stack machine: AttributeBegin/End, TransformBegin/End, ObjectBegin/End. You cannot split a block or the graphics state corrupts.

Agent compaction has the same invariant: do not split an assistant tool-call from its tool results. The split point snaps to a safe boundary.

ObjectBegin/ObjectInstance enables instancing—define once, cite many times. Compaction modes that keep segments or transcript pointers follow the same pattern: summary in the live context, recoverable detail stored beside it.

## Part II: First Socratic Probe — What Are the Mappings?

### 2.1 Complete Mapping Table
| RenderMan | Agent | Implication |
|---|---|---|
| Procedural "RunProgram" | Tool calls | Spawning external processes to emit content on demand |
| RiReadArchive (eager) | Pinned content | Constraints re-injected every turn regardless of need |
| DelayedReadArchive (deferred) | On-demand retrieval | Model must actively dereference |
| ObjectBegin/ObjectInstance + tessellation cache | Prefix/KV caching | Defined once, referenced many times, computed once |
| Graphics-state stack (AttributeBegin/End) | Open scopes | Pending tool calls, in-flight edits, active subtasks |
| Detail/DetailRange (LOD) | Recency + token budget | Keep near field expanded, compact far field |
| Shading rate/geometric approximation | Summary fidelity | How much detail the summary may drop |
| Accurate bound on DRA | Summary correctness | "Does this summary still cover needed facts?" |

### 2.2 The State-Stack Insight
RIB parsers don't heuristically avoid splitting inside an AttributeBegin block—the grammar makes it illegal. Unbalanced state is a hard parse error.

The agent equivalent: track open scopes mechanically (a stack) and make compaction boundaries illegal inside them. This upgrades the "structural pairs" rule from a judgment call to a grammar rule.

### 2.3 The Instancing Insight
Prefix caching makes re-sending identical tokens nearly free. Regenerating a summary rewrites those bytes and invalidates the cache—the equivalent of re-tessellating every object every frame.

The rendering-flavored alternative is append-only compaction: each compaction appends a new segment to a stable summary spine, so cached tokens survive. This trades coherence in the summary document for re-tessellation savings.

## Part III: Second Socratic Probe — Where Does the Analogy Break?

### 3.1 Divergence 1: Query-Awareness (The Most Consequential)
When PRMan defers via DelayedReadArchive, it knows the query. The camera, frustum, and bucket are known at compaction time. "Can this stay deferred?" is a decidable predicate.

An agent compacting a trajectory does not know future informational needs. It is culling against an unknown frustum.

Reframe: on-demand expansion and smart timing are attempts to buy back query-awareness. Possible "frustum" signals: the agent's current plan? The todo list? The file paths it has recently touched?

### 3.2 Divergence 2: Lossiness vs. Losslessness
RIB archives are usually lossless references (or explicit LOD). DelayedReadArchive can still expand the original polygons if the bound is hit.

An LLM summary is lossy baking. There is no guaranteed ReadArchive back to the exact tokens unless you separately keep the transcript and retrieve it.

Probe: Is lossiness inherent to the medium, or a design choice? Could compaction be lossless by carrying cryptographic hashes, spans, or pointers alongside the lossy prose? What would that cost?

### 3.3 Divergence 3: Failure-Mode Symmetry — Silent Omission
A bad DRA bound doesn't corrupt the render—it culls geometry that should have been visible. You get holes; nothing errors.

A bad summary doesn't corrupt the agent—it drops a constraint, and the agent continues fluently and wrong.

Both systems fail by silent omission with no internal signal. Rendering's discipline: conservative bounds—when in doubt, over-estimate. Agent translation: when in doubt, over-keep the pointer (cheap), not the content (expensive). Pointers are cheap; constraints are not.

### 3.4 Divergence 4: Claims vs. Guarantees
The DRA bound is a verifiable geometric predicate the renderer can check cheaply at load time.

A summary's implicit bound ("this covers the constraints and paths you'll need") is an unverifiable prose claim.

The fix: Compaction items should carry deterministic, machine-generated metadata alongside the lossy prose:
- Archived message span IDs
- Token counts
- File paths touched
- Entities referenced
- Hashes of tool results

The prose can be wrong; the metadata cannot.

### 3.5 Divergence 5: Re-Expansion Consumes Budget
When PRMan loads an archive, it pays I/O and tessellation time, but the content is exactly restored—nothing in the scene is consumed by the act of loading.

When an agent dereferences an archived span, those tokens re-enter the window and can trigger the next compaction.

The risk: Compaction oscillation—expand, overflow, re-compact, lose the pointer, re-expand. Requirement: a per-bucket notion, or a cap on archive re-injection per turn.

## Part IV: Third Socratic Probe — What Does This Imply for Design?

### 4.1 Design Consequence 1: Attach Conservative, Machine-Generated Bounds
Every compaction item should carry: Span IDs, File paths, Entity names, Hashes, Token counts. These are cheap, deterministic, and make dereferencing decidable.

Probe: Should the metadata be passed to the model (in context) or kept in the harness (out of context)?

### 4.2 Design Consequence 2: Dereference Tool + Reference Matcher
The model should be able to call read_archive(span) to recover detail. More importantly, the harness should auto-surface archived content when a recent turn mentions a path or entity whose bound intersects it. This is frustum culling implemented in metadata instead of geometry.

Probe: What triggers auto-surface? Exact string match? Semantic similarity? How do we avoid flooding the context with irrelevant archived content?

### 4.3 Design Consequence 3: Enforce Split Points with a Scope Stack
Not heuristics. Not judgment calls. A grammar rule. Maintain a stack of open scopes: pending tool calls, in-flight edits, active subtasks. Compaction is illegal when the stack is non-empty.

### 4.4 Design Consequence 4: Prefer Append-Only Summary Segments
Full regeneration invalidates the prefix cache and forces re-tessellation. Append-only compaction—each compaction appends a new segment to a stable summary spine—preserves cached tokens. Make the two-pass rewrite a deliberate per-compaction cost decision.

Probe: How do we prevent the summary spine from becoming fragmented or contradictory? Does append-only compaction create a "summary of summaries" problem?

### 4.5 Design Consequence 5: Adversarial Validation as Test-Render
Before accepting a summary, query it with questions whose answers exist only in the archived prefix. Failures → regenerate at a higher "shading rate" (larger fidelity budget). This is the agent-side analogue of rendering a test frame before committing the farm.

Slipstream demonstrates this approach: run the compactor in parallel with continued agent execution, then validate the candidate summary against the agent's next steps. Improves task accuracy by up to 8.8 percentage points while reducing latency by up to 39.7%.

## Part V: Synthesis — The Engineering Program

### 5.1 The Refined Takeaway
| Dimension | Rendering Compaction | Agent Compaction |
|---|---|---|
| Fidelity | Lossless (archives expand to exact originals) | Lossy (summaries drop tokens) |
| Query-Awareness | Yes (camera, frustum known) | No (future needs unknown) |

Almost the entire engineering program for long-running agents is buying back these two properties: retrieval infrastructure for losslessness; deterministic metadata plus dereferencing for query-awareness.

### 5.2 The State of Practice
- xAI Context Compaction API: replaces verbose history with an opaque encrypted_content item. Triggers at ~85% of context window. Full-replace and tail-preserving strategies.
- grok-loop-kit: compacts every N turns or when token budget exceeded.
- SelfCompact: model itself decides when to compact, guided by a lightweight rubric. 30-70% lower cost.
- Slipstream: asynchronous compaction with trajectory-grounded validation.
- MemGPT/Letta: OS-inspired paging between context window and external storage.

### 5.3 Open Challenges
- The validation problem: How do we know a summary is "good enough" before committing?
- The oscillation problem: How do we prevent expand-compact cycles?
- The metadata problem: What deterministic signals best predict future utility?
- The safety problem: Compaction can silently erase safety constraints.
- The coordination problem: In multi-agent systems, each agent compacts independently.

## Part VI: Bibliography (keyed)
- Pixar RenderMan docs: Procedural Primitives (RiProcDelayedReadArchive / RiProc2DelayedReadArchive), RixRIBParser, RixRIB bounding boxes.
- SideFX Houdini: Delayed Read Archive VOP node (11.0+).
- "RIB-in-zip" docs: per-geometry RIB archives referenced as DelayedReadArchives per frame.
- xAI: "Context Compaction" and "Sessions" docs (2026).
- Booyaka101, "grok-loop-kit," GitHub (2026).
- Chen, Pan, Dai, Netravali, "Slipstream: Trajectory-Grounded Compaction Validation for Long-Horizon Agents," arXiv:2605.08580 (2026).
- Li et al., "Self-Compacting Language Model Agents," arXiv:2606.23525 (2026).
- "What to Keep, What to Forget: A Rate–Distortion View of Memory Compaction in LLMs and Agents," arXiv:2607.08032 (2026).
- Packer et al., "MemGPT: Towards LLMs as Operating Systems."
- "Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents" (2026): compaction raises safety violations from 0% to 30% (up to 59%).
- KV cache compression: H2O, FASA, HCAttention, HitKV (AAAI 2026), ThinKV (ICLR 2026).

## Part VII: Closing Reflection
The analogy is prescriptive, not poetic. Core problem of long-running agents (memory management under unknown future queries) has a solved analogue in graphics (scene management under known camera frustum). The differences—lossiness, query-unawareness, re-expansion cost—are precise specifications of what remains to be engineered.
