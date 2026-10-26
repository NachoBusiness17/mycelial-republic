#!/usr/bin/env bash
# mcp-gap-synthesis finish-line battery (2026-10-11). Raw output = the .check.txt this tees to.
# NOTE for the record: grep exits 1 on zero matches; for the zero-hit probes
# (oauth, registry) exit 1 IS the passing evidence. Reported verbatim below.
cd "C:/Users/foste/Documents/projects/local_sovereign_agent" || exit 9

echo "=== CHECK 1: tools/mcp_parity.py (MCP-2 parity, live rerun) ==="
.venv/Scripts/python.exe tools/mcp_parity.py
echo "CHECK1_EXIT=$?"

echo "=== CHECK 2: seed MCP live probe (tools + resources) ==="
.venv/Scripts/python.exe - <<'PYEOF'
import json, subprocess
payloads = [
    {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"gala","version":"1"}}},
    {"jsonrpc":"2.0","method":"notifications/initialized"},
    {"jsonrpc":"2.0","id":2,"method":"tools/list"},
    {"jsonrpc":"2.0","id":3,"method":"resources/list"},
]
inp = "".join(json.dumps(p)+"\n" for p in payloads)
r = subprocess.run([r".venv\Scripts\python.exe","tools/seed_mcp.py"], input=inp, capture_output=True, text=True, encoding="utf-8", timeout=30)
for line in r.stdout.splitlines():
    try: msg = json.loads(line)
    except Exception: continue
    if msg.get("id") == 2 and "result" in msg:
        print("SEED_TOOLS:", [t["name"] for t in msg["result"]["tools"]])
    if msg.get("id") == 3 and "result" in msg:
        print("SEED_RESOURCES:", [res["uri"] for res in msg["result"]["resources"]])
PYEOF
echo "CHECK2_EXIT=$?"

echo "=== CHECK 3: oauth grep over MCP surfaces (zero hits expected; exit 1 = pass) ==="
grep -rin oauth mag/mcp_server.py tools/seed_mcp.py tools/gps_mcp/ mag/estate_bridge.py
echo "CHECK3_EXIT=$?"

echo "=== CHECK 4: mcp-registry integration grep (zero hits expected; exit 1 = pass) ==="
grep -rin "mcp-registry\|registry.modelcontextprotocol" mag/ tools/ --include=*.py
echo "CHECK4_EXIT=$?"

echo "=== CHECK 5: gateway auth probes (all 401 expected) ==="
echo "-- no key:"
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:8001/mcp -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' --max-time 10
echo "-- wrong key:"
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:8001/mcp -H "X-API-Key: wrong" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' --max-time 10
echo "-- .well-known/oauth-authorization-server:"
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8001/.well-known/oauth-authorization-server --max-time 10
echo "-- .well-known/openid-configuration:"
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8001/.well-known/openid-configuration --max-time 10

echo "=== CHECK 6: GPS router tests ==="
.venv/Scripts/python.exe -m pytest tests/test_gps_router_v0.py -q -p no:cacheprovider
echo "CHECK6_EXIT=$?"

echo "=== CHECK 7: MCP eval harness grep (expected: only the parity evaluate import) ==="
grep -rln "mcp.*eval\|eval.*mcp" tests/ --include=*.py
echo "CHECK7_EXIT=$?"
grep -in "eval" tests/test_mcp_parity.py
echo "CHECK7B_EXIT=$?"

echo "=== CHECK 8: pin gate presence in source ==="
grep -n "PIN GATE\|MAG_MCP_PIN_GATE" mag/mcp_server.py
echo "CHECK8_EXIT=$?"

echo "=== CHECK 9: sibling lanes dir (expected ABSENT at synthesis close) ==="
ls "watch/inbox/gala_20260925/2026-10-11_mcp-landscape/lanes/" 2>&1
echo "CHECK9_EXIT=$?"

echo "=== CHECK 10: quote byte-verification (fixed-string greps; 1 = present) ==="
grep -c "A bridge client can now file workflow-gate-grade receipts." watch/inbox/mcp_layer_status_20261010.md
echo "Q1_EXIT=$?"
grep -c "| house HTTP | POST /mcp gateway 127.0.0.1:8001, X-API-Key | full profile 42/42 | OK |" watch/inbox/mcp_layer_status_20261010.md
echo "Q2_EXIT=$?"
grep -c "the trycloudflare tunnel is the away path" tools/gps_mcp/config.gstd.json
echo "Q3_EXIT=$?"
grep -c "Unknown cost is a denial, not a free pass." watch/inbox/ractor50/mcp.md
echo "Q4_EXIT=$?"
grep -c "10/10 checks COLD JOIN PASS, 12/12 inline files hash-matched on rebuild, 1/1 pointer fetched seal-checked" watch/inbox/burn_wave_20260926/B2_181_seed_mcp_20260926.md
echo "Q5_EXIT=$?"
grep -c "GSTD allocation leg: PROVEN (100M per device wallet on chain)." watch/inbox/gstd_perimeter_build_20261010/LOOP_CLOSED.md
echo "Q6_EXIT=$?"
grep -c "means cold-of-knowledge, not cold-of-machine; a fresh git-clone join with no venv is filed as self-feed B2-539" watch/inbox/burn_wave_20260926/B2_181_seed_mcp_20260926.md
echo "Q7_EXIT=$?"
grep -c "PIN GATE (2026-09-29, wave5-repair mcp-pin-wire): tools/mcp_pin.py" mag/mcp_server.py
echo "Q8_EXIT=$?"
grep -c "estate_receipt_append" mag/mcp_server.py
echo "Q9_EXIT=$?"

echo "=== CHECK 11: em-dash scan over lane JSON (0 expected; grep exit 1 = pass; pattern is UTF-8 bytes e2 80 94) ==="
grep -c $'\xe2\x80\x94' "watch/inbox/gala_20260925/rung/lanes/mcp-gap-synthesis.json"
echo "CHECK11_EXIT=$?"

echo "=== BATTERY DONE ==="
