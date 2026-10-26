"""B2-467 preview-door parse (2026-09-26).

Parses the two fetched logged-out preview pages of t.me/s/MrPool_Q
(B2_467_preview_head.html ids 4644-4663, B2_467_preview_before4644.html ids
4624-4643) into ledger_delta_preview_20260926.jsonl rows for ids 4634-4663,
the growth past the Sep 18 Telethon snapshot (max msg_id 4633). The preview
door is the documented no-auth fallback of watch/SELF_STEAL_TELEGRAM_CHANNEL_20260905.md
after the harvest.session auth key came back AuthKeyUnregistered.

Fields the preview plane exposes: msg_id, date, text, views (K-rounded page
notation), reactions (page chips). Fields it does not expose are written null
and named in the receipt: edit_date, forwards, forward, replies_count,
media_type, file_size, file_ext, exact reaction counts.
"""
import html as html_mod
import json
import re
from pathlib import Path

LANE = Path(__file__).resolve().parent
EXP = LANE.parent / "mrpool_export"
OUT = EXP / "ledger_delta_preview_20260926.jsonl"
PAGES = [LANE / "B2_467_preview_before4644.html", LANE / "B2_467_preview_head.html"]

MSG_SPLIT = re.compile(r'<div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="MrPool_Q/(\d+)"')
TIME_RE = re.compile(r'<time datetime="([^"]+)"')
TEXT_RE = re.compile(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', re.S)
VIEWS_RE = re.compile(r'tgme_widget_message_views">([^<]+)<')
REACT_RE = re.compile(r'tgme_widget_message_reactions[^>]*>.*?</div>', re.S)


def clean_text(raw: str) -> str:
    t = re.sub(r"<br\s*/?>", "\n", raw)
    t = re.sub(r"<[^>]+>", "", t)
    t = html_mod.unescape(t)
    return t.strip()


def parse_page(path: Path):
    html = path.read_text(encoding="utf-8")
    parts = MSG_SPLIT.split(html)
    rows = []
    for i in range(1, len(parts) - 1, 2):
        msg_id = int(parts[i])
        block = parts[i + 1]
        tm = TIME_RE.search(block)
        date = tm.group(1) if tm else None
        tx = TEXT_RE.search(block)
        text = clean_text(tx.group(1)) if tx else ""
        vw = VIEWS_RE.search(block)
        views = vw.group(1) if vw else None
        react = REACT_RE.search(block)
        reactions = None
        if react:
            chips = re.findall(r'tgme_widget_message_reaction[^>]*>.{0,80}?>([^<]+)<.*?tgme_widget_message_reaction_count[^>]*>([^<]+)<', react.group(0), re.S)
            reactions = [{"e": html_mod.unescape(e).strip(), "n": n.strip()} for e, n in chips]
        rows.append({"msg_id": msg_id, "date": date, "text": text, "views": views,
                     "reactions": reactions, "source": "t.me/s logged-out preview 2026-09-26"})
    return rows


def main():
    all_rows = {}
    for p in PAGES:
        for r in parse_page(p):
            all_rows[r["msg_id"]] = r
    new = [all_rows[k] for k in sorted(all_rows) if k > 4633]
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        for r in new:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps({"delta_rows": len(new),
                      "ids": f"{new[0]['msg_id']}..{new[-1]['msg_id']}" if new else "none",
                      "min_date": min(r["date"] for r in new),
                      "max_date": max(r["date"] for r in new),
                      "out": str(OUT)}, ensure_ascii=False))
    for r in new:
        head = (r["text"][:90] + "...") if len(r["text"]) > 90 else r["text"]
        print(f"{r['msg_id']} {r['date']} views={r['views']} :: {head!r}")


if __name__ == "__main__":
    main()
