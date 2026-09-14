# VISION FLEET CHARTER — the read/write flow under one owner (2026-09-05)

**OPERATOR GRANT:** "you need to be in charge of the vision fleet as well —
writing and reading, organizing the flow." This card is the flow, owned by the
zcode seat (Max). Nothing here is new machinery — it is the census of organs
that now answer to one desk, with the gates named.

## THE FLOW (sense → record → read → decide → remember)

```
 SENSE   pastes (operator hand) · X decks (Pro) · android farm bodies ·
         MCP sensors · monitor · live_feed · feed absorbers
    ▼
 READ    READ verbatim ($0: web_reader/oembed/eye/burst) — vision pipeline v1
    ▼
 FILTER  against the goal lattice (rubric PULL axis; live arcs as data)
    ▼
 INTERPRET  clusters, not items (DeepSeek pattern; salons; roshomon)
    ▼
 CITE-GATE  mag/cite_gate.py — BUILT 09-06 by the research-lane seat, ADOPTED
         + anchor-amended (dashboard) same day by this seat. Deterministic,
         $0-law (URL fetch door stubbed pending operator GO). Falsifier holds
         live: fully-cited card = 1.0, uncited = demote to Unproven.
    ▼
 RIGHTSIZE   REMEMBER | WINDOWED | BUILD (launch same turn)
    ▼
 FILE+WIRE   card (+ Cites: line, cites_at_birth) + trail + room row +
         surface + mirror, same turn
    ▼
 READ ORGANS (the corpus reading itself)
         topic_index.py (what do we know about X) · read_receipts.py (who reads)
         stale_sweep.py (what's dying) · decision_hook.py (what needs the human)
    ▼
 DECIDE   operator board actions (decisions_done.jsonl) · gates
    ▼
 REMEMBER chain knots · seals · graveyard · mirrors
```

## THE DESK (organs + states)

| Organ | Does | State |
|---|---|---|
| cite_gate.py | claims→sources, demote-before-rightsize | LIVE (adopted 09-05, anchor-amended; falsifier 1.0 verified on 2 cards) |
| cites_at_birth.py | Cites: law on new cards; edges feed the meter | LIVE (self-test PASS; first card rc=0) |
| topic_index.py v3 | IDF topics + full-text query, nightly rebuild | LIVE (701 cards, 3,814 topics, 1.5s) |
| read_receipts.py | back-refs + page hits, nightly | LIVE (baseline 20 zero-backref) |
| stale_sweep.py | orphans + Unproven>7d; 14d→graveyard | LIVE (baseline 20; execute day-gated) |
| decision_hook.py | Decision: lines → the PDB board | LIVE (in nav) |
| intake rubric | the judgment as data | LIVE (58-law lattice behind it) |
| READ engines | web_reader, oembed, 3B eye, burst | LIVE $0 |
| GLM-OCR lanes (2) | metered vision reads | KEY-GATED (B2 family) |
| 5.3-flash SEES | multimodal read at concurrency 50 | LIVE on plan lanes |
| android eyes (B2) | screenshot→read loop on the farm | KEY-GATED |
| live_feed + swarm eye | board PNGs → qwen2.5vl 3B | LIVE $0 (eye reads shape, code owns numbers) |
| cite_gate URL door | fetch + content-sha receipts | STUB — operator GO for egress |

## THE THREE DOORS (one gate, operator hand)

Network egress for: cite_gate URL-VERIFIED class · B2 OCR metered reads ·
B2 android eyes. All are the same law (metered lanes need the word); all are
optional — the flow is complete without them, just RECORDED-not-VERIFIED.

## FALSIFIERS (inherited, live)

- Vision pipeline: rotation test + cite-rate 100% (falsifier #2 demonstrated
  day one: FIRST_CITE_CARD_EARBUD_FIX gates 1.0).
- Consumption: orphans 20→≤5, Unproven 209→≤150 w/ ≥10 re-tested, ≥90% new
  cards citing, decisions acted ≥3/wk — 14-day clock from 09-05.
- Kill-switch: if cite-gate can't hold after 3 batch runs, the wave reading
  dies and the card says so.

*Charter filed by the zcode seat, 09-05, under operator grant. Ownership is a
duty: the desk answers for every gate left yellow.*
