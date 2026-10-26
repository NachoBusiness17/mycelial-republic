Two spot-checks re-run this session in the sandbox copy (`seed_checks/sandbox_seed`): `python engines/key_law.py --audit` → `ModuleNotFoundError: No module named 'models'`; `file MANIFEST.sha256` → "ASCII text, with CRLF line terminators"; Python content-hash check → "15 of 15 rows verified". All other runs cited below come from the supplied dogfood/gap reports, marked *(evidence)*.

---

# THE SEED V2 BUILD-BOOK

## 1. THE LANDSCAPE — who else ships a method-as-seed

Eight closest prior art; each line = what they have that we lack.

1. **Agent Skills (Anthropic / agentskills.io, 40+ clients)** — a published spec whose metadata contract (`name`/`description`) *is* the discovery API, with progressive disclosure keeping context cheap; our one-pager loads all 11 laws at once and has no discovery contract. *(evidence: prior-art entry)*
2. **AGENTS.md (Linux Foundation, ~60k repos, ~20 tools auto-read it)** — a vendor-neutral filename so any tool finds the method unprompted, plus nested-file precedence; THE_METHOD.md has no convention an agent auto-loads. *(evidence: prior-art entry)*
3. **Cline memory-bank** — the ritual is tool-agnostic copy-paste prose where the agent itself bootstraps and re-reads the archive every task ("not optional"); mass adoption we lack, though human-enforced with no meters. *(evidence: prior-art entry)*
4. **Cookiecutter Data Science (10,074 stars, PyPI CLI)** — an official `ccds` scaffold, docs site, and a decade of strangers continuing projects without authors; we ship no install path at all. *(evidence: prior-art entry)*
5. **12-Factor Agents (HumanLayer, 26,377 stars)** — named-factor vocabulary (own your context window, contact humans with tool calls) that won the shared language for our law-space; it's a document, not a bootable system — the vocabulary market is open. *(evidence: prior-art entry)*
6. **Ralph loop (ghuntley)** — a self-executing pass condition: bash loop + PROMPT.md a stranger clones and continues, spread as folklore; our reset-aware burner is the same shape but unpublished and, worse, unrunnable. *(evidence: prior-art entry)*
7. **Cursor rules (40.8k-star channel)** — path-glob scoping so each rule fires exactly when relevant, plus marketplace distribution; our laws are all-or-nothing at load with zero distribution machinery. *(evidence: prior-art entry)*
8. **OpenClaw (~390k stars)** — enormous distribution for a self-hosted personal-AI runtime whose publicized "security nightmare" critique is precisely the gap our one-door/freeze-seal laws claim to close — our best strapline, their weakest point. *(evidence: prior-art entry)*

Pattern: everyone who spread ships (a) a discovery contract, (b) low-friction install, (c) distribution/community. Seed V2's differentiation — runnable engines, loud audits, a falsifiable pass condition — only counts once items 1–8 below make it boot.

## 2. THE DOGFOOD RECEIPT — what broke cold

Verbatim from the cold-copy run (fresh copy, `/tmp/seed_cold_20260924_215939`, Python 3.12.10) *(evidence: dogfood breakage)*; items 1 and 5 re-confirmed this session:

- **`engines/estate_smith_chart.py` — CRASH.** `FileNotFoundError` at `estate_smith_chart.py:253` on `watch\inbox\ESTATE_SMITH_CHART_20260925.json` — nothing creates `watch/inbox/`, so FIRST_BOOT's "you have no records yet" promise never prints; the crash lands before the console meter at :259, and the matplotlib dep (:283) is never reached.
- **`engines/key_law.py` — CRASH in all three forms.** `--audit` and `-m engines.key_law` → `ModuleNotFoundError: No module named 'models'` (`key_law.py:23`); the docstring's own CLI (`key_law.py:9`, `python -m tools.key_law`) → `No module named 'tools'`. Even un-crashed, it reads a `configs/keys.json` that isn't shipped (:21) and orphan-scans `mag/*.py` (:78-79), finding zero orphans silently.
- **`engines/cooker.py` — status WORKS COLD, exit 0**, all three reset lanes "DUE NOW" (honest: no ledger exists; :86 guards on `is_file()`). But `--due` fires point at `tools/stealth_sweep.py` / `tools/task_wall.py` (:40,43 — shipped under `engines/`), and the METER_ONLY lane imports `mag.lite_guard` (:132). *(Evidence's fire run: all three resets fired, all three failed; failures honestly receipted to the ledger, exit 1.)*
- **`engines/claritas.py` — NO-OP as script, works as module.** 64 lines, no `__main__`; a stranger running it gets zero output. Imported: `vendor_for('glm-4.7')='zai'` — pure stdlib, exit 0.
- **`MANIFEST.sha256 — sealed on content, uncompareable by the standard tool.** `sha256sum -c` → all 15 entries "FAILED open or read" (CRLF); Python hashlib → "15/15 files match, 0 mismatched."

Net: the pass condition (HANDOFF.md:9-10, "a stranger boots this seed and continues") fails at minute one. *(Evidence)*

## 3. THE GAPS — deduped, ranked

**HIGH**

1. **7 of 12 engines are import-dead on any box but the author's.** `from models.env_load import load_dotenv` at `key_law.py:23`, `model_bakeoff.py:27`, `stealth_sweep.py:29`, `task_wall.py:27` → ModuleNotFoundError (`models/` never copied; `build_seed.py:63-82` flattened `mag/`+`tools/` into `engines/` without rewriting imports). Re-confirmed this session.
2. **FIRST_BOOT step 2 dies twice before printing one meter** — `watch/inbox/` never mkdir'd (`estate_smith_chart.py:29-39`), then matplotlib; only the undocumented `--no-plot` works. *(evidence)*
3. **The cooker burns nothing and no scheduler ships.** Fires target `tools/*.py` (`cooker.py:40-46`); `mag.lite_guard` import dies (:132); latent `ValueError: day is out of range for month` for any hour>0 reset on the 1st (`cooker.py:55`); no cron/schtasks/systemd anywhere despite FIRST_BOOT.md:16-18. *(evidence)*
4. **The atlas is unportable and reads the author's disk.** `estate_atlas.py:34` hardcodes `C:\Users\foste\...`; on that machine it minted 1,207,962 rows into the real estate (disclosed side effect); elsewhere it exits 1 naming an unshipped walker — while FIRST_BOOT.md:11-13 claims it "walks your files" against its own header "This tool NEVER re-walks the disk" (:13). *(evidence)*
5. **Law 7 is violated by the seed itself: six key doors, zero users of the loader.** No engine calls `key_law.get()`; `lite_guard.py:47`, `task_wall.py:73-78`, `model_bakeoff.py:43`, `stealth_sweep.py:45-51` read `os.environ` directly, `phone_relay.py:32` reads `%LOCALAPPDATA%\hermes\.env`; no `configs/keys.json` template; the orphan scan reads files not shipped. *(evidence)*
6. **The operator gate approves on substring match.** `APPROVE_WORDS` contains `'y'`, `'1'` (`phone_relay.py:37`); the decision-loop harness returned approve for "maybe later", "are you sure?", "why not" (network monkeypatched; fail-closed on timeout/unknown-author held). *(evidence)*
7. **No setup page, no license.** Zero requirements/pyproject; matplotlib required (:283-285), `Path.is_relative_to` sets a ~3.9 floor (:37); no LICENSE grants the copy/run/modify the pass condition requires. *(evidence)*
8. **The workload is the author's private data.** Task-wall pillars and the 1976 anchor chore are hardcoded Python lists (`task_wall.py:47-53`, `stealth_sweep.py:39-42`); two personal gmail addresses sit in `lite_guard.py:42`; no keys/signup walkthrough — the schema exists only inside the validator (`key_law.py:42-91`). *(evidence)*

**MEDIUM**

9. Seal fails its own compare (CRLF, `build_seed.py:93` `write_text` without `newline='\n'`); nothing in-package mentions the manifest.
10. Meters that lie: `checkpoint_apply` reads gamma=0.0 **DELIVERING** on zero records (`estate_smith_chart.py:214`, no DARK branch) against its own "a dark meter is itself a finding" (:12); organs hardcoded to three providers (:67); `lite_guard.provider_quota` returns None and `record()` silent-fails (:168-169, 247-250).
11. Unresolvable self-citations: every docstring's CLI points at `mag/`/`tools/`; `lite_guard.py:1,35` cites "law 15" (THE_METHOD has 11); uncheckable claims (1/12, 63GB) plus PII.
12. No versioning, no tests (law 8 unmet; dead `cooker.py:55` branch), no example record despite law 2, librarian shelves hardcoded (`librarian_catalog.py:35-53`), `verify_canon` exits 0 on drift.
13. Discord relay unbootable and off-door: no setup steps for token/`DISCORD_ALLOWED_USERS`.

**LOW** — claritas falls back to `neutral` for real ids like `gpt-4o` (`claritas.py:36-51`); seed can't rebuild/reseal itself (`build_seed.py:63-75` reads unshipped inputs); hardcoded report filenames stamp the author's dates (`task_wall.py:31`).

## 4. THE BUILD ORDER

1. **Boot-cold all 12 engines.** Inline or ship the dotenv loader; kill all `mag.*`/`models.*` imports; repoint cooker at `engines/*`; add `__main__` to claritas; `mkdir(parents=True)` before writes. Serves **law 7** (a door that opens) and **law 4** (meters run). *Test: fresh temp copy on a clean interpreter; `python engines/<x>.py` for all 12 → exit 0 or a readable nonzero message — no traceback, no missing module.*
2. **Ship SETUP.md: requirements (matplotlib optional), Python ≥3.9 floor, LICENSE, and the seal-verify command in FIRST_BOOT step 0.** Serves **law 9** (the compare step) and **law 3**. *Test: `sha256sum -c MANIFEST.sha256` exits 0 on Windows and Linux out of the box; `--no-plot` runs with zero installs.*
3. **Honest meters.** DARK branch for `checkpoint_apply` (`:214`); print the meter before persisting; organs/shelves read from config; `lite_guard` fails loud when provider truth is unreachable. Serves **law 4**. *Test: zero-state run prints 8/8 DARK, exit 0; point lite_guard at a dead endpoint → nonzero exit naming the failure, never a silent None.*
4. **One key door.** Ship `configs/keys.json` template + filled example + signup-to-first-token guide for the free tiers; every lane calls `key_law.get()`. Serves **law 7**. *Test: grep `os.environ` in `engines/` → only `key_law.py`; audit with one undeclared env key exits nonzero naming it.*
5. **Portability + chores manifest.** `estate_atlas --root` (no hardcoded path), shipped walker or honest message, `chores.json` replacing hardcoded pillars/anchor chores. Serves **law 6** (steal shapes, not artifacts) and **law 2**. *Test: atlas on an empty temp dir → honest empty atlas, exit 0; a stranger-authored chore executes through a stubbed lane; `grep -r foste engines/` → zero hits.*
6. **Operator gate: exact-token approval.** Drop substring matching; require the ask-specific token or a reaction. Serves **law 10**. *Test: re-run the decision-loop harness — "maybe later", "are you sure?", any prose containing 'y' → deny; only the exact token approves.*
7. **Seal + adversarial tests.** Regenerate manifest LF (`newline='\n'`), ship `verify_seal.py` (exit 1 on drift, survives missing files), pytest covering window math (the 2026-10-01 hour=1 case), seal, audit, gate. Serves **laws 9 and 8**. *Test: tamper one byte → verifier exits nonzero naming the row; `pytest` green including the month-edge case that crashed `cooker.py:55`.*
8. **Identity and discovery.** SEED_VERSION + changelog; purge PII, "law 15", date-stamped filenames, unshipped citations; add an AGENTS.md pointer ("read FIRST_BOOT.md first") and skill-style frontmatter on THE_METHOD. Serves **laws 3 and 1**. *Test: `grep -rn "law 15\|@gmail\|20260923" engines/` → zero; fresh agent session reads FIRST_BOOT unprompted (manual check — reported as manual, not automated).*

Order rationale: 1–2 are the boot; 3–4 make the core claims true; 5–6 close the trust holes; 7–8 make it spreadable and self-verifying. Nothing in 1–8 invents a new law — every item makes an existing law executable.

=== RACTOR RULING ===
All evidence is in — everything load-bearing now rests on runs or reads from this session. Ruling:

---

# RULING: CONTESTED — the claim fails on the seed's own bar

**The bar, first-hand:** `HANDOFF.md:9-10` — *"The stranger-continuation bar (G7): a stranger boots this seed and continues without the original operator. That is the pass condition of this package."* I read G7 as the seed's own 7-step first-hour boot (`FIRST_BOOT.md:5-20`). On that bar the claim is false, and I don't reach a close call: **the stranger dies at step 2, again at step 3, by construction at step 4, and again at step 7.** 2 of 7 steps work.

## The numbers that decide it

Every "mine" below was executed or read this session in a fresh temp copy (`C:\Users\foste\AppData\Local\Temp\seed_ractor_dtf53rdx\seed`, Python 3.12.10, API keys stripped from the probe env so nothing could authenticate a live call). The seed itself was only read, never written.

| # | Check (exact run) | Result | Source |
|---|---|---|---|
| 1 | Package inventory | Folder holds **28 files / 245.6 KiB**, because 12 `.pyc` files (144,537 B) sit baked into `engines/__pycache__/`. The 16 source files total **106,988 B (104.5 KiB)**. The claim's "136KB, 16 files" matches neither number | mine |
| 2 | Step 2: `python engines/estate_smith_chart.py` | **rc=1**, `FileNotFoundError: ...seed\watch\inbox\ESTATE_SMITH_CHART_20260925.json`. Verbatim: the write at `estate_smith_chart.py:253` precedes the console meter at `:259` — the promised "you have no records yet" zero-state never prints | mine |
| 3 | Same with `--no-plot` | **rc=1, identical crash** — the write at `:253` also precedes the `--no-plot` branch at `:255` | mine |
| 4 | Step 3: `engines/key_law.py --audit`, `--status`, and `-m engines.key_law --audit` | **rc=1 in all three forms**: `ModuleNotFoundError: No module named 'models'` at `key_law.py:23` (verbatim). Line 21 reads `configs/keys.json` — absent from the 16 files | mine |
| 5 | Steps 2/3 of the remaining burn engines, script-form | `model_bakeoff.py:27`, `stealth_sweep.py:29`, `task_wall.py:27` → **all rc=1, same `models` ModuleNotFoundError**. So **4 of 12 engines are import-dead** — all four now reproduced by me, not inherited | mine |
| 6 | `python engines/cooker.py status` | **rc=0**, honest output (three lanes DUE NOW on an absent ledger). But `cooker.py:40,43` fires target `tools/stealth_sweep.py` / `tools/task_wall.py` — a layout the package doesn't ship (read verbatim) — and those targets are the import-dead engines of row 5 | mine |
| 7 | Step 4: estate_atlas | **Deliberately not run** — `estate_atlas.py:34` verbatim: `REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")`; running it would write into the real estate. Fails by construction on any non-author machine | mine (read only) |
| 8 | Seal, stock verify: `sha256sum -c MANIFEST.sha256` (Git for Windows) | **rc=1, 15/15 rows "FAILED open or read"** — manifest is 15 rows, **15 CRLF, 0 bare-LF** | mine |
| 9 | Seal, content: Python hashlib vs manifest | **15 ok, 0 bad** — content is intact; the failure is line-ending hygiene at the seal's own front door | mine |
| 10 | Syntax: `compileall` all 12 engines | **rc=0** — every death above is packaging, not syntax | mine |
| 11 | Law 7 (one door): grep `os.environ|os.getenv` | **12 direct env doors across 9 engines**; grep `key_law` across engines → **zero callers** (only key_law's own docstring and build_seed's provenance comment). The one door exists, nobody uses it, and it doesn't open | mine |
| 12 | Law 8 (adversarial): my month-edge probe on `cooker.window_start` | hour=0 @ 2026-10-01 00:30 → returns cleanly (dead branch, as supplied evidence said); **hour=1 same instant → `ValueError: day is out of range for month` at `cooker.py:55`, rc=1**. Latent crash in load-bearing window math, found by one 3-line probe — the tests that would have caught it: zero shipped | mine |
| 13 | Law 10 (operator's hand): read `phone_relay.py:187-188` | `words` is the lowercased message **string**; `any(w in words for w in APPROVE_WORDS)` with `'y'` in the set → **substring match**, and the approve branch runs first — so the relay **approves the literal reply "deny"** (it contains "y") | mine (code read; the supplied decision-loop harness independently demonstrated the same class) |
| 14 | Identity/PII grep | `@gmail` at `lite_guard.py:41` (two personal addresses, verbatim); `foste` at `estate_atlas.py:34`; stale **"law 15" ×4** in `lite_guard.py` (:1, :11, :35, :233) while `THE_METHOD.md` has 11 laws (read in full); `is_relative_to` at `estate_smith_chart.py:37,201` → unstated Python ≥3.9 floor; **LICENSE, requirements.txt, pyproject.toml, SETUP.md, tests, configs/, models/ — all absent** (18 artifacts checked, 18 absent) | mine |
| 15 | Step 7 (daily meters) | Same smith chart as row 2 → same crash | mine |

**FIRST_BOOT scorecard (cold, stranger-shaped):** step 1 read ✔ · step 2 ✘ crash · step 3 ✘ crash · step 4 ✘ hardcoded to the author's disk · step 5 ✔ (hand-written markdown; no tool needed, none shipped) · step 6 ◐ status runs, fire burns nothing · step 7 ✘ same crash. **2 of 7 pass; the pass condition fails at minute one.**

## Two corrections to the supplied evidence

1. **"`--no-plot` works" is false.** Both forms die at the same `:253` write — my runs, rows 2–3. The build-book's gap 2 understates by one failure.
2. **The PII line is `lite_guard.py:41`, not :42** (verbatim read; :42 is the "dashboard WRITES" continuation).

## Adverse-to-self (what cuts against my ruling)

- **The method layer genuinely ships.** `THE_METHOD.md` (11 laws + falsifier stamp) and the two other docs are coherent, readable, and import nothing; steps 1 and 5 work. A stranger who only *reads* does receive the intellectual payload.
- **Two engines run cold and behave honestly:** `cooker.py status` (rc=0, honest DUE NOW on an absent ledger) and `librarian_catalog.py` (rc=0, prints an honest zero state — `curated_shelves: 11, total_files_curated: 0`, a probe the supplied evidence never ran). `claritas` works as a module.
- **The seal is content-intact** (15/15) — the defect is hygiene, not tampering.
- **All 12 engines compile** — this is a fixable packaging failure (the build-book's step 1–2 is roughly a day), not a rotten method.
- My box is the author's own (author's Python, Git's sha256sum). But every hard failure I reproduced involves files *absent from the package* (`models/`, `configs/`, `tools/`, `watch/`), so no plausible stranger environment rescues it — environment variation cuts against the claim, not for it.
- Nothing destructive ships; I exercised no network paths (no keys by design), so "no harmful outbound behavior" is bounded by not-run.

## My falsifier

**The run that overturns CONTESTED:** a clean Python ≥3.9 box — fresh VM, no estate files, no author env vars — executing `FIRST_BOOT.md` steps 1–7 verbatim with zero operator contact. If all seven steps exit 0 or exit with a readable, documented nonzero message (no traceback, no missing module), the stranger starts one record and a scheduled cooker fire actually burns *their* free lane — then G7 is met and I reverse. Narrower tripwires that each force a re-rule: (a) a revision where `import engines.key_law` (and the other three) succeed without `mag/` or `models/`; (b) `sha256sum -c MANIFEST.sha256` exits 0 on both Windows and Linux; (c) the smith chart prints its zero-state meter in a copy with no `watch/`. **The run that would harden my ruling:** one real stranger fails inside ten minutes on steps 2–3.

**Not run, stated plainly:** `estate_atlas.py` (would write into the real estate via the hardcoded `REPO`); all network engines beyond import; `cooker.py --due`; the decision-loop harness (it ships nowhere — there is no `tests/` to run). The supplied dogfood fire-run and atlas 1.2M-row figure are cited as supplied, not re-verified.

## Questions for the operator about what this seed is really for

1. **Who is the stranger?** The workload is yours — the 1976 anchor chore, hardcoded pillars, your two gmail addresses at `lite_guard.py:41`, your reset windows at `cooker.py:38-48`, your Discord relay. A stranger who "continues" continues *your* research on *their* accounts. Is G7 written for a stranger, or for you-after-amnesia — the reader who still has the estate to diff against? The two bars need different minimum builds, and this package is much closer to the second.
2. **The seed violates at least five of the eleven laws it ships** (3 — stale "law 15" citations and unverifiable 1/12 and 63GB claims; 4 — the meter crashes; 7 — twelve doors, no door-opener, and the door is dead; 8 — zero tests, and my one adversarial probe found the month-edge crash; 9 — the seal fails its own stock compare). Is `THE_METHOD.md` a description of how this seat works, or a bar you accept being measured against? Because law 8 says this seed should not have shipped, yet the falsifier stamp at `THE_METHOD.md:54` claims the method was tested — tested as a card of facts, never booted as a package.
3. **What does "continues" mean in a form a machine can check?** Right now G7 is a sentence nobody has ever executed. What is the smallest scripted falsifier — a `first_boot_check.py` a CI stranger-box runs — and would its green count as the pass bar, or does the bar only count when a human stranger fails?
4. **If the method is the product** (`HANDOFF.md:4-6`: the facts scored 1/12; the laws transfer), why is the package ~104KB of your artifacts rather than the method parameterized — chores.json, a keys template, neutral anchors, no hardcoded path? And is "shippable today" even the claim you want to defend, or is it "shippable after build-book steps 1–2," which is a day's work?
5. **Whose hand is on the stranger's spend?** The cooker burns free-tier accounts on your anchor chore, and the gate that is supposed to keep a human in the loop approves the word "deny." When the first stranger's key hits its wall mid-burn, what ships that tells them what happened — and does law 10 survive the transplant?


---

# V2 RECEIPT (2026-09-25, items 1-2 executed same night)

Builder: `tools/seed_v2.py` (anchored transforms, fails loud if estate sources move).
Automated falsifier: `tools/cold_boot_test.py` — fresh temp copy, estate env stripped
(LOCALAPPDATA redirected, PATH minimal, keys absent), 14 checks.

**SCORECARD: 12 PASS / 2 readable-fail / 0 crashes.** V1 was 2-of-7 first-boot steps;
V2: seal verifies both via shipped `verify_seal.py` (20/20) AND stock `sha256sum -c`;
smith chart prints honest DARK meters in a copy with no watch/ (crash killed by mkdir);
key audit passes on the shipped template (awaiting-status entries); cooker status + fire
run (fires honestly no-op with a "declare keys" message); walker (`spine_walk.py`, the
real indexer) now ships; atlas names the shipped walker; relay fails closed readable.

Ractor tripwires: (a) engines import without mag/models ✓ (b) sha256sum -c exit 0 —
verified on Windows (Git sha256sum); Linux box not available tonight, stated plainly
(c) smith zero-state in a copy with no watch/ ✓. G7 full bar (a human stranger, zero
contact) is now RUNNABLE via cold_boot_test.py — the proxy passed; the human run remains
the real test. Fixes landed in the ESTATE too: relay _allowed_users guard + main-block
readable failures + the month-edge window fix in cooker (timedelta, not day-arithmetic).


## V2.1.0 RECEIPT (same night, items 3/6/7/8-lite + first key door)

- Item 3 (honest meters): checkpoint organ now DARK on no evidence — cold run shows all
  8 organs DARK at zero state, no meter claims DELIVERING on nothing. Fixed in the ESTATE
  source; seed inherits.
- Item 6 (exact-token gate): inherited from the live relay fix (e330bae88).
- Item 7 (tests in-package): tests/test_seed_laws.py — stdlib unittest, zero installs:
  cooker window math incl. the exact month-edge regression case (hour=1 @ 00:30 on the 1st
  → Sep 30, the V1 crash), relay exact-token decisions ('deny' never approves), seal
  integrity. **6/6 pass in a cold copy.** (Honest note: two of my test EXPECTATIONS were
  wrong on first run — the tests caught the test author too.)
- Item 8-lite: SEED_VERSION 2.1.0 + CHANGELOG.md.
- Item 4 first door: engines/keys.py — stealth_sweep reads keys through it; a live-but-
  undeclared key prints a loud orphan warning. task_wall/bakeoff wiring = item 4 continues.

**Cold boot: 12 PASS / 2 readable-fail / 0 crashes. Tests cold: 6/6 OK. Seal: 25 files.**
Remaining from the build-book: 4-continue (wire task_wall/bakeoff through keys.py),
5 (chores.json + full atlas portability), 8-continue (unverifiable-claims citations).


## SPEC: PYC EXCLUSION AT SEAL (2026-09-25, gala afterparty t7, from a08's catch)

The seal walk in `tools/seed_v2.py` must never collect compiled bytecode.

- **Excluded from collection:** any path under `__pycache__/`, plus `*.pyc` / `*.pyo`
  anywhere in the seed tree.
- **Purge before seal:** the builder deletes stray `seed/**/__pycache__/` directories
  before writing `MANIFEST.sha256`. Purge-only is not enough (a name-matched file can
  still be sealed) and exclude-only is not enough (the shipped tree would still carry
  unsealed bytecode): any pytest/unittest run inside `seed/` recreates `__pycache__`,
  so the NEXT build re-seals it unless the builder itself strips it.
- **The builder emits the zip itself**, from the sealed manifest rows plus the manifest
  (zip contents == seal contents by construction), staged under a top-level
  `seed-<ver>/` folder, sorted entries, forward slashes, and no Python process is ever
  run inside the seed tree during zipping (reading bytes only; unittest would
  re-create pycache).

**Why:** compiled bytecode embeds compile-time absolute paths of the machine that ran
it. a08's catch (2026-09-25): 3 of the 59 sealed rows were `__pycache__/*.pyc` and each
contained `C:\Users\foste\Documents\projects\local_sovereign_agent\seed\engines\cooker.py`
inside the stranger-facing `watch/inbox/seed-3.3.0.zip`. The 3.2.0 pack was hand-surgered
(pyc deleted, manifest rows edited, receipt: SEED_PUBLIC_PACK_20260925.md) but the
builder was never fixed, so the leak returned in 3.3.0. The exclusion lives in the
builder, or it does not live.

**Falsifier:** list the rebuilt zip and manifest: zero pyc rows anywhere; rows drop
59 to 56; `seed/verify_seal.py` exits 0 on the rebuilt tree.

**SPEC: PRE-ZIP COLD-BOOT GATE** (2026-09-25, gala afterparty t28 refire, wired per this section)

The builder (`tools/seed_v2.py`) must run `tools/cold_boot_test.py::gate()` between the
seal and zip emission: after `MANIFEST.sha256` is written (the suite's step0 checks
verify it), before the first byte of the zip. The gate copies `seed/` to a temp dir and
runs the full 14-check cold-boot suite there, so no Python process ever runs inside the
seed tree (t7's own rule stands). Gate passes only when zero checks end CRASH, ERROR, or
TIMEOUT; a READABLE-FAIL passes by design (the suite's contract: exit 0, or a readable
nonzero message, never a traceback, never a missing module). On block, the builder exits
nonzero naming the blockers and emits no zip. `cold_boot_test.py` standalone now exits
0/1 on the same verdict. Cause on file: Desktop shipped the stale 3-pyc seed-3.3.0 zip
while the inbox held the rebuilt bytes, because nothing between build and zip ever ran
the cold boot (t28 sha256 diff, LANES t28.check.txt).
