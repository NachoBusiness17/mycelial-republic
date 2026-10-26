# CHAIN_APPENDONLY_RESEARCH_20261019

- class: RECEIPT
- writer: grok-bot executor (read-only research follow-up to AUDIT_MAG_STATE_20261019)
- audited_at: 2026-10-19T12:00 America/New_York (UTC-4)
- HEAD: f77a55470 (same tree as prior audit; no repo edits this turn)
- prior: watch/inbox/AUDIT_MAG_STATE_20261019.md
- operator ask: "This seems like a stupid problem that could be solved by doing a little research. Summon lessig and ponytail, self steal."
- rules: read-only on repo; only this receipt written; no .env/secrets/cookie contents; no recursive Get-ChildItem; no em-dashes; NEW vs KNOWN + staleness

## Summary (plain)

Lessig means: make rewrite physically or mechanically impossible (architecture, not a prompt). Ponytail means: reuse the smallest already-built organ (AH19 v2 + OS append-only + disable lab relaunch), do not invent a new transparency stack. The 24 leaf rewrites came from `mag/verkle_knot.py` v1 amend path calling `_rewrite_chain` (full-file tmp+os.replace) while `chain_mode` was still v1; lab PID 13 and Windows labs relaunched because STOP/suspend do not survive reboot or `restart: unless-stopped` + `mag_launch` always wanting lab. Ranked fix: (1) OS append-only on the chain file, (2) keep/enforce v2 correction rows only and delete runtime rewrite paths, (3) durable lab-off via env/compose not kill -STOP, (4) patrol consistency proof against sealed `ab595c33` prefix, (5) single-writer lease fail-closed for external rewriters.

---

## 1. SUMMON: what Lessig and Ponytail are

### Lessig (found; estate organ, not a person seat)

| Source | Date | What it says |
|---|---|---|
| ZCode memory `lessig-ponytail-summon-20261003.md` | 2026-10-03 | "**LESSIG** = code-as-law (`mag/law.py`, `mag/canon_gate.py`, `docs/ref/lessig_1_6.md`). Architecture regulates more than content: don't ASK models for compliance in prose - make non-compliance mechanically impossible or irrelevant." |
| `.agents/skills/operator-corrections/LAWS_COMPILED_20261003.md` law 22 | compiled 2026-10-03; quote from 2026-08-10 | "RAILS OVER DIRECTION (code is law). ... Laws live in the tool path with exit codes" |
| `docs/ref/lessig_1_6.md` | 2026-07-27 | Four modalities: Law, Norms, Markets, **Architecture (code that makes the above hard to violate)** |
| `mag/law.py:1-6` | mtime 2026-08-30 | Module docstring: "CODE-AS-LAW enforcement registry ('Lessig: architecture regulates more than content')" |
| `watch/VAST_PERSONA_VERDICT_20260905.md` | 2026-09-05 | Lessig as jurisdiction lens: provenance append-only before teardown |

**Lens applied to this problem (Lessig):** A policy flag (`chain_mode: v2`) and a paused process are norms/prose. Real law is: the filesystem refuses in-place rewrite; the writer has no `_rewrite_chain` on the runtime path; relaunch cannot resurrect a writer you meant to kill. "Code is law" here means NTFS AD-without-WD / `chattr +a` + deleting the amend rewrite from the hot path.

### Ponytail (found; coding skill / YAGNI ladder)

| Source | Date | What it says |
|---|---|---|
| ZCode `lessig-ponytail-summon-20261003.md` | 2026-10-03 | "**PONYTAIL** = over-engineering ladder audit (`mag/ponytail_audit.py`, github dietrichgebert/ponytail). Ladder cuts code bloat; tiers/gates/residual never cut." |
| `docs/ref/weaves/W8-ponytail-ladder.md` | weave skill | Lazy senior: Need exist? In codebase? Stdlib? Native? Dep? One line? Else minimum. Max 10 files. Run `ponytail-audit` before FILE. |
| `docs/ref/PONYTAIL_CAVEMAN_AUDIT.md` | baseline | Ponytail = minimum necessary code, safety preserved; pairs with Lessig governance |
| `configs/skills.yaml` `ponytail-ladder` | | hard_code / audit skill; "YAGNI ladder; run ponytail-audit before merge" |
| `mag/skill_seat.py` | | maps "ponytail" seat to W8 ladder + `run_audit` |
| LAWS_COMPILED law 21 | 2026-09-17 restated 10/3 | "SELF-STEAL BEFORE SIDEBUILDS... summon lessig and ponytail" |

**Lens applied to this problem (Ponytail):** Do not build a private Certificate Transparency service. AH19 append-leaves already exists (`watch/inbox/last_mile_20260930/AH19_AMEND_PERF.md`, `chain_mode: v2` already on). Smallest fix stack: (a) keep v2, (b) OS append-only so v1 rewrite cannot run even if someone flips the flag, (c) `MAG_DISABLE_LAB=1` in compose so reboot cannot resurrect the writer, (d) one patrol check against the seal. Hostile overbuild = new Merkle CT daemon, new DB, new lease broker when `verkle_lock` + `restricted_leases` + TipWitness already exist.

Ponytail was found (many hits). Not invented.

---

## 2. ROOT CAUSE (file:line, mtimes)

### 2a. How old leaves get rewritten (the 24 on 2026-10-17)

**Hot path (v1 amend):** `mag/verkle_knot.py`

| Symbol | Lines | Role | File mtime |
|---|---|---|---|
| `chain_mode()` | 73+ | reads `configs/mag.yaml` `chain_mode`; fail-closed to v1 | 2026-10-17 16:27 ET |
| `_rewrite_chain` | 680-722 | loads all rows, recomputes every `verkle_root`/`parent_verkle_root`, writes **entire** file via tmp + `os.replace(tmp, CHAIN)` | same |
| `_append_verkle_knot_unlocked` | 960-1201 | v1: if `existing_i is not None` (same session_id already in chain) then `rows[existing_i] = chain_row` and `_rewrite_chain(rows)` at **1086-1099** | same |
| `append_verkle_knot` | 1204-1211 | takes `verkle_lock()` then unlocked body | same |
| heal-after-append | 1144-1168 | on race, **rewrites whole chain again** via tmp.replace even on the "append" path | same |
| `consolidate_chain_one_leaf_per_session` | 1214-1226 | external whole-chain rewrite tool (lease warn-only) | same |

**Config flip timing:** `configs/mag.yaml` line 8 `chain_mode: v2` mtime **2026-10-17 15:17:57 ET**. Prior audit leaf-rewrite timestamps were **12:06Z-18:42Z on 2026-10-17** (= 08:06-14:42 ET), i.e. **before** the v2 flip for most of the wave; one cluster (18:15Z+) aligns with container respawn at 18:15 UTC while mode may still have been v1 in the running process until restart picked up yaml.

**Callers that feed dossiers into that path:**

| Caller | Line | Notes |
|---|---|---|
| `mag/session_dossier.py` | 542-544 | `append_verkle_knot(...)` on dossier write; `amend` flag at 435-495 |
| `mag/knot_at_close.py` | 274 | backfill / close bridge |
| `mag/ghost.py` | 1504-1525 | autonomous-janitor fold (`auto-fkb-*`) |
| `mag/law.py` | 124-125 | law enforcement knots (often empty theme) |
| `mag/memlang.py` | 151-152 | memlang harvest knots |
| `mag/agent_os_loop.py` | 73 | cycle fold |
| others | (arrival, fact_bus, castle_foundation, ...) | many fold-to-verkle organs |

**v2 re-knots (post-flip, not leaf rewrites of old rows):** same `append_verkle_knot` under `chain_mode==v2` sets `existing_i = None`, appends one line with `supersedes_index` / `supersedes_leaf_hash` (1080-1085), writes `.s{seq}.knot.json`. That explains the 854 mag-agent-orc **appends** after the prefix (NEW rows, old rows intact) once lab came back under v2. Disease class differs: history length grows; sealed prefix bytes stay if v2 holds.

**Staleness:** AH19 disease description (2,821/8,626 amend rewrites) dated 2026-09-29/30; verified-at-HEAD 2026-10-19: `_rewrite_chain` still present; v2 flag ON; 24 leaf rewrites after the 10-16 sealed restore prove v1 path ran again before the flip.

### 2b. Why suspend/pause did not survive reboot

| Mechanism | What it is | Why it failed |
|---|---|---|
| Windows `NtSuspendProcess` on 28 lab PIDs | process-local suspend | Host reboot **2026-10-19 00:14:21 ET** (Win32 LastBootUpTime); PIDs die; resume script cannot revive them |
| `kill -STOP` on container lab PID 13 | signal to one PID | Container recreate assigns a **new** PID 13; STOP does not transfer |
| `docker-compose.yml` mag-sovereign `restart: unless-stopped` (line 109) | Docker policy | After Docker Desktop / host reboot, container comes back healthy and runs entrypoint |
| `mag_launch.py` lab slot 249-253 | always `wanted` if authoritative and `MAG_DISABLE_LAB != 1` | Every container start **spawns** `main.py lab --no-dashboard` |
| `mag-docker-watchdog` scheduled task | relaunches Docker Desktop if engine unreachable | Helps engine return; compose then recreates stack |
| No durable "lab off" flag in compose env | missing Lessig rail | Pause was a one-shot act, not architecture |

Evidence: prior audit (docker inspect StartedAt, mag_launch.log spawn lines 10-17 18:15Z / 10-18 06:29Z / 10-19 04:16Z / 10-19 11:54Z; /proc State R for PID 13).

**KNOWN** class (CHAIN_RESTORE_20261015.md already warned writers must stay paused until amend path changes). **NEW** confirmation that reboot + unless-stopped + mag_launch is the exact relaunch chain.

---

## 3. SELF-STEAL (prior Mag organs; verified at HEAD)

| Organ | First / design date | Path | Verified-at-HEAD 2026-10-19 | Outcome |
|---|---|---|---|---|
| AH19 append-leaves | 2026-09-29/30 | `watch/inbox/last_mile_20260930/AH19_AMEND_PERF.md`; `verkle_knot.chain_mode`; `tests/test_ah19_append_leaves.py` | `chain_mode: v2` in configs/mag.yaml; append path has supersedes_* | **reuse primary** |
| Heartbeat verkle_lock | commit fda902344 2026-10-15 | `mag/verkle_knot.py` verkle_lock + heartbeat | present; tests/test_verkle_lock_heartbeat.py | **reuse**; does not block rewrite, only serializes |
| conftest live-estate write fence | 2026-10-14/15 | `tests/conftest.py:99-160` | present; audit hook on memory/biography + state | **reuse** for tests only |
| seed_seal tip / restore seal | 2026-10-02 tool; restore seal 2026-10-16 | `mag/seed_seal.py`; `CHAIN_RESTORE_20261015.seal` key_id de5fc05e962c43ab | seal files present; live tip not certified | **reuse** for prefix checkpoint |
| TipWitness daily | script 2026-09-30 | `scripts/tip_witness_daily.ps1` | runs; **exit 2** gist scope (STILL-OPEN) | **reuse after credential**; publish signed tip |
| Estate Ratchet | scheduled 09:45 | `Estate Ratchet` task; `scripts/ratchet_daily.ps1` / `tools/violation_ratchet.py` | State=Ready; last result=1 (seal/ratchet fail class) | **reuse** to host prefix-seal check |
| restricted_leases | doctrine 2026-10-17 | `configs/restricted_leases.json` `chain:biography`, `proc:lab`; `mag/leases.py` | present; consolidate uses warn-only | **gap:** runtime append exempt; consolidate not fail-closed |
| archive_guard | 2026-10-18 | `tools/archive_guard.py` | 10/10 tests prior audit | pattern for lookaround deny; not yet on chain |
| CONFIG-SEAL | 2026-09-29 | `tools/config_seal.py` | verify FAIL mirrors.json today | pattern for sealed register |
| bintree_v2 shadow | 2026-10-17 | `chain_v2_shadow: true` | shadow on; signing/publish false | optional parallel log; not yet the law |

Ponytail verdict on self-steal: **do not invent**; wire AH19 + OS append-only + MAG_DISABLE_LAB + ratchet/TipWitness consistency check.

---

## 4. RESEARCH (external systems; URLs)

| System | Append-only mechanism | Mag mapping | URL |
|---|---|---|---|
| Certificate Transparency RFC 6962 | Merkle tree; **consistency proofs** show newer tree is append-only extension of older; Signed Tree Head (size + root + sig) | Seal `ab595c33` at size 12016 as trusted STH; patrol proves live tip consistent with that prefix | https://www.rfc-editor.org/rfc/rfc6962.html |
| CT v2 RFC 9162 | Same idea; consistency_proof_v2 | Same | https://datatracker.ietf.org/doc/rfc9162/ |
| Sigstore Rekor / Trillian | Tamper-evident append-only log; auditors monitor consistency; checkpoints / witnesses | TipWitness + Estate Ratchet as auditor; optional witness cosign later | https://docs.sigstore.dev/logging/overview/ ; https://google.github.io/trillian/docs/TransparentLogging.html |
| Rekor consistency API | `GET /api/v1/log/proof?firstSize=&lastSize=` | Patrol: firstSize=12016 root ab595c33 vs live n/root | https://raw.githubusercontent.com/sigstore/rekor/main/openapi.yaml |
| git | Content-addressed objects; history rewrite is a **new** tip (force-push detectable) | Leaf hash already content-addressed; problem was rewriting the **log of leaves** | (standard git model) |
| Datomic | Facts indelible; corrections = new assertions/retractions; history queryable | AH19 v2 `supersedes_*` rows = retractions-as-new-facts | https://docs.datomic.com/datomic-overview.html ; https://docs.datomic.com/client-tutorial/retract.html |
| Windows NTFS | `FILE_APPEND_DATA` without `FILE_WRITE_DATA`: writes cannot overwrite existing bytes | icacls grant AD, deny WD on verkle_chain.jsonl for Mag runtime users | https://learn.microsoft.com/en-us/windows/win32/fileio/file-access-rights-constants ; https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls |
| Linux `chattr +a` | Append-only inode flag; truncate/rewrite fail (needs CAP_LINUX_IMMUTABLE to clear) | On bind-mounted chain inside container FS if supported; else rely on host NTFS | https://man7.org/linux/man-pages/man1/chattr.1.html |

---

## 5. SYNTHESIS: ranked fix plan (suggestions only; not done)

### Rank 1 - OS append-only on the chain file (Lessig max leverage)

- **What:** Host: strip WD from Mag runtime principals; grant AD+RD on `memory/biography/verkle_chain.jsonl` (and optionally tip via separate careful policy). Writer opens append-only (`open(..., "a")` already at 1116). Container: if FS supports it, `chattr +a` on the file; note Docker mount is Windows bind so **NTFS ACL is the real lever**.
- **Reuses:** pure-append path already in verkle_knot 1100-1117; B2-393 LF-safe append.
- **New:** one-time ACL script + receipt; document break-glass (admin clears ACL to restore).
- **Size:** ~1 small script + docs; <1 day.
- **Tests:** attempt `_rewrite_chain` / `os.replace` under test ACL must raise AccessDenied; append one row succeeds; verify OK.
- **Hostile pass:** admin / SYSTEM can reset ACL; Python `os.replace` of a temp file may replace the inode if DELETE+CREATE allowed (must also deny DELETE on the file or deny create-in-dir for temp swap). **Mitigation:** deny DELETE on chain file; deny WRITE on directory for non-admin except create of knot files elsewhere; or move chain to a dedicated dir with tighter ACLs. Another bypass: rewrite via a principal that still has Full Control (operator account). Accept: Lessig against accidental/runtime writers, not against the owner.

### Rank 2 - Amend = correction row only; remove runtime rewrite (Ponytail + AH19)

- **What:** Keep `chain_mode: v2` fail-closed (treat missing/unknown as **v2**, or hard-reject v1). Delete or gate `_rewrite_chain` so runtime `append_verkle_knot` never calls it; leave consolidate behind `leases.guard(..., enforce="conflict")` + explicit CLI. Fix heal path 1144-1168 so race repair appends a correction tip row or refuses instead of rewriting the whole file.
- **Reuses:** AH19 spec, supersedes_*, session pointers, tests/test_ah19_*.
- **New:** flip fail-closed default; heal redesign; lease enforce on consolidate.
- **Size:** ~1-2 days in verkle_knot + tests.
- **Tests:** existing AH19 suite; new test that same session_id twice yields two rows and identical first-row bytes; heal under concurrency.
- **Hostile pass:** someone sets `chain_mode: v1` in yaml. **Mitigation:** Rank 1 ACL still blocks rewrite; CONFIG-SEAL / ratchet alerts on mag.yaml change; restricted_leases already advisory on `file:mag/verkle_knot.py`.

### Rank 3 - Reboot-durable writer posture (disable relaunch source)

- **What:** Set `MAG_DISABLE_LAB=1` in compose environment for mag-sovereign (and document). Optionally remove lab from default `wanted` slots until operator flips a sealed config. Do **not** rely on kill -STOP / NtSuspendProcess. Use `proc:lab` lease conflict before any compose up that enables lab.
- **Reuses:** mag_launch.py already checks MAG_DISABLE_LAB; restricted_leases `proc:lab`; docker-compose env.
- **New:** compose env line + CURRENT/owed note; optional sealed "lab_enabled" bit.
- **Size:** hours.
- **Tests:** container recreate under disable still has no lab in `docker top`; enable path requires named seal update.
- **Hostile pass:** someone unsets the env and recreates; host `main.py lab` outside compose. **Mitigation:** Rank 1 ACL; scheduled patrol that alerts if lab PID exists while lab_enabled=false; do not leave host lab launchers in Startup.

### Rank 4 - Signed tree head + consistency proof in patrol (CT / Rekor pattern)

- **What:** Treat sealed restore (size 12016, root ab595c33, sha256 0da8026d) as trusted STH. Daily Estate Ratchet / new drift check: hash first 8,619,201 bytes of live chain (or recompute merkle of first 12016 leaves) must match seal; then prove tip is append-only extension (Mag already stores per-row parent/root; a thin consistency check = "rows[0:12016] leaf_hashes unchanged"). Wire TipWitness to publish tip root once gist scope fixed.
- **Reuses:** seed_seal companion; scripts/verify_verkle_full.py; TipWitness; Ratchet.
- **New:** ~50-100 LOC check + receipt field; fix TipWitness credential (KNOWN).
- **Size:** <1 day after TipWitness credential.
- **Tests:** mutate a prefix leaf in a temp copy -> check fails; append-only copy -> passes.
- **Hostile pass:** attacker replaces seal files too. **Mitigation:** seal public key / key_id de5fc05e962c43ab pinned offline; compare key_id as CHAIN_RESTORE already warns.

### Rank 5 - Single-writer lease fail-closed for external rewriters

- **What:** `consolidate_chain` and `chain_repair` take `chain:biography` with `enforce=conflict` (not warn). Stealth driver's `chain_repair --dry` must not take the lock (KNOWN STILL-OPEN from CHAIN_RESTORE).
- **Reuses:** mag/leases.py, restricted_leases.json.
- **New:** change enforce; stealth dry-run lock-free.
- **Size:** hours.
- **Hostile pass:** lease file deleted; two containers different hostnames. **Mitigation:** heartbeat lock already blocks cross-host steal; lease is defense-in-depth, not Rank 1.

### Explicit non-goals (Ponytail cut)

- Standing up Trillian/Rekor locally.
- New database for the chain.
- Critique of Church campaign content (out of scope; cookie-disk risk remains in prior audit only).

---

## Findings table

| # | Finding | Evidence | NEW/KNOWN | Severity | Staleness | Suggested next step |
|---|---|---|---|---|---|---|
| 1 | Lessig = architecture-enforced rails; Ponytail = YAGNI ladder / self-steal | ZMEM lessig-ponytail-summon-20261003; LAWS 21-22; lessig_1_6.md; W8-ponytail-ladder.md | KNOWN estate vocabulary; NEW application to chain | info | sources 2026-07 to 2026-10-03; verified 2026-10-19 | Apply lenses as ranked plan |
| 2 | Root rewrite path = v1 amend -> `_rewrite_chain` full-file replace | verkle_knot.py:1086-1099, 680-722 | KNOWN disease in AH19; NEW post-restore recurrence dated | high | AH19 2026-09-30; verified HEAD still has path | Rank 1+2 |
| 3 | v2 re-knots append; do not rewrite old leaves | verkle_knot.py:1004-1085; configs/mag.yaml chain_mode v2 | NEW clarity vs audit confusion | medium | flip 2026-10-17; verified | Keep v2; fail-closed |
| 4 | Heal path can still rewrite whole file | verkle_knot.py:1144-1168 | NEW (relative to AH19 writeup) | medium | code at HEAD | Redesign heal |
| 5 | Suspend/STOP lost to reboot + unless-stopped + mag_launch lab wanted | docker-compose.yml:109; mag_launch.py:249-253; boot 00:14 ET | KNOWN warning; NEW exact relaunch chain | high | CHAIN_RESTORE 2026-10-16; verified | Rank 3 MAG_DISABLE_LAB |
| 6 | Self-steal stack already covers most of the fix | AH19, seed_seal, TipWitness, Ratchet, leases, fence | KNOWN organs; NEW wiring gap | medium | dates in table above | Wire, don't invent |
| 7 | External research converges on consistency proofs + OS WORM/append ACL | RFC 6962/9162; Rekor; NTFS AD; chattr +a; Datomic | NEW citations this receipt | info | fetched 2026-10-19 | Rank 1 + 4 |

---

## Ranked plan in plain sentences

1. Make the chain file append-only at the OS (NTFS AD without WD; deny delete/replace), so `_rewrite_chain` fails even if called.
2. Keep AH19 v2 as the only amend model; remove or hard-gate runtime full-file rewrite and the heal rewrite.
3. Turn lab off with `MAG_DISABLE_LAB=1` (and sealed config), not with kill -STOP, so reboot cannot bring the writer back.
4. Add a daily consistency check that the first 12,016 leaves still match sealed root `ab595c33` / sha `0da8026d`, and publish tip via TipWitness once gist works.
5. Make consolidate/chain_repair take a fail-closed `chain:biography` lease and stop stealth dry-runs from holding the lock.

Receipt path: `watch/inbox/CHAIN_APPENDONLY_RESEARCH_20261019.md` (and box copy under `/workspace/mag-audit-20261019/`).
