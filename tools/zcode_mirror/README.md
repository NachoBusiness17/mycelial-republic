# zcode-mirror (read-only ZCode session mirror over Tailscale)
Source of truth: ZCode's append-only rollout logs `%USERPROFILE%\.zcode\cli\rollout\model-io-*.jsonl` (read-only tail).
Headers (incl. set-cookie) and request bodies (system prompt/tools) are stripped before storage. ZCode is not patched/restarted.
Why not the live WS (task_stream_mirror_batch)? The desktop app (3.16.x) exposes that only over Electron IPC/its relay; the only
local WS server is `zcode --web` (packages/server/src/http.ts, /ws), which would mean launching a second ZCode server process
(optional Bearer token from env ZCODE_SERVER_AUTH_TOKEN). Not done per scope; can be added later as a second ingest source.

Run (bob):  start.ps1   | Stop: stop.ps1  (kills PID in data\zmirror.pid)
Bind: 100.125.103.60:8790 only (refuses 0.0.0.0).  Endpoints: /sessions /snapshot/{id} POST /sync /subscribe/{id} /view/{id} /trajectory/{id} /health
Phone: python zmirror_pull.py --list ; python zmirror_pull.py <sessionId>   (local copy ~/zmirror/<sid>.db)
       test flags: --truncate N (drop last N local chunks), --corrupt (force hash mismatch -> RESET)
Viewer: http://100.125.103.60:8790/view/<sessionId>  (IndexedDB cache, same HAVE/WANT protocol, JS chain verify)
MCP (not auto-registered): add to an MCP client config:
  "zcode-mirror": {"command":"python","args":["tools/zcode_mirror/zmirror_mcp.py"],"env":{"ZMIRROR_URL":"http://100.125.103.60:8790"}}
  tools: list_sessions, get_snapshot, pull_since
Rib: trajectory digests (last 8 turns, plain extraction) are written to rib_stage\<sid>.trajectory.json.
  NOT published: mag.rib_bus.publish_rib folds into the Verkle knot chain (hash-chained) -> needs Nacho's go.
  To publish after approval (PC repo):  python -c "import json,sys;from mag.rib_bus import publish_rib;t=json.load(open(sys.argv[1]));print(publish_rib(json.dumps(t)[:4000],domain='zcode_mirror',source='zcode_mirror'))" <file>
At rest: not encrypted (would need a new key/secret); protection = tailnet-only bind + NTFS ACL (owner-only) on data\.
