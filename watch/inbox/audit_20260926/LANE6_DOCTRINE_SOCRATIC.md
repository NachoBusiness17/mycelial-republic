# LANE 6 — DOCTRINE SOCRATIC AUDIT
**Auditor:** lane6 · **Date:** 2026-09-26 · **Mode:** read-only, report only, nothing fixed, nothing committed.
**Subject:** the repo's own written law system — which laws are enforced by code, which are prose.

## VERDICT IN ONE LINE
Of **18 discrete laws** extracted: **7 are code-gated**, **4 have a tool that nothing invokes**, and
**7 are prose-only or unenforceable**. Worse — the 7 code-gated laws are all **pre-push**, on a branch
with **no upstream**, whose remote ref last moved **2026-09-19**, so the whole enforcement apparatus
has **never run on the 51 commits made since it was armed**.

---

## 0. THE FINDING THAT SWALLOWS THE REST

`githooks/pre-push` was added `ea04ebc15` (2026-09-25 06:26) and `core.hooksPath=githooks` is set.
It carries **10 gate blocks** and is genuinely good work. It has never once gated this branch.

```
active branch      mag/run-beta1-factory-build-audi-20260806T231709Z
upstream           fatal: no upstream configured
remote             "local" -> C:\Users\foste\Documents\projects\Mag-backup.git
backup ref mtime   2026-09-19 21:53          <-- six days BEFORE the hook existed
commits since hook 51
commits ahead of backup  87
origin remote      0 (git_backup.cmd line 25 gates push on "origin"; there is no origin)
```

`git_backup.cmd:25` — `git remote -v | findstr /i "origin"` — the only push driver in the repo
looks for a remote named **origin**. The only remote is named **local**. So the backup script
never pushes. The hook is armed, correct, and **structurally unreachable**.

**Socratic question:** the estate wrote a law ("Never loosen the hook") and a machine that enforces
it, and then never noticed the machine is not plugged in. Which of the two failures is this — the law
being unenforced, or the estate's own trust-bytes law being skipped? `seed/TRUST_BYTES_LAW.md:10`
says *"verify with the bytes you ran."* Nobody ran `git rev-parse --abbrev-ref @{u}`.

---

## 1. LAW TABLE

### TIER A — CODE-GATED (a machine can refuse)

| law_id | law (quoted) | source | enforcement | evidence it fires |
|---|---|---|---|---|
| A1 | "Registered debt passes; NEW debt blocks the push" | AGENTS.md:106 | CODE-GATED | `tools/violation_ratchet.py check --changed` → **RC=1**, "hits=70; registered=64; **NEW=6**" |
| A2 | "Config drift re-seals by NAME" | githooks/pre-push:12 | CODE-GATED | `tools/config_seal.py verify` → **RC=1**, 3 MODIFIED + 4 UNSEALED |
| A3 | "a count is a snapshot of one tree at one moment … never difference two counts taken at different moments" (census denominator law, B2-216) | AGENTS.md:27 | CODE-GATED (opt-in) | `tools/census_drift_patrol.py --collect` → **RC=1**, "pytest holds **2288** vs carrier claim **1910** (delta **+378**, bar 20)" |
| A4 | "flags this line when its census date is older than 7 days while `tests/` has gained files" (B2-215) | AGENTS.md:27 | CODE-GATED (WARN at hook) | `census_drift_patrol.py` → RC=0 today (0d old); the STALE arm is real, exit 1 |
| A5 | "a red suite blocks the push the way the ratchet does" (LAW-12 card suite) | AGENTS.md:107 | CODE-GATED (conditional) | `workflow_gate.py check --scenarios` → RC=0, "7 cards validated read-only" |
| A6 | "every checked row in the queue's Open section must name a receipt path that resolves on disk" (B2-316) | pre-push:104 | CODE-GATED (WARN at hook) | `checkbox_receipt_gate.py` → **RC=1**, "405 checked Open rows, 69 baseline, **1 offender**" |
| A7 | "Boot docs go STALE at >7d" | AGENTS.md:109 | **TOOL-EXISTS, NOT WIRED** | `freshness_check.py` → RC=0 PASS — but `grep -c freshness_check githooks/pre-push` = **0**. Hand-run only. |
| A8 | "one key, one canonical name … any reader wanting a key calls key_law.get()" | mag/key_law.py:3 | **TOOL-EXISTS, NOT WIRED** | `python -m mag.key_law --audit` → RC=0, orphans:[] — but `grep -c key_law githooks/pre-push` = **0**, and the ratchet **exempts** it: `ENV_EXEMPT_FILES = {"mag/key_law.py", "models/env_load.py"}` |

### TIER B — PROSE-ONLY (a wish with a docstring)

| law_id | law (quoted) | source | enforcement | why it is a wish |
|---|---|---|---|---|
| B1 | **"Spec before behavior change. The doc/spec that owns a behavior is updated BEFORE the code that changes it. No orphan behavior."** | AGENTS.md:103 | **PROSE-ONLY** | The estate's own seed doc says so: seed/BUILD_DISCIPLINE_LAWS.md:11 — *"review law; **no tool can order this for you**"*. Exhaustive search: no tool compares doc mtime to code mtime. `mag/spec_gate.py` is a **different law** (sha256 of a frozen *target file*, not doc-before-code). **NO GATE EXISTS.** |
| B2 | "No timeouts papering over sync problems. No fallback-branch creep." | AGENTS.md:104 | **PROSE-ONLY** | The ratchet's newest rule is literally `except-pass` (650 files, "the estate's biggest disease") — the *symptom* B2 forbids is the one the estate counts most. **A ratchet that counts the disease is not a ban on the disease.** |
| B3 | "Fix comments carry the receipt … names the cause and the evidence" | AGENTS.md:105 | **PROSE-ONLY** | No lint, AST check, or hook inspects comment content. Unknowable by machine in general. |
| B4 | "Data tiers T0–T3 (T0/T1 never to free remote train-on-input APIs)" | CONSTITUTION.md:10 | **PROSE-ONLY** | `configs/lanes.yaml:16` declares `never_tiers: [T0, T1]` and **nothing reads it** — `git grep -rn never_tiers` returns only the declaration + a copy in `dist_audit/`. `mag/dispatch.py:135` only *comments* that T0/T1 "is refused by chat_provider" — **`mag/chat_provider.py` does not exist**. `mag/operator_os.py:36-38` lists "Hard private → remote refuse" as `status: "next"`, an **unbuilt backlog item**. The repo's most load-bearing law is a YAML key no code opens. |
| B5 | "Model text can propose; only the switchboard/effect broker authorizes effects" | AGENTS.md:20 | TOOL-EXISTS (shared_surface validate) — **not in pre-push** | Validatable by hand per AGENTS.md:20; no hook invokes it. |
| B6 | "Chat is heat. Residual on disk is truth." / "fidelity lives in files + chain" | COMPASS:30, DNA.md:4 | **UNENFORCEABLE** | A philosophy, not a predicate. Correctly so. |
| B7 | "a doctrine card that no other file references for N days is demoted" | mag/doctrine_statute.py:1 | **TOOL-EXISTS, NOT WIRED** | `git grep doctrine_statute` outside its own file → **zero callers**. Its own docstring: "no scheduled runs — you call it." A 90-day demotion law that nothing calls has demoted nothing. |
| B8 | "If that file is missing, stop and restore it before public claims" | CONSTITUTION.md:15 | **PROSE-ONLY (and its target is missing)** | `../mycelial-republic/docs/CONSTITUTION.md` **exists** ✓. But AGENTS.md:116 points at `mycelial-republic docs/CONSTITUTION.md` and, read locally, `local_sovereign_agent/docs/CONSTITUTION.md` **does not exist**. A stop-law with a broken pointer. |
| B9 | "never trust a hand-written count" / "Trust bytes, not reports" | AGENTS.md:27, TRUST_BYTES_LAW.md:10 | CODE-GATED for the *one* carrier; **PROSE-ONLY everywhere else** | The law names a specific discipline and gates exactly one number in the repo. |

**Count (matches lane6_laws.json): 7 code-gated · 4 tool-exists-not-wired · 7 prose-only/unenforceable.**
(Of the 7 code-gated, one is the hook itself, recorded as G1 — armed, correct, and unreachable.)

---

## 2. SOCRATIC INTERROGATION — the eight questions that would embarrass each law

### Q1. "Never trust a hand-written count." The census carrier IS a hand-written count.
**The law does not bind the law-writers.**
- Carrier (AGENTS.md:27, written 2026-09-26): **"1,910 tests collected / 303 files"**
- Bytes I ran: `pytest --collect-only -q` → **2288 tests collected in 6.81s**
- **The carrier is wrong by 378.** The law's own `tools/census_drift_patrol.py --collect` says so: `COLLECT-DRIFT … delta +378, bar 20`, RC=1.
- The task brief's suspicion of "378 wrong" is **confirmed by bytes, exactly**.

### Q2. Does the law bind the law-writers? Partially — and only after 11 hours.
The gate exists and is correct. It is **opt-in** (`--collect`), deliberately kept out of pre-push
("it needs the venv"), so its default form cannot see a wrong number. Its scheduled home
`MagCensusPatrolDaily` is **registered and Ready** (next 8:30) — and its own log shows it working:
```
11:33:20  carrier 1879 vs pytest 1910 → COLLECT-DRIFT +31 → ALERT to memory/attention.md → exit=1
11:34:24  carrier 1910 vs pytest 1910 → ok → exit=0
```
So the law caught +31 at 11:33, the carrier was refreshed to 1910, and **by 21:00 the same day the
truth moved to 2288 and nobody noticed** — the next run is 8:30 tomorrow. **A law on a 21-hour poll
against a corpus that gained 378 tests in nine hours is a law that is late by construction.**

### Q3. "Census denominator law: never difference two counts taken at different moments."
**The law has no gate, and the carrier violates it about itself.** The same bullet states
`1,910 collected / 303 files` and, in the same sentence, `disk candidate files: 348` — two instruments,
one moment, differenced in prose. The tool prints that as "instrument lag … evidence only" and exits 0.
The law is honored as a *maxim in a sentence* and unenforced as a *rule in the tool*.

### Q4. "No orphan behavior." Is there a machine check?
**No. None. And the repo admits it.** `seed/BUILD_DISCIPLINE_LAWS.md:11` — "review law; no tool can
order this for you." Law B1 is the *first* of the estate's five build-discipline laws and the only
one with no command beside it. Its siblings all have commands (rules 4 and 5 name their tools).
**The estate shipped four runnable laws and one wish, and numbered them together.**

### Q5. "Fix comments carry the receipt." Enforceable?
**No, and it is the right kind of unenforceable** — comment *quality* is not a predicate. But note
the repo proves the receipt discipline elsewhere with great energy (every card cites file:line), which
makes this law's absence from CI the odd one out rather than principled.

### Q6. Which law does the fleet itself violate most?
**`configs/violation_baseline.json` — 933 accepted debts.** The ratchet's own register is the largest
artifact in the constitution. The reflog names the disease honestly: `54ef0c4bc "ratchet v2: three
rules from real diseases — except-pass (650 files! **the estate's biggest disease**, now counted) …
register 192→867"`. And 6 NEW debts are sitting unregistered right now, 5 of them in **untracked**
files (`tools/ledger_lock.py`, `tools/openrouter_free_gate.py`, `tools/queue_dupes_check.py`,
`tools/transport_precheck.py`, `tools/visor.py`) — the ratchet scans untracked files, the *push* that
would catch them is the one that never runs.

**The single law most violated by the fleet is the ratchet law itself** — not by ignoring it, but by
*reaching for the escape hatch as routine*: 933 named acceptances and a live `baseline-update --by <who>`
path make "accept debt by NAME" the cheapest way to stay green. The escape hatch that was designed to
be rare is now the load-bearing mechanism.

### Q7. Do the last five commits obey the laws they cite?
Yes — and that is the problem's shape. Every recent message is a receipt-bearing, byte-verified,
falsifier-naming commit (`027baff4c`: "bytes verified pre==post sha256 6eec2f0…"). Meanwhile
`6d417abd5` (the tip, 17:43) **touched `configs/violation_baseline.json`** — the very file the config
seal covers — and `config_seal.py verify` is **red right now** (3 MODIFIED, 4 UNSEALED).
**The discipline is exemplary in prose and unenforced in the path.** Also note `git push` was never
run, so the gate that would have said so never spoke.

### Q8. "Trust bytes, not reports" — the sharpest embarrassment.
The estate wrote a 40-line law whose entire content is *"a report is a rumor."* It then shipped a
**git remote 7 days stale, a hook 0 days from arming, a census 378 wrong, a config seal red, and
six new ratchet debts** — every one of which is a *report-shaped* fact that a 30-second byte check
would have caught. The law is not wrong. It is **unread by the people who wrote it**, which is the
only enforcement that was ever really available for prose.

---

## 3. RANKED — LAWS THAT ARE PURE DECORATION

| # | law | why decorative | cost of believing it |
|---|---|---|---|
| **1** | **B4 — T0/T1 never remote** | YAML key no code reads; the guarding module does not exist; the refusal is a `status:"next"` backlog row | **The highest-stakes law in the repo is the least enforced.** A single bad dispatch leaks operator-private data and no gate, test, or hook will ever say so. |
| **2** | **B1 — Spec before behavior change / no orphan behavior** | Estate-admitted: "no tool can order this for you" | The stated headline of the build-discipline section has zero enforcement; behavior drifts from spec silently and forever. |
| **3** | **A7/B9 — Boot-doc freshness** | `freshness_check.py` passes and is wired to **nothing** | Boot docs are the first thing every seat obeys. A stale one is obeyed *confidently* (the law's own words). |
| **4** | **A8 — key_law "one canonical name"** | Audit is green, and the ratchet **exempts** the very files that would catch a violation | The secret-boundary law is enforced by a tool nobody schedules, exempting its own enforcement surface. |
| **5** | **B7 — doctrine_statute 90-day demotion** | Zero callers repo-wide | A law that auto-demotes stale doctrine has demoted nothing; the shelf is whatever the last human felt like filing. |
| **6** | **B2 — No fallback-branch creep** | The estate's *biggest counted disease* is `except-pass` (650 files) | The law names the failure mode the fleet is currently failing at scale, and the ratchet turned it into a **number to manage** instead of a thing to stop. |
| **7** | **B3 — Fix comments carry the receipt** | Unknowable by machine | Low cost; high ceremony. Honest prose. |
| **8** | **B8 — "stop and restore it before public claims"** | Pointer target `docs/CONSTITUTION.md` missing locally | A stop-law with a broken address. |

---

## 4. THE DENOMINATOR OF THE WHOLE THING
**7 laws a machine can refuse, and the refusal path is itself unrunnable.** Even granting full
enforcement, the estate's gates are **pre-push only** on a repo that:
- has **no `origin`** (so `git_backup.cmd` silently no-ops its push),
- has **no upstream** on the active branch,
- whose only remote ref is **6 days older than the hook**.

A pre-push gate on a never-pushed branch is a **ratchet with no wheel**. The single highest-leverage
act for this estate is not a new law, not a new organ, not a new card: it is
`git push -u local HEAD` once, and watching what the hook says. It has opinions. They are good ones.
Nobody has asked it.

---

## 5. WHAT I DID NOT DO
No file was fixed. No gate was flipped. No config was re-sealed. No commit was made. The chain was
not touched. Docker was not touched. The 6 new ratchet debts, the red config seal, and the 378-item
census drift are reported, not repaired — all three are the operator's to accept by name.
