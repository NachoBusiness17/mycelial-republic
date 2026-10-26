# W3 — TIP WITNESS: external checkpoint for the verkle chain (refire)

Date: 2026-09-30 · Lane: last_mile W3 (ZCode refire; prior attempt wall-killed)
File ownership: `tools/tip_witness.py` + `tests/test_tip_witness.py` (+ the two
schedule-hook scripts and this receipt the mission itself demands).

## Mission

The chain is writer-only tamper-evident: outsiders cannot forge it, but the
writer can rewrite the whole thing and no in-repo byte survives to contradict
the rewrite. Worst-economics fix: pin the tip outside the estate — one line
(root + leaf count + timestamp) in a GitHub gist — and make the witness a
RATCHET so a rewrite cannot launder itself past the checkpoint.

## Build (all six mission points landed)

1. **Tip read** — `load_tip()` reads `memory/biography/verkle_tip.json`
   (root must be 64-hex, n_leaves a non-negative int; anything else is
   exit-2 fail-closed). Trust boundary stated in the tool docstring: the
   witness reads the TIP FILE; tip-vs-chain consistency is AG5's verify
   paths, not recomputed here.
2. **Gist publish** — one line `MAG-TIP-WITNESS.v1 root=<hex>
   n_leaves=<int> ts=<ISO-UTC>`; ONE gist, id in
   `memory/biography/tip_witness_state.json` (gitignored, machine-local);
   a lost state file re-adopts the gist by its description marker — never a
   second gist. Secret gist by default (`--public` flips first creation).
   Token via `mag.key_law.get("github_token")`, declared in
   `configs/keys.json` (key law: no reader guesses env names; the token
   value is never printed).
3. **`--verify`** — fetch gist, compare live tip:
   `WITNESS-MATCH` (exit 0) · `WITNESS-LAG` live ahead, publish due
   (exit 0) · `WITNESS-DIVERGENT` = chain SHRANK or same-count root change
   = **chain rewritten = laundering alarm** (exit 1) · cannot-verify
   (no token / network / unparseable witness line) exit 2.
   **Ratchet:** the publish path verifies FIRST and REFUSES DIVERGENT —
   the witness never moves backward or sideways, only forward on
   leaf-count growth; a rewritten chain cannot re-launder the checkpoint.
4. **Dry-run default** — bare run prints the plan + read-only verify;
   `--publish` alone re-explains the gate; only `--publish --go` writes.
5. **Schedule hook** — `scripts/tip_witness_daily.ps1` (log
   `logs/tip_witness.log`, alerts `memory/attention.md` on exit 1/2) +
   `scripts/register_tip_witness_task.ps1`. **Registered:
   MagTipWitnessDaily, daily 09:30** — rides the chain after
   MagImproveDaily 08:00, MagCensusPatrolDaily 08:30, MagFtsIndexDaily
   09:00. Registering the task is the operator's standing --go consent;
   the ratchet keeps that consent safe.
6. **Mocked-API tests** — `tests/test_tip_witness.py`, **27 passed**:
   transport seam (tests never touch network/token), line roundtrip +
   garbage rejection, the four compare verdicts, fail-closed tip loads,
   gating (bare/`--publish`-without-`--go` write zero), single-gist law
   (create/patch/adopt-by-description), ratchet refusals (shrunk chain +
   same-count rewrite → zero witness writes), verify exit codes incl.
   network/gone-gist/unparseable, and token-secrecy on the scope-403 path.

## Scope check (probed live 2026-09-30, byte truth)

- `GET /user` → 200, login NachoBusiness17; **no `X-OAuth-Scopes`
  header** → fine-grained PAT shape.
- `GET /gists` → 200 `[]` → gist **read** works.
- `POST /gists` (create+delete probe, deleted nothing — it never created)
  → **403 "Resource not accessible by personal access token"** → gist
  **write DENIED**.

## Staged state — built, gated, and DARK until one operator credential fix

- Live dry-run: `python tools/tip_witness.py` → plan line
  (`root=aaaaf899… n_leaves=8691` at 23:18Z) + `WITNESS-NONE`, exit 0.
- Live scheduled run (by hand): START → SCOPE 403 message → alert block in
  `memory/attention.md` → END exit 2. The whole alert chain is proven.
- **No gist exists yet. Nothing was published.** First `--publish --go`
  (manual or the 09:30 task) fails exit 2 with the SCOPE note until the
  operator widens the PAT (**Account permissions → Gists: Read and write**)
  or swaps in a classic PAT with the `gist` scope. Until then the surface
  alerts daily (loud-by-design, the fleet's dark-surface law).

## Side effects beyond the owned files (named)

- `configs/keys.json`: +1 entry `github_token` (HEAD bytes preserved, 6-line
  insert; key-law door for the token read; `python -m mag.key_law --audit`
  passes, `github_token present: true`; pre-existing orphan GROK_API_KEY
  untouched).
- `memory/attention.md`: 1 live alert block (the true scope-denial signal).
- Scheduled task `MagTipWitnessDaily` registered at 09:30 daily.
- Ratchet: `tip_witness.py` clean (400 lines; env-key-read fixed via
  key_law, except-pass fixed, file-too-long trimmed). Remaining NEW ratchet
  rows (`pain_replication/runner.py`, `rule_parity.py`,
  `trajectory_minimizer.py`) are other lanes' uncommitted work — untouched.

## Evidence

- `pytest tests/test_tip_witness.py -q` → **27 passed** (2026-09-30)
- `pytest tests/test_tip_witness.py tests/test_ag5_tip_verify.py
  tests/test_env_load_mistral_keys.py -q` → **46 passed** (2026-09-30)
- `python -m mag.key_law --audit` → empty `[]`, orphans pre-existing
- `schtasks /Query /TN MagTipWitnessDaily` → created, daily 09:30
