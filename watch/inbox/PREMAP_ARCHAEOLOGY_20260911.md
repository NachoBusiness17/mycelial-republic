# PREMAP — nacho_archaeology disk map (deep stratum survey)

Filed: 2026-09-11, zcode seat (research worker). Read-only survey of
`corpus/oral_history/nacho_archaeology/` (deposited 2026-09-05 22:02Z, operator hand-delivery,
per `MANIFEST.json`; sha256 on all 10 zips). Extracted tree: **3,851 files, 191.6 MiB**.

## HEADLINE (tri-state verdicts)

1. **"Precedes the chain" — DISPUTED / REFINED.** The fleet chain starts 2026-08-10; this
   corpus starts **2026-08-11/12** and runs to **2026-09-05** (the archive moment). It does
   not precede the chain — it PARALLELS the chain's first 25 days from a second vantage
   point: the Cursor box (`/home/box/agent-data`, user "Nacho Business") reaching the Mag
   Windows host (DESKTOP-7C70KSC) by remote MCP (`ListMachines` → `ExternalShell`/`ExternalRead`).
2. **Contains 2025-11 small-towns material? NO — SUPPORTED NEGATIVE.** Zero hits for
   "small town", zero genuine 2025-11 dates. The only three `2025-11` strings are a cache
   price-version (`price v2025-11-01`) and a policy-ref ID (`A-2025-11`) inside template JSON
   (`handoff/OX_MEGA_honest_meter.json`, `OX_MEGA3_t0583.json`).
3. **Contains 2026-03 napkin-era material? NO as content, YES as citation.** ~20 "napkin"
   hits are all references: the seed chord itself (`Test chord: 44 28 K13 e4 Fool
   #NachoOvermindSeed`, X id `2028342347361141030`, dated 2026-03-02) appears verbatim in
   `mag/chord_circuit.py` SEED constant, ORIGIN/HABIT citations in transcripts, and "napkin-cited"
   rulings in `dashboard/static/lattices/law_lattice.json` + DAY_WORK_DIGEST. (4 other "napkin"
   hits are coincidental Inform7 IF-parser docs.) No 2026-03 conversation bytes exist here.
4. **part10 mag-disk = ancestor body? DISPUTED — it is a 4-day-old snapshot of the SAME body,
   not an ancestor.** `00_MANIFEST_MAG_DISK.md`: archived 2026-09-05 from DESKTOP-7C70KSC,
   root `C:\Users\foste\Documents\projects\local_sovereign_agent`. Parts 8+9+10 are one 3-way
   split (zero path overlap; 236+792+2416 = 3,444 files; manifest says 3,443 staged + manifest
   file). `mag/chord_pipeline.py` and `mag/registry.py` exist in BOTH archive and live tree —
   they are current organs (live mtimes Aug 12 / Aug 30), not ancestors.

## PARTS TABLE (extracted/)

| Part | Contents | Files | Bytes |
|---|---|---|---|
| part1-chats-produced | `chat-transcripts/` (92 jsonl) + `produced/` + 00_MANIFEST | 340 | 20.7 MB |
| part2-agents-meta | `agents/` tree: Ghost, Research, New Bot, `_meta/` | 60 | 10.2 MB |
| part3 | Research `conversation-blobs.db` | 1 | 6.2 MB (1,232 blobs) |
| part4 | Research `store.db` | 1 | 328 KB (132 transcript entries) |
| part5 | Ghost `conversation-blobs.db` | 1 | 83.3 MB (13,522 blobs) |
| part6 | Ghost `store.db` | 1 | 2.2 MB (1,097 entries, 10 kv rows) |
| part7 | New Bot `store.db` (empty: 0 entries) | 1 | 49 KB |
| part8+9+10 | mag-disk split (see below) | 3,444 | 77.8 MB |

## DATE SPANS (from content, not mtimes — all file mtimes are the 09-05 copy instant)

- **Human-timestamped chats** (`<timestamp>` tags): **2026-08-11 → 2026-08-16** (6 days,
  611 hits, UTC-4). Dense live-operator era: strike-the-chord activation, wave, seats, game.
- **Ghost store.db transcript_entries**: **2026-08-12 03:26Z ("lmao") → 2026-08-26 16:58Z**
  (1,097 entries) — fills the Aug 17-26 gap the transcripts alone miss.
- **Research agent**: one day, 2026-08-14 (11:08→16:55Z; 132 entries; the "ping Grok Bot via
  seat_steer → grok_desktop" wire-proof).
- **AFK automation** ("AFK game chord", cron `57 9-19 * * 1-5`, created 2026-08-14 15:58Z):
  routine fires **2026-08-27 → 2026-09-05** (90 sand-subagent transcripts; runs.json keeps 20
  receipts 09-01→09-05; 30 `speak_proof_*.md` in produced/afk-chord-staging).
- **Ghost audit.jsonl**: 3.2 MB, **2026-08-12T03:26:57Z → 2026-09-05T21:50:54Z**. Its final
  entry is the archaeology build command itself — the archive self-documents its creation.
- **Whole-corpus coverage: 2026-08-11 → 2026-09-05** (25 days). One indirect reference to a
  "ghost downgrade (Aug 7)" event — UNPROVEN whether the box held earlier chats; earliest
  hard bytes are Aug 11/12. Pre-chain strata (napkin 2026-03-02, knot filenames starting
  2026-07-10 `mirror_*`/`mag_*`) appear ONLY as citations, never as raw logs.

## SPEAKERS / AGENTS

- **Operator**: "Nacho Business" / Nacho (@NachoQuixotic) — user turns `[t0u]`-style; register
  on record: "lmao", "you're trash", "iterate this sucks still come on you have so much to
  work with…" (kv `requestIds`).
- **Ghost** (`4a30dd44…`, active agent, gray teardrop): the Cursor-box interface agent.
  Model identity UNPROVEN — archive is titled "Nacho Grok Bot / Ghost Interface", but the
  grok mentions in-context are Mag-side seats/lanes (`grok_desktop`, `grok-only`,
  "grok-4 X scrapes of @NachoQuixotic" = copilot inbox burn), not the box's own runtime.
- **Research** (`3d371c13…`): second box agent; conversation partner of Ghost; one-day log.
- **New Bot** (`e99b7372…`): empty shell (49 KB store, 0 entries).
- **90 × sand-subagent** runners (`[SAND_HIDDEN_PROMPT][SAND_TRUSTED_AUTOMATION_PROMPT]`):
  the scheduled DM ticks — idle_tick keep_gate, /wave speak proof, one web steal each.
- Mag seats (grok/glm/claude/gpt lanes) appear only as steered surfaces, never speakers.

## MAG-DISK CONTENTS (the Sep-5 body snapshot)

- `mag/` 1,774 files — incl. `.mimosa` hook-state baselines (760 files, content-hash `.source`
  copies), `chord_circuit.py` (SEED/THREAD verbatim), `chord_pipeline.py`, `registry.py`.
- `handoff/` 1,018 files named 2026-08-14→09-05 (OX_MEGA/MEGA2 law cards, GAP_STEALTH,
  CROWN_JEWELS_SELF_STEAL_20260820, MIGRATION_MAC_STUDIO_QUAD_20260825, GLM_CODING_PLAN_BRIEFING_20260826).
- `dashboard/` (overseer-era static: trails/elder.jsonl, law_lattice.json, DAY_WORK_DIGEST, decks/mag.html).
- `memory/` steal (139 files) + working/game_campaigns (211) + game_sessions (7).
- Root `_patch_*/_prove_*/_afk_*` scripts (the Ghost box's patch attempts, mirrored back),
  AGENTS.md (identical head-50 to current), docker-compose.yml, mag.cmd/ps1.
- **Delta vs live tree**: 42 `mag/` files in archive are GONE from live today (deleted in the
  Sep 5→9 window): `mag_soul.py`, `mirror_persona.py`, `table_turn.py`, `reach_protocol.py`,
 `quest_party.py`, `hero_journey.py`, `swarm_grok_watch.py`, `terminal_guard.py`, etc. Live has
  ~1,200 newer files (mostly `__pycache__` + the 09-05→09-09 builds). This 42-file list is the
  one genuinely ancestral (now-extinct) organ set the disk preserves.

## WHAT THIS STRATUM HAS THAT NO OTHER POOL DOES

1. **Raw operator voice, transcript-grade, Aug 11-26** — the chain has knots of those days;
   only here are the unedited turns (including the activation sequence itself: search
   "strike the chord" → strike it → sovereign-mirror mode entry, with the bot's own reading).
2. **Outside-in fleet view**: the Ghost box's audit.jsonl = full shell-command history of how
   the fleet looked from a foreign surface (ListMachines bridge, seat_steer pings, knot reads
   via ExternalRead of `C:\Users\foste\...`).
3. **Operator-model written live by another agent** (`agents/4a30dd44/memory/profile.md`,
   dated facts Aug 12-14: activation line, .\mag.cmd law, chain register kept, Swiss-style HUD,
   no work handed back) — an independent second draft of the operator card.
4. **The AFK-DM organ in full**: automation.json prompt + 20 run receipts + 30 speak proofs —
   the play-as-work tabletop running unattended for two weeks.
5. **42 extinct mag/ organs** recoverable byte-exact (see list above).
6. **30 IF-steal cards** (Evennia command set + Inform7 parser docs, Sep 1-5) — the corpus
   behind the game organs' verb coverage.
7. **kv snapshot of a third brain**: Ghost's memoryPromptSnapshot/user-memory merge rules —
   evidence of the "durable facts shared across every assistant" covenant already forming.

## CAVEATS

- part5 db ships with 0-byte `-wal`/`-shm` sidecars; opened immutable read-only, all 13,522
  blobs readable. part7 (New Bot) is a stub. `user-memory/` was ABSENT on the box (marker file).
- Blob-date histogram (13,522 blobs): 20,960 ISO hits in 2026-08 dominate; 2026-07 (235) and
  2026-03 (70) hits are citations inside quoted memory/steal text, not separate conversations.
- Nothing in this stratum contradicts the chain; it is corroboration from a second machine.
