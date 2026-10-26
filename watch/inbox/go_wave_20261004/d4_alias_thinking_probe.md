# d4_alias_thinking_probe - the omission default for the ALIAS deepseek-chat

B7 filed-not-fixed sweep item 4 (2026-10-05). Companion to
`watch/inbox/go_wave_20261004/d4_thinking_probe.md` (2026-10-04, which settled
the CANONICAL name deepseek-v4-flash: thinks by default). This probe settles
the alias every ds_workhorse batch actually rides.

## VERDICT (the line)

**deepseek-chat (the tools/ds_workhorse.py:64 alias) DOES NOT THINK BY
OMISSION: the omission default is OFF.** Arm 1 (key omitted) returned 0
reasoning_content chars and 2 completion tokens - byte-identical to the
explicit disabled arm. This is the OPPOSITE default of the canonical
deepseek-v4-flash name measured 2026-10-04 (70 chars / 18 reasoning tokens on
omission). The enabled arm proves the param still drives the state on the
alias in both directions (16 reasoning tokens when explicit), so arm 1's
silence is the default state, not a param echo or an ignored field.

- Probe: 2026-10-05, lane B7 (build_wave filed-not-fixed sweep), script
  landed beside this receipt as `d4_alias_probe.py`, run via
  `.venv/Scripts/python.exe watch/inbox/go_wave_20261004/d4_alias_probe.py`
  (single invocation, exit 0, first run unambiguous, no repeats).
- Endpoint `https://api.deepseek.com/v1/chat/completions`, Bearer
  DEEPSEEK_API_KEY from .env, model `deepseek-chat`, ask identical all arms
  ("Reply with the single word: pong"), max_tokens 512, temperature 0.3,
  stream false. ONLY the thinking key varied.
- Spend: 50 prompt + 23 completion tokens = ~$0.00004 at the flash rates
  ($0.27/M in, $1.10/M out) - under the ~$0.0001 task estimate.

## Arm configs and measured outputs (raw, byte-quoted from the run)

| arm | thinking key on the wire | finish_reason | content | reasoning_content chars | reasoning_tokens | completion_tokens |
|---|---|---|---|---|---|---|
| 1 omitted | none (key absent from body) | stop | "pong" | 0 | (no details block) | 2 |
| 2 disabled | `{"type": "disabled"}` | stop | "pong" | 0 | (no details block) | 2 |
| 3 enabled | `{"type": "enabled"}` | stop | "pong" | 62 | 16 | 19 |

Raw usage blocks (verbatim):
- omitted: `{"prompt_tokens": 12, "completion_tokens": 2, "total_tokens": 14, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12}` (no completion_tokens_details)
- disabled: byte-identical to omitted.
- enabled: `{"prompt_tokens": 38, "completion_tokens": 19, "total_tokens": 57, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 16}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 38}`; reasoning head: `The user wants me to reply with the single word: pong. Simple.`

## Consequences (measured, not judged)

1. The d4_thinking_probe.md consequence 1 ("every deepseek-v4 batch ran
   thinking-ON by default") does NOT extend to ds_workhorse batches: those
   rode MODEL=deepseek-chat, whose omission default was already OFF. The
   2026-10-04 erratum + explicit `thinking:{"type":"disabled"}` in
   tools/ds_workhorse.py ask() is now proven a no-op-by-default on this alias
   (harmless, keeps the wire form canonical with route_chat).
2. The two names differ in thinking default on the same key: routing that
   swaps deepseek-chat for deepseek-v4-flash (or vice versa) changes the
   omission behavior silently. configs/providers.yaml's "DeepSeek v4 defaults
   thinking ON" is TRUE for the canonical v4 name and FALSE for this alias;
   any lane reasoning from the alias to the v4 family inherits the wrong
   default.
3. mag/inference_budget.py FAMILY_TABLE deepseek row (d4_thinking_probe.md
   consequence 2) should scope its fix to the canonical v4 names, not the
   alias: on deepseek-chat, omission is already the off state.
