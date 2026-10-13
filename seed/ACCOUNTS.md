# ACCOUNTS — the access playbook (2x everything)

The estate's lanes are doubled on purpose: two accounts per provider means when one
hits its wall, the other is still fresh — and free-tier ceilings double. Two Google
accounts (call them `you-a@` and `you-b@`) are the handles. Sign up for each service
once per account. Write every key into `.env` AND its `configs/keys.json` entry
(copy the template's shape; name them `<provider>_1` and `<provider>_2`).

| service | free tier you get | the float |
|---|---|---|
| **Groq** (console.groq.com) | gpt-oss-120b/20b, fast | $0 — free tier carries real work |
| **OpenRouter** (openrouter.ai) | the `:free` model wall, doubles with 2 keys | $0; optional $5 for paid-tier models |
| **NVIDIA Build** (build.nvidia.com) | ~100 models incl. big open weights | $0 |
| **Cerebras** (cloud.cerebras.ai) | very fast small models | $0 |
| **Mistral** (console.mistral.ai) | small models | $0 |
| **Google AI Studio** (aistudio.google.com) | gemini flash models | $0 |
| **Together** (api.together.xyz) | DeepSeek-V4-Flash serverless | **$5** — months of bulk work |
| **DeepSeek** (platform.deepseek.com) | the cheapest good workhorse | **$5** — months at ~$0.43/day |

The $5 rule: float ONLY the two workhorses (DeepSeek, Together). Everything else runs
on free tiers — and when a free tier churns its models away (they will), the lane
supervisor pattern and the key audit catch it; you re-point, you don't rebuild.

**The data-tier guard before you paste anything anywhere:** read DATA_TIERS.md.
T0/T1 data never goes to free remote tiers, no matter how good the model looks.
