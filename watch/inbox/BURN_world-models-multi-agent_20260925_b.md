# BURN: world-models-multi-agent, 2026-09-25 (_b)

## Verdict

steal

## Evidence

The owed Agora-2 technical report was reached this pass. The prior burn's guessed paths 404'd, but the announcement anchor "Read Technical Report" points to https://agora-2.odyssey.systems/agora-2.pdf (23 pp, read 2026-09-25). arXiv holds no Agora-2 entry; the PDF is the only source.

Actor census: "up to four human-controlled entities alongside sixteen autonomous entities." Twenty actors = 4 human + 16 autonomous.

Identity persistence is architectural, not measured. Section 4.5: "Entity tokens encode appearance through categorical attributes and identity labels." Section 6.4: "All renderers receive a common reference for entity positions, identities, and interaction outcomes while retaining separate visual histories." Serving: "visual history is reset on transitions between alive and non-alive states, including respawn, and on camera discontinuities. These resets interrupt visual context while the shared world state persists."

Drift is conceded unmeasured. Limitations: "Long-horizon visual quality, agreement across views, end-to-end action adherence, and agent-policy performance remain unevaluated in this report." Table 6 caption: "these metrics do not measure autoregressive rollout accuracy." Limitations: "Errors in movement, combat, and animation predictions can accumulate as the simulation advances." Figure 3 caption: "This is a qualitative example rather than a measurement of cross-view consistency."

Measured is short-horizon only: renderer PSNR 30.11 vs 20.67 baseline on 30 clips; single-step movement accuracy 85.17% (68.17% blocked); animation mode accuracy 95.84% with predicted mode-switch rate 7.49% vs recorded 3.54%.

Fresh search (NPC identity persistence / character memory, late Sept 2026) was degraded by provider rate limits; the freshest surfaced item (Gitnux character listicle, Feb 2026) 404'd at fetch. Nothing research-grade indexed; filed owed, not synthesized.

## Steal or Vacuous

Steal; this pass closes the prior burn's owed item with a sharper answer. The report itself concedes drift across the 20 actors is unevaluated: identity persistence exists as structure (identity labels in shared server state), and long-horizon plus cross-view agreement are named unevaluated. Fleet canon: CANVAS anchors confirmed as the load-bearing mechanism, and drift measurement is an open lane nobody has shipped, ours to build.

Two new transfers. (1) The paired drift probe: report mode accuracy AND a transition-frequency delta (7.49% vs 3.54% over-switching) instead of accuracy alone; adopt as the seat-drift metric shape. (2) The dropout dose-response: any nonzero history deletion improves state-reliance, cold-start latent MSE falls 0.21082 to 0.19550 from 0% to 80% dropout, at small streaming cost; "state over history" now has a vendor curve behind it.

Also named: the single-authority world server guarantees state agreement but not perceptual agreement across seats ("independently generated images can still disagree in appearance, visibility, or event timing"). Seat-level perception drift survives arbitration; that residual is the fleet's measurement target.

## Falsifier

none proposed

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md, section 6
- watch/inbox/BURN_world-models-multi-agent_20260925.md (prior burn)
- https://odyssey.systems/introducing-agora-2 (refetched 2026-09-25; anchor extraction)
- Agora-2: An Action-Conditioned World Model for Real-Time Multiplayer Environments, https://agora-2.odyssey.systems/agora-2.pdf (fetched and read 2026-09-25)
- arXiv API, search_query=all:"Agora-2" (0 results, 2026-09-25)
- Owed: research-grade work on NPC identity persistence / character memory late Sept 2026 (search rate-limited; sole candidate URL dead)
