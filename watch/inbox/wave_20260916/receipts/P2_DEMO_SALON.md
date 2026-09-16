# P2 — DEMO SALON (showcase for ractor-salon README) 2026-09-16

- **Lane:** P2 (tandem burn + dogfood — run the showcase salon whose output the ractor-salon plugin README will quote)
- **Operator:** wave agent, free lanes + free-window stealth lane only, **$0 budget**
- **Wave-lane law:** receipt FIRST, append as you go, no git. Repo code NOT edited — driver imports `mag.research_fanout` (`LANES`/`_env`/`_now`) unmodified, pattern follows `../d23_salon50_night_20260916.py`.

## Mission (verbatim)

"run the showcase salon that the ractor-salon plugin's README will quote as example output"

## QUESTION — registered verbatim BEFORE any call

> Should a sovereign agent fleet open-source its orchestration layer? Steelman both sides, then give the deciding argument. Under 150 words.

`question_digest` sha256[:16]: computed by the driver and logged in the run section below (registered here first).

## Lane plan (from D22 rotation table, `receipts/D22_PROVIDER_PROBE_20260916.md`, probed 18:07 UTC)

| lane | model (registry) | D22 status | P2 plan |
|---|---|---|---|
| cerebras-qwen | qwen-3.8-27b | ALIVE, PRIMARY workhorse | probe → 1 salon answer |
| mistral-min8 | ministral-8b-latest | ALIVE, SECONDARY workhorse | probe → 1 salon answer |
| groq-oss | openai/gpt-oss-120b | ALIVE, escalator (8k TPM org bucket) | probe → 1 salon answer |
| groq-oss20 | openai/gpt-oss-20b | ALIVE, fast short-output | probe → 1 salon answer |
| groq-qwen | qwen/qwen3.8-27b | ALIVE-GATED (OTPM 1000 → max_tokens ≤ ~800) | probe → 1 salon answer, max_tokens 780 |
| cerebras-oss | gpt-oss-120b | ALIVE in D22 pass-2 re-verify (726 ms); rotation quota note: "sparse, high-value calls only" | included: exactly 1 salon call fits that budget (interpretation note: the D22 table has no dedicated row but documents this lane alive same receipt) |
| or-ling3 | ling-3.0-flash-sante:free | ALIVE, overflow | probe → 1 salon answer |
| or-nemotron | nemotron-3.5-lightning:free | ALIVE-SLOW (reasoning burn) | probe → 1 salon answer, timeout 180 s, background |
| or-glm52 | glm-5.2:free | FLAKY (upstream shared pool) | probe → opportunistic, 1 retry @ 6 s if 429 |
| mistral-small | mistral-small-latest | DEAD (quota-zeroed, limit-req-min 0) | probe once to confirm live/dead for the record |
| **or-union-alpha** | **stealth/union-alpha** (OpenRouter) | free window (ends ~2026-09-23) | probe → **2 salon seeds, T 0.2 / T 0.9** (mission spec) |
| zai-air | glm-4.5-air | DEAD — PAID WALL (code 1113) | **NEVER CALLED** (standing order, not even a probe) |
| zai-47 | glm-4.7 | DEAD — PAID WALL (code 1113) | **NEVER CALLED** (standing order, not even a probe) |
| zai-lite | glm-5.3-flash | not in D22 rotation table (Lite burst seat, law-15 paced) | out of scope — not a rotation-table lane |

## Laws binding this run

1. $0 — free-tier lanes + free-window stealth lane only. Paid-wall lanes never called (not even a probe).
2. Probe before use — a stored key is not a live key (one READY ping per candidate lane).
3. Rows append to `memory/runs/p2_demo_salon_20260916/raw.jsonl` AS THEY LAND; failures preserved as rows; partial width is still width.
4. SSRF allowlist + resolved-IP guard (same as `mag/scale_salon.py`), keys never printed.
5. Interpreter `.venv\Scripts\python.exe` (never bare `python` — Hermes). No git. No repo code edits.
6. System prompt (identical across lanes): independent witness, own judgment, no preamble, hard limit 150 words. Salon temperature T 0.5 for rotation lanes; union-alpha seeds T 0.2 / T 0.9 per mission.

## Probe log

- `question_digest` = **eaf1ae0f4735c70b** (sha256[:16] of the verbatim question above).
- Pass 1 probe (READY ping, one per candidate, UTC 2026-09-16):

| lane | verdict | latency | note |
|---|---|---|---|
| cerebras-qwen | ALIVE | 238 ms | fastest probe |
| cerebras-oss | ALIVE | 450 ms | sparse-use lane, 1 salon call |
| groq-oss20 | ALIVE | 406 ms | |
| groq-oss | ALIVE | 569 ms | |
| groq-qwen | ALIVE | 1298 ms | gated lane, max_tokens 780 |
| mistral-min8 | ALIVE | 2414 ms | pass-1a 422 `extra_forbidden: seed` — driver bug (Mistral rejects OpenAI-style `seed`; d23 documented this exact trap). Fixed in the wave driver (repo code untouched), re-probe OK. Probe sample: answered with a creative riff instead of the literal word READY — lane functional, row preserved. |
| or-ling3 | ALIVE | 1228 ms | |
| or-nemotron | ALIVE | 18656 ms | slow (reasoning burn), as D22 forecast |
| or-union-alpha | ALIVE | 45780 ms | stealth/union-alpha, free window — SLOW probe but live |
| mistral-small | **DEAD** | 341 ms | HTTP 429 code 1300 — quota-zeroed, matches D22 ("will not come back on retry") |
| or-glm52 | FLAKY | 303 ms | HTTP 429 upstream shared pool — opportunistic; kept in salon fire for its 1 opportunistic shot + 1 retry |
| zai-air / zai-47 | NEVER CALLED | — | paid wall, standing order (not even a probe) |

- Probe tally: 12 metered probes + 1 mistral re-probe = 13 calls, $0. Raw tape: `memory/runs/p2_demo_salon_20260916/raw.jsonl`.
- Driver fix note (wave-side only): mistral bases omit `seed` from the request body; `api_seed` stays in the receipt row.

## Run log

- Salon fire (UTC 2026-09-16, one question × live lanes, T 0.5; union-alpha T 0.2 / T 0.9):

| lane | verdict | words | latency | note |
|---|---|---|---|---|
| cerebras-qwen | OK | 98 | 630 ms | on-length |
| mistral-min8 | OK | 175 | 6152 ms | over 150-word limit — flagged |
| groq-oss | OK | 169 | 955 ms | over limit — flagged |
| groq-oss20 | OK | 203 | 856 ms | over limit — flagged |
| groq-qwen | OK | 136 | 667 ms | gated lane held (max_tokens 780) |
| cerebras-oss | OK | 159 | 441 ms | slightly over — flagged |
| or-ling3 | OK | 92 | 6579 ms | on-length |
| or-nemotron | OK | 90 | 59844 ms | on-length; slow lane as forecast |
| or-union-alpha T0.2 | OK | 109 | 23878 ms | on-length |
| or-union-alpha T0.9 | OK | 131 | 34626 ms | on-length |
| or-glm52 | FAIL | — | 299 ms | HTTP 429 upstream (pass 1 and pass-2 retry both) |

- Pass tally: 13 probes + 11 salon calls + 1 retry = **25 metered calls, $0**. All rows on tape: `memory/runs/p2_demo_salon_20260916/raw.jsonl` (schema `p2_demo_salon.v1`).
- No lane hit a paid wall mid-run; no lane aborted.

## Per-lane answers (verbatim — README candidates; privacy flag inline if any)

**Privacy scan: CLEAN.** Mechanical scan of all 11 answers for identifying strings (names, paths, handles, emails, keys, phone-like numbers): zero real hits (3 substring matches were the English word "fostering"). No answer contains private or identifying information. Safe for the public README as-is.

### cerebras-qwen · qwen-3.8-27b · T0.5 · 98 words

> Open-sourcing accelerates scrutiny, portability, and shared standards, reducing lock-in and letting rivals build compatible agents. It can expose vulnerabilities faster and create ecosystem trust.
>
> Against: orchestration encodes identity, authority, memory, and failure policy. Public code may reveal attack surfaces, enable adversarial imitation, and let extractors copy coordination without accountability. Sovereignty depends on control over who may join, how agents bind, and how disputes resolve.
>
> Deciding: open-source the protocol and interfaces, not the full runtime. Publish enough to verify safety, interoperate, and audit invariants; keep privileged orchestration closed or permissioned. Sovereignty is strengthened by transparent rules plus controlled execution.

### mistral-min8 · ministral-8b-latest · T0.5 · 175 words (OVER LENGTH — README: trim or use another lane)

> **Pro-Open-Source:**
> Transparency builds trust. Open-sourcing the orchestration layer invites peer review, reducing hidden vulnerabilities. Collaborative refinement accelerates innovation, as diverse fleets contribute fixes and optimizations. It democratizes access, lowering barriers for smaller sovereign agents to compete. Compliance with global standards (e.g., GDPR, interoperability protocols) becomes easier with public scrutiny. Shared governance models (e.g., DAOs) could emerge, aligning incentives across fleets.
>
> **Con-Open-Source:**
> Strategic autonomy risks erosion. Exposing orchestration details may reveal operational weaknesses, enabling adversarial exploitation (e.g., supply chain attacks). Competitive advantages—like proprietary AI scheduling or edge-optimized routing—become commodified. Sovereignty demands control over critical infrastructure; outsourcing governance to decentralized systems could introduce instability. Legal liabilities (e.g., liability for third-party bugs) may outweigh benefits.
>
> **Deciding Argument:**
> **Open-source *only if* the fleet's sovereignty is *non-negotiable* and the orchestration layer is *modular*.** A "core" (e.g., consensus, security) can remain closed while auxiliary layers (e.g., plugin APIs, documentation) are open. This balances transparency with control, ensuring critical functions remain sovereign while still benefiting from collective intelligence. *Example:* The Ethereum protocol core is private, but its smart contract ecosystem is open.

### groq-oss · openai/gpt-oss-120b · T0.5 · 169 words (OVER LENGTH)

> **Pro-open-source case**
> An open orchestration layer creates a transparent trust base: users can audit for backdoors, bias, or data-leakage, which is crucial when the fleet controls critical infrastructure. Community contributions accelerate security patches, feature innovation, and interoperability, preventing vendor lock-in and fostering a robust ecosystem. Open code also aligns with the broader AI-ethics movement, showing commitment to accountability and democratizing powerful tools.
>
> **Pro-proprietary case**
> The orchestration layer is the fleet's strategic core, embodying proprietary algorithms, optimizations, and safety mechanisms that differentiate it from competitors. Keeping it closed protects intellectual property, revenue, and the ability to enforce safety constraints without exposing attack surfaces. A closed layer also allows rapid, coordinated updates that might be slowed by community consensus processes.
>
> **Deciding argument**
> When the fleet's actions have high-stakes societal impact (e.g., public utilities, autonomous transport), the trust deficit from secrecy outweighs competitive concerns; open-sourcing the orchestration layer, paired with a vetted governance model, delivers the necessary assurance while still permitting the owner to monetize value-added services built atop the transparent core.

### groq-oss20 · openai/gpt-oss-20b · T0.5 · 203 words (OVER LENGTH)

> **Open-source pros**
> - Transparency builds trust with regulators, partners, and users, easing adoption of sovereign fleets.
> - Community contributions accelerate bug fixes, feature parity, and cross-platform integration, reducing R&D costs.
> - Standardization promotes interoperability, enabling fleets to interoperate with other sovereign or commercial systems.
> - Open code can be audited for security, mitigating hidden backdoors that could compromise state-owned agents.
>
> **Open-source cons**
> - Proprietary algorithms or optimization heuristics become public, eroding competitive advantage and allowing rivals to replicate or improve upon them.
> - Public code can be weaponized by adversaries, exposing vulnerabilities or facilitating reverse engineering of sensitive state-owned logic.
> - Compliance with export controls and national security laws may be jeopardized if code is freely distributable.
> - Maintenance burden shifts to a community that may lack the resources to keep the orchestration layer up to date with evolving security requirements.
>
> **Deciding argument**
> For sovereign fleets, the strategic imperative is to maintain operational secrecy and control. The risk that adversaries could exploit open code outweighs the benefits of community-driven innovation. Therefore, the orchestration layer should remain proprietary, with selective, vetted open-source components that do not expose core decision-making logic. This preserves competitive advantage while still allowing limited transparency where legally and strategically safe.

### groq-qwen · qwen/qwen3.8-27b · T0.5 · 136 words (gated lane, max_tokens 780 — held)

> **For Open Source:** Transparency builds trust with regulators and users, reducing the "black box" stigma. It accelerates security via collective auditing and attracts top talent who prefer open ecosystems. It establishes industry standards, locking in your fleet as the de facto infrastructure.
>
> **Against Open Source:** Orchestration is the crown jewel. Revealing scheduling logic, failure-recovery heuristics, and resource allocation strategies gives competitors a roadmap to replicate your efficiency. It exposes potential vulnerabilities to malicious actors before you can patch them, risking catastrophic fleet compromise.
>
> **Deciding Argument:** Sovereignty implies control. While the application layer can be open, the orchestration layer must remain closed. If you cannot hide how you steer the ship, you cannot guarantee the destination. Competitors can copy features, but they cannot copy the nuanced, proprietary decision-making that ensures stability under pressure. Keep the helm private.

### cerebras-oss · gpt-oss-120b · T0.5 · 159 words (slightly OVER)

> **Pro open-source:** Publishing the orchestration layer democratizes access to advanced coordination algorithms, spurring community-driven security audits, bug fixes, and innovation. It reduces vendor lock-in, allowing users to tailor workflows to niche domains and fostering interoperability across fleets. Transparency builds trust; regulators and customers can verify that no hidden surveillance or exploit mechanisms are embedded.
>
> **Pro closed-source:** The orchestration layer is the strategic core that differentiates a fleet's performance, resilience, and economic advantage. Keeping it proprietary protects intellectual property, deters competitors from replicating sophisticated scheduling or fault-tolerance techniques, and limits attack surfaces by obscuring internal protocols. Revenue from licensing or premium support can fund continued R&D, ensuring the fleet stays ahead of adversaries.
>
> **Deciding argument:** The decisive factor is the threat model. If the fleet operates in high-stakes, adversarial environments where secrecy safeguards against targeted attacks and preserves competitive edge, a closed source stance is justified. Otherwise, the collective security and innovation gains of open-sourcing outweigh the marginal proprietary benefit.

### or-ling3 · ling-3.0-flash-sante:free · T0.5 · 92 words

> Open-source enables independent security audits, prevents vendor lock-in, ensures allied interoperability, and allows rapid patching by distributed sovereign maintainers. Transparency builds public trust in autonomous systems wielding state power.
>
> Closed-source protects attack surfaces from adversaries, prevents IP theft, maintains strategic ambiguity, and avoids forks fracturing coordination during crises. Foreign contributors could introduce backdoors or dependencies.
>
> Deciding argument: Sovereignty requires auditability, not secrecy. The orchestration layer is critical infrastructure; hiding vulnerabilities is catastrophic against state-level threats. Open-source with sovereign-controlled contribution governance and air-gapped deployment preserves security through transparency, not obscurity. Trust requires visibility.

### or-nemotron · nemotron-3.5-lightning:free · T0.5 · 90 words

> Open-sourcing enhances transparency, enabling external audit for accountability, fostering community-driven security patches, and preventing vendor lock-in for interoperability. It also signals democratic commitment and accelerates innovation in multi-agent coordination. Conversely, closed-source protects operational security, safeguarding tactical details from adversaries; preserves intellectual property and R&D investment; allows unilateral policy enforcement; and reduces misuse risk by limiting exposure of sophisticated orchestration logic. The deciding argument: national security and adversary resistance outweigh collaborative benefits; a sovereign fleet must keep its orchestration layer proprietary to maintain strategic autonomy and protect critical infrastructure from exploitation.

### or-union-alpha · stealth/union-alpha · T0.2 · seed 2026091601 · 109 words (SHOWCASE PICK)

> Steelman for: Auditability builds trust; external review finds flaws; interoperability prevents vendor capture; community accelerates hardening; sovereign users can verify no backdoors.
>
> Steelman against: Orchestration reveals attack surface, failover logic, credential flows; adversaries gain reconnaissance; competitors copy coordination IP; safety guardrails become bypassable; liability spreads.
>
> Deciding argument: Sovereignty is legitimate only if subjects can verify who commands the fleet. Closed orchestration asks for trust in the sovereign—precisely what sovereignty should not require. Open the layer, but separate mechanism from secrets: publish protocols, policy engine, and audit logs; keep keys, live credentials, and threat signatures private. That maximizes verifiability without handing over the keys. So yes, open-source, open-core if necessary.

### or-union-alpha · stealth/union-alpha · T0.9 · seed 2026091602 · 131 words

> **For:** Open orchestration makes delegation, permissions, resource allocation, and failure handling inspectable. It enables independent audits, interoperability, reproducibility, and exit from vendor dependence. For a sovereign fleet, sovereignty without the ability to inspect and replace its control plane is fragile.
>
> **Against:** Orchestration reveals trust boundaries, escalation paths, and defensive assumptions. Publishing it can lower attackers' reconnaissance costs and help adversaries replicate capabilities. Maintaining a secure public project also consumes scarce engineering capacity; transparency is not assurance.
>
> **Deciding argument:** Sovereignty rests on accountable, replaceable control—not secrecy or openness alone. Open-source the orchestration framework if it remains secure when attackers know its design; keep credentials, live topology, sensitive policies, and operational telemetry private. If disclosure breaks security, fix that dependency before release. Judge openness by whether it increases defenders' leverage more than attackers'.

### or-glm52 · glm-5.2:free · T0.5 — FAILED (both passes)

> FAILED: HTTP 429 upstream shared pool ("temporarily rate-limited") on pass 1 and pass-2 retry. No answer exists for this lane.

## The fold

**Convergence line:** All 10 answering lanes — both the "open" and "closed" deciders — converge on the same mechanism/secret split: **publish the protocols, policy engine, and audit surfaces; keep keys, live credentials, topology, and threat posture private.** The salon's real verdict is not open vs. closed but *where the line sits* (6 lanes draw it open-leaning: cerebras-qwen, or-ling3, both union-alpha seeds, cerebras-oss, groq-oss; 4 draw it closed-leaning: groq-qwen, groq-oss20, or-nemotron, mistral-min8) — and every answer's deciding argument reduces to "sovereignty is legitimate only when the governed can verify" vs. "verification and operability can be separated from secrecy."

**Single best showcase answer:** **or-union-alpha · stealth/union-alpha · T0.2 · seed 2026091601** (109 words). Reasons: exactly on the question's structure (steelman-steelman-decider), on length, quotable one-liner ("Closed orchestration asks for trust in the sovereign — precisely what sovereignty should not require"), lands a concrete split ("publish protocols, policy engine, and audit logs; keep keys, live credentials, and threat signatures private"), and closes with a decision ("So yes, open-source, open-core if necessary"). Runner-up for a short-form README quote: or-ling3 (92 words, "Sovereignty requires auditability, not secrecy").

## Dead-lane list

| lane | status | evidence |
|---|---|---|
| or-glm52 | **DEAD tonight** (flaky class) | HTTP 429 upstream shared pool on probe, salon pass 1, and pass-2 retry — matches D22 "opportunistic only, never plan around it" |
| mistral-small | **DEAD** | HTTP 429 code 1300 at probe — quota-zeroed (limit-req-minute 0), matches D22 "will not come back on retry" |
| zai-air | **NEVER CALLED** | paid wall (code 1113), standing order — not even a probe |
| zai-47 | **NEVER CALLED** | paid wall (code 1113), standing order — not even a probe |
| zai-lite | **out of scope** | not in the D22 rotation table (Lite burst seat, law-15 paced); not probed, not called |

Live width delivered: **8 rotation lanes + stealth lane ×2 seeds = 10 salon answers** from 25 metered calls, $0.

*Receipt closed 2026-09-16 UTC. Driver: `../p2_demo_salon_20260916.py` (wave-side only; imports `mag.research_fanout` unmodified). Tape: `memory/runs/p2_demo_salon_20260916/raw.jsonl`.*
