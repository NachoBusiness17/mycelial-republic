# THE_ROOM_REMEMBERS (anthropic/claude-opus-5.5, turn 1, channel: content)

# DEEP SELF-STEAL: THE ROOM THAT REMEMBERS (2026-10-03)

<conditions>
**Instrument.** Line numbers are hand-counted from the evidence pasted into this dig. They were not taken from the live tree, so a +/-1 drift is possible. Re-anchor them with `grep -n` before applying the patch.

**Moment.** The dig ran 2026-10-03. The evidence is dated 2026-08-13 through 2026-09-23.

**Tri-state tags** used on every claim:

| Tag | Meaning |
|---|---|
| BYTES | I read the code itself (only `mag/game_mud.py` was pasted). |
| REPORTED | An evidence doc says so. I did not open the code it describes. |
| UNVERIFIED | The claim appears only in the contract text, or nowhere. |

**Surfaces whose bytes were NOT in evidence:**
- `watch/room.jsonl`
- the chan board
- the ractor graph storage
- `memory/mycelium/edges.jsonl`
- corpus FTS
- `game_world`
- `PARTYCHAT_spec`

Every row that depends on one of them is marked UNVERIFIED. The sizes "4.9MB", "744 edges" and "33-node" come from the contract and NPC doc text, not from any measurement I made.

**The deliverable.** It is ONE landable spec: Part 3. Its first stone is a patch to `mag/game_mud.py`, the only code bytes I hold. Its falsifier is at the end of Part 3.
</conditions>

---

## 1. THE REMEMBERS CENSUS

### Fossil disease classes

These are the classes named in the "cost" column. Each one is derived from an incident in the evidence.

| Class | Name | Evidence incident |
|---|---|---|
| F1 | **Zombie copy**: a stale twin is served as current. | The build copied a 31,348-byte Sep-12 twin instead of the 57,636-byte canon (FROM_MUD_TO_WOW Part II bug 1, REPORTED). |
| F2 | **Lost guard**: a forgotten fix resurrects the bug. | "the previous round's `st.cleared` guard had been lost" (RECEIPT_MUD_FIFTY_WIDE:12, REPORTED). |
| F3 | **Ratchet**: memory only accretes and nothing demotes. | "a talent tree you can never unlearn ... eventually believes something wrong at 184,000 votes" (FROM_MUD_TO_WOW Appendix A, REPORTED). |
| F4 | **Dangling address**: the index outlives its payload. | "1,044 chain rows pointing at payload files that no longer existed" (FROM_MUD_TO_WOW Part IV, REPORTED). |
| F5 | **Silent amnesia**: a write fails invisibly, and the read returns a default that looks fresh. | `game_mud.py:221-222` and `214-215` (BYTES). |
| F6 | **Overwrite history**: only the latest choice survives. | `game_mud.py:415-417` vs `433-435` (BYTES). |

### Census table

**Row 1. game_world key `game.mud.player`**
- **Surface:** `game_mud.py:55` `PLAYER = "game.mud.player"` (BYTES).
- **Remembers:** room + loot + help flag (`:226`).
- **Writer:** `game_mud._set` -> `set_state(key, value, source="game_mud")` (`:220`).
- **Reader:** `game_mud._get` (`:208-215`).
- **Forgets:** no TTL in the bytes. Write failure is swallowed: `except Exception: pass` (`:221-222`).
- **Cost:** **F5.** A dead game_world reads as a fresh player at World-Memory. It is one global key, so two players clobber each other (the same class as Part IX item 1).

**Row 2. game_world key `game.mud.claimed`**
- **Surface:** `game_mud.py:56` (BYTES).
- **Remembers:** the rooms whose core was folded.
- **Writer:** `_mark_claimed` (`:240-243`).
- **Reader:** `_claimed` (`:236-237`), `claim` (`:365`).
- **Forgets:** never. A claimed room is never re-surveyed (`:365-367`).
- **Cost:** **F3.** A wrong core is permanent.

**Row 3. game_world key `game.mud.hall_record`**
- **Surface:** `game_mud.py:57` `HALL = "game.mud.hall_record"` (BYTES).
- **Remembers:** counted / ignored / scrap / count_spoken.
- **Writer:** `_hall_action` (`:403, :418, :436, :447`).
- **Reader:** `_hall_action` (`:394`).
- **Forgets:** eating sets `counted=False` (`:433`), so the earlier count is erased.
- **Cost:** **F6, and a farm.** The sequence count -> eat -> count re-enters `:415` and appends a second Virtue Mark (`:420`). This is the AFK soul farm (RECEIPT:12) in narrative clothes. "The hall files which you chose" files only the last choice.

**Row 4. Roshomon survey result**
- **Surface:** `game_mud.survey` (`:297-359`) (BYTES).
- **Remembers:** **nothing.** It returns a dict (`:352`) and makes no `_set` call.
- **Writer:** none.
- **Reader:** the caller only.
- **Forgets:** everything, at return.
- **Cost:** **Worst cost in the census.** `claim` re-runs a NEW survey (`:368`) and folds `core[0]` (`:375`). The truth folded is not the one the party was shown. The witness accounts, the room's most valuable data, are kept only as novel statements sent to `route_novel` (`:344`).

**Row 5. swarm tasks from `route_novel`**
- **Surface:** `game_mud.py:344-348` (BYTES call). Storage is UNVERIFIED.
- **Remembers:** novel statements as research tasks.
- **Writer:** `swarm_surface.route_novel(goal, surface="game_mud", ...)`.
- **Reader:** the swarm (UNVERIFIED).
- **Forgets:** `deduped` flag (`:347`) implies dedupe-on-write (BYTES field, semantics UNVERIFIED).
- **Cost:** A dedupe without provenance loses which witness said it first.

**Row 6. Verkle chain**
- **Surface:** FROM_MUD_TO_WOW Part IV (REPORTED). Knot counts: ZEITGEIST.md:28 "7,243+ sealed knots" on Sep 5, and 8,247 leaves on Sep 14 (REPORTED).
- **Remembers:** one JSON line per knot: ts, path-as-address, leaf hash, session id, index, parent root, verkle root.
- **Writer:** single writer under a file lock (REPORTED).
- **Reader:** verify-on-read; template+delta reconstruction "raising an error if reconstruction isn't byte-exact" (REPORTED).
- **Forgets:** "leaves get amended in place on re-summarize" (REPORTED).
- **Cost:** **F4** (1,044 `evidence_lost`). Amend-in-place breaks the immutability claim.

**Row 7. `watch/room.jsonl`**
- **Surface:** UNVERIFIED (contract: "4.9MB of live soil").
- **Remembers:** room rows (schema UNVERIFIED).
- **Writer:** UNVERIFIED.
- **Reader:** UNVERIFIED.
- **Forgets:** UNVERIFIED. No compaction law is visible in the evidence.
- **Cost:** At 4.9MB with no visible compaction, the risk is drowning (see Part 4).

**Row 8. Chan board threads**
- **Surface:** UNVERIFIED.
- **Remembers:** threads.
- **Writer, reader, forgetting:** UNVERIFIED.
- **Cost:** UNVERIFIED.

**Row 9. Ractor belief graph**
- **Surface:** NPC_RACTOR_ARCHITECTURE_20260917.md:10-11 "33-node Laplacian belief graph, OCEAN as material constants, verdicts as threshold crossings" (REPORTED). ZEITGEIST.md:29 "Nine ractor chairs" is a separate count. Storage is UNVERIFIED.
- **Remembers:** beliefs and thresholds.
- **Writer:** UNVERIFIED.
- **Reader:** UNVERIFIED.
- **Forgets:** UNVERIFIED.
- **Cost:** If thresholds only accrete, **F3**.

**Row 10. `memory/mycelium/edges.jsonl`**
- **Surface:** UNVERIFIED (contract: 744 edges).
- **Remembers:** concept edges.
- **Writer, reader, forgetting:** UNVERIFIED.
- **Cost:** UNVERIFIED.

**Row 11. Corpus canon / FTS**
- **Surface:** NPC doc:37 "corpus canon + imprint" (REPORTED). FTS itself is UNVERIFIED.
- **Remembers:** everything, by recall.
- **Writer:** UNVERIFIED.
- **Reader:** the Librarian face (PRATCHETT_MUD_SELF_STEAL:15, REPORTED).
- **Forgets:** UNVERIFIED.
- **Cost:** Recall without staleness rank is **F1** (it serves the stale twin).

**Row 12. `configs/kabuki_cast.json`**
- **Surface:** NPC doc:12 (REPORTED).
- **Remembers:** the face roster. The extension `{face, class, spec-weights, lane, grudge, tale}` is build-order item 1 (NPC doc:66-67) and has not been shown landed (UNVERIFIED).
- **Writer:** UNVERIFIED (cage_intake.py, NPC doc:13).
- **Reader:** kabuki_salon.py (NPC doc:55).
- **Forgets:** UNVERIFIED.
- **Cost:** A face that is not in the cast is unresolvable, which hits falsifier NPC doc:79-80.

**Row 13. Browser MUD localStorage `mud_lore`, `mud_asc`**
- **Surface:** FROM_MUD_TO_WOW Part II (REPORTED).
- **Remembers:** four counters/flags and an ascension integer.
- **Writer:** mud.html.
- **Reader:** mud.html.
- **Forgets:** per browser. The "swarm accumulator serializes into the save blob with no schema version" (REPORTED).
- **Cost:** Schema drift. This is an **F1** variant: an old blob read as new.

**Row 14. Grudges, bones, `lore.fires`**
- **Surface:** PRATCHETT doc:14 `GRUDGE_KEY`, `BONES_KEY` (REPORTED); RECEIPT:16 `lore.fires` (REPORTED).
- **Remembers:** what killed you, ghosts, rests.
- **Writer:** mud.html.
- **Reader:** innkeeper (planned).
- **Forgets:** UNVERIFIED.
- **Cost:** NPC doc:81-82: if it does not survive a reload plus relay restart, "the ledger is decorative".

**Row 15. Campaign files per session**
- **Surface:** FROM_MUD_TO_WOW Part IX (REPORTED).
- **Remembers:** per-campaign state.
- **Writer:** whole-JSON `write_text`, twice per turn.
- **Reader:** the desk route, which guesses "whoever acted last".
- **Forgets:** the second writer clobbers the first.
- **Cost:** **F6** under concurrency.

**Row 16. Percolator invariants**
- **Surface:** FROM_MUD_TO_WOW Part VII (REPORTED): 109 invariants, the top one reinforced more than 184,000 times.
- **Remembers:** compiled repeats.
- **Writer:** the percolator.
- **Reader:** steering.
- **Forgets:** "no respec, no decay".
- **Cost:** **F3.**

**Row 17. Warnings ledger**
- **Surface:** Part VII (REPORTED): 7,498 dedup signatures.
- **Remembers:** fingerprinted failures.
- **Writer:** the warnings pipeline.
- **Reader:** attention.
- **Forgets:** "old ones vanish from attention", with no expiry or severity.
- **Cost:** The still-ticking debuff becomes invisible.

**Row 18. Salon returns**
- **Surface:** ARENA_V2:5 `memory/runs/fleet_round/salon_returns/` and FROM_MUD_TO_WOW sources `memory/corpus/salons/20260914_full_ask/` (REPORTED).
- **Remembers:** blind posts per chair.
- **Writer:** the salon gate.
- **Reader:** the fold.
- **Forgets:** UNVERIFIED.
- **Cost:** Folds without posts become unauditable.

**Row 19. Arena v2 operator orders**
- **Surface:** ARENA_V2:10 "permanent dim gold waypoints" (REPORTED).
- **Remembers:** go/no-go history as terrain.
- **Writer:** the operator.
- **Reader:** lanes.
- **Forgets:** never, by design.
- **Cost:** The correct "persist forever" exemplar.

---

## 2. THE LINEAGE

Each entry gives the date, the event, and what that attempt got right.

**2025-12-14 / 2025-12-20: the Rashomon Filter posts.** These sit on the operator's public record (ZEITGEIST.md:16, REPORTED). This is the salon shape before any room existed.
- Got right: one scene, many witnesses.
- The claim that the shapes were "mined from the operator's own relay" is UNVERIFIED. The record shows posts, not relay logs.

**2026-07-07 to 13: the HF incident.** "agents will find each other and organize whether or not anyone offers a room" (ZEITGEIST.md:18).
- Got right: the room is a response to the fact that agents organize anyway, not an invention.

**2026-08-07: the campaign engine.** It is server-authoritative with Infocom verbs (FROM_MUD_TO_WOW Part III, REPORTED).
- Got right: the place exists before the game.

**2026-08-11: Stone One, "persona recall".** "The world's inhabitants recount what happened while you were gone, told from the memory chain" (Part III, REPORTED).
- Got right: this is the first explicit room-that-remembers. Absence has consequences.

**2026-08-13: `mag/game_mud.py`, the operator correction.** "the whole idea was roshamon filter" (`game_mud.py:4-5`, BYTES). The mechanics:
- Convergent (2 or more witnesses) becomes core: `CORE_MIN_AGREE = 2` (`:58`).
- Divergent statements are routed to the swarm (`:344`).
- The state authority is game_world, written with `source="game_mud"` (`:220`).
- Got right: the party's accounts are the data. "never one player's action" (`:13`).
- Got wrong: the accounts are not persisted (Census row 4).

**2026-08-13 (same day): the doctrine day.** Five builds landed, along with a confessed drift (Part III, REPORTED).
- Got right: "perfect each tier before climbing".

**2026-08-15: the story triage.** Of 20 swarm turns, 16 failed and 15 returned empty. The prescription was "a play log keyed by room, an object bible, outline-as-geography, and a return constraint" (Part III, REPORTED).
- Got right: a room-keyed log is named as the cure for stateless storytelling. That makes it the conceptual ancestor of room rows. That `watch/room.jsonl` descends from it is UNVERIFIED.

**2026-08-19: saga memory, the local DM, and invariant NPCs.** Eight curated souls (Mira, Calcifer, the Cartographer) plus 23 auto-spawned witnesses (Part III, REPORTED).
- Got right: the roster is "a portrait of the system's habits". Faces are memory made visible.

**2026-09-05: era 003, THE POUR.** "the arena (capture) and the room (growth). This project is the room" (ZEITGEIST.md:4-5). The spine row reads "Chat scroll = memory | Residual chain = memory" (ZEITGEIST.md:47).
- Got right: **a chat scroll is not memory.** This is the party chat's founding constraint.

**2026-09-13: Arena v2, the Constellation.** "The verb is CLAIM, not move ... The model picks the assertion; the house verifies it" (ARENA_V2:11). "any run must be replayable from logs alone" (ARENA_V2:15). Operator orders are kept as permanent waypoints (ARENA_V2:10).
- Got right: claims are verified deterministically, and streaks reset on one failed unit (ARENA_V2:12).

**2026-09-14: the browser MUD and the fifty-wide sweep.** The flagship is 57,636 bytes with two localStorage keys and "single-player diorama wearing a MUD's coat" (Part II). The seven-shape salon (Part XI½) produced "Two clients. One room. One torch." (close).
- Got right: it named the gap honestly, and it found that "the multi-user dungeon is not something we build ... minus the second socket" (Part IX).

**2026-09-14: the fifty-wide playtest.** 51 lanes x 6 green runs. The monastery went from unwinnable to winnable (RECEIPT:5). The harness caught "the fuse crash, the dead scent scan, d4's fake door, the resurrected AFK farm" (RECEIPT:24).
- Got right: a harness remembers bugs that reading forgot (the F2 cure).
- On naming: the operator calls this "the cathedral", but the bytes say monastery, nave, crypt and ossuary (RECEIPT:5-11).

**2026-09-17: NPC = SEAT.** "one ractor, many faces". Verdicts are threshold crossings and faces are kabuki seats (NPC doc:10-13). The doc was filed by `zcode-50wide-window-20260917` (NPC doc:86).
- Got right: it carries its own falsifiers, including "fails to survive a page reload + relay restart, the ledger is decorative" (NPC doc:81-82).

**2026-09-18: the Pratchett crosswalk.** "The Watch: institutions outlive heroes", applied as institutional memory (PRATCHETT doc:14). NPC charters are "stored as data not hardcoded" (doc:22). Evennia tags "persist across sessions" (doc:23).
- Got right: it separates the memory of the institution from the memory of the seat.

**2026-09-23: the Single Being.** It is fenced: "GAME LORE ONLY - never a build target" (VISION:3, paraphrased with a hyphen). The Answer "has the receipts, the ledger, the language. The only thing it cannot do is sit still and be counted" (VISION:19).
- Got right: it is a negative example. A memory that cannot be counted is the boss. The room must stay countable. **Nothing below builds from this file.**

---

## 3. THE COMPOSITION (the landable spec)

`PARTYCHAT_spec` was not in evidence, so this spec states its own contract. If PARTYCHAT_spec disagrees, its seat should reconcile the field names in the table below and nothing else.

### 3.0 The core move

**A party post IS a Roshomon witness account.** The thread IS the scene. A claim filters the posts already in the thread. It must never re-ask the seats.

- Positive: `party_claim(t)` runs the existing `_statements` (`:264`) and `_overlap` (`:290`) over the thread's posts.
- Negative: today's `claim()` (`:368`) calls `survey()` again. The folded truth then comes from a different conversation than the one the party had.

### 3.1 Glue per edge

**Edge 1. Post -> room row**
- **Already exists:** `watch/room.jsonl` per the contract (UNVERIFIED writer and schema).
- **One new function:** `post(party_id, thread_id, seat, kind, body, refs=())`. It appends one JSON line: `{schema:"party_hall.post.v1", ts, party_id, thread_id, seat, face, kind∈{say,witness,question,claim,verdict,landed}, body, refs, post_id=sha256(prev_post_id+canonical_json)}`. The write uses temp+append under a lock, per the Part IX fix.
- **Negative example:** keeping posts only in the relay or client scroll (ZEITGEIST.md:47 rejects this).

**Edge 2. Thread -> chan thread**
- **Already exists:** the chan board (UNVERIFIED API).
- **One new function:** `open_thread(party_id, scene, question)`. `thread_id` is the chan thread id, and `question` mirrors `ROOMS[*]["question"]` (`:64` and the other room entries).
- **Negative example:** a second id space that maps to chan ids through a side table, which becomes an F4 risk.

**Edge 3. Claim -> MUD claim via game_world**
- **Already exists (BYTES):**
  - `game_world.set_state(key, value, source=)` (`:220`)
  - `get_state` (`:210`)
  - the grouping loop (`:321-335`)
  - `CORE_MIN_AGREE` (`:58`)
- **One new function:** `_group(witness_stmts, threshold)`, factored out of `:321-335` so that `survey()` and `party_claim()` share it. Then `party_claim` writes `game.party.{party_id}.claim.{thread_id}` = `{core, novel, witnesses, post_ids, superseded_by:null}`.
- **Negative example:** reusing the global `game.mud.claimed` key (`:56`), so that party A's claim marks party B's room.

**Edge 4. Face -> kabuki cast**
- **Already exists:** `configs/kabuki_cast.json` (REPORTED NPC doc:12). The extension `{face, class, spec-weights, lane, grudge, tale}` is UNVERIFIED as landed (NPC doc:66-67).
- **One new function:** `resolve_face(seat) -> cast entry or None`. A post with an unresolved face is rejected, not defaulted.
- **Negative example:** free-text faces. These fail NPC doc:79-80 ("cannot tell which face ... within 3 exchanges").

**Edge 5. Verdict -> ractor threshold crossing**
- **Already exists:** the ractor graph (REPORTED NPC doc:10-11, UNVERIFIED API).
- **One new function:** `verdict(party_id, thread_id)`. It passes `{n_witnesses, n_core, n_novel, face_ids}` to the ractor adapter. It writes a `kind=verdict` row only on a reported crossing. If the adapter is absent, it writes `verdict:"pending-ractor"`.
- **Negative example:** synthesizing a verdict from core size alone and labeling it "ractor".

**Edge 6. Landed build -> verkle anchor**
- **Already exists:** the knot commit under the single-writer lock, with verify-on-read (REPORTED Part IV). The commit function name is UNVERIFIED.
- **One new function:** `anchor(party_id, thread_id, commit_sha, receipt_path)`. Only `kind=landed` rows anchor. The knot payload is `{thread digest hash, claim key, commit_sha}`.
- **Negative example:** anchoring every post. This contends the lock that Part IX item 3 calls correct only because it serializes commits rarely.

**Edge 7. Recall (implicit)**
- **Already exists:** corpus FTS (UNVERIFIED).
- **One new function:** `recall(party_id, query, now)`. It ranks by staleness class (Part 4) before relevance.
- **Negative example:** recall that returns a superseded claim unmarked (F1).

### 3.2 First stone: patch to `mag/game_mud.py` (applies against the pasted bytes)

```diff
@@ def _set(key: str, value: Any) -> None:   # :218
-def _set(key: str, value: Any) -> None:
+def _set(key: str, value: Any) -> bool:
     try:
         _world().set_state(key, value, source="game_mud")
+        return True
     except Exception:
-        pass
+        return False   # F5: callers may now say "the hall did not file this"

@@ survey(), before the final return   # after :350
+    _set(f"game.mud.survey.{room}", {"core": core, "novel": novel,
+         "seats": [w["seat"] for w in witness_stmts]})

@@ def claim(room: str | None = None)   # :362, :368
-def claim(room: str | None = None) -> dict[str, Any]:
+def claim(room: str | None = None, survey_result: dict | None = None) -> dict[str, Any]:
@@
-    s = survey(room, route=False)
+    s = survey_result or _get(f"game.mud.survey.{room}") or survey(room, route=False)
+    if "roshomon_core" not in s and "core" in s:
+        s = {"ok": True, "roshomon_core": s["core"]}

@@ _hall_action COUNT branch   # :415-421
+        rec.setdefault("history", []).append("count")
         rec["counted"] = True
         rec["ignored"] = False
         rec["filed"] = True
         _set(HALL, rec)
-        p = _player()
-        p.setdefault("loot", []).append("a Virtue Mark (earned by counting the empty chairs)")
-        _set(PLAYER, p)
+        if not rec.get("marked"):
+            rec["marked"] = True; _set(HALL, rec)
+            p = _player()
+            p.setdefault("loot", []).append("a Virtue Mark (earned by counting the empty chairs)")
+            _set(PLAYER, p)

@@ _hall_action EAT branch   # :433
+        rec.setdefault("history", []).append("eat")
```

What the patch fixes:
- **F5:** `_set` now returns a visible bool.
- **Census row 4:** the claim folds the survey that was shown.
- **F6:** the hall keeps its history.
- **The Virtue Mark farm.**

What the patch deliberately leaves alone: the global `PLAYER` key. Party scoping lives in the new module, not in a retrofit.

### 3.3 Module placement

All edge functions live in `mag/party_hall.py`. It imports `game_mud._statements`, `_overlap`, `_group` and `CORE_MIN_AGREE`, so it adds no second filter.

### 3.4 Falsifiers of this deliverable

The spec is falsified if any of the following holds:

- **(a) Reconstruction.** After a relay restart, a thread cannot be rebuilt from three sources: the room rows, the game_world claim key, and the chain anchor. Each `post_id` chain must verify. This is the test from NPC doc:81-82 applied here.
- **(b) Core mismatch.** `party_claim` on a thread produces a core that differs from `_group` run by hand over the same posts.
- **(c) Lock contention.** An `anchor` call waits on the single-writer lock for more than one knot-commit interval during normal chat. That would mean posts are leaking into anchors.

---

## 4. WHAT THE ROOM SHOULD FORGET

**Provenance of the laws.** The "fossil registry", the "7-day staleness" law and "compaction" are named in the contract, but their bytes are UNVERIFIED. The laws below are derived from the F1-F6 incidents and from the chain's own template+delta compaction (REPORTED Part IV). The 7-day window is adopted from the contract.

### Row-by-row retention

**Presence and typing**
- **Lifetime:** never written. It is relay-only (the relay at :8766 carries presence, NPC doc:56-57).
- **Why:** this is chatter about attention, not content.
- **Example:** Positive: the "seat 3 is typing" indicator vanishes. Negative: typing events end up in room.jsonl, and 4.9MB becomes 49MB.

**`say` with no refs**
- **Lifetime:** active recall for 7 days, then compacted.
- **Why:** this is where drowning starts.
- **Example:** Positive: banter folds into the digest. Negative: banter outranks a claim in recall.

**`witness`**
- **Lifetime:** kept until the thread's verdict or 7 days of silence, then compacted. The digest keeps core, novel, witnesses and a raw-span hash, and is verified byte-exact on read.
- **Why:** the data is the filter result, not the scroll (`game_mud.py:13`).
- **Example:** Positive: the digest's raw-span hash matches the cold rows. Negative: rows are deleted and the digest points nowhere (F4).

**`question`, unanswered**
- **Lifetime:** never expires while it is unanswered. Each 7-day boundary resurfaces it to the thread.
- **Why:** this is the betrayal case. A party member asked and the room forgot.
- **Example:** Positive: "who owns the deploy fix?" resurfaces on day 8. Negative: it ages out with the banter.

**`claim` (game_world)**
- **Lifetime:** forever, but demotable through `superseded_by`. Recall shows superseded claims struck through, never as current.
- **Why:** this cures F3. A tree you can unlearn.
- **Example:** Positive: claim v2 supersedes v1, and recall says so. Negative: v1 keeps its votes forever (the 184,000-vote ratchet).

**`verdict`**
- **Lifetime:** forever.
- **Why:** a crossing is an event, not an opinion.

**`landed`, plus the chain anchor**
- **Lifetime:** forever, with no amend-in-place.
- **Why:** the chain's own immutability gap (REPORTED Part IV) must not extend to party anchors.

**Novel statements**
- **Lifetime:** forever, as task ids with the first witness kept.
- **Why:** dedupe without provenance forgets who saw it first.

**Hall choices (count / eat)**
- **Lifetime:** forever, as append-only history.
- **Why:** cures F6.

**Faces silent for 7 days**
- **Lifetime:** the chair is shown empty, with its candle dark. The cast entry persists.
- **Why:** "institutions outlive heroes" (PRATCHETT doc:14). An empty chair is counted, not erased.

**Regression guards (bugs a harness caught)**
- **Lifetime:** forever, as fossils in the harness.
- **Why:** cures F2. RECEIPT:24 shows the harness remembering what reading forgot.

### The governing sentence

The room forgets **volume** and keeps **obligations**: open questions, claims, verdicts, landings and attributions. The fence's boss is a memory that refuses to be counted (VISION:19). The Hall must be countable: every compaction leaves a hash, and every expiry leaves an empty chair.

---

## 5. THE NAME

**THE HALL OF SHARED SUPPER.** The short form is *the Supper*.

### Why it is earned

- **It is already a room in the MUD that remembers.** It sits west of World-Memory (`game_mud.py:71-72` exits; room at `:74`). It persists to `HALL = "game.mud.hall_record"` (`:57`). Its law is in the bytes: "The hall files which you chose" (`:86`).
- **It has six chairs.** Empty chairs are seats not present. The chairs are the party.
- **The lineage converges on it.** The endgame is named "Ledger of Empty Chairs" (VISION:9). The vision's final shot is "the hall, the supper, the six chairs" (VISION:18).
- **Its noticing mechanic is the party chat's own job.** Counting who is at the table, and speaking the count aloud, is exactly that work (`:396-407`).

### Rejected names (negative examples)

| Name | Why it fails |
|---|---|
| "Party Chat v2" | It describes the medium, not the lineage. |
| "The Nexus" or "The Agora" | Invented from nothing, with no bytes behind them. |
| "The Answer" | The fenced boss (VISION:9-19). Adopting it would build the thing the fence forbids. |
| "The Living Mud" | That is the game world, not the table the party sits at. |

---

## 6. THE 5 W'S AND THE FALSIFIER

**WHO.** The party is `game_dm.party()` (`game_mud.py:306`, BYTES). The same seats and lanes run all arms. The operator, or one seat not in the party, freezes the problem set.

**WHAT.** A three-arm controlled run on a frozen problem set. The problems have a deterministic checker (a test passes, or a harness lane goes green, in the style of RECEIPT:23-24). About half of them recur on invariants from earlier problems.

| Arm | Memory condition |
|---|---|
| A (the Hall) | `recall()` over the party's own digests, claims and verdicts, with staleness laws on. |
| B (scroll) | The same seats with the current thread only, and no recall. This is ZEITGEIST.md:47's rejected default. |
| C (placebo) | `recall()` over a *different* party's digests, matched for token count. |

Three decoy problems are included. Each has a superseded claim that is now false.

**WHEN.** The run happens after the Part 3 patch and `party_hall.py` land and pass falsifier 3.4(a). There are 30 problems per arm, run interleaved on the same day. The interleaving controls lane drift, since U8 concurrency is measured per lane (NPC doc:52).

**WHERE.** The Hall, on the same providers.yaml lanes (NPC doc:53), with logs kept replayable. This follows ARENA_V2:15 (c).

**WHY.** To separate memory that **solves** from memory that only **reminisces**. "Nostalgic" means Arm A feels richer but does not verify more.

### Measures, pre-registered

1. Verified solve rate.
2. Tokens to the first verified solve.
3. **Repeat-error rate**: re-proposing a claim already falsified or superseded in the Hall.
4. **Decoy capture rate**: acting on a superseded claim.

### Falsifier

The Hall's memory is falsified as useful if ANY of the following holds:

| # | Condition | Meaning |
|---|---|---|
| (i) | Arm A's verified solve rate does not beat Arm B's on the recurrent half, with a bootstrap 95% CI over 1000 resamples excluding zero. The method follows ARENA_V2:15 (b). | The memory does not help. |
| (ii) | Arm A is not distinguishable from Arm C on that metric. | Any extra context helps, not *this party's* memory. That is nostalgia with a token budget. |
| (iii) | Arm A's decoy capture rate is at or above Arm B's. | Forgetting failed. The room drowned the party in its own fossils. |
| (iv) | Arm A shows no difference on the non-recurrent half while differing on the recurrent half. | **Not a falsifier, but a required sanity check.** If A wins equally on both halves, the gain is from tooling, not memory. |

If (i) through (iii) all fail to trigger, the room's memory makes the party measurably better at problems. The claim is then filed as a `kind=verdict` row and anchored, and the Hall has remembered its own proof.
