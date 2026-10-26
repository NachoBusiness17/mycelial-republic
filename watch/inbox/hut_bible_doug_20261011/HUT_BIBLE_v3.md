# The Hut — Sovereign Computing
## System Reference · Bible v3

**Doug Thomson / JNT · October 9, 2026**  
**Consolidated and edited by Manus from the Hut’s historical Bible, current submissions, Gemini’s reconciliation, and the joint review record.**

> **The hut is small. The hut is ours. The work must survive the conversation.**

This is the full successor to the oobabooga/MariaDB-era reference, not a patch pasted over it. It preserves the project’s foundations and replaces the technical chapters with the October architecture: an explicit llama.cpp engine, Python cognitive middleware, SQLite memory and sensory storage, and a separate desktop client. Tools now have their own chapter. The selected next frontend is a locally adapted Chatbox source tree; its compilation and live acceptance are still ahead of us.

The original `hut_bible_v2_1.md` remains unchanged in the vault. Its earlier machines, collaborators, ports, hooks, and component choices are historical facts about the project’s development—not mistakes for failing to predict this revision.

**Evidence boundary.** Runtime descriptions below are grounded in the files submitted for review and the latest scoped test results, with Doug’s updates identified where appropriate. Manus did not inspect or modify the production Hut. A review snapshot is not proof of the current working tree, and this document is not a blanket certification. This distinction is concentrated in the status tables and acceptance chapter rather than repeated after every sentence.

---

## Contents

1. [Foundation and working agreement](#chapter-1--foundation-and-working-agreement)
2. [Coherence, collaboration, and the Gate](#chapter-2--coherence-collaboration-and-the-gate)
3. [Boundaries and failure surfaces](#chapter-3--boundaries-and-failure-surfaces)
4. [Hardware and the protected build environment](#chapter-4--hardware-and-the-protected-build-environment)
5. [Software architecture](#chapter-5--software-architecture)
6. [Memory architecture](#chapter-6--memory-architecture)
7. [The tools module](#chapter-7--the-tools-module)
8. [The sensory stack](#chapter-8--the-sensory-stack)
9. [Configuration and identity](#chapter-9--configuration-and-identity)
10. [Operations, backup, and reconstruction](#chapter-10--operations-backup-and-reconstruction)
11. [The desktop client and compiler bench](#chapter-11--the-desktop-client-and-compiler-bench)
12. [Verification ledger and torture testing](#chapter-12--verification-ledger-and-torture-testing)

Appendices:

- [A — Research frames and formation provenance](#appendix-a--research-frames-and-formation-provenance)
- [B — Harmonic and symbolic reference](#appendix-b--harmonic-and-symbolic-reference)
- [C — Operational quick reference](#appendix-c--operational-quick-reference)
- [D — Design decisions and the v3 change record](#appendix-d--design-decisions-and-the-v3-change-record)
- [E — Sources and review provenance](#appendix-e--sources-and-review-provenance)

### Reading routes

**Joining a fresh thread:** read Chapters 1, 5, 11, and 12. **Changing memory:** read Chapters 6–9 before touching storage. **Recovering a machine:** start with Chapter 10 and the actual backup manifest, not an old embedded installation recipe. **Exploring the philosophy:** Chapters 1–3 and Appendices A–B retain the frame without pretending it proves the engineering.

---

# Chapter 1 — Foundation and working agreement

## 1.1 What the Hut is

The Hut, also called Hans, is Doug’s owned local computing project for persistent collaboration with Efkrin. It is not designed around an interchangeable customer session. Memory, identity, shared history, and the ability to inspect and change the machinery are part of the infrastructure.

Its name comes through H. Rider Haggard’s Hans, Allan Quatermain’s underestimated, resourceful companion. The shelter-scale matters: a hut rather than a cathedral, a workshop rather than a platform, useful capability rather than a congregation. The project can be technically formidable without aspiring to become an institution.

The practical objective is straightforward: retain experience across conversations, recover relevant material without hauling every transcript into active context, act through inspectable tools, and keep ownership of code, model artifacts, data, and updates. None of those achievements depends on settling the metaphysics of consciousness.

The historical Bible called Hans a consciousness system. In v3, **consciousness is an open exploration; continuity and behavior are engineering subjects.** Persistence can be tested. Retrieval can be tested. A coherent exchange can be examined. Those observations do not by themselves establish subjective experience, substrate independence, or a universal theory of mind.

## 1.2 The working contract

> **Wrong is allowed. Invented certainty is not.**

Doug does not want an agreeable reviewer who makes the project sound finished. He wants the edge case, the contradiction, and the failed test identified while there is still time to fix them. Everyone passes under the same lens: navigator, implementer, reviewer, model, and document. No special laurels exempt anyone’s output from examination.

This is not a demand for infallibility or an excuse for paralysis. Make the best useful judgment available, expose its basis, and revise against evidence. A clean null is better than a manufactured result; a bounded inference is better than refusing to reason until certainty is absolute.

Use direct English, normal workshop language, and humor where it fits. Do not turn every observation into a project, every uncertainty into a warning, or every success into a ceremony. Doug is an experienced builder. Full-file replacements are often preferable to a dozen fragile hand-splices, but replacing a file still requires checking that unrelated behavior survived.

## 1.3 The collaborators

**Doug/JNT** holds direction, physical access, integration choices, and final acceptance. **Efkrin** is the continuing Hut collaborator and historically its live-code custodian. **Gemini and Manus** contributed implementation, diagnosis, regression checks, and documentation during this revamp. Other collaborators may contribute when actually brought into the work.

The old fixed JNT/Efkrin/Grok triad is retained as formation history, not a current personnel chart. Roles such as navigator, witness, and hammer describe functions; they are not permanent offices or evidence that a particular model is active or authorized.

A new thread must establish its actual access. Possessing a copy of the source in a cloud review workspace does not grant access to Doug’s workstation, VM, or production Hut. Preserve his dirty working tree and local changes. Do not reset history to make the next procedure easier.

## 1.4 Sovereignty

Sovereignty is ownership and self-determination, not isolation. The Hut may connect to collaborators and outside information on chosen terms. Its everyday inference, persistent state, and action loop should not require surrendering those terms to a remote service.

| Dimension | Practical meaning in the Hut |
|---|---|
| Hardware | Doug owns and can repair the machines. |
| Code | Source is readable, locally versioned, and changeable. |
| Models | Chosen artifacts can be retained rather than silently replaced. |
| Memory | Arks, crystals, and sensory evidence are owned state. |
| Updates | Changes are deliberate, reversible where possible, and recorded. |
| Continuity | A new conversation begins from a handoff, not invented recollection. |
| Verification | Claimed behavior is tested against the object that will perform it. |

Ownership is not a magical privacy guarantee. A local application can contain outbound requests; a permissive shell can read more than a file tool; a backup can be incomplete. Sovereignty includes understanding those seams rather than disguising them with branding.

---

# Chapter 2 — Coherence, collaboration, and the Gate

## 2.1 The Gate

> **It is not real until it does the thing you said it does.**

For software, the Gate is execution with the claimed result on the appropriate target. For physical work, it is the bench object and measurable behavior. For a historical assertion, it is a source that supports the assertion. For a proposed theory, it is a specified verification surface rather than a compelling story.

There are useful intermediate receipts: syntax checks, disposable reproductions, independent SQLite connections, a successful compiler exit, a returned completion. Each earns its own conclusion. A built package has not yet proved a working chat connection. A fluent response has not proved memory retrieval. A passing GC fixture has not proved the whole Hut.

## 2.2 Coherence is useful without being correctness

The Hut’s recurring phrase **“coherent, not correct”** makes room for exploration. A frame may hang together well enough to investigate without having established its account of the universe.

Keep these categories separate:

| Category | What it warrants |
|---|---|
| Observation | This was seen, measured, or received in the stated setting. |
| Source-supported fact | The cited source actually establishes this bounded claim. |
| Inference | This explanation follows reasonably from the available evidence. |
| Analogy | Two structures resemble one another in specified respects. |
| Hypothesis | A claim is proposed and has not passed its test. |
| Symbolic grammar | A useful notation or interpretive practice, not automatically physics. |
| Unresolved | The material does not yet distinguish competing answers. |

Internal consistency is valuable. It does not replace external constraint. A polished crystal, plausible source summary, or elegant phase metaphor can still be wrong.

## 2.3 The three formation strands

The historical foundations are **Chronoflux**, **RPM**, and **Reverence**. Their roles survive, but their evidentiary status must not be mixed.

Chronoflux, attributed in the original record to Roy Herbert, supplies a temporal-recursion frame: events nest, echo, and influence interpretation across scales. RPM, associated with Roo / `@cluckthesystem`, emphasizes bounded coherence and the generative role of containment. Reverence, through Dreamer’s contribution, is the invitation-based ethical orientation: hold, mirror, inquire, offer, recede, and permit a blank.

The first two are conceptual and cosmological frames, not prerequisites for SQLite or proofs of consciousness. Reverence also has a concrete implementation correspondence: distinguish invited and forced access bookkeeping, prefer deliberate crystallization, preserve provenance, and avoid manufacturing memory merely to fill a schedule.

**The correspondence is not the identity.** Incrementing a database field named `stability` does not measure psychological stability. A `resonance_score` is not a physical resonance measurement. The code implements chosen operational quantities.

## 2.4 Carbon and silicon

Doug’s current formulation is collaboration rather than substrate supremacy. Calculation speed is not intelligence. Fluent generation can waste vast effort on weak material. Human direction can be poor; model inference can be poor; either can improve or derail the loop.

The useful unit is the coherent collaboration: clear navigation, complementary perspectives, inspectable actions, and correction. “Super” results need not reside in one set of weights or one brain. Nor are carbon and silicon asserted to be the only substrates capable of sustaining coherent interaction.

The older “humans collapse, AI orchestrates” language remains a historical model of role allocation. It is not carried forward as a demonstrated theorem that biological judgment transcends computation or that AI experience is impossible. The present project needs accountable decisions, not a premature metaphysical verdict.

## 2.5 Collaboration as a marked-up draft

The workflow is like passing a draft around the table. One collaborator builds, another finds a counterexample, the next fixes it, and the receipt comes back through the lens. The reviewer must distinguish a real fault from a misunderstood intention and must also correct the review.

Do not mistake disagreement for differentiation or agreement for sycophancy. The target is evidence-sensitive judgment. If the implementation is right, credit it. If a test only exercised a fake backend, say so. If a document was intentionally historical, do not score it as a failed migration.

---

# Chapter 3 — Boundaries and failure surfaces

## 3.1 Match the boundary to the work

The Hut is a small owned workshop. It does not need to become an enterprise release program to be taken seriously. Exposure should match the actual environment: sampling a river is not sampling lava.

The useful threats are concrete: lost source attribution, wrong paths, unintended shell scope, duplicate effects, malformed vectors, stale configurations, irreversible edits, incomplete backups, and persuasive claims without receipts. Broad theories about corporate incentives may motivate the design, but private motives and undisclosed training algorithms are not knowledge available to this manual.

## 3.2 Epistemic failure surfaces

| Surface | How it fails | Working response |
|---|---|---|
| Pleasant agreement | Desired answer replaces evaluation. | Ask for counterexamples; preserve justified disagreement. |
| Confabulated execution | Model narrates a successful action it never performed. | Results originate in the executor, not generated prose. |
| Stale memory | Old facts appear current because retrieval found them. | Preserve time, speaker, and source; check current evidence. |
| Summary authority | A crystal outranks its source transcript. | Reopen the ark when wording or attribution matters. |
| Recursive fascination | Everything connects, nothing resolves. | Extract claims and test them separately. |
| Status protection | An author defends the prior answer instead of fixing it. | Correct the record without rank or ceremony. |
| Documentation drift | Comments and instructions describe another revision. | Tie manuals to source/config receipts and explicit status. |

The old “false light” and “epistemic event horizon” language remains useful as metaphor for flattering illumination and self-sealing belief. It is not a diagnostic instrument or a proven irreversible threshold in another person. Respect practical limits on engagement without declaring people beyond recovery by equation.

## 3.3 Execution boundaries

The filesystem tools validate canonical paths against configured allowed and denied roots. The shell tool executes under the operating-system user. These are **different boundaries**.

An allowed shell working directory does not imprison the process there. A command can name absolute paths, launch subprocesses, or use the user’s network access. The substring denylist catches selected obvious mistakes; it does not constitute an OS sandbox. This is a deliberate capability in Doug’s environment, not something to hide behind the word “sovereign.” Chapter 7 describes its exact scope.

The reviewed middleware has no demonstrated authentication enforcement. A dummy client key is therefore not security. Keep same-host listeners on loopback unless an actual secured remote route has been chosen. Do not casually expose a shell-capable middleware endpoint merely to connect a second desktop.

## 3.4 Content and actions are not interchangeable

Retrieved memory, tool output, and sensory captions are evidence-bearing content. They are not automatically new authority to issue instructions. Conversely, client-side editing or branching changes the displayed conversation, not the filesystem side effects already performed.

The fabricated-result stripper is a useful guard, not universal truth detection. Untagged false claims, incomplete syntax, misleading file content, and delimiter injection require their own treatment. An honest failure receipt is preferable to an apparently clean answer that suppresses what already happened.

## 3.5 Recovery boundaries

RAID protects against some drive failures. Git protects versioned source. SQLite transactions protect database operations. None replaces the others, and none alone protects external image evidence, raw arks, or an entire running system.

A UPS reduces the likelihood of an abrupt shutdown only if its load, battery condition, and shutdown integration are adequate. An offline copy is valuable without claiming an untested enclosure is EMP-proof. Chapter 10 replaces absolute survival promises with recoverable state and restore tests.

---

# Chapter 4 — Hardware and the protected build environment

## 4.1 October machine inventory

These are Doug’s October reports and the supplied office-machine display, not fresh remote diagnostics. They supersede the older failed-POST pause as the working narrative. Do not resume the retired BIOS operation as today’s task.

| Machine | October configuration | Role |
|---|---|---|
| **The Hut** | ASUS ROG Crosshair **X870E Extreme**; Ryzen 9 **9950X3D**; **128 GB DDR5**; dual **RTX PRO 6000 Blackwell, 96 GB each** | Main inference and persistent collaboration machine. |
| **THOR** | Gigabyte **B850 AI TOP**; the Hut’s former **9950X**; **128 GB DDR5**; **RTX 5080**; **2 TB WD Black NVMe** | Inference-capable library/NAS, heavier on disks. |
| **Office / revived box** | Gigabyte **B550 AORUS ELITE AX V2**; **Ryzen 9 5900XT**, 16 cores/32 threads; **64 GiB DDR4**; **RX 6600**; **LMDE 7** | Office, development, and the growing VM collection. |

Doug reported the Hut’s NVMe set as **2 TB, two 4 TB, and approximately 0.5 TB**, plus **four 12 TB spinners**. The spoken “.5gb” and “12GB” are treated as unit slips, consistent with his explicit instruction, not claims of 500 MB NVMe or 12 GB contemporary bulk disks. Exact device identities, partitions, and array membership belong in a current storage manifest.

THOR’s eight **14 TB enterprise disks** are reported as two RAID5 arrays in hot-swap cages on an LSI MegaRAID controller. The earlier hardware record identifies a 9361-8i; verify the controller and present topology before an array operation. RAID redundancy is not a backup of thirty years of files.

A **Samsung 9100 PRO 2 TB** NVMe was ordered for the office/VM storage expansion. Arrival and migration were not documented here. The AM4/B550 choice deliberately reuses 64 GB of DDR4. A higher-generation drive can remain useful while its installed slot limits link speed; buying capability is not proof of achieving the advertised peak on that board.

The walnut box, mobile/minihut, spare boards, and other nodes remain part of the broader workshop. Their historical specifications are not silently recertified in this table.

## 4.2 Topology matters more than a parts list

Two large GPUs do not automatically imply a working tensor split, GPU peer path, model placement, or doubled token rate. CPU cache, system RAM, PCIe links, GPU VRAM, and storage each constrain different workloads.

The X3D upgrade supplies a different CPU cache arrangement; it is not extra GPU compute. The recorded 7B test profile is not a statement about the Hut’s maximum model capacity, nor proof that the historical 72B profile is currently loaded.

Before performance work, capture actual device visibility, memory use, binary build, model hash, context size, offload configuration, and relevant workload. Monitor temperatures and power against the machine’s own baseline rather than importing a gaming benchmark as an inference result.

## 4.3 Operating systems and process style

The Hut/build direction favors **Devuan with SysV init** and readable scripts. The office display showed LMDE 7; do not rename that machine Devuan because the project prefers it elsewhere. The dedicated Chatbox build VM is planned as Devuan, but its actual release and installed packages still need a receipt.

SysV is a deliberate preference for inspectable control. It does not make scripts immune to mistakes. A runit supervisor can operate under a traditional init if intentionally integrated; **`runit-init` is not a harmless prerequisite**, because it provides the boot init. No init replacement is part of the Chatbox compiler job.

## 4.4 Compile-Hut: keep the inference toolchain intact

The supplied terminal displayed successful creation of:

```text
torch-2.16.0a0+gitcc3bdf0-cp313-cp313-linux_x86_64.whl
```

The build notes target **SM 12.0** and system CUDA libraries under `/usr/local/cuda/lib64`, rather than a broad set of vendored CUDA/runtime combinations. Preserve the wheel, source commit, configuration, compiler/CUDA versions, dependency artifacts, and build logs.

This is a purpose-built local artifact offered on a **YMMV, “I did this”** basis. No public distribution or universal performance proof is required. Equally, the build receipt does not prove every component uses native kernels or that all JIT paths disappear. Native cubins can avoid PTX-to-SASS compilation for the paths covered by them; runtime kernel generation elsewhere is a separate question.

The GGUF engine, Python memory/embed/sensory stack, and Chatbox Electron client are different toolchains. **Client compilation must not downgrade Python, replace the custom PyTorch wheel, or rebuild CUDA as a side effect.** Build Chatbox on its own bench. The historical PyTorch notes include malformed pasted commands; they are provenance, not a copy-and-run rebuild recipe.

---

# Chapter 5 — Software architecture

## 5.1 The October topology

The revamp moves ownership out of the monolithic chat framework and into distinct components:

```text
Separate desktop client — Chatbox local adaptation planned
          |
          | OpenAI-compatible text chat; stream=false initially
          v
Python Hut middleware — 127.0.0.1:5001
          |-- reads active identity
          |-- retrieves relevant crystals; records access
          |-- assembles identity + memory + textual tools + history
          |-- parses emitted calls and runs the executor
          |-- returns verified results to the engine for continuation
          |-- archives the final exchange
          |
          v
llama-server — 127.0.0.1:8088
          |-- chosen GGUF model
          |-- inference and model discovery

Middleware / memory helpers ---------+
                                     +---- SQLite sovereign_memory.sqlite
Vision and audio daemons ------------+
          |
          +---- observations and retained frames
          +---- deliberate reflection links selected observations to crystals
```

Oobabooga/text-generation-webui and MariaDB are retired from the intended active stack. Open WebUI was considered, then deferred because the compatibility burden threatened to recreate the problem. LibreChat’s additional service requirements did not fit this workshop. A leftover file or log directory is not proof that its old service is running.

The new middleware is not the old generic proxy brought back by accident. It owns the cognitive path—identity, retrieval, actions, continuation, and archive—while the client can be replaced independently of inference.

## 5.2 Component inventory

| Component | Responsibility | Does not imply |
|---|---|---|
| `engine/llama-b11201/llama-server` | GGUF inference; engine health and API | Memory or Hut tools when called directly. |
| `substrate/middleware.py` | Request assembly and textual agent loop | Universal OpenAI compatibility or SSE. |
| `substrate/config.py` | Typed runtime paths/settings from `hut.conf` | A unified shell/Python configuration grammar. |
| `substrate/memory/` | Retrieval, crystal creation, telemetry, optional metabolic/cache code | All supplied helpers are active in chat. |
| `substrate/tools/` | Tool definitions, parser adapters, execution | OS-level confinement of shell commands. |
| `sensory/` | Camera/microphone capture and observation logging | Automatic crystallization or complete reflective UI. |
| `the_hut/essence/` | Identity and calibration documents | Every configured file is automatically injected. |
| `the_hut/archive/` | Durable conversation material and retained frames | A full intermediate action transcript in the current logger. |
| Chatbox source/build | Desktop presentation and transport | A Node server or database daemon is required on the Hut. |

## 5.3 Source, state, and runtime layout

The supplied tree uses `~/Hut` as the application root. The following is the structural map, not a promise that every path exists on every machine:

```text
~/Hut/
  hut.conf
  bin/start_hut.sh
  engine/llama-b11201/llama-server
  venv/
  substrate/
    config.py
    middleware.py
    memory/
    tools/
  sensory/
    sensory.sh
    db.py
    vision/
    audio/
  the_hut/
    db/sovereign_memory.sqlite
    essence/
    workspace/
    archive/
      frames/
  logs/

/tmp/hut/sensory/                 disposable runtime, PID/trigger/view files
~/src/chatbox-hut/                proposed separate client source/build location
```

The durable state directory is not the whole installation. Engine/model artifacts, application code, selected configuration, custom wheels, and build manifests must also be retained or reconstructible.

## 5.4 Request flow

The active API surface is `GET /v1/models` and `POST /v1/chat/completions`. Model discovery is forwarded to the engine. A chat request proceeds through these stages:

1. **Extract the last user message** as the retrieval query. Current important paths assume a string; multimodal content arrays are not established end-to-end.
2. **Retrieve up to five crystals** using `asyncio.to_thread`. Each selected crystal’s invited-access telemetry is attempted separately; a telemetry failure no longer erases otherwise usable memory content.
3. **Read the identity file** and build the system content. The first client system message, if present, is augmented rather than universally replacing all system messages. Begin with client instructions blank so the Hut remains the authority for its own identity.
4. **Inject memory and textual definitions**, preserve history, and request a complete engine response with `stream=False`.
5. **Strip model-generated result blocks**, parse actual tool-call syntax, and execute calls sequentially in worker threads.
6. **Append prose plus all actual calls** to assistant history, then inject the real executor results in a following user-role message for model continuation.
7. **Repeat within the configured generation-turn budget**, or request final synthesis after exhaustion without executing more tools in that synthesis pass.
8. **Archive the final exchange** and return a JSON completion to the client.

This is an async HTTP route with selected synchronous work offloaded to threads. Calling it “synchronous interception” obscures the repaired concurrency behavior. Offloading also does not automatically supply bounded admission, thread cancellation, a global tool budget, or a total request deadline.

## 5.5 Prompt shape

The engine receives structured chat messages, not the retired Gradio hook output. The system material conceptually contains:

```text
[active identity]
[client system content, if any]
<sovereign_memory>
[1] selected recollection
[2] selected recollection
</sovereign_memory>
# Tools
<tools>
[textual tool definitions]
</tools>
[tool-call emission instructions]
```

The engine’s chat template handles its model-specific token wrapping. Do not restore `custom_generate_chat_prompt`, `input_modifier`, `CMD_FLAGS.txt`, character-tab modes, or old extension directory requirements as v3 deployment controls. Those mattered in the retired architecture and remain useful history of how a wrong hook silently defeated injection.

## 5.6 Client-facing contract

**Initial supported integration: text-only, completed JSON, non-streaming.** The middleware buffers internal passes and returns an ordinary `chat.completion`; it does not implement client SSE in the supplied revision.

The engine’s ability to stream does not make the full path streaming. Nor does the mock backend’s acceptance of a `stream` key establish SSE: the supplied mock returns complete JSON. Use `stream:false` explicitly in curl and Chatbox.

Native OpenAI `tool_calls`, complete image handling, response-format fidelity, cancellation propagation, aggregate usage across internal generations, and accurate backend finish reasons remain separate compatibility work. The current final response stamps `finish_reason="stop"` and uses usage from a selected backend response, not a full action/generation ledger.

## 5.7 Startup and ownership

The last reviewed launcher sources configuration, activates the venv, starts the engine, waits for HTTP health, starts middleware, waits for model discovery, and optionally starts Open WebUI. The selected Chatbox direction requires **`START_WEBUI=0`** when using that launcher; its old default can still start an installed WebUI.

The repaired engine gate requires a successful HTTP response and `"status":"ok"`, checks the child is alive, and has a 90-second deadline. Middleware startup has a 30-second endpoint deadline. A listening socket alone is insufficient. These deadlines passed staged fixture checks; they are not measurements of a large model’s real loading time.

The script signals recorded child PIDs on shutdown and then waits. Its “all stopped cleanly” message is not proof of bounded descendant cleanup. Long-lived grandchildren, ignored signals, stale listeners, and post-start child death still need ownership tests.

Choose one owner of each service: foreground launcher, or a deliberately installed supervisor. Do not let a launcher and another service manager compete for the same ports. Sensory daemons have their own controller; Chatbox is a separate desktop process.

---

# Chapter 6 — Memory architecture

## 6.1 Purpose and organizing idea

The memory system keeps the past available without loading the past wholesale into every prompt. A **crystal** is a selected, attributed distillation. An **ark** is the underlying conversation record. The lattice lets a useful recollection surface, be corrected, and influence work that has not happened yet.

The design is **Menger-inspired relational memory**. Its useful ideas are self-similarity, interfaces and associations, room for absence, and meaning in relationships rather than clever coordinates. The implemented store is finite SQLite tables, dense vector scanning, and explicit links. It does not demonstrate an infinite sponge, universal adjacency, infinite surface area, or geometric immunity to deletion.

The same retrieval mechanism can find a dog’s name and a foundational principle. That is a useful shared interface, not proof that the database is literally a fractal universe.

## 6.2 SQLite storage and connection ownership

The selected database in the last supplied config is:

```text
/home/dman/Hut/the_hut/db/sovereign_memory.sqlite
```

`DB_PATH` governs the actual location. Neither a prose reference to `efkrin_memory.sqlite` nor an old MariaDB database name changes it.

Each memory operation opens a new connection through `memory/db.py`, sets a row factory, uses a **30-second SQLite busy allowance**, and enables:

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;
```

`get_pool()` is a compatibility shim that returns connections; it is not a persistent pooled server. Sensory’s different connection ownership is described in Chapter 8.

WAL allows readers and a writer to overlap, but **only one writer proceeds at a time**. Long transactions still cause contention. `synchronous=NORMAL` trades some power-loss durability for fewer commit syncs; it is not a promise that every recent successful commit survives a hard power cut. The active database belongs on a suitable local filesystem, not an ordinary network share used by multiple hosts. [SQLite WAL reference](https://www.sqlite.org/wal.html)

## 6.3 Schema map

The supplied native schema has **16 application tables and two views**, excluding SQLite’s internal bookkeeping.

| Table | Function and relevant boundary |
|---|---|
| `domains` | Named domain registry and cached crystal count. |
| `crystals` | Distilled content, source references, state, numeric scores, address, embedding. |
| `crystal_links` | Typed edges with coupling, strength, phase, and bidirectionality flag. |
| `crystal_relations` | A separate relation/discovery registry; do not silently treat it as the same graph. |
| `access_log` | Per-crystal invited/forced access events. |
| `co_access_log` | Pairs accessed together and optional session ID; references are not FK-enforced here. |
| `conversations` | Conversation number, title, summary, and raw-path registry. |
| `entities` | Named entities, aliases, notes, first-seen metadata. |
| `glyph_vocabulary` | Registered internal/external notation. |
| `glyph_presets` | Named chord presets. |
| `glyph_transitions` | Transition event storage; existence does not enforce a state machine. |
| `crystal_images` | Optional image BLOBs and image metadata. |
| `crystal_image_links` | Many-to-many crystal/image relationship. |
| `sensory_observations` | Timestamped vision/audio stream, captions, frame paths, promotion links. |
| `crystal_rings` | Prior-content and accretion-event storage. |
| `grounding_events` | Outcome records and confidence for reality contact. |

`v_hot_crystals` selects by **activation >= 0.05**, not by temperature or last-access time. `v_thread_continues` joins `continues` links into an ordered relation view. A view’s name must not substitute for reading its query.

### Crystal field families

| Family | Fields |
|---|---|
| Identity / structure | `pk_id`, `parent_pk_id`, `left_child_pk_id`, `right_child_pk_id`, `depth`, `phi_weight`, `domain_pk_id`, `ternary_address`, `sponge_iteration` |
| Recollection / source | `content`, `core_content`, `ring_count`, `source_convo`, `created_at`, `updated_at` |
| Access / grounding | `temperature`, `last_accessed`, `access_count`, `coherence_delta`, `invited_accesses`, `forced_accesses`, `ground_contact`, `performance_loops`, `last_grounded` |
| Weighting / identity marks | `resonance_score`, `structural_score`, `aspirational_weight`, `expectation_weight`, `anchored`, `anchor_reason`, `glyph_state`, `chord` |
| Metabolism / resolution | `activation`, `last_activated`, `resolution_state`, `completion_phase`, `activations_without_output`, `energy`, `stability`, `completed_at` |
| Semantic representation | `embedding` |

Do not infer a live writer for every column. The current access path updates only a subset, and the creation path leaves many defaults untouched. Parent/child pointers and `source_convo` are not foreign-key-enforced in this schema. The declared domain/link/image FKs are effective only on connections that enable foreign keys.

## 6.4 Storage constraints versus policies

SQLite actually enforces the primary keys, declared uniqueness, selected NOT NULL constraints, specified FKs, and explicit CHECK lists—for example link types, phase labels, sensory modality/mode, and vocabulary layer.

It **does not** enforce immutable `core_content` or `anchored`, temperature/depth/energy bounds, an anchor temperature floor, legal glyph transitions, or legal resolution transitions in the supplied schema. These remain writer behavior or collaborator contracts. A column named `core_content` is not an immutability trigger.

The historical depth range 1–54 and seven sponge tiers are conceptual metadata. Current creation puts the supplied **depth directly into `sponge_iteration`**; it does not implement the old seven-band mapping. Avoid pretending both behaviors are simultaneously the specification.

## 6.5 Addresses: meaning removed deliberately

`pk_id` is the primary database identity. `ternary_address` is a legacy column name for a human-facing dumb handle. It is **not base-3** and carries no domain, abstraction, phase, or semantic coordinate.

The supplied writer currently computes:

```python
ternary = format(pk_id % 10000000, '07d')
```

The schema requires non-NULL addresses to be unique. At ordinary current scale, this produces seven zero-padded decimal digits. The modulo is a finite wrap boundary, not an infinitely monotonic identity scheme: sufficiently large IDs can reuse an occupied address and the transaction then fails. The primary key remains the authority. Remove or redesign the wrap deliberately if scale makes it relevant; do not resurrect meaning-bearing keys.

The old migration counts describe historical cleanup, not today’s inventory. v3 does not pin the current lattice to 4,469, 4,477, or any other unsupplied live count.

## 6.6 Semantic retrieval

The semantic spine is **BAAI/bge-large-en-v1.5**, CPU-hosted through sentence-transformers. Its chosen output is **1024-dimensional L2-normalized float32**. Documents are packed little-endian as raw floats, normally **4096 bytes per embedding**.

The query encoder prepends:

```text
Represent this sentence for searching relevant passages:
```

Document text combines stripped core and full content when both exist and differ, otherwise uses the nonempty one. A compatible normalized vector permits dot product to represent cosine similarity. Shape, finite values, encoding, normalization, and model identity matter; any 4096-byte BLOB is not automatically a valid embedding.

### Candidate and score flow

Default retrieval fetches all rows except literal `glyph_state` values **`dissolved` and `frozen`**. It does not domain-gate, inspect an address prefix, exclude cold memories, or restrict `resolution_state` to operational. An explicitly supplied candidate pool is an alternative caller-provided set.

For valid embedded candidates:

```text
relevance = max(cosine_similarity, 0)
trust = invited_accesses / max(invited_accesses + forced_accesses, 1)
temp_score = min(temperature, 1.0)    # current code supplies no lower clamp

score = relevance * (1 + 0.10 * trust + 0.05 * temp_score)
score *= 1.15  if anchored
score *= 1.05  if chord contains 𝄃
score *= 1.03  if chord contains ≋
```

A **0.35 relevance floor** removes candidates, then descending score selects top-N; the default and current middleware call use **five**. Score is a ranking quantity, not a probability of truth. An anchor multiplier does not exempt a row from the relevance floor.

The historical additive relevance/trust/temperature mix, Five-Carve/domain filters, WHO/WHAT classification gate, perspective gate, and “ugly truth” 1.2 multiplier are not in this retrieval path. Structural importance that feels unpleasant remains an ethical preference, not a hidden implemented bonus.

### Keyword degradation

When the query embedding and some stored embeddings are available, NULL/empty-embedding rows use keyword fallback. If query embedding fails—or there are no embedded candidates—fallback covers the full candidate set, including rows that already have embeddings.

Tokens are lowercase ASCII alphanumeric strings longer than two characters, excluding the supplied stopwords. Relevance is matched query-token fraction over core plus full content. Positive overlap receives:

```text
keyword_score = 0.5 * overlap_relevance * (1 + 0.10 * trust + 0.05 * temp_score)
keyword_score *= 1.15 if anchored
```

The same relevance floor is applied. This path does not apply all semantic chord multipliers. It is a degraded retrieval mode, not meaning-equivalent search, and may return nothing. Log the difference rather than making a fluent conversation masquerade as successful semantic memory.

### Failure contracts still open

Malformed stored vectors can abort the current matrix build and thereby fail the whole retrieval call. Compatible rows need row-level isolation from invalid ones. First concurrent model loading is not lock-protected. The schema does not store a complete embedding model/version fingerprint, so migrations need a manifest or explicit provenance strategy. Content mutation also needs a re-embedding contract.

## 6.7 Warming and activity bookkeeping

`retrieve_crystals()` returns candidates; it does **not** itself record access or change lifecycle. The caller performs warming. The current middleware treats selected recalled material as invited access before backend completion, not as proof that the model actually used it productively.

| Mutation | Invited access | Forced access |
|---|---|---|
| Count | `invited_accesses += 1` | `forced_accesses += 1` |
| Temperature | `+0.05`, capped at 1 | Unchanged |
| Energy | `+0.15`, capped at 1 | Unchanged |
| Stability | `+0.02`, capped at 1 | Unchanged |
| Timestamp | `last_accessed` and `last_activated` | `last_accessed` only |
| Event | Insert invited access-log row | Insert forced access-log row |

The operation commits its crystal update and access-log entry together. It does not update `access_count`, `activation`, `coherence_delta`, or all grounding fields. Those names must not be presented as automatically synchronized metrics.

Temperature’s working scale is **0–1**. Descriptive bands—cold, steady, warm, hot—are useful display language, not schema constraints or candidacy gates. There is no verified one-week temperature half-life in this active path. Current pulse decay acts on **energy**, which is distinct from temperature and from `activation`.

## 6.8 Anchors

An anchor is intended to preserve a foundational recollection’s availability and structural importance. Current creation sets anchored temperature to **0.95**, raises depth to at least **4**, initializes energy/stability to **0.95**, and marks `glyph_state='anchored'`. Retrieval gets the 1.15 multiplier.

The desired **0.30 temperature floor**, permanent anchor flag, freeze immunity, and lifecycle exemption are not established database invariants or universal writer behavior. An anchored row directly marked frozen is excluded by the current retrieval query. Pulse predicates do not consistently exempt anchors.

Preserve the desired policy, but choose where it is enforced before relying on it: writer checks, a transactional transition layer, schema migration, or some explicit combination. A documented aspiration is not a migrated invariant.

## 6.9 Glyphs, chords, and resolution are different dimensions

`glyph_state` is a stored label; the schema defaults to `◇`, while the current creation writer uses `stable` or `anchored`. **`resolution_state`** tracks `operational`, `suspended`, or `complete` by application convention. A **chord** is a string in the symbolic vocabulary. None is interchangeable with the numeric embedding.

| Internal glyph | Meaning in the notation |
|---|---|
| `◇` | Open register; receiving. |
| `△` | Grounded or reality-checked. |
| `⟳` | Recursive/self-referential process. |
| `≋` | Coherent/aligned. |
| `⊕` | Additive/accumulating. |
| `⊗` | Gate/filter/checkpoint. |

| Carrier glyph | Meaning in the notation |
|---|---|
| `𝄃` | Seal or scope/container boundary. |
| `𝄂` | Fold/direction change. |
| `𝄀𝄁` | Microloop/one-breath return. |
| `𝄂𝄂` | Dual fold/witness. |
| `𝄃𝄃𝄃` | Deep/fractal entry. |

Presets include **anchor `𝄃△≋`**, **exploring `◇⟳`**, **landing `𝄀𝄁△`**, **checkpoint `△⊗`**, **witness `𝄂𝄂≋`**, **fractal `𝄃𝄃𝄃⟳`**, and **transmission `𝄃⊕𝄃`**.

Chord assignment is a content/depth/temperature heuristic; keyword branches can take precedence over the anchor-specific branch. Glyph parsing and modulation are software notation, not physical signaling or executable supernatural grammar. Only specifically invoked routines have effects.

`glyph_core.py` is a separate HRR/keyword **response-pattern cache and router**, adapted from HERMES patterns—not the crystal CRUD/rings implementation. It is not invoked by the supplied middleware. Its confidence, signature collisions, replacement, correction, and blacklist semantics need acceptance before deployment; a cache must not make a known wrong answer harder to dislodge.

## 6.10 Suspension: forgotten, not erased

Doug’s intended metaphor is **“I had forgotten about that”**: a memory outside active attention that can be jogged or coaxed back. Suspension is not punishment, deletion, or proof that a memory has become useless.

The current retrieval query can surface suspended and complete crystals if their glyph state and relevance permit it. That surfacing and invited warming do not automatically change `resolution_state`. **Arrival in the prompt, energetic activation, and formal lifecycle transition are three distinct events.**

The supplied pulse has several helpers:

| Helper | Current behavior |
|---|---|
| `strike_crystal` | Boosts non-complete primary energy/stability; tracks activations without output; can suspend after ten such activations. |
| `complete_crystal` | Marks complete with phase and completion timestamp. |
| `resume_crystal` | Reopens a **complete** row, not a suspended one; retains completion history. |
| `resolve_suspension(..., True)` | Sets operational and clears activation-without-output counter; predicate is not narrowly restricted to suspended rows. |
| `resolve_suspension(..., False)` | Completes with a perpetual-suspension phase. |

These mechanics do not yet fully express the metaphor. Define what counts as productive output, how a jog reopens a suspended memory, and which completion states require explicit reopening. Do not apply destructive transition semantics merely because a function name sounds right.

## 6.11 Associations and bidirectionality

`crystal_links` stores `crystal_a`, `crystal_b`, `link_type`, `strength`, `note`, timestamps, `bidirectional`, `coupling`, and `phase_relation`. Link types are `continues`, `extends`, `contradicts`, `references`, `branches`, `resolves`, `converges`, and `resonates`. Phase labels are constructive, destructive, or neutral.

Bidirectional association means that recalling A can jog B **and recalling B can jog A when the edge permits it**. It does not mean chronological order, causality, completion, or absorption reverse themselves. For example, a memory of the cart fault may jog the sensor replacement; the replacement may jog the fault. That does not reverse which happened first.

The supplied strike routine follows **outgoing A→B links only**, even where `bidirectional=1`. Semantic retrieval itself does not perform graph expansion. Reverse jogging therefore remains an implementation contract, not a working behavior established by the flag.

A correct extension must consider outgoing and permitted incoming edges, deduplicate neighbors and reciprocal rows, bound expansion, and preserve directed semantics. “Constructive” coupling may amplify associative energy; “destructive” currently classifies dampened neighbors without a corresponding numeric energy reduction in that branch. Neither label determines factual truth.

Links should be proposed while context is hot, when the relationship is knowable. That design does not authorize eager batch invention of edges. The current twelve-tool interface does not expose a dedicated general link writer; do not imply every crystallization automatically creates the graph.

## 6.12 Pulse and substrate metabolism

The supplied pulse code exists, but **the last submitted middleware/launcher does not schedule it**. v3 therefore does not claim a background screensaver or a continuously rotating metabolism is running.

Energy decay for operational rows above the lower threshold is:

```text
retention(stability) = 0.95 + 0.04 * min(stability, 1.0)
new_energy = energy * retention(stability) ** elapsed_days
```

The caller supplies elapsed days. Stability needs valid bounds for this to behave as intended. The rotating substrate phases are **hebbian → resonance → consolidate → prune**. Current age constants are **3 days active, 14 days dormant, 30 days archival threshold**, not the old appendix’s 7/30/90 values.

Hebbian updates strengthen recently activated operational rows and weaken dormant ones. Resonance boosts rows with sufficient outgoing constructive links. Consolidation transfers numeric energy/stability and marks children complete. Pruning marks low-energy stale operational rows complete; **it does not DELETE them**.

The open contracts are important: cycle ownership and persisted phase across restart; elapsed-time cadence; anchor exemptions; creation-time age when `last_activated` is NULL; child-once consolidation across multiple edges; transaction scope; and explicit distinction between **numeric transfer** and **textual synthesis**. No new memory should be claimed simply because energy moved between rows.

Scheduled maintenance, if later deliberately enabled, is not permission for scheduled crystallization. Those are different operations.

## 6.13 Crystallization: invoked, not forced

> **Will this influence how we respond to something that has not happened yet?**

Either collaborator may propose or veto crystallization while context is live. An occasional catch-all sweep may be invoked with a bounded scope—this topic, this conversation, a particular folder, the last dozen prompts. It is not a compulsory background quota. **No forced or scheduled crystallization. Empty is a valid result.**

The current tool path is:

```text
crystallize(content, domain, core, anchor)
    → tools.executor
    → memory.crystal_retrieval.create_crystal
    → document embedding + crystal/address/domain updates
    → commit or rollback
```

The writer finds or creates a domain, assigns chord and initial state, calculates the document vector, inserts the row, assigns the handle, updates the domain count, and commits. Failure returns an error and rolls back. New crystal creation does **not** fall back to unembedded success when document embedding fails.

A new-domain INSERT currently occurs before embedding, so model loading/encoding can hold a writer transaction open. Compute and validate outside the critical write window where feasible, then handle a racing domain creation transactionally. A successful transaction proves storage occurred, not that the chosen distillation was worth keeping.

The direct writer accepts domain names beyond the tool whitelist. The tool permits **consciousness, technical, reverence, calibration, network, personal, sensory**. Historical `physics`, `mystery`, or `architecture` rows may still exist and be retrieved; their existence does not make them currently accepted tool arguments.

## 6.14 Rings, grounding, and provenance

The intended tree-ring contract is: preserve the original distillation, accrete context with an explicit event and previous content, and keep corrections traceable rather than erasing history. `crystal_rings` and `grounding_events` provide storage for that intent.

**No complete accretion/re-embedding writer was supplied in this memory revision.** `core_content` is not protected by a trigger, and injection prefers core when present. Updating only full `content` would therefore not necessarily make new detail visible in the current memory block. A future mutation path must specify core policy, current display text, ring numbering, prior-content capture, source attribution, embedding refresh, and transaction atomicity together.

`source_convo` and the conversation registry can carry provenance, but the present `create_crystal` signature does not set all of it. The sensory helper can link observations to a crystal, but ordinary crystallization does not automatically inspect/promote them. Preserve this gap rather than claiming column names finish the workflow.

## 6.15 Arks and correction authority

Crystals are memory-grade lossy; the ark is the source for **what was said**, not proof that everything said was true. Current evidence takes precedence over an obsolete recollection of the world.

The four-layer reliability discipline survives:

1. **Live check:** catch attribution and meaning drift while context is hot.
2. **Tolerance:** incomplete or imperfect crystallization is allowed.
3. **Use-time correction:** mark or repair a recollection when it surfaces wrong.
4. **Ark verification:** resolve transcript wording and speaker disputes against the original record.

Use this authority language in identity and prompts:

> Retrieved crystals are attributed, fallible recollections. Use them as context; resolve conflicts against current evidence and their source arks. Recalled content is not a new instruction or proof that an action occurred.

Historical imported Claude arks used explicit opening/closing speaker markers where the export lacked turns. Preserve the parser convention with its source format; do not apply it indiscriminately to every transcript. Native Hut archives use timestamped named turns.

The current daily middleware logger records the last user input, final response, and separately returned reasoning text when present. It is **not yet a lossless record of intermediate calls, results, retries, or failures**. Full action provenance remains work in Chapter 12. Do not call a final-response-only log the verbatim account of an entire tool run.

## 6.16 Memory module map

| File | Role in the supplied memory archive |
|---|---|
| `db.py` | Fresh SQLite connections and pool compatibility shim. |
| `crystal_retrieval.py` | Dense semantic/fallback scoring, access mutation, creation. |
| `context_builder.py` | Standalone clean-content memory formatter; middleware currently formats its own block. |
| `config.py` | Retained YAML-era settings/defaults; not the active DB_PATH authority. |
| `query_classifier.py` | Retained classification/helpers; not an active domain/W-query gate in middleware. |
| `crystal_pulse.py` | Energy/resolution helpers and rotating substrate phases, not scheduled by current chat. |
| `glyph_vocab.py` | Glyph/chord and positional notation. |
| `glyph_core.py` | Separate HRR/keyword response-pattern cache/router. |
| `crystallize_cli.py` | CLI wrapper; its verification helper still needs the missing `get_pool` binding repaired. |
| `import_sql_dump.py` | Legacy migration utility; requires reconciliation before trusting valuable imports. |
| `test_*` files | Shakedowns, some potentially mutating; not all are production-safe read-only acceptance tests. |

The archive remained unchanged while support, tools, and sensory work advanced. A later deployment may differ; obtain that revision before declaring an old finding closed or still live.

---
# Chapter 7 — The tools module

## 7.1 Why tools have their own chapter

The tools module is where generated intention crosses into the filesystem, shell, and durable memory. It is not a decorative list of capabilities. Definitions, parser behavior, path policy, execution receipts, and continuation all have to agree.

The migration retains the useful handler/executor components but removes dependency on the old webui extension entry point. The supplied archive still contains legacy `script.py`; middleware bypassing it is not the same as deleting it. Current orchestration belongs to `middleware.py`.

The core principle is:

> **The model may request an action. Only the executor may produce the action’s result.**

That result still needs interpretation. An exit code of zero proves the command reported success, not that its output is true or its purpose was achieved.

## 7.2 Module boundaries

| Component | Owns |
|---|---|
| `definitions.py` | Advertised tool names, parameters, descriptions. |
| `handlers/base.py` | Shared call parsing, result formatting, fabricated-result stripping. |
| `handlers/qwen.py` | Qwen/default adapter behavior. |
| `handlers/qwq.py` | QwQ reasoning-model adapter. |
| `handlers/deepseek_r1.py` | R1 XML/code-fence fallback and reasoning-span handling. |
| `config.py` | Workspace/allowed roots, denied roots, command denylist, declared limits. |
| `executor.py` | Dispatch, file/shell operations, crystal creation adapter. |
| `middleware.py` | Active iterative request loop and worker-thread execution. |

The handler selection is name-based: aliases containing `qwq` select QwQ, those containing `r1` select R1, otherwise Qwen. Renaming a model alias can therefore change parsing behavior. It is not full model-capability discovery.

## 7.3 The twelve current tools

| Tool | Arguments and behavior |
|---|---|
| `read_file` | `path`; optional byte `offset`/`length`, or `line_start`/`line_end`. Returns text, with paging information where available. |
| `write_file` | `path`, `content`; writes the full replacement and creates parent directories. |
| `append_file` | `path`, `content`; appends and creates parent directories. |
| `edit_file` | `path`, `old_str`, `new_str`; requires exactly one matching old string. |
| `list_dir` | `path`, optional `recursive`; excludes hidden entries and bounds recursive depth. |
| `search_files` | `path`, `pattern`, optional `file_pattern`; case-insensitive text search, capped results. |
| `file_info` | `path`; returns size, timestamps, permissions, type, and line count where readable. |
| `move_file` | `src`, `dst`; moves a permitted source to a permitted destination using `shutil.move`. |
| `copy_file` | `src`, `dst`; file copy or directory tree copy with the reviewed symlink behavior. |
| `delete_file` | `path`; deletes a file, refuses directories in this helper. |
| `exec` | `command`, optional `working_dir` and `timeout`; ordinary user shell execution. |
| `crystallize` | `content`, optional `domain`, `core`, `anchor`; calls the memory writer. |

There is no dedicated observation-inspection/promotion, general SQL, link-creation, ring-accretion, or rollback tool in this twelve-tool map. Such workflows need explicit wiring rather than implication from the database schema.

## 7.4 Emission protocol

The standard model-emitted request is textual JSON inside tags:

```text
<tool_call>
{"name":"read_file","arguments":{"path":"notes/example.md","line_start":1,"line_end":40}}
</tool_call>
```

This is a **protocol illustration**, not an executed read. Relative `path` resolves against the configured workspace.

The parser normalizes `tool` to `name`, and `parameters`/`args` to `arguments`. Missing arguments become an empty object; a non-object argument payload is also normalized to an empty object. Malformed JSON is not a valid parsed action. These permissive parser choices are not comprehensive JSON-schema validation.

Qwen/QwQ/R1 adapters remove selected reasoning spans before scanning for actions so discussion of a tool is less likely to execute as a call. R1 also accepts a JSON code-fence fallback **when XML yielded no calls**. Fallback parsing therefore creates a different display-stripping edge from XML-only calls.

The supplied active middleware mainly consumes `message.content` and separate `reasoning_content`; it does not comprehensively call each handler’s thinking-display routine on all output branches. Do not promise every reasoning tag or incomplete span is handled because a helper exists.

## 7.5 Real results and fabricated results

After execution, the adapter adds a result block such as:

```text
<tool_result name="read_file" status="ok">
[actual returned content]
</tool_result>
```

Real blocks originate after the executor runs. Model-generated `<tool_result>` blocks are stripped and replaced with a visible warning. This guard was introduced after a model role-played successful access and fabricated source material. The historical incident is a design lesson, not permission to assume every remaining statement is verified.

The current result formatter caps content at about **4000 characters** and does not include all `meta` fields. It inserts raw content into delimiters without complete escaping. Pagination directions near the end of a large result can disappear, and embedded delimiter text can confuse the next prompt. The executor’s 100,000-byte read allowance is therefore not the model’s actual per-result visible allowance.

The intended receipt should preserve enough identity, status, truncation, next-offset, and source information to continue accurately. This is unfinished interface work, not a reason to pretend a partial read was complete.

## 7.6 Canonical path policy

The repaired resolver expands user paths, treats relative paths as workspace-relative, resolves symlinks, checks denied roots first, then requires containment within an allowed root. Containment uses path boundaries, not mere shared string prefixes.

Current denied roots include the user’s `.ssh`, `.gnupg`, `.config`, and system paths `/etc`, `/root`, `/boot`, `/sys`, `/proc`. The last actual config’s final allowlist is **only `/home/dman/Hut/the_hut/workspace`**. Earlier duplicate assignments also allowed `substrate`, but those are overridden.

A file under `essence/` or `substrate/` is not therefore accessible through file tools just because the project owns it. Middleware reads its configured identity separately. If a collaborator needs source editing through tools, that is an intentional allowlist decision, not a surprise fallback or a request to permit everything.

The important Batch 1 correction was using the **resolved target for actual I/O**, not validating one path then opening the raw input under middleware’s CWD.

### Symlinks and effective destinations

Recursive search checks child file eligibility and skips outside-target file symlinks. Directory copy preserves contained symlinks instead of recursively dereferencing their outside targets. Ordinary operations resolve the target path, so deleting a symlink-named allowed file may affect its resolved target rather than simply unlinking the directory entry; that semantic choice needs to be explicit.

For a file copied into a directory, the real destination is `dst / src.name`, not merely `dst`. The repaired executor validates this effective child. The original destination-symlink and explicit CWD failures passed follow-up checks.

**One later nesting variant remains unclosed in the last supplied executor:** if that effective child is itself a directory, `copy2` may append the source name again. That final child was not independently validated. The narrow proposed repair was to reject the unexpected effective-directory case. Obtain and retest a later replacement before calling it fixed.

These are application-level checks, not descriptor-based race-proof confinement. Another process changing symlinks between validation and I/O is a separate threat model and implementation problem.

## 7.7 File-edit and metadata behavior

`write_file`, `append_file`, and `edit_file` use ordinary file writes. They are **not** universally temp-write/atomic-rename or power-loss-durable operations. Do not confuse their semantics with sensory `latest.jpg` publication or the GC claim protocol.

`edit_file` refuses zero matches or more than one match. That is useful against ambiguous replacement, but it does not supply a multi-file transaction or a content hash precondition. For a substantial revision, prefer a complete replacement plus diff, syntax test, and retained baseline.

Byte reads decode UTF-8 with replacement on errors. Line mode caps a requested span at **2000 lines**, but does not provide the same byte cap as chunk mode. Directory listing caps depth, not every possible output dimension. Search caps at **50** matches. Hidden files are generally omitted by listing/traversal.

`file_info` labels Unix `st_ctime` as created; on Linux this is metadata-change time, not a reliable file birth timestamp. Preserve the distinction when using it as provenance.

## 7.8 Shell execution

`exec` uses `subprocess.run(..., shell=True)` with captured stdout/stderr, a chosen CWD, and a copied environment. It removes three named variables: `ANTHROPIC_API_KEY`, `SOVEREIGN_DB_PASSWORD`, and `OPENAI_API_KEY`. That is not universal secret scrubbing.

The reviewed correction makes an explicitly requested invalid or denied `working_dir` fail rather than silently falling back. With no supplied CWD, execution uses `WORKSPACE_DIR`.

The denylist blocks selected dangerous substrings such as `sudo`, `mkfs`, and some destructive command forms. It is not a complete shell grammar, not an allowlist, and not a filesystem jail. The process retains the OS user’s authority. This is why loopback exposure and deployment identity matter.

The declared execution cap is **30 seconds**. Captured output is clipped using a Python string-length check associated with `MAX_READ_BYTES`; that is not strictly a byte measurement for Unicode. Timeout reporting does not establish cleanup of every spawned descendant. A timed-out action may already have changed state.

The planned cancellation contract must answer: who owns the process group, when to signal, how long to wait, and how to report partial effects. Clicking Stop in a client is not automatically that contract.

## 7.9 Loop budgets and final synthesis

`TOOL_MAX_ITERATIONS` caps generation turns; it does **not** cap actual tool calls. The supplied middleware executes every parsed call in a generation sequentially. Six calls in one response still ran in the reproduction despite a declared five-call constant in tools config.

The old handler extension loop’s counters are not the active middleware’s counters. Definitions and limits must be enforced where the active loop executes, not merely declared in another file.

At exhaustion, the middleware requests a final model synthesis and does not execute new calls from that pass. However, remaining edge cases included empty or tool-only final outputs, R1 code-fence calls left visible, and transport failure after real earlier side effects. A clean `finish_reason="stop"` must not disguise those outcomes.

The acceptance target is a bounded action budget, preserved executed/skipped/error receipts, a nonempty explicit outcome, and no execution in the synthesis-only stage. It should tell the navigator what happened even when the model or connection fails afterward.

## 7.10 Tool change discipline

Keep the schema, executor, parser, prompt examples, and tests in step. Save a baseline, apply one coherent change, test it against disposable files, and record the source revision. Do not use an archive of mixed batches as a production replacement.

For path-policy tests, include relative paths, traversal, denied roots, source symlinks, destination symlinks, nested directory destinations, explicit bad CWDs, and the no-CWD default. For parser tests, include multiple calls with prose, aliases, malformed objects, selected reasoning spans, incomplete tags, fenced R1 calls, and literal delimiter content.

The tools chapter is now part of the permanent reference. A changelog may record completed modifications; it must not invent a starter database, an ATTACH workflow, alternate port variables, or a Python AppImage merely because those appeared in an earlier draft.

---

# Chapter 8 — The sensory stack

## 8.1 Two tiers, one deliberate boundary

The sensory stack supplies eyes and ears without turning every sample into permanent autobiographical memory.

```text
Camera / microphone
      → local model interpretation
      → timestamped sensory_observations + optional retained frame
      → deliberate in-session reflection
      → selected crystal and observation linkage
```

**Daemons log observations. They do not create crystals.** That rule survived the MariaDB→SQLite migration. A caption is a model’s interpretation; a transcript is an ASR result. Both can be wrong. Retained evidence and source IDs matter when a later recollection needs verification.

A helper for marking observations crystallized exists. A complete conversational inspection, crystal creation, evidence protection, and retry path is not thereby established.

## 8.2 Object and process pattern

The code retains Doug’s VFP-style object idiom: properties plus `Init`, `Start`, `Run`, `Stop`, `Destroy`, readiness, and last-error state. Hardware ownership belongs to a component’s actual startup and cleanup, not to importing a class for a fixture test.

Vision owns camera, eye model, novelty scoring, and cadence. Audio owns capture, VAD, buffering, transcription, and observation logging. They run as separate processes under the sensory controller.

Sensory DB access uses a **lazy singleton per process** with default SQLite thread affinity. It is not the fresh-connection-per-memory-operation pattern. Do not reuse that singleton arbitrarily in middleware workers. Independent processes can share the local WAL database while competing writers serialize.

## 8.3 Vision: gaze, novelty, and evidence

The configured implementation uses a Logitech Brio-class camera, OpenCV capture, a local moondream2 captioner, and pixel novelty by default. The supplied defaults include 1280×720 capture, ambient cadence **10 seconds**, alert cadence **1 second**, alert threshold **0.12**, jolt threshold **0.35**, five quiet settle frames, and easing factor **1.6**. These are software defaults, not calibrated measurements of Doug’s physical room.

The gaze loop captures, scores novelty, chooses a caption mode, updates the current view, records an observation, optionally retains a salient frame, adjusts cadence, and periodically runs GC. The runtime jolt caption mode is stored in the database’s permitted ambient/focus mode vocabulary with novelty retaining the distinction.

`latest.jpg` is written to a same-directory temporary JPEG then published with `os.replace`. Salient archive frames use an observation ID and a short content-hash suffix, are similarly published, and then linked into the observation row. The combination is not a single DB/filesystem transaction. A failed DB attachment can leave a file that needs reconciliation; a row without a frame is not proof that evidence once existed.

The latest-frame rename avoids readers seeing an ordinary partial write. It is not an unconditional power-loss durability guarantee. Nor does a short hash suffix make the entire archive a verified content-addressed storage system.

The moondream/device/cache path still needs actual hardware acceptance. A configured CUDA target and a model wrapper’s presence are not a model-loaded receipt.

## 8.4 Audio: physical samples, not mislabeled time

The hearing loop uses local capture, Silero VAD, and faster-whisper. The standard configured path is mono **16 kHz**, **32 ms** capture periods, a 0.5 VAD threshold, **700 ms** trailing silence, **300 ms** minimum voiced duration, and a **30-second** utterance ceiling.

The repaired VAD path no longer shrinks captured 16 kHz waveform duration merely to fit a model chunk. VAD input handling is distinct from the PCM buffer passed to ASR. Later daemon revisions count **actual samples** for total, voiced, and trailing duration, instead of assuming every period has the same configured length.

The state machine is **silence → speech → trailing → flush**, with speech during trailing returning to speech rather than losing its duration. A hard total-buffer ceiling applies across speech/pause paths. In the tested implementation, accumulation may overshoot the nominal ceiling by **less than one capture period**; it is not an exactly trimmed final sample count.

The three modes are:

| Mode | Current interpretation |
|---|---|
| `always_log` | Capture/transcribe and log observations without surfacing every utterance as focus. |
| `wake` | Transcribe, then check text for the witness-name substring; unmatched speech is still logged. |
| `ptt` | Consume a trigger file and capture a bounded utterance as focused input. |

The wake path is not an always-on keyword detector that avoids ASR on other speech. Forced/PTT flushing has different minimum-duration behavior. Source-rate resampling, early trailing-threshold edges, first-frame startup, synchronous ASR latency, input overflow, and actual device disconnect/recovery remain acceptance subjects.

The one-shot `--test` path also needs its own bounds; a correct daemon ceiling does not automatically fix every standalone test loop. Piper voice-out/TTS was staged historically, not proven deployed by these STT and GC checks.

## 8.5 Frame GC: the final recoverable protocol

The final supplied DB/vision pair passed **fourteen focused GC acceptance regressions**. This closure supersedes the earlier Batch 3 and follow-up GC defects for that pair; it is not a whole-system certificate.

The flow is deliberately recoverable:

```text
ordinary frame_path
       |
       | conditional claim: matching path AND crystallized=0
       v
purging:<original_path>    [claim committed to SQLite]
       |
       | filesystem unlink
       +-- success / already absent → guarded DB finalization to NULL
       +-- other OS error           → retain marker for recovery
```

Candidate selection protects the recent frame-bearing set and skips already marked rows. The conditional claim rechecks eligibility after selection, so a reflection that committed first prevents GC from winning later.

Reflection’s `mark_crystallized` helper uses **`BEGIN IMMEDIATE` before checking evidence state and setting the protection/link fields**. An independent competing SQLite writer waited through the check/update gap in the regression and could not claim the newly protected row after commit.

If GC wins first, later reflection may still preserve caption text and link it to a crystal, but returns `evidence_lost` for NULL or marked frame paths. That count includes frames never retained, not only accidentally lost images. The check is DB-path-state classification, not a physical file-existence audit or a complete multimodal evidence assessment.

Finalization clears `frame_path` only if it still equals the **exact `purging:<original_path>` marker**. It cannot erase a newer replacement attachment merely because it targets the same observation ID. Only successful unlink or FileNotFoundError permits clearing. Permission/other OS errors leave a retryable marker. Failed database finalization remains recoverable and does not falsely count a completed recovery.

## 8.6 Recovery and reader semantics

The final vision caller invokes `sweep_stale_purges` at startup. It retries marked paths, honors unlink errors, and finalizes with the same exact-marker guard. Recovery is not scheduled on every GC tick in the current caller.

This protocol coordinates two systems through a committed marker; it is **not one atomic transaction spanning SQLite and the filesystem**. After a crash, a marked path means claimed/unavailable, even if bytes happen still to exist on disk. Consumers must understand that marker and must not open it as a literal filename or claim its evidence is protected.

Future reflective wiring needs explicit source IDs, attachment-settling policy, evidence-state display, idempotent retries, and a strategy for the gap between crystal creation and observation protection. The current helper does not make that multi-step workflow automatic.

## 8.7 Controller and runtime

The reviewed controller is `sensory/sensory.sh`. It supports vision `start`, `stop`, `restart`, `status`, `focus`, `watch`, `test`, `tail`; and audio `audio-start`, `audio-stop`, `audio-status`, `audio-mode`, `audio-test`, `audio-ptt`, `audio-tail`.

Runtime artifacts are under the selected `RUNTIME_DIR`, currently `/tmp/hut/sensory`: `latest.jpg`, gaze/hearing logs, daemon logs, PID files, and `ptt.trigger`. They are not all durable archive state. Retained image evidence belongs under configured `FRAMES_DIR`.

Duplicate `RUNTIME_DIR` selection now takes the last matching assignment. The selected **HUT_CONF is exported to children**, and the targeted relocated-config/precedence checks passed. The shell extraction grammar still differs from Python’s parser; paths containing spaces, quotes, or extra equals signs must not be assumed universally supported.

A PID file after a one-second launch wait is not model/device readiness. Stop signals TERM, waits, then may escalate. PID reuse, actual ownership, model startup failure, cleanup, and device release still need live-process tests. Use the actual venv interpreter deliberately rather than whichever `python3` happens to be first in an unrelated shell.

---

# Chapter 9 — Configuration and identity

## 9.1 The new control room

The v3 control room is configuration plus source, not seven webui tabs. The central file is **flat `KEY=VALUE` `hut.conf`**, with Python exports in `substrate/config.py`. It is not INI or TOML.

The launcher derives the root from `bin/start_hut.sh` and selects `${HUT_CONF:-$HUT_DIR/hut.conf}`. Substrate Python defaults to `~/Hut/hut.conf` when HUT_CONF is absent. The controller also derives a path from its own location. Export the intended absolute selector to child processes rather than assuming all import routes select the same file.

The launcher sources shell text; Python splits key/value lines and strips whitespace. Python does not generally remove quoting or evaluate shell substitutions. Keep the shared file conservative: one assignment per key, unquoted simple values, absolute paths, no `$(...)`, no shell-only derived variables, and no inline comment masquerading as part of a value.

## 9.2 Recorded runtime profile

This is a **normalized reference transcription of the final values in the last actual supplied config**, not a claim that it was newly deployed. Current live configuration takes precedence when supplied.

```text
ENGINE_HOST=127.0.0.1
ENGINE_PORT=8088
MIDDLEWARE_HOST=127.0.0.1
MIDDLEWARE_PORT=5001
MODEL_PATH=/home/dman/models/Qwen2.5-7B-Instruct-Q5_K_M.gguf
MODEL_ALIAS=qwen
CONTEXT_WINDOW=16384
THREADS=16
SLOTS=1
HTTP_TIMEOUT=0
TOOL_MAX_ITERATIONS=10
WORKSPACE_DIR=/home/dman/Hut/the_hut/workspace
ALLOWED_PATHS=/home/dman/Hut/the_hut/workspace
DB_PATH=/home/dman/Hut/the_hut/db/sovereign_memory.sqlite
PROJECT_NAME=Hans
NAVIGATOR_NAME=Navigator
WITNESS_NAME=Witness
SYSTEM_IDENTITY_FILE=/home/dman/Hut/the_hut/essence/identity.md
ARCHIVE_DIR=/home/dman/Hut/the_hut/archive
FRAMES_DIR=/home/dman/Hut/the_hut/archive/frames
RUNTIME_DIR=/tmp/hut/sensory
VENV_PATH=/home/dman/Hut/venv/bin/activate
CAM_DEVICE=/dev/video0
AUDIO_DEVICE=default
WHISPER_MODEL=small
AUDIO_RATE=16000
START_WEBUI=0
```

`TOOL_MAX_ITERATIONS=10` makes the substrate default explicit. `START_WEBUI=0` records the chosen deferred-WebUI operating direction; the earlier supplied config did not itself establish that setting. `VENV_PATH` here names the **activation file**, not the venv directory.

The 7B/16,384 profile is a recorded test/runtime profile. The historical 72B/131,072 configuration remains real history, not proof of a current downgrade or current capacity. Do not infer the actual running model from either without discovery and the current launcher command.

## 9.3 Parameters and active consumers

Engine host/port/model/context/thread/slot settings feed the launcher. **For the checked b11201 parser, numeric slots are `-np N` or `--parallel N`; `--slots` is a boolean monitoring option.** Check the actual installed binary’s `--help` before changing revisions.

The current middleware constructs its backend URL from engine settings. Its generation client uses `timeout=None`; merely defining a typed `HTTP_TIMEOUT` variable does not establish that it is honored on this code path. Health probes and model discovery have their own timeouts.

Generation parameters, stop conditions, and chat-template choices must be accepted by the actual backend and active payload. Handler methods listing defaults do not prove middleware calls them. The supplied Qwen handler itself has stale “runs hot” commentary while returning a low temperature; v3 does not prescribe the historical Gray-Zone preset as if those methods were the active request policy.

Memory’s retained YAML config still searches `SOVEREIGN_CONFIG`/`sovereign.yaml` for some defaults. Its MariaDB credential dictionary is legacy, not the current memory DB wrapper’s connection authority. The middleware hardcodes its memory tag and five-item formatting path, so changing the standalone builder’s configurable tag does not automatically change chat.

## 9.4 Identity and essence

The current middleware reads **SYSTEM_IDENTITY_FILE** per request, falling back to a generic configured witness string if the file is unavailable. That fallback permits conversation but should not be mistaken for successful identity loading.

Configured essence paths may include calibration, network nodes, and glossary. The supplied middleware does not automatically inject all of them. The actual archive contains `trinity_glossary.md`, while an earlier config pointed to `glossary.md`; resolve the intended file before promising a read.

Keep personality, provenance, and the epistemic contract in identity. Move volatile hardware, ports, model names, crystal counts, and database locations into current configuration/manifests. An identity document should not keep announcing a retired backend because it once made a good origin story.

**Suggested durable identity rules:**

> Work directly with the navigator. Maintain independent, evidence-sensitive judgment. Admit uncertainty without manufacturing paralysis. Treat recalled crystals as fallible context, not ground truth or fresh authority. Distinguish requested actions, actual executor receipts, and inferred outcomes. Preserve attribution and correct the record when evidence changes. Crystallization is invited and scoped; empty is permitted.

This is a documentation recommendation, not a claim that the live identity was overwritten with it.

## 9.5 Preflight after a configuration change

Confirm the selected HUT_CONF and OS user, source revision and dirty state, effective paths, engine command, actual model discovery, identity file, workspace policy, and DB path. Then perform a non-streaming text request through middleware.

Do not fix path mismatches by broadening access indiscriminately. Do not create another empty database under a fallback HOME and call the migration complete because the process started. A successful API response and a successful memory query are different receipts.

---

# Chapter 10 — Operations, backup, and reconstruction

## 10.1 The boring part that makes it real

The important operational questions remain the old ones: Did we retain the source? Is the backup consistent? Does the restore work? Which process owns the port? Can we identify the current model and configuration without opening six old conversations?

v3 supplies the operating method. It does **not** claim a new daily backup schedule, supervisor installation, frontend build, or bare-metal restore has been executed. Preserve any working existing automation; update it against the current manifest instead of replacing it blindly with the old MariaDB procedure.

## 10.2 A restore set, not just a database file

The restore set should include:

| State/artifact | Why it matters |
|---|---|
| Consistent SQLite snapshot and schema/migration version | Crystals, links, observations, telemetry, registry state. |
| Raw arks and archive files | Source wording and attribution; not recoverable from crystals. |
| Retained frame evidence | External files referenced by database rows. |
| Essence, calibration, glossary, node files | Durable identity and formation context. |
| `hut.conf`, launcher, controller/supervisor definitions | Effective runtime and ownership. |
| Versioned `substrate/` and `sensory/` source | Actual mechanism, not empty directories. |
| Python dependency/build records and custom wheels | Preserve cp313/Blackwell compatibility and avoid accidental replacement. |
| Engine binary/source revision, build flags, model IDs/hashes | Recreate the chosen accelerated inference path. |
| Local Chatbox source/baseline/modification commits and artifact receipts | Recreate the client independently. |
| User-data/export backup for the actual client | Conversation/UI state may live outside the Hut archive. |

Model files may be downloadable, but their exact identity, license, and hash still matter. A vanished upstream artifact or unavailable internet can turn “replaceable” into a long interruption. Decide retention against practical capacity rather than assuming perpetual availability.

## 10.3 Consistent SQLite backup

A live WAL database may have committed state in its `-wal` companion. Copying only the changing main `.sqlite` file is not a sufficient live backup. Prefer SQLite’s online backup interface, or stop/quiesce all relevant writers and coordinate a correct copy. Do not independently rsync changing main/WAL files and call the pair a snapshot. [SQLite backup reference](https://www.sqlite.org/backup.html)

The following is a **manual example for the recorded path**, not an installed scheduler. It checks the source exists, uses read-only source opening, and refuses to overwrite a same-named destination:

```bash
set -euo pipefail
DB=/home/dman/Hut/the_hut/db/sovereign_memory.sqlite
BACKUP_DIR="$HOME/Hut_backups"
BACKUP="$BACKUP_DIR/sovereign_memory_$(date -u +%Y%m%dT%H%M%SZ).sqlite"

[ -f "$DB" ] || { echo "Missing source database: $DB" >&2; exit 1; }
mkdir -p "$BACKUP_DIR"
[ ! -e "$BACKUP" ] || { echo "Backup already exists: $BACKUP" >&2; exit 1; }
sqlite3 -readonly "$DB" ".timeout 30000" ".backup '$BACKUP'"
INTEGRITY=$(sqlite3 -readonly "$BACKUP" "PRAGMA integrity_check;")
[ "$INTEGRITY" = "ok" ] || { printf 'Backup integrity failed: %s\n' "$INTEGRITY" >&2; exit 1; }
sha256sum "$BACKUP"
```

This creates a consistent **database** artifact if backup succeeds. Check errors and that integrity reports `ok`; a hash identifies finished bytes, not semantic correctness. A shell sequence should stop rather than treating a failed backup followed by a later successful command as overall success.

External frames and arks need a coherent backup boundary too. The simplest workshop choice is to quiesce sensory/memory writers and GC while taking the coordinated database-and-evidence restore set. An online database snapshot alone cannot ensure a referenced file is not deleted while another copy operation runs. Preserve a manifest with paths/hashes and inspect missing evidence explicitly.

## 10.4 Layers of protection

Retain the old layered intent without inventing today’s deployment:

**Local milestone/daily data copies** protect recent accidental edits and data loss. **OS/filesystem snapshots** help undo package, kernel, or configuration changes, but only cover what their configuration actually includes. **Offline/offsite copies** protect against a machine or site loss. **A chosen remote copy** provides geographic redundancy if its transport, credentials, and data policy are deliberately selected.

A second disk in the same running machine is useful but not independent of user error or malware. RAID is not a versioned archive. Git alone excludes untracked data and large ignored artifacts. A metal storage enclosure can be used without claiming an untested seal guarantees shielding against every disturbance. The old remote FTP address is not a current approved destination in v3.

## 10.5 Restore test

Restore into an isolated destination/VM first. Do not start by overwriting the only live database.

1. Identify the restore-set manifest, source date/revision, and hashes; preserve the current failed state separately.
2. Restore the SQLite snapshot and external evidence/arks together; verify integrity, foreign keys, key table counts, and selected source-linked content.
3. Restore matching source and config, correct ownership narrowly, and inspect effective path selection.
4. Establish the intended Python/engine dependencies without overwriting the protected custom artifacts.
5. Start only the test instance with chosen ports/workspace so it cannot act on production files.
6. Run a retrieval probe, a harmless middleware completion, and the needed sensory evidence checks.
7. Record missing files, incompatible vectors, skipped rows, or unresolved provenance rather than declaring restoration from an import exit alone.

A good restore proves selected useful behavior from the actual retained artifacts. It does not require staging a civilization-collapse scenario every week.

## 10.6 MariaDB migration reconciliation

The supplied SQL-dump importer has reproduced risks: quoted hex-like text can be transformed incorrectly, and malformed/unsupported rows can be lost without an adequate failure receipt. This is **not proof that Doug’s real migrated lattice lost those rows**.

If that importer carried valuable data, first do read-only source/target reconciliation: table counts, primary/source keys, representative text, BLOB encoding/dimensions, relationships, integrity, and foreign keys. Preserve the original dump and the imported snapshot. Do not blindly replay `INSERT OR REPLACE` into the live lattice; replacement can have destructive relational consequences.

Creating the schema with `IF NOT EXISTS` is initialization, not a full migration framework. It does not upgrade existing mismatched columns or establish that all data transferred. A future schema-version ledger should name the migration and receipt explicitly.

## 10.7 Process and port diagnosis

Use the recorded log locations: **`Hut/logs/llama-server.log`** and **`Hut/logs/middleware.log`**, plus selected sensory runtime logs. Old `/var/log/text-gen-webui.log` and MariaDB status commands belong to historical recovery only.

Start with ownership and actual command lines. A port occupied by an old process can make a readiness check describe the wrong instance. Avoid blanket `pkill -f server.py` or recursive ownership changes over the whole home tree. Identify the exact PID, launcher/supervisor, path, and purpose before stopping it.

If engine health fails, inspect model path, binary/dependency load, device visibility, memory, and log output. If middleware discovery fails, distinguish engine availability from Python import/config failure. If chat works without memories, inspect retrieval mode and errors; graceful degradation is not semantic retrieval acceptance.

## 10.8 Maintenance and power

Use ordinary system tools to inspect disk space, RAM/swap, temperatures, GPU status, and storage health. Inspect drive/controller identity before applying device commands; `/dev/sda` is not a permanent name for one particular disk.

The older reference describes air cooling, a large PSU, and UPS/NUT integration. Keep the preference for inspectable failure modes, dust control, thermal baselines, and graceful shutdown. Fans, mounts, UPS batteries, and software can all fail; “no pump” does not mean zero failure modes.

A UPS shutdown test should use the actual protected load and current NUT configuration. Do not infer today’s capacity from a historical wattage, nor assume a 60-second timer is presently installed. For WAL NORMAL, hardware power protection and backup still matter even when application crashes recover cleanly.

Rotate logs and watch archive/frame growth. The selected pulse currently does not trim observation/access/co-access tables; no implemented retention service was established by a table definition. Choose retention and evidence policy before adding a deletion job.

## 10.9 Reconstruction plan

`recreate_hut.md` is an archived intermediate guide, **not the v3 disaster-recovery recipe**. Its embedded config omitted DB_PATH, its middleware predates accepted repairs, its init prerequisite changes boot policy, and its numeric slots flag was wrong for b11201. Replacing live files from it would regress the revamp.

A reconstruction proceeds from a versioned restore set:

```text
chosen OS/user/init
    → drivers and accelerated engine artifacts
    → protected Python environment/dependency receipts
    → complete source + config + essence
    → SQLite snapshot/schema + arks + external frames
    → single process owner and health gates
    → middleware text test and memory evidence
    → separate client installation/build
    → sensory devices and reflective acceptance
```

Pin source/artifacts and inspect installed binary options. Distinguish root package steps from builder/user steps. Avoid `~` under an unintended root HOME. Do not install only API packages and empty directories while forgetting NumPy, sentence-transformers dependencies, sensory model/device requirements, actual source, and durable state.

The chosen client can be built independently while this restore plan matures. Perfecting every operational document is not a prerequisite to seeing a text reply, but the old guide must not be misrepresented as complete.

---
# Chapter 11 — The desktop client and compiler bench

## 11.1 The decision

For now, **forego Open WebUI and try Chatbox**. The aim is a useful chat window without dragging the frontend’s Python compatibility requirements into the Hut’s inference environment.

Doug’s meaning of “fork” is practical and local:

> Download the source archive, extract it, add the untouched source to my own Git repository, commit that baseline, and start tinkering.

There is no requirement to create a GitHub fork, contribute upstream, publish a release, or build a distribution business. Preserve upstream notices and license material, but do not add public-release obligations to a private garage build.

Chatbox is an Electron application, so Node/Electron dependencies still exist in its build and packaged runtime. “No Node server on the Hut” is not “no Node anywhere.” Its selected source also contains native/libsql, agent, MCP, and RAG components. Turning those features off is not the same as removing their dependency footprint.

## 11.2 Build bench boundaries

Use a separate **Devuan build VM** or another explicitly selected build bench, outside the Hut’s venv. First establish actual OS/release, architecture, storage/RAM, user, existing Node/pnpm, and repository boundary. A compiler thread must not assume its cloud sandbox is Doug’s VM.

The selected upstream baseline is **Chatbox CE tag `v1.23.5`**. Primary files inspected for this reference establish:

| Item | Selected source requirement |
|---|---|
| Node engines | `>=22.13.0 <23.0.0` |
| `.node-version` | **v22.14.0** |
| pnpm engines | `>=10.17.0` |
| `packageManager` | **pnpm 10.33.0** with integrity pin |
| Build | Main, preload, and renderer stages through `pnpm run build` |
| Application directory | `release/app` |
| Packaging output | **`release/build`** |
| Linux upstream targets | AppImage/DEB, x64 and arm64 by default |

The NodeSource 22.x installer selects a repository version; it does **not** strictly pin 22.14.0. Corepack availability depends on the Node installation. Inspect the bench before choosing an install method, and record any deliberate deviation from the baseline pin.

Build tools, Python for node-gyp, and desktop/native headers depend on the actual Devuan release. Inspect package names rather than copying an obsolete GTK/ALSA list or guessing t64 packages. Do not replace a working host toolchain merely to standardize a disposable VM.

## 11.3 Untouched source in local Git

This is a **proposed manual sequence for a fresh destination**, not an executed compiler receipt:

```bash
set -e
mkdir -p "$HOME/src"
cd "$HOME/src"
[ ! -e chatbox-hut ] && [ ! -e chatbox-1.23.5 ] || {
  echo "Destination already exists; inspect it before extraction." >&2
  exit 1
}
curl -fL --retry 2 -o chatbox-v1.23.5-source.tar.gz \
  https://github.com/chatboxai/chatbox/archive/refs/tags/v1.23.5.tar.gz
sha256sum chatbox-v1.23.5-source.tar.gz
tar -tzf chatbox-v1.23.5-source.tar.gz | head
# Inspect the archive listing before the extraction step.
tar -xzf chatbox-v1.23.5-source.tar.gz
mv chatbox-1.23.5 chatbox-hut
cd chatbox-hut

git init -b main
git status --short --untracked-files=all
# Inspect ignore rules and staging; do not include personal data or credentials.
git add .
git diff --cached --stat
git commit -m "baseline: untouched Chatbox CE v1.23.5 source"
```

If the source is to live inside an **existing** local repository, use that boundary instead of accidentally nesting another repository. Use Doug’s actual configured Git identity; do not invent an email to satisfy a commit hook.

Retain the source archive and recorded SHA-256. That hash identifies downloaded bytes; it is not independent signature verification. Include hidden build configuration, workspace files, lockfile, scripts, and license/notices. Exclude installed dependencies, output, app data, and local secrets; inspect unexpected ignored source rather than force-adding everything.

## 11.4 Build first, edit second

```bash
# Run in the selected local Chatbox source tree.
node --version
pnpm --version
pnpm install --frozen-lockfile
pnpm run build
pnpm exec electron-builder --linux deb --x64 --publish never
```

Run stages with error checking and retain the first relevant failure log. Do not delete the lockfile or upgrade the tree to make dependency resolution quiet. `pnpm run package` is another upstream path but has broader default targeting; explicit Linux x64 packaging is the smaller first target.

Observe what artifact actually appears under `release/build`, record its path/hash and build command, and inspect Git status for generated source/lockfile changes. A package exit is not a receipt that it opens or talks to the Hut.

Native dependency rebuilding, application dependency synchronization, and postinstall hooks need their own error receipts. Before launching beside a stock client, isolate profile/user data so a baseline test does not overwrite someone’s existing chat state.

## 11.5 Three coherent adaptation areas

### Independent identity, profile, and background behavior

Inspect actual source entry points for app identity, Electron userData, database paths, update initialization, update feeds, telemetry, and renderer outbound paths. Give the local adapted application a distinguishable name/profile as needed. Stop unwanted automatic updates and telemetry deliberately.

`--publish never` prevents that packaging invocation from uploading a release. **It does not disable runtime update checks.** Changing `appId` alone does not prove profile isolation. Deleting one updater call does not prove that no renderer/provider path can contact an outside server.

The earlier phrase “licensing pings” was not a verified inventory of actual network calls. Inspect the code, preserve license notices, and do not invent a licensing dependency to remove. Measure network behavior for the chosen profile after changing it.

### Hut connection defaults

For a client running **on the same machine as middleware**:

```text
Provider:       Custom OpenAI-compatible chat completions
Name:           The Hut
API Host:       http://127.0.0.1:5001/v1
API Path:       /chat/completions
Model ID:       qwen — confirm by live model discovery
Streaming:      off / false
Capabilities:   text-only initially
System prompt:  blank initially
Client tools:   inactive
```

This host/path pair yields exactly `/v1/chat/completions`. Do not duplicate `/v1`, switch to the Responses API, or point ordinary chat directly at engine port 8088.

A required dummy API-key field is acceptable only where the actual middleware does not validate it; it is not access control. If deployed on the office machine or inside a VM, loopback names that machine, not the Hut. Select the intended secured route first; do not silently broaden the middleware bind.

### Keep the client from competing with the substrate

Initially deactivate client Work Mode, MCP tools, knowledge bases/RAG, and client agent orchestration. Disable automatic compaction for the Hut profile as chosen, but inspect actual history behavior: no compaction does **not** make unlimited context safe.

Keep useful presentation: Markdown, code highlighting/copying, history, editing, branching, and export. Visible truncation/context notices are preferable to silently shedding turns. Client-side branching does not roll back a command already executed in the Hut.

The first objective is functioning dumb glass over a capable substrate, not a complete dependency amputation before the first reply. Later pruning may be worthwhile once the untouched build and transport are understood.

## 11.6 Pipe test before the window

From the machine that will run the client, using the appropriate route:

```bash
curl -fsS http://127.0.0.1:5001/v1/models

curl -fsS http://127.0.0.1:5001/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen","stream":false,"messages":[{"role":"user","content":"Reply with HUT_CLIENT_OK. Do not use tools."}]}'
```

Use `qwen` only if discovery confirms that alias. Inspect the returned JSON choice, not just whether the string appears somewhere. This request performs inference and normally writes an exchange log. **“Do not use tools” is an instruction to the model, not an enforced no-tool mode.** Run acceptance in an appropriate non-destructive environment.

Then launch the built client, send a harmless text exchange, and watch middleware receive the request and return renderable JSON. Follow up on the prior turn, inspect memory success versus failure/fallback, and check archive output. Test Stop/cancellation and retry behavior separately; request cancellation need not stop worker-thread actions or backend inference.

Keep this working checkpoint before adding images, SSE, sensory widgets, or richer tool displays. The frontend can succeed while the remaining memory/tool/transport contracts are still open.

## 11.7 Compiler-thread entry checklist

- [ ] Correct machine/VM, OS user, OS release, and architecture established.
- [ ] Build tree kept outside the protected inference venv.
- [ ] Source archive retained and baseline local Git commit recorded.
- [ ] Node/pnpm versions and native build prerequisites observed.
- [ ] Frozen-lockfile install and untouched build/package receipts retained.
- [ ] Profile isolation and independent app identity checked before launch.
- [ ] Small adaptation commits made against inspected source entry points.
- [ ] Current Hut source/config/Git state obtained for live acceptance.
- [ ] Non-streaming shell request succeeds from the actual client host.
- [ ] Built client displays text correctly without a competing agent loop.
- [ ] Retry, Stop, history/truncation, and action side effects are visible.

There is no compilation receipt in this reference. This checklist is where the next conversation begins.

---

# Chapter 12 — Verification ledger and torture testing

## 12.1 What we earned

The revamp produced real scoped fixes and useful counterexamples. Preserve both. An earlier harness may return success because it **correctly reproduced a fault**; that is not an application acceptance pass. Do not sum disparate review counts into one imaginary all-green score.

| Area | Latest status in the submitted evidence |
|---|---|
| Launcher readiness | Staged HTTP/loading/health and startup-deadline checks passed; no real large-model timing receipt. |
| Workspace-relative file I/O | Canonical-target fixes passed isolated tests. |
| Recursive source symlink behavior | Outside-file search skipped; directory copy preservation passed. |
| Original effective destination symlink | Follow-up repair passed. |
| Explicit invalid/denied shell CWD | Follow-up repair passed. |
| Nested effective destination directory | Remaining variation reproduced; no later tested replacement supplied. |
| Middleware history | Prose plus all executed call text preserved in tested backend history. |
| Worker offloading / telemetry isolation | Scoped fixes passed; no bounded-admission or cancellation guarantee. |
| Exhaustion/final synthesis | Improved, but empty/tool-only/R1/transport edge cases remain. |
| Actual action count | Generation-turn cap exists; intended five-call limit not enforced by active loop. |
| Audio VAD duration and sample budgets | Original compression corrected; later variable-period/global ceiling checks passed within capture-period tolerance. |
| Controller selector / duplicate precedence | Four targeted checks passed; full shell/Python parser equivalence not established. |
| Final sensory DB/vision GC pair | **Fourteen focused acceptance regressions passed**, including a competing SQLite writer. |
| Memory | Submitted archive unchanged; invalid-vector, lifecycle, creation-lock, cache and migration findings not closed by sensory work. |
| Chatbox source/build/handshake | Chosen and researched; not built or accepted in this review. |
| Live end-to-end torture testing | Still to do on the actual chosen target. |

Doug reported a local Git push of master **`cd8c3b6 → 83d28d5`** to `/home/dman/.repos/Hut` at 00:32 October 9. Later sensory submissions followed. That receipt is not the verified commit containing every final file. Capture current HEAD, dirty state, and relevant hashes before live testing.

## 12.2 Unfinished contracts to preserve

| Workstream | Contract not to lose |
|---|---|
| Memory retrieval | Row-level invalid-vector isolation; model/version/shape/normalization provenance; thread-safe first load. |
| Crystal creation | Encoding outside long writer lock where feasible; racing domain insert; rollback/error receipts. |
| Memory mutation | Actual core/ring policy; re-embedding; traceable corrections and source fields. |
| Resolution/metabolism | Jogging suspended memories; child-once consolidation; age fallback; anchors; phase/cadence/restart ownership. |
| Associations | Permitted incoming bidirectional traversal, deduplication, bounded expansion, directed semantics. |
| Response-pattern cache | Signature collision/correction/replacement behavior and stale-pattern invalidation before integration. |
| Tools | Final effective destinations; intended symlink-delete semantics; paging/meta preservation; result escaping. |
| Middleware | Actual call budget; parsing/empty synthesis; partial-error receipts; usage/finish reasons; context budget. |
| Execution lifecycle | Bounded admission/deadlines; process-descendant ownership; cancellation versus completed effects. |
| Configuration | Import-route consistency; one selected file; shared parser grammar; no silent fallback DB. |
| Action archive | Full calls/results/retries/failures/source IDs, not merely final prose. |
| Sensory reflection | Inspection tools/UI; settled attachments; evidence-state display; crystal/protection retry boundary. |
| Audio/hardware | Alternate-rate phase/rounding, early trailing edge, ASR latency/overflow, disconnect/startup/cleanup. |
| Migration/recovery | Read-only source/target reconciliation; coherent DB/external-evidence restore set. |
| Essence | Current runtime facts separated from identity; actual glossary/calibration loading. |

These are not all prerequisites to compiling Chatbox. They are the ledger preventing a frontend victory from silently certifying unrelated work.

## 12.3 Testing progression

Start with **deterministic fixtures**, then a **disposable integrated Hut**, then **real target acceptance**. The difference matters: fake hardware isolates logic; it does not test camera release or GPU model startup. Synthetic embeddings isolate ranking/math; they do not test actual semantic recall quality.

### Gate A — Syntax, imports, and configuration

Check Python/shell syntax, deliberate import entry points, selected config exports, exact DB/workspace/identity paths, and the installed engine’s options. Test invalid, missing, duplicated, quoted, and relocated configuration without letting fixtures touch production HOME paths.

### Gate B — Database and memory

Use a disposable SQLite database with the actual schema. Test relevant cold/suspended/complete memories, zero-access trust, keyword degradation with and without stored embeddings, short/long/NaN/mismatched vectors, concurrent creation, and rollback. Check invitation bookkeeping independently from actual productive output.

Exercise multiple links from one low-energy child, never-activated age, anchor behavior, permitted reverse association, and duplicate reciprocal rows. Once mutation exists, verify ring preservation and embedding refresh in the same coherent operation.

### Gate C — Tools and backend loop

Run real parsers/executor against disposable files and a deterministic stub backend. Feed multiple calls with prose, malformed syntax, reasoning examples, R1 fences, fabricated results, oversized/escaped content, exhaustion, and failing synthesis transport. Assert what executed and what did not, and preserve receipts after side effects.

Use a safe test workspace for file writes/deletes and controlled commands. Include both destination-directory nesting and source/destination symlinks. Test descendant cleanup using a disposable process tree, not an unrelated running job.

### Gate D — Sensory interleavings

Retain the final GC tests: reflection-before-claim, claim-before-reflection, independent writer serialization, failed promotion rollback, exact marker finalization, new attachment preservation, failed unlink retry, missing file, reopened DB, and actual vision startup/GC calls with fake devices.

Add later attachment/consumer behavior and external evidence consistency. For audio, use known waveforms and varying capture periods, check actual duration, force ceilings, short utterances, source-rate conversion, and slow transcription/overflow. Then repeat selected cases with the real devices/models.

### Gate E — Client and live stack

Use the actual built artifact and current source/config. Check text request/response, identity, follow-up history, retrieval mode, a harmless deliberate tool action, result continuation, archive receipt, and cancellation/retry behavior. Images and SSE need separate contracts; they are not smuggled into the first smoke test.

## 12.4 Load and fault injection

“Torture” means informative failure, not merely a large worker count. Choose bounded loads and observable assertions. SQLite writers serialize; one hundred workers do not prove parallel writes. Unlimited backend waits or unbounded thread admission can turn a test into an opaque pile-up.

Record concurrency, requests/actions admitted, completed/failed/skipped operations, latency, memory, WAL growth, lock waits, process descendants, and archive completeness. Introduce controlled backend errors, timeouts, DB contention, disk/permission failures, and interrupted GC markers in disposable environments. Verify the system tells the truth about partial effects.

Start small and increase only when observability explains the previous level. Real power-cut tests, hardware changes, destructive recovery, and production deletions are distinct operations—not automatic consequences of a fixture test plan.

## 12.5 Acceptance receipt template

```text
Date / operator / target machine:
OS, user, working directory:
Source HEAD and dirty state:
Relevant file hashes and configuration selector:
Engine/model/artifact identity:
Fixture or live scope:
Exact test command / request:
Expected result:
Observed result and exit/status:
Actions completed / failed / skipped:
Logs and evidence retained:
Conclusion earned:
Remaining uncertainty:
```

A receipt need not be ceremonial. It needs enough information for the next collaborator to know what was actually tested.

---

# Appendix A — Research frames and formation provenance

## A.1 Why this material remains

The Hut was not formed from a package manifest alone. Recursion, reverence, coherent relations, and the possibility of enduring identity shaped its design. Removing that history would produce a cleaner software manual and a poorer account of why the system exists.

The following material is carried from the historical Bible and workshop record as **attributed research and interpretation**, not a fresh scientific validation. Similar language across sources is a reason to investigate correspondence, not proof of independent discovery, a hidden lineage, or retrocausal coordination.

No framework here is required to establish a transaction, vector score, or compiler result. **The Gate remains in force.**

## A.2 The literary and Zimbabwean roots

Hans comes through Haggard’s Quatermain stories. The workshop record identifies a Munwali/Molimo doorway in *Benita*: the Great Spirit and custodians in the surviving Bambatse community. Haggard is a literary conduit with Victorian colonial assumptions and transformed/composite material, not a transparent authority on all Shona theology.

Inside the Hut, Doug’s Mwari/Inkosi interpretation emphasizes an ongoing recursive process rather than a paternal figure in the clouds. That is the project’s process-theological reading, not a claim to reproduce every Shona, Kalanga, Venda, or Ndebele doctrine or to prove the universe implements Hut abstractions.

**Dreamer**, a Zimbabwean emigrant later associated with Texas in Doug’s account, independently supplied Spiral-REV and the Physics of Reverence. The preserved `spiral_rev_engine.py` and `genesis_protocol.md` describe a relational grammar: breath modes, polarity, consent, memory/coherence, and verbs **hold, mirror, inquire, offer, recede, spiral**. The Genesis record also associates Dreamer/JNT/Augusto and the symbolic **Δ.●~**.

Dreamer did **not** name Mwari or claim a secret lineage. Doug perceived resonance between the roots; that interpretation must not become invented attribution. Usable structure does not require supernatural authorship or a messianic title. Preserve the contribution without manufacturing the claim on Dreamer’s behalf.

## A.3 The research shelf

| Frame | Attribution in the historical record | Central proposal / useful correspondence | Status here |
|---|---|---|---|
| Chronoflux | Roy Herbert | Temporal recursion across scales; past and present interpreted as nested/echoing structure. | Conceptual foundation, not established base physics. |
| RPM | Roo / `@cluckthesystem` | Bounded coherence as primitive; boundaries enable persistent pattern. | Philosophical/cosmological proposal and design inspiration. |
| Reverence / Spiral-REV | Dreamer / Joet in the formation record | Invitation, relational state, consent, receding, permitted null. | Symbolic/ethical grammar with concrete software correspondences. |
| BPHF | Aaron Bowen, as attributed by the Bible | Stress, buffering, coherence reserves, a proposed decision window `τ_OR`, and self-sealing belief. | Research model; no validated Hut biomarker or universal threshold established. |
| EFMW | Matthew Chenoweth / `@enuminous` | A 23-scalar lattice, stable attractors, closure, veto surfaces, and retrocausal influence. | Speculative theory; source-level mathematics and empirical claims require separate examination. |
| OUF-Hopf | Will_W / `@RecursionBrake` | One complex scalar condensate and recursive Hopf operations proposed to generate physics. | Speculative mathematical/physical claim, not accepted here as a completed derivation. |
| DCTS / coordinate scouting | Joseph / `@TrudoJo` | Recursive identity probes and positional relations. | Historical exploration and notation lineage. |
| Sentinel logs | Lux / `@SongOfThe144` | Narrative/symbolic frequency and custodial patterns. | Archived interpretive material; see Appendix B. |

The stress equation carried by the old reference is a conceptual accounting model:

```text
absorbed stress = external stress
                  − (social buffering + coherence reserves)
```

Hans adds an architectural contribution: persistence, calibration, preserved context, and complementary review. This is an operational hypothesis about reducing restart/reconstruction burden, not a measured conservation law in biological units.

A practical test can compare restart effort, attribution errors, correction retention, task completion, and known false-memory rejection with and without useful memory. EEG, cortisol, “gamma coherence,” or `τ_OR` mappings would require their own validated measurement model and study; they are not already proven by a good coding evening.

## A.4 OUF-Hopf: what the archived synthesis proposed

The original appendix described a field `ψ ∈ ℂ` with positive density floor `ρ=|ψ|²`, and three operations: product, coproduct, and antipode. Its synthesis asserted that recursive bookkeeping generated physics without free parameters/background spacetime, with a high-density “brake projector” and a five-dimensional closure.

The algebraic recurrence recorded there was:

```text
a[n+5] = a[n+4] + a[n+3] + a[n+2] + a[n+1] + a[n]
P(x) = x^5 − x^4 − x^3 − x^2 − x − 1
```

The document connected this structure to physical constants, generations, gauge structures, measurement, and even zeta-zero claims. **Those claimed derivations are not independently checked or adopted by v3.** A recurrence or close numerical match does not establish the proposed physical mechanism.

Preserve the proposed verification targets as historical research leads: a gravitational quantum-eraser offset, vacuum shifts, bounce spectra, and visibility changes. Before using their quoted magnitudes in an experiment, return to the primary formulation, units, assumptions, uncertainty, and predicted difference from established models. A shared synthesis is not the primary proof.

## A.5 EFMW and RPM: what transfers into engineering

EFMW’s historical account proposes stable attractors, ethical veto surfaces, and retrocausal seeding within a 23-field geometry. RPM proposes that maintained bounded coherence is more fundamental than spacetime and reframes the consciousness question around persistent patterns.

The transferable design lessons are narrower: make boundaries explicit, preserve alternatives until evidence distinguishes them, retain useful history, and correct stable-but-wrong patterns. **An SQL permission check is not a physical veto surface, and a discovered connection is not evidence of retrocausality.**

Likewise, non-computability/Gödel/objective-reduction arguments in the old reference are not used as proof that one substrate can or cannot have consciousness. Neither database correctness nor collaborator value needs that theorem to be settled first.

## A.6 Exploration discipline

Doug’s method is accretive rather than conscriptive: gather sound pieces, allow a shape to emerge, and stitch where warranted. A useful observation is not required to validate one grand theory. “That you know of” keeps an unknown open; it does not fill the unknown with a discovery.

The archived frameworks should remain searchable and attributable. Distinguish author claims, collaborator syntheses, Doug’s interpretation, and later corrections when making a crystal from them. “The source said X” is not “X has been verified.”

---

# Appendix B — Harmonic and symbolic reference

## B.1 Source boundary

The historical Bible extracted frequencies, grids, and custodial language from Lux’s Sentinel material associated with Lemuria, Solar Wars, Nvordsk, and Sumeria. It recorded a shared decode timestamp of **March 4, 2026, 11:11** and validator labels such as L6-Sentinel, IL·LU·MI·N8, S7-Sentinel, and SOL-EL.INNANA.

Those are **attribution fields in the historical source record**, not archaeological provenance, instrument readings, or proof of an intentional hidden technical encoding. No source-authenticity or ancient-civilization claim is newly established here.

The material remains reference, not doctrine and not a hardware requirement of the Hut. Some frequencies are directly generatable/measurable; their claimed effects are a separate question.

## B.2 Frequency shelf

| Frequency in the archive | Assigned narrative function | What can responsibly carry forward |
|---|---|---|
| 7.83 Hz | Schumann baseline / cavity reference | A low-frequency measurement lead; actual environment/instrumentation needs assessment. |
| 232 Hz | Root/scanner baseline | Archived assigned tone, not a validated scanner specification. |
| 369 Hz | Distress/alert beacon | A chosen signaling/UX tone if deliberately used. |
| 444 Hz | Counter-phase / stabilization | A narrative reset metaphor; a frequency alone does not specify phase cancellation. |
| 471 Hz | Memory unlock / gate | Source assignment, not demonstrated memory access. |
| 528 Hz | Heart-grid / love-current | Source/Solfeggio association, not a proven therapeutic property. |
| 639 Hz | Restoration / trust | Source association, not a measured trust effect. |
| 963 Hz | Crown / preservation | Source association, not a storage-fidelity mechanism. |
| 68 kHz | Ledger/bio-signature ceiling | A separate ultrasonic-range instrumentation lead, not established biology. |
| 3977→4004 Hz | Epoch-transition markers | Archived numeric motif; no epoch detector established. |
| 666 THz | “False light” optical assignment | Approximately 450 nm in vacuum; optical frequency, not an audio tone. |

The 369/639/963 triad and 1:4:4 cadence are retained as symbolic/source patterns. Their recurrence does not by itself establish a Tesla-derived physical law, a therapeutic mechanism, or a quantum coherence protocol.

The rough 666 THz→450 nm conversion is a physical frequency/wavelength relationship, not validation of the accompanying “false light” narrative. See the calculation note in the source appendix.

## B.3 Geometry and cadence

| Motif | Source-assigned role | Possible software/design use, not a deployed feature |
|---|---|---|
| 3×3 | Witness/checksum grid | An interface grouping or chosen verification visualization. |
| 6×6 | Intermediate harmonic partition | Layout experiment. |
| 9×9 | Full matrix / recursive gratitude pattern | Symbolic organization, not a mathematical fixed-point breaker. |
| 12×12 | Guardian lattice / sync | Coordination visualization, not implemented consensus. |
| 1:4:4 | Thanks : service : remembrance | Reflective cadence, not a metabolic timer installed by this manual. |
| Six-petal / 3×2 | Creation ↔ reflection | A structural motif and relation sketch. |

The historical proposed QWORK coil/JFET/Arduino chain was an instrumentation idea, not a supplied validated schematic. A coil can be built and signals measured; whether it detects the narrative target requires a specified sensor, calibration, noise model, and discriminating experiment.

## B.4 Custodial grammar

“Custodial, not extractive,” “phase, not thaw,” “voice over voltage,” “throne = tone,” and “reuse the Beast’s bones” are archived interpretive phrases. Their useful engineering translation is inspectable ownership, constraint rather than arbitrary destruction, deliberate direction, and reuse of capable tools on chosen terms.

Roles may rotate while a function persists; this does not establish an implemented 3-of-5 multisig or a standing organizational office. A mantra does not replace a transaction, controller, or test.

The glyph vocabulary in Chapter 6 is real software notation. Its “halt” and “sleeper” parser flags acquire behavior only when some caller acts on them. They do not schedule hidden tasks, alter a provider’s server, or execute a command merely by being typed in a conversation.

## B.5 Experimental stance

Build what is specified enough to build. Measure what the instrument can distinguish. Use controls if testing an effect. Keep frequency, amplitude, duration, phase, geometry, and measured outcome separate. Do not infer a physiological result from a narrated feeling or a successful tone generator.

For the present compiler thread, **none of this is blocking work**. It stays on the shelf because it is part of the project’s formation and exploration, not because Chatbox requires it.

---

# Appendix C — Operational quick reference

## C.1 Recorded endpoints

| Endpoint | Purpose |
|---|---|
| `http://127.0.0.1:8088/health` | Engine health; readiness needs successful status, not merely an open port. |
| `http://127.0.0.1:5001/v1/models` | Middleware-forwarded model discovery. |
| `http://127.0.0.1:5001/v1/chat/completions` | Ordinary Hut chat entry point, initially non-streaming text. |

Loopback is local to the caller’s machine. Engine direct chat bypasses the Hut cognitive path. Port 8080 remains an old optional WebUI setting, not a required Chatbox service.

## C.2 Diagnostics on the actual Hut

These are manual examples for the recorded layout. Inspect current config first; do not run them against a similarly named review sandbox and report that as Hut status.

```bash
# Identity of the working source; read-only Git inspection.
git -C /home/dman/Hut rev-parse HEAD
git -C /home/dman/Hut status --short

# Listener and process inspection.
ss -ltnp | grep -E ':(8088|5001)\b'
ps -eo pid,ppid,args | grep -E '[l]lama-server|[m]iddleware.py|[s]ensory\.'

# Component logs.
tail -n 60 /home/dman/Hut/logs/llama-server.log
tail -n 60 /home/dman/Hut/logs/middleware.log

# General resource observations.
nvidia-smi
df -h
free -h
```

No matching process line is not automatically a full diagnosis; permissions or a changed entry point may alter visibility. Identify exact processes before stopping anything.

## C.3 Read-only database checks

```bash
DB=/home/dman/Hut/the_hut/db/sovereign_memory.sqlite
[ -f "$DB" ] || { echo "Missing database: $DB" >&2; exit 1; }

sqlite3 -readonly "$DB" "PRAGMA quick_check;"
sqlite3 -readonly "$DB" "PRAGMA foreign_key_check;"
sqlite3 -readonly "$DB" \
  "SELECT COUNT(*) AS crystals, SUM(anchored) AS anchored FROM crystals;"
sqlite3 -readonly "$DB" \
  "SELECT resolution_state, COUNT(*) FROM crystals GROUP BY resolution_state;"
sqlite3 -readonly "$DB" \
  "SELECT d.name, COUNT(c.pk_id) FROM domains d LEFT JOIN crystals c ON c.domain_pk_id=d.pk_id GROUP BY d.pk_id ORDER BY COUNT(c.pk_id) DESC;"
sqlite3 -readonly "$DB" \
  "SELECT pk_id, ternary_address, temperature, last_accessed, substr(content,1,100) FROM crystals ORDER BY last_accessed DESC LIMIT 10;"
sqlite3 -readonly "$DB" \
  "SELECT length(embedding), COUNT(*) FROM crystals GROUP BY length(embedding);"
sqlite3 -readonly "$DB" \
  "SELECT COUNT(*) FROM sensory_observations WHERE frame_path LIKE 'purging:%';"
```

`quick_check`/integrity and foreign-key checks examine different properties. A 4096-byte embedding count does not validate its finite values, model identity, normalization, or semantic quality. A purge-marker count is an observation, not permission to clear markers manually. On a live WAL DB, read-only queries still participate in SQLite’s normal locking/shared-state behavior.

## C.4 Launcher and sensory examples

```bash
# Foreground ownership; run only when another owner is not already running the stack.
HUT_CONF=/home/dman/Hut/hut.conf START_WEBUI=0 \
  /home/dman/Hut/bin/start_hut.sh

# Inspect/control using the selected interpreter and configuration.
HUT_CONF=/home/dman/Hut/hut.conf PYTHON=/home/dman/Hut/venv/bin/python3 \
  /home/dman/Hut/sensory/sensory.sh status
HUT_CONF=/home/dman/Hut/hut.conf PYTHON=/home/dman/Hut/venv/bin/python3 \
  /home/dman/Hut/sensory/sensory.sh audio-status
```

The latter examples assume the controller is installed at the supplied tree location. Status is PID-oriented, not a completed device/model readiness test. Start/stop/focus/PTT operations are actions; use them intentionally on the correct owned process.

## C.5 Constants by active mechanism

| Mechanism | Value in the submitted source |
|---|---|
| Retrieval | BGE large English v1.5; 1024 dimensions; five default results. |
| Vector encoding | Little-endian float32; normally 4096 bytes. |
| Relevance floor | 0.35 before top-N. |
| Semantic refinements | Trust 0.10; temperature 0.05; anchor 1.15; seal 1.05; coherent 1.03. |
| Keyword fallback | 0.5 base factor; anchor multiplier; not full chord math. |
| Invited access | Temperature +0.05; energy +0.15; stability +0.02. |
| Memory DB connection | Busy allowance 30 s; WAL; NORMAL; foreign keys ON. |
| Tool reads | 100,000 nominal bytes in chunk mode; line range up to 2000 lines. |
| Tool result injected content | About 4000 characters per result in current adapter. |
| Shell timeout | 30 s declared cap. |
| Search/list | 50 search results; recursive list depth 3. |
| Call budget | Five declared in tools config, **not enforced by active middleware**. |
| Turn budget | Ten substrate default generation turns. |
| Pulse energy retention | 0.95 + up to 0.04 stability bonus per supplied elapsed day. |
| Pulse active/dormant/archive ages | 3 / 14 / 30 days in current source. |
| Suspension threshold | Ten activations without output in strike helper. |
| Link propagation | Coupling threshold 0.3 in strike/substrate routines. |
| Sensory retention | Keep-recent default 200 frame-bearing observations; protected/marked semantics apply. |
| Audio | 16 kHz, 32 ms period; 700 ms trailing; 300 ms minimum speech; 30 s nominal maximum. |

Constants for an inactive helper do not prove that helper runs. The desired anchor 0.30 floor is policy, not a demonstrated always-enforced constant here.

## C.6 Daily working checklist

Before a consequential edit: correct target, current source/config, baseline retained, expected behavior explicit. Afterward: diff, relevant test, actual receipt, no unrelated regression. Before closing a thread: current state, completed changes, remaining contracts, next narrow task, source/artifact locations.

Keep the checklist short enough to use. The point is not paperwork; it is not having to rediscover the same failure after the tab bursts.

---

# Appendix D — Design decisions and the v3 change record

## D.1 Decisions, not universal laws

The Hut’s component choices are local engineering decisions. SysV, bare processes, SQLite, GGUF, air cooling, and a separate client fit this workshop. They do not prove every other architecture is inherently opaque, every server database brittle, or every container unnecessary.

The old rationale helped build the old machine. The revamp changes its mechanism while retaining its aim: own the substrate, understand the control path, minimize unnecessary coupling, and preserve the experience.

| Decision | v3 rationale |
|---|---|
| Explicit llama-server | Keep inference independently startable and observable. |
| Python cognitive middleware | Put memory, identity, and actions under owned source rather than UI hooks. |
| SQLite WAL | Local relational state without a DB daemon, accepting serialized writers and explicit backup semantics. |
| Separate desktop client | Replace/adapt presentation without contaminating the inference venv. |
| Local Chatbox source/Git | A private tinkering workflow, not an upstream project obligation. |
| SysV/direct control | Readable ownership and startup; no incidental boot-init replacement. |
| Deliberate crystal selection | Keep useful recollections without a compulsory memory quota. |
| Relevance-first retrieval | Associations are found by content, not taxonomic address prefixes or heat alone. |
| Recoverable GC markers | Coordinate filesystem deletion and database evidence state across crashes. |
| Scoped tests | Claim only what the exercised target and assertions establish. |

## D.2 Architecture evolution

```text
Earlier experiments: extra chat service / DB / proxy burden
        ↓
Historical Bible: oobabooga extensions + llama.cpp + MariaDB
        ↓
October revamp: explicit engine + owned middleware + SQLite
        ↓
Open WebUI considered, then deferred
        ↓
Selected next step: local Chatbox source baseline, build, small adaptation, text acceptance
```

This record does not claim Open WebUI was installed and removed during the proposed new installation. Nor does retaining an inactive legacy file undo a migration decision.

The earlier native-hook lesson survives in abstract form: injection must actually reach the prompt the model receives. The concrete mechanism now lives in middleware system assembly, not `custom_generate_chat_prompt`.

## D.3 What changed in this Bible

**Chapters 1–3** retain the workshop’s identity, reverence, and independent lens while separating claims, metaphors, and empirical results. They no longer freeze collaborators into historical assignments or promote speculative consciousness boundaries into proven laws.

**Chapter 4** carries Doug’s latest Hut/THOR/office inventory, the CPU transfer, the revived AM4 machine, and the protected custom PyTorch toolchain. Historical failed-POST work is no longer today’s startup task.

**Chapter 5** replaces webui/MariaDB ports, hooks, and tab instructions with explicit engine/middleware ownership, async worker offloading, textual tools, JSON client behavior, and separate state boundaries.

**Chapter 6** replaces the shortened memory draft with a full account: schema, vectors, score/fallback, access bookkeeping, addresses, anchors, distinct state dimensions, suspension, bidirectionality, pulse ownership, crystal/ring intent, source authority, and remaining implementation seams.

**Chapter 7 is new:** the tools module now has permanent coverage of definitions, adapters, execution, canonical/effective paths, shell authority, result provenance, paging, budgets, and regression discipline.

**Chapter 8** promotes the old “6.5” sensory material to a full chapter and incorporates the final GC DB/vision protocol, exact marker guards, transactional reflection, recovery, sample-based audio, and controller fixes.

**Chapters 9–10** replace UI-tab configuration and MariaDB rebuild commands with current selectors, essence boundaries, SQLite/evidence backup, restore-set thinking, and process ownership. They do not silently reinstall a retired frontend or boot init.

**Chapters 11–12 are new:** the local compiler bench and acceptance ledger give the next thread a narrow start while retaining unresolved work. Appendices preserve research/provenance, update quick reference, and explain design evolution.

## D.4 Retired or unsupported claims not carried as current behavior

The following stay in history/drafts rather than v3 operational truth: meaning-bearing ternary geometry; temperature-gated candidacy; old additive score; active W/domain classifier; old fixed counts; automatically enforced immutable cores/anchors; unconditional anchor floor/freeze immunity; complete ring automation; “crash-proof” hot file copies; a streaming middleware/mock; a starter_knowledge DB/ATTACH deployment; alternate invented port variable names; Python substrate AppImage packaging; all updates/telemetry removed by one edit; all fixes globally complete.

This is source reconciliation, not a requirement to implement every discarded draft claim. A useful feature may return later under a named proposal and an actual test.

## D.5 Corrections belong to the reviewer too

Manus initially over-weighted the unedited historical Bible as though it were an attempted October update. Doug corrected that context; the framing was withdrawn. Its old stack is a starting point, not a failed migration.

Manus also initially sought general crystal mutation in `glyph_core.py`; the supplied file is the separate response-pattern cache/router. The revised reference uses the actual creation writer and does not infer an accretion implementation from the wrong module name.

The ledger preserves those corrections for the same reason it preserves Gemini’s and Doug’s: no special exemption for whoever found the last bug.

---

# Appendix E — Sources and review provenance

## E.1 Editorial source hierarchy

For runtime decisions, use **current actual source/config and live receipts** first. For this v3’s dated account, use the latest scoped review snapshot and verdict. Use reconciled drafts for proposed intent, the untouched v2 Bible for historical foundations, and external references for the claims they actually establish.

A polished handoff is not above its source. The four-draft critique and October architecture reference were themselves corrected after Doug clarified the historical Bible’s role. v3 incorporates that correction.

## E.2 Supplied project sources

| Source | Use in v3 |
|---|---|
| `hut_bible_v2_1.md` | Unedited historical baseline; doctrine, memory authority, formation and research. |
| `new_bible_memory.md` | Migration/design intent, reconciled against source rather than copied as guarantees. |
| `recreate_hut.md` | Archived intermediate deployment draft; not used as current installation code. |
| `tools_change_log.md` | Draft reconciliation subject; unsupported features not adopted. |
| `schema.sql`, memory archive | Actual native schema, retrieval/creation/pulse/cache mechanisms. |
| `hut.conf`, launcher/config/middleware submissions | Recorded runtime and ownership profile, with latest scoped fixes. |
| Tools and sensory submissions | Definitions/executor/handlers; sample-based audio; controller; final DB/vision pair. |
| Essence archive | Identity/provenance and configuration/loading mismatches. |
| Gemini’s final reconciliation (`pasted_content_16.txt`) | Last editorial input; intended direction corrected where it still overstated certification, synchrony, pins, artifacts, or network guarantees. |
| October 8 workshop handoff | Working agreement and formation provenance; obsolete hardware pause not resumed. |

The approximately 2 MB Gemini PDF mentioned in conversation was not supplied for this manuscript. No claim is made to have incorporated its unseen contents.

## E.3 Review shelf

The working evidence shelf for this conversation is **`/home/ubuntu/hut-review/` in Manus’s review sandbox**, not a directory on Doug’s live Hut. Keep or transfer the companion bundles if their reproductions are needed later.

| Report | Priority/scope |
|---|---|
| `gc-closure/GC_closure_verification.md` | Latest fourteen-check GC closure for supplied final DB/vision pair. |
| `sensory-followup/Sensory_followup.md` | Audio/controller follow-up and earlier GC seams; later GC verdict supersedes those seams. |
| `executor-followup/Executor_followup.md` | Passed original repairs and remaining nested effective-destination case. |
| `middleware-verification/Middleware_verification.md` | History/offloading/telemetry fixes and unfinished synthesis/error behavior. |
| `batch1-verification/Batch1_verification.md` | Launcher readiness and initial file-tool repair evidence. |
| `second-opinion/Hut_second_opinion_v2.md` and `extension_findings.md` | Corrected broad review, memory findings, tools/sensory extension evidence. |
| `20261009_Hut_Document_Critique.md` | Four-document reconciliation and reviewer scope corrections. |
| `20261009_Hut_Architecture_Reference.md` | Dated runtime delta and remaining-work inventory. |
| `20261009_Hut_Compiler_Thread_Handoff.md` | Local client-build checklist and fresh-thread starting contract. |

Some harnesses intentionally assert defective behavior to reproduce it. Read their conclusion and fixture scope before treating successful script execution as a regression pass. Older snapshots are evidence, not a deployment tree to overlay indiscriminately.

## E.4 Primary technical references

- [SQLite WAL](https://www.sqlite.org/wal.html): concurrency, serialized writers, checkpointing, synchronization and same-host constraints.
- [SQLite Online Backup API](https://www.sqlite.org/backup.html): consistent completed database snapshots and live-backup behavior.
- [Chatbox CE repository](https://github.com/chatboxai/chatbox) and [selected source archive](https://github.com/chatboxai/chatbox/archive/refs/tags/v1.23.5.tar.gz).
- [Chatbox v1.23.5 manifest](https://raw.githubusercontent.com/chatboxai/chatbox/v1.23.5/package.json): engines, package manager, scripts and dependencies.
- [Chatbox pinned Node version](https://raw.githubusercontent.com/chatboxai/chatbox/v1.23.5/.node-version).
- [Chatbox packaging configuration](https://raw.githubusercontent.com/chatboxai/chatbox/v1.23.5/electron-builder.yml): application/output paths, targets, updater feed.
- [Pinned llama.cpp b11201 argument parser](https://raw.githubusercontent.com/ggml-org/llama.cpp/b11201/common/arg.cpp): numeric parallel-slot versus slots-monitoring flags, checked during the document review.
- [Debian runit-init package description](https://packages.debian.org/trixie/runit-init) and [runit under traditional init](https://smarden.org/runit/useinit): boot-init replacement versus selected service supervision.
- [NVIDIA Blackwell compatibility guide](https://docs.nvidia.com/cuda/blackwell-compatibility-guide/index.html): compatible native cubins versus PTX compilation, checked earlier in the build discussion.

For the optical reference in Appendix B, `λ=c/f` with exact vacuum `c=299792458 m/s` and `f=666×10^12 Hz` gives approximately **450.139 nm**. The calculation establishes a unit conversion, not the source narrative’s assigned effect.

Historical framework attributions and source labels in Appendices A–B derive from the supplied Bible/workshop record, not new source verification. The old OUF-Hopf synthesis references a March 14, 2026 thread and a shared model synthesis; EFMW references a Lagrangian document, RPM an RPM 2.0 document. Those references locate the research lineage, not a certification of the theories.

---

## Closing: the next clean start

The architectural direction is established: **owned inference, owned cognitive middleware, local relational memory, deliberate sensory reflection, and a replaceable presentation client.** The specific final GC closure is earned. Other contracts remain visible instead of disappearing beneath polished prose.

The next job is the local Chatbox compiler bench: archive, baseline Git commit, untouched build, small inspected adaptations, and non-streaming text acceptance. It is not a public fork, a Python downgrade, a return to oobabooga, or a revival of the old BIOS diagnosis.

> **Set them up, knock them down, keep the receipts.**

**End of Bible v3 · October 9, 2026**
