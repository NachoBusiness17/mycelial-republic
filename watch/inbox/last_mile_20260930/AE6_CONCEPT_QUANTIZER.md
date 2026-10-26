# AE6 — NCP concepts vs the estate's percolator/quantizer (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Files read: mag/percolator.py, memory/corpus/quantized_thought/compile_report.json, memory/percolator/explore.jsonl, memory/percolator/invariants.json, tools/ldt_train.py, AC10_RL_REWARD.md, docs/report_v1/sources/receipts/0812.4360.md.

**(1) Kind of object.** Different species, same ecological niche. NCP's concepts are *learned discrete latents* (gradient-trained codebook over hidden states). The estate's are *extracted symbolic summaries*: `mag/percolator.py` classifies sentences deterministically ($0, stdlib), hashes signal text to a `canonical` hex, and the "concept" is the human-readable invariant string itself. The quantizer (`memory/corpus/quantized_thought/`, compile_report.json v0.4: 401 in -> 374 packed as 24 frontier / 12 flash / 338 local) is curation, not learning. But both yield a small discrete vocabulary over which next-symbol prediction is well-defined.

**(2) The prediction.** A next-CONCEPT predictor over the percolator stream yields: (a) queue scheduling — `memory/percolator/explore.jsonl` holds 1,902 rows, most `status: open`; (b) lane choosing — AC10's v0 lane-chooser (`watch/inbox/last_mile_20260930/AC10_RL_REWARD.md`) is currently a hand formula; a learned predictor makes it empirical.

**(3) Wiring.** Z13 already built the shape: `tools/ldt_train.py` numpy MLP, 0.8545 val accuracy, 15s, $0. Swap inputs from token renders to (source, domain, canonical, hour) history; output softmax over next canonical/lane. That is AC10 made concrete.

**(4) Data today.** YES: explore.jsonl's (ts, source, domain, canonical, lane) tuples; `invariants.json` (599 post-Z15 generations, counts now decay-honest: top 232,214 -> 27); the 374 quantized entries. Sequence order, not counts, is the training signal. Schmidhuber anchor confirmed banked: `docs/report_v1/sources/receipts/0812.4360.md`.

## The build implied (next wave candidate)

AF-candidate: `tools/concept_predictor.py` — ldt_train shape (numpy MLP, minutes, $0) over explore.jsonl sequences, target = next (canonical, lane); eval = holdout next-item accuracy vs the frequency baseline; if it beats baseline, wire it as AC10's chooser empirical core. Falsifier: it can't beat the frequency baseline on held-out sequences.
