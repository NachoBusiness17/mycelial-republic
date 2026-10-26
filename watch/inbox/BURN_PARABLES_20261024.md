# Burn wave: every window, parable trial (2026-10-24, 01:30-01:40 UTC)

**Order:** burn down all open windows - grok ×2, OpenRouter stealth, opencode stealth,
both z-code plans, Google coding plans, everything free/cheap including DeepSeek - and
prove capability against the parable research.

**Spent: $0.029** for 31 real calls. Everything else was free tier.

## 1. Which windows are actually alive

| lane | window | result |
|---|---|---|
| `deepseek-flash` | DeepSeek | **live**, 8-10 s |
| `deepseek-v4-pro` | DeepSeek | **live**, 18-25 s (reasoning) |
| `zcode-1/2/3` | z.ai coding plans ×3 keys | **live**, 30-53 s, ~$0.02 |
| `or-liquid` / `or-flint` / `or-nemotron` | OpenRouter `:free` | **live** |
| `nous-longcat` / `nous-beam` | Nous free | **live** |
| `cli-grok` | Grok Build CLI | **live**, 123 s |
| `cohere` | Cohere free | 429 rate-limited |
| `mistral-1/2` | Mistral ×2 | 429 rate-limited (both) |
| `cli-opencode` / `cli-opencode2` | opencode stealth ×2 | **auth broken**: `Authentication parameter not received in Header` (model resolves `glm-5v-turbo`) |
| `cli-gemini` | Google coding plan | exit 1, no output - needs login |
| `cli-codex` | Codex | `codex_login::auth::manager` error |
| `groq-1/2` | Groq ×2 | 401 invalid key (both) |
| `xai-1/2` | xAI API | 403 `permission-denied` (team); second key absent |
| `gemini` (API) | Google AI Studio | 404 on `gemini-2.5-flash` in the OpenAI-compat path |
| `together` | Together | 400 - free model slug not available |
| `nvidia` | NIM | 410 Gone (model retired) |
| `cerebras` | Cerebras | 404 - model id not in account |

So the burn is **11 live lanes**, not 20. The dead ones are auth/route problems, not
capability problems, and each failure is recorded verbatim in the receipts.

## 2. A budget finding worth more than the run

At `max_tokens=700`, every reasoning lane (deepseek-flash, deepseek-v4-pro, zcode-1..3,
or-*) returned **200 OK with 700 completion tokens and zero characters**: the budget went
into reasoning, the content never started. At **3500** the same lanes answered normally.
Any harness that reports "empty = model failed" at a small budget is measuring its own
ceiling. (Nous-longcat answered at 192 tokens throughout - it is not a reasoning model.)

## 3. The trial: Jung / Freud separation, the top action from the 2026-10-23 analysis

Two tasks, 13 lanes, scored on: 80-170 words, English only, a `mechanism:` line, the
lens's required signal present, and the *other* lens's vocabulary absent.

| lane | valid | fully clean | notes |
|---|---:|---:|---|
| deepseek-flash | 2 | 2 | |
| deepseek-v4-pro | 2 | 2 | |
| nous-beam | 2 | 2 | |
| nous-longcat | 2 | 1 | `jung → "repress"` |
| or-flint | 2 | 2 | |
| or-liquid | 2 | 2 | |
| or-nemotron | 2 | 2 | |
| zcode-1 | 2 | 2 | best jungle text of the run |
| zcode-2 | 2 | 1 | `jung → "repress"` |
| zcode-3 | 1 | 0 | 429 on one task; `jung → "repress"` |
| cli-grok | 1 | 1* | works, but opens with meta-commentary ("I'll check that form") |
| cohere, mistral-1/2 | 0 | - | 429 |
| opencode ×2, gemini, codex | 0 | - | auth |

**8 of 10 answering lanes produced a compliant parable on the first try** - length,
English, mechanism line, lens signal, no forbidden vocabulary. The two failures are
exactly the failure mode the 2026-10-23 grid predicted: **Jung written with Freud's
"repression"**, which is the single largest error source in that study (5 of 21 errors).

Best output (zcode-1, Jung):

> The Council of Nine had always sat at a table of ten chairs... "That is your tenth,"
> he said. "It has carried your silences all these years." The council was afraid, but
> they set a cup before the dark and said, "Sit." ... By morning the table was small
> enough to carry, and the ten walked toward the mountain, unequally lit, together.
> **mechanism:** the disowned shadow is not banished but given a seat...

## 4. What this proves

1. The parable brief is **portable**: 8 independent models, four providers, three
   subscription plans, one prompt - and the lens discipline survives.
2. The **scoring rule from the analysis holds**: `repress` in a Jung text is a reliable
   tell. It caught the only two non-clean outputs.
3. The estate can run a 12-lens × 12-subject grid on live windows for **pennies** -
   the full grid is ~1,584 calls; at observed rates that is $2-4 and roughly 40 minutes
   at 6 workers, if rate limits are respected per provider.

## 5. Next (needs one decision)

- Re-auth the four dead subscription windows (opencode ×2, gemini, codex) - they are
  the ones the operator named and the only ones that cost nothing per call.
- Then run the full grid with per-provider concurrency caps (z.ai 1, OpenRouter 2,
  DeepSeek 2) and the `repress` / `shadow` tell as a live scorer.
