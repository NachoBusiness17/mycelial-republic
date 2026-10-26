---
name: steam-corpus-mined
description: Steam library (16 installed games) mined into
  memory/game/steam_corpus.json + STEAM_LIBRARY_CORPUS.md — engines, appids,
  steal-lists; Exanima = Rayform in-house engine; next mining waves declared not
  done
metadata:
  node_type: memory
  type: project
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

Mined 2026-09-14 on operator directive ("map all of these locally installed games... mine their corpus like we do ours, find websites/apis/underlying tech"). Deliverables: `memory/game/steam_corpus.json` (machine-readable) + `memory/game/STEAM_LIBRARY_CORPUS.md` (readable, with canonical tech links). Source dir: `C:/Program Files (x86)/Steam/steamapps/common`.

- **Headline: 6 of 16 games run engines their authors wrote themselves** (Exanima, Destiny 2, Dwarf Fortress, PoE2, BG3/DOS2) — the operator's hand-rolled + public-beacon instinct is the library's dominant strategy.
- **Exanima = "Rayform" engine**, fully in-house by Bare Mettle (Madoc Evans wrote physics/renderer/audio/UI/tooling himself); custom physics rebuilt from scratch mid-development; Borland register conventions in the binary; `.rpk` resource packs + OpenAL; Exanima is the prelude that funded Sui Generis — the parables→game ramp pattern, proven by someone else. Sources: exanimamodding.codeberg.page Engine Details, baremettle.com forums, the 6-part Steam dev-history thread.
- **Marker fingerprints lie** — always correct against public records: BG3 flagged "Unreal" (it's Divinity 4.0, `.pak` false-positive), DOOM Eternal flagged Unreal (it's id Tech 7), BG1/2EE flagged RPGMaker (Infinity EE).
- **Steals already shipped:** SUPERHOT powerup ← Gunfire Reborn, torch-light vision ← Exanima (both in MUD, see [[mud-superhot-adam-access]]).
- **Open next waves (declared, not done):** save-file forensics per game, PCGamingWiki API sweep per appid, filing canonical links into LINKS.jsonl ([[link-library-canonical-registry]], dedupe first), "launch 16 wide" witness lane tasks per [[audit-our-way-game-medium]].
