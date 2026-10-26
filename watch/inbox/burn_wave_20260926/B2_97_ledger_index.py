# B2-97: INDEX.json receipt registration (text-anchored insert) + LEDGER.jsonl row (json.dumps).
import io, json, hashlib, sys, datetime

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
RECV_REL = "watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md"
IDX = ROOT + r"\watch\inbox\INDEX.json"
LEDGER = ROOT + r"\memory\burns\LEDGER.jsonl"

sha = hashlib.sha256(io.open(ROOT + "\\" + RECV_REL, "rb").read()).hexdigest().upper()

with io.open(IDX, "r", encoding="utf-8") as f:
    idx = f.read()

ANCHOR = '"sha256": "A2C96FA49E02D60B959AF887627DC95F004CBE56C173E29D507473DC80466743"\n    }\n  ]\n}'
if idx.count(ANCHOR) != 1:
    sys.exit("INDEX anchor fail: %d" % idx.count(ANCHOR))
if "B2_97_width15_probe_20260926.md" in idx:
    print("INDEX already registers receipt, skipping insert")
else:
    entry = ('''"sha256": "A2C96FA49E02D60B959AF887627DC95F004CBE56C173E29D507473DC80466743",
    },
    {
      "path": "burn_wave_20260926/B2_97_width15_probe_20260926.md",
      "class": "receipt",
      "purpose": "B2-97 width-15 ceiling probe: precondition sweep found NO explicit operator GO for width 15 on QUEUE.md or any 2026-09-26 receipt, so per the row's own when-operator-ordered gate the wave was NOT fired; ready-to-fire card with the full harvest plan (15 Task agents one wave, metadata.json status/createdAt/totalDurationMs/totalTokens/totalToolUseCount, window + tok/h on the B2-25 convention, 1302 + 429 grep over all agent outputs, no refire inside the probe, amend-envelope-block-either-way rule) plus metadata shape byte-verified on 156 agent dirs of sess_fd5ec147; AFTERPARTY_CLOSE envelope block amended append-only naming the armed probe; ladder unchanged 3-6-10-12"''' + ',\n      "sha256": "' + sha + '"\n    }\n  ]\n}').replace('"sha256": "A2C96FA49E02D60B959AF887627DC95F004CBE56C173E29D507473DC80466743",\n    },', '"sha256": "A2C96FA49E02D60B959AF887627DC95F004CBE56C173E29D507473DC80466743"\n    },')
    out = idx.replace(ANCHOR, entry)
    json.loads(out)  # validity gate before write
    with io.open(IDX, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("INDEX item inserted, json valid")

row = {
    "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-97-width15-probe-no-go",
    "verdict": "landed",
    "landing": RECV_REL,
    "one_line": "Width-15 ceiling probe precondition check: NO explicit operator GO for width 15 on QUEUE.md or any 2026-09-26 receipt (four greps 18:20-18:27Z; header order is generic burn quota; AFTERPARTY operator-gated list lacks width 15; six GO-language receipts are unrelated lanes), so per the row's own gate the wave was NOT fired; ready-to-fire card with harvest plan filed (15 agents one wave, metadata.json five fields byte-verified on 156 dirs of sess_fd5ec147, 1302+429 grep, no-refire rule, amend-envelope-either-way), AFTERPARTY_CLOSE envelope block amended append-only, ladder unchanged 3-6-10-12, 15-16 rung still untested; row sat pre-checked [x] with no receipt (B2-238 disease), this landing earns the check; self-fed B2-424..426 unchecked",
    "lane": "B2-97",
}
line = json.dumps(row, ensure_ascii=False) + "\n"
with io.open(LEDGER, "a", encoding="utf-8", newline="") as f:
    f.write(line)
print("LEDGER row appended: " + row["ts"])
