# deep-operator-model: the OPERATOR MODEL: stop running shit, start remembering

**Item:** deep-operator-model · **Banked:** 2026-09-28 · **Seat:** flash50 deep gopher
**Operator order under design:** "stop running shit and start remembering."

## 0. Reading of the order

The complaint is not memory scarcity. The estate holds 215,576 rows in
`logs/behavioral_events.jsonl`, 213,259 rows in `memory/decisions_log.jsonl`
(both counted this session via `wc -l`), a failure index whose top signature
`run_shell:c73866f2f1b5` carries 25,100 events, and a Verkle chain with 8,250
leaves (live `build_context_pack` tip read, 2026-09-28). What is missing is the
**model**: a compressed, structured, loadable, current representation of WHO THE
OPERATOR IS: preferences, decision patterns, correction history, values, such
that any fresh seat boots already knowing him instead of re-deriving him from
raw heat or serving him fifty-day-old law. "Stop running shit" = stop paying
tokens rediscovering the principal every seat; "start remembering" = compile
him once, load him always, amend him by protocol.

The estate itself already diagnosed this and registered it OWED:
`memory/research_polished/memory_engram.md:23` (the operator-input seam
taxonomy absorption) demands "(b) learn-back ... into
`memory/improve/operator_model.jsonl` (grok-style memory-of-user, local)" and
records the verified absence: "`operator_model.jsonl` absent. Register: OWED."
I re-verified this session: `os.path.isfile('memory/improve/operator_model.jsonl')`
returns False. And `memory/research_packs/20260809T020632Z_reliable-control-deterministic-layer.answer.remote.md:25,27`
names it layer 1 of the deterministic control stack: "The persistent operator
model translates operator preferences into deterministic rules so the system
doesn't re-negotiate through the model on every turn." This item is that owed
build, designed.

## 1. What already exists (the inventory, all read this session)

The operator's representation is currently smeared across ten surfaces with no
unifying schema, no shared query seam, and divergent hygiene:

| Surface | Content | State verified live |
|---|---|---|
| `.agents/skills/operator-corrections/SKILL.md` | 20 compiled laws with teeth, dated, operator-voiced | Richest correction store; human-curated; loaded only if the seat thinks to load the skill |
| `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md` | 10 input-shape cards (LINK-DROP, GO, CORRECTION, ...) | v1, explicitly "appended as transcript miners dig" |
| `memory/operator_directives.md` | autonomy contract, L0c layer | Loads every pack at `mag/context_pack.py:621` (2,800-char clip) |
| `memory/working/OPERATOR_CONTINUITY.md` | "cold seat must use this" card | **STALE 53 days** ("As-of: 2026-08-06"), loaded anyway at `mag/context_pack.py:762-767` with no staleness guard |
| `memory/corpus/quantized_thought/instructions_flash.jsonl` | 12 flash laws riding every boot | 4.1h fresh (`tools/thought_quantizer.py --check` exit 0) **but polluted** (see 2.1) |
| `memory/improve/daily/*-behavioral.md` | daily distilled themes | 2026-09-28 leaf mined 200 events (194 `pro_fire`) into 2 vague themes ("Operator-reported seat friction") |
| `memory/facts/behavioral.jsonl` | percolator-era compiled invariants | **No active writer in `mag/`** (repo grep finds only read-side research scripts); polluted with probe junk ("test ping from probe") |
| `logs/behavioral_events.jsonl` + `memory/decisions_log.jsonl` | raw event heat | Massive, unmodelled; `surface_tips` reads only last 60/40 rows (`mag/decision_framework.py:83,97`) |
| `memory/failure_kb/signatures.json` | deduped failure index | Healthy under B2-87 log-is-authoritative law (`mag/failure_kb.py:22-40`) but holds only tool-fail telemetry, not operator corrections |
| `state/mag_preferences.json` | drainer / operator_active toggles | Machine prefs only (`mag/preferences.py:11`) |

Two prior remote research answers (`20260809T012225Z_operator-input-seam-taxonomy`
and `20260809T020632Z_reliable-control-deterministic-layer`) already mapped the
seam taxonomy (advisory/directive/veto authority tiers, latency vs learnability
axes) and prescribed exactly this: a persistent operator model fed by a
learn-back loop. Neither landed. BOOT_4_7.md:12 even calls AGENTS.md "the
operator model", i.e. today the operator model is a hand-edited fence-owner
file drifting row by row.

## 2. Live defects proven this session (why another store is not the answer)

### 2.1 The compiler pollutes law with telemetry
`tools/thought_quantizer.py` compiles `memory/percolator/invariants.json` into
tiered packs (frontier 24 / flash 12 / local 12 defaults, `--flash/--local`
flags at lines 228-229) with weight = recency x shape (lines 82-100). Running
its own classifier on the junk currently in the flash pack:

```
>>> from tools.thought_quantizer import classify
>>> classify("No such file or directory: 'Get-ChildItem'")
('keep', 'imperative')
```

The row survives because `file` is in IMPERATIVE_RE's verb list
(`tools/thought_quantizer.py:39-43`) and the string contains no TELEMETRY_RE
marker (lines 44-47). That junk renders as OBEY-law in every boot pack's L0b
(`mag/context_pack.py:1075-1080`); my live `build_context_pack(mode='plan')`
returned it verbatim among the 12 flash laws. Law channels that carry noise get
discounted by every seat that reads them; the exact failure mode that makes
operators say "stop running shit."

### 2.2 Stale operator state served as current truth
`_quantized_laws` renders a visible debt pointer when packs age past 7 days
(`mag/context_pack.py:376-378`, "STALE ... law hidden until fresh"). The
continuity excerpt has no such guard: `context_pack.py:762-767` reads
OPERATOR_CONTINUITY.md unconditionally; the live pack served its "As-of:
2026-08-06" card as law. Same estate, two hygiene standards, 53 days of drift.

### 2.3 Correction memory is fragmented below the query seam
The estate's canonical false-success correction ("claimed edits but no
mutating tool ran") appears repeatedly in `memory/facts/behavioral.jsonl`
(5 exact `grep -c` hits) but was never logged into failure_kb, so the boot
pack's FKB query returns nothing for it:

```
>>> from mag.failure_kb import surface_hits, lookup, query
>>> surface_hits(goal='write_file claimed edits but no mutating tool ran', limit=3)  # n=0
>>> lookup(None, 'claimed edits but no mutating tool ran')                            # n=0
>>> query('backend reported failure')  # 3 hits, counts 25100/12285/1286
```

The query path works; the operator's corrections simply live in a different
store than the query reads. A fresh seat that never loaded the
operator-corrections skill has no path to law 6 ("NEVER CLAIM FIRST UNLESS
READ FROM DATA") at decision time.

### 2.4 The voice channel is dark
`_mirror_voice_excerpt` (`mag/context_pack.py:193-241`), the only seam that injects the operator's actual authored voice, is gated behind
`MAG_INJECT_MIRROR_VOICE` (line 195, default off). Live pack: 0 chars. The
estate mines his transcripts (`RIB_BEHAVIOR_CARDS` header names
`x_history_mine`, `oral_history`) but delivers none of it at boot.

## 3. The design: one compiler + one delivery contract, three planes

Not a new memory store. `memory/operator_model/` is a **schema and protocol**
over the stores that exist, in three planes, following the estate's own
memweave doctrine (feed structures, not prose):

### Plane A: LAW (`memory/operator_model/law.jsonl`, append-only, deterministic)
One row per operator law, formalized from the existing rich sources first
(the 20 correction laws, the 10 behavior cards, operator_directives.md; the
compile is mostly transcription, which is why it is cheap and honest):

```json
{"id": "om-007", "class": "prohibition",
 "statement": "Never claim done unless verified against the surface the operator touches.",
 "evidence": [{"src": ".agents/skills/operator-corrections/SKILL.md", "law": 4},
              {"src": "memory/rib/RIB_BEHAVIOR_CARDS_20260928.md", "card": "CORRECTION"}],
 "teeth": "tools/violation_ratchet.py + verify-bytes gates", "class_shape": "imperative-lead",
 "weight": 0.8, "minted": "2026-08-26", "last_corroborated": "2026-09-28",
 "status": "active"}
```

Design decisions, each answering a live defect:
- **Telemetry can never become operator law.** Rows enter via the CORRECTION
  card protocol (`RIB_BEHAVIOR_CARDS_20260928.md:26-33`: STOP -> root-cause ->
  mint as LAW with enforcement in code) or by transcription of the existing
  compiled sources, never by raw event mining. The quantizer keeps its job
  (fleet telemetry), the operator model gets a different intake. This is the
  structural fix for 2.1: two compilers, two corpora, one delivery seam.
- **Append-only, supersede-never-delete**, mirroring the B2-87 law the estate
  already holds for FKB (`mag/failure_kb.py:22-40`): the log is authoritative,
  derived views rebuild, receipts name what changed. Flips write
  `status: superseded, superseded_by: om-NNN`, consistent with the infinity
  rule's "the tide never amends the strata" (SKILL.md law 20).
- **Staleness is visible, never silent**, generalizing the
  `context_pack.py:376-378` pattern to every plane-C field and any law older
  than 30 days without corroboration.
- **Counts are provenance only**; the quantizer already learned this
  ("inflated echo", 232,214 raw -> weight 0.8; `thought_quantizer.py:153-157`).
  An operator law's authority comes from its evidence chain, not from how many
  times it was echoed.

### Plane B: VOICE (retrieval, probabilistic)
The mirror corpus (republic `data/annotated/mirror_train.jsonl`, X history,
oral-history transcripts) stays a separate index queried goal-conditionally at
render time. Flip `_mirror_voice_excerpt` default-on with a hard budget (600
chars as written, `context_pack.py:193`). Voice answers "how would he frame
this," never "what does he want"; want is Plane A's monopoly. The separation
matters: Park et al.'s Generative Agents (2023) retrieve on
recency x importance x relevance and reflect observations into higher-level
inferences; the estate's daily leaf is the reflection step and it is currently
the weak half (200 events -> 2 vague themes, verified above). Reflection
quality, not retrieval, is where the estate's memory work owes.

### Plane C: STATE (`memory/operator_model/state.json`, volatile, receipted)
Funding statement pointer (the driving ladder is the live instance:
`memory/rib/RIB_DRIVING_LADDER_20260928.md`), handshake ledger pointer
(`state/handshakes.jsonl`, SKILL.md law 14), current priorities,
`operator_active` (already in `mag/preferences.py:38-45`). Every field
timestamped; every render shows its age.

## 4. Delivery: ride the A2 frozen prefix

The boot seam already exists and is cache-priced correctly: `freeze_system_prompt`
(`mag/context_pack.py:452-489`) makes the system prompt byte-identical per
session, and the clip ladder protects directives while shedding context first
(`context_pack.py:1261-1268`: "Directive tier survives the ladder"). The
operator model renders as a new L0-OPERATOR block in the frozen prefix,
between the standing objective (lines 1063-1069) and compiled fleet laws
(1075-1080), tiered like MODE_CONFIG already tiers packs: janitor gets the
top-3 laws (~300 chars), plan/full gets the full law plane (~2KB). Because
Plane A changes only via the deliberate correction protocol, it is stable
within a session by construction; it satisfies the A2 byte-identity law
without contortion, and a mid-session correction legitimately refreezes.

## 5. Query protocol (how a seat asks)

Three entry points, one module (`mag/operator_model.py`):
1. **Boot:** `render(tier=...)` -> the L0-OPERATOR block; consumed by
   `build_context_pack` exactly as `directives` is today.
2. **Pre-action gate:** `check(action_text)` -> matching laws + FKB hits for a
   contemplated risky action; this is the operator-corrections skill's
   "pushy on purpose" posture made callable, so seats that never loaded the
   skill still hit the law.
3. **Provenance:** `why(law_id)` -> the evidence chain; answers "why do we do
   X" from receipts, the estate's reflex. Pre-action and provenance calls are
   deterministic local reads ($0, no model), matching the rib-loading law in
   AGENTS.md (boot-order: load ribs -> load state -> act).

## 6. Update protocol (how it remembers)

1. **Capture (same hour):** CORRECTION card fires -> mint law row with
   evidence pointers; funding changes -> Plane C field update. This is the
   learn-back the seam-taxonomy pack prescribed
   (`20260809T012225Z...answer.remote.md:60`).
2. **Corroborate (nightly):** the pile-classifier
   (`mag/state_snapshot.py:36-42`, `capture_summary` rows ->
   `tools/pile_classify.py`) proposes candidate rows from
   behavioral_events/decisions_log diffs; proposals land `status: proposed`.
   Free-lane sensing law applies: proposals are findings, never trusted work.
3. **Promote:** operator GO or two-seat cross-sign (the v4 cross-sign shape
   already used for VOID nominations, per Q-020 receipt practice).
4. **Amend, never rewrite:** supersede with pointer; monthly, stale-by-
   corroboration rows render their debt visibly in the pack. Law 10 ("NO
   SACRED COWS") is the standing amendment license.

## 7. Literature anchors (real, consulted via the estate's own intake doctrine)

- **Constitutional AI (Bai et al. 2022):** a fixed written constitution shapes
  every model instance's behavior without per-turn supervision; the operator
  model is a per-principal, empirically mined constitution. Its known weakness
  (constitutions drift from practice) is exactly what the corroboration
  protocol addresses; the estate's own law 10 is the amendment mechanism.
- **Generative Agents (Park et al. 2023):** memory stream + reflection into
  higher-level inferences; the estate has the stream (215k events) and a weak
  reflection (daily leaves). The operator model formalizes reflection OUTPUT
  as law rows with evidence chains.
- **MemGPT (Packer et al. 2023):** OS-style paging with self-edited core
  memory; the L0-L4 clip ladder (`context_pack.py:1235-1278`) is a
  hand-designed pager; Plane A is the "core memory block" that is always
  resident and edited only through explicit tools (the correction protocol).
- **RLHF reward models / policy distillation:** a reward model is a compressed
  preference function learned from comparisons; law.jsonl is the interpretable
  symbolic counterpart, trading statistical fidelity for auditability; the
  right trade for an estate whose constitution is "trust bytes, not reports."
- **Lessig, Code is Law:** already estate doctrine ("enforcement in code
  (lessig)", `RIB_BEHAVIOR_CARDS_20260928.md:29-33`); a law row without a
  `teeth` pointer is aspirational prose, and the schema above refuses it.

## 8. What I could not verify / open moves

- `mag/operator_inbox.py:44-63` still has only the binary
  `_is_veto_or_pause` contract (negation guard verified in source); the full
  advisory/directive/veto `tier` field remains unbuilt, so Plane A cannot yet
  inherit authority tiers from live input; the inbox seam is the right first
  enforcement point for the learn-back and is owed separately.
- `mirror_train.jsonl` lives in the sibling republic root
  (`_republic_root()`, `context_pack.py:186-190`); I did not audit its size or
  license posture, only the seam.
- Row counts cited for decisions_log/behavioral_events are this session's
  `wc -l` snapshots (B2-216: instrument, moment, delta; counts are
  snapshots, not constants).

## 9. Bottom line

The estate does not need another place to put operator facts; it needs one
place where operator facts become LAW with evidence, teeth, and visible
freshness, delivered in the frozen boot prefix every seat already parses, and
amended by the correction protocol the operator already runs by hand
(CORRECTION card -> mint -> enforce). The compiler split fixes the pollution;
the A2 placement fixes the delivery price; the append-only + corroborate +
cross-sign protocol fixes the staleness; the three entry points fix the
fragmentation. That is "start remembering": one compiler, one seam, and the
discipline to stop re-deriving him.
