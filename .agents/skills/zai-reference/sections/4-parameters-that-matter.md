## 4. PARAMETERS THAT MATTER

| Param | Type | Default | Notes |
|---|---|---|---|
| thinking.type | str | "enabled" | 5.3 and 5.3-flash: ONLY "enabled". 4.7-flash: can disable |
| reasoning_effort | str | "max" | 5.3/5.3-flash: max/high/low. Only works when thinking enabled |
| temperature | float | model dep | Low=factual, high=creative. Don't pair with top_p |
| top_p | float | model dep | 0.8-0.95 recommended. Don't pair with temperature |
| max_tokens | int | model dep | 5.3: default 65536, max 131072 |
| stream | bool | false | SSE streaming |
| tool_stream | bool | false | Stream tool calls in fragments (requires stream=true) |

> RECEIPTED 09-04: thinking/effort semantics per model, native + Coding-Plan effort remap
> tables, the 5.3 no-disable 1210 (docs + lived scar), reasoning_content shape, campaign
> scoping, queued $0 pings — §10 at the bottom. Cache/tool basics: ADDENDUM 09-03 below.
