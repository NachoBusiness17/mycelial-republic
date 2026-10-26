# SS-1 SEED-SEAL LANDED - lane fill-seed-seal, division B, 2026-10-01

The owed waltz from GAP_REGISTER rank 5
(`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`, fill spec 5 + a07-r3
ticket SS-1) and the pam.md port spec
(`watch/inbox/localfirst/pam.md`, clause "The estate port"): the estate's
verify_seal was PAM-class by construction (hashes-only, manifest and seal in
the same writable domain), the Ed25519 port spec existed and never landed,
zero .seal sidecars existed. All of that is now landed, armed, and
forge-drilled. The ENFORCING FLIP is deliberately left operator-gated.

## What landed (byte-cited)

1. `mag/seed_seal.py` - the seed_signer module, schema seed_seal.v1.
   - Sign-the-root-not-the-body, per spec clause 1:
     `seed_root = sha256(canonical_json{arc_root, chain_sha, seed_sha, session})`
     (canonical = sort_keys, tight separators, ensure_ascii, utf-8;
     `mag/seed_seal.py` canonical_root), Ed25519 signature over the
     seed_root hex utf-8 bytes. The root covers BOTH file byte strings
     (seed .md AND chain .json) plus the arc identity, so no body byte sits
     outside the signature - the exact opposite of PAM's narrow ID-list root
     (pam.md section 6, their spec-vs-code drift).
   - Key custody, NOT PAM's way (spec clause 3): private key hex seed at
     `state/keys/seed_seal_key`, minted on first use, chmod 0600 attempted
     (succeeded: `state\keys\seed_seal_key (chmod 0600)` in the sign output),
     gitignored by `.gitignore:40` (`state/`) - byte-proven by
     `git check-ignore -v` exit 0 in the check file section 5. The PUBLIC key
     travels inline in the .seal sidecar (the verifying falsifier may be a
     stranger seat) and `key_id` = sha256 over domain-separated pubkey bytes,
     16 hex (`de5fc05e962c43ab`), gives strangers a rotation path. Shape
     follows the landed AH2 pattern in `mag/proof.py` (hex-seed keyfile,
     mint-on-first-use, never committed).
   - Verify-at-consume FAIL-CLOSED (spec clause 2): `verify_seed()` recomputes
     both shas from bytes on disk, takes session/arc_root from the chain json
     (never the seal's own word), rebuilds seed_root, cross-checks every seal
     field, then verifies the Ed25519 signature with the inline pubkey. Every
     failure path returns ok=False with the reason. There is no code path
     that returns True by silence - that exact shape is PAM's SEC-005 defect,
     live-proven in `watch/inbox/gala_20260925/localfirst-steal/lanes/pam.check.txt`
     section 4, and pinned refused by test.
   - CLI: `python -m mag.seed_seal sign|verify|keyinfo`.
2. One real .seal sidecar:
   `watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal` over the
   pam.md-cited real seed (`arc_root: eacb5b32e9ad5b9a`, session
   sess_f4ad2dcb, chain `arc_chain_sess_f4ad2dcb_20260907_0026.json`).
   seed_root `426b74e13707cba9...c440c1`; the re-sign run reproduced the same
   seed_root, key_id and signature (deterministic root; only sealed_at moved).
3. The forge-drill test: `tests/test_seed_seal.py`, 14 tests, ALL PASS
   (0.96s). The named drill is `test_forge_drill_seed_body_tamper_with_full_rehash`:
   tamper seed bytes, RECOMPUTE seed_sha, patch the seal's seed_sha AND
   seed_root with the attacker's honest-looking values (PAM check [3]'s
   attacker), assert the verifier refuses - the signature is the one thing an
   attacker without the key cannot mint. Also pinned: chain-tamper full
   rehash, session swap, stripped signature (PAM SEC-005 shape) refused not
   silent, missing seal fail-closed, byte drift fail-closed, self-consistent
   pubkey/key_id swap refused, wrong-key signing refused, key mint-once-reuse,
   and the real repo seal verifies green.
4. THE ENFORCING FLIP IS NOT LANDED (the SS-1 boundary, operator-gated):
   nothing in `mag/arc_seed.py` or any consumer refuses an unsealed or forged
   seed yet. The flip, when the operator orders it: call
   `mag.seed_seal.verify_seed()` at the consume site and treat ok=False as
   fatal (fail-closed), plus decide key ceremony (who holds
   state/keys/seed_seal_key, rotation cadence). Until then the capability is
   armed and opt-in.

## Checks run this session (raw output)

`watch/inbox/gala_20260925/fillball-1001/lanes/fill-seed-seal.check.txt`:

- [1] `python -m mag.seed_seal sign watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.md`
  exit 0, key_id de5fc05e962c43ab.
- [2] `python -m mag.seed_seal verify watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.md`
  exit 0, ok=true, session + arc_root match the chain.
- [3] `.venv/Scripts/python.exe -m pytest tests/test_seed_seal.py -v` -
  14 passed, exit 0.
- [4] `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
  final run: PASS, NEW=0, exit 0. Honest history: my first run exited 1 with
  NEW=4 - one was MINE (except-pass at mag/seed_seal.py:63, the stdout
  reconfig handler copied from proof.py's registered-debt shape; fixed in
  code, not by acceptance), three were in staged files I did not touch
  (tools/field_experiment.py, tools/hermes_burn.py, tools/model_garden.py);
  between my runs a concurrent lane ran baseline-update accepting those by
  name (final scope=16, hits=5, registered=5). One GROWTH warning stands on
  mag/percolator.py (accepted 580, now 738) - not this lane's file.
- [5] `git check-ignore -v state/keys/seed_seal_key` exit 0 (`.gitignore:40:state/`).
- [6] landed artifacts listed; [7] seal content shown (pubkey only, never the
  private key); [8] zero em-dashes in both landed code files.

## Decision ledger

Closes: SS-1 (GAP_REGISTER rank 5 / a07-r3) - the seed-seal Ed25519 port is
landed, sealed on a real seed, and forge-drilled; the estate no longer has a
PAM-class verify_seal as its ONLY seed trust anchor. No prior decision
reversed. Deliberately NOT closed by this lane: the enforcing flip (consume
refuses unsealed seeds) and key ceremony - both stay with the operator, per
the ticket boundary "capability armed but not enforced".

## Honest gaps

- win32 key custody is 0600-attempted (succeeded this run) but the durable
  guarantee is gitignore + never-commit, same accepted debt as mag/proof.py;
  DPACL/DPAPI port stays named debt (pam.md section "Honest gaps").
- Only ONE seed carries a sidecar (the ticket says one real seed; the
  c424b80a seed remains unsealed and `verify_seed` fails closed on it, which
  is the correct armed-not-enforced posture).
- The full-repo pytest suite was NOT run (the ask names the forge drill as
  the finish-line test); the named test file is 14/14.
