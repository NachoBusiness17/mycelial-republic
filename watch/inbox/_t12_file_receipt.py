"""T12 receipt filing: append index event + LINKS row via json.dumps."""
import hashlib
import json
import time
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
receipt = ROOT / "watch/inbox/THE50_W3_T12_RECEIPT.md"
pack = ROOT / "memory/research_packs/THE50_W3_T12_PROPHECY_MARKETS.md"

sha_receipt = hashlib.sha256(receipt.read_bytes()).hexdigest().upper()
sha_pack = hashlib.sha256(pack.read_bytes()).hexdigest().upper()

event = {
    "seq": int(time.time() * 1000),
    "ts": "2026-09-19T00:00:00+00:00",
    "op": "register",
    "file": "/board/inbox/THE50_W3_T12_RECEIPT.md",
    "sha256": sha_receipt,
    "class": "RECEIPT",
    "purpose": (
        "THE50 W3 T12: prophecy-market game theory pack filed at "
        "memory/research_packs/THE50_W3_T12_PROPHECY_MARKETS.md sha256 "
        + sha_pack
        + "; cheap talk (Crawford-Sobel) costly signaling (Spence) credibility "
        "games (Sobel, Ely-Valimaki, Klein-Leffler) mapped to called-shot ledgers "
        "(Pool v1 16/16 BROKEN, v2 107 rows 94 expired/13 open, Q 3 rows, BG 0); "
        "7 results, 5 falsifiers; partner to THE50_W1_T05_PAYOFF_MATRIX which "
        "deferred this literature sweep"
    ),
    "writer": "zcode-seat",
}

links_row = {
    "ts": "2026-09-19T00:00:00Z",
    "id": "THE50-W3-T12-PROPHECY-MARKETS",
    "kind": "research-pack",
    "title": (
        "THE50 W3 T12: prophecy channels read as credibility games; cheap talk "
        "(Crawford-Sobel 1982), costly signaling (Spence 1973), reputation/bonds "
        "(Sobel 1985, Ely-Valimaki 2003, Klein-Leffler 1981) mapped to the "
        "called-shot ledger; computed: Pool v2 94/107 targets expired 13 open "
        "(horizons 2-541d median 74), extraction-not-credibility is the Pool "
        "equilibrium (no forfeitable bond), the card inverts Spence by putting "
        "cost on receivers; Brier scoreboard keeps the fleet's own Oct 4 2026 "
        "waypoint on the same table; falsifiers filed"
    ),
    "landing": "memory/research_packs/THE50_W3_T12_PROPHECY_MARKETS.md + watch/inbox/THE50_W3_T12_RECEIPT.md",
    "partner": "watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md (T5 deferred this literature sweep to T12)",
    "stats_script": "memory/research_packs/_t12_ledger_stats.py",
}

with open(ROOT / "watch/inbox/index_events.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")

with open(ROOT / "memory/corpus/LINKS.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(links_row, ensure_ascii=False) + "\n")

print("event seq:", event["seq"])
print("receipt sha256:", sha_receipt)
print("pack sha256:", sha_pack)
print("appended: 1 index event + 1 LINKS row")
