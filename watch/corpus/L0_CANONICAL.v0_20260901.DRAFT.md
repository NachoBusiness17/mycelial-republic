# L0 — Universal Game Contract (CANONICAL)
> **SUPERSEDED 2026-09-23** by L0_CANONICAL.md (Grok long-form, sealed).
> Vocabulary alias for estate continuity: SELF setup = F1 STATE ENCODING ·
> SELF turn/init = F2 INITIAL STATE · SELF legal = F3 LEGAL? ·
> SELF move = F4 TRANSITION · SELF evaluate = F5 TERMINAL? ·
> SELF render = F6 SCORE. One vocabulary, not two.



> **Status:** CANONICAL — merged from self-built `L0_contract.md` + `L0_universal_contract.DRAFT.md`.
> **Provenance tags:** `BOTH` = in both sources · `SELF` = self-built only · `DRAFT` = draft only.
> **Class:** L0 static prefix; instantiable by every L1/L2 race/dice game. This is the canonical
> six-function + RNG + verifier-vocabulary contract. Consumers: verifiers, L1 engine authors,
> L2 pack authors. Per-game `INIT`/`WIN`/`SCORE`/`board` grammar live at L2 and are appended
> atomically, never interleaved here.

---

## 1. THE SIX-FUNCTION CONTRACT  [BOTH]

A conformant game MUST expose exactly six functions. Two equivalent labelings exist in the
corpus; the canonical binding is: **abstract role names** (spec-level, SELF) map 1:1 onto the
**draft's role names** (prompt-level, DRAFT), as shown. `[DRAFT]` signatures are the concrete
canonical-state-string forms the LLM consumes; `[SELF]` signatures are the pure-spec forms a
verifier enforces.

| # | SELF name (abstract) | DRAFT name (prompt) | DRAFT signature (State is a canonical flat string) |
|---|----------------------|---------------------|-----------------------------------------------------|
| 1 | `setup`              | STATE ENCODING      | carry each game as one flat string, fixed field order (below) |
| 2 | `turn` / init        | INITIAL STATE       | seeded-deterministic from L2 `INIT` + external seed |
| 3 | `legal`              | LEGALITY            | `LEGAL?(state, T) -> {legal: Bool, reason: String?}` |
| 4 | `move`               | TRANSITION          | `APPLY(state, T) -> state'` (new canonical string) |
| 5 | `evaluate`           | TERMINAL DETECTION  | `TERMINAL?(state) -> {terminal: Bool, winner?: Role, score?: Score}` |
| 6 | `render`             | SCORING             | `SCORE(state) -> Score \| null` (pack `SCORE` rule) |

**Pure-function invariants [SELF]** (also honored by DRAFT determinism rule):
- All six are pure: same inputs -> same outputs.
- `legal`/`LEGAL?` is authoritative; `move`/`APPLY` MUST reject any action not returned legal.
- No function has side effects or depends on wall-clock time.

### 1.1 Canonical state encoding (DRAFT, adopted canonically)  [DRAFT]

Every game instance is carried as a single flat string, fixed field order:

```
<enum:zero-indexed game id>:<state-hash>:<turn-index>:<active-role>:<board>:<order>:<seed-phrase>:<reserved>
```

- `game id` — fixed per game, defined in its L2 statics.
- `state-hash` — deterministic digest, recomputed by verifier; never reused across states [SELF: replay guard].
- `turn-index` — non-negative; increments on every completed transition.
- `active-role` — role/piece whose turn it is.
- `board` — encoded play surface; grammar per game; MUST be reprinted verbatim, never paraphrased.
- `order` — enumeration/layout token stream; reprinted verbatim.
- `seed-phrase` — external entropy anchor; NEVER generated or guessed.
- `reserved` — future flags; leave `-`.

**Canonical-rule:** `board`+`order` are the ONLY authority on positions. A spoken sentence that
contradicts the canonical string loses. Replies must reprint the current canonical string, marked
with one leading `^`.

---

## 2. RNG PROTOCOL  [BOTH — reconciled]

All randomness is **seeded-external and deterministic**. Nothing is improv guessed; `value =
TABLE[game-id][mode-name][seed-phrase][draw-index]`. Two audit models are reconciled below:
DRAFT keys draws by `(seed-phrase, turn-index)`; SELF keys by a single monotonic stream.

**Canonical rule:** the authoritative reproducibility anchor is the **committed draw stream
`S`** [SELF]. Each random draw increments a monotonic draw-index `i`. Reproduction must assume the
draw-index is derivable from the recorded per-move draw log. For single-roll-per-turn games this
collapses to DRAFT's `(seed-phrase, turn-index)` keying; for games with multiple draws per turn,
consumers MUST count draws, not turns. **No cryptographic RNG required** — only determinism +
replay audit [SELF].

**Modern modes [DRAFT]** — algebra `XdY+Z`, evaluate left-to-right (low standard bit 0/1):
- `XdY` — X fair Y-sided dice, uniform 1..Y, total = sum.
- `+Z`/`-Z` — flat modifier after summing.
- `kX` — keep best (`a d20 k1`) / `kd` keep lowest.
- `!` — exploding; each die showing max re-rolls/adds; cap 8 re-rolls.
- `pool Y tN` — Y dice, count successes ≥N. Compose in order: pool → keep → mod.

**Historical modes [DRAFT]** — LLM reports, never rolls (all seeded-external):
1. **astragali** — 4 asymmetric knucklebones, faces 1/3/4/6, unequal probs (1&6 ~10%, 3&4 ~40%);
   outcomes = 54/240-cluster sums + all-different "Venus"; via seeded table.
2. **Ur binary tetrahedral** — 4 tetrahedral dice, each marks ONE corner="1" else "0"; result =
   count of marked (0..4); per Finkel BM 33333 (`reconstructed`).
3. **casting-sticks** — 1..4 flat sticks, one marked side, count marked. 1 stick = fair 0/1;
   2 sticks (Ur/pachisi) = 0,1,2 (double counts highest); 4 sticks (Patolli) = 0..4
   (`reconstructed` — Durán; Murray).
4. **cowries** — N cowries; open-toothed face =1. Count open; some schools double-count all-same
   (per pack).
5. **marked-beans** — draw from bag/field of marked beans (e.g. Patolli's 5); count marked = move.
   Reshuffle-reseed exhaustively (no re-use until pool refills) for a finite fair sample.

---

## 3. VERIFIER VOCABULARY  [BOTH — reconciled]

### 3.1 Verdict model [SELF] (canonical terminal judgment)
Verdict type `{result, reason_code, detail?}`:
- `PASS` — actor met the win/requirement condition.
- `FAIL` — actor violated a rule or failed a requirement on a terminal state.
- `TIE` — terminal state, no unique winner / no applicable judgment.

**Reason codes [SELF]** — stable strings, extended per contract:
- `RNG_DIVERGE` — replay stream did not match committed draws.
- `ILLEGAL_MOVE` — `move` accepted an action outside `legal`.
- `ILLEGAL_TURN` — `turn`/`move` acted out of legal turn order.
- `WIN_CONDITION` — PASS: win condition met.
- `VIOLATION` — FAIL: explicit rule broken (contract-specific sub-codes).
- `STALEMATE_TIE` — TIE: no legal action for any actor and no win.
- `PROVISIONAL` — non-terminal; `evaluate` called early (flagged inconclusive).

### 3.2 Verifier-signature checks [DRAFT] (adopted)
- `LEGAL?` returns `{legal, reason}`; determinism + hard `false` on any false (turn/order/dest).
  Never mark legal "by narrative"; ambiguity → hard `false`.
- `TERMINAL?` defined per pack `WIN` rule; a loop/state-repetition never auto-terminates unless
  `WIN` says so — otherwise reported as `LOOP` with prior matching `state-hash` [DRAFT] (aligns
  with `STALEMATE_TIE` for the no-legal-action case).
- Missing/unknown rule → `UNKNOWN-RULE`, refuse to invent [DRAFT].
- On contested/reconstructed history: emit status flag + one-line honesty note; never silently
  upgrade a flag (`reconstructed`/`speculative`/`attested`) [DRAFT].

### 3.3 Verifier role [SELF] (adopted)
Any verifier can replay the full game given `seed` + action log (each `move` records draw-index
consumed and held values). Divergence from the committed stream => `FAIL(code RNG_DIVERGE)`.
DRAFT's per-turn `state-hash` recomputation is the drift guard (primer Fact 6) [BOTH].

---

## 4. OUTPUT / BEHAVIOR CONTRACT  [DRAFT]

1. **Canonical restatement first** — every reply begins with the one-line `^`-flagged state, then
   roll/result, then the answer. [SELF: `render(state) -> View` emits this public view; hidden info
   only if the L2 spec allows.]
2. **Cite the rule** — quote the governing clause (function number or RNG mode) before acting.
3. **Never invent objects** — pieces/squares/cells/tiles/cards/paths exist ONLY if in cached
   `board`/`order` or pack statics. Encoded-less piece cannot move; uncached rule cannot apply;
   else `UNKNOWN-RULE`.
4. **Determinism over narration** — canonical string governs; prose is decoration after the string,
   never a replacement.
5. **Contested history** — always flag `reconstructed`/`speculative` + one-line honesty note.

---

## 5. CONTRACT EXTENSIBILITY  [BOTH]

L1/L2 games are L0 instantiations: same six functions, game-specific `reason_code` additions,
game-specific `render` view, per-game `INIT`/`WIN`/`SCORE`/`board` grammar appended atomically at
L2 (never interleaved). A verifier that enforces L0 shapes can enforce any L1/L2 built on these
six functions without new skeleton tooling. Cross-ref: L0 → `L1_engines/*` → L2 statics → L3 packs.

---

## 6. RESEARCH STATUS  [DRAFT]

- Ur dice — `reconstructed` (Finkel, BM 33333).
- Patolli casting — `reconstructed` (Durán; Murray).
- Astragali probabilities — `attested` (Greek/Roman epigraphy cluster).
- Flags must not be silently upgraded.
