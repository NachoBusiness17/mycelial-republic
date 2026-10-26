# DF Voice FOLD — the announcement grammar

**The grammar:** DF announcements are single declarative sentences with the anatomy [SUBJECT] + [DEED] + [DREAD-SCALER]. Subject first, always a proper name or a vague dread noun ("Something truly horrifying"), never a pronoun. The deed is a bare present-tense verb phrase ("has given birth to", "has been struck down", "is taken by a fey mood", "has arrived"). Dread is scaled not by wording but by delivery channel: `data/init/announcements.txt` gives all 353 event IDs flags — BOX (pause + modal), PAUSE, RECENTER, ALERT, UCR. Ordinary life ("The child Gasom Opirodoh begins playing make believe.") renders in the same voice as catastrophe, ending in a period; the exclamation mark is reserved and therefore enormous ("A vile force of darkness has arrived!"). Deaths are passive verdicts — the victim takes subject position, the killer arrives as a trailing agent.

**Descriptor vocabulary:** 462 procedural descriptors: 134 colors (Wikipedia-grade: puce, burnt umber, heliotrope), 43 shapes + 46 shape adjectives (stars get "three-pointed"; moons get "hidden|full|crescent"), 21 body patterns (SPOTS/STRIPES/MOTTLED, two-color combos), and 264 eye patterns (132 iris + 132 pupil; structure is fixed [WHITE, BLACK, variable-color] — one free slot each). Forgotten beasts are assembled from exactly this vocabulary; the first-sight line withholds the description, pauses the game, then recites it.

**Fold notes for the Roblox game:**
1. **DEATH-CAPS narrator:** keep DF's passive-verdict order — victim as subject, killer trailing — but rescale dread in CAPS/pause only on the event channel, never in wording; one exclamation mark lifetime budget per catastrophe.
2. **Forgotten-beast first-sight pause line:** announce "Something truly horrifying has vomited itself forth from the depths", hard-pause, then recite a procedurally assembled description from a fixed-slot descriptor table (color + shape-adjective + pattern) — withhold the noun until after the pause.
3. **Exchange purchase strings:** speak them as chronicle, not shop UI: "The dwarf Urist has bought the puce large gem." — subject-first, flat period, the price is a trailing agent; rarity scales by channel (sound/alert), not wording.

Sources: install read-only; templates byte-verified in binary + `data/init/announcements.txt` + `vanilla_descriptors/`. Full tables: `df_voice.json`.
