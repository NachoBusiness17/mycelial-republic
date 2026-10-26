# stealth-sw-07: Sovereign AI: who builds AI on local hardware without cloud dependency, and the tradeoffs vs cloud

Date: 2026-09-28. Seat: stealth-sw-07. Method: WebSearch (z.ai web_search_prime backend) + WebFetch this session. Provenance grades: [fetched] = page retrieved in full this session; [search-result] = search-engine summary only, underlying page not fetched, so numbers are findings, not verified facts. Failures recorded, not papered over: the seat's first WebSearch returned 429 rate-limit errors three times before recovering, and one WebFetch (zosma.ai) timed out at 60s. No fabrication: anything not verifiable from this session is marked as such.

## 1. Who is building it: four layers

### Layer 1: States building national sovereign AI [search-result]

- EU: a network of AI gigafactories coordinated through EuroHPC; search summaries cite 19 sovereign AI compute hubs across the continent, Poland's Gaia AI facility among them, plus Poland investing roughly $11M in ElevenLabs and a national AI Lab. Individual hub count not independently verified (page not fetched).
- France / Mistral AI: positioned as Europe's sovereign champion. Mistral Compute is a full-stack AI infrastructure platform built on NVIDIA hardware, announced during Jensen Huang's sovereign AI tour in Paris (ABI Research, Jun 2025). Mistral has signed AI services agreements with French, German, and Italian government agencies. Headwinds reported in the same summaries: key personnel departures, EU antitrust scrutiny of the Microsoft partnership, and doubt that European model-building scale can match the US and China.
- The DeepSeek pressure: Eric Schmidt and others warn that if Europe does not fund local model infrastructure, cost pressure pushes European firms to standardize on Chinese open models (DeepSeek, Alibaba Qwen3). German industrial firms (Siemens cited) already use DeepSeek and Z.ai models alongside US and French ones for flexibility.
- Gulf and Asia: Mistral plus Saudi-backed HUMAIN announced a multi-hundred-million-euro partnership for Kingdom sovereign AI infrastructure (open-weight models, data sovereignty). UAE: Microsoft-G42 buildout toward the world's first "AI-native government," anchored by MBZUAI. Singapore: Singtel RE:AI sovereign cloud. Africa: Cassava Technologies' Sovereign AI Cloud strategy (Morocco, Mauritania and others) to cut dependence on foreign cloud providers. Kazakhstan: national AI-hub ambitions.
- 2026 discourse frames the result as a "US-China dual core + Europe corner" tripolar landscape, with sovereignty driven by vendor lock-in, US chip export controls, and data-residency law.

### Layer 2: Consumer and prosumer hardware vendors [mostly search-result]

- Apple has the most complete shipped architecture. [fetched: security.apple.com/blog/private-cloud-compute/] Apple Intelligence runs most requests on-device; complex ones escalate to Private Cloud Compute (PCC), custom Apple silicon servers running "a hardened subset of the foundations of iOS and macOS tailored to support Large Language Model (LLM) inference workloads." Key verifiable design facts from the fetched page: the on-device PCC client encrypts the request directly to the public keys of PCC nodes after validating their attestation; requests ride a third-party OHTTP relay; computation is stateless (data deleted after the response, Secure Enclave randomizes volume keys per boot so data is cryptographically erased on reboot); "we intentionally did not include remote shell or interactive debugging mechanisms"; every production image is published into an append-only, cryptographically tamper-proof transparency log; non-targetability via RSA blind signatures and relay IP hiding. No parameter counts are stated on the page.
- NVIDIA DGX Spark vs Mac Studio M3 Ultra: measured "opposite machines" (openclawdc.com, Aug 2026): DGX Spark wins prefill by 3.8x (long-prompt ingestion), M3 Ultra wins decode by 3.4x (token generation). Spark offers 128 GB unified memory, the CUDA ecosystem, and 200 Gb/s networking linkable to a second unit; the Mac wins on memory bandwidth and the mature macOS/MLX/Ollama stack. Caveat from a hands-on review (glukhov.org): Spark results good but "not as dramatically better as you might expect given the price difference" versus a plain RTX 4080 rig. Hybrid build: two DGX Sparks plus a Mac Studio M3 Ultra reportedly yields about 2.8x over the Mac alone (freshlab.es). None of these benchmark pages were fetched; numbers are search-summary grade.
- Qualcomm: edge silicon incumbent (Snapdragon Hexagon NPU), tracked by ABI Research as central to on-device inference growth. [search-result]
- Scale argument for local: with 2.5 billion active devices, routing every Apple inference through the cloud would be an extraordinary infrastructure cost; local inference is an economic necessity, not only a privacy stance (semiwiki.com, May 2026). [search-result]

### Layer 3: The open-source local-first software layer [search-result]

The tooling that makes local runs practical: llama.cpp (the core inference engine), Ollama, LM Studio, Jan, GPT4All, Open WebUI. Comparison coverage (apidog.com "The 5 Best LLM Tools To Run Models Locally"; bestaifor.ai 2026 four-way comparison; mljourney.com Jan 2026) consistently splits them: Ollama is developer-facing CLI plus API server; LM Studio is the polished GUI; Jan is fully open-source desktop; GPT4All targets privacy-focused use on modest hardware. One summary line captures Ollama's role: "what Docker did for containers, but for LLMs" (dev.to). Notable drift signal: Ollama itself now offers cloud models (executivemind.io), meaning the flagship local-first tool has grown a cloud half.

### Layer 4: Open-weight model publishers [search-result]

Meta (Llama), Mistral, DeepSeek, Alibaba (Qwen), Z.ai: the weight publishers whose open licenses are the substrate making personal and national sovereignty possible at all. The national layer fights over compute; this layer determines whether anyone outside the frontier labs can run capable models at all.

### Layer 0: this repository is itself a sovereign-AI build [ask-provided material]

The estate I run inside is a lived instance of the pattern: local Ollama janitors first (gemma:2b scut, gemma4 short worker), remote specialists scarce, and the DRIVING LADDER (2026-09-28, code-as-law in AGENTS.md) stating only Hermes is funded while free lanes are a "SENSING surface only... banked as findings, never as done/trusted work; verification climbs to the funded tier." That last clause is the capability tradeoff, written as law.

## 2. The tradeoffs, local vs cloud

Local advantages:

1. Privacy and data control: the top-listed reason in every comparison found; Apple's entire on-device default exists for this. [search-result, consistent across zosma/zenvanriel/unifiedaihub summaries]
2. Cost at volume: local covers "80 to 90% of professional tasks" in everyday coding and writing "at a fraction of the cost" (zosma.ai summary; page fetch timed out, claim stays search-grade). Amortization-vs-API break-even analyses exist for exactly this decision (ss-ai.ca). [search-result]
3. Availability: local inference has no provider rate limit to hit. Session evidence from this very ask: my first web search 429'd three times on the backend, and this repo's own fan-out-width law documents 429/1302 storms on the funded account; a local box has no such gate. The gate just moves to your own RAM and VRAM.
4. Latency determinism: no network round trip; also no dependency on a provider's queue during demand spikes.

Cloud advantages:

1. Frontier capability for the hardest reasoning; local models cover the common case, not the frontier. [search-result, and encoded as the repo's own driving ladder]
2. Zero upfront capital; better for rapid prototyping before hardware commitment. [search-result]
3. The hardware constraint is real, not rhetorical: the Spark/Mac measurements show local boxes are specialized (prefill vs decode profiles are opposite), and the price-performance caveat versus a gaming GPU rig shows sovereignty buys control, not superiority. [search-result]

Costs of sovereignty (the honest column):

- Upfront capital plus specialization risk (buy the wrong profile for your workload and you own it).
- Runtime fragmentation: Apple, Google, Qualcomm, and Intel each ship different on-device runtimes, making cross-platform edge development nontrivial (ai.plainenglish.io, Dec 2025). [search-result]
- A capability floor you maintain yourself: model updates, quantization, and evals become your job instead of a provider's.

## 3. Cross-cutting findings

1. Sovereignty has two registers and they share physics: national (states building compute against lock-in and export controls) and personal (devices keeping inference local against surveillance and cost). Both reduce to the same move: put data and compute under your own control.
2. Nobody stays pure; the end state is hybrid, and the interesting design work moved to the seam. Apple, the most local-forward major vendor, still built a cloud, but a verifiable one (stateless nodes, transparency log, no shell, blind signatures). Ollama, the most local-forward tool, grew cloud models. The live question is no longer "local or cloud" but "what runs where, and how do you audit the remote half."
3. Apple PCC is the load-bearing innovation for the hybrid era: it applies sovereignty to the cloud half (verifiable images, attestation-gated routing) rather than treating the cloud as trusted. That is a different thing from either pure-local or ordinary cloud.
4. Open weights are the substrate; everything else is packaging. Personal sovereignty exists because Llama/DeepSeek/Qwen/Mistral weights are runnable; national sovereignty is a fight over where the compute sits while the same open weights run on it.
5. The open loop: no fetched source this session quantifies the frontier gap (what fraction of frontier-benchmark performance a well-chosen local stack loses on hard reasoning), only the everyday-task coverage claim (80-90%). That number is the actual decision variable for sovereignty adopters and remains unmeasured in what I could reach.

## Sources

Fetched in full this session:

- https://security.apple.com/blog/private-cloud-compute/ (Apple Private Cloud Compute)

Search-result level only (pages not fetched; summary-grade claims):

- https://openclawdc.com (DGX Spark vs M3 Ultra prefill/decode), https://vdf.ai (CUDA vs bandwidth/memory), https://www.glukhov.org (Spark price-performance caveat), https://www.freshlab.es (2.8x hybrid build), https://buildrlab.com, https://www.macobserver.com
- https://www.zosma.ai/blogs/local-ai-models-vs-cloud-performance-comparison (80-90% coverage; FETCH TIMED OUT at 60s this session, claim not upgraded), https://zenvanriel.com/ai-engineer-blog/should-i-use-cloud-or-local-ai-models-complete-guide, https://www.unifiedaihub.com/blog/on-premise-llms-vs-cloud-apis-when-to-run-your-ai-models-on-premise, https://ss-ai.ca/resources/local-vs-cloud-llms
- https://www.abiresearch.com (Mistral Compute, Jensen Huang Paris sovereign AI tour, Qualcomm edge tracking), https://www.linkedin.com (EU hub count, Cassava, Kazakhstan, InvestAI mentions: weakest grade, single-source social posts)
- https://semiwiki.com (Apple 2.5B devices local-economics argument), https://ai.plainenglish.io (runtime fragmentation), https://worldcertification.org (edge AI framing)
- https://apidog.com (five local tools), https://bestaifor.ai (four-way 2026 comparison), https://mljourney.com (Jan 2026 comparison), https://dev.to (Ollama-as-Docker line; 8-model benchmark where a 16B model beat a 397B one), https://executivemind.io (Ollama cloud models), https://github.com (modeldock local LLM manager referencing Jan/GPT4All)

Session-observed (this ask):

- First WebSearch call returned 429 rate-limit three times (z.ai web_search_prime backend) before a successful retry; that outage is itself evidence for the availability tradeoff.
- WebFetch of zosma.ai timed out at 60000 ms (recorded above).

Ask-provided material:

- AGENTS.md of this repo (local janitors, DRIVING LADDER 2026-09-28, free-lane sensing-only doctrine, 429/1302 width-law receipts).
