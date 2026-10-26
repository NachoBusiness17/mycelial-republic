# route_chat GO wave receipt - lane 1 (route-chat), 2026-10-04

Fold: corpus/steal/MASTER_MICKEY17_V2.md section 9 GO item 1. Evidence rows:
memory/runs/mickey17_v2/runs/run-0/lanes/a08-rails-laws.json (r1-r10) and
a06-sacred-cow rows #0/#3. Executor: lane 1 of the coordinator-partitioned wave.
All numbers below are byte-backed by the command shown next to them.

## Files touched

- mag/route_chat.py (edited)
- tests/test_route_chat_fence.py (new, 5 tests)
- tests/test_route_chat_banks.py (new, 2 tests)
- tests/test_route_chat_depth.py (new, 4 tests)
- watch/inbox/go_wave_20261004/route_chat.md (this receipt)

Nothing else touched. No commits made (coordinator commits).

## Sub-item 1: docstring claim scoped (a06-sacred-cow#0/#3, a08 r6/r7/r10)

route_chat docstring now reads: arm 1 (cow- ids, 4 asks) 4/4 complete with
zero AH10 failure modes, but arm 2 (cow2- ids, 10 asks) banked 2/10
ZERO-CONTENT rows at exactly the 16000-token cap; the earlier "zero AH10
failure modes" headline was arm-1-only and "16K+" is not a safe design budget
(7/14 probe rows pinned at or over the 16K cap); design asks need 32K+ or a
smaller ask. The unscoped claim previously lived at mag/route_chat.py:94-98
(185-line tree).

## Sub-item 2: disable_thinking wired, reasoning_content fallback fixed, depth enum validated (a06-sacred-cow#3, a08 r5)

- disable_thinking: route_chat now reads the lane config flag. mechanical
  depth on a lane carrying disable_thinking: true puts
  thinking:{type:disabled} on the wire (the config's own documented wire
  form, providers.yaml deepseek block); depth="design" overrides with
  thinking:{type:enabled}. Previously the flag had zero hits in the module
  (a08 r5 grep).
- reasoning_content: line 148 fallback was msg.get("reasoning"), a dead key -
  the openai_compat vendor field is reasoning_content. Fixed.
- depth enum: anything outside {mechanical, design} now raises ValueError
  before any lane resolution or network. Previously a typo'd depth silently
  rode mechanical.

## Sub-item 3: tests/test_route_chat_fence.py landed (a08 r2 steal, r7 steal)

The 5 executed offline checks from a08 r2/r7 as pytest cases: dormant saelis
B2-133 raise, http-scheme refuse, localhost resolving to loopback refused
(match on "non-public", not a pinned IP, so it holds on hosts that resolve
localhost to 127.0.0.1), host-mismatch refuse, unknown-lane raise. Offline by
construction: gate and unknown-lane raise before any DNS; scheme/host refuse
before resolution; the loopback case resolves only localhost.

## Sub-item 4: tests/test_route_chat_banks.py landed (a08 r6 steal)

Hollow-200 regression per the founding evidence pattern
(memory/runs/hermes_burn/usage.jsonl line 1151, ok:true at content_chars:1,
finish_reason length): a mocked 200 with content "x", finish_reason "length"
must bank an ok:false row. Asserts the full banked row (ok false,
content_chars 1, finish_reason length, lane, model, tokens). Plus a second
case for sub-item 6 (exception path banks an error row). Fully offline:
fence, keys, DNS, urlopen patched; bank sandboxed to tmp_path.

## Sub-item 5: tests/test_route_chat_depth.py landed

4 cases: unknown depth raises ValueError; mechanical on the real deepseek
lane (disable_thinking: true in configs/providers.yaml) wires
thinking:{type:disabled} into the captured request body; design wires
thinking:{type:enabled}; a lane without the flag sends no thinking key.

## Sub-item 6: exception-path _bank row (a08 r10 steal)

route_chat is now a thin wrapper (depth enum check, then try/except) over an
unwrapped _route body. Any exception escaping the call (fence, dormant gate,
missing keys, timeouts, all-keys-failed) banks an ok:false error row (error
class name, detail truncated to 200 chars, zero tokens) and then re-raises.
Cause and evidence named in the fix comment: inspect.getsource over the
185-line tree showed _bank absent from every except path (a08 r10), contrast
tools/ds_workhorse.py which banks __ERROR__ rows. Input-validation errors
(bad depth enum) fire before the try and bank nothing: no route was attempted.

## Sub-item 7: fence TOCTOU closed (a08 r7 steal)

Cause: _fence resolved DNS once (old line 75) while urlopen re-resolved at
connect time (old line 145), so check and connect could disagree (DNS
rebinding window). Fix, not a guard branch: _fence now returns the set of
validated public IPs, and _route installs _pin_dns(host, safe) around the
key loop (restored in finally): getaddrinfo answers the lane host ONLY with
the fence-validated addresses, and a re-resolution outside the validated set
raises. SNI/cert path untouched (connect still uses the hostname; only the
address set is pinned). No other callers of _fence exist (grep over tools/ +
mag/: only unrelated markdown-fence matches).

## Sub-item 8: one real production ask routed (a08 r3 steal)

Local ollama is UP (curl -s http://localhost:11434/api/tags returned the
model list, gemma2:2b-instruct-q5_K_M present, exit 0) but its lane
(providers.yaml ollama block) is base_url http://127.0.0.1:11434/v1, which
the https-only endpoint fence refuses by design (Mimosa ruling), so per the
task fallback the ask rode the cheapest fenced lane: deepseek / v4-flash,
mechanical (dogfooding the new thinking-disabled wire), max_tokens 64.

Command (repo root, the repo venv, never bare python):

    .venv/Scripts/python.exe -c "<route_chat('In one or two sentences: why
    must a model-call front door bank a ledger row on the exception path,
    not only on parsed responses?', lane='deepseek',
    model='deepseek-v4-flash', max_tokens=64, goal='mickey17v2 GO wave
    item 1 lane 1: route_chat exception-banking rationale (non-smoke
    production ask)')>"

Model answer (real output, used by this receipt):
"Because if the ledger row is only written after a successful parse, any
exception (timeout, malformed output, provider error) leaves the call
invisible - breaking cost accounting, retry/idempotency tracking, and
auditability for exactly the calls most likely to need investigation."

Ledger proof command:

    .venv/Scripts/python.exe -c "<json census of
    memory/runs/route_chat/usage.jsonl>"

Output: total rows 8; last row =
{"ts": "2026-10-04T08:33:00Z", "lane": "deepseek",
"model": "deepseek-v4-flash", "goal": "mickey17v2 GO wave item 1 lane 1:
route_chat exception-banking rationale (non-sm", "key_env":
"DEEPSEEK_API_KEY", "prompt_tokens": 33, "completion_tokens": 56,
"content_chars": 279, "finish_reason": "stop", "ok": true}

Note: goal is truncated at 80 chars by the bank's goal[:80]; that is why a
grep for the full phrase misses while the census shows the row. First
non-smoke goal string in the ledger (a08 r3/r4: all 7 prior rows were
smoke/substance-gate tests). Cost at ds_workhorse price truth
($0.27/M in, $1.10/M out): 33/1e6*0.27 + 56/1e6*1.10 = about $0.00007.
The live call also exercised the DNS pin end to end (validated IPs pinned,
connect succeeded).

## Test verdict (instrument: pytest, repo venv)

Command:

    .venv/Scripts/python.exe -m pytest tests/test_route_chat_fence.py
    tests/test_route_chat_banks.py tests/test_route_chat_depth.py -q

Output: "11 passed in 1.88s" (5 fence + 2 banks + 4 depth = 11; zero failed,
zero skipped, zero collection errors). Test banks are sandboxed to tmp_path;
production usage.jsonl gained only the sub-item 8 row.

## Blockers

None. Notes for the coordinator: (1) the ollama lane is structurally
unroutable through route_chat (https-only fence vs http loopback lane) - if
local janitors should ride the front door, that is an operator fence-policy
decision, not a lane-1 change; (2) the r5 steal (the $0.001 deepseek
thinking-default A/B) stays HELD per the fold's D3/D4 note and was not run;
(3) the a06 steals about PRIORS row 8 and re-firing the two zeroed cow2 asks
belong to other lanes and were not attempted here.
