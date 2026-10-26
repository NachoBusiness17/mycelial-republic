# X2 — grok_sessions support in oral_law_mine (2026-09-30)

Re-fire of the 1302-dead W3l lane, solo width 1 (stagger law). NO spend, NO API calls,
NO commit. File owned: `watch/inbox/mates_leave_protocol/oral_law_mine_20260930.py`.

## What changed

`thread_body()` kept its codex path byte-intact (glob `codex_sessions/*/*/*/rollout-*-{sid}.jsonl`
first); when codex misses, it now falls back to new `grok_thread_body(sid, limit)` +
`_grok_text()` helpers, which find and parse grok threads.

## grok pool layout (surveyed, not assumed)

`corpus/oral_history/seat_pools/grok_sessions/<url-encoded-cwd>/<session-uuid>/` with
`chat_history.jsonl`, `events.jsonl`, `updates.jsonl`, `system_prompt.txt`, `summary.json`.
852 session dirs carry a parseable `chat_history.jsonl`. None of the 36
`session_index.jsonl` rows are grok (all codex): the grok pool is not yet indexed, so the
parser matches ids directly against pool dir names.

## grok event shape (learned from
`C%3A%5CUsers%5Cfoste/01a011e2-8c33-73b3-8f2c-2fb79d0cd15a/chat_history.jsonl`, then
confirmed across 25 random sessions)

One JSON object per line, discriminated by `type`:

| type | content shape | parser action |
|---|---|---|
| `system` | plain string | skip |
| `user` | list of `{"type":"text","text":...}` parts | keep, unless tagged boilerplate |
| `reasoning` | none (`summary`+`encrypted_content`) | skip |
| `backend_tool_call` | none | skip |
| `assistant` | plain string | keep |
| `tool_result` | plain string | skip |

User-turn tags: `<system-reminder>` / `<user_info>` prefixes are injected env boilerplate
(skipped, the analog of the codex `<app-context>` skip); real queries arrive wrapped in
`<user_query>...</user_query>`, unwrapped by the parser. Same truncation contract as codex:
1200 chars/turn, 14 turns, 9000-char body cap, `len(txt) > 5` floor.

## Test results (local parse only, zero API calls)

3 grok thread ids (first/middle/last of the 852):

- `019febe0-385d-7a22-b7b7-0a03187518f9` -> body_len 942 ("specialist lane for Sovereign Mag")
- `01a079e4-4e02-7c30-b102-7c833b6d3373` -> body_len 585 ("Use x_keyword_search ONCE...")
- `01a0860b-1edf-7df3-94b9-6dba5af95659` -> body_len 968 ("Use x_keyword_search... LAST 24 HOURS")

Codex intactness: index row `019fccc3-6be6-7a41-8966-dd23ee266e68` ("Fix meta agent
handler stack") still parses through the unchanged codex path, body_len 6487.

Interpreter: `.venv/Scripts/python.exe` throughout. BUDGET untouched; `main()` unrun.
