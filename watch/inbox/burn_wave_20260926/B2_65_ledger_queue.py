"""B2-65 close: LEDGER row (json.dumps) + QUEUE self-feeds + receipt word count."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-65-registry-revival",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_65_registry_revival_20260926.md",
    "one_line": (
        "VERSION_REGISTRY release trail revival: death diagnosed (writers were "
        "mag/roadmap_runner.py:278 roadmap passes and mag/training_set.py:107 manual folds, "
        "last gate_record 2026-08-06T17:31Z, last fold 2026-08-10T00:07Z, memory/runs/roadmap/ "
        "holds only two 2026-08-06 evidence files, no scheduler ever wired either writer, "
        "468,061 training events moved since Aug 10 while the referent froze); revival designed "
        "as regime milestones (regime_ gate_id prefix, recorded against active era v5, writer = "
        "landing session at close via main.py release record, trigger = receipt filing, weekly "
        "drift stamp = staleness tripwire) with spec amended first in VERSION_REGISTRY.md "
        "(as-of 2026-09-26); 3 backfilled milestones filed through the real writer CLI and "
        "verified in both trails: regime_violation_ratchet (2026-09-24 ratchet gate, "
        "corpus/steal/ZCODE_RATCHET_LANDED_20260924.md), regime_fanout_width_law (2026-09-25 "
        "tether 429/1302 law, corpus/steal/TETHERED_LINK_STEAL_20260925.md), "
        "regime_drift_registry_t1_t6 (2026-09-26 T1-T6 codification, B2_05 receipt); disclosed: "
        "release status conflates regime rows into v5 gates_passed (mag/release_registry.py:116-124)"
    ),
}

ledger = ROOT / "memory" / "burns" / "LEDGER.jsonl"
existing = ledger.read_text(encoding="utf-8")
if "B2-65-registry-revival" not in existing:
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("ledger rows now:", sum(1 for _ in ledger.open(encoding="utf-8")))

feeds = [
    "B2-208 regime-trail staleness tripwire: the B2-65 revival names the weekly drift stamp as "
    "tripwire but tools/drift_pairs_stamp.py never reads gates.jsonl freshness; add a check to "
    "tools/drift_pairs_stamp.py that alarms when no gate row (regime_ or graduation) lands within "
    "14 days while memory/training/events.jsonl grows, so T4/T5 referent death files itself; "
    "pointers tools/drift_pairs_stamp.py:223-331 + docs/ref/releases/VERSION_REGISTRY.md Regime milestones section",
    "B2-209 regime gate display split: release status counts regime_ rows into v5 gates_passed "
    "(mag/release_registry.py:116-124 reads the log unfiltered; :58-73 status_summary), conflating "
    "graduation gates with era milestones so a version could drift toward shipped on regime rows; "
    "exclude the regime_ prefix from _gates_passed_for or show a separate regime count; pointers "
    "mag/release_registry.py:58-73,116-124 + watch/inbox/burn_wave_20260926/B2_65_registry_revival_20260926.md",
    "B2-210 pre-Sept regime backfill sweep: durable landed work between 2026-08-11 and 2026-09-23 "
    "(shared surface contract, link library, drift patrol adoption) has receipts but no regime rows "
    "because B2-65 backfilled only the three clearest; sweep watch/inbox/ and corpus/steal/ for "
    "landed receipts in that window and backfill or file the owed list; pointers "
    "watch/inbox/SHARED_SURFACE_CONTRACT.json + memory/burns/LEDGER.jsonl verdict fields",
]
queue = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
text = queue.read_text(encoding="utf-8")
for n in ("B2-208", "B2-209", "B2-210"):
    assert n not in text, f"number collision: {n}"
with queue.open("a", encoding="utf-8") as f:
    f.write("\n")
    for b in feeds:
        f.write(f"- [ ] {b}\n")
print("queue appended:", len(feeds), "briefs")

receipt = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_65_registry_revival_20260926.md"
words = len(receipt.read_text(encoding="utf-8").split())
print("receipt words:", words, "(limit 600)")
assert "\u2014" not in receipt.read_text(encoding="utf-8"), "em-dash in receipt"
assert "\u2014" not in json.dumps(row) and all("\u2014" not in b for b in feeds), "em-dash in appends"
print("em-dash law: clean")
