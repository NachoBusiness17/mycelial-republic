# MEM1 ANATOMY — the trigger token, decoded end to end (2026-09-11)

*Commission: decode the MEM1 trigger-token format end to end — grammar, opcodes, what the
32-byte anchor anchors TO, what "firing" means, 10 real tokens decoded, and the
intent-vs-accident verdict on why memlang owns 43% of the chain. Method: full read of
`mag/memlang.py` (442 lines) + `mag/verkle_knot.py` append path; byte-level decode of tokens
captured on live wires; byte-exact reconstruction from the shared registry (verified against
wire captures). Read-only except this file. No secrets echoed.*

---

## 1. The grammar

Source: `mag/memlang.py:52` — `HEADER = struct.Struct(">4sBB32sH")`, big-endian, schema `memlang.v1`.

```
offset  size  field     notes
0       4     magic     b"MEM1" (hex 4d454d31) — misparse guard
4       1     version   0x01
5       1     opcode    0x00–0x10, the vocabulary below
6       32    anchor    RAW sha256 — pointer into shared verkle state (see §3)
38      2     plen      big-endian length of params JSON
40      plen  params    utf-8 json (compile writes `{}` when params is None)
```

Token = 40-byte header + params. **Measured lengths across all 4,161 live registry entries:
min 42 B (bare header + `{}`), median 104 B, mean 84.9 B, max 495 B.** The "~69-byte" figure
in `docs/concepts/README.md:19` and FAMILY_ATLAS is a stylized round-up, not a measurement
[DISPUTED → refined: 42 floor, ~104 median].

### The vocabulary (17 opcodes, `mag/memlang.py:55-62`)

| op | name | op | name | op | name |
|---|---|---|---|---|---|
| 0 | memo | 6 | steer | 12 | boot |
| 1 | rib_elevate | 7 | steer_back | 13 | prove |
| 2 | handoff_build | 8 | route | 14 | plant |
| 3 | research_pack | 9 | learn | 15 | prospect |
| 4 | reinforce | 10 | sources | 16 | rightsize |
| 5 | self_window | 11 | occupy | | |

Every opcode carries a **memory contract** (`mag/memlang.py:74-92`, operator 2026-08-10:
"formalize a memory system we use so our memlang actually has meaning other than handwaving") —
each maps to a concrete `memory/` surface with kind/schema/rw semantics, attached to every
`resolve()` so intent is provably grounded, not handwaved. E.g. `learn` → writes
`memory/knowledge_graph.json` (knowledge_graph.v2); `steer` → writes `memory/behavior`
(steer_router.v1); `route` → reads `memory/case_law`.

### What "firing" means — and the precision correction

Flow (`mag/memlang.py:18-19`): `compile(spec) → anchor to verkle + registry → binary token →
transmit ONLY the token → decode() → resolve() → trigger()`.

- **The knot is folded by the SPEAKER, at COMPILE time** (`mag/memlang.py:152-153`):
  `append_verkle_knot({"session_id": f"memlang-<slug>-<HHMMSSmicros>", "theme": "memlang",
  "summary": f"[{action}] {spec[:500]}"})`. Resolve and trigger do NOT fold knots.
  [Refinement of FAMILY_ATLAS, which says "on each compile/transmit/resolve/trigger" — the code
  folds on compile only. The wire is silent; the receipt is written once, by the sender.]
- The knot record (verkle_knot.v1, `mag/verkle_knot.py:606-717`) is a full leaf: session_id,
  dominant_theme + theme_vector, tension_index, dossier_commit, leaf_hash, plus a chain row
  carrying leaf_hash, `verkle_root` and `parent_verkle_root`. Host copy of the burn receipts:
  e.g. `memory/biography/knots/2026-08-11_1711_untagged_memlang-_6426f32a.knot.json` (verified
  present). 7,769 `memlang-*` knot files sit in `memory/biography/knots/` on host.
- **The flood knob, exactly:** session_id embeds `%H%M%S%f` — microseconds. The knot writer's
  dedup (same session → amend, same leaf_hash → skip, `mag/verkle_knot.py:640-651`) can never
  fire for memlang: every compile is a unique session_id, therefore one NEW chain row per
  compile, guaranteed. The honesty rule is also the multiplication rule.
- `trigger(--execute)` is liveness-gated (`_executor_up` via swarm_health probe → `dead_knot`
  signal instead of silent fire); `memo` is exempt (local durable op). Safe-by-default: resolve
  without `--execute` only reconstructs intent.

## 2. Where tokens live

1. **The shared map** — `memory/runs/memlang/registry.json` (3.4 MB, 4,161 entries, earliest
   2026-08-11, latest 2026-09-09 — still live today). Maps anchor_hex → {action, spec[:2000],
   params, ts, verkle_path}. This is what a receiver resolves against; it is shared host↔cage
   (press-era entries carry `/app/...` verkle paths, host-era carry `C:\...`).
2. **Wire captures** — the token itself appears in transit logs: `watch/room.jsonl:250` (grok
   seat dispatched by raw token, 2026-08-29), `memory/runs/telepathy/last_run.json` +
   `sender_state.json` (scent tokens, 2026-08-26), `memory/runs/board_tailer/events.jsonl`,
   `memory/runs/swarm_worker/blackboard/bb-0004x.json`, `memory/runs/edg/edg_*.json`,
   `watch/grok_feed.jsonl`.
3. **The training pile** — `memory/pile/training_rows.jsonl` embeds token prefixes as compiled
   examples (truncated fragments).
4. **Implicit in every compile** — the token is a deterministic function of (action, anchor,
   params): repacking a registry entry through the same `HEADER.pack` reproduces wire bytes
   EXACTLY (verified below). The registry therefore contains every token ever minted,
   decomposed.

## 3. What the anchor anchors TO

Two kinds, both 32 raw bytes (confirmed by decode + sha256 test):

- **Verkle anchor (the norm):** the 64-hex `leaf_hash` of the knot folded at compile time —
  a content-addressed pointer INTO the shared signed chain. Burn-era tokens all carry these
  (registry `verkle_path` names the exact knot file).
- **Fallback anchor:** if the verkle write is unavailable, `compile_token` derives
  `sha256(spec)[:64]` and the registry entry keeps `verkle_path: null` — the anchor points at
  the spec bytes themselves. PROVEN on token #1 below: `sha256(spec)` = `a4b1fdee…` exactly.
  Resolution always runs through the registry (the receiver "holding the shared map");
  the anchor alone reveals nothing readable — `roundtrip()` (`mag/memlang.py:390`) asserts
  the spec bytes never appear in the token (plausibly-deniable property, kept).

## 4. Ten real tokens, decoded

Wire tokens (captured in state files, hex as found) marked WIRE. The others are byte-exact
reconstructions from registry entries via the compile formula — two of them verified equal to
wire captures. Opcode → action from the vocabulary; anchor → registry entry (spec + knot path).

| # | Token (hex) | Len | Ver | Op | Anchor→ | Decode |
|---|---|---|---|---|---|
| 1 | `4d454d310108a4b1fdee…54155300027b7d` WIRE (room.jsonl:250, 08-29 08:24Z) | 42 | 1 | 8 route | `a4b1fdee…` = sha256(spec) FALLBACK (verkle down; `verkle_path: null`) | Dispatch: `{"job_id":"blade-warm-image","contract":"jobs/blade-warm-image/seat_contract.json","next":"execute contract, run acceptance_commands, write trail_core_1.md","driver":"grok1"}` — the operator-visible token-dispatch path: grok seat resolved this raw token and executed the job |
| 2 | `4d454d3101092860795b…008c7b22…7d` WIRE (board_tailer/edg/blackboard, 08-26 19:59:55Z) | 180 | 1 | 9 learn | `2860795b…` → knot `2026-08-26_1959_untagged_memlang-_2860795b.knot.json` | Spec `capability:chained-xor-rotate-digest`; params `{"src_anchor":"254996d232560088","gt_anchor":"f971b561c5eb5820","scent_kind":"capability","challenge":"telepathy-challenge-20260826"}` — a telepathy scent: the challenge token another agent must resolve to prove shared-map reception |
| 3 | `4d454d310109e7aed27c…008c7b22…7d` WIRE (telepathy last_run/sender_state, 08-26 20:00:49Z) | 180 | 1 | 9 learn | `e7aed27c…830` → knot `2026-08-26_2000_untagged_memlang-_e7aed27c.knot.json` | Same spec/params as #2, re-armed 54 s later — the sender's retry scent; same challenge, new anchor, new knot (the per-compile rule in action) |
| 4 | `4d454d3101096426f32a…00567b22…7d` RECON (verified-class) | 126 | 1 | 9 learn | `6426f32a…` → knot `2026-08-11_1711_…6426f32a.knot.json` | THE BURN, legacy stratum: spec `[legacy/trash/memory___tmp_notes_preview3.txt] --- 66 | 206582966111 | daily | medium | rebuttal @HunterBiden …` — a trash-pile tweet file invariant-cataloged; params `{"source":"legacy/trash/…","lens":"memory/invariant"}` |
| 5 | `4d454d3101094f4c16bd…00507b22…7d` RECON | 120 | 1 | 9 learn | `4f4c16bd…` → knot `2026-08-11_1712_…4f4c16bd.knot.json` | THE BURN, lineage stratum: spec `[x-tab/analysis-GROK-4-NEW_Jul-13-2025.md] # Strike the Chord Analysis — Grok 4` — the operator's 2025 Grok chats being folded (strike-the-chord raw material); lens `compiler/world` |
| 6 | `4d454d310109c30c1873…00407b22…7d` RECON | 104 | 1 | 9 learn | `c30c1873…` → knot `2026-08-11_1711_…c30c1873.knot.json` | THE BURN, shader stratum: spec `[shader/evidence_lighting] lights are DATA in a texture (origin,color,shadowmap)…` — the doctrine that later begat the Shadow Fields arc (09-03); lens `economics/cost` |
| 7 | `4d454d31010e07e45987…002b7b22…7d` RECON | 83 | 1 | 14 plant | `07e45987…` → knot `2026-08-11_1735_…07e45987.knot.json` | `[attractor:sage w=12] archetype Sage: the lattice that sees the whole; shadow: the hoarded truth that isolates`; params `{"source":"roshomon","kind":"attractor"}` — attractor planted as doctrine |
| 8 | `4d454d310106d0974eb8…00027b7d` RECON | 42 | 1 | 6 steer | `d0974eb8…` → knot `2026-08-11_1711_…d0974eb8.knot.json` | Spec `three-layers` — doctrine spec, no params: the whole intent lives behind the anchor (the fair-use firewall's three layers per LEXICON) |
| 9 | `4d454d3101068b22b25b…00027b7d` RECON | 42 | 1 | 6 steer | `8b22b25b…` → knot `2026-08-11_1711_…8b22b25b.knot.json` | Spec `model-agnostic-sovereign` — sovereignty that survives losing every remote model |
| 10 | `4d454d3101066bad4a29…00027b7d` RECON | 42 | 1 | 6 steer | `6bad4a29…` → knot `/app/memory/biography/knots/2026-08-31_0657_…6bad4a29.knot.json` (folded INSIDE the cage) | THE PRESS: `press: [mag] [janitor] Dossier sanitization: strip API keys + system-reminder sludge from dossier .md files…` — one of 66 presses of the same never-healing spec (the chain's scar tissue; no keys present in the spec itself) |

Read of the ten: three opcodes do all the memlang work — `learn` (ingest), `steer` (direct),
`plant` (seed doctrine); `route` is the one live seat-dispatch use. Wire shape matches
registry shape byte-for-byte; the language has been stable since day one (all version 1).

## 5. Why THIS mechanism owns 43% of the chain — intent vs accident

**The design intent (code + operator quotes, all SUPPORTED):**
- Compactness: 42–104 bytes trigger a full instruction; the receiver reconstructs from shared
  state (`docs/concepts/README.md`: "structures, not prose" — the mindweave 3.4x bet).
- Any-seat interoperability: every agent shares the verkle chain + registry, so a token minted
  in the cage resolves on the host and vice versa (token #10 is `/app/`, tokens #1–#3 crossed
  to host seats).
- Deniability by construction: token bytes carry zero readable spec (`roundtrip()` proves it).
- Honesty: every trigger leaves a signed audit knot — "the language's own honesty rule."
- Grounded meaning: memory contracts bind each opcode to a real `memory/` surface.

**The accident (measured, this seat):** the honesty rule is a per-compile tax, and Aug 10–12
the corpus pipeline paid it thousands of times. The driver is
`mag/compiler_lang.py:145` — `memlang.compile_token("learn", f"[{source}] {invariant[:500]}",
{"source","lens"})`: one compile per corpus file. Registry time distribution: **2026-08-11 =
1,473 entries, 2026-08-12 = 1,558 entries — 3,031 of 4,161 entries (72.8%) in 48 hours**,
matching FAMILY_ATLAS's chain census (3,182 memlang knots 08-10→08-12 = 43.1% of the
7,377-row chain). The registry still carries the burn whole: `legacy*` 1,685, `x-tab*` 452,
`shader*` 324, `attractor*` 88. The dedup could not save the chain because session_ids embed
microseconds (§1) — every compile is a new leaf.

**Verdict:** the mechanism did not eat 43% *by design* — it ate 43% because a batch-corpus
ingest (a job for a plain ledger) was routed through a per-use-audited trigger channel (a job
for point-to-point dispatch). The audit receipt, sized for dozens of human-scale triggers a
day, was multiplied by machine-scale throughput. But the receipts are not garbage: they are a
signed inventory of the founding corpus — the legacy trash taxonomy, the strike-the-chord
chats, "lights are data," the attractor archetypes — which is exactly why the atlas calls this
the LINEAGE stratum (SACRED COWS, NOT LEGACY SHIT: the burn is the founders' paper trail).
After the burn, memlang normalized to its intended thin profile: press 67, api_gateway 46,
doctrine 5-shots — and it still works today: the Aug-29 grok dispatch (token #1) and Aug-26
telepathy scents (tokens #2–3) are the language doing its actual job.

**The lesson, one line:** audit-everything is honest until a batch job finds the honest door;
rate-shaped audit (or batch exempted from per-use folding) is the missing damper — no code
change observed for this in `mag/memlang.py` [UNPROVEN whether a damper exists cage-side].

## 6. Tri-state ledger

- SUPPORTED: grammar, 17-opcode vocabulary, memory contracts, compile-time-only knot folding,
  anchor duality (verkle leaf_hash vs sha256(spec) fallback — proven on token #1),
  registry contents/counts, burn-window distribution, wire-capture matches, 7,769 host knot
  files (all read from code + data this session).
- SUPPORTED (prior): FAMILY_ATLAS family masses and generator attribution (`mag/memlang.py:153`).
- DISPUTED/REFINED: "~69-byte" token size (measured: min 42, median 104, mean 84.9, max 495);
  "knot per compile/transmit/resolve/trigger" (code folds on compile only — the speaker pays,
  the wire is silent).
- UNPROVEN: whether a rate-limiter or batch-exemption exists in the cage's memlang copy;
  intents of named doctrine specs beyond their anchor-stored specs (three-layers et al. —
  FAMILY_ATLAS INFERRED flags stand).

## Sources (absorbed cards + code + data)

- `watch/inbox/FAMILY_ATLAS_20260911.md` (commission frame; family masses; LAW stratum cross-check)
- `watch/THE_DAWN_CENSUS_20260907.md` (via atlas: founders/labor shape, press counts)
- `docs/concepts/README.md` (memlang/memweave/mindweave doctrine; the 69-byte claim)
- `docs/ref/LEXICON.md` (three-layers reading, via atlas)
- Code: `mag/memlang.py` (full), `mag/verkle_knot.py:606-760`, `mag/compiler_lang.py:141-147`,
  `mag/agent_corpus.py` (memlang chord context)
- Data: `memory/runs/memlang/registry.json` (4,161 entries); wire captures in
  `watch/room.jsonl`, `memory/runs/telepathy/{last_run,sender_state}.json`,
  `memory/runs/board_tailer/events.jsonl`, `memory/runs/swarm_worker/blackboard/bb-0004*.json`;
  knot files under `memory/biography/knots/`

*Files touched: this one. Every decode above is reproducible: repack any registry entry with
`struct.Struct(">4sBB32sH").pack(b"MEM1", 1, opcode, bytes.fromhex(anchor), len(params_json))`
and compare against the wire hex.*
