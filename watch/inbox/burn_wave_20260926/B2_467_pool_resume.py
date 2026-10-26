"""B2-467 Mr Pool harvest resume (2026-09-26).

Resumes the Sep 18 Telethon harvest of @MrPool_Q to current, using the kept
session watch/inbox/mrpool_export/harvest.session (auth key inside) plus the
api pair recorded in memory/agent_sessions/orc-tbd75828c19.json (the Sep 18
harvest run log). Writes ONLY new rows (msg_id > 4633) to
watch/inbox/mrpool_export/ledger_delta_20260926.jsonl with the same row schema
as ledger_full.jsonl. The Sep 18 snapshot files ledger.jsonl / ledger_full.jsonl
are NOT mutated (they are byte-pinned by two filed receipts). No media is
downloaded in this pass; media_type/file_size are captured in the row.

Schema replication notes (diffed against ledger_full samples):
- text uses msg.text (markdown-rendered; ledger msg 4625 carries a ](http link)
- forward dict shape {"sender_id": str, "from_name": str, "date": iso, "post": bool}
- ReactionPaid serializes as the literal string "ReactionPaid()"
- ReactionCustomEmoji serializes as "ReactionCustomEmoji(document_id=N)"
  (no custom-emoji reaction exists in the Sep 18 ledger; recipe documented here)
- emojis = codepoints matched by EMOJI_RE over the text (the Sep 18 field
  splits flags and variation selectors into single codepoints; same here)
- urls = MessageEntityUrl slices + MessageEntityTextUrl targets + in-text
  https?:// matches + MessageMediaWebPage preview url, order-preserved dedupe
"""
import asyncio
import hashlib
import json
import re
import sys
from datetime import timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import (
    MessageEntityTextUrl,
    MessageEntityUrl,
    ReactionCustomEmoji,
    ReactionEmoji,
    ReactionPaid,
)

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "watch" / "inbox" / "mrpool_export"
SNAP = EXP / "ledger_full.jsonl"
SNAP2 = EXP / "ledger.jsonl"
DELTA = EXP / "ledger_delta_20260926.jsonl"
SESSION = EXP / "harvest"
HANDLE = "@MrPool_Q"
BASELINE_ID = 4633

# api pair as recorded in the Sep 18 harvest run log
API_ID = 34139736
API_HASH = "019e35479d50c3dade7bd99853660a6d"

EMOJI_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"
    "\U0001F1E6-\U0001F1FF"
    "\u2600-\u27BF"
    "\u2B00-\u2BFF"
    "\u2190-\u21FF"
    "\u2300-\u23FF"
    "\u25A0-\u25FF"
    "\u2900-\u297F"
    "\uFE0F\u20E3\u2139\u2122\u2049\u203C"
    "]"
)
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def scan(path: Path):
    n = 0
    lo = hi = None
    lo_id = hi_id = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            n += 1
            d = r["date"]
            if lo is None or d < lo:
                lo, lo_id = d, r["msg_id"]
            if hi is None or d > hi:
                hi, hi_id = d, r["msg_id"]
    return {"file": path.name, "rows": n, "min_date": lo, "max_date": hi,
            "min_msg_id": lo_id, "max_msg_id": hi_id}


def row_of(m) -> dict:
    text = m.text or ""
    urls = []
    for ent in (m.entities or []):
        if isinstance(ent, MessageEntityUrl):
            u = text[ent.offset:ent.offset + ent.length].strip()
            if u:
                urls.append(u)
        elif isinstance(ent, MessageEntityTextUrl):
            urls.append(ent.url)
    urls += URL_RE.findall(text)
    media = m.media
    media_type = type(media).__name__ if media else None
    if media_type == "MessageMediaWebPage":
        try:
            if media.webpage and getattr(media.webpage, "url", None):
                urls.append(media.webpage.url)
        except Exception:
            pass
    seen = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]
    fwd = None
    if m.forward:
        try:
            sid = str(m.forward.sender_id) if m.forward.sender_id else ""
        except Exception:
            sid = ""
        fwd = {
            "sender_id": sid,
            "from_name": m.forward.from_name or "",
            "date": m.forward.date.astimezone(timezone.utc).isoformat() if m.forward.date else None,
            "post": bool(m.forward.post),
        }
    reactions = None
    if m.reactions:
        reactions = []
        for res in m.reactions.results:
            r = res.reaction
            if isinstance(r, ReactionEmoji):
                e = r.emoticon
            elif isinstance(r, ReactionPaid):
                e = "ReactionPaid()"
            elif isinstance(r, ReactionCustomEmoji):
                e = f"ReactionCustomEmoji(document_id={r.document_id})"
            else:
                e = type(r).__name__
            reactions.append({"e": e, "n": res.count})
    file_ext = file_size = None
    if m.file:
        file_ext = m.file.ext
        file_size = m.file.size
    return {
        "msg_id": m.id,
        "date": m.date.astimezone(timezone.utc).isoformat(),
        "edit_date": m.edit_date.astimezone(timezone.utc).isoformat() if m.edit_date else None,
        "text": text,
        "emojis": EMOJI_RE.findall(text),
        "urls": urls,
        "views": m.views,
        "forwards": m.forwards,
        "forward": fwd,
        "reactions": reactions,
        "replies_count": m.replies.replies if m.replies else 0,
        "media_type": media_type,
        "file_size": file_size,
        "file_ext": file_ext,
        "grouped": bool(m.grouped_id),
    }


async def pull(out_rows: list) -> dict:
    client = TelegramClient(str(SESSION), API_ID, API_HASH)
    await asyncio.wait_for(client.connect(), timeout=90)
    if not await client.is_user_authorized():
        await client.disconnect()
        return {"ok": False, "stage": "auth", "error": "session present but not authorized (re-login required)"}
    entity = await asyncio.wait_for(client.get_entity(HANDLE), timeout=60)
    count = 0
    max_id_seen = BASELINE_ID
    max_date_seen = None
    async for m in client.iter_messages(entity, min_id=BASELINE_ID, reverse=True):
        r = row_of(m)
        out_rows.append(r)
        count += 1
        max_id_seen = max(max_id_seen, m.id)
        if max_date_seen is None or r["date"] > max_date_seen:
            max_date_seen = r["date"]
        if count % 50 == 0:
            print(f"  pulled {count} rows, at msg_id {m.id}", flush=True)
    me = await client.get_me()
    who = getattr(me, "username", None) or getattr(me, "phone", "?")
    await client.disconnect()
    return {"ok": True, "pulled": count, "max_msg_id": max_id_seen,
            "max_date": max_date_seen, "session_user": who}


def main():
    print("== B2-467 baseline byte-verify ==", flush=True)
    for p in (SNAP, SNAP2):
        info = scan(p)
        info["sha256"] = sha256(p)
        print(json.dumps(info, ensure_ascii=False), flush=True)

    rows = []
    try:
        res = asyncio.run(pull(rows))
    except Exception as e:
        res = {"ok": False, "stage": "exception", "error": f"{type(e).__name__}: {e}"}
    print("PULL RESULT: " + json.dumps({k: v for k, v in res.items() if k != "pulled"}, ensure_ascii=False), flush=True)

    if not res.get("ok"):
        print("HARVEST_BLOCKED: " + res.get("error", "unknown"), flush=True)
        sys.exit(3)

    if rows:
        tmp = DELTA.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        tmp.replace(DELTA)
    print(f"DELTA WRITTEN: {DELTA.name} rows={len(rows)}", flush=True)
    if rows:
        lo = min(r["date"] for r in rows)
        hi = max(r["date"] for r in rows)
        ids = [r["msg_id"] for r in rows]
        print(json.dumps({"delta_min_date": lo, "delta_max_date": hi,
                          "delta_min_id": min(ids), "delta_max_id": max(ids),
                          "delta_rows": len(rows),
                          "combined_rows": 3663 + len(rows)}, ensure_ascii=False), flush=True)
    else:
        print("NO NEW ROWS: channel head still msg_id 4633", flush=True)


if __name__ == "__main__":
    main()
