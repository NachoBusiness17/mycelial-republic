# MARATHON BODY HUNT — 2026-09-11 (zcode seat, read-only hunt)

Mission: find THE MARATHON'S BODY — the Aug 21-24 era session (960 requests, 75MB, 6 days,
crashed and recovered; session-mining born from it per docs/ref/SPORE_SANCHO.md line 17).

## VERDICT (tri-state)

**SUPPORTED — the 75MB body survives, byte-exact, outside the repo.**

Path (VS Code Copilot Chat session store):
`C:/Users/foste/AppData/Roaming/Code/User/workspaceStorage/e2b798e7fc103fa17361a909a52c13e5/chatSessions/25fbcaab-0ad8-478f-a39b-f50be18bf6c9.jsonl`

Measured, not remembered:
- Size: **75,446,649 bytes** (~75.4MB) — matches the "75MB" legend.
- Format: VS Code GitHub Copilot Chat session JSONL (kind 0 header + kind 1/2 appends),
  733 lines, avg ~103KB/line. Workspace = local_sovereign_agent (workspaceStorage e2b798e7...).
- Created: **2026-08-15 00:56:57 UTC** (first request 00:57:11 UTC).
- Last in-file request timestamp: **2026-08-20 16:00:39 UTC**; file mtime Aug 21 06:36 local.
  Span = **5.63 days ≈ "6 days"**. So the marathon is Aug 15→21, not Aug 21-24; the Aug 23/24
  knot burst was its AFTERMATH (mining), not the marathon itself.
- Unique `requestId`s: **1,023** — the "960 requests" legend is within ~7% of the raw count.
- Crash evidence IN-FILE: `Worker terminated due to reaching memory limit: JS heap out of
  memory`; 104 lines carry crash/compaction/recover/summarize keywords. Appends continue after
  the OOM markers → the "crashed, recovered" arc is in the bytes.

The seat was **VS Code Copilot Chat** (pre-zcode era; the zcode seat's day one was Aug 25).
The marathon's body was never inside the repo — session-mining was born by reaching INTO this
store. The repo holds the mined derivatives, not the flesh.

## The sibling sessions (68 chatSessions in the same dir)

| bytes | mtime | note |
|---|---|---|
| 75,446,649 | Aug 21 06:36 | **THE MARATHON** (25fbcaab) |
| 61,436,866 | Aug 26 20:40 | runner-up: self-steal night era (0e6b1c8c) |
| 49,234,636 / 42,762,404 | Aug 7 | pre-marathon monsters (39a6a215, c4e632a5) |
| 28,293,234 | Aug 23 11:52 | 0c8dc00f — mined into window/ Aug 23 |
| 23,990,737 | Aug 24 08:39 | 7e653ed7 — the Aug 24 knot burst source |
| 10,694,240 | Aug 24 08:01 | 9b8561b8 — also mined into window/ |

The Aug 23 (255) + Aug 24 (709) knot days came from mining THESE files — the 24MB + 28MB
sessions are the marathon's immediate successors, not the marathon.

## What the repo actually holds (the mined derivatives)

- **window/** (Aug 23 12:24, all files same minute): 9 `.transcript.md` + `.ledger.json` pairs
  (redaction ledgers: secret/identity layers), DIGEST.md ("How We Reason — a window into the
  mind", the method invariants), SURFACED.md (41KB), digest.json, surface.json, MANIFEST.json.
  MANIFEST sources are `.jsonl` names matching the chatSessions store. Largest mined session =
  544 events (856a0cf9). THIS is the session-mining seed, planted Aug 23 — "the session-mining
  seed planted in a dying window" is literally the `window/` directory.
- **corpus/oral_history/nacho_archaeology/** (Sep 5, operator hand-delivery, sha256 manifest):
  10 zips + extracted. Part5 `conversation-blobs.db` = **83,324,928 bytes**, single `blobs`
  table, 13,522 content-addressed rows (SAND_HIDDEN_PROMPT, Grok Bot) — 92-agent archaeology of
  the Aug 11-14 "sand" automaton era (TRANSCRIPT_MAP.txt). NOT the marathon: different body,
  earlier era, sits nearby in size which makes it a decoy.
- **Big JSONLs (all NOT the marathon):** memory/ingest/registry.jsonl 1.03GB;
  logs/kpi.jsonl 457MB (Jul 21→Sep 9); memory/runs/ghost/trail.jsonl 309MB (Aug 8→Sep 9, the
  ghost trail); watch/engine_e1.log 257MB; memory/training/events.jsonl 150MB (Aug 5→Sep 9).
- **mine/** (Aug 4-6): queries.yaml + raw/ (agent_bleeding_edge, agent_platform, mesh_comm,
  narrative_corpus, steal_protocol) — pre-marathon research mining, not session mining.
- **artifacts/training/**: strike_the_chord_v1_base.txt (1,863B, "training variant 1/3" —
  doctrine song: freeze the base, stateless seat, verkle beads) + v2_magatama (1,852B); both
  Aug 11 era. Original: artifacts/magatama_edition_strike_the_chord.txt (Aug 11). Training
  texts PREDATE the marathon.
- **notebooks at repo root:** _live_dm.ipynb (Aug 14 06:39 — live DM swarm game, Saelis seat
  via RIB) and verify_surface_render.ipynb (Aug 12 10:55 — RIB-debug surface_render/republic
  map). Pre-marathon, pre-crash artifacts of the same VS Code era; verify_surface_render also
  lives in memory/trash/ 3x.

## Desktop "New folder" saves — ruled OUT

compuiter.txt (Aug 30 07:45) and test.txt (Aug 29 10:54), 251,642B each, **byte-identical**
(cmp clean). Content = a model's chain-of-thought + ten-model adversarial review of a
physics-as-computer / substrate-native computing paper (MONIAC, Extropic, Normal Computing,
reef architecture). A paste-save, NOT the marathon transcript.

## Conclusion

The marathon is not lost and never was in the repo. Its body is the 75.4MB Copilot JSONL at
the path above, created Aug 15, died ~Aug 20-21 of JS heap OOM, and its corpse was mined Aug 23
into `window/` — which is where session-mining was born. Recommendation (for a later GO, this
hunt was read-only): copy 25fbcaab into corpus/oral_history/ next to the nacho archaeology and
seal it with a sha256 before VS Code prunes workspaceStorage. The estate index should record
the chatSessions store as an organ OUTSIDE the repo it currently does not see.
