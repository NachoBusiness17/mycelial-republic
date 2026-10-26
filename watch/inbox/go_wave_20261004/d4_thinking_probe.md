# d4_thinking_probe - the DeepSeek v4 omission default, settled by measurement

## VERDICT (ractor: this is the line)

**DeepSeek v4 (deepseek-v4-flash) THINKS BY DEFAULT: with the thinking
parameter OMITTED the model returned 70 chars of reasoning_content and
18 reasoning_tokens on a one-word ask. providers.yaml:367-371 was RIGHT
("DeepSeek v4 defaults thinking ON"); tools/ds_workhorse.py's "omitting
it IS the off state (AH10 law)" was WRONG and now carries a dated
erratum in place (lines 88-104). a08-rails-laws r5's quoted side
(providers.yaml ON-default) is the confirmed side; a06-sacred-cow#3's
operative mechanism claim ("route_chat keeps thinking off BY OMISSION")
is the refuted side.**

- Probe: 2026-10-04, lane A d4 (go_wave), script landed beside this
  receipt as `d4_probe.py`, run via `.venv/Scripts/python.exe
  watch/inbox/go_wave_20261004/d4_probe.py` (command + bytes below).
- Endpoint: `https://api.deepseek.com/v1/chat/completions`, Bearer
  DEEPSEEK_API_KEY from .env (same auth pattern as tools/ds_workhorse.py
  and mag/route_chat.py's deepseek lane).
- Model: `deepseek-v4-flash` (providers.yaml canonical v4 name, verified
  live in memory/runs/route_chat/usage.jsonl rows).
- Ask (identical all arms): "Reply with the single word: pong";
  max_tokens 512, temperature 0.3, stream false. ONLY the thinking key
  varied. 3 asks total (one per arm, first run unambiguous, no repeats;
  cap was 6). Spend: 88 prompt + 38 completion tokens, ~$0.00007 at the
  ds_workhorse flash rates ($0.27/M in, $1.10/M out) - 3 orders under
  the $0.10 cap.

## The contradiction, byte-exact as banked

- a08-rails-laws r5 (memory/runs/mickey17_v2/runs/run-0/lanes/
  a08-rails-laws.json, idem configs/providers.yaml#d42c9d8637d2), quote:
  "DeepSeek v4 defaults thinking ON; reasoning tokens eat max_tokens and
  small budgets return EMPTY content" - and its claim names the split:
  "providers.yaml:367 says thinking defaults ON, tools/ds_workhorse.py
  :55-56 says omitting the thinking object IS the off state".
- a06-sacred-cow#3 (a06-sacred-cow.json, key ee225394e567), claim:
  "route_chat.py:127-133 keeps thinking off BY OMISSION and never reads
  disable_thinking, so if the config comment is right, mechanical on the
  deepseek lane silently runs thinking-ON". Its negative restates:
  "the omission-default contradiction ... stands unruled".
- Underlying wrong source byte (tools/ds_workhorse.py:86-87 pre-erratum;
  the rows cite 55-56 from before the 2026-10-04 docstring rewrite grew
  the file): "# thinking-off: the v4 family disables reasoning unless a
  thinking object is present; omitting it IS the off state (AH10 law)."

## Arm configs and measured outputs (raw, byte-quoted from the run)

Command: `./.venv/Scripts/python.exe watch/inbox/go_wave_20261004/d4_probe.py`
(moment 2026-10-04, single invocation, exit 0)

| arm | thinking key on the wire | finish_reason | content | reasoning_content chars | reasoning_tokens (usage.completion_tokens_details) | completion_tokens |
|---|---|---|---|---|---|---|
| 1 omitted | none (key absent from body) | stop | "pong" | 70 | 18 | 21 |
| 2 disabled | `{"type": "disabled"}` | stop | "pong" | 0 | (block absent from usage) | 2 |
| 3 enabled | `{"type": "enabled"}` | stop | "pong" | 46 | 12 | 15 |

Raw usage blocks (verbatim):
- omitted: `{"prompt_tokens": 38, "completion_tokens": 21, "total_tokens": 59, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 18}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 38}`; reasoning head: `The user wants me to reply with the single word "pong". That's simple.`
- disabled: `{"prompt_tokens": 12, "completion_tokens": 2, "total_tokens": 14, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12}` (no completion_tokens_details at all)
- enabled: `{"prompt_tokens": 38, "completion_tokens": 15, "total_tokens": 53, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 12}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 38}`

Arm 3 is the sanity arm: it proves the param drives the state in both
directions, so arm 1's reasoning is the default state, not a param echo.

## Erratum location (landing 1)

- Appended dated erratum comment to `tools/ds_workhorse.py` immediately
  after the false comment (now lines 88-104; the false lines 86-87 are
  untouched - append, never rewrite). File re-parsed OK after the edit
  (`python -c "import ast; ast.parse(...)"` -> PARSE OK).
- The wrong row itself (a06-sacred-cow#3) is NOT rewritten; this receipt
  is its erratum carrier, per the append-never-rewrite law.

## Consequences the fold must carry (measured, not judged)

1. ds_workhorse.py `ask()` still omits the thinking key: every
   deepseek-v4 batch it has run rode thinking-ON by default (including
   the go_wave "uncapped, thinking-off" ds arm re-fire claim in
   ds_workhorse.md item 6, unless that arm rode route_chat mechanical).
   One-line body fix owed to the a10-ds-batches owning lane.
2. `mag/inference_budget.py` FAMILY_TABLE deepseek row (lines ~70-96):
   `thinking_control={}` + `thinking` in `forbidden_keys` means the
   budget harness strips the off-switch and sends the default = ON.
   Same wrong-source lineage ("harvested from tools/ds_workhorse.py
   :50-60 ... thinking-off via omission"). Fix owed there too.
3. `corpus/steal/MASTER_MICKEY17_V2.md` D4 (lines 174-177) held the
   contradiction "out of GO pending the A/B ... winner banked to
   memory/runs/route_chat/usage.jsonl". This probe IS that A/B; the
   winner is providers.yaml's comment. The conditional ruling can close.
4. route_chat's mechanical depth (post-fix) already sends explicit
   `thinking:{type:disabled}` on the deepseek lane, so the front door is
   correct as wired; the "~10-15x cheaper" providers.yaml claim was not
   re-measured here (out of scope) but its direction is confirmed
   (21 vs 2 completion tokens on the same ask).
5. The historical ok=false empty-content smoke rows and the sacred-cow
   arm-2 zero-content rows stay consistent with the ON default:
   reasoning eating max_tokens is exactly what the default does.
