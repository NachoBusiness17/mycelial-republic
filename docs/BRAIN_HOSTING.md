# Brain hosting: off-machine, multiple copies, append-only (2026-10-17)

> "Host the brain off machine, multiple backups, so it's literally a growing organism."

This doc covers:

- **the private brain**, which has several copies and only grows;
- **the public lattice**, a one-way mirror that needs your approval for each release;
- **the signed seat handshake** that guards the warm MCP doors;
- **seat-to-seat proposals**.

Everything here is copy-only and append-only: no target is ever synced, pruned or overwritten.

| piece | file |
|---|---|
| curated brain manifest | `scripts/brain_manifest.py` |
| replication + verify + restore | `scripts/brain_replicate.py` |
| targets | `configs/brain_targets.yaml` |
| public tier (one-way, approve-gated) | `scripts/public_lattice_manifest.py` → `PUBLIC_RELEASE_REVIEW.md` |
| seat handshake | `mag/seat_handshake.py`, `scripts/seat_keygen.py`, `configs/seat_allowlist.json` |
| seat proposals | `mag/proposals.py`, `scripts/proposals.py`, warm MCP tools `estate_propose` / `estate_review` / `estate_proposals` |
| receipts | `watch/receipts/brain_<utc>.json`, `watch/receipts/public_<utc>.json`, `watch/receipts/proposals/<id>/` |
| tests | `tests/test_brain_hosting.py` |

---

## 1. What "the brain" is

`scripts/brain_manifest.py` builds the curated set.

- **Warm pack:**
  - `memory/biography/verkle_tip.json`
  - `memory/warm_state.json`
  - `memory/zknot/LATEST.md`
  - `memory/rib_boot.json`
- **Library:**
  - `watch/LIBRARY/INDEX.md`
  - `catalog.jsonl`
  - every shelf's `*/LATEST.md`
- **Chain v2:** the top-level `memory/biography_v2/*.json(l)` files, including:
  - the row log `chain_v2.jsonl`
  - `checkpoints_v2.jsonl`
  - `tip_v2.json`

  It also takes `seed/` and `knots_v2/`.
- **Chain v1:** `memory/biography/verkle_chain.jsonl`, plus the v1 tip.
- **Backup:** the newest COMPLETE `memory/biography_backup/biography_backup_<date>/`. "Complete" uses the same rule as `scripts/backup_chain.py`: `BACKUP_COMPLETE.json` is present and `BACKUP_INCOMPLETE.json` is absent.
- **Verifier:** `scripts/verify_knot_v2.py`, so any copy can check itself.

Every file passes two screens taken from `mag/deepseek_direct_runner.py`: the path denylist (`is_denied`) and the redaction scanner (`redact_lines`). A file that trips either screen is **excluded**. Excluded files are listed by path only.

Nothing comes from `watch/inbox`, `memory/trajectory`, `.env*`, key files, `secret_gate_results` or `free_keys`.

## 2. The private tiers

```
repo ──(read once: hash + screen + write)──▶ LOCAL VAULT  C:\MagChainVault\brain\
                                               objects/<sha[:2]>/<sha>     (content-addressed)
                                               manifests/brain_manifest_<utc>_<sha12>.json
LOCAL VAULT ──robocopy /E /XC /XN /XO──▶ bob  \\100.125.103.60\MagBrain\brain   (Tailscale SMB)
LOCAL VAULT ──rclone copy --ignore-existing──▶ magbrain:  (crypt over gdrive:mag-brain/)
```

### How a run works

- The vault is the source of every other copy.
- New and changed files become new objects. Old objects and old manifests stay forever, so every earlier state can still be restored.
- **Verify:**
  - Local and SMB copies are checked by re-hashing every object listed in the manifest.
  - The crypt copy is checked with `rclone cryptcheck --one-way`, which compares hashes of the encrypted copy and downloads nothing.
- **Delete guard:** `guard()` refuses any command that contains any of these:
  - `sync`, `move`, `delete` or `purge`
  - `/MIR`, `/PURGE` or `/MOV`
  - any `--delete-*` flag
- **Skipping:**
  - bob is probed on TCP 445 first and skipped cleanly when it is offline.
  - The Drive copy is skipped with a message until `magbrain:` exists.

### Commands

```
.venv\Scripts\python.exe scripts\brain_replicate.py push               # vault + every reachable target
.venv\Scripts\python.exe scripts\brain_replicate.py push --local-only  # vault only
.venv\Scripts\python.exe scripts\brain_replicate.py push --only bob    # vault + bob
.venv\Scripts\python.exe scripts\brain_replicate.py restore --manifest C:\MagChainVault\brain\manifests\<file> --to D:\restore_test
```

## 3. One-time steps for Nacho

These are the steps the agents cannot do: sign-ins, passwords and shares.

### 3a. Private Drive vault (`magbrain:`)

1. **Optional: encrypt the rclone config itself.**
   - Run `rclone config`, choose `s) Set configuration password`, and type a password at rclone's own prompt.
   - After that, export it per session, or store it in Windows Credential Manager and set it in the scheduled task:

     ```
     $env:RCLONE_CONFIG_PASS = '<typed by you, never committed>'
     ```
2. **Create the Drive remote.**
   - Run `rclone config` → `n` (new remote).
   - Name it `gdrive_sd`, or reuse `gdrive_sd` / `gdrive_nacho` if they already exist on this PC.
   - Storage `drive`, scope `drive`. Sign in in the browser rclone opens.
3. **Create the crypt remote.**
   - Run `rclone config` → `n` (new remote). Name: `magbrain`. Storage: `crypt`.
   - Remote: `gdrive_sd:mag-brain`.
   - `filename_encryption = standard` and `directory_name_encryption = true`.
   - Type the password and salt (password2) at rclone's prompt. **Write both down offline: losing them loses the encrypted copy.**
4. **Check it.** `rclone listremotes` should show `magbrain:`. Then run:

   ```
   .venv\Scripts\python.exe scripts\brain_replicate.py push --only drive_private
   ```

The agents never run `rclone config`, never read `rclone.conf`, and never see these passwords. The replicator only calls `rclone listremotes`, `copy --ignore-existing` and `cryptcheck --one-way`.

### 3b. bob over Tailscale SMB

1. On bob, create a folder and share it as `MagBrain`. Grant read/write only to the account this PC uses. Allow SMB on the Tailscale interface only.
2. Create `\\100.125.103.60\MagBrain\brain`. Or change `path:` in `configs/brain_targets.yaml` to whatever share you chose.
3. Run `scripts\brain_replicate.py push --only bob`. When bob is offline, the run says `skipped` and carries on.

### 3c. Public Drive (`magpublic:`), a separate 5 TB account

1. Run `rclone config` → `n`. Name it `magpublic`. Storage `drive`, signed in with the separate public account. This is **not** crypt.
2. Never point `magpublic:` at the private account, and never nest it under `magbrain:`.

### 3d. Scheduled task (suggested, not created)

Run it as you, daily at 03:30, vault plus every reachable target:

```
schtasks /Create /TN "MagBrainReplicate" /SC DAILY /ST 03:30 /RL LIMITED /F ^
  /TR "\"C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe\" \"C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\brain_replicate.py\" push"
```

If you encrypted the rclone config, the task also needs `RCLONE_CONFIG_PASS`. Supply it from Windows Credential Manager through a small wrapper script; don't put it in the `/TR` string. The public tier is never scheduled.

## 4. The public lattice: a strict one-way mirror

Two Drives with two roles:

- **PRIVATE** (`magbrain:`) holds the whole brain, encrypted.
- **PUBLIC** (`magpublic:`) holds only the cleaned invariant lattice.

### What gets published

`scripts/public_lattice_manifest.py` uses a **strict allowlist**, not a denylist:

| public path | from (brain) |
|---|---|
| `law_cards.json` | `memory/rib_boot.json`, derived: `core_laws` plus law-rib heads and amendments only |
| `chain_v2/tip_v2.json` | the v2 chain root (n, root, chain_id, state_hash) |
| `chain_v2/checkpoints_v2.jsonl` | v2 checkpoints (currently `unsigned-pending-operator`, and they say so) |
| `verify/verify_knot_v2.py` | the stdlib verifier |
| `modules/<card>` | librarian module cards, once they exist (`watch/LIBRARY/modules/*.card.json\|md`) |

Nothing else is ever considered: no inbox, no memory bodies, no knots, no chain rows, no secrets.

### The one-way law

1. **The source is the private vault.** That means the newest vault manifest plus its objects, each re-hashed on read. The live repo is not read.
2. **Every published byte is masked.**
   - `warm_surface.redact_text` handles secrets, the repo path (→ `<repo>`), home paths (→ `<home>`) and tailnet IPs.
   - Any other IPv4 address becomes `<ip>` and any e-mail address becomes `<email>`.
   - The masked file is then re-scanned. A file that still trips the scan is excluded, path only.
3. **The public drive is write-only from our side.** The module can emit only two commands:
   - `rclone copy <local staging> magpublic:lattice/<sha> --ignore-existing`
   - `rclone check <local staging> magpublic:lattice/<sha> --one-way`, a hash and size compare whose output is discarded (only the exit code is kept)

   Nothing is ever read back into the brain, and no public content is trusted. `tests/test_brain_hosting.py::test_public_path_has_no_read_into_brain_path` asserts this, both by behaviour and statically.
4. **Nothing is ever pushed automatically.**

### Releasing

```
.venv\Scripts\python.exe scripts\public_lattice_manifest.py build
#   → C:\MagChainVault\public_staging\<sha>\payload\...  +  PUBLIC_RELEASE_REVIEW.md (repo root + staging)
#   read PUBLIC_RELEASE_REVIEW.md and the payload files
.venv\Scripts\python.exe scripts\public_lattice_manifest.py push --approve <sha from the review>
```

- `push` refuses unless `--approve` equals the staged manifest's sha.
- At push time it re-hashes every staged file and refuses if any file changed or any unlisted file appeared.
- Each release lands in its own folder, `magpublic:lattice/<sha>/`, and earlier releases are never touched.

## 5. Seat handshake (warm MCP doors)

Each request rides an envelope:

```json
{"mag_seat": {"seat_id", "ts", "nonce", "sig"}, "body": "<json-rpc string>"}
```

The signature is Ed25519 over `domain ‖ method ‖ sha256(body) ‖ seat_id ‖ ts ‖ nonce`.

- **Allowlist:** the server checks against `configs/seat_allowlist.json`, which holds public keys only.
- **Rejections:** the server rejects a skew over 60 s and any replayed nonce (bounded cache).
- **Silent failure:** a failed check gets no detail. HTTP `/mcp` returns a bare `404 {}`, and the TCP bridge closes the session.
- **Modes:** `MAG_SEAT_HANDSHAKE=off|optional|required`.
  - `off` is the default and keeps today's behaviour.
  - An unknown value counts as `required`.
  - The TCP bridge takes `--handshake optional|required`.
- **Library:** `cryptography` Ed25519, falling back to the pure implementation in `scripts/verify_knot_v2.py`.

### Getting a seat onto the allowlist

1. **The seat makes its own key.** It runs this on the machine where it lives:

   ```
   .venv\Scripts\python.exe scripts\seat_keygen.py --seat gemini
   ```

   - The private key goes to `%USERPROFILE%\.mag_seat\gemini.key`, or to `--out`.
   - Keygen refuses a path inside the repo and never overwrites an existing key.
   - Only the public allowlist row is printed.
2. **Nacho adds the row.** He pastes the printed row under `"seats"` in `configs/seat_allowlist.json`. To cut a seat off, set `"revoked": true`.
3. **The seat's client signs requests.**
   - Set `MAG_SEAT_KEY_PATH` to the key path.
   - For the container door, run `scripts\mcp_stdio_shim.py --sign`, which wraps every line.

## 6. Exposure: Tailscale first

- **Default.** The TCP bridge and HTTP `/mcp` stay on loopback. Nothing here opens a port.
- **Tailnet seats** (bob, phone, laptops):
  - Prefer `tailscale serve --tcp 8766 tcp://127.0.0.1:8766` on this PC, so the door is reachable only inside the tailnet.
  - Run the bridge with `--handshake required`. Tailnet ACLs are the outer wall and the seat signature is the inner one.
- **Cloud seats** (no Tailscale):
  - Put `cloudflared` in front of HTTP `/mcp` with a **Cloudflare Access** application.
  - Use a **service token** per cloud seat: `CF-Access-Client-Id` / `CF-Access-Client-Secret` headers, held by the seat's runtime.
  - Keep `MAG_SEAT_HANDSHAKE=required` behind it, so a leaked Access token alone still gets only `404`.
- Never use `tailscale funnel` or a public cloudflared hostname without Access.
- None of this is switched on yet. It's an operator decision.

## 7. Seat-to-seat proposals

Seats propose changes to each other through signed messages stored under `watch/receipts/proposals/<id>/`:

- `proposal.json`
- `review_<seat>_<utc>_<nonce>.json`
- `promotion_<utc>_<nonce>.json`

**Signing and storage.** Every message is signed with the seat's handshake key and checked against the allowlist. The 60 s skew applies at submission, and stored messages are re-verified on every tally.

**Counting the quorum:**

- **Distinct seats:** `quorum.default` distinct allowlisted seats must approve (2 by default).
- **Author excluded:** the proposal's author doesn't count toward its own quorum.
- **One vote per seat:** a seat that votes twice counts once, and its latest vote wins.
- **Operator approval:** an approve from an `operator_seats` member marks the proposal ready on its own (operator override).
- **Operator reject:** a reject from an operator seat blocks the proposal.
- **Revoked seats:** their votes stop counting.

**Promotion is a mark only.** It only writes a `ready` marker, and nothing is ever applied, branched or merged, because git belongs to the operator's git window.

```
.venv\Scripts\python.exe scripts\proposals.py list | show <id> | tally <id>
.venv\Scripts\python.exe scripts\proposals.py sign proposal --payload p.json --submit
.venv\Scripts\python.exe scripts\proposals.py promote <id>
```

**Warm MCP tools:**

- `estate_propose` and `estate_review` take either a pre-signed `signed` message or sign with the spawning seat's `MAG_SEAT_KEY_PATH`.
- `estate_proposals` is read-only: list, show, tally.

The tools are confined to `watch/receipts/proposals/`, which is already covered by the container's `./watch/receipts` rw mount.
