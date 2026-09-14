# CAMPAIGN SYNTHESIS — 2026-09-03 (salon folded, build order LOCKED)

Arc: operator plan (deep analysis → salon → synthesis → execute) · salon fired 15:43Z
openclaw lane (3/3 seats transport-dead: 429 congestion, dead zai-lite token, 330s gateway
timeout) · salvaged same hour on the shape-train lane (6/7 posts gated, 6 vendors) ·
clean judge refold on deepseek. Artifact: `memory/runs/salons/campaign_build_order_20260903/`
(brief_sha 564b7b6004df26ee). Receipt: `watch/salon_receipts/campaign_build_order_20260903.json`.

## THE ESCALATION (per plan law: conflicts surface, not silent)
The salon **BROKE the default order.** Blind convergence (S2/grok attacker, S4/zai cohort,
S5/ling elenchus) + the judge fold all invert explore-first into **corpus-first**: the
maze-keeper brain is the bottleneck organ; the corpus feeds it; explore feeds the maze it
inhabits. Recommendation: **adopt the inverted order** — it has 3-of-3 substantive posts
behind it and zero posts defending the default. S1/deepseek's load-bearing objection is
adopted as a gate: "open ≠ actionable" — Stage 0 triages before anything eats the vault.

## LOCKED BUILD ORDER (the muscle's route, Sep 3–20 window 15:00–01:00Z)
| Stage | Work | Window-days | Falsifiable receipt | Tri-state |
|---|---|---|---|---|
| 0 | DATA SANITY AUDIT: 228 explore signals parse schema; 46 wings intact+gated. **HALT RULE: >10% rejects → clean before feeding** | 0.5d | jq/python count = 228; 46 wings each pass substance gate; rejects < 10% | Supported (S1+S5) |
| 1 | QLoRA PACKAGING + HARDWARE PREFLIGHT (mag/lora_pipeline.py dry-run) | 0.5d | packaged .jsonl loads 512-token sample no truncation; VRAM headroom measured | QLoRA-ready claim: **Unproven until this runs** (S1) |
| 2 | WINGS-46 → CORPUS (churn queues, engine Z rides plan door) | 3d | 46 canonical corpus entries, source-tagged, gate-passed | Supported (S2/S4/S5) |
| 3 | EXPLORE-228 through fuel_feed → percolator | 4-6d | 228 signals triaged invariant/discard, zero collisions vs corpus | Supported |
| 4 | C_MAX RERUN — **only with pre-registered falsifier**: "GAP_TOO_SMALL was 429-noise" stands DISPUTED (S1: no logs shown; rerun-until-it-agrees = optionality abuse). Pre-register: loss-gap threshold + zero-429-in-run-logs, dated BEFORE the run | 2d | epoch loss curve posted vs 429-noise run; >0.02 gap reduction = falsified-or-confirmed | Disputed → conditional |
| 5 | QLoRA TRAINING (the deep compile) | 5d | adapter answers 5 held-out maze queries in-world; AzerothCore rung 4 gets the exported mind | Unproven until run |

STARVED (zero muscle, the window does not buy them): tale-re-encoder build, AzerothCore
rung-4 integration, raw-API anything on plan keys (fence: error 1113, freeze risk),
anything deepseek already does at pennies (watch, drains), off-window burn.

BIGGEST RISK (fold): **QLoRA on ungated wings corrupts the maze-keeper brain** — hence
Stage 0's halt rule ahead of everything. Secondary (S2): the window expires before Stage 1
closes if hardware preflight is skipped — measure VRAM day one, not day five.

## ROUTING CHANGES THIS SYNTHESIS IMPLIES (wired tonight)
1. `zcode-cli` headless seat — ALREADY in `mag/seat_dispatch.py` HEADLESS (campaign GO,
   fence-compliant first-party CLI, zero-quota door 15:00–01:00Z).
2. `overnight_churn.py` — `CHURN_SEAT` env (was hardcoded openclaw) so engine Z dispatches
   through the plan door.
3. `engine_reconciler.py` — bug 1: CHURN_SCRIPT pointed at nonexistent `watch/churn.py`
   (real runner: `overnight_churn.py`); bug 2: load_spec demanded dict-shaped engines,
   spec v1 ships a list. Both fixed, spec normalized, 1-based slots preserve live
   seat-g1..g4 names.
4. Engine Z in `engine_spec.json` — glm-5.3-flash plan sessions, 2 replicas (scale at T2),
   own queue `watch/engine_z_queue.jsonl` (one queue per engine — the runaway-incident law).
5. Covenant amendment — campaign exception Sep 3–20, supported-CLIs-only fence restated,
   auto-revert Sep 20 01:00Z, buyer_enabled stays false.

## PROBES (T1/T2/T3)
- T1 single headless zcode-cli dispatch: transport PONG = go. Quota-zero leg needs the
  operator's plan dashboard (my surface can't see it) — tri-stated Unproven until he reads it.
- T2 throttle at N=4 headless + the interactive session = 5 concurrent on one OAuth.
- T3 fence probe: LIVE variant (deliberate raw-API call on a plan key to watch 1113)
  **escalated, recommended AGAINST** — freeze risk is account-level and would kill the whole
  campaign for one receipt. Static variant instead: verify no plan key sits in any raw-API
  rotation (fuel_feed lanes, .env consumers). The live probe is one operator GO away.

## PRO PLAN (Step 4) — unchanged, GO-gated
Buy Pro (~$60/mo) ONLY if T2 hits a per-plan ceiling AND the queue starves, or the operator
wants the off-window 2× lane. buyer_enabled stays false until then.

## EXECUTION RECEIPTS — night of 09-03 (all measured, not asserted)
- **T1 zero-quota door: BLOCKED.** Full evidence chain in `mag/seat_dispatch.py`
  (zcode-cli entry). The standalone CLI bundle cannot resolve the coding-plan provider —
  `requireRuntimeModelConfig` throws "missing baseURL" no matter what config carries;
  the desktop exe's runtime builds it post-OAuth, the loose cjs cannot. The brief's
  "headless verified on this box" claim: **DISPUTED — no receipt exists in any exec log.**
  Also fixed en route: config.json model.main must be a `provider/model` STRING (object
  form was silently stripped); parser genuinely lacks --max-turns/--settings.
- **Door routes to reopen**: (a) ZCode Protocol app-server stdio client — a build, the
  desktop's own driving surface, 3 live instances prove the path; (b) the CLI update that
  ships the headless runtime builder. Engine Z set replicas 0 until one lands.
- **Fallback lane live**: opencode (compliant supported-CLI, 2× quota) — probe was cut by
  operator steer before firing; fire T1' on it next session.
- **T2 (N=4 throttle)**: deferred — meaningless until a plan door actually works.
- **T3 static fence check: INTACT.** No plan credential exists in any raw-API surface
  (plan rides OAuth at ~/.zcode/v2 only; seat_dispatch's reference is a comment). The
  ZAI_API_KEY_Pro/Lite .env keys are API-credit pool keys (fuel_feed lanes z_ai2/z_ai3),
  lawful to raw-call. Hygiene flag: salon_runner's `_campaign_fold()` raw-calls glm-5.3
  on the Pro credit key under the "campaign" name — lawful but blurs the fence line; rename
  suggested.
- **Stage 0 audit: PASS, no halt.** explore.jsonl: 1,337 rows, 0 unparseable, exactly 228
  open (brief claim now Supported). Wings: 124 tasks / 78 done+substantive / exactly 46
  pending (29 A + 12 B + 5 E — brief claim Supported).
- **Stage 1 hardware preflight: measured.** No NVIDIA (no CUDA), RX 5600 XT with no ROCm
  path, 68.7 GB RAM → 32B inference yes (maze-keeper lives), **QLoRA training NO on this
  box.** Stage 5 is Rocinante-gated (Oct 27) or needs a CUDA/MLX lane. Window muscle should
  flow to Stages 2–3 (corpus + explore = portable data assets, ready for whichever brain
  hardware lands). S2's biggest-risk warning validated by measurement on night one.
