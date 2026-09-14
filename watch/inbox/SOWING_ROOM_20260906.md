# SOWING_ROOM_20260906 — THE SOWING ROOM (salon unified-fold C3 minimal build)

**Builder:** fable (zcode seat) · **2026-09-06** · **$0, no network, no daemons** · one self-contained file:
`dashboard/static/conservation_room.html` — "THE SOWING ROOM — a fable of the conservation clause".
House dark style (#070d0c / #7cf5ff / #e8c96a), error-banner fixture (arrakis pattern), FNV-1a 32 chain.
Verify: node --check PASS (both blocks) · curl 200 on :8765 · recorded repair simulated in node → field 7/7.
Nav entry reported NOT wired: ["/static/conservation_room.html", "The Sowing Room"].

## The mapping (mancala conservation clause = refeed guard)
Board: 6 pits + THE FIELD (cell 6, the record — seeds that leave your hand into the ground) + YOUR STORE
(cell 7, self-feed). Sow = lift a pit's whole hand, drop one-by-one rightward. THE LAW (one line):
**a sow never lands in its own store** — a hand that overshoots the field reads REFUSED
(red flash on the store + the guard's own numbers: "122,000,000 in / 500,000 out — the session that fed
itself"). Refusal changes nothing (measure-or-no-move).INITIAL board [1,2,1,1,1,1,0] (7 seeds, 6 pits),
RECORDED repair = [0,1,5,4,2,5,3,5,4,5] (10 moves, BFS-derived canonical solution, embedded as data).
The natural trap: skip harvesting pit 5 and it jams at 2 — permanently REFUSED. Seed stamp = FNV-1a of
the room's own data hash (initial + recorded repair).

## Kill condition 1 — RECORD-EXIT = STORY-EXIT (openrouter)
Two doors at every pit:
- **THE TELLING (narrative door):** subtracts one seed from the pit (visibly), appends a fable line
  (12-line rotation: "Glow is not a seed"), counter reads "telling: n spent — record: unchanged".
  Hash strip never moves. Narrated seeds LEAVE the system — the field can never reach 7 again.
- **THE SOWING (record door):** the actual legal move. If it matches the next recorded move, the chain
  link appends (visible hash strip, seed-rooted, per-link hash = FNV(prev|move|state)). A legal move off
  the recorded sequence = CHAIN FORKS (amber banner, re-sow offered) — state is deterministic, divergence
  is permanent, and the room says so.
- **Endings fire when the pits empty:** field 7/7 + record 10/10 = "THE FABLE CLOSES" (chain verified).
  Anything else displays **"a coherent story that never happened"** with the shortfall itemized
  (seeds spent on the telling / forked link / alternate-order repair with chain short of 10/10).
  The story-exit done RIGHT is literally the record-exit: one board state, two ways to reach it.

## Kill condition 2 — RESTATEMENT GATE (deepseek-pro)
Fires ONLY on the true ending. The player must (1) restate the law in their own words, (2) answer the
novel scenario: "a pit learns to duplicate tokens — it can sow a copy of each seed without spending its
own count. Legal? Why?" The room does NOT judge: answers are sealed verbatim to localStorage
(`sowing_room_restatement`) + rendered as a copy-paste ledger block (room, LAW-061 stamp, seed, chain tip,
record/telling counts, ts). **How the seat judges (vision pass):** tri-state the law restatement against
the one-line law (conservation + never-land-in-own-store); for the duplication scenario, the DEFENSIBLE
answer is ILLEGAL-with-reasoning (duplicating breaks conservation — the room counts what leaves the hand;
a copy is a seed from nowhere = self-minting, the store's cousin) — but a NO with conservation reasoning
or even a reasoned YES that names the tension both teach; REFUSAL-TO-ANSWER or pure plot-summary = the
story-layer entertained without teaching → C3 falsifier hit.

## Footer
LAW-061 validate-the-field (which-lie stamp) · seed from data hash · "the story-exit and the record-exit
are the same door or the story is a lie."
