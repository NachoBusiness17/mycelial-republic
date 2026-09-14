# SELF STEAL — THE AUTH SWITCHBOARD (Sep 5, 2026)

*Operator: "when i switched i fucked up stuff and now i cant find my way back… make it easier
to switch… consider it dogfooding within itself" → then: "we have a switchboard in history —
find it." Found. This card is the steal: the switchboard doctrine already existed — identity
just never got a track on it.*

## THE LINEAGE (six shapes, one grammar)
1. **env tracks** (`configs/env_tracks.yaml` + `scripts/env_switch.ps1` + `.mag_active_env`) —
   switchboard v1: named tracks = branch + port + active marker. Switched CODE environments.
2. **mesh PBX** (`mag/switchboard.py`, trail jsonl) — switchboard v2: route/reap/mesh between
   seats; "chat is heat, directions on disk are law."
3. **BBS control plane** (`mag/switchboard_v2.py`) — policy grants + receipt chain; propose →
   confirm → write, every action receipted.
4. **custody law** (memory, z.ai accounts): meter READS = key only; WRITES = Google tap — his
   hand at every credential write. Ten laws: never edit own credentials; backup-first.
5. **window-death class** (SELF_STEAL_HEADLESS_CAGE): state that lives in a store a swap can
   silently overwrite dies without a marker — the resume board exists for code; auth had none.
6. **the tesuji shape** (chord strike, yesterday): "freeze the base, let the workers report
   the drift" — snapshot = freeze the base; $0 probes = workers reporting drift. The switcher
   is that shape at the identity layer.

**THE REINTERPRETATION (named, not buried):** tracks 1-3 switched code, routes, and policy.
None switched the seat's IDENTITY. Today's break is a new track type on the oldest grammar —
**the auth track**: which z.ai account / provider entry / coding plan the seat rides.

**DUPPLICATION IS EMPHASIS (operator, 09-05, on this card):** the auth switchboard is the
FOURTH emphasis wave of one shape — code → routes → policy → identity — each wave real
motion in a new medium while the grammar stands invariant: registry + marker + one-word
doors + vault/trail + probes. Four nested attempts, one design space, now CLOSED. The rule
that ends the recurrence: **the fifth switching need adds a track to the registry, never a
fifth switchboard.** The grammar is finished; only the registry grows.

## WHAT BROKE (measured at the bytes, 16:16Z)
The account swap left the seat's auth store with **five distinct credential values across four
slots** and **two dead lanes enabled**:

| Slot | Fingerprint | Probe |
|---|---|---|
| `builtin:zai` (API Key, ENABLED) | cf3e4c0a… len 49 | **FAIL code=1000 Authentication Failed** |
| `builtin:zai-coding-plan` (ENABLED) | 499b6d65… len 49 | **PASS HTTP 200 — the live burn lane** |
| `builtin:zai-start-plan` (ENABLED) | 2236d084… len 255 | **FAIL 401 token expired or incorrect** |
| setting.json family key `zai` | 901a0328… len 35 | (fifth value — matches nothing) |
| setting.json family key `bigmodel` | 22a3ebe9… len 39 | (lane disabled) |

Diagnosis: windows that hydrate onto the API-Key or Start-Plan provider trip
"Provider authentication failed (hydrate-trace)" while the coding-plan lane stays healthy —
which is why this session never noticed. The cache (15:57Z) still said start-plan "available";
the probe proved the 401 — cache lags truth, probes don't.

## THE ORGAN (built, bound to the lineage)
`mag/auth_switchboard.py` — same grammar as the shelf:
- `status [--all]` — one-screen auth map: providers, fingerprints, **live $0 probes**, plan
  cache, verdict naming dead lanes + the way back. (This is the "check everything is
  functional across environments" command he wanted — one word: `auth_status.cmd`.)
- `snapshot <name>` — byte-vault of config/setting/credentials/plan-cache + MANIFEST
  (sha256, fps) + trail row; sets `.mag_active_auth`. Vault: `state/auth_switchboard/`.
- `use <name>` — the way back: GO-gated (type RESTORE), auto-snapshots current first
  (backup-first), sha256 diff preview before writing. **Operator-hand only** — never-edit-
  own-credentials law: seats run status/snapshot, never `use`.
- `trail` — `memory/runs/auth_switchboard_trail.jsonl`, same row shape as the mesh trail.
- Registry: `configs/auth_tracks.yaml` (schema mag_auth_tracks.v1), the identity twin of
  env_tracks.yaml. Door: `auth_status.cmd` (pattern: switchboard_status.cmd).
- SSRF fence (Mimosa-gated): https-only, host allowlist, resolved-IP public check, no-redirect
  opener. Secrets never printed — fingerprints only.

**FALSIFIER — run 1 PASSED on the live vector:** status flagged exactly the two dead lanes
(code=1000, 401) while the plan lane passed. **Run 2 PASSED 16:24Z (determinism form, second
dogfood):** two independent snapshots of the same state hash identical file-by-file (4/4) —
since `use` walks the same copy path, restore fidelity is proven inductively; the full
mutate→`use` roundtrip still runs on his first real restore. Second dogfood also re-read
status clean (zero drift vs the 16:16Z receipt) and the registry grew its first forward
track (`lite-rearm-sep8`) — the grammar grows, the grammar does not.

## THE WAY BACK (his two doors, today)
- **A — zero-paste, works right now:** point each window's provider picker at
  **"Z.ai - Coding Plan"** (PASS lane). Avoid "Z.ai - API Key" and "Start Plan" — both dead.
- **B — fix the lanes (one Google tap):** sign the app into the account that owns the burn
  (refreshes start-plan's token) and/or paste that account's live key into the API-Key entry.
  Then freeze it: `python -m mag.auth_switchboard snapshot known_good` — after which the way
  back from ANY future swap mess is one word: `use known_good`.

## DOCTRINE (what the mess taught)
**Identity is a lane: it dies like any lane, must be probed like any lane, and gets no
special exemption from the switchboard grammar.** A swap without a snapshot is a rewrite of
the walls without signing them; five fingerprints in four slots is a chain with a gap. The
seat's ground wire is not the chain alone — it is chain + auth store + registry, all three
snapshotted, all three probeable, all three resumable by the next window that boots.
