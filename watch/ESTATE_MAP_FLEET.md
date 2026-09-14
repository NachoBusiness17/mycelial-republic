# ESTATE MAP — FLEET (self-steal lane 3/3 · census 2026-09-02 10:41Z)
Sources: /root/.openclaw/{workspace,workspace-worker} · staging/chain.log · openclaw.json + AGENTS_ROSTER_PATCH_20260901.json · ENV_INVENTORY_GAPS_PLAN §1 · WATER_NETWORK_SPEC · SELF_STEAL_C_SEAT · HANDOFF_0600Z

## 1. WORKSPACE HOLDINGS
**Skills — workspace/skills (7 SKILL.md):**
- archivist — self-steal archivist: deref RIB first, HOT-gate claims, file receipts
- chan — Primer public square imageboard play face (/chan /keep /b)
- fireball-cycle — fireball creates a tool, water keeps cycles, convert once
- front-door — main-session per-turn contract: intent mapping, routing, salon gates
- operator-corrections — operator correction laws compiled from the failure ledger
- quixote-planner — planning doctrine: plan-as-data on Workboard, no new planner code
- ractor-cast — rotating persona-lenses (Lessig/Jung/Ellul/…), RIB-anchored, decode-gated
**MEMORY.md (24.6KB) — 9 sections:** IP lineage · standing doctrine · riddler law · deep self steal · memory-RIB · switchboard boundary · archivist+inbox doctrine · founding memory · WINDOW LAW
**USER.md — 6 directive lines:** Nacho (foste) · timezone = Windows local, never invent · sovereign mirror, iterate with what exists · /mag = DNA home · chat=heat, files=DNA, FIND→FILE→LOAD · Control UI = hypervisor for seats, not a product
**Worker organs (workspace-worker/):**
- index_fold.mjs — append-only inbox event log: index_events.jsonl = truth, INDEX.json = derived fold; add/amend/invalidate/rebuild/verify; writers never rewrite INDEX
- staging/ chain state: [chain] DONE + GLM_STAGE_DONE 2026-09-01T18:05:41Z → CHAIN_COMPLETE 18:11:41Z (watchdog-verified part sizes)
**Agent roster — 13 seats** (openclaw.json agents.entries: main/worker + roster patch list):
- 1 Sancho Overseer — trusted operator coordinator; delegates bounded work, owns control surfaces
- 2 Bounded Worker — lean delegated executor; no gateway access, cannot spawn secondary workers
- 3 Economist — capacity vs burn, mixture law, route tables, water-window gates
- 4 Research Archivist — deref-first research; canonical receipt ledger; HOT-gate enforcement
- 5 Ractor Salon — persona-lens salons on HOT steps; decode-gated public forms
- 6 Director — frontier verdicts and what-to-build calls; never labor
- 7 Hands — coding labor, fan-out probes, diffs; codex paste seat
- 8 Tail — mechanical: dedupe, link-stack, formatting, digest scrub
- 9 Swarm — bulk free-lane fan-out: harvests, smell lanes, probe loops
- 10 Moonshot — R&D under the charter; labs are studies, not raids
- 11 Game Designer — campaign/arena design; engine owns truth, LLM narrates
- 12 Memory Worker — MEMORY-RIB mapping, warm spine upkeep, deref bound checks
- 13 Elder — deterministic audit; unknown stays unknown

## 2. CUSTODY (workspace-worker/staging vaults)
vault_cold 332 GiB · vault_warm 133 GiB · **total ~465 GiB (~500 GB)**; part sizes sha-tracked in chain.log
- DSV4F 145 GiB — DeepSeek-V4-Flash-UD-Q4_K_XL, 5/5 gguf parts
- GLM53F 188 GiB — GLM-5.3-Flash-UD-Q4_K_XL, 6/6 parts + mmproj-F16
- athena_zenodo ~1 GiB — Athena-class paper + artifacts (cc-by-4.0)
- warm/Q8_0 47 GiB — gpt-oss-120b-Q8_0, 2/2 parts
- warm/ggml-org 60 GiB — gpt-oss-120b-MXFP4 (single)
- warm/ top 25 GiB — qwen2.5-coder-32b-q6_k; timesfm3 2 GiB (safetensors + manifest)

## 3. LANES
**Water census — ENV_INVENTORY §1 (12 reservoirs):**
- ZAI_API_KEY slot1 — DELETED console-side; E5 cash lane dark → new intl key needed
- ZAI_API_KEY_2 (088650) — DEAD 401 garbage; purge at container recreation
- MAG (bafc5c) — LIVE shared pool, WALLED to 09-02 12:52:28Z (1310)
- Cache (e3c505) — LIVE backup, same shared pool, same wall
- ZAI_API_KEY_PRO (e18faf) — LIVE 200, zcode primary; plan-quota work
- ZAI_API_KEY_LITE (4f8ac5) — LIVE own bucket 2K/5h · 10K/wk, 13% used → ISOLATION GATE
- deepseek — LIVE $24.13 cash, 98% cache, off-peak ½ — driver+gopher backbone
- together — LIVE E6 100% cache proven — cache-mined scut arm
- cerebras — LIVE 1M TPD free — scut reservoir (full)
- groq — LIVE 200K TPD, 87% fuel — scut reservoir
- nvidia/others — credits, unprobed — backlog
- ollama — LIVE $0 local — T0 janitor, electricity-only
**Standing crons (board-tracked):** archivist_feed_harvest every 8h (delivery defect) · procurement_hunter every 12h (delivery defect) · garden-window-watchdog every 1h ok · intel-sweep cron ok · rnd_advisor_steering armed-dormant (first fire pending)

- ARCHIVIST OWNER ROW (board action 2026-09-06, from SELF_STEAL_WINDOWS_20260901): the Archivist layer (watch/\ARCHIVIST_RECEIPTS.jsonl, schema archivist_receipt.v1, dogfood 001 Aug 31) runs autonomously WITH receipts but had no owner — OWNER: vision desk (zcode seat) until a lane claims it. Stripped-toolprofile subagent class: mitigated by seat usage law (no bulk subagents from premium sessions); falsifier = usage-meter output-ratio sweep. Cites: SELF_STEAL_WINDOWS_20260901
