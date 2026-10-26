# LW4 REALMD CLIENT (2026-09-30)

Lane: last mile LW4, seat: ZCode subagent. Ownership: `tools/realmd_client.py` (new),
`tests/test_realmd_client.py` (new). No commit.

## Answer: YES, the handshake completed

The pure-stdlib SRP6 client connected to the live realmd (WSL, 127.0.0.1:3724), completed
CMD_AUTH_LOGON_CHALLENGE, computed M1, sent CMD_AUTH_LOGON_PROOF, the server answered with
M2, the client verified M2 (`m2_verified: true`), then fetched and parsed the realm list
(realm "MaNGOS" at 127.0.0.1:8085). End-to-end proof: realmd persisted sessionkey
`E569DA13...A00C` to `realmd.account` for LW4PROBE and it equals the client's derived K
(same bignum; the DB stores big-endian hex, the client buffer is little-endian order).
Wrong password is refused at proof stage with the 4-byte UNKNOWN_ACCOUNT (0x04) reply,
so the M1 agreement is genuinely checked, not assumed.

## What was built

- `tools/realmd_client.py` (379 lines): registration math (`srp6_x`, `srp6_verifier`,
  `verifier_sql`), packet builders (challenge / proof / realm-list request), parsers
  (challenge / proof / realm list, typed `ProtocolError` refusals), `client_session`
  (full client-side SRP6), `handshake()` live flow, CLI (`-u USER -p PASS`, or
  `--verifier USER PASS SALT_HEX` to arm a fixture account).
- `tests/test_realmd_client.py` (276 lines, 17 tests): DB vector (reproduces the exact
  v hex stored in the live account table), golden vector (pinned A/B/S/K40/M1/M2),
  server differential (SRP6.cpp formulas re-implemented in the test must agree with
  `client_session`), byte-shape tests for every builder and parser, two live tests
  (self-skip when realmd is down): full handshake + wrong-password falsification.
- Fixture account armed via mariadb: `LW4PROBE` / `LASTMILE` (id 6), v/s computed by the
  module itself (dogfood), salt `7E5C1A94...6978`. The `estate` account keeps empty v/s.

## The load-bearing findings (bytes, not reports)

1. **Every big number in this protocol is LITTLE-endian** (BigNumber.h:84
   `AsByteArray(minSize=0, reverse=true)`; SetBinary reverses input). N arrives on the
   wire as `B7...` (reversed hex), salt arrives reversed, A/M1/K hash inputs are
   little-endian minimal (trailing zeros stripped). A textbook big-endian SRP6 client
   fails against this server. Oracle: the known N constant in the challenge reply.
2. **The challenge size field is little-endian** on this build: the server reads it
   natively (EndianConvert is a nop on x86, ByteConverter.h:57-60; AuthSocket.cpp:310-315
   converts bytes 0-1, not the size). Empirical: LE size got a 119-byte reply, BE size
   made the server wait forever. (Some public docs claim big-endian; this build's bytes
   say otherwise.)
3. Challenge reply has NO length bytes for B (32, forced) or s (32); g and N have 1-byte
   length prefixes. Salt is sent minimal (`s.AsByteArray(), GetNumBytes()`), so a
   leading-zero-byte salt shortens the packet: fixture salts must keep the top byte
   nonzero (ours does).
4. M1 is the mangos variant `sha1(sha1(N)^sha1(g) || sha1(I) || s || A || B || K)` with
   every operand in LE-minimal form (SRP6.cpp:46-73); K is the WEAVE (not concat) of
   sha1(evens) and sha1(odds) over S's 32 LE bytes (SRP6.cpp:117-143).
5. `crc_hash` can be zeros: VerifyVersion returns true immediately when
   `StrictVersionCheck` is off (default, AuthSocket.cpp:1011-1013).
6. Server edge honored: SRP6::Proof memcmp's a 19-byte buffer as 20 when M1 ends in
   0x00 (SRP6.cpp:186-193); `client_session` regenerates `a` in that case (1/256 flake
   documented, not papered over).
7. realmd was NOT running when the lane started; booted in WSL
   (`~/mangos-wotlk/build/src/realmd/realmd -c realmd.conf`, pid verified, log
   `/tmp/realmd_lw4.log`, realm "MaNGOS" registered). MariaDB already up; account table
   base accounts + estate present.

## Gates + counts

- `pytest tests/test_realmd_client.py -q -p no:cacheprovider` (2026-09-30, this seat):
  **17 passed** in 0.98s (15 offline vectors/shapes + 2 live: full handshake and
  wrong-password refusal; realmd was up).
- Full-suite attempt `pytest -q -p no:cacheprovider --ignore=tests/test_behavioral_awareness.py`:
  died silently at ~38% in the background pipe, no failure line surfaced before the cut.
  Honest status: not completed on this seat; my file is green standalone. Pre-existing
  and unrelated: `tests/test_behavioral_awareness.py` fails COLLECTION with committed
  git conflict markers (`<<<<<<< Updated upstream`), the only tests/ file with them.
- Ratchet `check --changed`: PASS (scope=0; both files are new/untracked). Module is 379
  lines (under the 400 bar), zero except-pass, zero em-dashes in both files.
- Census note: +1 test file, +17 collected (2,303/352 carrier is a 2026-09-27 snapshot;
  this landing is the drift to attribute at the next census refresh).
- Probes that settled the byte shapes: LE-vs-BE size A/B test, N-order oracle, 119-byte
  challenge parse, wrong-password refusal. Raw probe scripts were throwaway bash (not
  landed); the landed tests re-derive every shape.

Receipt chain: dissection header
`watch/inbox/game_platform_basecamp_20260929/HOW_A_REAL_SERVER_WORKS_20260929.md` (body
facts verified directly against the clone at `~/mangos-wotlk/src/realmd/AuthSocket.cpp`,
`src/shared/SRP6/SRP6.cpp`, `src/shared/Auth/BigNumber.{h,cpp}`, `AuthCodes.h`).
