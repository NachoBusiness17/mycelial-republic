## ADDENDUM 2026-09-03 — CODING PLAN CREDITS + THE CONCURRENCY ABSENCE (docs sweep, 7 pages)

Sources fetched fresh: 4 capability pages (stream-tool, function-calling, cache,
struct-output) + devpack/overview + devpack/tool/claude + 2 404 probes (rate-limit,
usages-policy paths). 

### CONCURRENCY: RECEIPTED 09-04 (operator paste of the rate-limits page; supersedes "NOT PUBLISHED" — the page exists now or lives under a path we 404-probed).
**Scope header, verbatim: "The model concurrency on this page is only applicable to API users with balance consumption. GLM Coding users please refer to the package benefits."** So this table governs our credit-pool lanes (z_ai*); the PLAN door has its own (still = package-benefits/dashboard read). Higher limits: application form.

Concurrency limits (in-flight requests, API balance users) — fleet-load-bearing rows:
- **GLM-5.3-Flash: 50** ← the legions engine; ractor-legions ceiling on the API lane is now RECEIPTED
- GLM-4-Plus: 20 · GLM-4-32B-0414-128K: 15 (confirms the old sizing chart exactly)
- GLM-5.1: 10 · GLM-5.2: 10 · GLM-4.5: 10 · GLM-4.5V: 10 · GLM-4.6V: 10
- GLM-5.3: 5 · GLM-4.5-Air: 5 · GLM-4.5-AirX: 5 · AutoGLM-Phone-Multilingual: 5 · Web-Reader: 5 · Search-Prime(-Claude): 5
- GLM-4.6: 3 · GLM-4.6V-FlashX: 3 · GLM-4.7-FlashX: 3
- GLM-4.7: 2 · GLM-5: 2 · GLM-4.5-Flash: 2 · GLM-OCR: 2
- **GLM-4.7-Flash: 1** ← the scar explained: our old cache-mining lane was concurrency-1 by design — every saturation flap this season was the vendor's ceiling, not our error
- GLM-5-Turbo: 1 · GLM-5V-Turbo: 1 · GLM-4.6V-Flash: 1 · GLM-Image: 1 · CogVideoX-3: 1
- Video models (ViduQ1/Vidu2 family): 5 each

Routing consequences: (a) swarm/legion sizing on the API lane should key on 5.3-flash @50 — a 50-replica bay is vendor-legal with balance; (b) never build a concurrent workload on 4.7-flash (1) — single-flight only; (c) 1302 rate-limit errors map to these ceilings — backoff scales with the model's row.

### THE PUBLISHED QUOTA SHAPE (coding plan)
- 5-hour rolling credits + weekly credits: Lite 2,000/10,000 · Pro 12,000/60,000 · Max 28,000/140,000. 5h quota refreshes dynamically 5h after consumption; weekly resets every 7 days.
- Credit formula: (input×mult + cached×mult + output×mult)/10,000. GLM-5.3: in 6.9 / cached 1.7 / out 24. Flash: 2.3/0.56/8. MCP calls ×1.2 each. → OUTPUT COSTS 3.5x INPUT: terse-output doctrine is credit-optimal.
- Off-peak 50% credit rate (peak = Mon-Fri 14:00-18:00 SGT).
- CAMPAIGN: daily 23:00-09:00 UNLIMITED GLM-5.3-Flash via ZCode + doubled quota on other agents. NOTE: our locked campaign window 15:00-01:00Z IS 23:00-09:00 SGT — the window was vendor-aligned all along. Night Flash muscle is literally unlimited in-window.
- Token allowance (Pro, 95% cache hit): 290-580M tok/week GLM-5.3; Flash ~5x that.

### CACHE (vendor-confirmed fleet doctrine)
Implicit auto-caching, all GLM-5.x/4.x. API-side hits ~50% discount; coding-plan credits: cached multiplier 1.7 vs input 6.9 = ~75% off. TTL: "reasonable time limits", unpublished — resident-prefix cadence should assume decay; re-prime before long gaps (prime-then-flock holds).

### TOOL/STRUCT (organs)
Tool streaming: stream=True + tool_stream=True, glm-5 family only. tool_choice: auto only. JSON mode: response_format json_object, glm-5/4.7/4.6/4.5. [1m] model suffix = 1M context. Claude door env: ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic, CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000, verified CC 2.0.14+.

---
