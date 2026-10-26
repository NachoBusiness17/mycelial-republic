import json
from pathlib import Path

root = "C:/Users/foste/Documents/projects/local_sovereign_agent"
art = Path(root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.json")

doc = {
  "lane": "a04-df-raws",
  "division": "A",
  "ok": True,
  "note": "DF raws mine verified. Both rerunnable parsers (parse_spheres.py, parse_entities.py) re-ran exit 0 under the repo venv and regenerated df_spheres.json, df_bestiary.json, df_entities.json byte-identical to landed copies (sha256 match). Counts confirmed: lexicon 3223 entries in each of 4 languages (dwarf/elf/human/goblin, 12892 total, every entry pos-tagged), spheres canonical_sphere_count=130, bestiary roster 8 bosses + 74 difficulty-rated wildlife, economy tradegoods 40, procedural creature_profiles 235, entities 6. Negatives, first-class: build_df_procedural.py NOT rerunnable, its input _rcp_profiles_tmp.json is absent from corpus/df_mine; df_voice.json holds 200 deep descriptor entries vs the voice FOLD prose claim of 462 (the 264-entry eye pattern table and 46 shape adjectives are cited install-side, not stored in JSON); estate grep for df_lexicon is zero-hit in both corpus/steal/ and memory/corpus/ (the lexicon mine is unreferenced by any steal receipt so far); spheres is zero-hit in corpus/steal/ with the only memory/corpus hit being the mine's own LINKS-343 registration row. Quotes below byte-verified as exact substrings, one occurrence each, verification in the check log.",
  "rows": [
    {
      "law": "raws-as-corpus: a game's own data files are a parallel language corpus",
      "claim": "Four complete DF languages, 3223 entries each, fully POS-tagged via a join on language_words.txt, mined read-only with no wiki dependency; compound-slot roles make generated names grammatical by construction.",
      "quote": "Entries exceed keys because 907 of 2,124 keys are multi-POS",
      "source": root + "/corpus/df_mine/lexicon_FOLD.md",
      "steal": "Lane b4 names roblox artifacts/bodies from df_lexicon_full.json compound-slot roles only (FRONT/REAR_COMPOUND, THE_NOUN, OF_NOUN), never free word soup; landing in roblox/ src/shared alongside ArtifactLore tonight.",
      "falsifier": "Load df_lexicon_full.json: any language with entry count not 3223, or any entry missing a pos field, kills the row.",
      "leverage": "high"
    },
    {
      "law": "canonical census beats wiki renders",
      "claim": "The 130-sphere canon is closed from globals.lua random_sphere_adjective keys; raw-written creatures carry only 26 SPHERE tokens across 21 spheres, so the wiki image hid most of the vocabulary.",
      "quote": "The number the wiki image hides: 130 distinct spheres.",
      "source": root + "/corpus/df_mine/spheres_FOLD.md",
      "steal": "Lane b4 seeds all roblox sphere picks from the 130-key df_spheres.json spheres array (plus 16 evil / 15 good pools) instead of a hardcoded subset; landing in roblox/ Worldgen sphere tables tonight.",
      "falsifier": "df_spheres.json canonical_sphere_count != 130, or spheres array length != 130, kills the row.",
      "leverage": "high"
    },
    {
      "law": "kinship is an engine-side graph constraint, not flat random",
      "claim": "Sphere co-occurrence is gated by a parents/children/enemies graph in globals.lua; the engine blocks enemy spheres from co-occurring on one creature.",
      "quote": "`add_sphere_mpp` in globals.lua blocks a sphere's `parents`/`children`/`enemies` from co-occurring.",
      "source": root + "/corpus/df_mine/spheres_FOLD.md",
      "steal": "Lane b4 mirrors the enemy-exclusion pairs in the roblox sphere picker so generated beasts and deities never pair enemy spheres; landing in the Worldgen/Bodygen picker tonight.",
      "falsifier": "Read the DF install globals.lua: if add_sphere_mpp does not exist or has no co-occurrence blocking effect, the row dies.",
      "leverage": "high"
    },
    {
      "law": "procedural identity is a lock order: sphere, then form, attack, material",
      "claim": "FB assembly gates every downstream roll on the sphere draw (235 weighted RCP profiles, 12 attack tweaks, 1-in-20 uniform material flip), plus a per-world blacklist so forms never repeat.",
      "quote": "DF gates every downstream roll on the sphere: DEATH grays the palette, dumps ash into the material pool, and reshapes the description.",
      "source": root + "/corpus/df_mine/procedural_FOLD.md",
      "steal": "Lane b4 builds the roblox body generator as ordered gates off one sphere draw, with never-repeat form blacklist and big-weight rare keys, crossing independent axes instead of one giant table; landing in roblox/ bodygen tonight.",
      "falsifier": "df_procedural.json assembly_chain_forgotten_beast shows any roll independent of the sphere draw, kills the lock-order law.",
      "leverage": "high"
    },
    {
      "law": "price in material, decorate in quality",
      "claim": "DF value = BASE x MATERIAL_VALUE x QUALITY with artifact x20 +300; material tier is the real lever (adamantine 300 vs steel 30) and processing chains mint most wealth, not rarity.",
      "quote": "Ledger Exchange should weight tradegoods by MATERIAL_VALUE tier (2/10/30/40/300 metals; 2-60 gems) and let quality be a small multiplier, mirroring DF's anti-quality inflation.",
      "source": root + "/corpus/df_mine/economy_FOLD.md",
      "steal": "Reprice roblox LedgerExchange tradegoods by MATERIAL_VALUE tier with artifact ceiling x20 not x200; landing in roblox/ LedgerExchange constants next time economy is touched.",
      "falsifier": "df_economy.json tradegoods or artifact multipliers contradict the stated tiers, kills the row.",
      "leverage": "medium"
    }
  ],
  "checks": [
    {"command": "ls corpus/df_mine/ (27 files: 8 mine jsons + dfhack wave + 7 FOLDs + 3 parsers)", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "git show --stat 37de3d3f9 (mine landing commit confirmed, 21 files)", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "./.venv/Scripts/python.exe corpus/df_mine/parse_spheres.py (rerun; outputs byte-identical to landed, sha256 match)", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "./.venv/Scripts/python.exe corpus/df_mine/parse_entities.py (rerun; output byte-identical to landed, sha256 match)", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "json entry counts: lexicon 4x3223 all pos-tagged; spheres 130; bestiary 8+74; tradegoods 40; profiles 235; entities 6", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "NEGATIVE: build_df_procedural.py not rerun, input _rcp_profiles_tmp.json absent (ls exit 2)", "exit": 2, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "NEGATIVE: df_voice.json deep descriptor count 200 vs FOLD claim 462 (eye table install-side only)", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "estate grep df_lexicon: corpus/steal/ exit 1, memory/corpus/ exit 1 (zero hits both, finding)", "exit": 1, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "estate grep spheres: corpus/steal/ exit 1 (zero hits); memory/corpus/LINKS.jsonl line 126 LINKS-343 only", "exit": 1, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"},
    {"command": "quote byte verification: 6 spans checked as exact substrings, all occurrences=1", "exit": 0, "evidence": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.check.txt"}
  ],
  "decision_changed": "no",
  "artifact": root + "/watch/inbox/gala_20260925/w2/lanes/a04-df-raws.json"
}

text = json.dumps(doc, indent=2, ensure_ascii=False)
assert "\u2014" not in text, "em-dash law violated"
art.write_text(text, encoding="utf-8")
print("wrote", str(art), "bytes:", art.stat().st_size)
back = json.load(open(art, encoding="utf-8"))
print("valid json, rows:", len(back["rows"]), "checks:", len(back["checks"]))
