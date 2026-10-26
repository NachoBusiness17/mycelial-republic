# V5_PARITY — rule parity harness v0: GDScript mirror vs Python server engine, MEASURED

2026-09-30 · seat: zcode (pain_replication cwd) · ownership: `tools/rule_parity.py`,
`roblox_to_godot/tests/rule_parity_runner.gd`, `tests/test_rule_parity.py`, this receipt.
No commit (operator order). Artifacts: `tools/rule_parity_out/` (untracked).

## Mission (the lensing's C3 core finding)

mag/water_graph.py (the authoritative Python engine behind server/world.py) and
roblox_to_godot/systems/water_graph.gd (the offline client mirror) were WRITTEN to
agree but had never been compared. A silent divergence would sit directly under the
product's core differentiator — deterministic integer water physics, same laws on
both sides of the wire — invisible to every instrument. This harness makes the
comparison mechanical. Honest result either way: parity holds = differentiator
proven; first divergence = the top engineering item.

## Verdict (the <=100-word report)

PARITY BROKEN. First divergence: seq_018 (mountain family — the exact SHIPPING
board from server/world.py build_mountain_graph) tick 5.
hash_py `6f8676f7b46a1088cc2c65d10d70f7b70e5c511d16241740f2af667cfd3670ff`
hash_gd `bec1b88f402d547bcacb7f99ec55dd15529ed66338bda957b906510c06031a6a`.
GDScript double-spends spring volume (0 vs -1), manufactures water (terrace 1 vs 2).
29/100 sequences diverge; legality verdicts and the fracture law held everywhere
the states still agreed. Root cause named below. This is the top engineering item.

## The harness (v0)

- `tools/rule_parity.py` — one CLI, four verbs: `gen` / `python` / `godot` /
  `compare` (and `all`). Canonical JSON schema `rule_parity.v1`: board spec +
  per-tick action frames (staged verbs with sids, validated at receipt in
  arrival order, applied at tick start, physics after — server/world.py
  MountainWorld law, transplanted verbatim into HarnessWorld; faithfulness
  pinned by test: per-tick graph hashes EQUAL MountainWorld's on the same frames,
  so any reported divergence is engine-real, never shim artifact).
- State hash per tick = sha256 over canonical text: tick, then nodes then pipes
  sorted by name, fixed field order, booleans as 0/1 — identical bytes hashed by
  Python hashlib and GDScript `String.sha256_text()`. Integer law: the engine is
  all-int, so the hash is well-defined. Hash FIELDS include volume, steam, open,
  primed, stress, fractured — every mutable the laws touch.
- `roblox_to_godot/tests/rule_parity_runner.gd` — headless SceneTree runner
  (`tools/godot/Godot_v4.3-stable_win64.exe --headless --path roblox_to_godot
  --script res://tests/rule_parity_runner.gd -- <in> <out>`), consumes the SAME
  JSON, replays through systems/water_graph.gd AS-IS (measures, never patches),
  emits the same JSONL rows.
- Input families: mountain (the shipping board, imported byte-truth from
server/world.py) · gated_siblings (the LW5 seam) · economy (waste/cold/siphon
  recovery) · fracture_loop (boil 1/tick -> condense -> sustained full bore ->
  AC2 burst inside the [200,400]+1 window, 460 ticks) · random boards. Actions
  mix legal boil/valve with illegal probes (ghost sid / verb / target) so the
  legality engine is compared too.

## Run (N=100, seed 20260930, 120 ticks/board, 460 on loops = 14,040 tick frames)

```
.venv/Scripts/python.exe tools/rule_parity.py all --seed 20260930 --n 100 --ticks 120
parity: False  (rows py=14040 gd=14040)
  economy:         24 seqs, diverged  7, first divergent tick 1
  fracture_loop:    6 seqs, diverged  0, first divergent tick None   <- HELD
  gated_siblings:  24 seqs, diverged 19, first divergent tick 1
  mountain:        20 seqs, diverged  1, first divergent tick 5      <- first overall
  random:          26 seqs, diverged  2, first divergent tick 1
FIRST DIVERGENCE: seq_018 (mountain) tick 5 kind=state_hash
  nodes.spring.volume: py=0 gd=-1
  nodes.terrace.volume: py=1 gd=2
  pipes.p_bypass.primed: py=False gd=True
  pipes.p_bypass.stress: py=1 gd=2
```

3,469/14,040 tick rows diverge; 71/100 sequences hold full parity. A second,
independent corpus (seed 7, mountain-only smoke) hit the same board seam at its
seq_001 tick 5 — not seed luck.

## Root cause — the LW5 probe-time reserve never crossed languages

Python's LW5 fix (2026-09-29, "NEG-VOLUME LAW", mag/water_graph.py lines 192-197):
a pipe probing INTO a gated junction RESERVES its flow at probe time
(`src.volume -= flow` before the gate verdict), so a sibling pipe from the same
source cannot re-spend the same volume.

water_graph.gd has no such reserve — its own gated-branch comment (lines 208-215)
says "No probe-time reserve here: this mirror decrements the source at GATE phase
(its LW5 shape)" — and decrements at lines 230/244 instead. The two files disagree
about what LW5's fix WAS. Consequence, tick 5 of seq_018 (both sides identical
through tick 4: spring=1, p_bypass primed+open):

- Python: p_spring probes flow 1 -> spring reserved 1->0; p_bypass (later in
  insertion order) finds intake dry -> siphon BREAKS, moves nothing. Final:
  spring=0, terrace=1, primed=False.
- GDScript: p_spring probes flow 1, no reserve; p_bypass sees spring=1 still
  there -> moves 1 (spring->0, terrace->2, stress->2); THEN the gate phase
  decrements spring again: 0 -> -1. Final: spring=-1, terrace=2, primed=True.

GDScript manufactured one unit of water and drove a node negative — precisely the
double-count Python's law names ("a sibling pipe from the SAME source re-spends
it"). On the shipping Mountain board it needs the bypass siphon OPEN (valve verb)
while the main artery probes a low spring: 1 in 20 random 120-tick action
streams. Boards with two gated inlets from one source hit it at tick 1 (19/24).
The economy and random families diverge through the same seam.

## What held (the differentiator is not lost)

- fracture_loop 6/6 sequences, 2,760 ticks INCLUDING real bursts: every loop
  burst the SAME pipe on both sides (six different name-hash thresholds,
  200+djb2(name)%201) at the same tick with identical hashes through the spray.
  AC2/B1 fracture law + the cross-language djb2 name_hash + spray targeting have
  byte parity under load.
- mountain 19/20 sequences held full 120-tick parity (the seam needs the rare
  bypass-open + low-spring interleaving).
- Legality verdicts (UNKNOWN_SID / UNKNOWN_VERB / UNKNOWN_TARGET / DRY_POOL)
  agreed on every tick where the states still agreed. All 29 verdict-divergent
  rows (first: seq_020 tick 14, py reject:DRY_POOL vs gd ack) occur in sequences
  whose hashes ALREADY diverged at an earlier tick: DRY_POOL reads node.volume,
  and GDScript's phantom volumes make dry pools look wet. The legality tables
  are faithful; the verdict splits are downstream of the physics split.

## The fix (next engineering item, NOT applied — this task measures)

Port the probe-time reserve into water_graph.gd's gated-inlet branch: reserve
`src.volume -= flow` at probe time (with the B1 probe-time fracture already
correct there), drop the gate-phase `nodes[entry.src].volume -= entry.flow`
decrements (keep the `node.volume += flow` commits), and fix the mirror comment
that mislabels its shape as "its LW5 shape". Then rerun
`tools/rule_parity.py all` — the harness is the regression gate. Godot-side
verification of a negative spring or any (seq, tick) hash mismatch closes this.

## Tests (focused run; instrument and scope named — not the full-suite census)

`​.venv/Scripts/python.exe -m pytest tests/test_rule_parity.py -q` ->
11 passed. Pins: gen determinism per seed, family-mix shape, canonical-state
golden text, comparator first-divergence/verdict/missing-row laws, the
MountainWorld faithfulness cross-check, and an end-to-end both-engines run whose
verdict is self-checked against direct row equality (the verdict itself is the
measurement and lives in this receipt, not the test).

## Rerun

```
.venv/Scripts/python.exe tools/rule_parity.py all --seed 20260930 --n 100 --ticks 120
# exit 0 = parity, exit 1 = divergence (report: tools/rule_parity_out/parity_report.json)
```
