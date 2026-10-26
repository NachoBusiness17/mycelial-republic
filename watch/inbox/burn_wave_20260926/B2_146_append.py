"""B2-146: append one LEDGER row (json.dumps, no heredoc)."""
import json
from datetime import datetime, timezone

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "unregistered-files",
    "verdict": "steal",
    "landing": "watch/inbox/burn_wave_20260926/B2_146_unregistered_files_20260926.md",
    "one_line": (
        "5 unregistered inbox files registered via index_fold_host.mjs add "
        "(EVENTS.jsonl DATA, vault pack artifact, 3 BURN receipts RECEIPT; seqs "
        "1789823567015749390-394, 973 active items): all 51 EVENTS.jsonl rows "
        "byte-match LINKS.jsonl origin lines 275-331; vault pack sha matches "
        "trajectory steps.jsonl:22168 and its OneDrive copy; receipt claims "
        "re-verified live (arXiv 2606.26479, Sefaria Kol_HaTor.4 error, Cerebras "
        "card gate); INDEX.md + SHARED_SURFACE_CONTRACT.json left retired per "
        "events 1381/1379"
    ),
}
with open("memory/burns/LEDGER.jsonl", "a", encoding="utf-8") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
print("appended ledger row:", row["ts"], row["slug"])
