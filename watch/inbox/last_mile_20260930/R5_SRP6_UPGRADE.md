# R5 — SRP6 UPGRADE: RFC 5054 2048-bit + SHA-256 default, mangos behind compat flag

Q04 / V2ASK1 build · 2026-09-30 · owner lane: R5 (files owned: `server/auth_srp6.py`, `tests/test_auth_srp6.py`) · no commit made by this lane.

## The verdict read (step 1)

`watch/inbox/frontier_asks/volley2/results/V2ASK1.md` (Q04 decision tree): 256-bit mangos SRP is
inside reach of off-the-shelf DLP tooling — one logged login yields K, one leaked verifier is a
password-equivalent forgery kit. Tree: federation-width → OPAQUE; one-stranger-first +
"operator never sees the password" promised → Option A (SRP-2048/SHA-256, benchmark F4.2 first);
otherwise → Option B (TLS + memory-hard hash), which the full verdict RECOMMENDED for a
stranger-reusing-passwords world (scrypt-at-rest beats a fast SHA verifier).

**Branch built (operator's call, this mission): Option A.** The SRP6 account system is B4's
headline promise (server never sees the password), so the default becomes RFC 5054 2048-bit +
SHA-256; Option B stays the named successor if the promise is ever traded away (`auth_v2`
replaces, not amends).

## What landed (step 2)

`server/auth_srp6.py` (schema auth_srp6.v2):

- **`rfc5054-2048` is the DEFAULT** for every new registration and decoy challenge: RFC 5054
  Appendix A.2 #3 group (N byte-checked against the RFC text: 2048 bits, probable prime, safe
  prime q=(N-1)/2), g=2, SHA-256, big-endian PAD() to |N|, k=H(N|PAD(g)), x=H(s|H(I|":"|P)),
  u=H(PAD(A)|PAD(B)), K=H(PAD(S)), M1/M2 in the RFC 2945 [SRP-RFC] evidence shape (no published
  RFC vector — certified by cross-derivation), identity hashed verbatim, 16-byte salt.
- **`mangos-256` behind the compat flag**: `Srp6AuthService(..., allow_mangos=True)` (default ON
  — the CMaNGOS training path keeps it). Math stays the imported proven bytes from
  `tools/realmd_client` (anti-drift law; the differential test proves M1/M2/K byte-identity with
  `client_session`, the math wire-verified against live realmd 2026-09-30). `allow_mangos=False`
  RETIRES it: mangos register and grandfathered challenge raise ValueError → the server's
  existing typed BAD_AUTH path; no new verb, no wire change.
- Dialect surface (`SrpDialect`: normalize/ident_of/x_of/verifier/multiplier/public_b/u_of/
  server_s/session_key/m1_of/m2_of/salt_decode) — `tools/mountain_selfplay.py` (sibling lane)
  already drives its client through exactly this interface, verified green.
- `begin_challenge` result now carries `"group"` for the follow-up that puts it on the wire
  (server.py drops it today; the selfplay client documents the "own account state names the
  dialect" contract meanwhile).

## Client-side bigint question (verdict's answer, adopted as law in the docstring)

GDScript has no bigint: a 2048-bit client needs a hand-rolled bignum — 30-bit limbs (products
fit int64), Montgomery reduction, ~69 limbs, ~10k limb ops/modmul, ~3 exponentiations with a
≥256-bit ephemeral = ~15M limb ops ≈ **2–8 s at login (verdict inference)**. The F4.2 benchmark
on the slowest target device is owed BEFORE any client ship; wire stays plain lowercase-hex
integers to keep the client limbs byte-simple.

## Migration note (step 4): grandfather, never force

Verifiers are group-bound (a 2048-bit verifier cannot be recomputed from a 256-bit one), so
forced migration would mean forced re-registration. Instead: every new row carries `"group"`;
**B4 rows without "group" are grandfathered as mangos-256 and keep authenticating
byte-identically** while the compat flag is on; the NEXT re-registration (same op, same
password) silently upgrades the row to rfc5054-2048. Flip `allow_mangos=False` to retire.

## Certification (step 3) — tests/test_auth_srp6.py, 19 passed

- **RFC 5054 Appendix B vectors** replayed through the dialect API (1024-bit + SHA-1 instance):
  k, x, v, A, B, u, server premaster AND the client §2.6 premirror all equal the published
  bytes; 2048-bit N is the RFC constant (bit length + probable-prime + safe-prime checks).
- **Roundtrip both groups** over the real TCP wire (register → challenge → proof → welcome with
  verified M2 → world action acks): rfc5054-2048 default AND mangos compat (the mangos client
  is `tools.realmd_client.client_session`, the proven bytes).
- **Wrong password rejects BAD_PROOF in BOTH groups**, burn-at-receipt STALE_CHALLENGE on the
  consumed challenge, recovery on fresh challenge.
- Plus the standing B4 laws re-pinned: replay/nonce, decoy no-enumeration (default-dialect
  shapes), typed malformed refusals (per-group N, 32-byte RFC M1), grandfather + upgrade,
  compat-flag retirement over the wire (BAD_AUTH), fallback flag, frozen table rows, DEFAULT
  digest unmoved.

## Suite numbers (instrument, moment, delta — census law)

- `pytest tests/test_auth_srp6.py -q` → **19 passed** (2026-09-30, this lane; B4 baseline was
  13 — +6 inside one existing file: vectors, default-group, grandfather/upgrade, compat-flag,
  dual-group wire roundtrips).
- Focused executed runs (this refire, 2026-09-30 ~21:30 EDT): `pytest tests/test_auth_srp6.py -q` →
  **19 passed in 2.62s**; with `tests/test_frame_mac.py` + `tests/test_realmd_client.py` →
  **52 passed in 5.69s** (the R3 MAC layer and the realmd differential green against the new module).
- Full suite `pytest -q` (this refire, started ~21:36 EDT): run KILLED at 22% progress
  (harness/box load — 19 python.exe from sibling lanes; no summary line, so no count is filed;
  2 F dots visible in the 14–16% window, unnamed — attribution requires a completed summary).
  The census law outranks a filled placeholder: no full-suite number is claimed.
- Instrument-read partials and blast radius (same refire window, each a completed summary line):
  neighbors `tests/test_realmd_client.py + test_protocol_table.py + test_identity_binding.py +
  test_server_v0.py` → **100 passed**; SRP6 consumers `tests/test_frame_mac.py +
  tests/test_mountain_selfplay.py + tests/test_wow_world.py` → **41 passed** (mountain_selfplay
  drives the R5 dialect surface end to end over the wire); `tests/test_server_persist.py` → 5
  failed / 2 passed (the pre-existing reds below). A later verbose-instrument attempt
  (`pytest -v --tb=no --ignore=tests/test_census_drift_patrol.py`, persisted log) was also
  externally killed (exit 137, no assertion), at tests/test_ghost.py after **1,356 passed /
  1 failed** — the 1 being `tests/test_container_setup.py::test_compose_binds_localhost_only`
  (docker-compose binding check, outside this lane's files, pre-existing). Killed-run partials
  are a different instrument from any census count; no delta is claimed against the AGENTS.md
  carrier (2,303 collected / 352 files, 2026-09-27).
- Pre-existing reds NOT this lane (verified by hermetic repro / stash): `tests/test_server_persist.py`
  5 failures (fail with this lane's diff stashed too); `tests/test_census_drift_patrol.py::
  test_cli_collect_names_the_zero_collect_instrument_gap` (patrol tool flipped ZERO-COLLECT to
  exit-1 at ecf47999a 2026-09-29 23:01 after the test was written 10:19 — owner: patrol lane);
  `tests/test_container_setup.py::test_compose_binds_localhost_only` (outside this lane's files).

## Provenance note (shared tree)

This lane made NO commit. The sibling R12/D-wave commit `0b846c01f` (2026-09-30 19:20:42,
"server bytes committed — existed NOWHERE ELSE") swept this lane's then-current
`server/auth_srp6.py` into HEAD; HEAD's copy is byte-identical to the working tree
(sha1 f37bc89820715d6361390882053550f601059af4). A later sibling commit (`860adcb60`) likewise
swept the lane's `tests/test_auth_srp6.py` (digest above). This lane's only uncommitted delta
is this receipt.

## Refire addendum (2026-09-30 ~21:30 EDT): byte truth re-proven

The first R5 pass died before certification; this refire re-verified every claim against bytes:

- **Constants vs the live RFC text:** `rfc-editor.org/rfc/rfc5054.txt` downloaded fresh
  (44,445 B); EVERY constant proven verbatim by whitespace-stripped containment — the 2048-bit
  N (512 hex chars), g=2 in Appendix A.2 #3, and all Appendix B vectors (s, k, x, v, a, b, A,
  B, u, S, the 1024-bit N, "alice", "password123"). "Byte-checked" is re-proven, not trusted.
- **Digests:** `server/auth_srp6.py` sha256 `c35a8083a5d564a92940733648c7292549fa117d5fab251f4d7301e1cdc6e4d6`
  (= HEAD, empty diff); `tests/test_auth_srp6.py` sha256 `214d39a1f4c5c7661e4bab34980df4dd6b44f351166b011fea16cc217d2ab566`
  (working tree, uncommitted).
- **The persist-failure non-involvement was re-checked by scope, not stash:** `.git/index.lock`
  is intermittently held by sibling lanes (a mid-lane `git stash` fails harmlessly; the
  pre-existing `stash@{0}` from `e0ff8cec0` belongs to another session, untouched). The 5
  `test_server_persist.py` reds run against HEAD bytes for every module they load — R5's only
  working-tree change (`tests/test_auth_srp6.py`) is not in their import graph.
- **CLI self-check:** `python -m server.auth_srp6` prints usage, exit 0.
