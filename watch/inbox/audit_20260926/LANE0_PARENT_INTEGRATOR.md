# LANE 0 — PARENT SEAT / INTEGRATOR FINDINGS
## 2026-09-26 network audit — measurements taken directly by the parent seat

*These are the findings I verified myself, with commands, before/independent of
the 10 dispatched lanes. Written so the cross-lane synthesis can weigh them
against the children's numbers. Trust bytes: every claim below has a command.*

---

## P1 — A REAL RSA PRIVATE KEY IS TRACKED IN GIT AND PROPAGATED TO THE BACKUP

**Severity: highest finding of the audit.**

`memory/tls/lan.key` — an RSA private key, **1,675 bytes**, **mode 644**
(world-readable), tracked in git, in history since **2026-08-19**, and its blob
is present in the `Mag-backup.git` bare repo across **39 refs**.

Structural check only (first line masked, key type confirmed, no content read):

```
PEM header of the memory/tls/lan.key file: RSA PRIVATE KEY block
line count: 27
```

```
$ git ls-files memory/tls/
memory/tls/lan.crt
memory/tls/lan.key

$ git check-ignore -v memory/tls/lan.key
  NOT IGNORED (confirmed tracked)

$ git log --oneline -- memory/tls/lan.key
799ddb6fe  wip 20260819: ... plus general working-tree changes
            (LOCAL ONLY, not pushed)

$ git --git-dir=Mag-backup.git cat-file -s f5e6dea5f45ae6ec6deb5c3b424f68743e36a131
1675
$ git --git-dir=Mag-backup.git log --all --oneline -- memory/tls/lan.key
799ddb6fe  wip 20260819: ... (LOCAL ONLY, not pushed)
```

**The load-bearing detail: the commit message says "LOCAL ONLY, not pushed" and
that is false.** The `local` remote is not a network host — it is a bare repo on
this same disk:

```
$ git remote -v
local  C:\Users\foste\Documents\projects\Mag-backup.git (fetch/push)
```

`git branch -a --contains 799ddb6fe` lists five `remotes/local/*` branches. The
key object exists in that backup. So "local only" meant "local disk", not "not
committed" — and the label on the commit is what would mislead a future reader
into thinking the exposure is contained.

**Operator decision required** (I am not rotating, not rewriting history, not
committing — read-only audit):
1. Rotate/revoke this key. It has been readable by anything with repo access
   since Aug 19, and sits in a backup that a single `git gc` will not purge.
2. If the LAN TLS cert is still live, rotation breaks clients until reissued.
3. History rewrite (`filter-repo`) is a separate, larger decision — the backup
   repo would need rewriting too, and it has 39 refs.

---

## P2 — MY OWN "18,733 PRIVATE FILES" NUMBER WAS WRONG. Corrected: 225.

My first recon pass excluded files by name-substring and I reported
"18,733 private files skipped" as if it were a privacy control. It was mostly
noise. Breaking down what the filter actually matched:

| pattern | hits | reality |
|---|---:|---|
| `private` | 17,933 | **C/C++ headers** (`jemalloc/internal/private_namespace.h`, `bzlib_private.h`), pytest temp artifacts (`test_save_and_load_private_map0/`) |
| `secret` | 345 | mixed |
| `journal` | 143 | DFHack source (`scripts/internal/journal/journal_context.lua`) |
| `.env` | 126 | real, plus 8 pytest-tmp copies |
| `credentials` | 91 | real |
| `.key` | 87 | real |
| `.pem` | 8 | real |

The English word "private" in a C header is not a secret. The corrected
secret-bearing surface:

| tier | count |
|---|---:|
| HARD (exact secret filenames) | 27 |
| HARD (secret extensions .pem/.key/.pfx/…) | 91 |
| dotenv (`.env*`) | 107 |
| **REAL secret surface** | **225** |
| SIGNAL (name-matched, needs triage) | 2,878 |

`memory/audit_20260926/private_boundary.py` + `.json` hold the full path list.
**The exclusion rule I used was 83× too broad and would have hidden the real
surface inside noise** — which is exactly why the boundary needed auditing
rather than trusting.

---

## P3 — THE GIT SECRET BOUNDARY IS OTHERWISE GENUINELY SOLID (negative finding)

Stated as a positive, because negative findings are load-bearing too:

- `local_sovereign_agent/.env` — **not tracked** ✓
- all 6 `state/auth_switchboard/*/credentials.json` snapshots — **ignored** ✓
- `state/`, `corpus/library/`, `agents/pytest-*/`, `mine/raw/` — all ignored ✓
- `git ls-files state/auth_switchboard/` → **0 files**
- secret-scan over tracked content: 7 hits, **all test fixtures or shader code**:
  - `tests/test_embassy_deliver.py:38` — writes a fake `ghp_…` string
  - `tests/test_trajectory_rib.py:49,55` — asserts a fake `sk-…` is NOT present
  - `memory/corpus/shadertoy21k/...` × 3 — GLSL matching `sk-` incidentally
  - `memory/trajectory/steps.jsonl:3310` — no key pattern; incidental
- `.env.example` is tracked and is **template-only** — all 13 keys EMPTY except
  `XAI_MODEL=grok-4` (a model name; my own scanner flagged it, a false positive)

**So the boundary works, with exactly one hole: `memory/tls/`.** One unignored
directory in an otherwise disciplined `.gitignore`.

---

## P4 — NO SECRET SCANNER EXISTS IN THE REPO

Searched `tools/`, `scripts/`, `githooks/`, `.githooks/` for scanner-shaped
source (a scanner must contain the patterns literally). **No scanner.** No
gitleaks, no detect-secrets, no trufflehog, no custom `sk-` gate.

This closes a question the prior socratic pass left open — `SOCRATIC_GAPS_20260918.md`
item 8: *"Dossier sanitization (API keys in .md files) pending — and nothing this
window filed has been key-scanned."* Still true, now with a specific reason: the
scanner was never built, and the 1,087 untracked files plus the 2,878 SIGNAL-tier
name matches remain unscanned.

**P1 got in precisely because the one secret that mattered was in a `.key` file
in a directory nobody wrote an ignore rule for** — and no scanner existed to
catch what the ignore rules missed.

---

## P5 — `watch/` IS 7.1 GB — BIGGER THAN `.git` (7.5 GB combined pressure)

Scoped measurement (full-tree `du` timed out at 300 s twice; this is per-dir):

| dir | size |
|---|---:|
| **watch/** | **7.1 G** |
| catalog/ | 352 M |
| tools/ | 174 M |
| state/ | 96 M |
| mag/ | 42 M |
| docs/ | 32 M |
| tests/ | 10 M |
| scripts/ | 2.6 M |
| memory/tls/ | 8.0 K |
| corpus/ | TIMEOUT (>45 s) |
| **.git** | **7.5 G** |

My earlier report said the worktree size was "unknown" — it is now bounded:
**`watch/` alone is 7.1 GB**, and the two 590 MB byte-identical
`ESTATE_INDEX.jsonl` files live there and under `dashboard/data/`. `corpus/`
remains unmeasured (timed out); the honest statement is `>45 s to walk`, not a
number.

---

## P6 — `Mag-backup.git` IS A REAL BARE REPO WITH 39 BRANCHES

Correcting an inventory artifact: my recon listed it as "178 files, no working
tree, looks bare." Confirmed bare (`rev-parse --is-bare-repository` → `true`),
**6.3 GB**, **39 refs** spanning `cursor/*`, `codex/*`, `archive/*` namespaces.
It is the `local` remote for the main repo, so it is the fleet's actual
persistence layer — and, per P1, it holds the private key.

---

## Integrator's cross-check harness

`memory/audit_20260926/crosscheck.py` loads all 10 lanes' JSON and flags any
lane whose numbers disagree with the ground truth measured here (collected
tests 2288, dirty paths 1313, network files 1,946,684, ratchet 6 NEW, etc.).
The repo's own law — "trust bytes, not reports" — applies to my own children.
Run it once lanes land:

```
.venv\Scripts\python.exe memory\audit_20260926\crosscheck.py
```

**Zero contradictions is the pass condition. A contradiction is a finding about
the fleet's instruments, not about the audit.**
