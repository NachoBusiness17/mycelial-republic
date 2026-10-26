"""break-economics byte-check instrument (2026-10-10).

Reruns the lens's two data claims with named instruments and moments:
  1. zcode db.sqlite user-turn census (mode=ro, same query shape as tools/zknot.py load())
     with the cron-template split the lens's raw count may have missed.
  2. memory/runs/hermes_burn/usage.jsonl lane aggregation.
  3. dir censuses: ractor output dir, salon vault, olm mine; scoped greps.
Deterministic, read-only, no LLM calls. Zero writes outside stdout.
"""
import datetime as dt
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT / "tools"))
from zknot_alarm import template_prefixes, is_template  # noqa: E402

now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
WK = 7 * 86400 * 1000
out = {"now_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}

# ---------- 1) zcode db census ----------
DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"
conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
db = {}
db["user_role_origin_distribution"] = conn.execute(
    "SELECT coalesce(json_extract(data,'$.semantics.origin'),'(null)'), count(*) "
    "FROM message WHERE json_extract(data,'$.role')='user' GROUP BY 1 ORDER BY 2 DESC"
).fetchall()

row = conn.execute("""
SELECT count(*), total(length(coalesce(t.txt,''))),
       total(CASE WHEN t.is_child=0 THEN 1 ELSE 0 END),
       total(CASE WHEN t.is_child=0 THEN length(coalesce(t.txt,'')) ELSE 0 END)
FROM (
 SELECT CASE WHEN s.parent_id IS NULL THEN 0 ELSE 1 END AS is_child,
  (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p
    WHERE p.message_id=m.id AND json_extract(p.data,'$.type')='text') AS txt
 FROM message m JOIN session s ON s.id=m.session_id
 WHERE json_extract(m.data,'$.role')='user'
   AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user')='real_user'
) t WHERE t.txt IS NOT NULL AND length(trim(t.txt))>0
""").fetchone()
db["alltime_realuser"] = {"turns": row[0], "chars": round(row[1] or 0),
                          "toplevel_turns": row[2], "toplevel_chars": round(row[3] or 0)}

msgs = []
for sid, t, is_child, ttype, txt in conn.execute("""
SELECT m.session_id, m.time_created, CASE WHEN s.parent_id IS NULL THEN 0 ELSE 1 END,
       s.task_type,
  (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p
    WHERE p.message_id=m.id AND json_extract(p.data,'$.type')='text') AS txt
FROM message m JOIN session s ON s.id=m.session_id
WHERE json_extract(m.data,'$.role')='user'
  AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user')='real_user'
  AND m.time_created >= ?""", (now_ms - 40 * 86400 * 1000,)):
    if txt and txt.strip():
        msgs.append({"sid": sid, "t": int(t), "child": is_child, "ttype": ttype or "", "text": txt})

prompts = {}
for m in msgs:
    prompts.setdefault(m["sid"], []).append({"t": m["t"], "text": m["text"]})
tmpl = template_prefixes(prompts)


def stats(ms):
    return {"n": len(ms), "chars": sum(len(m["text"]) for m in ms)}


w7 = [m for m in msgs if m["t"] >= now_ms - WK]
db["last7d"] = {
    "raw_all": stats(w7),
    "raw_toplevel": stats([m for m in w7 if not m["child"]]),
    "raw_child": stats([m for m in w7 if m["child"]]),
    "nontmpl_toplevel": stats([m for m in w7 if not m["child"] and not is_template({"text": m["text"]}, tmpl)]),
    "nontmpl_all": stats([m for m in w7 if not is_template({"text": m["text"]}, tmpl)]),
    "voice_lt500_raw": stats([m for m in w7 if len(m["text"]) < 500]),
    "voice_lt500_nontmpl_toplevel": stats([m for m in w7 if len(m["text"]) < 500 and not m["child"]
                                           and not is_template({"text": m["text"]}, tmpl)]),
    "ttype_raw_top8": Counter(m["ttype"] for m in w7).most_common(8),
}
db["templates_found_40d_pool"] = len(tmpl)
out["zcode_db"] = db

a = conn.execute("""
SELECT count(*), total(length(coalesce(json_extract(p.data,'$.text'),'')))
FROM part p JOIN message m ON m.id=p.message_id
WHERE json_extract(m.data,'$.role')='assistant' AND json_extract(p.data,'$.type')='text'
""").fetchone()
out["assistant_text_parts"] = {"parts": a[0], "chars": round(a[1] or 0)}
conn.close()

# ---------- 2) burn ledger ----------
u = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
rows = []
for ln in u.read_text(encoding="utf-8", errors="replace").splitlines():
    ln = ln.strip()
    if ln:
        try:
            rows.append(json.loads(ln))
        except Exception:
            pass
b = {"path": str(u.relative_to(ROOT)), "rows": len(rows)}
if rows:
    b["sample_keys"] = sorted(rows[-1].keys())

    def g(r, *names):
        for n in names:
            if n in r and r[n] is not None:
                return r[n]
        return None

    costk = next((k for k in rows[-1] if "cost" in k.lower()), None)
    modk = next((k for k in rows[-1] if "model" in k.lower()), None)
    provk = next((k for k in rows[-1] if k.lower() in ("provider", "lane", "service", "account")), None)
    b["fields_used"] = {"cost": costk, "model": modk, "provider": provk}
    agg = {}
    for r in rows:
        key = f"{g(r, provk) or ''}/{g(r, modk) or '?'}"
        a_ = agg.setdefault(key, {"n": 0, "cost": 0.0, "last": ""})
        a_["n"] += 1
        try:
            a_["cost"] += float(g(r, costk) or 0)
        except Exception:
            pass
        ts = str(g(r, "ts", "timestamp", "time", "created_at") or "")
        if ts > a_["last"]:
            a_["last"] = ts
    b["by_lane"] = {k: {"n": v["n"], "cost_usd": round(v["cost"], 4), "last_ts": v["last"]}
                    for k, v in sorted(agg.items(), key=lambda kv: -kv[1]["cost"])}
    try:
        b["total_cost_usd"] = round(sum(float(g(r, costk) or 0) for r in rows), 4)
    except Exception:
        b["total_cost_usd"] = "ERR"
    b["glm53prime_rows_full"] = [r for r in rows if "glm-5.3-prime" in str(g(r, modk) or "")]
    b["sonnet_rows_20261007"] = [r for r in rows if "sonnet" in str(g(r, modk) or "").lower()
                                 and str(g(r, "ts", "timestamp", "time", "created_at") or "").startswith("2026-10-07")]
out["burn"] = b

# ---------- 3) dir censuses ----------
d = ROOT / "watch/inbox/ractor_engine/2026-10-10-interaction-counterparts"
out["ractor_dir"] = sorted(p.name for p in d.iterdir()) if d.exists() else "MISSING"


def find_dirs(substr, roots):
    prune = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}
    hits = []
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [x for x in dirnames if x not in prune and not x.startswith(".")]
            for dd in list(dirnames):
                if substr in dd.lower():
                    p = Path(dirpath) / dd
                    try:
                        files = [f for f in p.rglob("*") if f.is_file()]
                        hits.append({"dir": str(p.relative_to(ROOT)).replace("\\", "/"),
                                     "files": len(files),
                                     "total_bytes": sum(f.stat().st_size for f in files)})
                    except OSError:
                        hits.append({"dir": str(p.relative_to(ROOT)).replace("\\", "/"), "err": True})
    return hits


out["salon_dirs"] = find_dirs("salon", [ROOT / "memory", ROOT / "watch", ROOT / "dashboard", ROOT / "corpus"])
out["olm_dirs"] = find_dirs("olm", [ROOT / "memory", ROOT / "watch"])

# ---------- 4) scoped greps ----------
pats = {"clarification_zero": re.compile(r"clarification[_ ]zero", re.I),
        "mimesis_or_261009484": re.compile(r"mimesis|2610\.09484", re.I)}
simrx = re.compile(r"simulat", re.I)
hits = {"clarification_zero": [], "mimesis_or_261009484": [], "simulator_in_astra_docs": []}
roots = [ROOT / "watch/inbox", ROOT / "memory", ROOT / "docs", ROOT / "configs", ROOT / "state",
         ROOT / "queue", ROOT / "tools", ROOT / "mag"]
CAP = 40
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__") and not x.startswith(".")]
        for fn in filenames:
            if not fn.endswith((".md", ".py", ".yaml", ".txt")):
                continue
            p = Path(dirpath) / fn
            rel = p.relative_to(ROOT).as_posix()
            try:
                if p.stat().st_size > 3_000_000:
                    continue
                txt = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            lines = txt.splitlines()
            for k, rx in pats.items():
                if len(hits[k]) < CAP:
                    for i, ln in enumerate(lines, 1):
                        if rx.search(ln):
                            hits[k].append(f"{rel}:{i}: {ln.strip()[:110]}")
                            break
            if "astra" in rel.lower() and len(hits["simulator_in_astra_docs"]) < CAP:
                for i, ln in enumerate(lines, 1):
                    if simrx.search(ln):
                        hits["simulator_in_astra_docs"].append(f"{rel}:{i}: {ln.strip()[:110]}")
                        break
out["grep"] = hits

print(json.dumps(out, indent=1, default=str))
