# L08: UE5 destruction tech + noir assets (agent bank, honest-degradation noted)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L08) · **Class:** RECEIPT / steal
**Closes debt:** #1 from the noir pack (The Finals' inner destruction tech), PARTIALLY: search layer was heavily degraded (built-in search 429/1302 past retry budget; DuckDuckGo/Mojeek captchas; Epic docs and fab.com JS-walled/403). The agent banked with verification labels instead of guessing.

## The Finals mechanism (labeled: leads to confirm against the DF video/article, not session-verified)

- Digital Foundry did produce the tech review + Embark tech interview (eurogamer.net / DF YouTube, Dec 2023 launch window). Entry points named; article text not retrieved this session.
- Reported mechanism (from the agent's prior reading of that coverage, unverified this session): The Finals does NOT use stock UE5 Chaos for headline destruction. Embark wrote a custom hybrid pre-fractured + runtime system: buildings authored as kits of destructible chunks/cells with baked fracture patterns, runtime damage updates structural state. Whole-building live voxelization was rejected for cost. Dedicated-server-authoritative: destruction is EVENT-replication, not state sync; debris physics GPU-assisted with aggressive despawn. Lumen interaction (destroyed geometry vs surface cache) was a stated engineering challenge.

## UE5 Chaos reality (verified against Epic docs hub via Wayback)

- Chaos destruction state does NOT replicate out of the box. Epic's networking answer is the separate experimental Networked Physics / physics prediction stack (resimulation-based). Production pattern for multiplayer: replicate discrete damage events + re-trigger local fracture, or pre-bake via Chaos Cache/Cache Manager for deterministic playback.
- Practical shape: Geometry Collections cost scales with cluster/piece count; per-building pre-fractured meshes with event-based triggering is the accepted open-city pattern, i.e. closer to Embark's approach than voxelizing the city.
- No open-source Finals clone exists (GitHub API search). Nearest: TypeDreamMoon/DreamFracture (one-click Chaos fracture + bake to Chaos Cache, cinematics-only), cem-akkaya/NetworkedPhysics (UE 5.7 tutorial), SamuelDucca/chaosathome, lefrenchywtf/RealisticDestruction. NONE carry licenses: contact authors before reuse. Commercial lead unverified: Voxel Plugin (voxelplugin.com).

## 1950s noir assets

NOT verified this session (fab.com 403, search engines captcha'd). Leads only, do not treat as confirmed: Synty POLYGON City (stylized, ~$30, not period-accurate); manual Fab searches for "1950s", "noir", "diner", "vintage car". Stays on the debt list.

## Shader repos (all three verified to exist)

- chrisloop/Unreal5_ToonShader: real, 272 stars, but 1 commit and near-empty README ("# Pic"); reverse-engineer the Content folder; reference art only.
- lexULL/UE5_ToonShader: real; university project recreating the killer7 cel shader + Kuwahara; small, undocumented, engine version unstated.
- alicepm800/Kuwahara-Filter-Plugin: real; Kuwahara in HLSL as a global shader via custom C++ module (Source/MyCustomModule/Shaders/KuwaharaFilter.usf); strongest code starting point; global-shader plugin pattern still fully supported in UE5, porting mechanical.
- Integration read: low-friction noir route = post-process material with scene-color Kuwahara variants; the plugin is the code base, lexULL the stylistic reference.

## Bottom line for the UE5 build path

Plan Embark-style architecture (per-building pre-fractured kits + event-replicated damage), not whole-city Chaos; Chaos per-building with Chaos Caches for determinism; no clone to lift; all shader repos reference-grade.

## Agent debts

DF article text unretrieved (mechanism from prior reading, flagged); Fab listings unverified; Epic numeric solver limits not pulled (JS wall).
