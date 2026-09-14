## 2. THE FLEET'S CODING PLAN CREDITS

| Plan | 5h credits | Weekly credits | $/mo |
|---|---|---|---|
| Lite | 2,000 | 10,000 | $18 |
| Pro | 12,000 | 60,000 | ~$60 |
| Max | 28,000 | 140,000 | ~$120 |

Credit formula: `(input_tok × in_mult + cached_tok × cache_mult + output_tok × out_mult) / 10,000`

| Model | Input mult | Cached mult | Output mult |
|---|---|---|---|
| GLM-5.3 | 6.9 | 1.7 | 24 |
| GLM-5.3-Flash | 2.3 | 0.56 | 8 |
| Web Search MCP | — | — | 1.2/call |

**Off-peak: 50% credits.** Peak = weekdays 14:00-18:00 UTC+8. All day weekends = off-peak.

**Weekly token capacity at 95% cache (Max plan):**
- GLM-5.3: 676M - 1.35B tokens/week
- GLM-5.3-Flash: **2.0B - 4.1B tokens/week**
