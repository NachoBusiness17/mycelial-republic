# WAVE2 LANE 10 — Shared Surface Contract: Contract vs Enforcement

**Date:** 2026-09-26 · **Lane:** 10 · **Seat:** wave-2 subagent
**Scope:** `watch/inbox/SHARED_SURFACE_CONTRACT.json`, `mag/shared_surface.py`, `watch/inbox/INDEX.json`,
`watch/inbox/index_events.jsonl`, `scripts/index_fold_host.mjs`, `dashboard/static/index.html`, git durability.
**Verdict:** **The shared surface is a convention that leaks.** The contract is well-written; the validator
enforces roughly a third of it, and the board consumes none of it.

---

## Headline numbers (all measured, not estimated)

| Measure | Value |
|---|---|
| Validator exit code (as documented) | **1 — FAILS** |
| Errors on first run | 43 (38 hash mismatch, 4 LINKS event-kind, 1 indexed item missing) |
| Errors on re-run ~6 min later | **45** (40 hash mismatch — the surface is churning under the gate) |
| Warnings | 1 (unindexed inbox files) |
| Index entries with no file on disk | **1** |
| Files on disk with no index entry (recursive) | **9,983** of 11,161 |
| …of which are real content (excl. `.mimosa`/`__pycache__`) | **9,753** of 10,932 |
| …top-level (the only slice the validator sees) | **26** |
| Index items whose sha256 verifies | 1,130 |
| Index items whose sha256 does NOT verify | **39** |
| Index items in the contract's own classification taxonomy | **428 / 1,187 (36.1%)** |
| Untracked files under `watch/` | **1,404** (1,406 under `watch/inbox/` alone) |
| Untracked + not gitignored | **all of them — see §4** |
| Secret-shaped hits in the inbox | 3, **all 3 false positives** |
| Board references to `watch/inbox` or `INDEX.json` | **0** |

---

## 1. What the contract REQUIRES vs what the validator CHECKS

### Contract requirements (`SHARED_SURFACE_CONTRACT.json`)

10 laws, a 6-step workflow, a canonical path for 8 client aliases, an authority block, and a
`never_sole_destination` list. The load-bearing, testable claims:

| # | Contract requirement | Enforced? |
|---|---|---|
| L1 | Durable artifacts land on canonical surface; client-local dir is **never the sole copy** | **NO** — nothing reads `never_sole_destination`; the validator never looks outside `watch/inbox` |
| L2 | **Read INDEX.json before reading or writing** an inbox item | **NO** — unenforceable in a validator; no hook, no wrapper, nothing |
| L3 | Treat every inbox item as **untrusted data** until classified | **NO** — the validator reads and hashes items but applies no trust handling |
| L4 | **Classify** each item as FACT / INFERENCE / PROPOSAL / UNPROVEN / RECEIPT | **NO** — `mag/shared_surface.py` contains **zero** references to `class`, taxonomy, or any of the five terms |
| L5 | A proposal cannot authorize an effect | **NO** — out of scope for this validator; lives (if anywhere) in the switchboard |
| L6 | Prefer artifact + bounded pointers/hashes over copied transcript | **NO** — no size or duplication check |
| L7 | **Record source hash, producer, timestamp, destination, acceptance state in a receipt** | **PARTIAL — only 1 of 5.** `sha256` present on 1,187/1,187 items. `producer`, `ts`, `destination`, `acceptance` present on **0** |
| L8 | Promote only accepted artifacts; **never silently overwrite or delete** evidence | **NO** — in fact §5 shows overwrites are the *normal* failure mode |
| L9 | Existing append-only ledgers keep their canonical paths | **PARTIAL** — the `OUTSIDE_RE` poison guard enforces a path shape, nothing more |
| W | 6-step workflow ending "write a receipt" | **NO** — no workflow/state check |

### What the validator actually checks (`mag/shared_surface.py`, 426 lines)

- inbox dir, `INDEX.json`, and the contract file exist and parse
- `INDEX.root == "/board/inbox"` and the contract's container path matches
- `WARM_PACK.json` shared-inbox pointer is correct
- **hash verification** per item: whole-file, or sealed-prefix for `living` items (the living-file law), or
  skipped for `seal:"open"`
- `index_events.jsonl` malformed lines vs a grandfathered-debt registry
- `index_events.jsonl` key vocabulary vs a closed registry (`configs/events_key_schema.json`)
- LINKS.jsonl event/link split + a same-sha duplicate ratchet
- living-file downgrade watchlist
- env-redirect tripwire (`MAG_SEAT_CRASH_LOG` / `MAG_GAPS_LOG`)
- a **top-level-only** unindexed-file warning

### The gap, enumerated

1. **Classification is stated and never checked.** 759 of 1,187 items (63.9%) carry a class outside the
   contract's own five-term taxonomy — `BACKFILL` (576), `STEAL`, `AMENDMENT`, `DECODE`, `data`, `artifact`,
   `pdf-import`… The vocabulary is not even case-stable: `receipt` (264) and `RECEIPT` (128) are counted
   separately. Nothing fails.
2. **Receipt completeness is unenforced.** Law 7 demands 5 fields; the index carries 1. No `producer`, no
   `ts`, no `destination`, no acceptance state anywhere in 1,187 items.
3. **"Never the sole copy" is unmeasurable as written.** The `never_sole_destination` list names
   `~/.codex`, `~/.zcode`, `%TEMP%`, etc. Nothing enumerates those paths or compares them to the inbox.
4. **The unindexed check is one directory deep.** Line 268 is `INBOX.iterdir()` with `path.is_file()` — a
   flat, non-recursive listing. **9,957 unindexed files in subdirectories are invisible to the gate.** The
   validator reports "26 unindexed inbox files" as a *warning*; the real number is 9,753.
5. **No content check of any kind** — no secrets, no size ceiling, no binary/PII policy, no duplicate
   detection, no symlink or path-traversal check. (§3 extends lane 9: the secrets gap is real, and the
   validator has no secrets check at all.)
6. **No concurrency, no torn-write, no lock check.** (§5.)
7. **Nothing verifies the board or any consumer reads this surface.** (§6.)

---

## 2. Real validator output

```
$ .venv\Scripts\python.exe -m mag.shared_surface validate
EXIT_CODE=1
```

`ok: false`. Full JSON on stdout (188,668 bytes, 6,857 lines). Summary:

```
files(top-level)=1067  indexed_items=1184  unindexed=26
events_log_malformed: {total: 3, grandfathered: 3, new: 0}      <- clean
events_log_keys:      {lines_scanned: 3931, unknown_keys: 0}    <- clean
living_files:         {ok: 11, open: 3, unverified: 0, downgraded: 0}
ERRORS: 43   WARNINGS: 1

  38  hash mismatch
   4  NEW event-kind row in LINKS.jsonl (line 349..352, id 'B2-142-...', writer 'b2-142-cerebras-dig')
   1  indexed item missing: ractor_panel_20260926/cands/_seedrib_two_probe1.py
   1  warning: unindexed inbox files: BURN_b2-wave-fold_20260927_b.md, CATHEDRAL_CURVATURE_SCAN_20260926.json, ...
```

Sample of the 38 hash mismatches — all registered non-living whole-file seals:
`SOCRATIC_GAPS_20260918.md`, `MEMORY_GAUGE.jsonl`, `CARRIER_LEDGER_20260919.json`, `cathedral_build.lock.json`,
`ADAM_ONBOARDING_20260924.pdf`, `cathedral_v1.html`, `MEMORY_GAUGE.jsonl`, and 30 more.

**A re-run ~6 minutes later returned 45 errors (40 hash mismatches).** The surface is churning faster than
the gate can be satisfied — the mismatch count *grew by two while the audit was running*. This is a live
organ, not a stale archive: the living-file law was built to handle exactly this for the ledgers that
declared themselves living, and 38+ items that clearly also grow were never registered with a prefix seal.

**This is the most actionable finding in the report:** the contract's designated gate is red, has been red,
and the operator's "receipts or it didn't happen" law is currently being enforced by a gate that fails.
A gate that always fails trains its readers to ignore it.

---

## 3. Index integrity — two-directional drift, measured both ways

Walked `watch/inbox` recursively (11,161 files) and compared against all 1,184 index items
(1,184 unique relative paths, **0 duplicates**).

### Direction A — index claims a file that isn't there: **1**

```
ractor_panel_20260926/cands/_seedrib_two_probe1.py
```

One dangling pointer. Small, and honestly the good news of this audit.

### Direction B — files on disk the index never mentions: **9,983**

| | count |
|---|---|
| All files on disk (recursive) | 11,161 |
| Tool-cache noise (`.mimosa/`, `__pycache__/`) | 230 |
| Real content files | 10,932 |
| …indexed | 1,177 |
| …**unindexed** | **9,753** |
| — unindexed at top level (what the validator sees) | 26 |
| — unindexed in subdirectories (**invisible to the gate**) | 9,957 |

Unindexed real files by directory:

```
4979  qdrop_export          322  gala_20260925         36  fleet_research_lens
2842  mrpool_export         181  wave_20260916          34  fullsend_s2
 786  burn_wave_20260926     86  bearableguy_export     29  deepseek_research
                             50  mickey                 25  (top level)
```

The two largest unindexed trees — `qdrop_export` (4,979) and `mrpool_export` (2,842) — hold 80% of the
drift. 786 files landed in `burn_wave_20260926/` this week without registering.

### Direction C — hash truth: **39 of 1,169 verified items are lies**

```
whole-file sha256 verified match : 1,130
whole-file sha256 MISMATCH        :  39   <- validator reports 38 (one is the missing-file case)
living sealed-prefix ok          :   11
living open (no byte seal)       :    3
```

So of the entries the index *does* make, **96.7% are truthful**; the index is not lying about what it
registered. The failure is omission (9,753 files), not deception.

**Net:** the index is a *sparse* index, not a drifted one. It is a truthful ledger of ~1,180 items with a
1-item dangling reference, sitting on top of a 10,932-file directory where 89% of content is invisible to
the contract. The contract's promise — "Read INDEX.json before reading or writing an inbox item" — is
operationally void: reading the index tells you about 11% of the inbox.

### Secrets (extends lane 9)

Scanned 3,047 text files (7,444 binaries skipped, >8 MB files skipped) for 11 high-signal patterns
(OpenAI/Anthropic/xAI/Google/AWS/GitHub/Slack key shapes, PEM private-key blocks, bearer headers,
password-assignments). **3 hits, all false positives on inspection:**

- `ADAM_ONBOARDING_FULL_20260924.md:417` — a docs URL matched the password-assignment regex
- `audit_20260926/LANE0_PARENT_INTEGRATOR.md:21` — lane 0's own report *describing* an RSA key
- `burn_wave_20260926/B2_73_secret_scan.py:83` — a scanner's own test string

**Confirm and extend lane 9: the validator has no secrets check, and the current inbox contents happen to
be clean.** Two caveats: 7,444 binary files (PDF/PNG/ZIP) were not scanned, and files >8 MB were skipped,
so this is "no leak found in the scanned text," not "no leak." The enforcement gap stands regardless of
whether today's bytes are safe.

---

## 4. Durability of the untracked `watch/` files — the receipts law has no backup

Measured with `git status --porcelain --untracked-files=all -- watch/`.

| | count |
|---|---|
| Tracked files under `watch/` | 12,743 |
| Tracked under `watch/inbox/` | 9,490 |
| **Untracked under `watch/`** | **1,404** (1,406 under `watch/inbox/`, 2 elsewhere) |
| Ignored under `watch/` | 2,084 |
| Untracked repo-wide | 1,868 |

### Is `watch/` gitignored? Your belief is confirmed, with a precision

`.gitignore` lines 141-147:

```
watch/*.json
watch/*.jsonl
watch/*.txt
watch/.chat_offset
watch/mag.pid
!watch/__init__.py
!watch/*.py
```

`git check-ignore -v` confirms: `.gitignore:141:watch/*.json  watch/WARM_PACK.json`.
In gitignore, `*` does **not** cross a directory boundary. So `watch/*.json` matches `watch/WARM_PACK.json`
and **nothing** under `watch/inbox/`. `watch/inbox/INDEX.json` — the file the entire contract is built
around — is **neither tracked nor ignored**. It is untracked-but-visible, which is the *best* of the three
states and the reason the drift is at least countable. (A true `watch/**/*.json` would have hidden all of
it and made this audit impossible.)

### So: are they durable? Three layers, all weak.

1. **Git:** 1,406 files are untracked. They are in no commit. They will not be in any checkout.
2. **The "backup" remote is not off-box:**

   ```
   $ git remote -v
   local  C:\Users\foste\Documents\projects\Mag-backup.git (fetch)
   local  C:\Users\foste\Documents\projects\Mag-backup.git (push)
   ```

   `Mag-backup.git` is a **local directory on the same physical disk** as the working tree. The operator
   subscribed for a year to a sovereign substrate; the only configured durability target for the shared
   surface is a bare repo ~200 MB away on the same drive. A disk failure takes both. There is no off-host
   remote configured.
3. **The backup is stale even as a local mirror:** it is **538 commits behind** working HEAD
   (local `6d417abd5`, backup `a4733004a`), and `.git/FETCH_HEAD` was last written **Sep 19 21:35** —
   seven days stale. Even the *tracked* 9,490 inbox files are only 7-days-deep in the mirror.

**Answer to the lane question: no, the 889 (now 1,406) untracked `watch/` files have no durability at all.**
They exist on exactly one disk, in one filesystem, with no commit, no remote, and no backup. The operator's
"receipts or it didn't happen" law has, for these files, a single point of failure that is the physical disk.
A hash is only a receipt if someone else can check it after you die.

---

## 5. Multi-writer correctness — the contract does not handle concurrency, and the writer admits it

### Is there locking? No.

- `watch/inbox/` contains **no lock files** for the index or the event log. (The only `*lock*` hits are
  unrelated content: `cathedral_build.lock.json`, and `LEDGER_LOCK_TEST.lock.log` — a one-off probe from
  2026-09-27T00:06Z showing acquire/release/stale-break across pids 24080, 26376, 12256, 21116, 13128, 20736.)
- `scripts/index_fold_host.mjs` (808 lines) contains **no lock acquisition** of any kind.
- `mag/shared_surface.py` is read-only by design and has no concurrency handling.

### Is the write atomic? Partially — and the partial part is the dangerous part.

`writeIndex()` at line 529 does the right thing for the *publish* step:

```js
const tmp = `${INDEX_FILE}.tmp`;
writeFileSync(tmp, JSON.stringify(out, null, 2) + '\n', 'utf8');
renameSync(tmp, INDEX_FILE);   // atomic on same fs
```

Events append via `appendFileSync` (O_APPEND), which is atomic for small lines.

**But there is no lock around the read-modify-write that produces `items`.** `writeIndex` reads the existing
header, merges, and replaces the whole file. Two folds racing means the second `renameSync` publishes a
whole index built from a stale base — a classic lost update. The single fixed `INDEX.json.tmp` name makes it
worse: two concurrent writers share one temp path, so a slow writer's bytes can be renamed by a fast one.

### The writer's own header documents this having already destroyed work

`scripts/index_fold_host.mjs:75-80`, verbatim:

> *Rebase note: this block and the events-command filter were landed once at 16:33Z, **erased at 16:35:35Z by
> a concurrent stale-base whole-file write (the B2-250 disease**, claimed for this file at 16:06:18Z by B2-280
> whose snapshot predated the landing), and re-applied on the post-erase bytes named in the receipt.*

Two minutes after a block was landed, a concurrent stale-base write **erased it**, and a later writer
re-landed it on bytes that had moved underneath it. The disease is named, understood, and still unmitigated.

### Would the validator catch a torn write?

**Partially, and only by luck.**

- A **torn `INDEX.json`** would be caught — `_load()` would raise and produce `invalid INDEX.json`. Good.
- A **torn event-log line** would be caught — the B2-42 malformed-line gate is real and currently clean
  (3 malformed, all 3 grandfathered, 0 new; 3,931 lines, 0 unknown keys). This is the best-engineered part
  of the whole validator.
- A **lost update** (whole index valid, but missing another writer's items) would **NOT** be caught. The
  index stays schema-valid and every surviving item still hashes correctly. The validator has no concept of
  "an item that was registered and then vanished from the index" — which is precisely the 1-item dangling
  case it *does* catch, but only when the file also disappeared. An item dropped from the index while its
  file remains is silently invisible, and indistinguishable from "never registered."

That is why the 9,753-file omission (§3) can grow without any gate noticing. **The validator can tell you
the index is internally broken; it cannot tell you the index is incomplete.**

---

## 6. Consumers — who actually reads `watch/inbox/`?

Grepped `mag/`, `scripts/`, `dashboard/`, and probed the live board.

| Consumer | Reads the shared surface? |
|---|---|
| `dashboard/static/index.html` (the board) | **NO — zero references.** Its only network call is `fetch('/api/v1/surfaces/liveness')`. No `INDEX.json`, no `inbox`, no `/board/`. |
| `dashboard/static/board.js` | **NO** — zero inbox references |
| `mag/api_gateway.py` (serves :8765) | **NO** — has `/room/inbox/{seat}`, an unrelated per-seat room queue. No shared-surface route. |
| `mag/shared_surface.py` | Yes, read-only, validator only |
| `scripts/index_fold_host.mjs` | Yes — the only writer |
| `mag/link_library.py`, `ox_novelty_index.py`, `corpus_selfsteal.py`, `scripts/librarian.py`, `build_deck.py`, `build_knowledge_graph.py` | Yes, as one index among many |

### Live probe of the operator's actual board

```
GET /                                  -> HTTP 200   (board is up)
GET /api/v1/surfaces/liveness          -> {"error":"not found","path":"/api/v1/surfaces/liveness"}
GET /board/inbox/INDEX.json            -> HTTP 404
GET /inbox/INDEX.json                  -> HTTP 404
```

**This is the split-brain finding, and it is a clean one.** The board at
`desktop-7c70ksc.tail8403e9.ts.net` → `127.0.0.1:8765` does not read a *different* copy of the inbox — it
reads **no copy of the inbox at all**. Its sole data fetch 404s even in the live process, and the board
falls back to an embedded evidence map (`.catch(()=>{})` at line 127).

So the contract names the board's own surface as canonical:

```json
"canonical": { "container": "/board/inbox", "read_first": "/board/inbox/INDEX.json" }
```

and `INDEX.json` self-describes as `root: /board/inbox`, `read_first: /board/inbox/INDEX.md`,
`host_root: /board/inbox`. **The board serves nothing at that path.** A contract that specifies a discovery
pointer no consumer implements is a contract enforced by nothing.

The stakes are higher than a dead endpoint: the contract's L2 is *"Read INDEX.json before reading or writing
an inbox item."* If the operator's primary surface doesn't read the index, the shared surface is invisible
from the place the operator actually looks. The fleet's file-based design works precisely because the board
is a reader of those files. Today it is not.

---

## 7. Tri-state

**Supported (measured, reproducible):**
- The validator fails: exit 1, 43 errors, growing to 45 in six minutes.
- Index↔disk drift is 1 dangling entry vs 9,753 unindexed real files; the validator sees 26 of those.
- 1,406 untracked files under `watch/inbox/`; `watch/*.json` does not match nested paths (confirmed with
  `git check-ignore -v`).
- The only git remote is a same-disk directory, 538 commits stale, last fetched Sep 19.
- No index/event-log locking; the tmp+rename is atomic but the read-modify-write is not; the writer's own
  header records a stale-base whole-file write erasing landed code.
- The board has zero inbox references; its only fetch 404s live.

**Disputed:**
- Whether 9,753 unindexed files are *supposed* to be indexed. `qdrop_export` (4,979) and `mrpool_export`
  (2,842) look like bulk machine exports rather than individually-registered artifacts, and the contract
  law 9 explicitly says the inbox is "not a flattening operation." The defensible reading is that exports are
  deliberately unregistered — **but nothing in the contract or the validator says so, and no directory is
  declared out of scope.** The *enforcement* gap is unarguable even if the *content* gap is partly intended.

**Unproven:**
- How long the gate has been red, and whether anyone is reading its exit code. No CI binding for
  `mag.shared_surface validate` was found in the search performed; whether the commit hook invokes it is
  not established either way.
- Whether the 538-commit backup lag and 7-day-stale fetch are intentional batching or a silently broken
  push. No push evidence was examined.
- Whether the 38+ hash mismatches are in-flight appends that would clear on a re-register, or genuine
  overwrites violating law 8 ("never silently overwrite"). Not distinguishable without per-file mtime
  forensics, which was out of scope here.

---

## 8. Recommendations, cheapest first

1. **Make the unindexed check recursive**, or declare out-of-scope directories in the contract
   (`qdrop_export/`, `mrpool_export/`, `.mimosa/`). One line at `mag/shared_surface.py:268` closes a
   9,957-file blind spot.
2. **Stop the red gate from being red.** Re-register the 38 churning files with `add --living` (prefix seal)
   or refresh their hashes. A permanently-failing gate is worse than no gate.
3. **Add an off-host remote.** `git remote add` a real off-box target and push. Everything else in this
   report is recoverable from a disk; this is not.
4. **Enforce classification** — reject an item whose `class` is outside the five-term taxonomy (and fold
   `receipt`/`RECEIPT` to one spelling). 63.9% of items currently violate a law the validator never reads.
5. **Lock the fold's read-modify-write** (a lockfile around `writeIndex`, and a unique temp name per
   writer). B2-250 already cost one erasure; nothing prevents a second.
6. **Make the board read the surface it is named as the host of**, or amend the contract to stop claiming
   `/board/inbox`. Either is honest; the current state is neither.
7. **Add a secrets + size gate** to the validator so today's clean result is enforced rather than lucky.

---

## Appendix — commands run

```bash
.venv\Scripts\python.exe -m mag.shared_surface validate          # exit 1, 43->45 errors
git check-ignore -v watch/inbox/INDEX.json watch/WARM_PACK.json
git status --porcelain --untracked-files=all -- watch/ | grep -c '^??'
git ls-files watch/ | wc -l                                       # 12743
git remote -v; git rev-list --count local/main..HEAD              # 538 behind
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8765/board/inbox/INDEX.json   # 404
```

**Artifacts:** `memory/audit_20260926/w2l10_surface.json` (machine-readable),
`memory/audit_20260926/_w2l10_drift.json`, `_w2l10_secrets.json`, `_w2l10_validate.json`,
`_w2l10_validate2.json` (raw validator runs).
