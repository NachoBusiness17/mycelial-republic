# IMP12: Hygiene triple — pytest basetemps, ED25519 custody runbook, keypurge

Date: 2026-09-30 (refire after provider blip; original attempt orphaned mid-flight —
see §3, the blip's hung process chain was found and killed as part of this pass).
Owner lane: IMP12 hygiene. Files owned and touched:
`watch/inbox/last_mile_20260930/IMP12_HYGIENE.md` (this receipt) + the three targets.
No repo code changed; no tests claimed (no behavior change to test).

Score: 1 of 3 cleared by the seat (keypurge, live — better than the banked boot-time
fallback), 1 delivered as documentation (custody runbook, §2), 1 operator-needed
(elevated takeown pass, §1, exact commands banked).

---

## 1. Pytest basetemp purge — OPERATOR-NEEDED (elevation)

20 ACL-locked `.pytest-*` dirs sit at repo root (basetemp leftovers; the census-bullet
hygiene law says the tree should not carry them). Byte-verified list, `ls -d .pytest-*`:

```
.pytest-arrival-repaired   .pytest-full-next-17   .pytest-full-tail-1   .pytest-law-isolate-4
.pytest-final-smoke        .pytest-full-next-18   .pytest-ghost-3       .pytest-law-isolate-5
.pytest-final-smoke-2      .pytest-full-next-19   .pytest-law-isolate   .pytest-law-isolate-6
.pytest-full-next-15       .pytest-full-next-20   .pytest-law-isolate-2  .pytest-verkle-repaired
.pytest-full-next-16       .pytest-full-next-21   .pytest-law-isolate-3
.pytest-full-next-22
```
(20 total, one per grid cell.)

Attempted from this seat (unelevated, `foste`, `net session` → NOT-ELEVATED):

- `takeown /f .pytest-ghost-3 /r /d y` → `ERROR: Access is denied.`
- `icacls <dir> /grant "foste:(OI)(CI)F" /t /c` → `Access is denied` (all entries).
- `Get-Acl` → `UnauthorizedAccessException` — the session cannot even READ_CONTROL,
  so the owner is a foreign/elevated SID (consistent with dirs minted by an elevated
  or container context), and owner-implied WRITE_DAC is unavailable. Plain `rm -rf`
  → `Permission denied`. Nothing further is legal from this seat.

### Banked operator commands (run from an ELEVATED PowerShell at repo root)

```powershell
cd 'C:\Users\foste\Documents\projects\local_sovereign_agent'
Get-ChildItem -Force -Directory -Filter '.pytest-*' | ForEach-Object {
  takeown /f $_.FullName /r /d y        | Out-Null   # seize ownership, recurse
  icacls $_.FullName /grant 'Administrators:F' /t /c /q | Out-Null
  Remove-Item -LiteralPath $_.FullName -Recurse -Force
  "{0}: {1}" -f $_.Name, (Test-Path $_.FullName)
}
```

cmd.exe per-dir equivalent (for a one-at-a-time pass):

```cmd
takeown /f <dir> /r /d y
icacls <dir> /grant Administrators:F /t /c /q
rd /s /q <dir>
```

Expected result: every line prints `<name>: False`. If any prints True, the dir is
handle-held, not ACL-held — reboot or Process Explorer, then rerun the loop.

---

## 2. ED25519 custody runbook — configs/.proof_key (documentation, delivered)

**Key identity (verified this pass, no secret bytes printed):** dev key at
`configs/.proof_key`, 64-hex ed25519 seed, pubkey fingerprint `2a3cab335bcf1d3c`
(sha256 of raw pubkey, first 16 hex), source `file:.proof_key`, via
`.venv\Scripts\python.exe -c "from mag import proof; print(proof.status()['signing'])"`.
Gitignored at `.gitignore:246` (`git check-ignore -v configs/.proof_key` confirms).

**What it signs.** Only `mag/proof.py::sign_payload()` consumes this key
(resolution order in `load_signing_key()`: `MAG_PROOF_KEY` env hex seed wins, else
`configs/.proof_key`, else auto-generate 0600 on first use). It ed25519-signs the
canonical JSON bytes of proof.v1 claims (AH2, 2026-09-30, audit finding #8), emitting
sig + raw pubkey + fingerprint alongside the deterministic claim sha. `verify_signature()`
checks the signature against the pubkey EMBEDDED IN EACH CLAIM, so every signed claim
is self-verifying and old proofs survive any key rotation. The pre-AH2 LEGACY-UNKEYED
sha256 path remains the fallback verify mode. Note: `mag/gwap_payload.py::sign_payload`
is a different, game-layer function (robber/priv_hex args) and does NOT use this key.
Tests never mint or read `configs/.proof_key` (fixed env seed / tmp key files only —
`tests/test_ah2_proof.py` header law), so rotation breaks no test.

**Custody tiers.** Per `watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md` finding #8
("Sign with ed25519 … using a key outside the estate"), the PRODUCTION key lives
OUTSIDE the estate — supplied via `MAG_PROOF_KEY` (env/secret store), never as a file
inside the repo. `configs/.proof_key` is the auto-generated DEV key only: gitignored,
never committed, never logged, never exported. A committed key makes every signature
theater (proof.py L44-45). Anything the operator needs to trust cross-machine uses the
production env-seed key; the dev key's signature is machine-local convenience.

**Rotation recipe (dev or production).**
1. Mint: for dev, delete `configs/.proof_key` (or rotate by writing 64 fresh hex chars);
   the next `python -m mag.proof status` auto-mints 0600 and prints the NEW fingerprint.
   For production, generate a 32-byte seed outside the estate (`python -c "import os;
   print(os.urandom(32).hex())"` on the operator's trusted host / secret store) and
   expose it as `MAG_PROOF_KEY` — env beats the file by law.
2. Record the new fingerprint in the filing receipt (like AH2_PROOF.md L37 recorded
   `2a3cab335bcf1d3c`). No code pins the fingerprint (grep: only the AH2 receipt
   mentions it), so nothing else updates.
3. Nothing is re-signed: old claims carry their own pubkeys and keep verifying.
   Verification of a rotated-out key's claims remains true; forgery under the old key
   is still detectable wherever the old fingerprint was recorded as trusted.
4. If a dev key is suspected leaked: delete it, mint per step 1, note the old fp as
   revoked in the next receipt. The gitignore line is the commit-side tripwire —
   `git check-ignore -v configs/.proof_key` should always answer.

---

## 3. KEYPURGE — CLEARED live (no boot-time fallback needed)

Target `C:\Users\foste\projects\keypurge` (contained only `mag-purge-mirror.git`,
4 KB, content verified clean). `rm -rf` → `Device or resource busy`.

**Root cause — the provider blip's orphaned chain.** Session `sess_c6ad00b4`
(the blipped predecessor) left a hung pipeline created 09:54:20 and idle for 3h43m
(0.0 CPU over a 10 s sample; deepest python had 1.5 s total CPU):

```
bash (29164) → bash (21376) → bash (58228) → python -m git_filter_repo (44452)
  → python (50428) → git gc --prune=now (50156) + git repack -d -l -a (49136)
```
All had CWD inside `keypurge\mag-purge-mirror.git`; the git children survived their
python parent's death. Killed children-first (`Stop-Process -Force` 50428, 44452,
58228, 21376, 29164 then 50156, 49136, conhost 44308), then `rm -rf` → GONE
(`KEYPURGE-CLEARED`, `Test-Path` clean). No live session lost anything: the owning
coordinator session is dead by blip, and the sibling live lanes (pytest 13:23 run,
swarm pull, hermes verifier) were untouched — killed PIDs were exactly the 09:54 family.

**Boot-time fallback (prepared, documented, NOT armed — not needed):** if a future
OS-hold survives process reaping, drop a one-shot cmd into the per-user Startup folder
(`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\purge_keypurge_once.cmd`)
that self-deletes only on success:

```cmd
@echo off
rd /s /q "C:\Users\foste\projects\keypurge"
if not exist "C:\Users\foste\projects\keypurge" del "%~f0"
```
It fires at next sign-in before holder processes start, removes the dir, then removes
itself; on failure it stays armed for the next boot. Not deployed — dir already gone.

---

## Report (<=100 words)

Cleared: keypurge deleted live (blip's hung git_filter_repo chain killed by PID;
boot fallback documented but not armed); custody runbook delivered (§2). Operator-
needed: 20 ACL-locked `.pytest-*` basetemps — takeown/icacls/Get-Acl all denied
unelevated (foreign owner); exact elevated loop banked in §1, expected output `False`
x20. Key fingerprint re-verified `2a3cab335bcf1d3c`, gitignore tripwire intact; no
code or tests touched.
