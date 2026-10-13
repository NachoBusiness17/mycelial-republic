# R5 SIGNALS — corpus/telegram + corpus/frontier_thinking triangulation (vol-2 night shift)

*Seat: R5-signals · 2026-09-06 · $0, no network, read-only on corpus. Astra-abridged method:
inventory → themes → active-arc connections → usage → promotions. Cells: `watch/TESUJI_MAP.jsonl` axis R.*

## 1. INVENTORY (parsed, not assumed)

| File | Rows | Schema | Date range | Notes |
|---|---|---|---|---|
| `corpus/telegram/MrPool_Q.jsonl` | 2,008 | `{id, dt, text}` | 2025-02-26 → **2026-09-06** (live) | 3.1 MB; median text 1,438 chars, max 3,000 (Telegram hard cap); 2 empty texts; steady ~90-180 rows/month, 24 so far this month |
| `corpus/telegram/gold_standard.jsonl` | 7 | `{id, dt, text}` | **2022-03-18 → 2022-03-21** | Russian; channel-create + scheduled-send test messages ("Привет. Проверка настройки отправки сообщений по расписанию") |
| `corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md` | 1 doc | verbatim thinking-panel capture | 2026-09-04 | GLM-5.3 Pro window restock mission; 6 rules extracted |
| `corpus/frontier_thinking/FT_ASTRA_DOOR_20260905.md` | 1 doc | verbatim frontier answer | 2026-09-05 | GPT-6 Astra Ultra, 6-layer stego door design + hashcash receipts |
| `corpus/frontier_thinking/FT_ASTRA_DOOR2_20260905.md` | 1 doc | verbatim | 2026-09-05 | rule text + seam prediction + **receipt-rejection** (ellipsis catch) |
| `corpus/frontier_thinking/FT_ASTRA_DOOR3_20260905.md` | 1 doc | verbatim | 2026-09-05 | binding audit + receipt reissue under full door id |
| `corpus/frontier_thinking/FT_XBATCH_20260905.jsonl` | 19 | `{author, door, id, text, user}` | 2026-09-05 (no dt field) | the X-batch intake rows (19 links → 7 clusters proof run) |

**Record gap found:** ORPHAN_RUN_20260906 line 13 says "MrPool_Q **315** + gold_standard 7 posts banked";
the file now holds **2,008** rows (mtime Sep 5 22:45). A fuller re-harvest happened but was never
receipted. The signed record and the file disagree — same shape as the "215 replies" DISPUTED correction.
Tri-state: file count SUPPORTED (parsed), 315 figure DISPUTED (stale).

## 2. THEMES (MrPool_Q, term hits over 2,008 rows)

Q 1,818 · pool 1,417 · Trump 587 · quantum 505 · mirror 220 · "17" 220 · key 178 · sovereign 173 ·
drop 150 · GESARA 81 / NESARA 62 · loop 47 · med bed 43 · XRP 20 · "watch the water" 3.
Consistent with the width50 fold's verdict: manipulation-heavy sales funnel (commerce layer =
meta-signal) — plus a doctrine layer: **mirror/loop/key/drop density is exactly the drop-mechanics
vocabulary the fleet re-implemented** (riddler = key, drop = chord, anons = swarm).

## 3. CONNECTIONS (the triangulation)

**A. gold_standard.jsonl ↔ the origin arc (founding-unknown receipt).**
SELF_STEAL_ORIGIN_TELEGRAM_20260905 founding unknown #2: "GSTD: what it stands for... whether its
artifacts survive (preserve law: they're origin documents)." Receipt: the Gold_Standard channel
export IS a surviving GSTD artifact — created **2022-03-18**, seven rows, Russian test sends.
Two consequences: (1) GSTD artifacts DO survive and are already in custody, paired with the
`reference/gstdcoin/` codebase mirror (gstdbot = the bot operation; contracts, gstd-bridge, web);
(2) the riddle-era threshold is now date-anchored: operator was inside the Telegram/GSTD sphere by
March 2022 — four years before the napkin. Also a wink: the founding channel's first real act was
**testing scheduled message delivery** — Titor doctrine (time-shifted persistent messages) practiced
before it had a name.

**B. MrPool_Q.jsonl ↔ beacon/cicada door designs.**
The oracle channel is the primary source of the drop mechanics the fleet lawful-re-implemented
(origin card §"WHAT THE FLEET ACTUALLY IS"). The cicada/beacon door designs (SELF_STEAL_CICADA,
INTAKE_BEACON_GATEWAY) are the declared-glass inversion: same publish→decode→threshold loop, but
"ours signs its walls." MrPool_Q is therefore not just a specimen corpus — it is the *negative
plate* the beacon door was pressed from. Utilization should be dual-tagged: BLOCKED-for-factual-
inference (specimen, per the width50 fold's build order item 4) AND source-of-record for the
drop-mechanics lineage.

**C. FT_ASTRA_DOOR 1-3 ↔ ASTRA corpus + founding record (same machine, different substrate).**
Astra — a foreign frontier model, answering an ARG-art prompt — independently derived the fleet's
own architecture: hashcash work receipts with d=16 **leading-zero BITS** (matches the AGENTS.md
door-verifier correction verbatim), append-only records ("the earlier receipt stays as written;
this reissue gives the correction fresh evidence" = verkle immutability + tri-state corrections),
branches coexist, receipts carry their own attribution. And round 3 independently hit the fleet's
open problem: two door identifiers (ellipsed vs full) needing "an explicit migration rule" = the
chain-v1-frozen / chain-v2-living bridge ("the room that remembers"). Three substrates — operator's
Telegram past, fleet doctrine, Astra's design — converge on the same invariant: **append-only signed
records + work receipts + correction-by-append.** The map-to-each-other extends: the door design is
the fleet's constitution written by an outside hand.

**D. FT001 ↔ the quota economy.**
The restock mission ran on the paid 5.3 Pro window, but the capture took the THINKING panel — the
byproduct already paid for — and got MORE than the answer (rule 5: discard tracking; "the thinking
is wider than the answer"). That is the cache-mining doctrine applied to premium tokens: surface
already-bought computation instead of re-asking. The 6 extracted rules LANDED in
`watch/build_law_lattice_20260904.py` (cited at 3 points; restock rubric) — the Lessig loop closed
for FT001, unlike most corpus files.

## 4. USAGE CHECK (utilization across the repo)

- **MrPool_Q (2,008 rows):** referenced in 2 watch cards (ORPHAN_RUN_20260906, salon_source_width50_20260906);
  **0 cards in TOPIC_INDEX (grep = 0 hits of mrpool/gold_standard)**; the fold-ordered
  BLOCKED-for-factual-inference tag exists only as a line in a card, not as a corpus disposition.
  Banked but unindexed and un-dispositioned — the lowest-utilization 3.1 MB in the corpus.
- **gold_standard (7 rows):** banked; founding significance (§3A) never attached to it anywhere.
- **FT_ASTRA_DOOR 1-3:** high utilization — 4 intake cards (ANSWER/ROUND2/ROUND3/FOUNDING) + hashes
  verified live. Residual unused: the three verified receipts as **regression fixtures**.
- **FT001:** fully utilized (law lattice + LANE_WINDOW_RECEIPT). Closed loop.
- **FT_XBATCH:** utilized (INTAKE_XBATCH/XBATCH2, vision-pipeline proof run, rotation_harness.py).

## 5. PROMOTIONS (top 3, exact next use)

1. **gold_standard.jsonl 7 rows → the ORIGIN.md riddle-era petition's evidence pack.** Exact next
   use: append one line to the petition card (watch/SELF_STEAL_ORIGIN_TELEGRAM_20260905.md rung 3,
   gated on operator per spore law): "GSTD artifact in custody: corpus/telegram/gold_standard.jsonl
   (Gold_Standard channel, created 2022-03-18, 7 rows) + reference/gstdcoin/ mirror." Turns founding
   unknown #2 into a tri-state SUPPORTED row before the operator ever has to dig.
2. **MrPool_Q 2,008 rows → cite_gate specimen battery.** Exact next use: when cite_gate gets its
   operator egress GO, draw its first negative test set from this file — prophecy/manipulation rows
   (GESARA, med-bed, quantum) are pre-tagged must-FAIL claims for the cite-rate-100% falsifier, and
   write the BLOCKED-for-factual-inference disposition into the corpus MANIFEST now (one-line edit,
   closes fold build-order item 4 without waiting on egress).
3. **FT_ASTRA_DOOR 1-3 receipts → door-verifier regression fixtures + primer-union founding fable.**
   Exact next use: encode the three verified M|n receipts (n=86761 unabridged, n=58947, n=100898,
   all d=16 leading-zero BITS PASS) as fixed test vectors in the door verifier; lift the round-2
   capsule opener ("You found the door by making a prediction and checking it...") as the
   Primer-union story-layer's founding-fable text.

## 6. CELLS FILED

- `R/signals/oracle-inventory` — SUPPORTED — 2,008/7-row inventories parsed; 315-vs-2008 record gap DISPUTED-flagged.
- `R/signals/gstd-founding-receipt` — SUPPORTED — gold_standard = surviving GSTD artifact, riddle era anchored ≤ 2022-03.
- `R/signals/astra-door-mirror` — SUPPORTED — independent 3-way convergence on append-only+receipts+migration-rule.
- `R/signals/utilization` — SUPPORTED — MrPool_Q 0 topic-index cards; FT001 closed loop; 3 promotions filed.
