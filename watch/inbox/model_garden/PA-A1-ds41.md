# PA-A1-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# Anti-Forgery and Replay-Rejection for the Estate's Steering Channels

Deliverable shape follows the contract's five-part order. Every claim about code cites `file:line` from the supplied evidence. Where the evidence is truncated or a claimed file is not shown, the citation is marked UNVERIFIED with the reason.

Evidence files (call these by short tag):
- `[HS]` = `watch/inbox/model_garden/premium_autopsy/evidence/A1/00__hermes_steering.py`
- `[PD]` = `watch/inbox/model_garden/premium_autopsy/evidence/A1/01__phone_door.py`
- `[GS]` = `watch/inbox/model_garden/premium_autopsy/evidence/A1/02__grok_steer.py`
- `[FQ]` = `watch/inbox/model_garden/premium_autopsy/evidence/A1/03__FIFTY_QUESTIONS_ANSWERED.md`

A structural fact that drives the whole threat model: `[HS]:21-24` already imports `mag.steer_seal` (with a direct-script fallback), so the import site exists and the verifier is owed at that seam. `[FQ]` addendum 2 names the two standing FAILs: "Q41 steer verifier, Q42 steering-channel verify" staged, "5 STAGED with named reasons". Q42 requires a read-path bind; Q41 requires a keyed verdict at the verifier.

---

## 1. THREAT MODEL

### Channel A - file steers (`hermes_dispatch_log.jsonl` + `hermes_jobs/*.md`)

Writer surface: any process that can `open(..., "a")` on `memory/runs/hermes_dispatch_log.jsonl`. `[HS]:111-114` `_append_receipt` is exactly that, with no lock and no signature. Consumers: `cmd_jobs` at `[HS]:365-380` reads it and prints rows verbatim; nothing between disk and terminal verifies a byte. `[FQ]:Q21` proved the class concretely: "8 threads, 8 SrpStore sessions on one users.json -> 1/8 persisted, 7 users LOST (last-writer-wins)" - same JSONL append shape, same absence of atomic temp+rename.

Attacker primitives available today:
- Any local process (including a compromised agent body, a misbehaving cron stub, a curious editor) can append a `{"kind":"steer", "goal":"...", "resume":"..."}` row that `cmd_jobs` will render as a legitimate steer.
- File-write is sufficient; no channel authentication exists on disk.

### Channel B - Discord messages

Evidence: `[FQ]:Q42` names "steering-channel verify" as the standing FAIL. The Discord transport itself is not shown in the supplied bytes (grep for `discord` in the four evidence files returns zero hits) so the transport is UNVERIFIED here; the threat model binds to the invariant, not to the transport. What can be claimed: the operator's steering channel currently has no verifier in any read path, so a Discord peer who can post into the steering channel can forge a directive - the same shape as Channel A. Any fix must not depend on Discord's own author id being trustworthy, because a compromised webhook or a leaked bot token is inside the threat surface.

### Channel C - phone-door hooks

`[PD]:45-55` `ensure()` shells out to `tailscale ping`, writes a JSON row to `memory/runs/phone_door_log.jsonl`, no signature. `[PD]:57-68` `status()` reads the log and reports fire rate. Nothing in the file verifies who fired. A tailnet peer who can write to that path, or a caller who can invoke `python -m mag.phone_door ensure`, produces an indistinguishable row. The telephone door is a *health* channel today, but `[FQ]` calls it a steering-adjacent instrument (Q41/Q42 bracket the whole read path), and its log is consumed by other organs as ground truth about whether the tunnel is up.

### Channel D - grok overlay steers

`[GS]:93-113` `decide_steer` produces a steer string and returns it to the caller; `[GS]:115-121` `status()` advertises channels. There is no field in the returned dict that ties the steer to the operator (`[GS]:99-104` returns `"steer"` and `"channel"` with no signature). Any process holding the same overlay can craft a return value indistinguishable from a real one. Same class as A/B/C.

### Invariant the threat model defends

For each of A/B/C/D there is exactly one property that has to hold: *a steering directive consumed by any downstream read path resolves to bytes that were produced by the operator's secret, within a bounded time window, in a canonical envelope.* The fix is at read time, not write time, because write-time only seals rows that legitimately went through the writer; it does nothing for a writer that bypasses the writer.

Non-goals (state explicitly so the seat does not add ceremony):
- No second factor on the operator. His side stays one word.
- No new daemon, broker, or clock service.
- No new file format for `hermes_jobs/*.md` (backward compatibility during migration).

---

## 2. VERIFIER DESIGN

### 2.1 Where verification binds

Read path only. Three specific bind points, chosen because they are the exact read paths the evidence shows are currently unguarded:

1. `[HS]:365-380` `cmd_jobs` row renderer: every row must pass `steer_seal.verify_row` before print. A failing row renders as `REJECTED <reason> <raw-hash>` and the byte length of the original row is printed; the row is never echoed verbatim.
2. `[PD]:57-68` `status()` aggregation: the recent-fire set is filtered to verified rows before `oks` is computed. Unverified rows are counted separately and printed as `unverified: N`; they do not move the `ok` fraction.
3. `[GS]:99-113` `decide_steer` return value: the `steer` field is only populated when `steer_seal.verify_envelope` passes on a matching recent envelope; otherwise `need_steer` is true and `steer` is `""` with `"unverified_source": true`. This is the correct bind because the overlay is a *producer* that downstreams treat as an authority; if it cannot name a verified source, it must not emit a steer.

Q42 demanded "steering-channel verify" in the read path. These three bind points are the read paths. That is the whole reason the design forbids write-time-only sealing: Q42's verdict stands until a reader refuses a forged byte.

### 2.2 Key material and who holds it

One secret, held by the operator: 32 bytes, base32-encoded (52 chars, no padding), stored at `state/steer_secret.b32` with mode 0600. This is the *only* new infrastructure the design adds, and it is one file.

Derivation: HMAC-SHA256 as defined by RFC 2104 (`https://www.rfc-editor.org/rfc/rfc2104`). No novel primitive. The key is imported raw by `mag.steer_seal` at first call and cached in-process for the lifetime of the process; it is never logged, never echoed, never written elsewhere.

Operator-side ceremony: none. The operator types the word (or taps the Discord huddle, or speaks the phrase) exactly as today. The envelope is constructed by the *producer* side (the code path that receives his word and forwards it), using a key it reads from disk on the operator's own machine. The operator does not paste a code; the operator does not open an app; the operator does not count anything.

Rotation: on rotation, `state/steer_secret.b32.prev` is written alongside the new key for one replay window (default 24h, per §2.4). `verify_row` accepts envelopes that verify under either key during that window. Old key is deleted after the window by the same process that rotated.

Key custody is documented as: *the operator's secret lives on the operator's machine and in one backup on a hardware token he already owns.* This is the "single word stays single-word easy" constraint translated into storage.

### 2.3 Canonical envelope

A steering directive is a single line of the form:

```
STEER <b64url(kid)> <b64url(nonce16)> <b64url(ts8)> <b64url(hmac32)> <word>
```

Fields:
- `STEER` literal magic, three bytes plus space.
- `kid`: 4-byte key id (first 4 bytes of SHA-256 of the key, hex-truncated to 8 chars for human-readability).
- `nonce16`: 16 random bytes from `os.urandom`, base64url no padding.
- `ts8`: 8 bytes big-endian unix seconds, base64url no padding.
- `hmac32`: HMAC-SHA256 over `b"STEER.v1\0" || kid || nonce16 || ts8 || word_utf8`, base64url no padding.
- `word`: the operator's literal text, one line, no leading/trailing whitespace.

Canonicalization rules, no knobs:
- `word_utf8` is the UTF-8 encoding of the word after stripping trailing `\n` and mapping any remaining `\r` to `\n` (so Windows clipboard paste does not fork the byte stream).
- All base64url fields use no padding and lowercase alpha.
- The magic string is `STEER.v1\0` including the trailing NUL; this binds the version so a future v2 cannot replay into v1.
- No whitespace folding anywhere else in the line; the four spaces are literal.

### 2.4 Replay window

Two gates, both deterministic:
- Absolute: `|now - ts8| <= REPLAY_WINDOW_S` with `REPLAY_WINDOW_S = 86400` (24h) default. Chosen to survive a phone that slept through the night without opening a hole a patient attacker can walk through; the operator's directive to run right now will fall inside it.
- Monotonic-per-key: `max(nonce16)` seen per `kid` is stored at `state/steer_seal_seen.jsonl`, one append row per accepted directive: `{"kid":..., "nonce":..., "ts":..., "count":...}`. A directive whose nonce equals a previously accepted nonce for the same `kid` is rejected with `REPLAY`. Different `kid` (rotation grace window) tracks separately.
- Per-kid nonce count cap: 4096. On overflow the oldest 1024 rows for that kid are dropped (drop-oldest ring, matching the `[FQ]` `game.gd 64-slot drop-oldest ring` precedent so the design stays inside the estate's existing storage idiom). Dropping old rows is only safe because the absolute window already excludes them from acceptance.

Reject codes, fixed strings, one per cause:
- `STALE`: outside absolute window.
- `FUTURE`: ts8 more than 60s ahead of `now` (clock skew guard).
- `REPLAY`: nonce seen for that kid.
- `BADKID`: `kid` not in `{current, prev_within_window}`.
- `BADMAC`: HMAC mismatch.
- `MALFORMED`: envelope does not parse under §2.3.

### 2.5 The seal module

New module `mag/steer_seal.py`. Exports, all pure functions with a single side effect on the seen-log:

```python
# mag/steer_seal.py
def load_key() -> bytes: ...
def sign(word: str, *, _now: int | None = None) -> str: ...   # producer side, one call
def verify(word_line: str, *, _now: int | None = None) -> tuple[bool, str, str]: ...
    # returns (ok, code, canonical_word)  code in {OK, STALE, FUTURE, REPLAY, BADKID, BADMAC, MALFORMED}
def verify_row(row: dict) -> tuple[bool, str, dict]: ...
    # row is a parsed JSONL row; looks for row["goal"] if row["kind"]=="steer"
```

`_now` exists for tests only; production callers do not pass it. `verify_row` never mutates the input row. The seen-log append only happens on `OK`, so a repeated forgery attempt does not grow the seen-log and cannot be used to DoS the store.

### 2.6 Backward compatibility during migration

Phase 0 (land now): `verify` returns `UNVERIFIED` for envelopes missing the `STEER` magic, but the three call sites above *still render the row*, with a leading `UNVERIFIED ` prefix and the raw-hash suffix. Nothing breaks; every existing row remains visible. A counter `state/steer_seal_stats.jsonl` records unverified counts per consumer per day.

Phase 1 (after 7 days, operator word): the three call sites upgrade `UNVERIFIED` from "render with prefix" to "reject with `MALFORMED`". Rejection is the read-path only; rows stay on disk and stay inspectable by `cat`.

Phase 2 (after 30 days): Phase 1 behavior becomes the default and the `UNVERIFIED ` prefix path is deleted. `git log --grep "steer_seal phase"` is the audit trail.

---

## 3. THE PATCH SPEC

All patches below are stated against the head bytes of `[HS]` as supplied. The seat can apply them as-is. Where the evidence file is truncated (`[HS]` head+tail only), the line numbers are the supplied ones; UNVERIFIED is marked where the absence of bytes blocks confidence.

### P1 - new module

Add file `mag/steer_seal.py` implementing §2.5. No `file:line` anchor because the file is new; the caller anchors below are what matter.

### P2 - Hermes dispatch: seal on producer side

File `[HS]`, function `cmd_steer` (the steer subparser arm; the dispatch/steer entry points are named at `[HS]:348-354` `sub.add_parser("steer", ...)`). Locate the call site in `cmd_steer` that builds the `goal` string for `_run_hermes`. Replace:

```python
    goal = args.nudge
```

with:

```python
    from mag import steer_seal
    goal = steer_seal.sign(args.nudge) if not args.nudge.startswith("STEER ") else args.nudge
```

The `startswith("STEER ")` guard is the migration door: an already-sealed word (for example when an upstream caller sealed and this function received the envelope) is not double-sealed.

Anchor: `[HS]:348-354` where the `steer` subparser is declared, and the `cmd_steer` body which is UNVERIFIED in supplied bytes (the file is truncated at head+tail; the body of `cmd_steer` sits inside the middle 75% that the premium autopsy step omitted). The seat reads the live file and applies to the body; the shape is what matters.

### P3 - Hermes dispatch: verify on read side (`cmd_jobs`)

File `[HS]:365-380` `cmd_jobs`. Current:

```python
    for r in rows[-args.n:]:
        kind = r.get("kind", "dispatch")
        label = r.get("resume", "") if kind == "steer" else r.get("persona", "") or r.get("dir", "")
        print(f"{r['ts']} {kind:8s} exit={r['exit']:>3} {label} :: {r.get('goal','')[:80]}")
        print(f"    -> {r.get('output_path','')}")
```

Replace with:

```python
    from mag import steer_seal
    for r in rows[-args.n:]:
        kind = r.get("kind", "dispatch")
        label = r.get("resume", "") if kind == "steer" else r.get("persona", "") or r.get("dir", "")
        goal_for_display = r.get("goal", "")
        seal_tag = ""
        if kind == "steer":
            ok, code, canonical = steer_seal.verify_row(r)
            if ok:
                goal_for_display = canonical
                seal_tag = "SEALED "
            elif code == "MALFORMED":
                seal_tag = "UNVERIFIED "
            else:
                seal_tag = f"REJECTED:{code} "
                goal_for_display = f"<unverified bytes: len={len(r.get('goal',''))}>"
        print(f"{r['ts']} {seal_tag}{kind:8s} exit={r['exit']:>3} {label} :: {goal_for_display[:80]}")
        print(f"    -> {r.get('output_path','')}")
```

This is the Q42 read-path bind for the Hermes channel. The `REJECTED:` rows never echo the raw goal, only its length; this matches the "operator single-word stays single-word" rule because the operator's own word is never *shown back* to him, so there is nothing for a shoulder-surfer to photograph.

### P4 - Phone-door: verify on read side

File `[PD]:57-68` `status()`. Current:

```python
    rows = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    recent = rows[-10:]
    oks = sum(1 for r in recent if r.get("ok"))
```

Replace with:

```python
    from mag import steer_seal
    rows_raw = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows, unverified = [], 0
    for r in rows_raw:
        ok, code, _ = steer_seal.verify_row(r)
        if ok:
            rows.append(r)
        else:
            unverified += 1
    recent = rows[-10:] if rows else []
    oks = sum(1 for r in recent if r.get("ok"))
```

Then extend the return string at `[PD]:66` to include `unverified: {unverified}` on its own line. If `rows` is empty and `unverified > 0`, the returned string must read `door health unknown (all fires unverified)` rather than claiming either UP or PRUNE; the hook must not lie about a door it cannot authenticate.

### P5 - Grok overlay: refuse to emit unverified steers

File `[GS]:99-113` `decide_steer`. At the last return before the patch-detected branch, when a steer string is produced, wrap it:

```python
        ok, code, canonical = steer_seal.verify_word(steer)  # envelope-shaped check
        if not ok:
            return {"ok": False, "schema": SCHEMA, "need_steer": True, "gate": gate,
                    "steer": "", "unverified_source": True,
                    "channel": "refused: no verified envelope"}
```

`verify_word` is a sibling of `verify` that accepts a bare word with an attached envelope on the same line (the DFHack overlay receives steers from a producer that may not be the Hermes dispatch path). This is the only asymmetry in the seal module and it exists because the overlay has two producers, not one.

### P6 - Rotation and seen-log

Add to `mag/steer_seal.py`:
- `rotate(new_key: bytes) -> None` writes `state/steer_secret.b32` and moves the old key to `state/steer_secret.b32.prev` with an mtime marker.
- `_prune_seen(kid: str, cap: int = 4096) -> int` implements the drop-oldest ring; called once per `verify` OK, so the store stays bounded without a daemon.

### P7 - Tests (fifth deliverable, but listed here to keep the patch contiguous)

New file `tests/test_steer_seal.py`. See §4 for the case list.

All seven patches total <= 180 lines of diff. No new process. No new dependency beyond `hmac`, `hashlib`, `base64`, `os`, `json`, `time` from the standard library.

---

## 4. TEST PLAN

Positive cases (must be REJECTED):

1. **Forged word, no envelope.** Row `{"kind":"steer","goal":"stop everything"}`. Expect `MALFORMED` in Phase 1; in Phase 0 `UNVERIFIED `. Never `OK`.
2. **Forged envelope, random HMAC.** `STEER <kid> <nonce> <ts> <random32> stop everything`. Expect `BADMAC`.
3. **Wrong kid.** Valid HMAC under a key the verifier does not hold; kid not in `{current, prev}`. Expect `BADKID`.
4. **Replayed envelope.** Sign a word, verify it once (`OK`), verify the same line again. Second call must return `REPLAY`.
5. **Stale envelope.** `ts8 = now - 86460`. Expect `STALE`.
6. **Future envelope.** `ts8 = now + 120`. Expect `FUTURE`.
7. **Tampered word, valid prefix.** Envelope from case 4 with `stop everything` changed to `stop nothing`. HMAC over the tampered word does not match. Expect `BADMAC`.
8. **Byte-level near-miss.** Envelope from case 4 with one base64url byte flipped in `nonce16`. HMAC covers nonce, so `BADMAC`. Must not be `MALFORMED` (would indicate the parser is too permissive).
9. **Windows clipboard newline fork.** Envelope produced on Windows with trailing `\r\n`; verifier canonicalizes. Must be `OK`, and the canonical word must not contain a trailing `\r`.
10. **Envelope with wrong magic.** `STEER.v2 ...` under a v1 parser. Expect `MALFORMED`. This prevents version-confusion replay.

Negative cases (must still PASS unchanged):

11. **Fresh operator word, correct envelope.** `steer_seal.sign("kill the build")` produces a line. `verify` returns `OK` and `canonical == "kill the build"`. This is the interrupt law's happy path.
12. **Operator word with punctuation, quotes, non-ASCII.** `"stop! 'kill the build', 好"`. `sign` then `verify` round-trips byte-identical to the input after the canonicalization map.
13. **Operator word longer than 80 chars.** Must verify OK and render truncated only for display (`[HS]:365-380` `[:80]` slice preserved). No rejection based on length.
14. **`cmd_jobs` end-to-end against a mixed log.** Append one sealed row, one forged row, one pre-migration row. Run `cmd_jobs`. Output must show three lines: `SEALED `, `REJECTED:BADMAC `, `UNVERIFIED `; the `REJECTED:` line must not contain the forged word.
15. **Phone-door status with 9 verified + 1 forged fire.** `status()` must report `9 ok in last 9, unverified: 1`. The `ok` fraction denominator is 9, not 10.
16. **Rotation grace.** Sign under key A, rotate to B, verify the A-signed line at `now + 1h`. Must be `OK`. At `now + 25h` must be `BADKID`.
17. **Single-word path timing.** `sign` under 1 ms, `verify` under 1 ms on a 2020-class laptop. Measured with `time.perf_counter` in the test; a regression above 5 ms fails the test. This is the "no ceremony added" law made testable.
18. **Producer-side no-double-seal.** `sign(sign(word))` must not produce a nested envelope; the second call sees `STEER ` prefix and returns its input unchanged (matching P2's `startswith` guard).

Forgery cases that clarify the "challenging IS the affection" clause: 1, 2, 3, 4, 7, 8 are the six that would, without this design, reach an agent as a live steer and are now hard-failed at the reader. Case 4 is the one that replay-protects the operator's actual past word from becoming an attacker's future word.

---

## 5. FALSIFIER

The design is wrong if any of the following is observed on the live estate. Each is a single command or a single read, not a survey.

F1. **Read-path bypass.** Any consumer of `hermes_dispatch_log.jsonl`, `phone_door_log.jsonl`, or `decide_steer` output is shown to render a `REJECTED:*` row's raw goal verbatim. Instrument: `grep -rn "goal" watch/inbox/model_garden/premium_autopsy/evidence/A1/00__hermes_steering.py` plus a live run of `cmd_jobs` against a poisoned scratch log. If P3 is applied and a forged word still prints, P3's slice is not where I claim.

F2. **Nonce store divergence.** Two readers on two machines accept the same nonce in the same window. Instrument: run `cmd_jobs` on two hosts against the same seen-log over a network share; if the second reader accepts, the seen-log is not the single authority I claim and the replay guarantee is weaker than stated. Verdict today: UNVERIFIED because the estate is a single-host layout in the evidence; if the estate is actually multi-host this falsifier is a live risk, not a hypothetical.

F3. **Operator ceremony regression.** `time` the operator from "the thought fires" to "the word is typed" before and after Phase 1. If the delta exceeds 500 ms or requires a new keystroke (a copy, a paste of an envelope, a second app), the "single-word easy" constraint is violated and the design has failed on its most important non-negotiable. Instrument: two 10-trial stopwatch runs, one on the old path, one on the new, same operator, same day.

F4. **Migration break.** Any pre-migration row that a consumer used to render is now invisible under Phase 1. Instrument: `wc -l` the log, run Phase 0 `cmd_jobs`, count lines; run Phase 1 `cmd_jobs`, count lines. Lines must match. If Phase 1 drops lines rather than rejecting them, backward compatibility is broken.

F5. **Key leak.** `state/steer_secret.b32` appears in any `git log -p`, any `hermes_dispatch_log.jsonl` row, any traceback, or any `[:200]` error slice in the seal module. Instrument: `git log --all -S "$(head -c 8 state/steer_secret.b32)" --` returns empty, and a `grep -R "$(head -c 8 state/steer_secret.b32)" memory/ state/` returns nothing outside the key file itself. If the key leaks, this design's central secret is worthless and the whole patch is a null operation.

F6. **Q41/Q42 flips without the reader.** If a future census shows Q41 or Q42 flipped to PASS while `mag/steer_seal` is not imported by `[HS]:365-380`, `[PD]:57-68`, and `[GS]:99-113`, the flipping instrument measured the writer, not the reader, and the standing FAILs about to be un-flipped were un-flipped by a write-side patch that does not answer the contract.

The design's own name for its failure mode, so a seat can say it in one breath: *the seal is a substring of the envelope and not a gate on the reader.* If any reader can still see the raw word, the seal's job is decoration, not verification.

---

## Falsifier of my own deliverable

If `[HS]` in the live tree imports `mag.steer_seal` at a call site inside `cmd_steer`'s body (which the supplied head+tail truncation does NOT show; the import at `[HS]:21-24` is present but its call site is UNVERIFIED), then P2 is already landed and my §3 P2 is a duplicate that a seat must not apply. The seat's first command before editing `[HS]` is:

```
grep -n "steer_seal" watch/inbox/model_garden/premium_autopsy/evidence/A1/00__hermes_steering.py
```

If it returns more than the two hits at `[HS]:21-24`, the seat re-reads and skips P2 accordingly. This is the one byte I could not verify against the supplied evidence, and I am naming it rather than papering it over.
