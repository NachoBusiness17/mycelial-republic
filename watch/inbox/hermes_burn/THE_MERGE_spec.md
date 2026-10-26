# THE_MERGE_spec (anthropic/claude-opus-5.5, turn 1, channel: content)

# THE MERGE v1: one object for play sessions and problem threads

**Deliverable.** This is one landable spec for `tools/partychat.py`. It covers the unified row schema, the merged state table, the function-by-function wiring, the gap importer, and the cost model with its falsifier. The falsifier for this spec itself is at the end of Part 5.

**Citation convention**
- Lines marked *(pc)* were paste-counted from the evidence block. The quote binds, not the number.
- Elsewhere I cite `file::symbol` with quoted bytes and mark the line `UNVERIFIED`. Grep the quote to find it.
- Files absent from the evidence are marked **UNVERIFIED**. These include the gap register, the workflow gate, the builder lane, `mag/party_chat.py`, and `tools/hermes_burn.py` internals.

**Three corrections to the premise, on record (from bytes, not reports)**

| # | Premise | Bytes say | Consequence for the merge |
|---|---|---|---|
| C1 | "personas" can satisfy PARTYCHAT's cross-family promotion rule | `tools/dungeon.py::ROSTER`: `"grok": {"model": "anthropic/claude-fable-5.1"`, `"deepseek": {"model": "anthropic/claude-haiku-4.5"`, `"chatgpt": {"model": "anthropic/claude-sonnet-5.5"`. All four seats are one vendor. | With the shipped roster, PARTYCHAT rule 3.3.2 ("at least one of those trips is from a family different") can never pass. Every thread would die. Fix in Part 1 (`family` rule) and Part 2 (`REFUSED` guard). |
| C2 | The dungeon "refuses to run" without golden vectors | `tools/dungeon.py:12-13` *(pc)* "golden vectors: the module's three pinned preimages must reproduce at startup or the session refuses to run". But `check_golden` only computes and writes them (`pins[pre] = roll(pre)`) and never compares them to a pinned value. | No refusal path exists. The merge adds a real comparison (Part 3, `pin_golden`). |
| C3 | Tavern "never replays" | `tools/tavern.py:18` *(pc)* "no re-fire law: a run dir with DONE never replays (use --force to legate)". `tavern.py::main` defines no `--force` flag, and `Run.__init__` always allocates a fresh dir. | The no-replay law is unenforced in tavern. The merge enforces it per `gap_id` (Part 2, `OPEN` guard). |

---

## 1. THE UNIFIED OBJECT

### 1.1 Identity

One **session** is one **thread**. One gap row yields one session id, `P-<gap_id>-<stamp>[_<seq>]`.

The run dir is `watch/inbox/playground/party_<gap_id>_<stamp>[_<seq>]/`. It holds:
- `transcript.jsonl`: the hash-chained post log, which is the thread
- `sheet.json`: the scene sheet, which is the thread body
- `golden_vectors.json`
- `play.md`: render only, never evidence
- `DONE`
- `GWAP_BANKED`

**Why the playground and not PARTYCHAT's `watch/party/<thread>.jsonl`.** `tools/arena_gwap.py` banks only from `PLAY_DIR = ROOT / "watch" / "inbox" / "playground"` and requires `(d / "transcript.jsonl").is_file()` (`arena_gwap.py::main`, line UNVERIFIED). Wire, don't build: the merged session lives where the existing bank already looks. This is a deliberate deviation from PARTYCHAT_spec 3.1, recorded here.

### 1.2 The mapping (game term = thread term = what the bytes do)

| Game term (source) | Thread term (PARTYCHAT) | Merged meaning, enforced by the carrier |
|---|---|---|
| **Scene sheet** (`dungeon.py::S1_SHEET`, rendered into every prompt as `f"SCENE: {S1_SHEET}"`) | Thread body: the referee's `OPEN` survey | `sheet.json` is generated from the gap row (Part 4). It holds the targets, the falsifier, and the scrolls (claims to check). It is rendered into every party prompt in place of `S1_SHEET`. |
| **Personas** (`dungeon.py::ROSTER`, `tavern.py` scenario `personas`) | Participants (trips) | Each roster entry is a trip, `!sha256(f"{family}:{face}:{secret}")[:10]`. `family` is the **vendor prefix of `model`** (the text before `/`), never the persona name. C1 shows why: the name `"grok"` sits on an anthropic model. |
| **Quirks** (`ROSTER[*]["quirk"]`) | Lint rules | These are carrier law, not flavor. Mapping in 1.4. |
| **Dice** (`dungeon.py::roll`, preimage `f"{tip}:{scene}:{turn}:{actor}"`) | Seeded speaker order | Dice choose **who speaks next**. Dice never decide **what is true**. That is the law `dungeon.py` already states above `REAL_SCROLLS`: "The dice decide WHO gets to try; the bytes decide WHAT IS TRUE." |
| **Audits** (`[AUDIT <scroll>]`, `REAL_SCROLLS`, `_check_*`) | `[VERIFY >>N]` and greentext | A real byte-check runs by the carrier against a declarative check row (Part 4). The result is `TRUE` or `PHANTOM`, with a detail string. |
| **The brawl** (`tavern.py::play`, `sum(self.esc.values()) >= self.heat`) | `FORKED` and rival builds | Two qualifying candidates become two builds on branches `party/<sid>/A` and `party/<sid>/B`. The trigger is the deterministic PARTYCHAT promotion rule. It is **not** a judge-scored temper sum (1.3, negative example). |
| **The gate** (S1 warden: "Name what you claim, or claim nothing.") | Referee: gate, smoke, falsifier | The workflow gate (path **UNVERIFIED**) plus the gap row's falsifier command. It is the only source of `[SCORE]`. |
| **The Wyrm / the hoard** (S4 sheet: "every scroll it hoards cites a row ... that resolves to nothing") | The open gap | The Wyrm is the gap's falsifier **failing on the base commit**. Phantom scrolls are claims in the thread that a check found false. |
| **Root anchor** (`self.root_anchors`, "three [AUDIT root] successes at DC 15") | `LANDED` | Exactly three carrier byte-checks. No DC applies, and dice play no part. A1: the gate passes on the landed commit. A2: the falsifier passes on the landed commit. A3: the same falsifier **fails** on the landed commit's parent. A3 proves the fix is not vacuous. `anchors == 3` is the only route to `LANDED`. |
| **Gardener / DM** (`dungeon.py::_dm`, "you only narrate consequences") | WELL host | The gardener narrates at phase changes only. It never scores, never writes `[STATE]`, and never sees `family`. |

### 1.3 Merged row schema (one JSONL row per post, `transcript.jsonl`)

This is the PARTYCHAT_spec 3.1 schema, unchanged in meaning, plus the dungeon fields that `arena_gwap.actor_payloads` already reads. New fields are marked **NEW**.

| field | type | rule | source |
|---|---|---|---|
| `thread` | str | session id `P-<gap_id>-<stamp>` | PARTYCHAT 3.1, extended |
| `n` | int | 1-based and contiguous | PARTYCHAT |
| `ts` | str | ISO-8601 UTC `Z` | `hermes_burn._now` (reused) |
| `actor` | str | `party`, `anon`, `ref`, or `garden` (**NEW**: gardener rows, which carry no state) | PARTYCHAT, extended |
| `trip`, `face`, `family` | str | `family` is the vendor prefix of `model` | PARTYCHAT, and C1 |
| `model` | str | the model id actually called | `tavern.py::_paid` row has `model=model`. `arena_gwap.actor_payloads` falls back to "the row's own field, never a guess". |
| `phase` | str | the current state from Part 2 (**NEW**, replaces dungeon `scene`) | `dungeon.py` `scene=` |
| `roll_committed` | str | `f"{tip}:{phase}:{n}:{trip}"`, written **before** the call | `dungeon.py` `roll_committed=` |
| `roll_value` | int | `roll(roll_committed)`. Used for speaker order only. | `dungeon.py::roll` |
| `body` | str | 150 words or fewer. Opens with exactly one PARTYCHAT tag. | PARTYCHAT 3.1. Truncation via `dungeon.py::strip_and_cap`. |
| `artifact` | obj or null | required on `PROPOSE`: `{targets, falsifier}` | PARTYCHAT |
| `check` | obj or null | **NEW**. Written by `ref` only: `{"scroll":id,"kind":k,"true":bool,"detail":str,"cmd_sha":hex}` | generalizes the `real` dict in `dungeon.py::_verdict` |
| `verdict` | str or null | written by `ref` only: `[STATE ...]`, `[SCORE ...]`, `[ANCHOR i/3 ...]`, `[VOID ...]` | `dungeon.py` `verdict=`, read by `arena_gwap._ruling_verb` |
| `finish_reason` | str | from the vendor response | `dungeon.py::_paid` "VOID CENSORSHIP LAW" |
| `cost` | obj | `{"prompt_tokens","completion_tokens","attempts","estimated"}`. `attempts` is **NEW** (see Part 5, the D1 undercount fix). | PARTYCHAT and `_paid` |
| `prev`, `hash` | str | sha256 chain | PARTYCHAT 3.1 |

**Positive example (an audit beat, a ref row after a party `[VERIFY >>3]`):**
```json
{"thread":"P-gap042-20261005T120000Z","n":4,"ts":"2026-10-05T12:01:10Z","actor":"ref","trip":"ref","face":"ref","family":"ref","model":"carrier","phase":"DISCUSS","roll_committed":null,"roll_value":null,"body":"[CHECK s2]","artifact":null,"check":{"scroll":"s2","kind":"row_count","true":false,"detail":"LINKS.jsonl rows counted = 391 (claim: 405)","cmd_sha":null},"verdict":"[CHECK s2 PHANTOM]","finish_reason":"","cost":{"prompt_tokens":0,"completion_tokens":0,"attempts":0,"estimated":false},"prev":"<hash n=3>","hash":"<sha256>"}
```

**Negative examples:**
- A party row carrying `"check":{...}` or `"verdict":"[ANCHOR 3/3]"` is an over-claim, under the same class as PARTYCHAT's `[STATE` rule. `check` and `verdict` are ref-only fields. The audit rejects the row.
- `"family":"grok"` on `"model":"anthropic/claude-fable-5.1"` is a fabricated family. `family` must equal `model.split("/")[0]`.
- A brawl decided like `tavern.py::judge_round` ("Score escalation 0-5 for each persona", parsed from a judge model's JSON) is forbidden as a merged verdict. PARTYCHAT 3.3 says "No model scores a build". The fork trigger is the promotion rule.

### 1.4 Quirks become lint (carrier law, never model manners)

| Dungeon quirk (bytes) | Merged lint rule | Penalty |
|---|---|---|
| saelis: "CLAIM before ATTACK, otherwise the beat has no effect" (`ROSTER["saelis"]["quirk"]`) | A `PROPOSE` whose `artifact.targets` include a path no live `[CLAIM <slot>]` in this thread covers is `void:unclaimed`. | The post stays on the chain but cannot promote. |
| grok: "Speech over 1000 characters has no effect this beat" | A body over 150 words (the PARTYCHAT cap) is truncated by `strip_and_cap(cap=150)` and logged `rule_break`. | Same as `dungeon.py` `"word_overflow_truncated"`. |
| chatgpt: "Self-verdict tokens (SUCCESS/VERIFIED/PROVEN) void the beat" | Any party body containing `[STATE`, `[SCORE`, `[ANCHOR`, `PROVEN`, or `VERIFIED` outside a `>` greentext line is `void:overclaim`. | The post costs one unit of the trip's budget. |
| deepseek: "Cheap seat: you act TWICE per round" | The cheapest roster model by `PRICING` gets budget 2x. | The budget is per-trip, not per-round. |
| `_pc_beat` "3-STRIKE VOID BREAKER" | Three consecutive voided party posts lead to the terminal `VOID` state. | This is a terminal state (Part 2). |

---

## 2. THE STATE MACHINES

### 2.1 The merge principle

The dungeon's scenes are a **beat lifecycle** (`S0 -> S1 -> S2 -> S3 -> S4`, with exits on cut, void, or budget). PARTYCHAT's phases are a **problem lifecycle**. They merge 1:1. Each phase *is* a scene, and the scene's mechanic is the phase's guard.

| Phase | Scene it absorbs | Why that scene fits (bytes) |
|---|---|---|
| `OPEN` | S0 omen + `_forced_audit_beat` | The omen is a carrier roll before play. The forced audit is "beat one is structurally an audit". In the merge, the carrier runs the falsifier on base and every scroll check before any model speaks. |
| `DISCUSS` | S1 keep gate | Claim gate ("Name what you claim, or claim nothing") is the CLAIM-before-PROPOSE lint. |
| `CONVERGED` / `FORKED` | S2 lexical stair | "ordered as text, not time": candidates are ranked by the deterministic support count, then earliest `n`. |
| `BUILDING` | S3 wiping vault | "Load-Failure Wipe": a build that fails drops its unverified hunks (see `MINED`). |
| `GATED` -> `LANDED` | S4 hoard + root anchoring | Downing the Wyrm does not win. Three anchors do. |
| `MINED` | `campaign` loot log | Loser hunks are the loot. |
| `REDTEAM` | (new, swarm) | No dungeon equivalent. Taken from PARTYCHAT 3.2. |

### 2.2 The transition table (every legal transition)

The writer of every transition is `ref`, as a row with `verdict="[STATE <to> ...]"`. **Any transition not in this table is illegal.** `audit` exits 1 on it.

| # | From | To | Guard (all must hold) |
|---|---|---|---|
| T0 | (none) | `OPEN` | The gap row has `gap_id, title, target_paths, falsifier`. Roster has ≥2 distinct `family` values. Golden vectors match their pins. There is no prior `DONE` for this `gap_id` with verdict `LANDED` or `CLOSED`. |
| T1 | (none) | `REFUSED` | Any T0 guard fails, **or** the falsifier passes on base. A passing falsifier means there is no Wyrm, because the gap is already fixed or the falsifier is vacuous. |
| T2 | `OPEN` | `DISCUSS` | All scroll checks ran (each produced a `check` row), and the first party post was appended. |
| T3 | `DISCUSS` | `CONVERGED` | Exactly one `PROPOSE` meets PARTYCHAT 3.3, and no rival gains support within the next 6 posts. |
| T4 | `DISCUSS` | `FORKED` | Two candidates meet 3.3 with overlapping targets, plus a `FORK` or cross-`OBJECT` between them. |
| T5 | `DISCUSS` | `DEAD` | The DISCUSS token cap is hit, or the bump limit (40 posts) is reached without promotion. |
| T6 | `DISCUSS` | `VOID` | Three consecutive party posts are void (empty, `content_filter`, or length ≤1). This is the `_pc_beat` breaker. |
| T7 | `CONVERGED` | `BUILDING` | Builder lane health OK (path **UNVERIFIED**). One branch `A`. |
| T8 | `FORKED` | `BUILDING` | Builder lane health OK. Branches `A` and `B`. |
| T9 | `CONVERGED`, `FORKED` | `DEAD` | Builder lane health fails 3 consecutive probes. PARTYCHAT carries the risk "OSError 22 on every cycle for hours". |
| T10 | `BUILDING` | `GATED` | Every enqueued build has returned, with a commit or a recorded build failure. |
| T11 | `BUILDING` | `DEAD` | The BUILDING token cap is hit. |
| T12 | `GATED` | `LANDED` | A winner by lexicographic `(gate, smoke, fals)` then smaller `diff`, merged, **and** `[ANCHOR 3/3]` (A1 gate passes, A2 falsifier passes on HEAD, A3 falsifier fails on HEAD^). |
| T13 | `GATED` | `DISCUSS` | No build scores `gate=1 fals=1`, **and** `retries == 0`. Then set `retries = 1`. |
| T14 | `GATED` | `DEAD` | No build qualifies and `retries == 1`, **or** a merge happened but anchors stayed below 3. In the second case the merge is reverted and the revert commit is recorded. |
| T15 | `LANDED` | `MINED` | Always. The referee posts loser hunks absent from the winner, plus `DUP` hunks. The single-build case posts zero hunks. |
| T16 | `MINED` | `REDTEAM` | Always. |
| T17 | `REDTEAM` | `CLOSED` | Every anon `OBJECT` with a repro was re-run by the carrier. Each confirmed finding has spawned a child gap row citing this session id. |
| T18 | `REDTEAM` | `CLOSED` | The REDTEAM token cap is hit. The partial wave is recorded as `redteam=partial` in DONE. This is not `DEAD`, because the fix already landed and anchored. |
| T19 | any non-terminal | `DEAD` | The total USD cap is hit (`spend >= budget`). DONE is still written (see D2, Part 3). |

**Terminal states.** `CLOSED`, `DEAD`, `VOID`, `REFUSED`. Every terminal writes `DONE` and then banks (Part 3, `main`). `LANDED` is **not** terminal. A fix without red-team is not closed.

**Positive path:** `OPEN -> DISCUSS -> FORKED -> BUILDING -> GATED -> LANDED -> MINED -> REDTEAM -> CLOSED`.

**Negative paths (each is an audit violation):**
- `DISCUSS -> LANDED`. This skips the build and the gate. No row in the table allows it.
- `GATED -> LANDED` with `[ANCHOR 2/3]`. This is the S4 rule: "Dropping it to 0 does NOT win".
- `GATED -> DISCUSS` a second time. `retries` is capped at 1.
- A `[STATE ...]` row with `actor != "ref"`.

### 2.3 The beat inside every model-facing phase

This sequence is the same in `DISCUSS`, the builds, and `REDTEAM`. It is the dungeon beat with the verdict moved from dice to bytes.

1. Compute the eligible trips: under budget, not the author of post `n-1`.
2. Pick the speaker: `eligible[int(sha256(f"{tip}:{thread}:{n}").hexdigest(),16) % len(eligible)]`.
3. Write `roll_committed` before the call. This is the dungeon law, `dungeon.py:11` *(pc)* "the roll is committed BEFORE the actor speaks, and the actor never sees it".
4. Call the model. Lint the reply. Append the row.
5. If the post is `[VERIFY >>N]` or `[OBJECT >>N]` and names a scroll id, the referee runs that scroll's check and appends a ref `check` row.

**Negative example taken from the shipped bytes.** `dungeon.py::_forced_audit_beat` tells the actor its roll ("The carrier rolled your audit: d20={r}+..."). That breaks the module's own `:11` law. In the merge, prompts never contain `roll_value`.

---

## 3. THE CARRIER MERGE (wire, don't build)

**Defects found in the bytes, fixed at merge time** (cited once here and referenced below):

| id | Defect | Bytes |
|---|---|---|
| D1 | Retry usage is undercounted. The loop runs up to 3 calls, but only the last response's usage is banked. | `dungeon.py::_paid`: `for attempt in range(3):` ... then, after the loop, `usage = resp.get("usage", {})` |
| D2 | A budget hit in S0/S1 raises before DONE is written, so the bank is skipped. | `dungeon.py::_paid`: `raise SystemExit(f"DUNGEON: budget ${self.budget} hit at {tag}")`. The bank block in `main` runs only after `d.play()` returns. |
| D3 | Same-second dir collision (dungeon) | `dungeon.py::__init__`: `self.dir.mkdir(parents=True, exist_ok=True)` with no sequence loop. Tavern fixed this class ("SAME-SECOND COLLISION FIX", `tavern.py::Run.__init__`). |
| D4 | Dead reasoning fallback name (tavern) | `tavern.py::_paid`: `.get("reasoning")`. Dungeon documents the fix: "Dead fallback name: the vendor field is "reasoning_content", not "reasoning"". |
| D5 | The GWAP intent parser is line-initial, and has no ATTACK family. | `arena_gwap.py::_speech_verb`: `if s.startswith("["):`. `_SPEECH_TAG_VERBS` lacks `"ATTACK"`. So `[ATTACK warden]` and any trailing tag parse as `"spoke"`. This is the same class dungeon fixed in `extract_tag` (a02#0) but not in arena_gwap. |
| D6 | The GWAP kind sniff would misfile party dirs. | `arena_gwap.py::actor_payloads`: `kind = "dungeon" if run_dir.name.startswith("dnd") else "tavern"`. A `party_*` dir would bank as tavern. |
| D7 | Unused code in tavern | `tavern.py:30` *(pc)* `import time`. `tavern.py:40` *(pc)* `ESC_BRAWL = 18` is never read, because `play` uses `self.heat`. |

### 3.1 From `tools/tavern.py`

| Symbol | Verdict | Wiring into `tools/partychat.py` |
|---|---|---|
| `LAWS` | **REUSE + extend** | Prepended to every party system prompt. Two lines are appended: the tag-first rule and "Never write [STATE], [SCORE], [ANCHOR]". |
| `TEMPER`, `ESC_BRAWL` | **DROP** | Temper is judge-scored. ESC_BRAWL is dead (D7). |
| `_roll` | **DROP** | Duplicates `dungeon.py::roll` with the same formula. Keep the single dungeon copy. |
| `Run.__init__` dir allocator (seq loop) | **REUSE, lift to `alloc_dir(kind, stamp)`** | This also fixes D3 for dungeon. The rest of `__init__` (the pressure and threshold math) is dropped. |
| `Run.row` | **REUSE pattern** | Replaced by `append_row`, which adds `n`, `prev`, and `hash`. The `play.md` render branch is kept as `render_md`. |
| `Run._paid` | **DROP** in favor of the dungeon `_paid` | It has D4, and it lacks finish_reason banking. |
| `Run.bar_round` | **REUSE skeleton** | Becomes `discuss_beat`. It keeps the per-speaker budget check: `if self.spend >= self.budget: ... hard stop (family-box law)`. |
| `Run.judge_round` | **DROP as verdict** | A judge model may not score (PARTYCHAT 3.3). Nothing replaces it, because the promotion rule is deterministic. |
| `Run._lines` | **REUSE** | Becomes `mount()`: the transcript of party plus ref rows, clipped to 6000 chars (PARTYCHAT Part 4 context). |
| `Run.play` | **REUSE skeleton** | The loop becomes the Part 2 state driver. Its `total` recomputation from the transcript `cost_usd` is kept as the DONE spend cross-check. |
| `main` argparse | **REUSE** | Flags `--gap <id>`, `--budget-usd`, `--tip`, `--dry`, and a real `--force`. `--force` closes C3. |
| `main` FIRE-ATOMIC BANK block | **REUSE verbatim** | `from tools.arena_gwap import SessionLedger, bank as arena_bank` ... "Bank failure never fails the play run". |

### 3.2 From `tools/dungeon.py`

| Symbol | Verdict | Wiring |
|---|---|---|
| `GENESIS` (`dungeon.py:42` *(pc)*) | **REUSE** | The default `--tip`. |
| `roll` | **REUSE** | Speaker order and `roll_value` only. |
| `check_golden` | **REUSE + fix** | Becomes `pin_golden()`. It adds a frozen dict of the three expected ints and refuses on mismatch (closes C2). |
| `ROSTER` | **REUSE shape, move to config** | Loaded from `configs/party_roster.json` (**NEW**). `family` is derived from `model`. T0 refuses a single-family roster (C1). |
| `REAL_SCROLLS`, `_check_links_405`, `_check_room_big`, `_check_zombie_budget` | **REUSE as seed scrolls; GENERALIZE the mechanism** | The three functions become three rows of declarative check kinds (Part 4). Hardcoded claims like `n == 405` move into data. |
| `strip_and_cap` | **REUSE** | `cap=150`. |
| `TAG_RE`, `extract_tag` | **REUSE in arena_gwap (fixes D5)** | Party lint uses PARTYCHAT's stricter leading-tag regex. `extract_tag` is imported by `arena_gwap._speech_verb` so that trailing tags in legacy dungeon rows parse. |
| `Dungeon._paid` | **REUSE + fix D1, D2** | Sums usage across attempts into `cost.attempts`. On a budget hit it returns a sentinel. The driver then writes `[STATE DEAD cap=usd]` and DONE, and does not raise. |
| `Dungeon._dm` | **REUSE as `garden()`** | Prompt: "narrate the phase change; never score; never name a family". Called on state transitions only, not per beat (Part 5 saving). |
| `Dungeon._verdict` | **SPLIT** | The quirk branches become `lint_post` (1.4). The AUDIT branch becomes `run_check`. CLAIM is kept (slot registry). ATTACK, CHECK, and persuade are dropped. |
| `_pc_beat` | **REUSE** | Becomes `discuss_beat`. It includes the 3-strike void breaker (T6). |
| `_warden_beat` | **DROP** | The adversary is the gate, not a monster. |
| `_tail` | **REUSE** | The gardener's context. |
| `s0` | **REUSE shape** | Becomes `open_session`. The omen roll is replaced by the falsifier-on-base run (T0 and T1). |
| `_forced_audit_beat` | **REUSE shape** | Becomes `audit_scrolls`. It runs every scroll check before the first party post. No model call is needed here. |
| `s1` loop | **REUSE** | Becomes the `DISCUSS` loop, with the bump limit as `S1_BEATS_CAP`'s analog. |
| `SCENES`, `_enemy_sheet`, `_wyrm_regrowth` | **DROP text, keep idea** | Regrowth is not ported. Unresolved PHANTOM scrolls are instead listed in every mount (pressure without HP). |
| `_beat_outcome`, `_mimic_wipe` | **REUSE concept in `mine()`** | A losing build's hunks that no `VERIFY` row backs are dropped from the mined pool. That is the "Load-Failure Wipe" applied to hunks. |
| `_find_scroll` | **REUSE** | A casefolded scroll lookup for `[VERIFY ... s2]`. |
| `_phantom_count` | **REUSE** | Becomes `open_phantoms`, written into DONE. |
| `_grade` | **DROP** | Replaced by `score_build` and `anchor_root`. |
| `campaign` | **REUSE skeleton** | The phase driver plus the DONE writer. Its DONE keys (`verdict, spend_usd, audits, voided_readbacks, voided_calls`) are kept, plus the Part 4 keys. |
| `main` bank block | **REUSE verbatim** | (same as tavern) |

### 3.3 From `tools/hermes_burn.py`, `tools/arena_gwap.py`, and PARTYCHAT_spec

| Symbol | Verdict | Note |
|---|---|---|
| `_bank, _call, _hermes_key, _now, PRICING` | **REUSE** | Same import line as `dungeon.py:38` *(pc)*. Bank id `f"{sid}_n{n}_{trip}"` follows the BURN-ID LAW. |
| `arena_gwap.bank`, `SessionLedger`, `verify_chain` | **REUSE unchanged** | |
| `arena_gwap.actor_payloads` | **PATCH (small)** | Add `kind = "party"` for `party_` dirs (D6). Intent comes from the party tag via the leading regex. Report comes from the matching ref `check` or `verdict` row (cop). Use `extract_tag` (D5). |
| PARTYCHAT Part 5 `check`, `metrics`, `rhash` | **REUSE as-is, extended** | Lives inside `tools/partychat.py`. Two extensions: (a) ref-only fields `check` and `verdict` on party rows count as `overclaim`; (b) transitions not in table 2.2 count as `badstate`. Whether `mag/party_chat.py` was ever landed is **UNVERIFIED**. If it was, import from it instead of copying. |

### 3.4 Genuinely new in `tools/partychat.py`

| Function | Role |
|---|---|
| `import_gap` | Gap row to `sheet.json` (Part 4) |
| `append_row` | Hash-chained append |
| `lint_post` | |
| `promote` | |
| `enqueue_build` | Builder lane, **UNVERIFIED** interface |
| `score_build` | Gate, **UNVERIFIED** path |
| `run_check` | Declarative scrolls |
| `anchor_root` | A1-A3 |
| `mine` | |
| `redteam` | |
| `write_done` | |
| `audit` | |

Everything else is reused.

---

## 4. THE GAP-TO-QUEST WIRE

### 4.1 Input row (the register path is UNVERIFIED; required fields follow PARTYCHAT 3.2)

```json
{"gap_id":"gap042","title":"store wiped on load-or-default RMW",
 "target_paths":["mag/store.py"],
 "falsifier":{"cmd":"python -m pytest tests/test_store.py::test_rmw_no_wipe -q","pass_exit":0},
 "claims":[{"id":"s1","claim":"LINKS.jsonl holds exactly 405 rows","kind":"row_count","path":"watch/inbox/LINKS.jsonl","expect":405}]}
```

### 4.2 The REAL_SCROLLS pattern, extended from claims to problems

`dungeon.py` hardcodes one function per claim, for example `_check_links_405`. The merge replaces functions with **whitelisted check kinds**. A new problem therefore needs a data row, not new code.

| kind | Semantics (carrier-run, zero tokens) | Generalizes |
|---|---|---|
| `row_count` | Count lines in `path`, compare to `expect` | `_check_links_405` |
| `size_gt` | `stat().st_size > expect` | `_check_room_big` |
| `substring_count` | `read_text().count(arg) >= expect` | `_check_zombie_budget` |
| `file_exists` | `Path(path).is_file() == expect` | (new) |
| `falsifier` | Run the gap row's `falsifier.cmd` in the builder sandbox and compare the exit code | (new; the Wyrm) |

**Safety law.** Commands come **only** from the gap row, never from a post body. `cmd_sha` (the sha256 of the command string) is stored in every `check` row, so a replay can prove the same command ran. Every check catches `OSError` into `true=false, detail="check failed: ..."`. That matches `_verdict`'s `except OSError`, which `_forced_audit_beat` lacks: it calls `REAL_SCROLLS[0]["check"]()` unguarded.

**The sheet that is generated** (it replaces `S1_SHEET` in prompts):

```
SCENE (gap042): store wiped on load-or-default RMW.
THE WYRM: falsifier `<cmd>` FAILS on base <sha8> (checked n=2).
TARGETS: mag/store.py. CLAIM a target before you PROPOSE on it.
SCROLLS: s1 "LINKS.jsonl holds exactly 405 rows" -> PHANTOM (391).
WIN: three root anchors (gate, falsifier passes, falsifier fails on parent).
```

**Positive import.** The falsifier exits 1 on base and every claim has a whitelisted kind. Result: T0 to `OPEN`.

**Negative imports:**
- The row has no `falsifier`. Result: `REFUSED`. "A build nobody can fail is not a build" (PARTYCHAT 3.3).
- The falsifier exits 0 on base. Result: `REFUSED (no-wyrm)`. Either the gap is already fixed, or the falsifier tests nothing.
- A post says `[VERIFY >>3 rm -rf watch/]`. The text names no scroll id, so `_find_scroll` returns `("","")`. Nothing executes, and the post is `void:unknown-scroll`.

### 4.3 Work product: what a session banks as a real artifact

An artifact is a byte that exists outside the transcript and that a seat can re-check without a model. Every terminal session writes `DONE` with these keys. Each value must resolve to such a byte.

| DONE key | Real artifact | Banked even if `DEAD`? |
|---|---|---|
| `landed` | `{"commit":sha,"branch":"party/<sid>/A","parent":sha}` on main | no (`LANDED` only) |
| `anchors` | three `check` row refs `[n_a1, n_a2, n_a3]` with `cmd_sha` | no |
| `audits` | every scroll result `{scroll, claim, true, detail}`. This is the dungeon `self.audits` shape. A PHANTOM found is a real catch. | **yes** |
| `mined` | path `mined.jsonl`: loser hunks plus `DUP` hunks | if `MINED` was reached |
| `children` | gap ids opened by red-team or by PHANTOM scrolls | **yes** |
| `transcript_sha` | sha256 of `transcript.jsonl`. This is the `replay_tape_ref` that arena_gwap already computes. | **yes** |
| `spend`, `tokens`, `attempts`, `voided_calls` | cost receipts (Part 5) | **yes** |

**Not artifacts (negative):** `play.md`, gardener narration, `roll_value`, and any party post's claim that something works. Those are reports. The bytes are the `check` rows.

---

## 5. THE COST MODEL AND THE FALSIFIER

### 5.1 The only measured dollar anchor, with its conditions

**Number.** Two dungeon S1 sessions reported `spend_usd` of 0.0731 and 0.057, each cut at about 8 beats.

**Provenance.** This comes from SEASON_design's reasoning channel. The DONE files themselves are not in my evidence. **UNVERIFIED secondhand.**

**Instrument.** `dungeon.py::_paid` cost math, `pin * cin + pout * cout`.

**Moment.** The 2026-10-03 to 2026-10-04 runs. The exact stamps are UNVERIFIED.

**Context:**
- S1 only.
- Two calls per PC beat: the PC call plus `_dm`.
- **Biased low by D1.** Only the last of up to three attempts is counted.

**Implied rate.** About $0.007 to $0.009 per dungeon beat, which is two calls.

### 5.2 Per merged session (token caps are binding; dollars are derived)

| Line item | Calls | Tokens (cap) | Basis |
|---|---|---|---|
| OPEN: falsifier on base and scroll checks | 0 model | 0 | carrier bytes |
| DISCUSS: party posts | ≤40 | 120,000 | PARTYCHAT bump limit, about 3k per post (6000-char mount, body ≤150 words) |
| Gardener narration | ≤8 (state changes only) | inside DISCUSS cap, about 2k each | Replaces `_dm` per beat. This halves the calls against dungeon's 2 per beat. |
| BUILDING | ≤2 | 120,000 | 2 builds at 60k |
| GATED and anchors | 0 model | 0 | gate plus 3 checks |
| REDTEAM | ≤7 | 60,000 | PARTYCHAT 7 chairs at about 8k |
| **Session cap** | **≤57** | **300,000** | hard cut, T5, T11, T18, T19 |

**Dollar ceiling formula:** `usd ≤ Σ_calls (pin*cin + pout*cout)` using `PRICING`. The `PRICING` values are **UNVERIFIED** (not in evidence).

**Secondhand estimate.** A full 57-call session lands near **$0.20 to $0.26**, extrapolated from 5.1 at about $0.0035 to $0.0045 per call. This assumes the same model mix and mount size, and it is **UNVERIFIED** until the first session's `cost` column replaces it.

**Default `--budget-usd` 4.0.** This follows `dungeon.py::main` `default=4.0`. It is a safety rail, roughly 15x the estimate, not a target.

**Positive example (cost accounting):** a post reports `"cost":{"prompt_tokens":2810,"completion_tokens":96,"attempts":2,...}`. Tokens are summed across both attempts (D1 fixed).

**Negative example:** `attempts:3` with the usage of the third attempt only. That is the shipped `dungeon.py::_paid` behavior. The audit flags `cost.attempts > 1` rows whose usage equals a single call's usage as `estimated=true` at best.

### 5.3 The falsifier: merged sessions vs the current non-play pipeline

**Baseline arm.** The estate's existing path for a gap row: one strongest seat drafts, the builder lane builds, the workflow gate scores. These paths are **UNVERIFIED**. The baseline seat is the single model that the routing rule names the "strongest free" (NPC_RACTOR `:58` *(pc)*, as quoted in PARTYCHAT 5.1).

**Pre-registration (written before the first live session):**

| Element | Fixed value |
|---|---|
| Sample | 20 gap rows that pass T0. Arm assignment is **paired**: every row runs in both arms on isolated branches from the same base commit. Neither arm lands until both are terminal. Then the A3 winner lands. |
| Equalized | Same base commit, same 300k token cap, same gate, same falsifier, same anchors A1-A3, same `--budget-usd`. |
| Instrument | Merged arm: `python tools/partychat.py audit <run>/transcript.jsonl` (exit 0 required, else the pair is void). Baseline: lane trail timestamps (**UNVERIFIED** path) plus the same `anchor_root` run on its branch. |
| Moment | Scored once, after all 40 runs are terminal. Never mid-sample, because of the moving-tree law (`arena_gwap.py::status` docstring: "any row/session count without a moment stamp is stale on arrival"). |
| Primary metric | **TTAF**: wall seconds from `OPEN` to `[ANCHOR 3/3]`, censored at the cap. Also reported as tokens per anchored fix. |

**Kill table.** Merged sessions are falsified as faster problem-solvers if **any** of these holds:

| Kill | Condition |
|---|---|
| F1 | Anchored fixes, merged arm, are ≤ the baseline arm's count over the 20 pairs. |
| F2 | Median TTAF of pairs where **both** arms anchored is merged ≥ baseline. |
| F3 | Tokens per anchored fix, merged, exceed 2x the baseline. |
| F4 | Fewer than 5 pairs reach any terminal state other than `REFUSED` or `VOID`. The test is then uninformative. Fix the carrier, not the metric. |

**Survives (positive):** merged anchors 9 of 20 against baseline 5. Median TTAF is 41 min against 63. Tokens per fix are 1.6x.

**Dies (negative):** merged anchors 6 against 6. That alone trips F1. It also dies if the merged arm wins only because the baseline hit `T9` (builder lane down) more often. The lane health log is attributed per pair, and those pairs are voided in both arms.

### 5.4 This deliverable's own falsifier

This spec is wrong if any of these is observed:
1. A hand-written `OPEN -> ... -> CLOSED` session in this schema fails `audit` without a real violation. Run this before the first live session.
2. `audit` passes a session containing a transition absent from table 2.2.
3. `audit` passes a session containing a party row carrying `check` or `verdict`.
4. Any `DONE` value listed in 4.3 does not resolve to a byte a seat can re-check without a model.
5. The patched `arena_gwap.actor_payloads` scores a fixture `[VERIFY >>3 s1]` post plus its `check` ref row as a disagreement.
6. A budget hit leaves a run dir with no `DONE` (D2 not fixed).
