# B2-144 free-cache model map (2026-09-26)

## Verdict

LANDED, bounded: two of six provider rows verified against official docs
today (DeepSeek, z.ai), one row verified to the community-report level
(Gemini implicit caching), three rows pointed but UNVERIFIED-TODAY (Kimi
context cache, Qwen DashScope implicit cache, OpenRouter cached-provider
listing; the search lane was 429-stormed, the docs URLs are filed for the
next pass and no number is invented for them). Estate fit is real and
byte-measured: the boot/load-order prefix is roughly 15-20K tokens of
near-identical text per seat (AGENTS.md 14,099 B + FRAMEWORK_LOAD 13,309 B +
COMPASS 13,132 B + SCIENCE_MAP 12,875 B + OPERATOR_CARD 4,888 B) plus
queue/todo.md 30,014 B, all byte-stable within a day, which is exactly the
shape cache pricing rewards.

## The map

| provider | cached-input price (per 1M) | vs plain input | min prefix | verification |
|---|---|---|---|---|
| DeepSeek (deepseek-flash) | $0.003 off-peak / $0.006 peak | 2% of miss ($0.15/$0.30) | auto (context caching, no code) | official docs fetched 2026-09-26 |
| DeepSeek (deepseek-v4-pro) | $0.022 / $0.044 | 3.3% of miss ($0.66/$1.32) | auto | same fetch |
| z.ai (GLM-5.3-Flash) | $0.03 | 20% of $0.15 | auto | official docs fetched 2026-09-26 |
| z.ai (GLM-4.7-Flash, GLM-4.5-Flash) | Free | free lane already | auto | same fetch |
| Gemini 2.5 implicit cache | ~25% of input price reported | ~75% off | 1,024 tok Flash / 2,048 tok Pro, community reports say effectively ~6K | forum-corroborated, not docs-fetched today |
| Kimi/Moonshot context cache | storage fee + reduced hit price (shape known, rates UNVERIFIED-TODAY) | pointer platform.moonshot.cn | explicit cache create | UNVERIFIED |
| Qwen/DashScope implicit cache | cache-hit vs cache-write rates (shape known, rates UNVERIFIED-TODAY) | pointer help.aliyun.com model-studio | implicit | UNVERIFIED |
| OpenRouter cached providers | per-provider passthrough of upstream cache fields (shape known, rates UNVERIFIED-TODAY) | pointer openrouter.ai/docs | upstream | UNVERIFIED |

Estate workload fit and measured prefixes (bytes, this repo, 2026-09-26):
- Seat boot load order (AGENTS.md + 4 ref docs): 58,303 B, roughly 15K tokens,
  byte-stable across a session day: highest cache-hit probability of anything
  the estate sends.
- queue/todo.md 30,014 B and context-pack inputs (brief 2,182 B + bonds):
  stable for hours, rewritten daily: good intraday hit window.
- Byte-identical asks (the ZCode cache law, byte-identical prompts for cache
  hits): exact-match reuse is the strongest form and works on every provider
  above with zero prefix discipline.
Savings math, honest scale: a 15K-token boot prefix at DeepSeek peak costs
$0.0045 uncached vs $0.00009 cached per call (98% off); 1,000 boot-class calls
per day would save about $4.4/day. At z.ai GLM-5.3-Flash the same prefix saves
80% (about $0.0018/call). The estate's remote API volume is currently small
and mostly free-tier, so the practical ranking is: (1) keep hard janitor
lanes local/free, (2) route paid long-context work to DeepSeek off-peak
(weekends and all non-peak-UTC hours are half price, a lever independent of
caching), (3) z.ai paid lanes get cache-hit pricing automatically.

## Per-provider falsifiers

- DeepSeek: one call with a >1M-token-equivalent repeated prefix, read
  usage.prompt_cache_hit_tokens in the response; absence of the field or
  hit-priced billing absent means the map row is wrong. Off-peak leg: same
  call weekend vs peak-UTC Monday, factor-2 bill delta must appear.
- z.ai: one repeated-prefix call, cached-input line in usage billing; absence
  falsifies the 20% row.
- Gemini: send a >6K-token identical prefix twice and read
  usageMetadata.cached_content_token_count; zero on both falsifies implicit
  caching at our prompt sizes (the community thread's exact claim).
- Kimi / Qwen / OpenRouter: fetch the pointer URLs; if no cache price class
  exists on the fetched page, the row is wrong and the map demotes it.
- Whole map: if the byte-stable boot prefix claim fails (the 5 files churn
  within a day), the estate-fit column collapses and the map's workload
  ranking is void.

## Work done

1. Byte-measured the estate's repeated-prefix files (sizes above).
2. Fetched official pricing for DeepSeek and z.ai (2 pages, 2026-09-26);
   attempted Kimi/Qwen/OpenRouter/DeepSeek searches (429-stormed, retried),
   got one corroborating Gemini forum hit, marked 3 rows UNVERIFIED-TODAY
   instead of inventing numbers.
3. Appended 2 LINKS.jsonl rows (the two verified official sources, writer
   zcode-sw-11-b2-144).
4. Filed this receipt with per-provider falsifiers; LEDGER row; QUEUE
   pointer; INDEX registration.

## Falsifier

Map-level: any provider row whose price class cannot be reproduced from its
official page within 7 days demotes to UNVERIFIED and out of the routing
recommendation; the estate-fit claim is falsified by the boot files churning
daily (then only byte-identical-ask reuse survives). Meta: this receipt
invents no unverified number; if any UNVERIFIED row above is later quoted
with figures, those figures came from somewhere other than this receipt.

## Bibliography closed

https://api-docs.deepseek.com/quick_start/pricing (fetched 2026-09-26, full
price table read); https://docs.z.ai/guides/overview/pricing (fetched
2026-09-26, full table read); Gemini implicit caching corroborated via
discuss.ai.google.dev thread (search result, not fetched); Kimi/Qwen/OpenRouter
pointers named, unfetched (429s). Local byte sizes from this repo's tree.
