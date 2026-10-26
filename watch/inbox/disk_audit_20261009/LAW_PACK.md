# LAW PACK - the disk-storm never-again legislation - 2026-10-09

Lane D deliverable of the disk-audit wave: the consolidated spec, ready to become ribs + code. This file IS the spec (repo discipline: spec precedes code), and every law names the organ that carries it - a law without a carrier is prose, not code-as-law (the Lessig frame the operator ordered). Once L1/L2/L5 hold, the runbook phases (giant-junk pass, one-shot retention purge, HF purge - runbook/CLEAN_RUNBOOK.md) become never-again-necessary at this scale; its P0 admin steps become bounded recurring organs. Sources: the wave's own landed outputs under watch/inbox/disk_audit_20261009/ (cited per law).

## Genesis

Operator coinage, quoted verbatim (LESSONS.md L11 - the genesis line):

"this is like adopting our own 5 hour compute window limited that zai uses for their hosts only stolen for our own purposes... the flywheel lattice concept standing wave self steal."

The mapping: the provider's rolling compute window is a governor the HOST runs on tenant exhaust; the retention + budget layer this wave specs is the same organ, evolved on our side, recognized as convergent - then stolen. Differences that matter: theirs is denominated in tokens and opaque to us; ours is tokens-as-disk (LESSONS.md L1), readable in our own ledger (smith deltas), rolling by construction (7d retention = the window's width, the free-space floor = its edge). The wave persists, the medium does not accumulate; the flywheel turns burn -> exhaust -> measure -> delta-vs-budget -> tune. Minted under his orders this window: "clean everything ponytail lessig style after an audit of what happened, what was in that data, what can we learn, how do we avoid it, how do others handle it" (WAVE_PLAN.md), "steal this has to be a solved problem" (external/PRIOR_ART_CARDS.md), "i think we can better organize our shit this is crazy" (ORGANIZATION_SPEC.md), and the optimize order behind ADDENDUM_SQL_INDEX_OF_RECORD.md. Retraction law in force: the "700GB in days" / "1.3TB in 36h" figures are RETRACTED-BY-AUTHOR, estimate class (OPERATOR_CORRECTION_GROWTH_CLAIMS.md); the measured curve in evidence_pack/digest.md is the only growth truth.

## The laws

### L1 - per-call stdout cap, capture AND write side
- LAW: every captured tool-call stdout is middle-truncated at 30000 chars (head+tail kept, clipped marker written into the log) and every written exhaust file is hard-capped at 20MB keeping 5 compressed generations - byte cap and count cap ship together or not at all.
- EVIDENCE: one unbounded capture x one mis-scoped command = 64.16GiB in 8 files (full-disk find dumps, FINDSTR loops) against a 28MB/file average in the 309.12GiB forest - the tail dominates, not the average (evidence_pack/digest.md; internal/ATTRIBUTION.md; LESSONS.md L2).
- PRECEDENT: external/PRIOR_ART_CARDS.md cards 2.1-2.3 (Claude Code 30k middle-truncate, OpenHands 30k with clipped marker, Codex official half-head/half-tail rule - independent convergence), 3.3 (Docker: a count cap without a size cap is a NOOP), 3.4 (local driver: 20m x 5 compressed bounded by default) - top steal 1; card 2.4 names the gap nobody fills: context caps without disk caps.
- ORGAN: the harness capture layer (upstream - needs the harness cap) plus our own tools' subprocess wrappers NOW: one shared capped-capture helper in mag/ adopted by tools/ds_workhorse.py and every new walker; uncapped capture in mag/ + tools/ becomes a violation class in tools/violation_ratchet.py.
- FALSIFIER: any single call leaving a file over the 20MB cap through our wrappers, or a future monster grown inside a sink this law claims to bound.

### L2 - retention contract on the daily smith
- LAW: the smith daily sweeps every exhaust dir under a four-field retention contract {enabled, max_age_days 7, max_count, min_age_days 1} inside a fleet budget (total exec-bytes cap + C: keep-free floor + per-file cap), and alerts on GB/day delta growth.
- EVIDENCE: purge prize 81.22GiB at 7d+ today while the younger buckets (~228GiB) age past 7d within a week - a one-shot purge re-grows; the curve peaked 61.2GiB on 10-04 (evidence_pack/digest.md; runbook/CLEAN_RUNBOOK.md P2: "wire it into the retention law, do not one-shot it").
- PRECEDENT: external/PRIOR_ART_CARDS.md card 1.4 (Gemini CLI four-field knob {enabled, maxAge, maxCount, minRetention} - steal the shape verbatim, our setting is 7d not their 30d), 1.1 (Claude Code sweep semantics: 0 refused, pause-with-warning when retention is undeterminable), 3.2 (journald: total budget + keep-free + per-file + age as independent axes) - top steal 2.
- ORGAN: tools/disk_smith.py inside MagDiskSmithDaily (the existing 08:50 task); deltas in logs/disk_smith.jsonl carry the GB/day alert; min_age protects the live window's files.
- FALSIFIER: the forest regrowing past the fleet budget with no smith alert, or the sweep deleting a file younger than min_age_days.

### L3 - burn orders carry an exhaust budget
- LAW: every burn/workflow ask declares an expected GB/day class; the smith delta adjudicates intended vs actual; an overrun pages memory/attention.md the way the 15GB floor does.
- EVIDENCE: 255.86GiB = 82.8 pct of the forest maps to 30 named burns, and 100 pct of the top-20 writer sessions are unattended dwf actors - autonomy concentrates exhaust (internal/ATTRIBUTION.md; LESSONS.md L3).
- PRECEDENT: external/PRIOR_ART_CARDS.md card 1.3 (Codex issue 34061 checklist - per-session/global quotas + disk-exhaustion warnings: a ready-made requirements doc; we are that issue), 1.6 (OpenHands watchdog: retention must name EVERY artifact class a run produces).
- ORGAN: tools/workflow_gate.py ask-block check (EXHAUST_BUDGET field) + the descent-protocol ask template (memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md) grows the field; adjudication rides the smith delta rows.
- FALSIFIER: a burn whose declared budget never meets an adjudication row, or growth diverging from declared budgets with no alert.

### L4 - freeze sweeps both registries
- LAW: any "shut everything down" order executes as ONE receipted sweep enumerating schtasks + ZCode session crons (CronList) + in-flight workflow runs + docker + ollama; a partial freeze is a noop freeze.
- EVIDENCE: the 10-08 shutdown disabled 3 schtasks but the hourly free-burn kept dispatching 3 x 1M-token agents/hour through the freeze, and the flash dispatcher no-oped every 10 min for 12 days past its own close date - second occurrence of the class (CRON_FREEZE_20261009.md; LESSONS.md L4).
- PRECEDENT: external/PRIOR_ART_CARDS.md card 3.3 (Docker's documented noop tripwire - one control surface set while the other writes on is no control at all).
- ORGAN: tools/longrunner_patrol.py grows the freeze-sweep row with a receipt to watch/inbox; runbook/CLEAN_RUNBOOK.md P4 already gates re-enable on the registry state.
- FALSIFIER: a future freeze order leaving any registry firing - the sweep receipt enumerating every registry must exist within one patrol cycle of the order.

### L5 - lifecycle classes at write time
- LAW: every artifact is classed at write time - junk (delete at wave close; keeper = command line + bounded head sample), re-derivable (TTL 30d or rebuild-on-change; keeper = the build script), unique (no TTL; the artifact is its own keeper); keep the recipe, delete the mass.
- EVIDENCE: nothing load-bearing lived in the forest - durable work landed as receipts in a physically separate tree; junk + re-derivable were ~everything big (internal/ATTRIBUTION.md durable-work check; LESSONS.md L7; ORGANIZATION_SPEC.md layout item 4).
- PRECEDENT: external/PRIOR_ART_CARDS.md card 6.1 (HF: accessed>1y filters + dry-run + prune-unreferenced + pinned allowlist - the recipe-keeping shape; top steal 5), 6.2 (audit-verb + guarded purge-verb convention); estate-internal: ollama rotation with modelfile receipts (internal/TIMELINE_AND_ESTATE_LAW.md).
- ORGAN: lifecycle-class rows on the daily smith (tools/disk_smith.py, MagImproveDaily) + verbs main.py disk-audit / disk-prune --class hf|temp|toollogs --dry-run behind one door (card 6.2 adoption note).
- FALSIFIER: a purge destroying unique-class bytes (the class map is wrong - freeze and re-set it), or a re-derivable artifact whose keeper script cannot rebuild it.

### L6 - layout law (cited, not duplicated)
- LAW: every wave lands in ONE dated workspace dir watch/inbox/<YYYY-MM-DD>-<slug>/ holding a mandatory receipt file (RECEIPT.md / SYNTHESIS.md / DIGEST.md) whose header carries the run id; loose arrival at inbox top level is a bug in the writer, not a style choice; all moves are index-first.
- EVIDENCE: 1654 top-level entries and 1511 loose work files at census; founding incident c13997d8 - 5.95GiB exhaust with no receipt dir, its conclusions unverifiable (ORGANIZATION_SPEC.md census; internal/ATTRIBUTION.md caveat row).
- PRECEDENT: external/PRIOR_ART_CARDS.md card 1.3 (Codex 34061: accounting/report verbs presuppose per-run records - the receipt dir IS the accounting organ).
- ORGAN + SPEC (cite ORGANIZATION_SPEC.md, do not duplicate): sections "The law: canonical layout" items 1-4 (dated dirs, mandatory receipt set, machinery-stays-top, lifecycle classes), "Citation-safety protocol (index-first moves)" (MOVE event + moved-to stub + MOVED-PATH lint class; all three registries - git, INDEX, citation prose - change in ONE commit), "Migration plan" (phase 0 = enforce-new-only, zero moves; mass moves never mid-audit). Teeth: workflow gate RECEIPT_DIR, drift-patrol orphan-receipt row, shared-surface LOOSE-AT-TOP WARN.
- FALSIFIER: a landed burn whose deliverable cannot be joined to its exhaust by run id (another c13997d8), or a moved path ghosting between git, INDEX, and prose.

### L7 - fast-crawl + sqlite index of record
- LAW: new work product carries schema in its filename (<YYYY-MM-DD>_<kind>_<slug>_<8-char-digest>.<ext>); the fold gains a sqlite sink beside INDEX.json (one writer remains the fold); any crawler reads the index first and walks metadata-only - content walks where the index answers are a violation class.
- EVIDENCE: the find-dump disease (64.16GiB of accidental C:\ root walks in 8 files) is the founding incident, and the sqlite-over-catalog shape already runs in production here (the FTS5 organ) (ADDENDUM_SQL_INDEX_OF_RECORD.md; internal/ATTRIBUTION.md junk share).
- PRECEDENT: external/PRIOR_ART_CARDS.md card 1.5 (opencode: storage consolidated into one SQLite DB - the queryable-store steal); estate-internal: knot filenames already embed date_time_author_type_hashfragment (ADDENDUM).
- ORGAN: the shared-surface fold host (mag.shared_surface) grows the sqlite sink (schema: seq, ts, sha256, path, kind, wave, lifecycle_class) beside INDEX.json, which stays the derived JSON view; tools/violation_ratchet.py registers the content-walk-without-index class. Priority AFTER cleanup + retention per the ADDENDUM.
- FALSIFIER: a crawler opening file bodies where the index would answer, or the sqlite sink drifting from INDEX.json (two truths).

### L8 - dot-dir first-class
- LAW: agent seats' cache/exhaust dirs (.zcode class) are permanent first-class smith rows; no inventory, patrol, or audit ever walks non-dot globs again; no human is a tripwire.
- EVIDENCE: the largest estate item (.zcode, 335.3GB) was invisible to the first inventory because it walked non-dot globs, and the only disk-full tripwire was the operator reading an OS screenshot at 26.8GB free (internal/TIMELINE_AND_ESTATE_LAW.md root cause 2; LESSONS.md L5).
- PRECEDENT: external/PRIOR_ART_CARDS.md card 1.1 (Claude Code documents ~/.claude as the first-class data home - monitoring must be consumer-aware: measure what the consumer actually writes).
- ORGAN: tools/disk_smith.py monsters/seats rows (landed with cd118ed70 - already true; the law locks it), enforced by tests/test_disk_smith_dotdirs.py; the dot-dir list is config, not code.
- FALSIFIER: any future disk audit whose instrument misses a dot-dir the seats write to, or the operator learning disk state from an OS screenshot again.

## Enforcement map (which organ grows which tooth)

| Organ | Grows | Laws |
|---|---|---|
| tools/disk_smith.py (MagDiskSmithDaily 08:50) | four-field retention sweep, GB/day delta alert, lifecycle-class rows, permanent dot-dir rows (already landed cd118ed70; lock with test) | L2, L5, L8 |
| tools/longrunner_patrol.py | freeze-sweep row: schtasks + CronList + in-flight dwf runs + docker + ollama, one receipted pass | L4 |
| tools/workflow_gate.py | EXHAUST_BUDGET field in the ask block; RECEIPT_DIR fold check (dated wave dir + receipt file with run id in header) | L3, L6 |
| tools/census_drift_patrol.py | orphan-receipt census row (wave dirs without receipts; loose files absent from INDEX); WARN-only at pre-push, flip-to-enforce is an operator call (B2-215 precedent) | L6 |
| mag.shared_surface validate | LOOSE-AT-TOP WARN; sqlite sink beside INDEX.json, one writer (the fold) | L6, L7 |
| tools/citation_lint.py | MOVED-PATH class: moved-to stub resolves to an existing target = STUB-RESOLVED pass; dead stub keeps the hard FAIL | L6 |
| tools/violation_ratchet.py + configs/violation_baseline.json | new debt classes: uncapped capture (mag/ + tools/), content-walk-without-index; NEW=0 at pre-push | L1, L7 |
| memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md | ask template grows the exhaust_budget field (the protocol's prompt block) | L3 |
| Admin organs (operator; runbook/CLEAN_RUNBOOK.md P0) | fixed pagefile 32-48GB (steal 3, card 5.1), monthly vhdx compact task (steal 4, card 4.1 - same registration pattern as scripts/register_census_patrol_task.ps1), AV exclusions | runbook class |

## Test list (spec precedes code: this pack is the spec; every test lands WITH its law's code; ratchet NEW=0)

- tests/test_capped_capture.py - helper middle-truncates at 30000 chars with clipped marker, enforces 20MB per-file cap + 5 generations, logs spill path + full byte count, never the body (L1).
- tests/test_disk_smith_retention.py - contract refuses 0, deletes only past max_age while min_age protects the live window, max_count hard cap, delta row carries GB/day (L2).
- tests/test_workflow_gate_exhaust_budget.py - ask without exhaust_budget fails the gate; fold without a receipt dir fails RECEIPT_DIR (L3, L6).
- tests/test_freeze_sweep.py - sweep enumerates a schtasks mock AND a cron-registry mock; a registry missing from the sweep output fails the test (L4).
- tests/test_disk_smith_dotdirs.py - smith monsters/seats rows include .zcode-class dot dirs; a non-dot-glob inventory shape fails (L8 lock).
- tests/test_lifecycle_rows.py - junk past TTL flagged, re-derivable past TTL without keeper script flagged, unique never TTL'd (L5).
- tests/test_shared_surface_sql_sink.py - sqlite sink item count equals INDEX.json active items; writes outside the fold writer fail (L7).
- tests/test_citation_lint_moved_path.py - moved-to stub resolves STUB-RESOLVED; dead stub target keeps the hard FAIL (L6).

## Build order (small-first)

1. TOMORROW, no new organs: L8 test lock (the smith already walks dot dirs - only the test is owed) then L2 retention sweep on the existing daily smith task (top steal 2, about a day).
2. THIS WEEK: L4 freeze-sweep row in the patrol; L1 estate side - the shared capped-capture helper + ratchet class + ds_workhorse adoption (the harness capture-layer cap stays flagged upstream; our wrappers and ask-steering land now).
3. NEXT: L3 exhaust_budget (gate + descent ask), L5 lifecycle rows + main.py disk-audit / disk-prune verbs.
4. AFTER cleanup + retention prove out: L6 phase 0 (enforce-new-only, zero moves, immediate) then gate RECEIPT_DIR + lint MOVED-PATH; L7 sqlite index of record LAST (the ADDENDUM sets its priority after retention).
NEEDS THE HARNESS CAP: only L1's capture-layer half - every other law is estate code.

## Rib drafts (paste-ready heads; the first lands for real this wave)

### RIB_STANDING_WAVE_BUDGET (lands now: memory/rib/RIB_STANDING_WAVE_BUDGET_20261009.md)
Minted 2026-10-09, operator coinage (LESSONS.md L11). Tokens are disk: the exhaust curve IS the burn ledger in physical form. No unbounded sink - cap, retention, and budget ship together. Burns declare GB/day; smith deltas adjudicate intended vs actual. Keep the recipe, delete the mass. The wave persists, the medium does not accumulate: 7d retention is the window's width, the free-space floor its edge.

### RIB_ESTATE_LAYOUT (draft head; lands with the L6 code)
Minted 2026-10-09, operator: "i think we can better organize our shit this is crazy" (ORGANIZATION_SPEC.md). Every wave lands in ONE dated dir watch/inbox/<YYYY-MM-DD>-<slug>/ with a mandatory receipt file whose header carries the run id; loose arrival at top level is a bug in the writer; moves are index-first (MOVE event + one-line stub + MOVED-PATH lint; git, INDEX, and prose change in one commit); exhaust is classed junk / re-derivable / unique at write time. Full spec: watch/inbox/disk_audit_20261009/ORGANIZATION_SPEC.md + LAW_PACK.md L6/L7 - nothing duplicated here.

## LANDED

- 2026-10-09 lane B2, L8 test lock landed: tests/test_disk_smith_dotdir_lock.py (this pack's test-list line "test_disk_smith_dotdirs.py", lock filename per lane order) - 7 tests, all green (pytest -q, venv 3.11.15, 1.00s combined with the sibling smith/prune fast set, 21 passed): founding dot seats asserted on AGENT_HOMES constants (.zcode / .ollama / .cache/huggingface), dot seats floor >= 7 rows, no wildcard in any seat/monster path (no glob inventory ever), the founding incident replayed permanently on a synthetic tmp home (glob.glob "*" misses .zcode while os.listdir and rglob see it; non-dot inventory under-reports; smith _size_gb row sees the bytes), zcode_cache flows through delta as a first-class row (335.3 -> 340.0 = +4.7GB), monsters keep pagefile.sys + docker_data.vhdx, zero live disk walks; ADJACENT CURE in tools/disk_smith.py snap(): round(_size_gb(p), 2) crashed the whole sweep with "type NoneType doesn't define __round__ method" when a path exists but stat/walk raises OSError (locked AppData Temp subdir, evidence: tests/test_disk_smith.py::test_snap_shape_live TypeError in the 2026-10-09 combined run) - now _row_gb records a None row instead (locked by test_snap_records_none_row_for_unmeasurable_path), because a smith that dies mid-loop blinds L8's seats; sibling L2 prune code untouched by this lane.
- 2026-10-09 lane B2 close-out number: the cured live walk passes - tests/test_disk_smith.py::test_snap_shape_live 1 passed in 741.79s (0:12:21) post-fix versus the pre-fix TypeError at 57s; the fix lets the smith's full 335GB-seat sweep run to completion instead of dying mid-loop.

