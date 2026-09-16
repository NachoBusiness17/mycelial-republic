# W2 — PLAYER FILES (M2) — receipt

Wave: wave_20260916 · Lane: W2 · Blueprint: `watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md` (M2)
Artifact: `mag/wow_player.py` + `tests/test_wow_player.py`
Law: a character is an append-only ledger, not a database row — login is resume-from-ledger.
Worker: stealth/union-alpha drafts (OPENROUTER_API_KEY via `mag.flight_recorder.load_env`, never printed).
Editor: zcode seat. $0. No git commands. `.venv\Scripts\python.exe` only.

## Log (appended as I go)

- [t0] Receipt opened. Blueprint read: M2 falsifier = "state survives restart byte-identical".
- [t0] Pattern source read: `mag/wow_bones_session.py` — `canonical()` (json.dumps, sort_keys,
  compact separators, ensure_ascii=False) is the ONLY serialization; `session_id_for()` derives
  ids from sha256 of schema+seed; save writes canonical bytes, load rebuilds object. Reusing all three.

## Design contract (editor, before the draft)

```
player file (schema wow_player.v1):
  schema      "wow_player.v1"
  player_id   "ply-" + sha256("wow_player.v1:name")[0:12]   (derived, secret-free)
  name        str
  traits      {room: str, stamina_max: int, inventory: [pack_receipts]}
  ledger      [{n: int, event: str, data: {}, prev: hex, hash: hex}]
```

- NO timestamps anywhere (determinism — created_ts deliberately omitted).
- Every mutation appends exactly one ledger row; hash chain: `hash = sha256(canonical({n, event, data, prev}))`.
- Resume = replay rows through pure reducers; final state must equal stored traits (checked on load).
- Tamper detection: `verify()` recomputes the chain; typed error `TAMPERED`.
- Inventory is append-only at the file level: grants append receipts; spends append a row that
  shadows (never mutates) earlier rows.

- [t1] Call harness reused from wave U1 (`u1_union_call.py` pattern: stream, 3 attempts,
  storm backoff on 429/402). Prompt filed: `watch/inbox/wave_20260916/w2_union_prompt.md`.
  Editor contract fixed BEFORE the draft (above) so the draft has no design authority.

- [t2] Worker call: attempt 1, streamed, finish=stop, 13,808 chars, 5,992 tokens,
  **cost $0.00**, latency 261 s. Draft filed: `w2_union_draft.txt`.

## Editor pass (what changed from the draft)

- Docstring rewritten to house voice (law + file shape + determinism + RUN block), matching
  `wow_bones_session.py`; draft's 10-line aphorism replaced.
- Removed a dead `except UnicodeError` branch around `player_id_for` (sha256 of a str cannot raise it).
- Added explanatory comments (spend-shadows-grant; byte-identity surface); added create()
  docstring noting ALREADY_EXISTS → resume-with-load.
- Everything else kept as drafted: typed reasons, chain verify, replay-on-load, conflict guard.

## Verification (editor seat)

union-alpha's implied self-check (create → move → grant → spend → save → fresh load →
byte-identical) was RUN, not trusted — it held. Its checks were correctly signed this time
(hash payload = {n, event, data, prev}, excludes the row's own hash; strict key-sets).

Test command: `.venv/Scripts/python.exe -m pytest tests -k wow_player -q` (run from repo root)

```
17 passed, 1440 deselected, 2 warnings in 6.55s
```

Whole wow family regression (bones + session + family + manifest + player):

```
52 passed, 1405 deselected, 2 warnings in 15.65s
```

Note: one intermediate run errored 17× with PermissionError at setup (Windows file-lock/AV
transient right after file writes); a single-test run and the re-run both passed clean.
No flake in the module or tests themselves.

## Union-alpha grade (editor's honest grade; its self-grading is known broken)

**A-** as a drafter. Contract-faithful on first pass: canonical-only serialization, typed
refusals in the contract's order, replay-vs-view on load, exclusive-create genesis, and an
LEDGER_CONFLICT save-guard it was NOT even asked for. Zero invented APIs, zero timestamps.
Docked for the dead exception branch and missing RUN block. Falsifiers, not its word, are
what make it shippable — 16/17 tests passed against it unedited; the 1 failure was the
EDITOR's tamper being wrong (whole-row swap trips BAD_N before BROKEN_CHAIN), fixed in the test.

## Design decisions flagged

1. **created_ts omitted + strict key-sets**: `_FILE_KEYS` / `_ROW_KEYS` exact-match makes a
   timestamp structurally impossible, not conventionally absent. Determinism enforced by schema.
2. **player_id salt = the schema string** (`wow_player.v1:<name>`): secret-free, deterministic,
   same shape as `session_id_for`. No secrets in file, no uuid, no clock.
3. **Spends shadow grants**: grant and spend rows both live in the ledger forever; only the
   replayed view drops the spent item. File-level inventory append-only.
4. **History guard on save** (`LEDGER_CONFLICT`): a stale instance can never truncate or
   rewrite a written chain — append-only at the file level, not just the API level.
5. **Genesis is exclusive-create** (`xb`): second `create` for a name refuses with
   ALREADY_EXISTS; login is `load()` — resume-from-ledger, no upsert row. The anti-MySQL law
   made structural.
6. **load() never trusts the view**: replays every row through pure reducers and raises
   VIEW_MISMATCH if the stored traits disagree.
7. Typed reason order fixed: BAD_SCHEMA → BAD_ID → BAD_N → BROKEN_CHAIN → TAMPERED → VIEW_MISMATCH.

## Artifacts

- `mag/wow_player.py` — player-file ledger (schema wow_player.v1)
- `tests/test_wow_player.py` — 17 falsifier tests, all green
- `watch/inbox/wave_20260916/w2_union_prompt.md` — editor contract (fixed before the draft)
- `watch/inbox/wave_20260916/w2_union_draft.txt` — union-alpha's raw draft (13808 chars)

M2 falsifier MET: state survives restart byte-identical, proven cross-process.
