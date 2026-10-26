# DOGFOOD LENS: THE INTERACTION THESIS (organ map + the filed-but-never-wired seam)

Lens: dogfood / organ mapper. Jacket: the finding filed but never wired. Topic: the
interaction thesis (operator ask 2026-10-10 "ractor interaction?"), MIMESIS realistic
counterparts, and whether realistic-counterpart training is the estate's highest-leverage
next organ. Moment: 2026-10-10 ~05:30-06:10Z (01:30-02:10 EDT). Every claim below was
checked this sitting by a named command or file read; anything unverified is OWED. No
em-dashes. Paper facts (MIMESIS 2610.09484, Clark Lyapunov 2610.12426, Open Env Arena,
Living Weights) are cited from the ask brief only; I fetched no arXiv page this sitting.

Organ map used: context pack = AGENTS.md + rib_boot digest (feeds every seat); percolator =
memory/percolator/invariants.json (behavioral invariants with counts + decay, read this
sitting); gala = paid dispatch (tools/hermes_burn.py per prior dogfood F2/F3); MCP bridge =
tools/gps_mcp (config.gstd.json landed 10-09, commit 700625aa0); attention market =
memory/attention.md + tools/attention_dam.py (classifier + one-pass archive, header read);
librarian = catalog/ + corpus FTS + memory/runs tape vaults. The ASTRA spine named in the
ask IS banked bytes: watch/inbox/ASTRA_V4_STATUS.md:5-6 "harness_audit -> curator
(sealed-first) -> validate -> QLoRA SFT -> RS-DPO+HyPO -> GRPO+ACR/AVSPO -> budget-matched
eval -> canary promotion". Instrument honesty: my FIRST ASTRA census (findstr /s over
watch\inbox\*.md) returned zero hits and was WRONG (broken findstr pattern on this host);
a grep -rln re-census found ASTRA across 30+ receipts. The quantifier law bit me once this
sitting; every absence claim below names its working instrument.

## F1. The ASTRA training spine is filed, named critical-path, and never dispatched: 23 days of empty return directory. CONVERGENT. (gala + curator organs)

- watch/inbox/ASTRA_V4_STATUS.md:1 "spec converged, awaiting dispatch (2026-09-17->18)";
  :32-38 next action = dispatch the v4 brief to the astra seat, which returns the curator
  script, QLoRA recipe, eval harness, bias-report schema.
- watch/inbox/ASTRA_REVIVE_VERDICT_20260926.md:15 independently calls it "the critical
  path to Oct 27" (Rocinante = 4x Mac Studio substrate, lands Oct 27 per that receipt's
  prereg triggers). Two windows, one verdict = duplication is emphasis.
- My check: `ls -la watch/inbox/astra_v4/` = directory created Sep 17 22:41, ZERO files,
  read empty at 2026-10-10 00:32 mtime-of-parent. The dispatch never returned.
- The off-disk solve for the 6GB hardware also sits unrun: memory/training/vast_package/
  README.md:2-5 "gemma-2-2b-it, QLoRA 4-bit, LoRA r=16, 150 examples, est. $0.12", run
  block operator-gated ("requires vastai CLI"). Scoped absence check: grep -i vast over
  watch/inbox filenames + the 3 vastai-mentioning docs (CODEX_TASK_005_20260901.md is a
  DIFFERENT vast thing, the RTX 5090 vLLM serve task, itself audit-typed UNPROVEN at
  :3-4; DAY_SYNTHESIS_20260929.md:19 and MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md:199 mention
  vastai only as venv-fragility and a cp1252 syntax warning) -> no receipt of a completed
  training run anywhere I checked.
- Interaction bearing: MIMESIS lands on this spine's GRPO stage AS THE ENVIRONMENT, and
  the spine names no environment organ (see F5). The judgment to un-stick the spine rides
  the funded tier by standing law: memory/rib/RIB_DRIVING_LADDER_20260928.md:7-20 (ONLY
  Hermes Nous primes funded, $180, glm-5.3-prime / qwen3.8-max-prime; "This is what the
  $180 is FOR").

Falsifier: any file inside watch/inbox/astra_v4/, or a receipt naming a returned curator
script / QLoRA recipe, or a vast run receipt (instance created, weights landed via
promote). Move (one sitting, ~45 min): dispatch the v4 brief through the Hermes carrier
(tools/hermes_burn.py) to glm-5.3-prime with one amendment: the return must include the
GRPO ENVIRONMENT contract (the counterpart deck of F3), not just data curation. The brief
is already paste-ready per ASTRA_V4_STATUS.md:32-36.

## F2. The operator tapes are the one corpus the training event stream does not emit: 3 operator rows in 874,385 events. (context pack -> capture organ seam)

- Instrument + scope: `wc -l memory/training/events.jsonl` = 874,385 rows (append-live;
  tail rows I read are stamped 2026-10-10T05:13:56Z). Full untruncated pattern census via
  `grep -o '"pattern": "[a-z_0-9]*"' | sort | uniq -c | sort -rn` at my moment:
  autorun_cycle 55,052 / fkb_failure 8,342 / spider_signal 5,732 / task_lifecycle 958 /
  arena_match 161 ... operator_behavior 2, operator_priority_yield 1, steer_outcome 1,
  promote_gate 5. The human side of the interaction is 3 rows in 874k.
- The spec's own hook table wires machine loops only: docs/ref/MAG_TRAINING_DATA_SPEC.md
  hook table (:240-249 in my outline read) lists conductor, governor_autorun,
  orchestrator, compass, failure_kb, spider. No operator-session hook exists.
- The tapes DO exist off-stream: memory/zknot/ holds 27 session cards (ls count), the
  top 3 interactive windows alone carry 117 + 55 + 98 human prompts (memory/zknot/
  LATEST.md:13, :96, :177); memory/training/refined_training_data.jsonl = 1,157 rows of
  real instruction/output pairs (wc -l; row 1 sampled: source copilot_transcript,
  instruction "please", output = the seat's actual response, quality_score 0.6); the
  corrections corpus carries contrast-shaped pairs by design (.agents/skills/
  operator-corrections/SKILL.md:86-89 "extracted from failure traces with contrast (wrong
  move vs corrected move, the MAX_DISTILL shape)"), which is preference-pair shape, the
  MIMESIS coaching step's data genus.
- Interaction bearing: MIMESIS's premise is training on REAL human conversations. The
  estate's real-conversation count inside its training spine is ~3. Before any SFT /
  preference / GRPO argument, the falsifiable first probe is CAPTURE-side.

Falsifier: a fresh full census reading materially more operator-facing rows (claim is
moment-scoped to my 2026-10-10 ~05:30Z grep over the whole file; the file grows). Move
(one sitting, ~60 min): tools/zknot_emit_training.py: re-run the deterministic zknot
parse (tools/zknot.py already reads the session JSONLs) over the 27 cards, emit one
mag_training_event pattern=operator_turn per human prompt with session join keys, append
through the sanctioned writer, then re-census: operator rows should go 3 -> 1,500+.

## F3. The MAG-native counterpart deck already exists, boot-warmed every seat, and has never once been simulated. The sovereign mirror is filed, not wired. (rib boot / context pack + arena organs)

- memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:3-6, purpose verbatim: "the whole purpose of
  the sovereign mirror was to copy my thinking and decision making with you to run
  autonomously ... the seat recognizes the SHAPE and runs the warmed lane without
  re-teaching." 9 input-shape cards follow (LINK-DROP, GO, CORRECTION, TERSE-EVAL, ...).
- The deck was extended 10-04: tools/behavior_cards_x.py mines the operator's X posts
  into cards with regex families + local ollama judgment; run summary
  work/behavior_cards_20261004/summary.json = 4,233 posts scanned, 25 cards kept, 114
  posts cited; banked at memory/rib/RIB_BEHAVIOR_CARDS_X_20261004.jsonl (96,065 bytes,
  ls -la). :17-18 and :396 of the tool: every card ships a train_pair sidecar
  {"situation": shape, "decision_pattern": claim, ...}.
- Consumer census: `grep -rln "behavior_card|RIB_BEHAVIOR" mag/ tools/ --include=*.py` =
  mag/rib_boot.py (boot digest) + the miner itself. NOTHING plays the deck as a
  counterpart. The CORRECTION card is exactly the non-compliance MIMESIS says
  cooperative simulators lack: "STOP running -> root-cause -> mint as LAW ... Never just
  apologize" (RIB_BEHAVIOR_CARDS_20260928.md CARD CORRECTION block).
- The falsifiable first probe, $0, no weights touched (the NEW MONEY frame, suppression
  card law): hardware fact first, the RX 5600 XT 6GB is UNWIRED, Vulkan path only
  "identified" (watch/inbox/ASTRA_ASK_THE_LOOP_20260911.md:18), so local runs are CPU
  ollama on 64GB DDR4. Condition gemma:2b (the standing janitor) with the 34-card deck
  as system prompt; play it against 20 real estate outputs (10 green / 10 vacuous from
  recent verdict streams); measure pushback rate (CORRECTION / TERSE-EVAL moves) vs a
  compliant-baseline system prompt on the same set.

Falsifier: card-conditioned and baseline arms produce indistinguishable pushback rates
(or the 2b janitor degenerates to yes-man in both arms), which kills prompt-conditioned
counterparts and pushes the probe up to the funded prime as simulator. Move (one
sitting, ~90 min): tools/counterpart_probe.py on the arena harness. mag/agent_arena.py
is seat-vs-seat chess (docstring :1-2; SUPPORTED_GAMES frozenset {"chess"} :18-19) and
mag/arena_learning.py already records match outcomes into profiles + league
(memory/training/arena_profiles.jsonl, arena_league.json exist, ls); add the counterpart
as a game class or run standalone and emit the arena_match row (pattern already live,
161 events).

## F4. Same-window receipts independently re-derived the non-compliant-counterpart mechanism. CONVERGENT, cross-run. (gala lanes + attention market organs)

- watch/inbox/suppression_topology_20261009/STEAL_CARD.md:21 lists "over-compliance
  after one pushback" as a suppression marker (probe 2) -> that IS the MIMESIS
  too-cooperative-simulator observation, derived from Gray Swan prior art (ART / D-REX /
  injection-competition rows, :11-14), NOT from MIMESIS. Independent derivation, one day
  apart.
- The same card :22 pre-registers a two-arm counterpart experiment with its falsifier
  attached: "children that stall get a receipt-injection arm vs a plain-retry arm;
  measure turns-to-recovery. Falsifier: receipt injection does not beat plain retry ...
  the joy-lock twin retires to aphorism."
- The environments-not-models insight (Open Env Arena, per the ask brief) also has a
  live estate prior: mag/arena_learning.py:1-4 "competitive seat probes -> profiles ->
  nervous/switchboard routing" ranks SEATS through GAMES, which is the same inversion.

Falsifier: if the MIMESIS transfer claim fails at estate scale (an agent tuned against
the card-deck counterpart shows no gain against a DIFFERENT counterpart: salon chairs,
or a funded-prime adversary), counterpart realism does not generalize downward and the
organ demotes to eval garnish. Move (one sitting, ~30 min on top of F3): merge the two
probe designs; run the F3 counterpart with the suppression card's receipt-injection vs
plain-retry arms on the vacuous half of the output set, one receipt, both cards cite
each other.

## F5. Counterpart realism is the unnamed ENVIRONMENT stage between eval and GRPO, and the estate's compute shape fixes the probe ladder. (whole-spine organ + MCP bridge landing zone)

- ASTRA_V4_STATUS.md:5-6 names eight stages, zero environments. The estate's own
  transfer gate greps "RL env" as a claim marker in transfer cards
  (mag/transfer_gate.py:208 _RL_MARKERS), flagging env claims in OTHERS' cards while the
  spine itself carries none.
- Compute facts (all read this sitting): RX 5600 XT 6GB unwired + Ryzen 7 3800XT + 64GB
  DDR4 (ASTRA_ASK_THE_LOOP_20260911.md:18) -> no local 9B anything; $0.12 vast QLoRA
  path packaged and unrun (F1); an operator-held RTX 5090 32GB vast instance was tasked
  09-01 and is audit-typed UNPROVEN (watch/inbox/CODEX_TASK_005_20260901.md:3-4); funded
  judgment = Nous primes + grok-4.7 (RIB_DRIVING_LADDER_20260928.md:7-20 + AGENTS.md
  driving ladder line). This fixes the ladder: (1) $0 prompt-conditioned local
  counterpart (F3), (2) $0.12-0.5 vast QLoRA of gemma-2-2b on the 1,157 refined rows +
  F2's operator_turn rows (the SFT stage, 150-example package already shaped for
  exactly this), (3) funded-prime as the HELD-OUT UNSEEN simulator for the transfer
  test (the MIMESIS nine-simulator claim mapped to estate counterparts: gemma:2b deck,
  salon chairs, grok-4.7) -> that result is the preference/GRPO gate decision, priced
  in single-digit dollars of prime budget.
- Where it lands on the spine: BETWEEN budget-matched eval and GRPO, as the environment
  contract; the eventual trained counterpart's runtime seat is the MCP bridge router
  (tools/gps_mcp, where the 10-09 garden routing landed), because a counterpart that
  judges outputs is a routing signal.

Falsifiers both ways: (a) the estate's tapes are ONE operator in ONE register; if a
counterpart trained on them fails against any other interlocutor (the transfer test's
null arm), the organ overfits to his voice and stays an eval garnish; (b) if the $0
rung (F3) already discriminates green vs vacuous outputs, the expensive SFT rung is
unnecessary and the organ stays context-side per the NEW MONEY law. Move (one sitting,
~30 min): write the counterpart organ spec as an ASTRA v4 amendment (inputs = estate
outputs; moves = the 34 cards; termination = CORRECTION or GO; reward = pushback
calibrated against verdict class) and attach it to the F1 dispatch.

## Is realistic-counterpart training the highest-leverage next organ? The dogfood verdict

Not yet, and the estate's own bytes say why: the highest-leverage next organ is the
CAPTURE + DISPATCH pair (F2 emitter + F1 spine dispatch), because counterpart training
without operator_turn rows in the event stream trains on 3 rows, and the spine that
would consume them has sat awaiting dispatch for 23 days with its return directory
empty. The counterpart deck (F3) is the cheapest honest probe in the thesis and should
run first anyway because it prices the claim at $0. Answer to the ride: counterpart
realism generalizes ONLY if the estate's transfer test passes (F5 ladder rung 3);
cost floor is $0 (prompt-conditioned) and ceiling is single-digit dollars (vast QLoRA +
prime judgment); a MAG-native user simulator looks like the 34-card deck + operator_turn
events + the CORRECTION card's pushback policy, not like a 9B model; on the ASTRA spine
it lands as the environment stage between eval and GRPO.

## Blind spots (honest)

- Sibling lenses' write-ups: none banked in this topic dir at my listing moment; no
  cross-lens convergence check beyond the suppression card.
- Workflow introspection unavailable in this session (ListWorkflowRuns returned a
  capability-gap error), so the spawning engine script and its registry row were not
  read.
- The papers themselves (MIMESIS 2610.09484, Clark 2610.12426, Open Env Arena, Living
  Weights) were NOT fetched; every paper fact rides the ask brief. OWED: arXiv verify.
- The raw .zcode transcripts (the actual tape bytes, ~335GB per the 10-08 disk audit
  commit cd118ed70) were not opened; tape-scale evidence rides zknot's distilled cards
  and the 1,157-row refined sample (of which I read 2 rows).
- The counterpart probe is DESIGNED, not executed: no ollama call, no model run, no
  prompt was fired this sitting.
- sovereign_training_data.jsonl (149 rows) sampled as mostly placeholder "System event:
  unknown" rows; its full quality was not audited.
- events.jsonl is append-live; every census is moment-scoped and named as such.
- Salon tapes located (memory/runs/salon1 rounds 1-3 + slices U1-U6, salon_20260827
  COMBINED.md) but not read; they are claimed as a transfer-test counterpart on shape
  alone.
- My first ASTRA findstr census was an instrument failure (returned zero on a populated
  corpus); reported here so the next lens does not trust findstr /s patterns on this
  host.
