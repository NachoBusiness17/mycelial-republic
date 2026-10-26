"""break-economics adjudication probes: agent_runtime part split by role + astra_v4 def check."""
import json
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
out = {}
out["parts_origin_agentruntime_anyrole"] = conn.execute("""
SELECT count(*), total(length(coalesce(json_extract(p.data,'$.text'),'')))
FROM part p JOIN message m ON m.id=p.message_id
WHERE coalesce(json_extract(m.data,'$.semantics.origin'),'')='agent_runtime'
  AND json_extract(p.data,'$.type')='text'""").fetchone()
out["parts_origin_agentruntime_by_role"] = conn.execute("""
SELECT json_extract(m.data,'$.role'), count(*), total(length(coalesce(json_extract(p.data,'$.text'),'')))
FROM part p JOIN message m ON m.id=p.message_id
WHERE coalesce(json_extract(m.data,'$.semantics.origin'),'')='agent_runtime'
  AND json_extract(p.data,'$.type')='text' GROUP BY 1""").fetchall()
out["userrole_agentruntime_messages_alltime"] = conn.execute("""
SELECT count(*) FROM message m
WHERE json_extract(m.data,'$.role')='user'
  AND coalesce(json_extract(m.data,'$.semantics.origin'),'')='agent_runtime'""").fetchone()
conn.close()

d = ROOT / "watch/inbox/astra_v4"
out["astra_v4_dir"] = sorted(p.name for p in d.iterdir()) if d.exists() else "MISSING"
hits = []
if d.exists():
    for p in sorted(d.rglob("*")):
        if not p.is_file() or p.stat().st_size > 3_000_000:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, ln in enumerate(t.splitlines(), 1):
            low = ln.lower()
            if "clarification" in low or "simulat" in low:
                hits.append(f"{p.relative_to(d).as_posix()}:{i}: {ln.strip()[:100]}")
out["astra_v4_clarification_or_simulator_hits"] = hits[:25]
print(json.dumps(out, indent=1))
