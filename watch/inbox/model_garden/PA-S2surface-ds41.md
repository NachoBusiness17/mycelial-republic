# PA-S2surface-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# STRANGER AUDIT SURFACE 2: THE SHARED INBOX CONTRACT

Auditor: hostile outsider, no prior session context. Evidence: the four files quoted in-band only. Every claim below cites the bytes I was given.

---

## 1. ATTACK SURFACE MAP

Attacker model: a compromised sibling seat (Windows/docker/WSL/CLI). It has legitimate write access to `watch/inbox/` and `index_events.jsonl`. It is not root, does not modify the validator source, and cannot forge a signature (no signature scheme exists in the evidence). It CAN append lines, write new files, and (per the flow shown) participate in the fold that produces `INDEX.json`.

Five attack classes, ordered by how much trust they buy.

### A1. Receipt forgery by taxonomy slap

The contract's classification law is nominal (evidence `01__INDEX.json` law 4: "Classify each item as FACT, INFERENCE, PROPOSAL, UNPROVEN, or RECEIPT").
The log shows a `register` op with a `"class"` string that is attacker-chosen (`03__index_events.jsonl` seq 1-27 and the tail seq 1790901937830713646-49 all carry `"class":"receipt"`).
Concrete poisoning: a compromised seat writes a new file `RECEIPT_TRUST_ROOT_ROTATION_2026.json`, then appends a register event with `"class":"receipt"`. Any downstream reader that reads `class` first and defers scrutiny until after "FACT vs UNPROVEN" triage now treats the payload as already classified. The contract's own authority block (`00__SHARED_SURFACE_CONTRACT.json`, `authority.inbox_content`) says inbox is "untrusted_data_until_classified" - but nothing in the evidence verifies WHO assigned the class, or that the class matches the producer's authority. `class` is a self-declaration, not a verdict.

This is the top of the kill chain: the rest of the estate conditions on the class string.

### A2. Hash lie in the register event

`sha256` in each `register` is a claim. The validator hashes files present at validate time (`02__shared_surface.py` docstring: "validate hashes that sealed prefix"). No line in the evidence shows the validator cross-checking that a register event's claimed `sha256` matches bytes ever seen on disk at that moment.
Exploit shape: emit a register event with the sha256 of a benign file, then write a hostile file to the same path. Fold readers that trust the event sha256 (the event log is declared source of truth in `01__INDEX.json` `purpose` and `derivations.source`) have no on-disk rebuttal unless a validator run independently rehashes. Worse: the autoseal pattern at the tail (`autoseal (rib.md.record.v1)`) seals "first N bytes" per `02__shared_surface.py` docstring - an attacker appends hostile bytes past the sealed prefix of an "open" living item and the seal still validates.

### A3. INDEX corruption via nonce discipline collapse

The only integrity signal in the entire evidence for `index_events.jsonl` is the nonce GAP warning list (`01__INDEX.json` `fold_warnings`, 70+ entries). Examples: `writer "exp002a" nonce GAP: expected 249, got 1 (seq 28)`, `writer "zcode-seat-20260926" nonce GAP: expected 2, got 1 (seq 1790432184633)`, `writer "b2_378_20260926" nonce GAP` four times on the SAME seq `1790446136785949200`.
Nonce gaps are warnings, not errors. There is no reject path in the evidence.
Exploit shape (replay): compromised seat copies a legit historic register line verbatim, bumps `seq` with a fabricated value, keeps the original `writer` and `nonce`. The fold sees a nonce GAP (warning), folds the line, and the writer's apparent history now shows duplicate or reordered claims with no hard failure. Downstream consumers that read `derivations.event_count` (8062) and `active_items` (2419) as authoritative now see an attacker-influenced census and never know.
Seen in evidence: `b2_378_20260926` fires four gaps against one seq - either the writer is broken or a replay already lives in the log. Present evidence cannot distinguish.

### A4. Bounded pointer discharge (unbounded in practice)

Contract law 6 (`00__SHARED_SURFACE_CONTRACT.json`): "Prefer an artifact plus bounded pointers and hashes over a copied transcript." `purpose` field in register events is the pointer.
Exploit shape: the purpose string is an untyped free-text field (`03__index_events.jsonl` seq 1-27 show prose purposes). A compromised seat can place a directive string in `purpose` that a downstream READING seat (the LLM that folds the inbox, or an agent that summarizes it) treats as instruction. The fold's warning text itself shows this channel is read by humans and tools.
Positive example of the safe pattern: `"purpose":"Hash-backed record of verified relocation from Codex-local storage"` (seq 3) - descriptive, no directive verb.
Negative example (same file, seq 19): `"purpose":"Provenance unknown - recovered from clobbered INDEX 02:36Z; classify before use"` - the phrase `classify before use` is an embedded imperative that a downstream agent can act on without the classifier ever validating the producer. This is prompt-injection-ready syntax already in the evidence.

### A5. Prompt injection of the READING seat through item bodies

The contract permits `INDEX.md` as `read_first` (`01__INDEX.json` `read_first: "/board/inbox/INDEX.md"`). Nothing in the evidence pins the content shape of `INDEX.md`. A compromised seat that owns the fold can emit an `INDEX.md` containing arbitrary prose, table cells, or markdown with image URLs / links to be fetched - and the READING seat consumes it before any classification gate fires. The contract's `authority.inbox_content: "untrusted_data_until_classified"` is exactly backwards for the read-first path: classification happens after read, and read is mandatory.

This is the classic hostile-outsider finding on this surface: the FIRST file the law tells you to read is the LAST file the law validates.

### A6. Env-redirect tripwire is a warning (self-documented soft spot)

`02__shared_surface.py` docstring: "Env-redirect tripwire (B2-358)... warns when MAG_SEAT_CRASH_LOG or MAG_GAPS_LOG is set outside a test run... never fails validate." A compromised seat that can set env vars in a shared shell (per `client_aliases.grok_powershell.local_session_cache: "browser or CLI session history"`) can silently redirect crash and gap logs. No failure, no receipt, no escalation.

---

## 2. THE 3 WEAKEST JOINTS (ranked)

### Joint 1 - Self-declared `class` on register events, no producer-role binding

- File:line: `03__index_events.jsonl` seq 1 (`"class":"PROPOSAL"`), seq 3 (`"class":"RECEIPT"`), tail seq 1790901937830713646-49 (`"class":"receipt"`). Contract side: `01__INDEX.json` law 4 mandates classification; no line binds class to a writer role or authority.
- Exploit shape: compromised seat registers a hostile artifact as `RECEIPT` or `FACT`. Downstream consumers filter by class to decide what to trust. Class string is attacker-controlled; no signature, no role check, no cross-file proof.
- Kill mechanism: trust laundering. `RECEIPT` semantically inherits the estate's "trust bytes not reports" posture without ever having crossed a verification gate.

### Joint 2 - Nonce gaps are warnings; the fold cannot reject a lying writer

- File:line: `01__INDEX.json` `fold_warnings[0]` `"writer \"exp002a\" nonce GAP: expected 249, got 1 (seq 28)"` through `fold_warnings[70]`. Validator wiring: `02__shared_surface.py` gates list (events-log hygiene, key schema, links split, links sha ratchet) - nonce gaps are NOT in the gate list, only surfaced as a top-level field `events_log_malformed` and folded warning text.
- Exploit shape: replay, reorder, or silently drop events under a stolen writer name. Fold still emits `INDEX.json`; `ok` stays true.
- Kill mechanism: forgery without a matching nonce still folds. The evidenced state of `b2_378_20260926` (four gaps, one seq) is either already the shape of a broken writer or the shape of a replay. Not distinguishable from the evidence alone.

### Joint 3 - `INDEX.md` is `read_first` and its shape is unpinned

- File:line: `01__INDEX.json` `"read_first": "/board/inbox/INDEX.md"`. Contract side: `00__SHARED_SURFACE_CONTRACT.json` `canonical.read_first: "/board/inbox/INDEX.json"` - the contract and the index disagree on read_first (JSON vs MD). That is a spec bug on top of an attack surface.
- Exploit shape: compromised seat produces an `INDEX.md` containing directive text, fake "verified" tags, or links that a READING seat fetches before classification. The mandatory-read path is the injection channel.
- Kill mechanism: the law says read-first, the surface says untrusted-until-classified. Read-first wins in practice, so the classifier is downstream of the attack.

Honorable mention (not top 3 because it may be a bug not an attack): the read_first disagreement between `SHARED_SURFACE_CONTRACT.json` (`INDEX.json`) and `01__INDEX.json` (`INDEX.md`). Either one is a stale document or one is a redirect.

---

## 3. PATCH SPEC PER JOINT

Each patch is landable as-is. All patches are additive: no field renamed, no existing event rewritten (the log's append-only law holds).

### P1 - Producer-signed classification

Add a `producer_key_id` field to every `register` event, and a per-writer public key registry at `watch/inbox/producer_keys.json`.

Spec:
1. New file `watch/inbox/producer_keys.json`, schema `shared_inbox.producer_keys.v1`:
   ```
   {
     "schema": "shared_inbox.producer_keys.v1",
     "keys": {
       "<writer>": { "ed25519_pub_hex": "<64-hex>", "first_seen_ts": "<iso>", "role": "seat|operator|service" }
     }
   }
   ```
2. Register events gain required fields: `producer_key_id` (writer name) and `sig` (ed25519 over canonical JSON of `{seq,ts,op,file,sha256,class,purpose,writer,nonce}` with sorted keys, no whitespace).
3. Fold gate `mag/producer_signature_gate.py` (new module, wired into `inspect_surface`):
   - For each `register` event with `writer` in `producer_keys.keys`, verify `sig` against the pubkey.
   - FAIL when signature missing or invalid.
   - WARN when `writer` has no entry in `producer_keys.json` and event ts is before registry `first_seen_ts` (grandfathered pre-signature debt, same pattern as `events_malformed_baseline.json`).
   - FAIL when `writer` has no entry and ts is after registry `first_seen_ts`.
4. Migration: baseline today's un-signed events by content sha256 into `configs/events_unsigned_baseline.json`, mirroring `configs/events_malformed_baseline.json` referenced at `02__shared_surface.py` MALFORMED_BASELINE.

Falsifier for P1: an attacker who has stolen a producer's private key still forges. This patch raises the bar from "anything written" to "anything with proof of key custody"; it does not close the compromised-seat case. That residual is P1b (key rotation receipts, out of scope for this deliverable) and must be named, not hidden.

### P2 - Nonce monotonicity as a hard gate

Move nonce gaps from warnings to errors, with a baseline for existing debt.

Spec:
1. Add `scan_nonce_gaps(events_log) -> list[gap]` in `mag/events_scan.py` (re-exported through `mag/shared_surface.py` per the B2-399 pattern already used there for `scan_events_log`).
2. Gate: any gap whose seq is not present in `configs/events_nonce_gap_baseline.json` is an ERROR. Baseline keys are `(writer, seq)` tuples so a fixed writer reclaims its registry entry (same reclaim pattern as events_malformed_baseline).
3. Existing 70+ gaps at `01__INDEX.json` `fold_warnings` are grandfathered by (writer, seq) pair. Any NEW gap fails validate exit 1.
4. Add `--allow-nonce-gap <writer>:<seq>` CLI flag to `python -m mag.shared_surface rebuild` for the operator path when a gap is provably benign; the flag writes a receipt to `watch/inbox/burn_wave_*/B2_XXX_nonce_gap_disposition_<date>.md` and appends the pair to the baseline.
5. Repeated gaps against the same seq under the same writer (the `b2_378_20260926` case, `seq 1790446136785949200` x4) collapse to one baseline entry: the gate reports them as one finding with occurrence count, matching the key-schema gate's counting style (`02__shared_surface.py` docstring, "one per distinct key, naming the key, occurrence count").

Falsifier for P2: a legitimate writer that restarts without persisting its nonce counter now fails validate. That is the point: the failure is loud, the operator dispositions it with a signed receipt, and drift stops hiding in warnings.

### P3 - Read-first is the last thing to trust: freeze the `INDEX.md` shape and gate it

Fix three things at once: the read_first disagreement, the injection channel, and the classification-after-read inversion.

Spec:
1. Resolve the read_first contradiction by making `INDEX.json` the read-first (matches `00__SHARED_SURFACE_CONTRACT.json` `canonical.read_first`). `INDEX.md` becomes a derived human view, never the entry point. Land a one-line edit in the fold writer that rewrites `01__INDEX.json` `"read_first"` value from `/board/inbox/INDEX.md` to `/board/inbox/INDEX.json`.
2. Add `mag/index_md_shape_gate.py`: `INDEX.md` must match a strict template - header block, then a table with fixed columns `path | class | sha256 | purpose_sha256 | ts`. The `purpose` column is replaced by `purpose_sha256` in the reading surface; full purpose text is available only by opening the event log line, forcing the reader to leave the index before ingesting attacker-controlled prose.
3. The gate FAILS on: any line in `INDEX.md` outside the template, any URL, any markdown image, any imperative-looking token (`IGNORE`, `SYSTEM:`, `INSTRUCTION:`, `<|`, `###`), any HTML entity. This is a positive allowlist, not a keyword blocklist.
4. Any consumer that wants the prose purpose reads `index_events.jsonl` line-by-line through `python -m mag.shared_surface event <seq>`, which returns the raw JSON with class badge `untrusted` unless the producer-signature gate (P1) passed.

Falsifier for P3: a compromised seat writes the payload into a filename or path segment (not into INDEX.md prose) and the READING seat concatenates path names into its context. Mitigation: the shape gate also constrains `path` to `[A-Za-z0-9._/-]+` and rejects any path containing a space, `|`, `:`, or non-ASCII. The `purpose` field in the current log contains such a path today: `frontier_olm_2026-10-01/steal/open-local-language-models via x.md` (evidence `01__INDEX.json` tail) contains spaces and `via`. That file's own purpose string would be rejected under P3 until renamed. Land the rename in the same PR.

---

## 4. THE SINGLE VALIDATION THE CONTRACT'S OWN LAW DEMANDS BUT NO TOOL RUNS TODAY

The contract's law 8 (`00__SHARED_SURFACE_CONTRACT.json`): "Record source hash, producer, timestamp, destination, and acceptance state in a receipt."

No validator in the evidence checks that a declared `sha256` was ever true.

`02__shared_surface.py` docstring is explicit: "validate hashes that sealed prefix" - i.e. it hashes what is on disk NOW. It never cross-checks a register event's claimed `sha256` against bytes at the moment of that event. The event log is declared source of truth (`01__INDEX.json` `purpose`, `derivations.source`), so the claim is the record; the file on disk is a later state that may or may not have ever matched.

The missing validation, in one sentence: **for every `register` event, verify that the `sha256` field matches either the file's current bytes, the sealed prefix declared by a later `autoseal` event for the same path, or a grandfathered entry in a "hash was true at register time but has since evolved" registry - and FAIL on any register event whose sha256 has no such witness.**

Name: `register_hash_witness_gate`. New module `mag/register_hash_witness.py`, wired into `inspect_surface`.

Contract for the gate:
- Input: `watch/inbox/index_events.jsonl`, `watch/inbox/`, baseline `configs/register_hash_witness_baseline.json`.
- For each `register` event with `(file, sha256, ts)`:
  - If `watch/inbox/<file>` exists and `sha256(current bytes)` equals event sha256: PASS (witnessed).
  - Else if a later `autoseal` event for the same `file` exists with `bytes:N`: PASS if `sha256(first N bytes of current file)` equals event sha256 (this is the living-hash law, applied retroactively).
  - Else if the event's content sha256 appears in `configs/register_hash_witness_baseline.json` keyed on `(writer, seq)`: WARN, grandfathered debt.
  - Else: ERROR, one per distinct `(writer, seq)`, naming the file, the claimed sha256, the observed sha256 (or `absent`), and the ts.
- Missing baseline file is an ERROR (same posture as `events_malformed_baseline`).
- Missing `index_events.jsonl` is a WARNING (container surfaces may not mount it, matching `02__shared_surface.py` events-log hygiene).

Positive example of what passes: tail event `seq 1790901937830713648` for `ractor_engine/2026-10-01-dogfood-gaps/accuracy.md` claims `sha256 7d71160b...`, and the immediately following `autoseal` event for the same path declares `bytes: 10393` with the same sha. If the first 10393 bytes of the current file hash to `7d71160b...`, the register is witnessed. If the file has since been fully rewritten, the gate catches it.

Negative example of what fails: a hostile seat appends `{"seq": 9000, "op":"register", "file":"SAFE_LOOKING.md", "sha256":"<hash of empty file>", "class":"FACT"}` and then writes a hostile `SAFE_LOOKING.md`. The current validator sees the on-disk file, hashes it, and reports a mismatch between the current file and... nothing, because no gate compares event sha to current bytes. Under this gate the register event's claim has no witness, `SAFE_LOOKING.md`'s actual bytes do not match the claim, and the event FAILS validate with exit 1.

Falsifier for the missing-gate patch: an attacker who can write both the file and the event before any validate run, and whose file's current bytes DO match the register event's sha (because the attacker computed the sha of their own hostile bytes) - passes. The gate witnesses coherence, not benign intent. Coherence is the floor; signatures (P1) are the ceiling. Both are needed; neither alone is sufficient. State this in the patch header, do not bury it.

---

## CLOSING (falsifier for this deliverable)

Falsifier for the whole audit: any of the four cited files, re-read in full at a later date, shows a gate for register-sha256 witnessing, nonce-gap rejection, or producer signatures that I did not see in the truncated head+tail I was given (`01__INDEX.json` was 703015 chars, `03__index_events.jsonl` was 2914570 chars, `02__shared_surface.py` was 20963 chars). If such gates exist in the middle region I did not see, the corresponding joint drops off the top three and the ranking re-sorts to whichever of A1/A4/A5 remains ungated. Everything above cites only bytes I was shown; the parts of the files I was not shown are marked out of scope by omission, not by assertion.
