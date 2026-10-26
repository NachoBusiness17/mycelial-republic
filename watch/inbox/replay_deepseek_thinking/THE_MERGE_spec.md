# THE MERGE v1: one surface for play sessions and problem threads

**Deliverable.** One landable spec for `tools/partychat.py`. It merges the thread layer (`PARTYCHAT_spec`, `mag/party_chat.py`) with the two live play carriers (`tools/tavern.py`, `tools/dungeon.py`) on the shared rails (`tools/hermes_burn.py`) and the shared banker (`tools/arena_gwap.py`). Parts 1 through 5 as contracted.

**Citation convention.**
- I have the full bytes of `tools/tavern.py`, `tools/dungeon.py`, `tools/arena_gwap.py`, `PARTYCHAT_spec.md`, and `SEASON_design.md`. Claims from those cite by function name (exact and grep-able) or by quoted bytes. Line numbers are UNVERIFIED because I did not count them.
- Files absent from the evidence (`mag/party_chat.py`, `mag/chan.py`, `mag/game_mud.py`, `watch/room.jsonl`, `configs/kabuki_cast.json`, the gap register, the workflow gate, `watch/inbox/LINKS.jsonl`, `AGENTS.md`) are UNVERIFIED and carry a grep target.
- No em-dashes. Plain hyphens only.

**Two preconditions carried in, on record.**
- Persona persistence is a test, not a proven input. `BARFIGHT_spec.md` (line UNVERIFIED): "Honest limit. No run of this scenario exists yet." Gate G0 stays as PARTYCHAT_part 3.0 defines it.
- The only live prices in evidence are two dungeon chapters, each cut at beat 8, verdict PARTIAL, spend $0.0731 and $0.057, `warden_hp` 18/18 undamaged, per-beat $0.0063 to $0.0091 (`SEASON_design`, reading the DONE rows; raw DONE files UNVERIFIED, grep: `watch/inbox/playground/dnd0_*/DONE`). A chapter cut is not a session verdict. Part 2 fixes the machine that let that label stand; Part 5 prices it.

---

## 1. THE UNIFIED OBJECT

**The object.** A session is one file, `watch/party/<thread>.jsonl`, one hash-chained row per beat. A row is simultaneously a game beat and a thread post. There is no second transcript and no second ledger.

The six bindings the contract names, stated as field-level facts:

| Contract term | Binds to | Evidence |
|---|---|---|
| scene sheet = thread body | The ref `OPEN` row's body carries the scene sheet: `targets` = the gap row's `target_paths`, `falsifier` = the gap row's `falsifier`, plus the obstruction sheet. Dungeon's `S1_SHEET` and `SCENES[scene]["sheet"]` are the template; `Dungeon._scene_sheet` resolves it. | `tools/dungeon.py` `S1_SHEET`, `SCENES`, `_scene_sheet`; PARTYCHAT_part 3.2 `OPEN` row fields |
| personas = thread participants | Tavern persona `{name, model, register, want, secret, tell, escalation_threshold}` and dungeon `ROSTER` `{model, cls, hp, ac, atk, dmg, chk, quirk}` are two sheets of one participant. Merged participant = `{face, trip, family, sheet, secret}`. | `tools/tavern.py` `bar_round` persona block; `tools/dungeon.py` `ROSTER` |
| audits = real byte-checks | `[AUDIT <scroll>]` calls `scroll["check"]()` and gets `(truth, detail)`. The dice decide who gets to try; the bytes decide what is true. | `tools/dungeon.py` `_verdict` AUDIT branch, `REAL_SCROLLS`, `_check_links_405`, `_check_room_big`, `_check_zombie_budget`, and the GWAP rung comment above `REAL_SCROLLS` |
| the brawl = competing builds | Tavern's brawl trigger (`sum(esc) >= heat`, `heat = ESC_BRAWL - 2*pressure`) becomes the fork trigger. The fight is two builds, never two rhetorics. | `tools/tavern.py` `ESC_BRAWL`, `Run.__init__` heat, `Run.play` brawl check; PARTYCHAT_part 3.2 `FORKED` = "2 builds, max" |
| the gate = the referee | `partychat.py` plus the workflow gate (path UNVERIFIED, grep: workflow gate). The dice law computes beat verdicts; the gate computes build scores. No judge model scores a build. | PARTYCHAT_part 3.3 build scoring; `tools/dungeon.py` `_grade`; DND_module law "The carrier computes the verdict, not the DM" (line UNVERIFIED) |
| the root anchor = the landed fix | `[AUDIT root]` at DC 15, three successes, each bound to the landed tip sha. It is the entry guard of `LANDED`, not a later phase. | `tools/dungeon.py` `_grade` AUDIT root branch, `root_anchors`, `campaign` S4 sheet and close |

### 1.1 The merged row schema

| Field | Game source | Thread source | Rule |
|---|---|---|---|
| `thread` (str) | dungeon `Dungeon.tag` / tavern `Run.run` | PARTYCHAT `thread` = `T-<gap_id>` | One identity. Run dir name and thread id are the same string. |
| `n` (int) | dungeon `turn` + row index | PARTYCHAT `n` | 1-based, contiguous over the whole session. A gap is a deleted post. |
| `ts` (str) | both, via `_now()` | PARTYCHAT `ts` | ISO-8601 UTC with `Z`, set at append. |
| `scene` (str) | dungeon `scene` in `{S0,S1,S2,S3,S4}` | (new) | The stage the phase is running in (Part 2). Tavern sessions carry `scene="TAVERN"`. |
| `actor` (str) | dungeon `actor` (`saelis`, `grok`, `warden`, `dm`) / tavern persona | PARTYCHAT `actor` in `{party, anon, ref}` | Merged values `party`, `anon`, `ref`. The seat goes in `face`. |
| `face` (str) | dungeon `ROSTER` key / tavern persona name | PARTYCHAT `face` = kabuki face id | The character sheet. |
| `trip` (str) | (new) | PARTYCHAT `trip` = `!` + `sha256(family:face:secret)[:10]` | Persistent persona. Secret held by the carrier, never in a prompt. Value is `ref` or `anon` for those actors. |
| `family` (str) | tavern persona `model` / dungeon `ROSTER[a]["model"]` | PARTYCHAT `family` from carrier config, never self-reported | Drives the cross-family support rule (Part 2). Stored but hidden from party prompts. |
| `body` (str) | dungeon `speech` / tavern `speech` | PARTYCHAT `body` | One tagged action. Carrier law `strip_and_cap(body, 120)` applies; the schema ceiling is 150 words. The stricter carrier law wins. |
| `artifact` (obj or null) | dungeon `verdict` + `roll_committed` | PARTYCHAT `artifact` = `{targets, falsifier}` | Required on `PROPOSE` and on every `VERIFY`. See 1.3. |
| `roll_committed` (str) | dungeon `roll_committed` = `f"{tip}:{scene}:{turn}:{actor}"` | (new) | The preimage. Committed before the actor speaks. |
| `roll_value` (int) | dungeon `roll_value` | (new) | `int(sha256(preimage)[:8], 16) % 20 + 1`. |
| `verdict` (str) | dungeon `verdict` / tavern `verdict` | (new) | The carrier's ruling. Only the referee writes it. |
| `gate` (obj or null) | (new) | PARTYCHAT `[SCORE ...]` | The deterministic build score, only on referee rows post-`BUILDING`. |
| `cost` (obj) | both, `prompt_tokens` + `completion_tokens` via `_paid`/`PRICING` | PARTYCHAT `cost` | `{"prompt_tokens":int,"completion_tokens":int,"estimated":bool}`. |
| `prev` (str) | (dungeon has no chain) | PARTYCHAT `prev` | Hash of row n-1; 64 zeros for n=1. |
| `hash` (str) | (new) | PARTYCHAT `hash` | sha256 of the canonical JSON minus `hash`. |

**Referee-only content.** `verdict`, `gate`, and the body tokens `[STATE ...]` / `[SCORE ...]`. Any of these inside a party body is an over-claim violation. PARTYCHAT's audit section already catches it: `REF_ONLY = ("[STATE", "[SCORE")`.

### 1.2 The tag grammar, merged

Party tags from PARTYCHAT_part 3.1: `[CLAIM <slot>]`, `[PROPOSE]`, `[EXTEND >>N]`, `[OBJECT >>N]`, `[FORK >>N]`, `[VERIFY >>N]`, `[SAGE]`, `[ASK]`.
Action tags from dungeon: `[ATTACK <obj>]`, `[CHECK persuade|investigate|athletics]`, `[AUDIT <scroll|root>]`, `[CLAIM <obj>]`.
Merged: one tag set, one parser, `extract_tag` semantics preserved (last bracketed tag whose head token is pure letters, so inline dice notes like `[d20=18 + 5 = 23 vs DC 15-SUCCESS]` stay untagged).

The two tags that carry the merge are `[PROPOSE]` and `[AUDIT]`. A `PROPOSE` promises a build. An `AUDIT` banks a byte-check. Every thread must contain at least one of each before it can reach `GATED`.

### 1.3 The artifact object

`artifact` is the join key between play and problem. One field, three shapes:

```json
{"targets":["mag/party_chat.py"],"falsifier":"audit exits 1 on a mutated row","scroll":null,"true":null,"detail":null}
```
```json
{"targets":null,"falsifier":null,"scroll":"Ledger Page","true":true,"detail":"LINKS.jsonl rows counted = 405 (claim: 405)"}
```
```json
{"targets":null,"falsifier":"<root claim>","scroll":"root","true":true,"detail":"<measured return>","tip":"<landed tip sha>"}
```

- Party `PROPOSE`: `targets` (at least one path) and `falsifier` (one checkable line). PARTYCHAT_part 3.3 rule 1. Missing `falsifier` = no promotion.
- Referee `VERIFY` minted from `[AUDIT <scroll>]`: `scroll`, `true`, `detail`, where `detail` is the literal return of the check function. A retyped or paraphrased `detail` is a fabrication, same rule as BARFIGHT: "no paraphrase credit" (line UNVERIFIED).
- Root row: `scroll = "root"`, `true`, `detail`, `tip` bound to the landed sha.

**Positive merged row (ref):**
```json
{"thread":"T-gap042","n":1,"ts":"2026-10-04T12:00:01Z","scene":"S1","actor":"ref","face":"ref","trip":"ref","family":"ref","body":"[STATE OPEN] targets=mag/party_chat.py falsifier=audit exits 1 on a mutated row. Obstruction: the unlabeled door. Loot: Ledger Page (REAL).","artifact":{"targets":["mag/party_chat.py"],"falsifier":"audit exits 1 on a mutated row"},"roll_committed":"<tip>:S1:0:ref","roll_value":0,"verdict":"SCENE OPEN","gate":null,"cost":{"prompt_tokens":0,"completion_tokens":0,"estimated":false},"prev":"0000000000000000000000000000000000000000000000000000000000000000","hash":"<sha256>"}
```

**Negative rows:**
- `"body":"I think we should fix the lock."` No leading tag. Burns one post from the trip's budget. The estate's swarm history is why empty and untagged posts must cost: "of twenty swarm turns attempted, sixteen failed outright and fifteen of them returned empty text" (`FROM_MUD_TO_WOW_20260914.md`, line UNVERIFIED).
- `"body":"[PROPOSE] Fixed. [STATE LANDED]"` Over-claim. Only the referee writes state. Caught by `REF_ONLY`.
- `"body":"[EXTEND] building on the above"` No `>>N`. Unattributable. Violates the schema.
- A `VERIFY` whose `detail` is not the literal return of a check function. Fabrication.

---

## 2. THE STATE MACHINES

Two lifecycles, merged into one table with one writer (the referee) and one clock (the seeded speaker order).

### 2.1 The two lifecycles, stated separately first

**Session beats (the carriers).** Dungeon: S0 omen (1 beat), S1 gate (`Dungeon._forced_audit_beat` then up to `S1_BEATS_CAP = 8`), S2 stair (`beats_cap 10`), S3 vault (`beats_cap 10`), S4 hoard (`beats_cap 16`). Tavern: rounds `1..rounds`, each round is N persona beats plus one judge round, with a brawl check after each round. Beat kinds: PC beat, enemy/obstruction beat, DM readback, forced audit, judge round, ref state row. Evidence: `tools/dungeon.py` `s0`, `s1`, `campaign`, `SCENES`, `S1_BEATS_CAP`, `INITIATIVE`; `tools/tavern.py` `bar_round`, `judge_round`, `play`.

**Thread phases (the spec).** PARTYCHAT_part 3.2: `OPEN -> DISCUSS -> {CONVERGED | FORKED | DEAD} -> BUILDING -> GATED -> {LANDED | DISCUSS (once) | DEAD} -> MINED -> REDTEAM -> CLOSED`. `DEAD` terminal, rows kept.

### 2.2 The merged transition table

| State | Entered by (beat) | Thread rule | Legal transitions | Terminal |
|---|---|---|---|---|
| `OPEN` | S0 omen. Ref posts the scene sheet and the forced audit of the row's first scroll. | The gap row carries `{gap_id, title, target_paths, falsifier}`. No falsifier = refuse. | `DISCUSS` at the first party post; `DEAD` if the row is refused or not compilable. | no |
| `DISCUSS` | Party beats roll (`CLAIM`, `PROPOSE`, `EXTEND`, `OBJECT`, `FORK`, `VERIFY`, `SAGE`, `ASK`); obstruction beats; DM readbacks. S1 gate, S2 stair, tavern rounds. | Posting. The promotion rule is watched on every post. | `CONVERGED`, `FORKED`, `DEAD` (phase cap, bump limit, or VOID). | no |
| `CONVERGED` | Exactly one `PROPOSE` qualifies and no rival gains support within 6 posts. | PARTYCHAT_part 3.3 rules 1 through 4. | `BUILDING` (1 build); `FORKED` if a rival later qualifies; `DEAD`. | no |
| `FORKED` | Two candidates qualify with overlapping targets plus a `FORK` or cross-`OBJECT`. This is the brawl: support count at or above the threshold. | PARTYCHAT_part 3.2. Tavern heat `18 - 2*pressure` becomes the support threshold. | `BUILDING` (2 builds, max); `DEAD`. | no |
| `BUILDING` | Builder lane runs. Branches `party/<thread>/A` and `party/<thread>/B`. This is S3 vault: extraction under a load that wipes unverified carries. | `_mimic_wipe`: a HIT against a trip whose previous beat was `FAIL`/`MISS`/`FUMBLE` drops that trip's unverified artifacts. Runner health is checked first. | `GATED`; `DEAD` (budget, runner down). | no |
| `GATED` | Referee posts one `[SCORE A|B gate=.. smoke=.. fals=.. diff=.. matters=..]` row per build. S4 hoard is this phase's adversary: the phantom wyrm hoards unresolvable citations. | Lexicographic on `(gate, smoke, fals)`, then smaller `diff`, then earlier proposal. No judge model. `LANDED` requires the 3 root anchors at DC 15. | `LANDED`; `DISCUSS` once if every build fails the anchor; `DEAD`. | no |
| `LANDED` | Winner merged, bindings written by the referee only, three `[AUDIT root]` successes at DC 15 against the landed tip sha. This is the root anchor, and it is the entry guard, not a later phase. | The landed fix. | `MINED`. | no |
| `MINED` | Referee posts loser hunks absent from the winner; shared hunks marked `DUP`. | Duplication is emphasis to mine for nuance. | `REDTEAM`; `DEAD`. | no |
| `REDTEAM` | 7 swarm chairs post `[OBJECT >>N]` as `anon`, each with a repro command and expected output. The tavern brawl with models swapped for chairs. | Every confirmed finding either spawns a child `OPEN` thread citing the parent or is closed. A failed wave suspends only that wave. | `CLOSED`; `DEAD`. | no |
| `CLOSED` | No confirmed finding, or every finding has a child thread. | terminal | none | **yes** |
| `DEAD` | Phase cap hit, bump limit reached without promotion, or `VOID` (3 consecutive voided beats). | Rows stay; "down seats stay records" (DND_module, line UNVERIFIED). | none | **yes** |

### 2.3 The exhaustive legal edge list

```
OPEN       -> DISCUSS | DEAD
DISCUSS    -> CONVERGED | FORKED | DEAD
CONVERGED  -> BUILDING | FORKED | DEAD
FORKED     -> BUILDING | DEAD
BUILDING   -> GATED | DEAD
GATED      -> LANDED | DISCUSS (once, all builds fail the anchor) | DEAD
LANDED     -> MINED
MINED      -> REDTEAM | DEAD
REDTEAM    -> CLOSED | DEAD
CLOSED     (terminal)
DEAD       (terminal; VOID is a DEAD cause)
```

The `GATED -> DISCUSS` allowance is counted once across the thread's life, not per phase. This is a new rule and is marked as such.

### 2.4 The beat-to-state map

| Carrier beat | Merged state it runs in | Source |
|---|---|---|
| S0 omen + scene sheet + forced audit | `OPEN` | `Dungeon.s0`, `_forced_audit_beat` |
| S1 gate | `DISCUSS` | `Dungeon.s1` |
| Tavern bar round | `DISCUSS` (same phase, different room; the tavern is the social scene sheet) | `Tavern.bar_round` |
| S2 stair | `DISCUSS` (the ordering problem: proposals sorted as text, not time) | `Dungeon.campaign` S2 |
| Fork trigger | `FORKED` | new `support()`, replacing the tavern judge escalation |
| S3 vault | `BUILDING` | `Dungeon.campaign` S3, `_mimic_wipe` |
| S4 hoard + `[AUDIT root]` | `GATED` | `Dungeon.campaign` S4, `_wyrm_regrowth`, `_grade` AUDIT root |
| Ref `[SCORE]` rows | `GATED` | new `score()` |
| Loser hunks | `MINED` | new `mine()` |
| 7 anon chairs | `REDTEAM` | new `redteam()` |

**The one thing that does not transfer.** Tavern's `judge_round` asks a model to score escalation. In the merged object a judge model may not write state (`GATED` scoring is deterministic; ARENA: "the runtime validates against the graph and operator history deterministically (no judge model)", line UNVERIFIED). Escalation is recomputed from cross-family `EXTEND`/`VERIFY` counts. The judge call is removed from the state path. If kept at all, it narrates and cannot write state.

### 2.5 The clock

One clock governs every beat. The next speaker is `argmin` over eligible trips of `sha256(f"{tip}:{thread}:{n}")`. Eligible means under budget and not the author of post n-1. This replaces `INITIATIVE` and mirrors DND_module: "the tip is fixed before the actor is called" (line UNVERIFIED). Calls are sequential on the main retry path per GALA as quoted in `BARFIGHT_spec.md` (line UNVERIFIED): "Workflow children get zero adapter attempts and die on first 429".

---

## 3. THE CARRIER MERGE

Destination: `tools/partychat.py`. (PARTYCHAT_spec names `mag/party_chat.py`; the contract names `tools/partychat.py`. The audit section is imported from wherever it lands.) Three verdicts: **REUSE** (verbatim), **ADAPT** (same body, new caller or signature), **NEW** (does not exist in either carrier).

### 3.1 What `tools/tavern.py` contributes

| Source | Destination | Verdict | Note |
|---|---|---|---|
| `_roll(chain, scene, turn, actor)` | `roll(preimage)` | REUSE | Same preimage shape and same modular law as `dungeon.roll`. One roll function. |
| `LAWS` | `LAWS` | REUSE | Estate laws block, verbatim, as the system prompt prefix. |
| `TEMPER` | `PRESSURE` | ADAPT | 0-5 labels reused as escalation and pressure labels. |
| `ESC_BRAWL = 18` | `HEAT_BASE = 18` | REUSE | `heat = 18 - 2*pressure`, `Run.__init__`. |
| `Run.__init__` | `Session.__init__` | ADAPT | Reuse run-dir ownership, `scenario.json` write, same-second collision suffix loop, DONE marker. Add: gap-row import, hash-chain seed, phase init. |
| `Run.row` | `Session.row` | ADAPT | Reuse JSONL append and `play.md` render. Add `prev`/`hash` before append; render `verdict` and `gate`. |
| `Run._paid` | `Session._paid` | REUSE | The single paid-call seam: `_call`, usage, `PRICING`, `self.spend`, `_bank`, `ok=bool(content)`. Add dungeon's `finish_reason` field and the retry-through-`content_filter` loop. |
| `Run.bar_round` | `Session.party_round` | ADAPT | Reuse persona loop, per-beat budget check, system prompt assembly, transcript tail as user context. The temper/threshold block becomes the fork-pressure block. |
| `Run.judge_round` | `Session.support_round` | **REPLACE** | A judge model may not score. Escalation is recomputed deterministically from cross-family `EXTEND`/`VERIFY` counts. The judge call leaves the state path. |
| `Run._lines` | `Session.tail` | ADAPT | Reuse; add the 6000-char mount clip (DND_module: `party_subchain.mount(max_chars=6000)`, line UNVERIFIED). |
| `Run.play` | `Session.play` | ADAPT | Reuse round loop and brawl check. The brawl becomes the `FORKED` transition. DONE write stays. |
| Fire-atomic bank at exit (`from tools.arena_gwap import SessionLedger, bank`) | same | REUSE | Both carriers already do this. `partychat` inherits it verbatim. |

### 3.2 What `tools/dungeon.py` contributes

| Source | Destination | Verdict | Note |
|---|---|---|---|
| `check_golden()` + `GENESIS` + `roll` | `check_golden()` | REUSE | Three pinned preimages must reproduce at startup or the session refuses to run. `partychat` pins its own three: `(tip, "OPEN", 0, "ref")`, `(tip, "DISCUSS", 1, "<first face>")`, `(tip, "GATED", 0, "ref")`. |
| `strip_and_cap(speech, cap=120)` | `lint_body(body)` | REUSE | Em-dash to hyphen, 120-word cap, logged rule break. Carrier law, not model manners. |
| `extract_tag(speech)` | `parse_tag(body)` | REUSE | Last `[VERB ...]` tag whose head is pure letters. The parser fix is a precondition: the line-initial scan reads tagless past the one-line flattening (`extract_tag` docstring, `tests/test_dungeon_parser.py`). Extend the tag set with PARTYCHAT's party tags. |
| `Dungeon.__init__` counters (`audits`, `root_anchors`, `voided_calls`, `voided_readbacks`, `pc_hp`, `claims`, `packs`) | `Session.__init__` | ADAPT | Reuse all. `claims` becomes per-slot claims; `packs` becomes per-trip artifact packs. |
| `Dungeon._paid` | `Session._paid` | REUSE | 3-attempt retry through `content_filter`, void counter, `finish_reason` bank, the dead fallback name fixed to `reasoning_content`. |
| `Dungeon._dm` | `Session.narrate` | REUSE | The DM prompt is fed the carrier verdict and asked to narrate only. DND_module law. |
| `Dungeon._verdict` (S1) | `Session.grade_s1` | ADAPT | S1 compatibility only. `_grade` is the general path. |
| `Dungeon._grade` | `Session.grade` | REUSE | The general grader. Its two fixed defects are preconditions: the tag parse (`a02#0`) and the S4 disjunct parenthesization (`a02#1`, 14/14 logged S4 verdicts). |
| `Dungeon._pc_beat` | `Session.party_beat` | REUSE | System prompt with quirk, transcript tail, pay, strip, grade, narrate, row. |
| `_warden_beat` + campaign enemy branch | `Session.obstruction_beat` | ADAPT | Generalized over `_enemy_sheet`; stats come from the scene sheet. |
| `Dungeon._tail` | `Session.tail` | REUSE | |
| `Dungeon.s0` | `Session.open` | ADAPT | The omen becomes the `OPEN` beat: scene sheet post plus forced audit of the row's first scroll. |
| `Dungeon._forced_audit_beat` | `Session.open_audit` | ADAPT | The forced audit generalizes: beat one of every thread structurally audits the row's first scroll. The pre-registered TURN-ONE-AUDIT lance becomes the default, because the measured voluntary-audit baseline was 0-for-4. |
| `Dungeon.s1` | folded into `Session.play` | ADAPT | The S1 loop body. |
| `Dungeon.campaign` | `Session.build_gate_anchor` | ADAPT | The S2/S3/S4 loop. Packs, regrowth, wipe, root anchors all carry. |
| `_wyrm_regrowth(ehp, packs)` | `Session.regrowth` | REUSE | Obstruction heals 5 per unfalsified claim. Merged meaning: the problem grows while the falsifier is unproven. The spec'd but never-enforced defect is a precondition: see the `_wyrm_regrowth` docstring. |
| `_mimic_wipe(target, packs)` | `Session.wipe` | REUSE | A HIT against a trip whose previous beat was `FAIL`/`MISS`/`FUMBLE` drops that trip's unverified artifacts. The off-spec party-wide wipe is a precondition to fix. |
| `_find_scroll(packs, obj)` | `Session.find_artifact` | REUSE | Case-folded lookup. The lowercasing defect at `dungeon.py:515` (HEAD `37e2fba7e`) is a precondition. |
| `_phantom_count(packs)` | `Session.unverified_count` | REUSE | The falsifier-debt counter. |
| `_packs_str(packs)` | `Session.carried_str` | REUSE | |
| `_beat_outcome(verdict)` | `Session.outcome(verdict)` | REUSE | Verdict to outcome token. The wipe and phase guards read it. |
| `_scene_sheet` / `_enemy_sheet` | `Session.scene_sheet` | ADAPT | Resolves the scene sheet from the gap row, not a hardcoded `SCENES`. |
| `REAL_SCROLLS`, `_check_links_405`, `_check_room_big`, `_check_zombie_budget` | `AuditScroll` protocol + `compiler.gap_row_to_scrolls` |