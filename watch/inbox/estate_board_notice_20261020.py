import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")))
from mag.fleet_report import file_report
r = file_report(seat="grokbot-mag", kind="NOTICE", model="grokbot", report={
 "notice_id": "N-20261020-estate-board-canon",
 "category": "law_change",
 "subject": "ESTATE_BOARD_20261020 is the canon front page",
 "affects": ["all seats", "watch/LIBRARY/INDEX.md"],
 "narrative": ("watch/LIBRARY/ESTATE_BOARD_20261020.md is the single front page: (a) 12 items that need Nacho, (b) seat work plus red-task triage, (c) watching rows with duplicates folded (8765 portproxy ghost = ONE row W1; Ollama bind canon = loopback, W2), (d) October done. "
  "COMMIT_PLAN_20261020.md proposes 9 ordered commit batches + pre-flight (EOL renormalize, exclusions); nothing committed. OCTOBER_MAP_GAP_20261020.md holds the timeline. "
  "Fixes applied: configs/mates.yaml pointer -> tools/leave_dispatcher.py (.bak kept); main.py CRLF restored (6-line real diff)."),
 "action_required": ("Read the board before work; do not re-file portproxy/Ollama rediscoveries, update the canonical row instead. "
  "Claim (b) items via a lease or receipt. Need-Nacho items are his only. ACK this notice."),
 "in_force_until": "until_cancelled"})
print(json.dumps(r, default=str)[:500])
