---
name: mud-enrichment-wave
description: Mud enrichment wave — bones files (NetHack death-to-content), souls
  messages (512 legal messages from 24-word lexicon), ghost personalities
  (champion grudge memory + telegraphs + stances), replay port (18 sites
  seeded), StS ascension consumer, puzzle vault + inventory consumers — all
  landed green
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---
Mud enrichment wave landed across FX4/W2/W3/W4/W5/N10/N12: mud replay law ported (18 gameplay sites seeded on toy's LCG, 7 cosmetic-allowed, 11/11 replay + 58/58 fifty-gate), bones files (NetHack death-to-content: death writes {seed, room, cause, name, grit} to localStorage mud_bones FIFO cap 10; later runs raise ghosts that whisper "a walker took me — their grit still holds"; ghosts cannot kill), souls messages (512 legal messages from 24-word lexicon via 3-slot compose UI, cross-run spot law, replay law, lexicon-only law — 49/49 frontier lanes), ghost personalities (4 champions carry grudge memory capped 5 freshest; rematch telegraphs from per-class 4-line lexicon keyed FNV-1a of last grudge = zero stream draws; seeded stance adaptation; 41/41 replay + 63/63 gate), StS ascension consumer (victory → nextRun persists ng+1; ascension pins as run identity; difficulty flows through ng-multipliers only; 24/24 ASC lanes), puzzle vault consumed (gate was imaginary — no wall carried gate:true; fixed + 7 new lanes), inventory consumer (makeLoot exposed on window.MUD; pickup→add→use replay lane). Second rollback incident: mud.html reverted to pristine 17:14 by the sync_games backward flow — W2 rebuilt atomically (60 exact-match edits re-landing all 5 lanes), both stale mirrors synced (clobber cycle dead). Latent finds filed: hurtFishTouch G.shake undefined crash, schedMusic dead code, tomb evlog embeds cosmetic Math.random grudge-name (deterministic cause kind in evlog, cosmetic name in bonesWrite).
