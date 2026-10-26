# V2 feasibility and inventory evidence

Read-only observations on 2026-09-11, approximately 12:15–12:19 UTC. This is not a sealed corpus census, workload benchmark, or peak-memory trace. Repository root: `C:/Users/foste/Documents/projects/local_sovereign_agent`. C0 means these observations; C1 means proposed pilot review 2026-09-12T23:59:59Z; C2 means proposed full-seal review 2026-09-20T23:59:59Z. The latter dates and proposed envelopes are **NEW SPECULATION**, not promises to execute. An unrun check remains Unproven.

## F1 — Current 40 GiB resident cage envelope fails the pre-seal feasibility gate

**Status: Disputed for the current configuration. Confidence: high.** The v1 registration, lines 40–42, proposed at most eight active task executors, 40 GiB aggregate fixture-worker memory, and a separate 2 GiB control/observer reservation. Docker reports `MemTotal=33,627,451,392` bytes = 31.32 GiB for its Linux VM. A 40 GiB simultaneously resident in-cage worker set cannot fit within this physical capacity, before the observer and existing services. Merely setting a 40 GiB maximum is possible, but that is not a demonstrated 40 GiB reservation or resident workload. Swap would change latency and residency semantics, not establish fit.

Host observations from elevated read-only CIM, not source documentation:

| Measure | Observed value | Source / limitation |
|---|---:|---|
| CPU | AMD Ryzen 7 3800XT; 8 cores / 16 logical processors | Win32_Processor |
| Visible physical RAM | 67,058,352 KiB = 63.951 GiB | Win32_OperatingSystem |
| Free physical RAM, first snapshot | 35,875,100 KiB = 34.213 GiB | Around 12:16 UTC; availability, not peak |
| Free physical RAM, second snapshot | 35,709,760 KiB = 34.056 GiB | 12:17:30 UTC; availability, not peak |
| GPU | AMD Radeon RX 5600 XT | Win32_VideoController; returned AdapterRAM=4,293,918,720 bytes is not a reliable six-GiB-capacity measurement |
| Docker VM physical total | 33,627,451,392 bytes = 31.319 GiB | `docker info`; 16 logical CPUs |
| WSL | docker-desktop running WSL2; Ubuntu stopped WSL2 | Distribution enumeration; no user `.wslconfig` file found |
| mag-sovereign | 1.41 GiB / 31.32 GiB; 71.85% CPU | One `docker stats` sample |
| mag-worker | 25.83 MiB / 31.32 GiB | One sample |
| mag-redis | 8.867 MiB / 31.32 GiB | One sample |
| Three containers' explicit memory, swap, NanoCPUs | All zero; PidsLimit unset | `docker inspect`; zero means no explicit per-container limit, not zero consumption |
| Host Ollama `GET /api/ps` | Connection refused on 127.0.0.1:11434 | Both sandboxed and elevated read-only requests; does not establish unavailability at other endpoints |
| Existing model process query | No `ollama` or `llama` named process returned | Point-in-time CIM query; other runtimes not excluded |

`docker-compose.yml:25–29` directs the cage to host Ollama; lines 36–41 expose the local task ports. The three observed healthy container labels do not establish a working inference dependency. No model was loaded, no service restarted, no resource fence changed. An initial Ollama CLI status attempt unexpectedly tried Windows application startup/log maintenance and failed on denied writes; later checks used GET-only API and process inventory.

**Change-my-mind / resolution:** at C1 or a newly dated pre-seal run, a frozen hardware/configuration receipt plus measured workload trace establishes resident-worker demand, host and VM headroom, and independent observer survival within actual enforced limits. Until then the 40 GiB resident envelope is rejected; eight logical lanes remain a separate Unproven performance claim.

## F2 — Shared model residency permits many clients, not eight free contexts

**Status: Supported as mechanism; feasible local throughput Unproven. Confidence: high.** Separate task executors can call one loaded model server rather than each loading weights. This can amortize model weights. Per-request contexts, KV state, scratch buffers, activation buffers, queues, and CPU/memory bandwidth still matter. Disk aliases sharing a blob do not prove runtime sharing; incompatible options or distinct loaded instances may defeat it. A sequential model server can support eight logical lanes while only one inference request executes at a time. Therefore register executor concurrency and model-request concurrency separately.

Official Ollama documentation distinguishes concurrent loaded models from parallel requests within one model and says required RAM grows with parallelism times context length: [Ollama FAQ](https://docs.ollama.com/faq#how-does-ollama-handle-concurrent-requests). Documentation read at C0; actual runtime version/configuration remained unobserved because the configured API was unavailable.

Existing `dashboard/static/model_census.json` reports 21 model records and 146.5 GB at 2026-09-11T06:16:02-04:00. A bounded metadata recheck found all 24 referenced weight paths present, summing to **146,546,500,755 logical bytes**. This is disk inventory, with duplicates and wrappers, not a distinct-model count or residency measurement. The 1.12 GB R1-distill and 1.68 GB Gemma entries are candidate small-model fixtures; no adequacy or loaded-RAM claim follows from file length alone.

**NEW SPECULATION — initial LLM envelope:** one shared model instance, one in-flight generation, context at most 4,096 tokens, two logical task executors, no embedding build during inference, frozen bounded queue, model selected by task adequacy pretest. Promote to two and then eight in-flight requests only by fresh preflight traces; these are experimental levels, not promised throughput. **Resolution:** C1 readiness receipt and C2 matched p95 latency, accepted-task rate, sampled resident/committed RAM, paging, and observer health. The check fails if a registered hard bound is exceeded; an unrun test stays Unproven.

## F3 — The reconciled inventory is incomplete, and the gaps must remain null

**Status: Supported for the scoped metadata count; whole-corpus reconciliation Unproven. Confidence: high.** The metadata scan in `v2-inventory-metadata.json` walked the live root in 22.906 seconds without reading file content. It observed **882,366 ordinary files and 25,493,584,793 logical bytes**. It did not follow the `training` reparse point and encountered **62 unreadable directories**, principally temporary-test paths. Queue exhaustion is recorded as `complete_walk=true`; that field does not mean complete filesystem coverage. The root was mutable. This count does not contradict a historical 1.3M-file count with a different scope; it does prevent using 1.3M as today's measured eligible denominator.

Selected observed groups: `memory` 485,179 files; `.mimosa` 141,790; `mine` 103,949; `.venv` 56,637; `corpus` 54,773. These include dependencies, duplicates, receipts, backups, and non-text bytes. No implicit eligibility rule can turn the raw total into a defensible corpus denominator.

| Reconciliation stage | Value now | Reason |
|---|---:|---|
| Live metadata-observed ordinary files | 882,366 | Scoped count above |
| Eligible files in a sealed corpus | **null** | No sealed eligibility manifest reconciled |
| Unique chunks under a named chunker | **null** | No whole-corpus chunk mapping reconciled |
| Successful embedding slots under a named encoder | **null** | No whole-corpus embedding receipt reconciled |
| Total raw vector bytes actually allocated | **null** | Not inferred from proposed dimensions |
| Peak RAM for the workload | **null** | No workload or continuous peak/resource trace executed |

The `memory/lenses/corpus_index.json` inspected at C0 declares and contains 107 keyed records, with fields including `pack_id`, `answer_excerpt`, `key_terms`, and `answer_path`. It is a research-lens index, not evidence of nineteen million dense embeddings.

Actual `mag/ram_cache.py:29` caps aggregate text at 2,000,000 characters; lines 59–67 retain at most 1,200 characters per selected file; lines 83–86 select at most 200 research packs + 200 steals + 100 ribs. This particular path therefore has at most 500 snippets and roughly 600,000 snippet characters before separators, metadata and temporary full-file reads. Its docstring mentions embeddings, but the inspected file contains no embedding allocation. Character limits are not byte/RSS limits.

`mag/corpus_ingest.py:56–60` hashes normalized, lowercased whole-file text into a truncated 20-hex-character identifier. Lines 79–97 count deduplicated files and write aggregate metadata, not durable nineteen-million-chunk slots. This existing ingester cannot substitute for a frozen chunker-plus-encoder manifest.

**Change-my-mind / resolution:** at C2, produce a sealed path/size/content-digest/eligibility-reason manifest; deterministic chunk occurrences mapped to unique chunk hashes; encoder/configuration/dtype dimensions and successful-slot receipts; bijection/orphan checks; then allocation and resource traces tied to those artifacts. Report skipped, malformed, empty, revoked, deduplicated and failed items separately. No extrapolated count may be promoted to an observed count.

**F3.1 — Bounded reconciliation of the current cache path. Supported; high confidence.** At 2026-09-11T12:27:27Z, an independent read-only reproduction of the captured selection rules found 150 research-pack files, 140 steal files, and 38 rib files: **328 selected readable files → 328 snippet occurrences → 328 distinct SHA-256 snippet hashes → zero embedding slots allocated by this code path**. Their joined text encodes to **378,181 UTF-8 bytes**. This measures serialized text, not Python heap or peak RSS; source-file reads, titles, duplicated strings and runtime memory are additional. Full selected-source hashes are retained in [current-cache-reconciliation.json](./current-cache-reconciliation.json). No production module was imported. **Change my mind:** the frozen production route identifies another actual vector allocator, or a reproduced selection count differs on identical source bytes. **Resolution:** C2 requires the separate whole-corpus manifest and memory trace above; this bounded observation must not be extrapolated.

## F4 — The 9.7 GB estimate is arithmetically consistent but excludes the design's overheads

**Status: Supported conditional arithmetic; whole-corpus size Unproven. Confidence: high.** The assumption comes from `watch/inbox/OFFLOAD_WAVE_FOLD_20260911.md:12`, also quoted by v1 §5.4. Conditional on exactly 19,000,000 unique slots, dimension 256 and fp16:

| Component | Decimal bytes | GiB |
|---|---:|---:|
| Vectors: 19M × 256 × 2 | 9,728,000,000 | 9.060 |
| Binary SHA-256 keys: 19M × 32 | 608,000,000 | 0.566 |
| One uint64 slot ID each | 152,000,000 | 0.142 |
| Raw subtotal | **10,488,000,000** | **9.768** |

The 608 MB key figure assumes exactly 32 binary bytes per key; hex text doubles payload bytes, before object overhead. The subtotal excludes hash-table load factor/buckets, adjacency/index structure, corpus text, metadata, maps, content occurrences, access history, tombstones, in-flight queries, models, KV state, runtime overhead, and temporary build copies. A full extra vector copy alone adds 9.060 GiB. Peak construction can exceed final steady-state residency. Neither is measured here.

**NEW SPECULATION — accounting contract:** bound memory by measured categories, avoiding double counting shared pages:

`host + VM overhead + corpus structures + resident model weights + concurrent KV/activation/scratch + executors + broker/controller/observer + build temporaries + explicit headroom`.

Measure host physical availability and commitment, VM memory, cgroup current/peak, and process shared/private residency separately; do not sum each process's RSS as if shared mappings were distinct. Reserve corpus construction separately from serving. **Resolution:** C2 compare this budget against sampled peaks and enforced limits; every unknown component blocks scale promotion rather than being assigned zero.

## F5 — Smallest honest pilot

**Status: Unproven proposed envelope. Confidence: medium. NEW SPECULATION.** One disposable deterministic worker, zero model loads, one local effect fixture, one independently protected observer/controller; worker memory capped at 2 GiB and observer/controller at 1 GiB; one active operation, no recursive spawn. Begin only after measured host/VM available memory supports both allocations plus 4 GiB spare headroom, and enforce the caps. A fixture broker test needs no LLM. This proves only one specified protocol path under one fault boundary; it cannot support AI task quality, learning, whole-corpus memory, or eight-way throughput.

Choose the single most discriminating case: receiver commits; worker is killed before completion receipt; replay reconciles without a second commit. Use an independent destination ledger/counter and retained fault-controller record. The full effect contract and verifier design belongs to the companion v2 deliverable.

**Resolution:** C1 compare committed verifier output to the sealed expected case, exact destination effect count, intent accounting, UNKNOWN behavior if necessary, and enforced memory/resource limits. Pass makes this pilot Supported within scope. Any duplicate effect or false completion makes it Disputed. Missing trace or no execution means Unproven.
