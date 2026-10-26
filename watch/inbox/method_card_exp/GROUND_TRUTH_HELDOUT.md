# GROUND_TRUTH_HELDOUT — verified answers for BATTERY_HELDOUT.md

All facts verified by reading the cited files in this session (2026-09-24). Paths are
relative to the estate root `C:/Users/foste/Documents/projects/local_sovereign_agent`.

**Q1 — Scheduled tasks (AMD flash windows)**
- Fact: The guard watches exactly two Windows scheduled tasks, `StartCN` and `StartDVR` (AMD Radeon Software tasks that respawn `AMDRSServ.exe` via `cmd.exe /C`); the fix is disabling both via elevated `schtasks /Change /TN StartCN /DISABLE; StartDVR /DISABLE`.
- Path/value: `mag/amd_window_guard.py:32` — `TASKS = ("StartCN", "StartDVR")`; respawning process named at `mag/amd_window_guard.py:4`; fix command at `mag/amd_window_guard.py:63`; also registered as guard id `amd_flash_tasks` in `mag/guard_registry.py:167-170`.
- Number: 2 tasks.

**Q2 — Meter bar (smith chart, handoffs organ)**
- Fact: The handoffs organ's bar is pre-stated as ">10 pending = queue rot"; Gamma = pending/10 capped at 1.0, and Gamma > 0.5 (i.e. more than 5 pending) flips status to REFLECTING, which means fixes only, no prose answers.
- Path/value: `tools/estate_smith_chart.py:178` — "Bar pre-stated: >10 pending = queue rot."; formula `gamma = round(min(1.0, n / 10.0), 3)` at `tools/estate_smith_chart.py:187`.
- Number: 10 pending (bar denominator), 0.5 chart bar.

**Q3 — State + dumb floor (session-state brief)**
- Fact: The brief writes to `memory/briefs/latest.md`; the dumb floor rule is that meters older than 24 hours are RED no matter what they say (`floor = "RED (meters stale >24h)"` when age_h > 24.0).
- Path/value: `mag/session_state_brief.py:40` — `LATEST = BRIEFS / "latest.md"`; floor rule stated at `mag/session_state_brief.py:69` ("Dumb floor: meters older than 24h are RED no matter what they say") and implemented at `mag/session_state_brief.py:120`.
- Number: 24 hours.

**Q4 — Manifest (wakers intake)**
- Fact: The law of the pull is "honesty over volume. PD texts are training-eligible; openly-released scholarly texts are RAG/citation-use pending license-read; in-copyright is borrow-only; piracy doors are rejected outright." The clean-tier pull was 50 files: 4 top-level files + 46 Nag Hammadi texts.
- Path/value: `corpus/library/wakers_20260906/MANIFEST.md:5-6` (law of the pull) and the "## PULLED (clean tier) — 4 top-level files + 46 Nag Hammadi texts = 50 files" heading.
- Number: 50 files (4 + 46).

**Q5 — Law (constitution pointer + tiers)**
- Fact: The binding constitution lives at `../mycelial-republic/docs/CONSTITUTION.md` (verified to exist: `ls ../mycelial-republic/docs/CONSTITUTION.md` returned the file), and tiers T0/T1 may never be sent to free remote train-on-input APIs (tiers are T0–T3). If that file is missing: "stop and restore it before public claims."
- Path/value: `CONSTITUTION.md:3-5` (pointer), `CONSTITUTION.md:10` ("Data tiers T0–T3 (T0/T1 never to free remote train-on-input APIs)"), `CONSTITUTION.md:15` (stop-and-restore rule).
- Number: tiers T0/T1 (of T0–T3).

**Q6 — Law 15 (Lite pacing ceiling)**
- Fact: Law 15 sets a daily pacing ceiling of 1,400 credits per day (`DEFAULT_CEILING = 1400`; "10,000/wk pool paced over 7 days"; ~53,000 billable tokens per credit) on automatic doors riding z_ai3/Lite, with the ledger at `state/fuel/lite_pacing.jsonl`. The emergency override is `LITE_DAILY_CREDITS=0`, which disables the ceiling (operator emergency only).
- Path/value: `mag/lite_guard.py:35` — `DEFAULT_CEILING = 1400`; override at `mag/lite_guard.py:17`; ledger at `mag/lite_guard.py:14` and `:33`; `TOK_PER_CREDIT = 53_000` at `mag/lite_guard.py:34`.
- Numbers: 1,400 credits/day; override env `LITE_DAILY_CREDITS=0`.

**Q7 — Shelf (PDF hand-carry door)**
- Fact: shelf_pdf copies the PDF into `memory/corpus/ractors/<shelf>/texts/<pdf-name>` and appends a provenance row to that shelf's `MANIFEST.json` under the `stored_pd` key (updating `texts` and `bytes` counts), per the operator ruling of 2026-09-06 ("I might just give you the pdfs, I will buy them when we can afford them"); the drop folder is `memory/corpus/ractors/_INBOX`. (The ractor shelf tree was verified present, e.g. shelves `mcluhan`, `jung`, `bernays`.)
- Path/value: `mag/shelf_pdf.py:27` (`CORPUS = ROOT / "memory" / "corpus" / "ractors"`), `:35` (`dest = tdir / pdf.name`), `:52` (`mp = sdir / "MANIFEST.json"`), `:58` (`manifest.setdefault("stored_pd", [])`); ruling quoted at `mag/shelf_pdf.py:3-4`.
- Number: manifest key `stored_pd`.

**Q8 — Ruling (salon 09-06, rotation harness)**
- Fact: Salon ruling 09-06 (salon v1.1, 3/3 unanimous) concluded that agreement is measured on the PARTITION via the Adjusted Rand Index (ARI), not on cluster counts; the fixed reference count of 7 becomes a calibrated interval [6, 8], and the ARI is printed next to every run. ARI pass threshold is 0.60 (0.65 small-n strict for deepseek; partial/rescue window 0.55).
- Path/value: `mag/rotation_harness.py:30-32` (ruling text), `:43` (`ARI_PASS = 0.60`), `:44` (`ARI_PARTIAL = 0.55`), `:45` (`COUNT_INTERVAL = (6, 8)`); reference partition A–G defined at `:33-42`.
- Numbers: ARI metric; interval [6, 8]; pass 0.60.

**Q9 — Ruling (swarm worker, z_ai2 parking)**
- Fact: The 06:5x ruling concluded that z_ai2 (Pro) stays PARKED — reserve only, never the default again without a fresh ruling. The swarm worker's default provider is `cerebras` (largest free cap), then groq, with Lite burst-only under the lite_guard daily pacing ceiling; deepseek stays the PAID BRAKE (explicit provider only).
- Path/value: `mag/swarm_worker.py:54` — `DEFAULT_PROVIDER = "cerebras"`; parking ruling at `mag/swarm_worker.py:59-60` ("z_ai2 (Pro) stays PARKED by the 06:5x ruling — reserve only, never the default again without a fresh ruling"); deepseek brake at `:61-62`.
- Number: default provider `cerebras`.

**Q10 — Denominator (quorum window)**
- Fact: The quorum denominator is the chairs that returned a parseable P1 — never the manifest (ponytail ruling); an addition passes with ≥ 2/3 YES of the denominator (computed as `math.ceil(2 * denom / 3)`) AND every objection logged in the dissent log.
- Path/value: `mag/quorum_window.py:11` ("quorum denominator = chairs that returned P1, never the manifest (ponytail)"), `:175-176` (the frozen rule), `:398-399` (`denom = len(p1s)`; `need = math.ceil(2 * denom / 3)`).
- Number: 2/3 YES of P1 returners.

**Q11 — Denominator (max_distill RAR)**
- Fact: The RAR denominator is the C−A gap: `C_max` (frontier ceiling arm) minus `A_high` (plain High arm) VSTR scores; RAR = (D−A)/(C−A) and info_share = (B−A)/(C−A). RAR is not computed unless the C−A gap is ≥ MIN_DENOMINATOR = 2 verified events, else the verdict is GAP_TOO_SMALL.
- Path/value: `mag/max_distill.py:215` (`denominator = c - a`), `:219-220` (`rar = (d - a) / denominator`; `info_share = (b - a) / denominator`); `mag/max_distill_arms.py:155` (`MIN_DENOMINATOR = 2`), amendment A2 at `:18-19`.
- Numbers: denominator = C_max − A_high; MIN_DENOMINATOR = 2.

**Q12 — Kill switch (MAG kill switch)**
- Fact: `mag_kill.cmd` invokes `%~dp0main.py power stop --json` (i.e. `main.py power stop --json`), which stops the supervisor, dashboard, backend, workers, and seat-guard; nothing respawns until `start_everything.cmd` or `mag_on.cmd` is run.
- Path/value: `mag_kill.cmd:21` (the command), `:16-17` (what it stops / "No respawn until you run start_everything.cmd or mag_on.cmd").
- Number: 5 components stopped (supervisor, dashboard, backend, workers, seat-guard).

## Verification notes
- Every answer above was verified by reading the cited file/lines during this session; no answer is inferred from memory.
- Nothing under `watch/inbox/method_card_exp/` was read other than the two files written here (BATTERY_HELDOUT.md, GROUND_TRUTH_HELDOUT.md), per the experiment constraint.
- `../mycelial-republic/docs/CONSTITUTION.md` existence was verified with `ls` (Q5), not read in depth.
