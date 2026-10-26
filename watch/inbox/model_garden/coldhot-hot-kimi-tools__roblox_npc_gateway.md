# coldhot-hot-kimi-tools__roblox_npc_gateway (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: `ask_lane` uses `str()` conversion on payload fields which passes through `None` as literal string "None" rather than rejecting malformed input | EVIDENCE: tools/roblox_npc_gateway.py:168-171 | FIX: validate `payload.get("player")` and `payload.get("message")` are non-None strings before `ask_lane` call, reject with 400 if missing

DEFECT 2: `receipt` function writes to shared jsonl without atomic tmp+replace (known organ violation pattern) | EVIDENCE: tools/roblox_npc_gateway.py:124-127 | FIX: write to `RECEIPTS.with_suffix(".tmp")` then `os.replace()` to final path

DEFECT 3: `Handler.do_POST` catches all exceptions and returns generic fault message, masking `json.JSONDecodeError` which should be 400 not 500-class gateway fault | EVIDENCE: tools/roblox_npc_gateway.py:188-190 | FIX: catch `json.JSONDecodeError` separately before broad `Exception` handler to return 400 with specific parse error

DEAD-CODE: `OR_API_KEY` and `OR_API_KEY_2` in `_lanes()` are unreachable aliases since `OPENROUTER_API_KEY` and `OPENROUTER_API_KEY_2` are checked first with identical env access pattern | EVIDENCE: tools/roblox_npc_gateway.py:108-111 | FIX: remove `OR_API_KEY` and `OR_API_KEY_2` from loop keys

ONE-SITTING FIX: `ask_lane` `str()` conversion defect allowing "None" strings through | EVIDENCE: tools/roblox_npc_gateway.py:168-171
