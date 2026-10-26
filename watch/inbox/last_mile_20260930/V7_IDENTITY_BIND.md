# V7 — IDENTITY BINDING: FIRST CONTACT SIGNED BY THE GITHUB-PUBLISHED SSH KEY (2026-09-30)

Lane: lensing C1 step 4. Mission: build the server-side half of SSH-key identity binding NOW so first contact is identity-bound the moment Adam's username arrives. No commit (operator's fence). File ownership kept: `server/identity_binding.py` + `tests/test_identity_binding.py` + this receipt; no other file touched.

## Why (the LW2 stop, closed from the other side)

LW2 refused the invite: no GitHub username for Adam exists in the estate, both guesses 404'd, and a push-permission invite to a guessed handle would grant a possible stranger write access — the identity-skipped-for-resemblance failure. This module is the other half of that stop: when the REAL username arrives, the server binds the claim to the SSH key GitHub itself serves at `https://github.com/<user>.keys`. Adam proves ownership the standard way — an sshsig signature (`ssh-keygen -Y sign`) — and the server verifies it the standard way (`ssh-keygen -Y verify`). No password, nothing stored that he did not already publish.

## What landed

| File | Change |
|---|---|
| `server/identity_binding.py` | NEW. `fetch_github_keys` (stdlib urllib, timeout 10s, no auth, exact URL `github.com/<user>.keys`, 64KiB cap) → strict `parse_public_keys` (known keytype + valid base64 + agreeing wire-type, no silent skip); `IdentityBindService` (`mint_challenge` / `verify_proof` / `drop`): nonce (32 hex, `secrets`) + issued + expires (300s TTL) in an exact-bytes challenge template, pending SINGLE-USE per connection, burned at proof receipt (the srp nonce law), expiry enforced server-side; verify = temp allowed_signers file + `ssh-keygen -Y verify -f <signers> -I <user> -n core -s <sig>` with the challenge bytes on stdin; fingerprint parsed from the Good line and cross-derived in hashlib (`PublicKeyLine.fingerprint`, `ssh-keygen -lf` shape). CLI probe: `python -m server.identity_binding <username>` |
| `tests/test_identity_binding.py` | NEW. 41 tests. Every keypair LOCALLY GENERATED at test time (`ssh-keygen -t ed25519 -N ""`, comment `mag-test-fixture`) — never a real key, never the network (fetch surface tested against a fake `urlopen`). The peer side of the roundtrip is real ssh-keygen, the reference implementation |
| `server/protocol_table.py` | NOT touched (fence). The frozen rows live in `identity_binding.py` — see the table law below |

## The table law (srp pattern, B4)

`IDENTITY_AUTH_TABLE` compiles the DEFAULT rows plus `identity_challenge` / `identity_proof` as frozen data rows (`required_state` CONNECTED — pre-auth by definition, the B4 precedent; handlers `auth_identity_challenge` / `auth_identity_proof`; `reject_code` UNKNOWN_SID as the reserved never-fires slot). The dialect's real laws ride the closed reject VOCABULARY, never per-verb rows (the LW6/LW7 law): `STALE_CHALLENGE` (no pending / user mismatch / expired — the replay law), `BAD_PROOF` (wrong key, tampered bytes, wrong namespace, bad armor, subprocess failure), `NO_KEYS` (fetch failed or login publishes nothing). Ownership kept the table in `identity_binding.py`, compiled via the shared `compile_table` — promoting it to `protocol_table.py` (B4's placement) rides with the server.py wiring lane.

## The exact flow Adam follows (byte-truth)

1. Server mints (op `identity_challenge`, user = his GitHub login) and hands him the challenge string — five lines, no trailing newline:
   ```
   the-mountain identity binding v1
   user: <username>
   nonce: <32-hex>
   issued: <UTC ISO-8601>
   expires: <UTC ISO-8601, issued + 5min>
   ```
2. Adam saves it EXACTLY as delivered (byte-exact — an editor adding/stripping a trailing newline moves the signed content and the proof rejects; that is the signature working) and signs with the private half of a key published on his GitHub account:
   ```bash
   ssh-keygen -Y sign -n core -f ~/.ssh/id_ed25519 < challenge.txt > challenge.txt.sig
   ```
   (stdin form, verified live on this box's OpenSSH 10.3p1: "Signing data on standard input", armor to stdout. The everyday file form works identically: `ssh-keygen -Y sign -n core -f ~/.ssh/id_ed25519 challenge.txt` → `challenge.txt.sig`.)
3. Adam returns the armor (`-----BEGIN SSH SIGNATURE-----` ... ) as op `identity_proof`. Server: `ssh-keygen -Y verify -f allowed_signers -I <user> -n core -s <sig>` with the challenge on stdin; exit 0 + `Good "core" signature for <user> ... SHA256:<fp>` ⇒ bound, fingerprint filed.

Dialect note (probed 2026-09-30, both binaries on this box — Git's OpenSSH 10.3p1 and System32 OpenSSH): modern ssh-keygen (8.2+) takes the allowed_signers file via `-f` after `-Y verify` and the MESSAGE on stdin; the old positional-tail form is refused ("Too few arguments for sign"). The Good line rides stderr on Unix but STDOUT on Windows OpenSSH — the server searches both (exit code is the verdict; the line only yields the fingerprint).

## The laws

- **Username = injection law.** GitHub login grammar (alphanumeric + inner hyphens, 1-39) validated before anything; the name is interpolated into a URL, an allowed_signers principal line, and an `-I` argument — the grammar forecloses traversal, queries, spaces, newlines on all three surfaces.
- **Strict parse.** A key list with junk in it is not a key list: unknown keytype, bad base64, or a blob whose embedded wire-type disagrees with the line type all raise typed `IdentityError`. Nothing silently skipped.
- **NO_KEYS is signal, not leak.** The username is the claimed identity, not a password: a 404 (no such user) or a 200-empty page (user publishes no keys — proven LIVE on `nachobusiness17`) is exactly the operator's "wrong username" signal LW2 needed. The no-enumeration law belongs to password surfaces, not this one.
- **Nonce law (srp, verbatim).** Pending challenges are single-use, keyed by connection, burned at receipt — success, failure, or garbage; a fresh mint burns the old; `drop` kills a dead connection's pending. Replayed proofs find `STALE_CHALLENGE`.
- **Exact bytes.** The challenge string has no trailing newline; the server verifies the same bytes it minted (stdin, utf-8, untouched). Armor-only hygiene: CRLF in the pasted armor is normalized; the message never is.
- **Fail closed.** Wrong key, tampered challenge, wrong namespace (`file` vs `core`), missing armor, missing ssh-keygen binary, subprocess timeout — all `BAD_PROOF`.

## Named deviations (fix comments carry the receipt)

- **`secrets` for nonces** — the auth_srp6 precedent: challenge nonces use real entropy (clock+counter would be guessable, and guessability is fatal to a signed-ownership proof). Determinism law governs the world log; auth material never enters it.
- **Network + subprocess** — urllib fetch and the ssh-keygen child are the point of the module. Tests stay deterministic: fake fetchers, generated fixture keys, no network.

## Digests (trust bytes; sibling contracts unmoved)

- `PROTOCOL_DIGEST d41f7cba635174628cfdff928555de340258ac6f33612dfb84217ff0958179cf` — DEFAULT byte-identical, matches B4/LW7's pin; `compile_table(None).digest == PROTOCOL_DIGEST` asserted in tests.
- `IDENTITY_AUTH_DIGEST 9de8ad04e75e2e1c46fadc844187a57f942b8c08542ff925760b08b2362b9897` — a NEW contract version.
- Siblings unchanged: `SRP6_AUTH_DIGEST 4981f23e...`, `CHAT_DIGEST 3ce934f5...`, `ANTICHEAT_DIGEST 5702c4d8...`, `MOTION_DIGEST ce259465...` (full values in `server/protocol_table.py`).

## Tests (real counts, this tree, this moment)

`tests/test_identity_binding.py`: 41 collected, 41 passed (2026-09-30, one run) — table law x2; username grammar x2 (5 accept + 15 refuse shapes); strict parse x3; fetch law x2 (exact URL/timeout/UA, 404/URLError/empty/503 typing); fingerprint vs `ssh-keygen -lf` reference; mint shape + lifecycle; typed refusals; roundtrip with real ssh-keygen; the Adam stdin-sign flow; wrong key; tampered bytes; wrong namespace; replay burn (incl. burn-on-garbage); expiry boundary (301 stale / 299 pass); user mismatch + armor laws; missing binary.

Sibling drift check, same tree, same moment: `pytest tests/test_protocol_table.py tests/test_auth_srp6.py tests/test_motion_rows.py tests/test_chat.py tests/test_anticheat.py tests/test_server_v0.py tests/test_realmd_client.py -q` → **151 passed**.

Live operability probe (by hand, not a test): `python -m server.identity_binding torvalds` → `1 key(s) published, SHA256:SlSdsTYgtT3jhz1QFhVbDqazjuoZLbtqMs8nIVqaL9A ssh-rsa`; `nachobusiness17` → typed `NO_KEYS ... publishes no usable keys` (the 200-empty path, live).

## Owed next (not this lane)

- `server/server.py` op-ladder wiring: gate `identity_challenge`/`identity_proof` through `IDENTITY_AUTH_DISPATCH` (the auth_srp_* enforcement-point precedent), `_grant_session` on a good proof (identity-bound sid), `stats()` counters.
- `server/protocol.py` wire builders + docstring rows; promotion of the table to `protocol_table.py` if that lane prefers B4's placement.
- Binding policy at grant time (does an identity-bound session outrank plaintext hello? flag shape mirrors `allow_plaintext_hello`).
- When Adam's username arrives: `python -m server.identity_binding <his-login>` first (the LW2 verify-it-first law), then the challenge mint against his real keys.
