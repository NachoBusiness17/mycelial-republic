## 5. ERROR CODES (fleet-critical)

| Code | Meaning | Fleet response |
|---|---|---|
| **1302** | Rate limit (concurrency) | Backoff + retry (transient) |
| **1305** | Service overloaded | Exponential backoff (transient) |
| **1308** | Usage limit hit, resets at {time} | Wait for window |
| **1310** | Weekly/monthly exhausted | Wait for period reset |
| **1316/1317** | 5h/7d limit, no balance | Wait or top up |
| **1318-1321** | 5h/7d limit + spend cap | Wait or raise cap |
| 1309 | Coding plan expired | Renew |
| 1311 | Plan lacks this model | Upgrade |
| 1313 | Fair Usage Policy violation | Submit request to restore |
| 1113 | Insufficient balance | Recharge |
| 1210 | Invalid parameter (e.g. thinking disabled on 5.3) | Fix the param |
| 1261 | Prompt too long | Truncate |
| 1301 | Unsafe content detected | Rephrase |
