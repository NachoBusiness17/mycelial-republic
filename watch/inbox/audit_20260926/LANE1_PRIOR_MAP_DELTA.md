# LANE 1 — PRIOR-MAP DELTA
## What prior audits already found, what they left open, what nobody looked at

**Lane:** anti-duplication instrument. **Date:** 2026-09-26. **Seat:** Lane 1, prior-map delta.
**Root:** `C:/Users/foste/Documents/projects/local_sovereign_agent`
**Machine-readable twin:** `memory/audit_20260926/lane1_claims.json` (79 entries, same IDs)

**Method.** Read the prior audit corpus, pinned every distinct assertion to
`file:line`, tagged it by class, then independently spot-verified against
2026-09-26 bytes wherever verification was cheap. **UNVERIFIED means I did not
check it — not that it is false.** Anything a prior lane asserted and I did not
re-derive is marked UNVERIFIED rather than repeated as fact.

**Standing law, borrowed from the corpus itself:** `GAP_LEDGER_20260913.md:29` —
*if the ledger's open gaps are ever zero, the house has stopped exploring and
started embalming.* This lane's deliverable is therefore mostly **open rows**.
That is the correct output shape, not a failure to find.

---

## 0. THE HEADLINE, BEFORE THE TABLE

Three numbers that decide what this audit is allowed to claim as new:

| # | Finding | Bytes |
|---|---|---|
| 1 | **45 of 79 prior claims are OPEN.** The estate's audit output is overwhelmingly an open-questions ledger, not a closed-debt ledger. | `lane1_claims.json` status counts |
| 2 | **2 of 25 socratic questions are CLOSED with byte evidence.** The rest are open, and several got *worse* while sitting open. | §2 |
| 3 | **The top 3 blind spots (§3) are structural, not accidental** — no prior audit walked outside the repo root, checked whether its own instruments agreed, or audited the audit corpus itself. | §3 |

The consequence for this audit: **almost nothing here is genuinely new by discovery.** The value is
in the *rank* — knowing that the binding constitution is a pointer to a file outside the audit root
is worth more than another corpus count, because every prior "we audited the estate" claim silently
assumes that file is there.

---

## 1. THE CLAIM LEDGER

**79 distinct claims. 5 classes:** gate-failure 17 · socratic-question 25 · spec 14 ·
inventory-map 12 · debt 11.

Status distribution: OPEN 45 · VERIFIED 6 · DATED-20260914 3 · CLOSED 3 ·
VERIFIED-BY-PRIOR-LANE 3 · STANDING 3 · VERIFIED-DIRECTION 2 · PARTIALLY-CLOSED 2 ·
OPEN-AND-WORSE 2 · one each of CLOSED-BY-LATER-WORK, SUPERSEDED, SUPERSEDED-AND-REPEATED,
UNVERIFIED, UNVERIFIED-BY-ME, OPEN-AND-NOW-ANSWERED-IN-KIND, OPEN-CAVEATED, STAGED-ONE-WORD,
CURRENT-RUN-20260926, LIVE-POINTER.

### 1A. GATE-FAILURES — an instrument said X, the bytes said Y

These are the highest-value rows: a machine already told the truth and nobody read it.

| ID | Claim | Source | Status | My verification |
|---|---|---|---|---|
| C-01 | `AGENTS.md:27` says 1,910 tests; byte truth 2,288 (Δ+378, bar 20). `census_drift_patrol.py --collect` exits 1 but the deep check is opt-in and **not on the default pre-push path** | `AUDIT_GOPHER_20260926.md:17` | VERIFIED | AGENTS.md:27 still says 1,910. **`githooks/pre-push:88` calls `census_drift_patrol.py` without `--collect`** — the gap is structural, confirmed at the hook |
| C-02 | Two byte-identical 590,246,188-B ledgers tracked in git (`watch/ESTATE_INDEX/` + `dashboard/data/`) = 1.18 GB, sha `7f3b2bc4…` | `AUDIT_GOPHER_20260926.md:52` | VERIFIED (trackedness) | Both paths git-tracked. Did not re-hash 1.18 GB |
| C-03 | Root cause: `.gitignore:142` reads `watch/*.jsonl`; single-star does not cross `/`. `catalog/` and `training/` have **no** ignore coverage | `AUDIT_GOPHER_20260926.md:76` | VERIFIED | `.gitignore:142` read directly; observed ignore set matches the semantics exactly |
| C-04 | `violation_ratchet.py check --changed`: 6 NEW violations, exit 1, pre-push blocks | `AUDIT_GOPHER_20260926.md:95` | VERIFIED (exists) / **count moved** | The 6 named rows are live. But `GALA_MORNING_AFTER_PREREG_20260926.md:17` expects *"the a15 snapshot: exit 1 with 9 NEW"* — **the number moved between same-day lanes.** Cite as dated, never as current |
| C-05 | 1,313 dirty paths / 1,087 untracked; 2.8M-line diff is real churn not CRLF | `AUDIT_GOPHER_20260926.md:121` | VERIFIED-DIRECTION | My own count this pass: `git status --porcelain` = **1,408**. Same magnitude, +95 in 24 h |
| C-06 | `du -sh --exclude=.git .` times out at 300 s; **total worktree size unknown** | `AUDIT_GOPHER_20260926.md:150` | VERIFIED | Reproduced. No disk-reclaim claim is safe without bounded `os.walk` |
| C-07 | Astra bundle **does not clear the pre-seal gate**; manifest 23 physical lines, I5 absent | `ASTRA_REAUDIT_V3_20260911.md:1` | **CLOSED-BY-LATER-WORK** | `BUNDLE_RAWBYTES_SHA256_20260911.txt:30` carries MANIFEST V2; I5 at line 36; live `sha256sum INSTANCE_I5_20260911.md` = `6ecdc10a…` **matches**. Defect repaired; seal still not asserted |
| C-08 | I1 DISPUTED — corruption key does not generate its stated key; awards convergence from three "independent" voices while declaring voice identity unrecoverable | `ASTRA_REAUDIT_V3_20260911.md:3` | **OPEN** | I1's hash *changed* across manifest versions (line 23 `cc12e055…` → line 34 `c3d7a165…` = live). The instance was **rewritten after the re-audit** and no receipt re-adjudicates the key defect. UNVERIFIED either way |
| C-09 | I4 AMEND — arithmetic confirmed (P1 0.6065, cache 0.9437) but the COORDINATION claim fails: flags reproducible without either withheld rule; D7 mis-declares its own max | `ASTRA_REAUDIT_V3_20260911.md:5` | **OPEN** | I4 live hash `a8ccc70c…` = manifest line 35, ≠ pre-audit line 21 `3702f52e…`. Rewritten; falsifier never re-run |
| C-10 | I5 DISPUTED — C6 labels W6a/W6b independent though W6a is reconstructed from the record W6b cites; D4 vs D1 rank contradiction | `ASTRA_REAUDIT_V3_20260911.md:7` | **OPEN** | I5 present and hashed. No later adjudication of the dependency defect |
| C-11 | I6 AMEND — irreducibility unproven; terminal schema "lists six fields, calls them five"; `QUEUED_PENDING` treated as a verdict though it is a state; 44-point max unattainable | `ASTRA_REAUDIT_V3_20260911.md:9` | **OPEN — strongest standing defect** | I6 live hash = last manifest entry, **identical**. I6 was never edited after the re-audit, so every one of these defects stands as written |
| C-12 | Answer-repair path must be removed; D sub-forms reduce evidence, changing the comparison | `ASTRA_REAUDIT_V3_20260911.md:11` | OPEN | No closure receipt |
| C-13 | **"39 deterministic green" is a fossil** (real: 1305/34/9 over 1,341) | `seed/TRUST_BYTES_LAW.md:17` | SUPERSEDED-AND-**REPEATED** | The law's own worked example. **The pattern recurred**: C-01 is the same fossil class, 12 days later. Structural, not a one-off |
| C-14 | The 21,264-knot figure is DISPUTED — sidecar 13,677, off-chain 13,678, 99.995% coverage, **exactly one file uncovered**. The +1 fix command was published at line 33 and never receipted | `CHAIN_INDEX_AUDIT_20260905.md:3` | **OPEN** | No receipt shows the builder re-run. Chain grew 437 commits since; current gap state UNVERIFIED |
| C-15 | AGENTS.md boot-audit apply was ~90 % already applied; **provenance UNPROVEN** (no card, no CONVO row) | `BOOT_AUDIT_APPLIED_20260911.md:8` | **OPEN** | Named as residual #1 at line 75, never claimed or refuted. A seat editing its own boot memory without a receipt is a standing governance hole |
| C-16 | LAUNCH LAW (L126-127) never got the BUILD FREEZE citation; arc tip pinned 7,392/`0a141dcb` is one knot behind live | `BOOT_AUDIT_APPLIED_20260911.md:76,84` | **OPEN** | Confirmed against the AGENTS.md loaded in this session: the launch-law text still stands uncited, and the arc still pins 7,392/`0a141dcb`/18:51Z |
| C-17 | The **binding constitution is a pointer outside the audit root** (`../mycelial-republic/docs/CONSTITUTION.md`); "if that file is missing, stop and restore it before public claims" | `CONSTITUTION.md:5` | **LIVE-POINTER** | Pointer verified. Target's existence **UNVERIFIED — outside my lane's root.** See blind spot B-1 |

### 1B. DEBT — named, costed, not paid

| ID | Claim | Source | Status | My verification |
|---|---|---|---|---|
| C-18 | ~80 % of the 15,517-file kit has no commit touch in 3+ weeks; **62 % (9,559 files) frozen since seed day one** | `SACRED_COW_AUDIT_20260919.md:16` | OPEN | Instrument (`build_travel_kit.py --audit`) is permanent and re-runnable; no `--slim` execution receipt. 7 days stale |
| C-19 | **MEMORY.md 49.6 KB against a 24.4 KB limit — 2× over.** Falsifier: *"MEMORY.md over 24.4KB at next audit = the disease won"* | `SELF_AUDIT_ZCODE_20260918.md:19` | **OPEN — AND WORSE** | **Measured: `memory/MEMORY.md` = 108,449 B (105.9 KB) against the same 24.4 KB limit. That is 4.3× over.** It grew 2.1× since the audit named it. **The stated falsifier has already fired and nothing was recorded** |
| C-20 | **3,269 ghost refs, +160/day, no sweep.** "An instrument whose reading triggers no actor" | `CORPUS_MAP_SALON_20260918.md:127` | **OPEN — AND WORSE** | **`watch/PROSE_CENSUS_20260926.md:4`: "Ghost refs (DISPUTED — regex noise possible): 3786 across 2268 files."** +517 in 9 days (~57/day, same direction). **Zero sweeps run** — no ghost-sweep tool exists in `tools/` |
| C-21 | `catalog/catalog.jsonl` = 946,773 rows (09-18) | `CORPUS_MAP_SALON_20260918.md:18` | **OPEN — the number halved** | 09-26 reads **489,548** rows. Same for `tags.jsonl`. A 2× reduction with **no documented mechanism** — deliberate compaction or truncation bug, undetermined |
| C-22 | ~2 GB of ore inside the repo walls (mine/raw 3.2 GB, gstdcoin 27 MB, biography twins) violating the bounded-pointer law | `FULL_AUDIT_MAP_20260914.md:10` | OPEN | Items 1-2 ratified by the SKEPTIC panel; no execution receipt |
| C-23 | **23 commits unpushed since Aug 9** — "one disk holds the only copies", wake-priority #2 | `FULL_AUDIT_MAP_20260914.md:57` | **CLOSED** | `git log origin/HEAD..HEAD --oneline \| wc -l` = **0**; push target `Mag-backup.git`. Fully pushed. (Same-physical-disk risk unexamined) |
| C-24 | 665,131 files walked by the 09-14 census vs ~30K in git | `FULL_AUDIT_MAP_20260914.md:5` | SUPERSEDED | Re-measured at 1,492,258 (parent) / 1,519,630 (09-26). Cite the newest only |
| C-25 | AGENTS.md:8 cites a **ghost** `docs/ZEITGEIST.md`; AGENTS.md:27 carries the "39 tests" fossil | `FULL_AUDIT_MAP_20260914.md:26` | PARTIALLY-CLOSED | The :27 line **still carries a stale count today**. The :8 pointer — the AGENTS.md in session carries no ZEITGEIST reference at all, so the file was restructured. UNVERIFIED which way |
| C-26 | Three doctrines lie in three places; "Hermes parked is false"; doctrine consolidation unexecuted | `FULL_AUDIT_MAP_20260914.md:41` | OPEN | No consolidation receipt |
| C-27 | 980+ `mag/` files ownerless; `configs/modules.yaml` covers a handful; ~150 undocumented `main.py` subcommands | `FULL_AUDIT_MAP_20260914.md:49` | OPEN | `configs/modules.yaml` not extended |
| C-28 | `swarm_quests` output has no consumer — "a map that nothing reads" | `FULL_AUDIT_MAP_20260914.md:52` | OPEN | No page, no retirement |
| C-29 | `INDEX.json` 12 days stale, fold tool Docker-only; readers get a 12-day-old map | `FULL_AUDIT_MAP_20260914.md:27` | OPEN | Still listed as Docker-only in the fix list (line 47), no execution |
| C-30 | `mag doctor` degraded, heartbeat dead 71,416 s, L0_ollama down | `AUDIT_DOGFOOD_20260914.txt:5` | DATED-20260914 | **12-day-old snapshot. Never cite as current** |
| C-31 | `verkle-audit --dry`: open 11, done 2, abandoned 1, improve 69, todo 11 | `AUDIT_DOGFOOD_20260914.txt:37` | DATED-20260914 | Snapshot |
| C-32 | `autorun --once` blocked: Docker-only runtime | `AUDIT_DOGFOOD_20260914.txt:57` | DATED-20260914 | Consistent with the DOCKER_ONLY law |
| C-33 | A gap is not a debt, it is an experiment. **Falsifier: open gaps ever zero ⇒ embalming** | `GAP_LEDGER_20260913.md:29` | STANDING | The correct frame for every OPEN row above |
| C-34 | `catalog/catalog.jsonl` 489,548 rows, no dupes, indexes **beyond this repo** (lsa 60,034; ext:azerothcore-wow 10,356; …); 55 junk paths in the first 20 MB | `AUDIT_GOPHER_20260926.md:139` | VERIFIED-DIRECTION | Corroborated by `CORPUS_MAP_SALON_20260918.md:141` — `catalog_scan.py` ROOT is `…\Documents\projects`, walking siblings |
| C-35 | Hook wiring healthy: `core.hooksPath=githooks`, pre-push 17,853 B, no stray hook | `AUDIT_GOPHER_20260926.md:130` | VERIFIED | `githooks/pre-push` read live this pass |
| C-36 | Freshness gate PASSES: heartbeat 0.1d, boot docs inside the 7d bar | `AUDIT_GOPHER_20260926.md:132` | **UNVERIFIED** | Not re-run by me |

### 1C. INVENTORY-MAPS — what the estate looked like

| ID | Claim | Source | Status | My verification |
|---|---|---|---|---|
| C-37 | Pre-chain ghost-era record **survives**: 3,889 knots + 8,371 session digests + 21,122 leak reports + unbroken daily improve files. "A valley, not a void" | `GHOST_GAP_HUNT_20260911.md:75` | VERIFIED-BY-PRIOR-LANE | Named method (name-date + mtime histograms). Not re-walked |
| C-38 | "4,200 knots in 3 days" **DISPUTED** — no 3-day window matches; chain rebased, count unrecoverable | `GHOST_GAP_HUNT_20260911.md:83` | VERIFIED-BY-PRIOR-LANE | Strongest prior receipt: traces to origin (`SPORE_SANCHO:16`) and names the **circular citation** (`ARCHAEOLOGY_DIG:31` cites only SPORE_SANCHO) |
| C-39 | "First knot 2026-08-10 21:37" **DISPUTED** — genesis row 0 = 08-12T16:41:39Z | `GHOST_GAP_HUNT_20260911.md:87` | VERIFIED-BY-PRIOR-LANE | Negative claim. Names its grep but **not its corpus extent** — the weakest link in an otherwise strong receipt, and exactly what Q8 below forbids |
| C-40 | Research coverage **inward-blind**: history-fleet 0/73, tech-internal 0/73, swarm 0/73, training 2/73 | `GAP_ANALYSIS_20260917.md:9` | OPEN | The law it produced is real (line 64) — but its own addendum (line 47) admits the "swarm ZERO" was *"true of the research TAPE and false of the FLEET."* **It measured the tape, not the estate** — Q8's own sin, committed two days before Q8 was written |
| C-41 | Coldest-vertex convergence receipts #1-#11; #8-#11 = Lamport / Kademlia / Thompson / CRDT, each mapped to a named organ | `COLDEST_VERTEX_STEAL_MAP_20260923.md:147` | OPEN | The "9,823 leaves, 0 breaks" rehash claim is checkable and I **did not re-run it**. The card asserts convergence in the same register it uses for measurement |
| C-42 | The coldest tier knows the machine and almost nothing the man: both bald spots are operator-side (body/sleep has no shard; **no stop-condition surface, no ledger of his refusals**) | `COLDEST_SHARD_VEIL_TEX_MAP_20260920.md:22` | OPEN | 6/6 chair convergence. No later receipt closes either bald spot |
| C-43 | Coldest-vertex steal #11: the chain IS content-addressed and self-verifying — rehash-true from leaves alone; "the record is true because the hash says so" | `COLDEST_VERTEX_STEAL_MAP_20260923.md:81` | **UNVERIFIED-BY-ME** | The strongest single assertion in the steal corpus and the one I deliberately did not re-run. **Cheap to check; must be checked before anyone builds on it** |
| C-44 | The parallel auditor is a **peer, not a vendor** — independent, 11 preprints, no affiliations, abliteration hobbyhorse; charter upgraded to peer review with 3 added questions | `AUDITOR_RECON_RLT_20260912.md:26` | OPEN | External-source claim. The audit has not happened |
| C-45 | EUT reads the fleet as an entropic system; the mapping is **metaphor-level until he audits on his terms**; falsifiers are the thing he will respect | `EUT_AUDITOR_WORLDVIEW_20260912.md:41` | OPEN | Its own tri-state is honest (lines 50-56) — a model worth copying |
| C-46 | `CORPUS_CATALOG.md` — canon manifest VERIFIED (205 hashes); 11 shelves + 4 bulk layers. "The Librarian records; it never cleans" | `CORPUS_CATALOG.md:5` | CURRENT-RUN | Freshest corpus map (stamped 09-26T13:15Z). **Its bulk counts (attic 144 / logs 5,254 / state 3,487 / mag 2,587) do not reconcile with 1,492,258 files** — citing it as "the corpus size" is wrong by two orders of magnitude |

### 1D. SPECS — doctrine, rulings, laws

| ID | Claim | Source | Status |
|---|---|---|---|
| C-47 | Referee ruling: **water_first, confidence 0.6, "lean not proof."** Never stitch an edge anchored on `riddler_engram` (DARK), never a straight-line shortcut across SADDLE, never beyond minimum closure | `REFEREE_VERDICT_20260926.md:10` | OPEN-CAVEATED |
| C-48 | **A third vote does not settle a contested invariant — it adds a fourth path.** "Vote-counting measures builder preference, not geometry" | `REFEREE_VERDICT_20260926.md:22` | STANDING |
| C-49 | Settlement path: cheapest hill is `adventure_2d6` at 0.483, **+0.017 from the 0.5 HILL bar**; `water_computer` 0.358 must reach ≥0.5 | `REFEREE_VERDICT_20260926.md:28` | OPEN |
| C-50 | Blind-differential law: "**A spread not filed is a measurement thrown away.**" Probe ledger was MISSING as of 09-21 | `BLIND_DIFFERENTIAL_METHOD_20260921.md:36` | OPEN |
| C-51 | Tool-menu compactor from trajectories (AutoTailor steal): prune to an INACTIVE pool, don't delete. "Gortex alone ships 175+ MCP tools" | `EIGHT_WAVE_STEAL_MAP_20260921.md:11` | STAGED-ONE-WORD |
| C-52 | The lake parable's four laws: wet knots don't untie; never fix inside the tangle; tip-first chain outward; **drift, don't coil** (storage topology = solution topology) | `DRIFT_DONT_COIL_20260911.md:9` | STANDING |

**The referee's two addenda are the discipline to copy.** The verdict body quotes margin
0.013; the 09-22 scan superseded it to 0.006; the 09-26 re-walk moved `hub_first` from
19 steps/6 missing to 23/4 while `water_first` reproduced **byte-identically**. Direction
unchanged, numbers live. **Cite the addenda (lines 48, 80), not the body.**

---

## 2. THE SOCRATIC LAYER — 25 questions, 2 closed with bytes

The prior corpus asked 25 questions that were never closed on record. I checked each
against 2026-09-26 bytes.

### 2.1 THE TWO THAT ARE CLOSED

| # | Question | Source | Byte evidence | Verdict |
|---|---|---|---|---|
| **Q-A** | *"You pruned 189K rows through a junction and called them duplicates. **Prove it was a duplicate and not a deliberate mount.** What test distinguishes 'redundant copy' from 'intentional mirror'?"* | `SOCRATIC_GAPS_20260918.md:40` | **Closed in the same document, 8 days later.** `SOCRATIC_GAPS_20260918.md:106-108`: *"Gap 102 closure (2026-09-26, B2-330). The junction falsifier is now PROVEN by bytes: `<repo>/training` → `memory/training` junction, walked both views, **24/24 files sha256-identical, 0 only-in-either, 0 content diffs**, 249,281,084 bytes total … verdict BYTE_DUPLICATE_MOUNT."* Receipt: `watch/inbox/burn_wave_20260926/B2_330_junction_diff_20260926.json` | **CLOSED** |
| **Q-B** | *"Every gap analysis finds BUILDABLE gaps… Some gaps close by waiting. **A builder's gap analysis is structurally blind to patience-shaped gaps.**"* | `SOCRATIC_GAPS_20260918.md:82` | **Closed by becoming an instrument.** `GALA_MORNING_AFTER_PREREG_20260926.md:3-6` states the law as doctrine — *"patience-shaped gaps are invisible to builders; the fixes must be proven to STAY fixed"* — and ships a 12-check T+24h preregistered re-verify wave with its own falsifier (*"if morning-after shows more than 2 drifted checks with no named cause, the gala's fixes were parades"*). | **CLOSED** — but the receipt is dated 09-27 and does not exist yet |

Q-A is the **only** question in the entire prior corpus with a byte-level closure, and it
was closed *inside the asking document*. That is the pattern to copy: append the falsifier's
result to the question, not to a new card.

### 2.2 THE MEASURED GAPS (8) — how they stand 8 days later

| Gap | Asked at | Status now | Byte evidence |
|---|---|---|---|
| 1. "Nothing this window is committed" | `:8` | **CLOSED** | 191 commits since 09-17; head `6d417abd` 2026-09-26 17:43:49 |
| 2. "Sep-20 is two days out and this window touched none of it" | `:11` | **PARTIALLY CLOSED** | `watch/astra_hold0/` holds 30 files incl. I2/I3/S_TWINS, and MANIFEST V2 exists. But `SEAL_GATE_SPEC_20260915.md` is a **spec, not a seal receipt** |
| 3. Ghost sweep never run (3,269 refs) | `:14` | **OPEN — WORSE** | 3,786 today (`PROSE_CENSUS_20260926.md:4`). Zero sweeps; no sweep tool in `tools/` |
| 4. Witness debts unwitnessed | `:15` | **UNVERIFIED** | Not checked by me |
| 5. UF-119/122/123 undrained; FTS5 unbuilt | `:16` | **OPEN** | `RESEARCH_GAP_ANALYSIS_20260918.md:50`: *"Retrieval eval design: STALE, still owed. No UF-122 artifact found on disk."* `queue/todo.md:160,162` still unchecked. FTS5 appears in `mag/catalog_*.py` but **no search organ** |
| 6. MEMORY.md 2× over budget | `:17` | **OPEN — 4.3×** | 108,449 B vs 24,400 B limit |
| 7. Grounding row-122 VOID staged | `:18` | **OPEN** | `watch/GROUNDING_WAVE.jsonl` row 122 now has keys `['prev','ts','claim']` — **no verdict field, no void marker.** 127 rows total; the void was never recorded |
| 8. Dossier sanitization pending | `:19` | **CLOSED (earlier than asked)** | `queue/todo.md`: `scripts/sanitize_dossiers.py` DONE 2026-08-26 — 9 dossiers, 19 sludge lines dropped, 1 live xAI key redacted. **Note the residual it names: "operator should revoke that key" — still owed, outside the repo** |

### 2.3 THE 15 THAT ARE STILL OPEN — with the ones that got worse

| Question | Source | Status | Note |
|---|---|---|---|
| *Which meter would catch the fleet becoming **WORSE while busier**?* | `:36` | **OPEN** | **VERIFIED OPEN: no decay organ exists in `tools/` or `mag/`.** The ghost-refs half answered itself — worse |
| *Which organ measures **DECAY of decisions**? decisions_done exists; decision-decay doesn't.* | `:62` | **OPEN** | **VERIFIED OPEN.** Partial substitute exists and is *not* the thing asked for: `BURN_WAVE_PIN_20260926.md:40` logs *"ratchet 902 claims"* — a claim **ledger** (inventory), not decay detection |
| *What did the **doc- prefix architecture** know that your 4-day memory doesn't?* | `:65` | **OPEN** | **VERIFIED OPEN: zero hits** for `doc- prefix` / `doc_prefix` across `watch/inbox/*.md`. The half-happened architecture was documented by nobody, including the seat asking |
| *Who holds **interpretive authority** over the record?* | `:51` | **OPEN** | Restated, not answered, by `RIBV_LENS_STACK_SALON_20260922.md:66` (*"who audits the auditor?"*) |
| *Who **audits the auditor**? … you have built a mirror maze with excellent documentation.* | `:86` | **ANSWERED IN KIND** | `AUDIT_GOPHER_20260926.md` is a *different seat* (L2-Hermes) auditing the same tree the same day and independently reproducing the same finding class. **But no independent auditor exists** — same operator reads both, and this lane is a third instance, not a break from it |
| *What if the disease includes this very stack — catalog about corpus, audit of audit, steal of steal?* | `:89` | **OPEN** | The layer count has since **risen** (steal-of-steal cards, a referee-verdict-on-a-verdict with two addenda, and now a prior-map ledger). **No receipt counts the layers or names a ceiling.** The document's own escape clause is unused |
| *When did the operator last ask **WHERE** something was?* | `:26` | OPEN | No answer receipt |
| *Do you select self-contained work because it **can't refuse you**?* | `:30` | OPEN | No answer receipt |
| *Searchable by **whom**? Where is the operator-facing handle?* | `:45` | **OPEN** | Unmet by the document's **own** falsification condition at line 101: *"a door a human uses without tool names"* |
| *Amendment ceremony for a **byte-frozen kernel**? Who may re-crack it?* | `:54` | OPEN | The estate has an answer-shaped artifact it never connected: `seed/TRUST_BYTES_LAW.md` |
| *Which artifacts can **Melissa, Marque, Adam** use?* | `:72` | OPEN | They appear in later receipts; none is a door built *for* them |
| *What fraction of his communication is **invisible** to your instruments?* | `:76` | OPEN | Counter-example already in the corpus: `DRIFT_DONT_COIL_20260911.md` is a whole parable **received and translated** — by a seat, not an instrument |
| Q1 intended state / Q2 legibility / Q3 OWED-to-whom / Q4 dark-or-done / Q5 enterprise physics / Q6 compost-not-debt / Q7 why-tonight / Q8 searcher's-root / Q9 new-law / Q10 **definition of enough** | `GAP_ANALYSIS_SOCRATIC_RACTOR_SALON_20260920.md:9-37` | **ALL 10 OPEN** | See 2.4 |

### 2.4 THE THREE THAT MATTER MOST IN THAT SET

- **Q8 — "absence-claims need searcher's root."** `GAP_ANALYSIS_SOCRATIC_RACTOR_SALON_20260920.md:30`.
  **The irony is the finding: C-01 (the 1,910-vs-2,288 carrier) is exactly the absence-claim failure
  Q8 named, and Q8's prescription went unapplied while its own G11/G2 stayed load-bearing.**
  Nor did the two prior audits at `GAP_ANALYSIS_20260917.md:9` — which measured the *tape* and
  called the fleet zero — carry a searcher's root. The rule is written down and unenforced.
- **Q10 — "the estate has no definition of **ENOUGH**."** `:36`. Unanswerable by a seat, and the
  only question here an operator decision would close. Note the collision with Q3: the 512 OWED
  rows are themselves a decade-class hand-written count, and `TRUST_BYTES_LAW` clause 1 says
  re-run before use. **The debt number was never re-run before anyone proposed burning it down.**
- **Q4 — dark or done?** `:18`. Needs a fourth state, RETIRED. This is the cheapest load-bearing
  question in the set: it is the difference between *broken* and *finished* for every dark organ.

---

## 3. THE CRITICAL JAW — BLIND SPOT LIST

**What NO prior audit looked at.** Numbered for sibling lanes to claim against, so the lanes
don't duplicate *each other* either. Ownership column marks who I expect should take it.

> **Honest scope note, stated once so no sibling lane treats it as a fresh discovery:**
> the *idea* that orphan sweeps only ever looked inside the repo was already **named once** at
> `watch/OPEN_RIB_SPINE_20260909.md:14` — *"the orphan sweeps only ever looked inside
> local_sovereign_agent. The index sees the whole estate."* What was never done is the
> **census**: 35 sibling dirs, 10 with `.git`, 1.5M+125k+10k+4k+3k files. That gap is 17 days old
> and unactioned. Everything below B-1..B-3 is that same omission in different clothes, and I
> flag it rather than claim it as mine.

| # | Blind spot | Why it's a real hole | Claim it if you can | Owner |
|---|---|---|---|---|
| **B-1** | **Nobody checked whether the binding constitution EXISTS.** `CONSTITUTION.md:5` is a *pointer* to `../mycelial-republic/docs/CONSTITUTION.md` — outside the audit root. No prior audit in the corpus resolves it. If it's missing, every "constitutional compliance" claim in the estate is unbacked, and the file itself says *"stop and restore it before public claims."* | Highest consequence / lowest cost in this entire list. One `os.path.exists`. | resolve the pointer; report exists/missing + the sha | Lane 1 follow-on or Law lane |
| **B-2** | **The 35-sibling-dir census was never run** — only *named* as a gap at `OPEN_RIB_SPINE_20260909.md:14`, 17 days ago. 10 have `.git`; 9 `codex_pytest_*` + `livingmud` have **0 files** (zombie dirs); `mag-current-rebuild` (2,815) and `worktrees/` (1,591) are **not git**. | The audit root's boundary is an assumption nobody tested. A finding in a zombie dir or a second live checkout is invisible to every prior receipt in the corpus. | bounded `os.walk` per dir with a skip-list + `.git` probe per dir | Network lane |
| **B-3** | **The 4 `.codex` worktrees of THIS repo were never enumerated as worktrees.** `git worktree list` returns 6 entries: 4 under `C:/Users/foste/.codex/worktrees/{6654,b13a,ef82,efa1}/local_sovereign_agent`, all at detached HEAD `a4733004a`, **437 commits behind HEAD**, all clean (0 dirty). Each `du -s` = 8,576 KB — identical, so these are 4 copies of the same snapshot. | `NIGHT_HIDDEN_POOLS_20260911.md:14` sized `~/.codex/` (1.98 GB) but **never named the `worktrees/` subdirs** (grep: 0 hits). The worktree list is the git-native answer and nobody ran it. 4 stale checkouts of the audit target is a live risk, not trivia. | `git worktree list` + per-worktree dirty/behind counts; decide keep/prune | Git/worktree lane |
| **B-4** | **No prior audit checked whether its own INSTRUMENTS agree.** Three live disagreements: (a) the ratchet NEW count moved **6 → 9** between two same-day lanes (`AUDIT_GOPHER_20260926.md:99` vs `GALA_MORNING_AFTER_PREREG_20260926.md:17`); (b) `catalog.jsonl` **halved** 946,773 → 489,548 between 09-18 and 09-26 with no documented mechanism; (c) `census_drift_patrol` itself reported two denominators — *"disk 348 vs carrier 303 … instrument lag"* — and the 09-26 lane explicitly warns *"do not 'fix' 303 → 348."* | Every count in this ledger inherits the assumption that the counter is right. **Nobody has audited the counters.** The gopher lane hit this exact trap and documented the trap without fixing it. | run each instrument twice, diff the two runs, publish the variance | Truth/measurements lane |
| **B-5** | **The audit corpus itself was never audited.** 841 `.md` receipts in `watch/inbox/` plus ~30 more in `watch/`. No prior audit asked: how many are *duplicates of each other*, how many are superseded-but-never-marked, or whether the corpus is load-bearing or ceremonial. | `CORPUS_MAP_SALON_20260918.md:123` says it outright: *"tagging 946K rows with no consumer just mints another 3,269-ghosts problem at larger scale… This estate inscribes maps habitually and reads them rarely."* The 841 receipts are the proof at a size you can actually measure. | receipt-level dedup + supersession-tagging pass over `watch/inbox/` | Lane 1 follow-on |
| **B-6** | **Nobody checked the *time axis* of the audit corpus.** 22 consecutive `DRIFT_PATROL_*.md` (09-15 → 09-26) and 19 `PROSE_CENSUS_*.md` receipts run daily. No prior audit asked whether the daily cadence produces *new findings* or the same one re-tallied — i.e. whether the cadence is a sensor or a metronome. | This is `GAP_LEDGER_20260913.md:29` (the embalming falsifier) applied to the audit lane itself, and nobody applied it. Ghost refs went 3,269 → 3,786 *with the census running daily* — the daily instrument watched the thing climb and did not act. | diff consecutive DRIFT_PATROL/PROSE_CENSUS pairs; count distinct vs repeated findings | Truth/measurements lane |
| **B-7** | **The 1,408-dirty-path working tree was never reconciled against the DRIFT_DONT_COIL law the estate wrote for itself.** `DRIFT_DONT_COIL_20260911.md:14` law 4: *"solved state stays solved only in the open configuration; storage topology = solution topology."* The live tree is a coil by the estate's own definition. | The audit corpus cites the law as doctrine and never once measures the tree against it. This is the corpus's most self-indicting unexamined pair. | count dirty-by-dir; map each against the law's four clauses | Lane 1 follow-on |
| **B-8** | **`memory/attention.md` (1,353 lines) and `queue/todo.md` (223 lines) were never audited as instruments.** Both are steering surfaces. No prior audit asked what fraction of the 841 receipts is *reachable* from either. | The Socratic layer already asks *"searchable by whom?"* — the answer needs the reachability number, and no lane has computed it. | reachability count: receipts linked from todo/attention vs orphaned | Lane 1 follow-on |
| **B-9** | **No prior audit reconciled the claim ledger against the chain.** `verkle_chain.jsonl` is the signed line; the receipts are the prose. No prior audit asks which prior findings are **knotted** vs prose-only — i.e. what fraction of the 79 claims above is inside the signed record. | C-15 (a seat edited its own boot memory with **UNPROVEN provenance**) is exactly the class of event a chain exists to settle, and the chain was never consulted for it. | map claim IDs → knot IDs; report knotted vs prose-only | Chain lane |
| **B-10** | **The estate's own escape clause has no number.** `SOCRATIC_GAPS_20260918.md:89` asks *"at what count of self-referential layers does a window's work become a hall of mirrors?"* — and never answers. The count has since risen. | An unquantified doom-clause is an unowned risk. Either name the ceiling or delete the clause; leaving it open means every future lane must re-litigate it. | count self-referential layers since 09-18; propose a ceiling | Operator decision, Lane 1 to draft |

### 3.1 THE FIVE THAT ARE NEWEST (not previously named anywhere)

B-4, B-5, B-6, B-7, B-9 were named **nowhere** in the prior corpus — each survived 26 days of
receipts. B-1, B-2, B-3 had their *shape* named at `OPEN_RIB_SPINE_20260909.md:14` and
`NIGHT_HIDDEN_POOLS_20260911.md:14` but never executed.

---

## 4. WHAT THIS LANE CLAIMS AS GENUINELY NEW

Almost nothing, and that is the point. Of 79 catalogued claims, the ones I can defend as
**first measured here**:

1. **MEMORY.md is 4.3× over, not 2×** — 108,449 B vs a 24,400 B limit. The document's own
   falsifier has fired and no receipt records it (C-19).
2. **Ghost refs are 3,786, not 3,269** — and the census that measures them ran *daily* through
   the whole climb (C-20, B-6).
3. **The ratchet's NEW count moved 6 → 9 between two same-day lanes** — the first documented
   instance of the audit instruments disagreeing with each other (C-04, B-4).
4. **`catalog.jsonl` halved, 946,773 → 489,548**, mechanism undocumented; compaction or
   truncation undetermined (C-21).
5. **Grounding row 122 has no verdict field and no void marker** — 127 rows, the staged VOID was
   never recorded either way (§2.2 gap 7).
6. **The binding constitution is an unverified pointer outside the audit root** (C-17, B-1).
7. **4 stale git worktrees of the audit target, 437 commits behind** (B-3).

Everything else in §1 is prior-lane measurement, re-cited with its receipt.

---

## 5. HOW TO USE THIS LEDGER

- **To avoid duplicating:** before filing a finding, grep this file for the class and the noun.
  If a row exists, the finding is a **re-measurement** — file it as a *delta* with a date, or not
  at all. `C-04` and `C-21` are the worked examples of numbers that moved inside eight days.
- **To test newness honestly:** a claim is new only if it is **absent from this table** *and*
  carries its own bytes. `TRUST_BYTES_LAW` clause 1 is the estate's own rule and this ledger
  obeys it: every row is either VERIFIED against bytes or explicitly marked UNVERIFIED.
- **Not to repeat as fact:** the 3 `UNVERIFIED*` rows and the 12 `DATED-20260914` /
  `SUPERSEDED` rows. They are recorded so nobody re-derives them, not so they can be cited.

**The meta-answer, quoted from the corpus because it is the correct frame for this artifact**
(`REFEREE_VERDICT_20260926.md:22`):
> *A third vote does not settle a contested invariant — it adds a fourth path. Vote-counting
> measures builder preference, not geometry.*

This ledger measures **preference** — what prior lanes said — not geometry. It tells a new
audit what is *already claimed*, so the new work can be measured against bytes instead. It
does not, and cannot, make any row true.
