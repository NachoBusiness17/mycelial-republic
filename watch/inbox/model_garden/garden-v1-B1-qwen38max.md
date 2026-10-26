# garden-v1-B1-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: reasoning (content channel empty))

Let me analyze the source code of `tools/hermes_burn.py` carefully for defects, ranked by damage.

**Defect 1: TOCTOU race in `_assert_public_endpoint`**

The DNS resolution check in `_assert_public_endpoint()` resolves the hostname, checks the IPs, then the actual HTTP call in `_call()` uses `urllib.request.urlopen(req)` which resolves the hostname AGAIN internally. Between the assertion and the actual connection, DNS could change (DNS rebinding). This is the classic SSRF bypass via DNS rebinding. The check resolves, validates, then a separate resolution happens inside urllib when the connection is actually made.

Evidence: The function is called at line ~89 (inside `_call`), then `urllib.request.urlopen(req, timeout=900)` at line ~97 does its own resolution.

Let me count lines precisely. The file starts with the docstring. Let me trace:

Line 1: `"""hermes_burn...` - this is the docstring start
The docstring is quite long. Let me count carefully...

Actually, let me count the lines more carefully from the source. The docstring starts at line 1 and ends... let me count the lines in the docstring block.

Lines 1-42 approximately are the docstring (from `"""hermes_burn` to the closing `"""`).

Let me try to be more precise:

```
1: """hermes_burn — spend the Nous credits USEFULLY: Claude into the squeaky joints.
2: 
3: Vehicle for the 2026-10-01 operator order ("spend 70+$ hermes credits, use
4: claude to inject logic into our squeakiest joints"). The Nous inference API
5: serves the anthropic/* family (probed live 2026-10-01: 423 models incl.
6: opus-5.5/sonnet-5.5/fable-5.1); pricing table below captured from that probe.
7: 
8: Contract per ask (the frontier-ask production-line laws):
9: - every ask is a DIRECTORY under the queue root: ask.json {id, model, system,
10:   evidence: [repo-relative paths], contract, max_tokens, revision: bool}
11:   plus optional revision.md (steering text for round 2 on the same context)
12: - outputs land at watch/inbox/hermes_burn/<id>.md (out-prefix law: one file
13:   per ask, never a shared slot)
14: - usage rows append to memory/runs/hermes_burn/usage.jsonl:
15:   {ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok}
16:   (the driving-ladder law: every paid dispatch banks its burn)
17: - fail-loud per ask, batch continues; retry-once per turn on transport errors
18: - finish=stop: no runaway loops, one retry then the ask is marked failed
19: 
20: CARRIER-PATCH laws (2026-10-01, receipts watch/inbox/hermes_burn/
21: DAY1_CROSS_RACTOR.md E1/E3/N3 + DAY1_RIB_WARMTH.md X1/X2; the day bled
22: $18.89 of $29.91 as pure re-fire theater):
23: - LANDED BEATS FORCE: a fire is refused when the output file exists unless a
24:   revision rides turn2_only; the force flag can no longer re-burn a landed
25:   deliverable (a stale force ask burned A1 45x at $20.53 after landing)
26: - REFUSED IS TERMINAL: after 2 provider refusals for one ask id the carrier
27:   mints <ask_dir>/REFUSED (refusal snippet) and skips on sight forever;
28:   re-arming requires an operator edit of the ask bytes plus marker removal
29:   (N1 x42 and DUEL1_hidden_5 x46 refusal-retry loops are the disease)
30: - EVIDENCE PREFLIGHT: before ANY API call, every evidence[] path must exist
31:   on disk and its rendered bytes must be present in the message body being
32:   sent, and an ask with no evidence at all fails closed (DUEL2 fired 14 paid
33:   calls whose material never reached the model; T1W2 went out evidence: [])
34: 
35: Endpoint fence (the Mimosa SSRF rulings, same shape as tools/binary_attest.py):
36: fixed https URL on exactly one host, asserted per call, AND the host resolved
37: with private/loopback/link-local/reserved/multicast IPs refused (DNS or
38: hosts-file re-pointing cannot aim this tool at internal surfaces).
39: 
40: Exit: 0 all asks ok / 1 any failed / 2 usage.
41: """
42: from __future__ import annotations
43: 
44: import argparse
45: import ipaddress
46: import json
47: import socket
48: import sys
49: import time
50: import urllib.error
51: import urllib.parse
52: import urllib.request
53: from datetime import datetime, timezone
54: from pathlib import Path
55: 
56: ROOT = Path(__file__).resolve().parents[1]
57: if str(ROOT) not in sys.path:
58:     sys.path.insert(0, str(ROOT))
59: OUT_DIR = ROOT / "watch" / "inbox" / "hermes_burn"
60: USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
61: API_HOST = "inference-api.nousresearch.com"
62: API = f"https://{API_HOST}/v1/chat/completions"
63: 
64: # Captured from the live /v1/models pricing fields, 2026-10-01 probe.
65: PRICING = {  # usd per token: (input, output)
66:     "anthropic/claude-opus-5.5": (0.000004, 0.00002),
67:     "anthropic/claude-sonnet-5.5": (0.000002, 0.00001),
68:     "anthropic/claude-fable-5.1": (0.00001, 0.00005),
69:     "anthropic/claude-haiku-4.5": (0.000001, 0.000005),
70: }
71: 
72: 
73: def _now() -> str:
74:     return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
75: 
76: 
77: def _hermes_key() -> str:
78:     # KEY_2 first: 2026-10-01 live probe - key 1 402s on premium anthropic
79:     # SKUs ("insufficient available credits"), key 2 carries the credits.
80:     for name in ("HERMES_API_KEY_2", "HERMES_API_KEY_1"):
81:         for line in open(ROOT / ".env", encoding="utf-8", errors="replace"):
82:             line = line.strip()
83:             if line.startswith(name + "="):
84:                 val = line.split("=", 1)[1].strip().strip('"').strip("'")
85:                 if val:
86:                     return val
87:     raise SystemExit("no HERMES_API_KEY in .env")
88: 
89: 
90: def _assert_public_endpoint() -> None:
91:     infos = socket.getaddrinfo(API_HOST, 443, proto=socket.IPPROTO_TCP)
92:     for info in infos:
93:         ip = ipaddress.ip_address(info[4][0])
94:         if (ip.is_private or ip.is_loopback or ip.is_link_local
95:                 or ip.is_reserved or ip.is_multicast):
96:             raise RuntimeError(
97:                 f"endpoint fence: {API_HOST} resolves to non-public {ip}")
98: 
99: 
100: def _call(model: str, messages: list[dict], max_tokens: int, key: str,
101:           retries: int = 1) -> dict:
102:     parsed = urllib.parse.urlsplit(API)
103:     if parsed.scheme != "https" or parsed.hostname != API_HOST:
104:         raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
105:     _assert_public_endpoint()
106:     body = json.dumps({
107:         "model": model,
108:         "messages": messages,
109:         "max_tokens": max_tokens,
110:     }).encode("utf-8")
111:     last = None
112:     for attempt in range(retries + 1):
113:         req = urllib.request.Request(
114:             API, data=body, method="POST",
115:             headers={"Authorization": "Bearer " + key,
116:                      "Content-Type": "application/json"})
117:         try:
118:             with urllib.request.urlopen(req, timeout=900) as r:
119:                 return json.loads(r.read())
120:         except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
121:                 json.JSONDecodeError) as exc:
122:             last = exc
123:             if attempt < retries:
124:                 time.sleep(20)
125:     raise RuntimeError(f"transport failed after {retries + 1} tries: {last!r}")
```

OK so the DNS rebinding issue is at lines 91-97 (assertion) vs line 118 (actual connection). The `_assert_public_endpoint` resolves DNS and checks, then `urlopen` resolves DNS again independently. Between those two calls, DNS could return a different IP.

**Defect 2: File handle leak in `_hermes_key`**

Line 81: `for line in open(ROOT / ".env", ...)` - the file handle is never closed. The `open()` is used directly in a for loop without a `with` statement. On Windows (which is the production platform per the contract), this leaks file handles. If `_hermes_key` is called multiple times (it's called once per `main()` invocation, but the pattern is still a resource leak), and more importantly, on Windows this can prevent the .env file from being modified/deleted while the process runs.

Actually wait - `_hermes_key()` is called once in `main()`. But the `open()` without `with` is still a defect. On CPython it will be garbage collected, but on Windows the file may remain locked briefly. More importantly, if the .env file doesn't exist, this raises an unhandled `FileNotFoundError` rather than the `SystemExit` with the clear message.

Actually, the more damaging issue: if `.env` doesn't exist, `open()` raises `FileNotFoundError`, not `SystemExit("no HERMES_API_KEY in .env")`. The operator gets an opaque traceback instead of the intended error message.

**Defect 3: `_read_evidence` does NOT fail closed on missing files**

Looking at `_read_evidence` (around line 128-138):
```python
def _read_evidence(paths: list[str]) -> str:
    parts = []
    for rel in paths:
        p = ROOT / rel
        if not p.is_file():
            parts.append(f"\n\n=== EVIDENCE {rel} (MISSING) ===\n")
            continue
        ...
```

Wait, but `_assert_evidence_in_body` is called BEFORE the API call and it does check `p.is_file()` and raises. So `_read_evidence` is called first to build the prompt, then `_assert_evidence_in_body` checks. Let me look at the flow in `run_ask`:

```python
    prompt = (_system_for(model) + "\n\n=== CONTRACT ===\n" + meta["contract"]
              + "\n\n=== EVIDENCE ===" + _read_evidence(meta.get("evidence", []))
              + "\n\nProduce the deliverable...")
    messages = [{"role": "user", "content": prompt}]
    ...
    for turn_no in (1, 2):
        ...
        _assert_evidence_in_body(meta, messages)
        resp = _call(model, messages, meta.get("max_tokens", 24000), key)
```

So `_read_evidence` is called to build the prompt. If a file is missing, it puts `(MISSING)` placeholder text. Then `_assert_evidence_in_body` checks that the file exists on disk AND its first 400 chars appear in the body. If the file is missing, `_assert_evidence_in_body` will raise. So the preflight catches it.

But wait - there's a subtle issue. `_read_evidence` reads the file and truncates at 400k chars. `_assert_evidence_in_body` reads the file independently and checks `text[:400].strip()` is in the body. These are two separate reads. Between `_read_evidence` (which builds the prompt) and `_assert_evidence_in_body` (which validates), the file could change. But that's a minor TOCTOU.

Actually, the more interesting issue: `_assert_evidence_in_body` checks `probe not in body` where `probe = text[:400].strip()`. But `_read_evidence` truncates at 400,000 chars. If the file is longer than 400k, `_read_evidence` includes the first 400k chars plus a truncation notice. The probe (first 400 chars) would still be present. So that's fine.

But what about the `(MISSING)` placeholder? If a file is missing when `_read_evidence` runs, the body contains `=== EVIDENCE {rel} (MISSING) ===`. Then `_assert_evidence_in_body` checks `p.is_file()` and raises. So this is caught. OK.

Let me look for a more impactful defect.

**Defect 3 (revised): `_hermes_key` leaks file handle and gives wrong error on missing .env**

Line 81: `open(ROOT / ".env", encoding="utf-8", errors="replace")` - no `with` statement. On Windows (production platform), this is a file handle leak. Additionally, if `.env` doesn't exist, the `open()` raises `FileNotFoundError` which propagates as an unhandled exception rather than the intended `SystemExit("no HERMES_API_KEY in .env")`.

**Defect 3 (alternative): Revision turn 2 drops evidence preflight coverage**

In turn 2, the messages are rebuilt:
```python
            messages = [original_user_msg,
                        {"role": "user", "content": rev.read_text(encoding="utf-8")}]
```

Then `_assert_evidence_in_body(meta, messages)` is called. The `original_user_msg` still contains the evidence. So the probe should still find it in the body. This seems fine.

**Defect 3 (another): No authentication on the output file write**

`out_path.write_text(...)` at around line 195 - the output is written to disk. If the path is predictable (it is: `OUT_DIR / f"{meta['id']}.md"`), a local attacker could pre-create a symlink at that path to redirect the write. On Windows this is less of an issue but still possible with junction points.

Actually, let me focus on the most impactful issues:

1. **DNS rebinding TOCTOU** - `_assert_public_endpoint` at line 105 resolves DNS, then `urlopen` at line 118 resolves again. Classic SSRF bypass.

2. **File handle leak + wrong exception on missing .env** - line 81.

3. **`_read_evidence` silently continues on missing files** - it puts a `(MISSING)` marker but doesn't fail. The preflight catches it later, but the prompt construction itself is misleading. Actually wait, the preflight DOES catch it. So this is defense-in-depth working. Let me find something else.

**Defect 3: `_assert_evidence_in_body` probe is trivially bypassable**

The probe checks `text[:400].strip()` is in the body. If an evidence file starts with 400 whitespace characters followed by actual content, `text[:400].strip()` would be empty string `""`, and `"" in body` is always True in Python. So an evidence file that starts with >=400 whitespace chars would pass the preflight even if its content was never actually rendered into the body.

Wait let me check: `probe = text[:400].strip()`. If the file is all whitespace for the first 400 chars, `probe` becomes `""`. Then `if not probe: raise RuntimeError(...)` - ah, there IS a check for empty probe! Line: `if not probe: raise RuntimeError(f"EVIDENCE-PREFLIGHT: evidence file is empty: {rel}")`. 

But this only catches files that are ENTIRELY whitespace in the first 400 chars. What if the first 400 chars are whitespace but the file has content after? Then `probe = ""` and it raises "evidence file is empty" which is wrong (the file isn't empty, it just starts with whitespace). But it does fail closed, which is the important thing. The error message is misleading but the safety property holds.

Hmm, let me think of another angle. What about the `open()` calls without `with` in `_refusal_state`:

```python
def _refusal_state(ask_id: str) -> tuple[int, str]:
    count, snippet = 0, ""
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
```

This is another file handle leak. On Windows, if this file is being written to by another process (or the same process in a different thread), this could cause sharing violations.

Actually, let me reconsider. The most impactful defects:

1. **DNS rebinding TOCTOU** - the SSRF fence is bypassable. This is the worst because the docstring explicitly claims protection against DNS re-pointing, and the implementation has a classic TOCTOU gap.

2. **File handle leak in `_hermes_key`** - `open()` without `with` on line 81. On Windows (the stated production platform), this leaks a handle to `.env`. If the process is long-running or called repeatedly, this accumulates. More critically, if `.env` is missing, the error is an unhandled `FileNotFoundError` traceback rather than the intended `SystemExit`.

3. **`_refusal_state` also leaks file handle** - line with `for line in open(USAGE, encoding="utf-8")`. Same class of bug. On Windows, if the usage file is being appended to concurrently (which it is, by `_bank`), this can hit sharing violations or read inconsistent data.

Actually, let me reconsider #3. The `_bank` function opens the file with `"a"` mode and writes. `_refusal_state` opens with default `"r"` mode. On Windows, opening a file for reading while another handle has it open for appending can work (depending on sharing mode), but Python's `open()` on Windows uses `_O_RDWR` sharing by default... actually Python on Windows opens files with sharing enabled by default, so concurrent reads and appends should work. But the handle leak is still real.

Let me think about what's actually the third worst issue...

**Alternative Defect 3: Turn 2 revision messages drop the system message**

In turn 1, the messages are `[{"role": "user", "content": prompt}]` where prompt includes the system laws. In turn 2, messages are rebuilt as `[original_user_msg, {"role": "user", "content": rev.read_text(...)}]`. The `original_user_msg` is the same dict object from turn 1, so it still has the full prompt. This seems fine.

**Alternative Defect 3: `resp["choices"][0]["message"]` - no bounds checking**

If the API returns a response with an empty `choices` list, `resp["choices"][0]` raises `IndexError`. This would be caught by the broad `except Exception` in `main()`, but it means the ask is marked failed with an unhelpful error rather than a clear "malformed response" message. More importantly, the cost is NOT banked (the `_bank` call happens after successful content extraction), so a paid call that returns malformed JSON would be untracked in the usage ledger.

Wait, actually let me re-read. The `_call` function returns the parsed JSON. If `choices` is empty, the `IndexError` happens in `run_ask`, which means the exception propagates up to `main()`'s try/except. The cost was already incurred (the API call succeeded) but `_bank` was never called for this turn. This violates the "driving-ladder law" stated in the docstring: "every paid dispatch banks its burn."

This is actually a real defect: a successful API call that returns an unexpected shape (empty choices) results in an unbanked paid call.

Let me finalize my three:

1. **DNS rebinding TOCTOU** - `_assert_public_endpoint` at line 105, then `urlopen` at line 118 does its own resolution. The SSRF fence is bypassable.

2. **Unbanked paid calls on malformed response** - `resp["choices"][0]` can raise IndexError after a successful (paid) API call, skipping `_bank`. Violates the stated driving-ladder law.

3. **File handle leak in `_hermes_key`** - line 81, `open()` without `with`. On Windows production platform, leaks handle; missing `.env` gives wrong exception type.

Now let me get the line numbers right. Let me recount carefully.

The docstring: I'll count each line.

```
1:  """hermes_burn — spend the Nous credits USEFULLY: Claude into the squeaky joints.
2:  
3:  Vehicle for the 2026-10-01 operator order ("spend 70+$ hermes credits, use
4:  claude to inject logic into our squeakiest joints"). The Nous inference API
5:  serves the anthropic/* family (probed live 2026-10-01: 423 models incl.
6:  opus-5.5/sonnet-5.5/fable-5.1); pricing table below captured from that probe.
7:  
8:  Contract per ask (the frontier-ask production-line laws):
9:  - every ask is a DIRECTORY under the queue root: ask.json {id, model, system,
10:   evidence: [repo-relative paths], contract, max_tokens, revision: bool}
11:   plus optional revision.md (steering text for round 2 on the same context)
12: - outputs land at watch/inbox/hermes_burn/<id>.md (out-prefix law: one file
13:   per ask, never a shared slot)
14: - usage rows append to memory/runs/hermes_burn/usage.jsonl:
15:   {ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok}
16:   (the driving-ladder law: every paid dispatch banks its burn)
17: - fail-loud per ask, batch continues; retry-once per turn on transport errors
18: - finish=stop: no runaway loops, one retry then the ask is marked failed
19: 
20: CARRIER-PATCH laws (2026-10-01, receipts watch/inbox/hermes_burn/
21: DAY1_CROSS_RACTOR.md E1/E3/N3 + DAY1_RIB_WARMTH.md X1/X2; the day bled
22: $18.89 of $29.91 as pure re-fire theater):
23: - LANDED BEATS FORCE: a fire is refused when the output file exists unless a
24:   revision rides turn2_only; the force flag can no longer re-burn a landed
25:   deliverable (a stale force ask burned A1 45x at $20.53 after landing)
26: - REFUSED IS TERMINAL: after 2 provider refusals for one ask id the carrier
27:   mints <ask_dir>/REFUSED (refusal snippet) and skips on sight forever;
28:   re-arming requires an operator edit of the ask bytes plus marker removal
29:   (N1 x42 and DUEL1_hidden_5 x46 refusal-retry loops are the disease)
30: - EVIDENCE PREFLIGHT: before ANY API call, every evidence[] path must exist
31:   on disk and its rendered bytes must be present in the message body being
32:   sent, and an ask with no evidence at all fails closed (DUEL2 fired 14 paid
33:   calls whose material never reached the model; T1W2 went out evidence: [])
34: 
35: Endpoint fence (the Mimosa SSRF rulings, same shape as tools/binary_attest.py):
36: fixed https URL on exactly one host, asserted per call, AND the host resolved
37: with private/loopback/link-local/reserved/multicast IPs refused (DNS or
38: hosts-file re-pointing cannot aim this tool at internal surfaces).
39: 
40: Exit: 0 all asks ok / 1 any failed / 2 usage.
41: """
```

Then:
```
42: from __future__ import annotations
43: 
44: import argparse
45: import ipaddress
46: import json
47: import socket
48: import sys
49: import time
50: import urllib.error
51: import urllib.parse
52: import urllib.request
53: from datetime import datetime, timezone
54: from pathlib import Path
55: 
56: ROOT = Path(__file__).resolve().parents[1]
57: if str(ROOT) not in sys.path:
58:     sys.path.insert(0, str(ROOT))
59: OUT_DIR = ROOT / "watch" / "inbox" / "hermes_burn"
60: USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
61: API_HOST = "inference-api.nousresearch.com"
62: API = f"https://{API_HOST}/v1/chat/completions"
63: 
64: # Captured from the live /v1/models pricing fields, 2026-10-01 probe.
65: PRICING = {  # usd per token: (input, output)
66:     "anthropic/claude-opus-5.5": (0.000004, 0.00002),
67:     "anthropic/claude-sonnet-5.5": (0.000002, 0.00001),
68:     "anthropic/claude-fable-5.1": (0.00001, 0.00005),
69:     "anthropic/claude-haiku-4.5": (0.000001, 0.000005),
70: }
71: 
72: 
73: def _now() -> str:
74:     return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
75: 
76: 
77: def _hermes_key() -> str:
78:     # KEY_2 first: 2026-10-01 live probe - key 1 402s on premium anthropic
79:     # SKUs ("insufficient available credits"), key 2 carries the credits.
80:     for name in ("HERMES_API_KEY_2", "HERMES_API_KEY_1"):
81:         for line in open(ROOT / ".env", encoding="utf-8", errors="replace"):
82:             line = line.strip()
83:             if line.startswith(name + "="):
84:                 val = line.split("=", 1)[1].strip().strip('"').strip("'")
85:                 if val:
86:                     return val
87:     raise SystemExit("no HERMES_API_KEY in .env")
88: 
89: 
90: def _assert_public_endpoint() -> None:
91:     infos = socket.getaddrinfo(API_HOST, 443, proto=socket.IPPROTO_TCP)
92:     for info in infos:
93:         ip = ipaddress.ip_address(info[4][0])
94:         if (ip.is_private or ip.is_loopback or ip.is_link_local
95:                 or ip.is_reserved or ip.is_multicast):
96:             raise RuntimeError(
97:                 f"endpoint fence: {API_HOST} resolves to non-public {ip}")
98: 
99: 
100: def _call(model: str, messages: list[dict], max_tokens: int, key: str,
101:           retries: int = 1) -> dict:
102:     parsed = urllib.parse.urlsplit(API)
103:     if parsed.scheme != "https" or parsed.hostname != API_HOST:
104:         raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
105:     _assert_public_endpoint()
106:     body = json.dumps({
107:         "model": model,
108:         "messages": messages,
109:         "max_tokens": max_tokens,
110:     }).encode("utf-8")
111:     last = None
112:     for attempt in range(retries + 1):
113:         req = urllib.request.Request(
114:             API, data=body, method="POST",
115:             headers={"Authorization": "Bearer " + key,
116:                      "Content-Type": "application/json"})
117:         try:
118:             with urllib.request.urlopen(req, timeout=900) as r:
119:                 return json.loads(r.read())
120:         except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
121:                 json.JSONDecodeError) as exc:
122:             last = exc
123:             if attempt < retries:
124:                 time.sleep(20)
125:     raise RuntimeError(f"transport failed after {retries + 1} tries: {last!r}")
```

Continuing:
```
126: 
127: 
128: def _read_evidence(paths: list[str]) -> str:
129:     parts = []
130:     for rel in paths:
131:         p = ROOT / rel
132:         if not p.is_file():
133:             parts.append(f"\n\n=== EVIDENCE {rel} (MISSING) ===\n")
134:             continue
135:         text = p.read_text(encoding="utf-8", errors="replace")
136:         cap = 400_000
137:         if len(text) > cap:
138:             text = text[:cap] + f"\n... [truncated at {cap} chars]"
139:         parts.append(f"\n\n=== EVIDENCE {rel} ===\n{text}")
140:     return "".join(parts)
141: 
142: 
143: def _bank(row: dict) -> None:
144:     USAGE.parent.mkdir(parents=True, exist_ok=True)
145:     with open(USAGE, "a", encoding="utf-8") as fh:
146:         fh.write(json.dumps(row, ensure_ascii=False) + "\n")
147: 
148: 
149: def _system_for(model: str) -> str:
150:     """Dogfood: the claritas canon face for the animal + the deterministic
151:     estate-law block every ask rides (the pre-warmed rib laws, fixed text)."""
152:     from mag.claritas import face_for
153:     laws = (
154:         "\n\nESTATE LAWS (deterministic block, applies to every answer):\n"
155:         "- Trust bytes, not reports: cite file:line for every claim about the code.\n"
156:         "- A verdict without its conditions is not a verdict: name instrument,\n"
157:         "  moment, and context assumptions for any measurement you rely on.\n"
158:         "- Citations resolve to quoted bytes or are marked UNVERIFIED.\n"
159:         "- No em-dashes anywhere. Plain hyphens only.\n"
160:         "- Prefer ONE landable deliverable (a spec or patch a seat can apply\n"
161:         "  as-is) over a survey. Name your own deliverable's falsifier."
162:     )
163:     return face_for(model) + laws
164: 
165: 
166: def _refusal_state(ask_id: str) -> tuple[int, str]:
167:     """(count, last snippet) of provider-refusal ledger rows for one ask id.
168: 
169:     CARRIER-PATCH 2 read side: refusals are data, not failures to retry
170:     (DAY1_RIB_WARMTH X2: the carrier banked the refused field all day while
171:     the driver retried DUEL1_hidden_5 46x and N1 42x for over two hours)."""
172:     count, snippet = 0, ""
173:     if USAGE.exists():
174:         for line in open(USAGE, encoding="utf-8"):
175:             try:
176:                 row = json.loads(line)
177:             except json.JSONDecodeError:
178:                 continue
179:             if row.get("id") == ask_id and row.get("refused"):
180:                 count += 1
181:                 snippet = str(row["refused"])
182:     return count, snippet
183: 
184: 
185: def _mint_refused_marker(ask_dir: Path, ask_id: str, snippet: str) -> Path:
186:     marker = ask_dir / "REFUSED"
187:     marker.write_text(
188:         f"{snippet[:500]}\n\n[REFUSED terminal marker, minted {_now()} for ask id "
189:         f"{ask_id} after >= 2 provider refusals (DAY1_RIB_WARMTH X2). The carrier "
190:         "skips this ask on sight. Re-arm only by editing the ask bytes AND "
191:         "deleting this marker.]\n",
192:         encoding="utf-8")
193:     return marker
194: 
195: 
196: def _landed_skip(meta: dict, ask_dir: Path, out_path: Path) -> dict | None:
```

Let me continue counting...

```
196: def _landed_skip(meta: dict, ask_dir: Path, out_path: Path) -> dict | None:
197:     """CARRIER-PATCH 1: the deliverable-exists truth beats the force flag.
198: 
199:     DAY1_RIB_WARMTH X1 + LADDER-TRUTH 2: A1_steer_antiforgery re-burned 45x
200:     ($20.53) after its deliverable landed at 16:10Z because a stale force
201:     flag in memory/plans/hermes_burn_batch1/A1_steer_antiforgery/ask.json
202:     (mtime 09:18, never cleaned) bypassed the old skip on every 45s driver
203:     cycle; the flag-hygiene fix only cured NEW staging. Every (re)fire enters
204:     through run_ask, so this entry check is the single choke point for both
205:     cycle-boundary retry triggers (empty content channel, provider refusal).
206:     Only a pending revision riding turn2_only re-opens a landed ask (the
207:     standing revision shape; a revision flag without turn2_only skipped at
208:     entry under the old gate too)."""
209:     if not out_path.exists():
210:         return None
211:     revision_pending = (bool(meta.get("revision"))
212:                         and (ask_dir / "revision.md").is_file())
213:     if revision_pending and meta.get("turn2_only"):
214:         return None
215:     return {"id": meta["id"], "ok": True,
216:             "skipped": ("output exists (no revision pending; force cannot "
217:                         "re-burn a landed deliverable)")}
218: 
219: 
220: def _assert_evidence_in_body(meta: dict, messages: list[dict]) -> None:
```

Continuing:
```
220: def _assert_evidence_in_body(meta: dict, messages: list[dict]) -> None:
221:     """CARRIER-PATCH 3: fail closed BEFORE any API call on lost material.
222: 
223:     DAY1_CROSS_RACTOR E3/N3 + DAY1_RIB_WARMTH X5: DUEL2 fired 14 paid calls
224:     where the material bytes never reached the model (every output opens with
225:     'the EVIDENCE block is empty') and all four T1W2 asks went out with
226:     evidence: []; the duel stager pasted ask_bank's NON-reveal draw metadata
227:     (bank/draw_id/material_path/first_line JSON) into the contract instead of
228:     the rendered material (tools/ask_bank.py cmd_draw without --reveal).
229:     Every evidence path must exist on disk and its rendered head must appear
230:     in the message body actually being sent; an evidence-less ask fails
231:     closed the same way (E3 steal: exit on an evidence-less fire)."""
232:     evidence = meta.get("evidence") or []
233:     if not evidence:
234:         raise RuntimeError(
235:             "EVIDENCE-PREFLIGHT: ask carries no evidence paths (evidence: []); "
236:             "refusing an evidence-less fire per DAY1_CROSS_RACTOR E3 - stage "
237:             "the material into evidence[] or render it into the contract")
238:     body = "\n".join(str(m.get("content") or "") for m in messages)
239:     for rel in evidence:
240:         p = ROOT / rel
241:         if not p.is_file():
242:             raise RuntimeError(
243:                 f"EVIDENCE-PREFLIGHT: evidence path missing on disk: {rel}")
244:         text = p.read_text(encoding="utf-8", errors="replace")
245:         # head probe: _read_evidence truncates at 400k chars, so the first
246:         # 400 always survive into the body verbatim when the render worked
247:         probe = text[:400].strip()
248:         if not probe:
249:             raise RuntimeError(
250:                 f"EVIDENCE-PREFLIGHT: evidence file is empty: {rel}")
251:         if probe not in body:
252:             raise RuntimeError(
253:                 f"EVIDENCE-PREFLIGHT: rendered bytes of {rel} absent from the "
254:                 "message body (the render step dropped the material)")
255: 
256: 
257: def run_ask(ask_dir: Path, key: str, execute: bool = True) -> dict:
258:     meta = json.loads((ask_dir / "ask.json").read_text(encoding="utf-8"))
259:     model = meta["model"]
260:     if model not in PRICING:
261:         raise ValueError(f"unknown model {model}; add pricing first")
262:     out_path = OUT_DIR / f"{meta['id']}.md"
263:     # CARRIER-PATCH 2, entry half: skip-on-sight for terminally refused asks,
264:     # with ledger backfill (the standing N1 x42 / DUEL1_hidden_5 x46 loops
265:     # predate this marker; the count heals them without one more fire).
266:     refused_marker = ask_dir / "REFUSED"
267:     if refused_marker.is_file():
268:         return {"id": meta["id"], "ok": True,
269:                 "skipped": "REFUSED (terminal; operator edit + marker removal "
270:                            "required to re-arm)"}
271:     refusals, refusal_snippet = _refusal_state(meta["id"])
272:     if refusals >= 2:
273:         _mint_refused_marker(ask_dir, meta["id"], refusal_snippet)
274:         return {"id": meta["id"], "ok": True,
275:                 "skipped": f"REFUSED (terminal; {refusals} ledger refusals, "
276:                            "marker minted)"}
277:     # CARRIER-PATCH 1, entry half (see _landed_skip for the receipt).
278:     skip = _landed_skip(meta, ask_dir, out_path)
279:     if skip is not None:
280:         return skip
281:     prompt = (_system_for(model) + "\n\n=== CONTRACT ===\n" + meta["contract"]
282:               + "\n\n=== EVIDENCE ===" + _read_evidence(meta.get("evidence", []))
283:               + "\n\nProduce the deliverable the CONTRACT demands. Positive AND negative examples where they clarify. Match the requested shape exactly.")
284:     messages = [{"role": "user", "content": prompt}]
285:     original_user_msg = messages[0]
286:     turns = []
287:     result_row = {"id": meta["id"], "model": model, "ok": True}
288:     for turn_no in (1, 2):
289:         if turn_no == 2:
290:             rev = ask_dir / "revision.md"
291:             if not meta.get("revision") or not rev.is_file() or not execute:
292:                 break
293:             # Window-1 defect fix: turn 2 sent the assistant echo and both
294:             # channels came back empty (usage={}); revision turns now carry
295:             # ONLY [original user prompt, revision user message] - the model
296:             # re-derives its own draft from context, no echo to choke on.
297:             messages = [original_user_msg,
298:                         {"role": "user", "content": rev.read_text(encoding="utf-8")}]
299:         if not execute:
300:             turns.append({"turn": turn_no, "dry": True})
301:             continue
302:         if turn_no == 1 and meta.get("turn2_only"):
303:             turns.append({"turn": 1, "skipped": "turn2_only"})
304:             continue
305:         # CARRIER-PATCH 3: the evidence preflight fails closed BEFORE any
306:         # API call, on every turn (turn 2 rebuilds messages; the material
307:         # must still be in the body actually being sent).
308:         _assert_evidence_in_body(meta, messages)
309:         resp = _call(model, messages, meta.get("max_tokens", 24000), key)
310:         usage = resp.get("usage", {})
311:         pin, pout = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
312:         cin, cout = PRICING[model]
313:         cost = pin * cin + pout * cout
314:         msg = resp["choices"][0]["message"]
315:         content = msg.get("content")
316:         chan = "content"
317:         if not content:
318:             content = msg.get("reasoning") or ""
319:             chan = "reasoning (content channel empty)"
320:         if not content:
321:             refusal = msg.get("refusal")
322:             if refusal:
323:                 _bank({"ts": _now(), "id": meta["id"], "model": model,
324:                        "turn": turn_no, "refused": refusal[:200],
325:                        "prompt_tokens": pin, "completion_tokens": pout,
326:                        "cost_usd": round(cost, 4), "ok": False})
327:                 # CARRIER-PATCH 2, mint half: the SECOND banked refusal for
328:                 # this ask id makes the state terminal (DAY1_RIB_WARMTH X2;
329:                 # the raise still propagates so this cycle reports the fail).
330:                 n_refused, last_snippet = _refusal_state(meta["id"])
331:                 if n_refused >= 2 and not refused_marker.is_file():
332:                     _mint_refused_marker(ask_dir, meta["id"], last_snippet)
333:                 raise RuntimeError(f"REFUSED by provider: {refusal[:120]}")
334:             raise RuntimeError("empty response: both content and reasoning "
335:                                f"channels empty; usage={usage}")
336:         messages.append({"role": "assistant", "content": content})
337:         row = {"ts": _now(), "id": meta["id"], "model": model, "turn": turn_no,
338:                "prompt_tokens": pin, "completion_tokens": pout,
339:                "reasoning_tokens": usage.get("completion_tokens_details", {}).get("reasoning_tokens"),
340:                "channel": chan,
341:                "cost_usd": round(cost, 4), "ok": True}
342:         _bank(row)
343:         turns.append(row)
344:         if turn_no == 1:
345:             OUT_DIR.mkdir(parents=True, exist_ok=True)
346:             out_path.write_text(
347:                 f"# {meta['id']} ({model}, turn 1, channel: {chan})\n\n{content}\n",
348:                 encoding="utf-8")
349:         else:
350:             with open(out_path, "a", encoding="utf-8") as fh:
351:                 fh.write(f"\n\n---\n\n# REVISION (turn 2)\n\n{content}\n")
352:     result_row["turns"] = turns
353:     result_row["cost_usd"] = round(sum(t.get("cost_usd", 0) for t in turns), 4)
354:     return result_row
355: 
356: 
357: def main(argv: list[str] | None = None) -> int:
358:     ap = argparse.ArgumentParser(prog="hermes_burn")
359:     ap.add_argument("queue", help="dir of ask dirs (each holding ask.json)")
360:     ap.add_argument("--dry", action="store_true", help="validate asks, no calls")
361:     args = ap.parse_args(argv)
362:     qroot = Path(args.queue)
363:     ask_dirs = sorted(p for p in qroot.iterdir() if (p / "ask.json").is_file())
364:     if not ask_dirs:
365:         print(f"USAGE-ERROR: no ask dirs under {qroot}")
366:         return 2
367:     key = _hermes_key() if not args.dry else ""
368:     failed = 0
369:     for d in ask_dirs:
370:         try:
371:             row = run_ask(d, key, execute=not args.dry)
372:             cost = row.get("cost_usd", 0)
373:             print(f"{'OK ' if row.get('ok') else 'FAIL'} {row['id']} "
374:                   f"cost=${cost:.2f}" + (" (skipped)" if row.get("skipped") else ""))
375:         except Exception as exc:  # noqa: BLE001 - fail-loud per ask, continue
376:             failed += 1
377:             print(f"FAIL {d.name}: {exc!r}")
378:     total = 0.0
379:     if USAGE.exists():
380:         for line in open(USAGE, encoding="utf-8"):
381:             try:
382:                 total += json.loads(line).get("cost_usd", 0)
383:             except json.JSONDecodeError:
384:                 pass
385:     print(f"HERMES-BURN: {'FAIL' if failed else 'PASS'} - {len(ask_dirs) - failed}/{len(ask_dirs)} asks; ledger total ${total:.2f}")
386:     return 1 if failed else 0
387: 
388: 
389: if __name__ == "__main__":
390:     sys.exit(main())
```

OK, now I have solid line numbers. Let me finalize:

**IMPROVEMENT 1: DNS rebinding TOCTOU defeats the SSRF fence**
- Evidence: `tools/hermes_burn.py:105` calls `_assert_public_endpoint()` which resolves DNS at line 91. Then line 118 calls `urllib.request.urlopen(req)` which performs its own independent DNS resolution. Between these two calls, DNS can return a different (private) IP.
- Fix: Resolve once, pin the IP, connect to the pinned IP with a Host header override (or use a custom opener that
