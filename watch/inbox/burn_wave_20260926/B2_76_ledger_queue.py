"""B2-76 ledger append + queue receipt pointer + self-feed.

Run with .venv/Scripts/python.exe. Laws honored: self-feed briefs entered
UNCHECKED (never pre-checked); brief numbers renumbered highest+1 if a
concurrent lane took 330-331-332 mid-lane (B2-167 law, B2-246 precedent),
with the receipt and ledger one_line patched to match; anchored unique
replacement on freshly-read bytes for the B2-76 receipt pointer.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECEIPT = "watch/inbox/burn_wave_20260926/B2_76_junction_policy_20260926.md"
assert (ROOT / RECEIPT).is_file(), "receipt must exist before landing"

# ---------------------------------------------------------------- ledger ---
row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-76-catalog-junction-policy",
    "verdict": "LANDED",
    "landing": RECEIPT,
    "one_line": (
        "junction prune codified as scanner policy: mag/catalog_scan.py "
        "v2->v3 spec P1-P5 from LINKS XIDIG-WIN-* 2026-09-26 (63/31 per-path "
        "reparse limit, 16KB reparse data cap, junctions local-volume dirs "
        "only never network, symlink UNC contrast with junction violation "
        "split); live estate walk 485,998 rows, 0 under the training/ "
        "junction prefix, the real junction (tag 0xA0000003, win32 device "
        "target) recorded device_local+pruned to new catalog/junctions.jsonl "
        "so the SOCRATIC_GAPS duplicate-vs-mirror diff is runnable; the "
        "-189,106 Sep-18 delta attribution stays Unproven by design, and "
        "today's live-vs-filed -271,669 is attributed to measured estate "
        "churn (biography_backup -144,328 files, ghost -125,862, "
        "biography_backup_20260825 -42,249), not the junction (24 rows); "
        "9/9 junction-policy tests pass, ratchet NEW=0; MFT fast-refresh "
        "spec-cited not coded; self-feeds {briefs}"
    ),
}

brief_templates = [
    "- [ ] {{n0}} Junction mirror-vs-duplicate diff: (self-fed by B2-76) run "
    "the SOCRATIC_GAPS falsifier the 2026-09-18 prune left Unproven: walk the "
    "live junction target local_sovereign_agent/memory/training, sha256 every "
    "file, byte-compare against the real-path tree so the pruned junction is "
    "proven byte-duplicate or named an intentional mount; the v3 policy "
    "ledger makes this runnable (catalog/junctions.jsonl carries path+tag+"
    "target+class per reparse point); pointers "
    "watch/inbox/burn_wave_20260926/B2_76_junction_policy_20260926.md + "
    "watch/inbox/SOCRATIC_GAPS_20260918.md:40,102.",

    "- [ ] {{n1}} MFT/USN fast-refresh spec: (self-fed by B2-76) codify "
    "XIDIG-WIN-MFT-ENUM + XIDIG-WIN-USN-REFRESH (FSCTL_ENUM_USN_DATA once "
    "for the full-volume listing, FSCTL_READ_USN_JOURNAL deltas for fast "
    "refresh, NTFS only, SMB 3.0 No) into the catalog refresh spec; v3 still "
    "os.walks (485,998 rows on 09-26) and the Sep-18 fold went 271,669 rows "
    "stale in 8 days, so the next refresh design must split full walk from "
    "journal deltas; pointers watch/inbox/LINKS.jsonl:330-331 + "
    "watch/inbox/burn_wave_20260926/B2_76_junction_policy_20260926.md.",

    "- [ ] {{n2}} Catalog refresh + retag decision: (self-fed by B2-76) the "
    "filed catalog.jsonl (757,667 rows, Sep-18) overstates the estate by "
    "271,669 rows (live walk 485,998; measured churn: "
    "memory/biography_backup -144,328 files, memory/ghost -125,862, "
    "memory/biography_backup_20260825 -42,249) while tags.jsonl + "
    "catalog_fts.sqlite still quote Sep-18 mass; decide the refresh flow "
    "(v3 module append semantics vs the salon's atomic-replace contract), "
    "run it, and re-run the tag pass so TAG_REPORT.md stops quoting dead "
    "trees; pointers watch/inbox/burn_wave_20260926/B2_76_scan_verify.json + "
    "catalog/TAG_REPORT.md.",
]

# ------------------------------------------------------------- queue read ---
queue = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
text = queue.read_text(encoding="utf-8")
assert text.endswith("\n")

nums = [int(m) for m in re.findall(r"B2-(\d+)", text)]
highest = max(nums)
n0, n1, n2 = 330, 331, 332
taken = {330, 331, 332} & set(nums)
if taken:
    n0, n1, n2 = highest + 1, highest + 2, highest + 3
    receipt_path = ROOT / RECEIPT
    rtext = receipt_path.read_text(encoding="utf-8")
    rtext = rtext.replace("B2-330/331/332", f"B2-{n0}/{n1}/{n2}")
    rtext = rtext.replace("self-fed as\nB2-331.", f"self-fed as\nB2-{n1}.")
    receipt_path.write_text(rtext, encoding="utf-8", newline="\n")
    text = queue.read_text(encoding="utf-8")  # receipt edit done, re-read queue
    print(f"renumbered self-feeds to B2-{n0}/{n1}/{n2} (330-332 taken: {sorted(taken)})")

for n in (n0, n1, n2):
    assert f"B2-{n}" not in text, f"B2-{n} already present"

briefs = "\n" + "\n\n".join(
    t.replace("{{n0}}", f"B2-{n0}")
     .replace("{{n1}}", f"B2-{n1}")
     .replace("{{n2}}", f"B2-{n2}")
    for t in brief_templates) + "\n"

# ------------------------------------------- receipt pointer on B2-76 row ---
anchor = ("so junction pruned 189K rows becomes policy; pointers "
          "watch/inbox/LINKS.jsonl XIDIG-WIN-* 2026-09-26 + "
          "RESEARCH_GAP_ANALYSIS_20260918.md windows row.")
assert text.count(anchor) == 1, "B2-76 anchor not unique; re-read and rebase"
text = text.replace(
    anchor,
    anchor + " (receipt 2026-09-26: "
             "watch/inbox/burn_wave_20260926/B2_76_junction_policy_20260926.md)")
queue.write_text(text, encoding="utf-8", newline="\n")

with open(queue, "a", encoding="utf-8", newline="\n") as f:
    f.write(briefs)
print("queue appended: receipt pointer on B2-76, self-feeds "
      f"B2-{n0}/B2-{n1}/B2-{n2}")

row["one_line"] = row["one_line"].format(
    briefs=f"B2-{n0}/{n1}/{n2}")

ledger = ROOT / "memory" / "burns" / "LEDGER.jsonl"
with open(ledger, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("ledger rows now:", sum(1 for _ in open(ledger, encoding="utf-8")))
