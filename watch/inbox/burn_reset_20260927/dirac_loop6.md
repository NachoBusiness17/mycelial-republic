# dirac loop 6 closed: water proof anchored (burn reset evening, 2026-09-27)

Lane 8/10 of BURN_RESET_20260927_EVENING. Loop: `organ:water_computer->organ:manifest`
(`proof`), invariant `d7d325817e116ccf4076ad6ff5d6934912cbe14abb00e25c25bdb361bee4203c`.
Gap-reader verdict (watch/inbox/lens_20260927/DIRAC_GAPS_READ.md): one-wire build, the
anchor mechanism already landed. Status at lane start: closed_solved=1, open_gaps=5.

## What was wired (caller-side only; manifest.py untouched)

`mag/water_computer.py`, new proof section after `_save_graph`:

- `proof_payload(camp)`: the REAL artifact, claim "the water computer computed its route
  to OUT by gravity" + evidence = the live `water:graph` spec and the final node volumes
  (graph mode only; legacy 3-tank keep has no network, returns None honestly).
- `anchor_proof(camp, force=False)`: `manifest.anchor()` takes no payload, so the CALLER
  adapts: the proof's canonical sha256 is pinned through the same `verkle_knot.append`
  writer manifest.anchor() uses, as the chain leaf's `dossier_commit` (session
  `water_computer`, one leaf amended not appended, the manifest/team_knot dedupe), then
  `manifest.anchor()` itself is refreshed so the bones stay a chain fact on the same
  chain. Record (full payload + leaf + root + manifest hash) lands at
  `state/water_proof_anchor.json` (state/ is gitignored, runtime truth). Deduped once
  per campaign via the `water:anchored` flag (the proof is the win-time snapshot; later
  ticks are the same win). Chain failures are reported in the returned dict and in the
  play events, never hidden, and never break play.
- Win hook: `_graph_tick` calls `anchor_proof(camp)` right after the honest graph-mode
  gravity win (`won(camp)`: heights earned via flowed, never bucketed). Events surface
  "Proof anchored: <hash16> (leaf <leaf12>)" or an honest "Proof NOT anchored: <why>".
- Explicit call: `python -m mag.water_computer proof` (CLI verb added next to `glass`).

## Live proof (bytes, not claims)

Driven by the suite's own honest win path (`test_graph_flow_wins_honestly`): volumes at
win time out=2, source=4, junction=0, reservoir=2, waste=0 (6 walked out of source
through the XOR by gravity). proof_hash `5b8097dcce342408`, chain leaf `2ccea18ff768`,
chain_ok true (chain verified, 8056 rows + this amended leaf), manifest_hash
`111fc776cb9739f3` re-anchored in the same act.

## Tests

- tests/test_water_computer.py + test_water_graph.py + test_water_graph_campaign.py:
  22 passed in 37.92s (7 + 7 + 8). No test touched; the graph-mode win test now also
  exercises the anchor (one amended chain leaf per run, bounded by session dedupe).

## Bank row

`.venv/Scripts/python.exe -m mag.dirac_loop bank --edge "organ:water_computer->organ:manifest" --receipt "water proof wired: anchor_proof() in mag/water_computer.py fires on the graph-mode gravity win inside _graph_tick, plus explicit verb python -m mag.water_computer proof; pins sha256 of claim+graph_spec+final_volumes as chain leaf dossier_commit via verkle_knot.append (session water_computer, amended not spammed) and refreshes manifest.anchor(); record at state/water_proof_anchor.json; water suite 22/22 green (test_water_computer.py 7, test_water_graph.py 7, test_water_graph_campaign.py 8); live win proof 5b8097dcce342408 with out=2"`
-> ok, banked at 2026-09-27T23:18:15Z, invariant d7d32581... recorded in
watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl (4th row; rows 2-3 are lane 9's
admission<->openclaw pair, landed in the shared ledger before my commit).

## New scan verdict

`python -m mag.dirac_loop scan` (operational): betti1=8, n_loops=6, **closed_solved=4,
open_gaps=2**. CLOSED: verkle_knot->manifest (loop 3), context_admission<->openclaw
(loops 4+5, lane 9), water_computer->manifest (loop 6, this lane). Remaining open:
context_pack->swarm_surface (loop 1), context_checkpoint->context_pack (loop 2).

Laws held: trust bytes (all numbers above from live runs), no fabrication (only the real
win artifact anchored, chain-gated), one writer per file (only mag/water_computer.py
edited code-wise; the ledger is the sanctioned shared append surface), no em-dash in
landed text.
