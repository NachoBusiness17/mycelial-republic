"""dd-corpus-holdings finish-line byte check (gala dd-selfsteal, division B, 2026-10-03).
Re-verifies the receipt's core inventory claims against bytes on disk.
Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/dd-selfsteal/lanes/dd-corpus-holdings.check.py
Exit 0 = all claims verified; nonzero = a claim failed.
"""
import json
import os
import subprocess
import sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
os.chdir(ROOT)
checks = []


def check(name, ok, detail):
    checks.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def jload(rel):
    with open(rel, encoding="utf-8") as f:
        return json.load(f)


# 1. dnd_classic_stub.v1.json
d = jload("memory/game_modules/dnd_classic_stub.v1.json")
check("dnd_classic_stub parses", d.get("module_id") == "dnd_classic_stub", f"module_id={d.get('module_id')}")
check("dnd_classic_stub rooms=14", len(d.get("rooms", {})) == 14, f"rooms={len(d.get('rooms', {}))}")
check("dnd_classic_stub event_tables=8", len(d.get("event_tables", {})) == 8, f"tables={len(d.get('event_tables', {}))}")
ps = d.get("player_start", {})
check("dnd_classic_stub fighter 12hp/14ac/+4/1d8+2",
      ps.get("hp") == 12 and ps.get("ac") == 14 and ps.get("attack_bonus") == 4 and ps.get("damage") == "1d8+2",
      f"hp={ps.get('hp')} ac={ps.get('ac')} atk={ps.get('attack_bonus')} dmg={ps.get('damage')}")

# 2. other game_modules
a = jload("memory/game_modules/audit_dungeon.v1.json")
check("audit_dungeon rooms=10", len(a.get("rooms", {})) == 10, f"rooms={len(a.get('rooms', {}))}")
adv = jload("memory/game_modules/adventure_2d6_stub.v1.json")
check("adventure_2d6 rooms=4 system=2d6-adventure-lite",
      len(adv.get("rooms", {})) == 4 and adv.get("system") == "2d6-adventure-lite",
      f"rooms={len(adv.get('rooms', {}))} system={adv.get('system')}")

# 3. campaigns
sun = jload("campaigns/sunless_citadel/module.json")
check("sunless_citadel keys dm/party_roster/ghost",
      all(k in sun for k in ("dm", "party_roster", "ghost")),
      f"dm={bool(sun.get('dm'))} party_roster={bool(sun.get('party_roster'))} ghost={bool(sun.get('ghost'))}")
qf = jload("campaigns/quiet_forge/module.json")
vg = jload("campaigns/villains_guild/module.json")
pl = jload("campaigns/parable_ledger_capture/module.json")
check("campaigns quiet_forge 1 room / villains_guild 5 rooms / parable parses",
      len(qf.get("rooms", {})) == 1 and len(vg.get("rooms", {})) == 5 and isinstance(pl, dict),
      f"qf={len(qf.get('rooms', {}))} vg={len(vg.get('rooms', {}))} pl_ok={isinstance(pl, dict)}")

# 4. dungeon_map
dm = jload("memory/dungeon/dungeon_map.json")
check("dungeon_map 6 rooms", len(dm.get("rooms", {})) == 6, f"rooms={len(dm.get('rooms', {}))}")

# 5. evennia docs count + evadventure LOC
n_docs = sum(len(fs) for _, _, fs in os.walk(os.path.join(ROOT, "corpus", "library", "evennia", "docs", "source")))
check("evennia docs/source = 710 files", n_docs == 710, f"files={n_docs}")
ev_dir = os.path.join(ROOT, "corpus", "library", "evennia", "evennia", "contrib", "tutorials", "evadventure")
loc = 0
for fn in os.listdir(ev_dir):
    if fn.endswith(".py"):
        with open(os.path.join(ev_dir, fn), encoding="utf-8", errors="replace") as f:
            loc += sum(1 for _ in f)
check("evadventure = 7164 py LOC", loc == 7164, f"loc={loc}")

# 6. SRD cache absence (byte-verified negative)
proc = subprocess.run(
    ["git", "bash", "-c",
     "find . -maxdepth 4 \\( -iname '*srd*' -o -iname '*dnd5e*' -o -iname '*open5e*' "
     "-o -iname '*monsters.json' -o -iname '*spells.json' \\) 2>/dev/null | grep -v node_modules | grep -v '\\.git/' | head -20"],
    capture_output=True, text=True, timeout=300)
srd_hits = [l for l in proc.stdout.splitlines() if l.strip()]
check("no SRD/dnd5e/open5e/monsters.json/spells.json content files on disk",
      len(srd_hits) == 0, f"hits={srd_hits}")

# 7. engine archetypes at mag/game_campaign.py:29-32
with open("mag/game_campaign.py", encoding="utf-8") as f:
    lines = f.readlines()
seg = "".join(lines[28:32])
arch_ok = all(k in seg for k in ('"fighter"', '"rogue"', '"wizard"', '"cleric"'))
check("game_campaign 4 archetypes at lines 29-32", arch_ok, seg.strip()[:120])
with open("mag/game_campaign.py", encoding="utf-8") as f:
    src = f.read()
check("game_campaign 1d20 attack roll present", "1d20" in src, "found d20 notation in engine")

# 8. dice engine
with open("mag/game_dice.py", encoding="utf-8") as f:
    dice_src = f.read()
check("game_dice.roll_dice(notation, seed) exists", "def roll_dice(notation" in dice_src and "seed" in dice_src,
      "def roll_dice(notation: str, *, seed" in dice_src)

# 9. DICE-LAW module doc: hermes_burn draft carries the exact law line; replay_flash is a different draft with the hash law present
dice_law = "int(sha256('{chain_tip}:{scene}:{turn}:{actor}').hexdigest()[:8], 16) % 20 + 1"
with open("watch/inbox/hermes_burn/DND_module.md", encoding="utf-8") as f:
    t = f.read()
check("DICE-LAW doc present with law line: watch/inbox/hermes_burn/DND_module.md", dice_law in t, f"bytes={len(t)}")
with open("watch/inbox/replay_flash/DND_module.md", encoding="utf-8") as f:
    t2 = f.read()
check("DICE-LAW second draft with sha256 law present: watch/inbox/replay_flash/DND_module.md",
      t2 != t and "sha256" in t2 and "DICE-LAW DUNGEON v1" in t2,
      f"bytes={len(t2)} different_draft={t2 != t}")

# 10. design theory library manifest = 37
n_man = sum(1 for l in open("memory/corpus/game_design_docs/manifest.jsonl", encoding="utf-8") if l.strip())
check("game_design_docs manifest = 37 entries", n_man == 37, f"entries={n_man}")

# 11. actual-play negative on file
with open("corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md", encoding="utf-8") as f:
    ap = f.read()
check("actual-play intel carries the no-transcripts negative",
      "found no full transcripts on the" in ap and "UNVERIFIED-PATH" in ap,
      "operator-attested layer marked UNVERIFIED-PATH")

# 12. receipt exists and is em-dash clean
with open("watch/inbox/dd_dogfood/corpus-holdings.md", "rb") as f:
    rb = f.read().decode("utf-8")
check("receipt exists, em-dash clean", len(rb) > 5000 and rb.count(chr(0x2014)) == 0,
      f"bytes={len(rb)} emdash={rb.count(chr(0x2014))}")

# 13. evennia EvAdventure + Turnbattle contrib docs on disk
for rel in ("corpus/library/evennia/docs/source/Contribs/Contrib-Evadventure.md",
            "corpus/library/evennia/docs/source/Contribs/Contrib-Turnbattle.md",
            "corpus/library/evennia/docs/source/Howtos/Turn-based-Combat-System.md"):
    check(f"evennia doc on disk: {os.path.basename(rel)}", os.path.isfile(os.path.join(ROOT, rel)),
          f"size={os.path.getsize(os.path.join(ROOT, rel))}")

fails = [c for c in checks if not c[1]]
print(f"\nTOTAL: {len(checks)} checks, {len(fails)} failed")
sys.exit(1 if fails else 0)
