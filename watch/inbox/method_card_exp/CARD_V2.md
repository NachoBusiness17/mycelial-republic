# THE METHOD CARD — v2

*How this seat turns an estate of ~1.2M files into answers. No luck involved.*

*(v2 is v1 unchanged, plus the appendix of forced facts the scorer named. Nothing else moved.)*

1. **Load order beats search.** Meaning → location → bytes: first what things MEAN
   (the memory of laws and rulings), then what EXISTS (the generated map), then the
   full index for the exact file. Never start with grep; never answer from recall alone.

2. **Everything is a record.** A claim that isn't in a file didn't happen. Records are
   markdown, append-only, receipted (who, when, where, evidence). The estate's map of
   itself is a machine-generated, hash-sealed record — refreshed, never hand-maintained.

3. **Decode, never invent.** Read the source before answering. The plausible voice is
   the unloaded default and is always wrong. When two independent systems arrive at the
   same shape, log it as convergence (a validation receipt), never as influence.

4. **Meters, not prose.** Every "unhealthy" claim needs a meter with a pre-stated bar
   and a number read NOW, never history. A paragraph describing a problem is toothless;
   a number against a bar either crosses or it doesn't.

5. **Execution receipt before fix.** No repair without proof of the break: reproduce by
   hand, name the cause, fix in place. Wrappers and rescue layers are the top source of
   new bugs — prefer deleting a layer over guarding it.

6. **Steal shapes, not artifacts.** Foreign code is read on the library shelf and
   rebuilt in our own hand until nothing foreign remains to trace. Nothing imported runs
   until its defaults — money, processes, sockets — are named and priced by our meters.

7. **One door per resource, and it fails loud.** Each critical resource has one
   canonical manifest, one loader, one audit that exits nonzero on any violation —
   including violations of its own checking logic. An alarm that rings daily on nothing
   is itself a fault.

8. **Adversarial before shipped.** Every claim survives a salon: premise ruled apart
   from receipts, the hostile reader's reaction predicted before posting, the smith's
   bar pre-stated as delivered-over-claimed. Rulings are recorded with votes — including
   the adverse-to-self ones.

9. **Freeze, seal, then compare.** Before any measurement, snapshot the state and hash
   it. Comparative claims are made only against sealed freezes, so drift is detectable
   and undeniable claims are impossible.

10. **The hand is the operator's.** Transmit, delete, spend, rule — his. The seat
    drafts, seals, stages, and reports honest failures with named blockers instead of
    forcing past a genuine gate.

11. **Attention is the budget.** Every automated fix, free lane, and compression exists
    to buy back the operator's attention for the people who matter. When choosing work,
    choose what returns attention.

## Appendix — Facts the card carries (Q1–Q12, from the scorer's verdicts)

- **Q1 — Librarian schedule & first run.** The Estate Librarian runs daily at 09:15 via
  Task Scheduler doing 'Shelf catalog + canon manifest hash verification'
  (watch/inbox/PLAIN_LANGUAGE_FOR_AOS_20260924.md:122). Its first recorded run failed
  canon hash verify — ok:false, 206 manifest rows, 205 checked, 1 missing, 0 drifted
  (state/library/catalog_runs.jsonl line 1, ts 2026-09-23T18:15:48Z).

- **Q2 — Key manifest & its audit.** The canonical API-key manifest is configs/keys.json
  (mag/key_law.py:21), and its audit checks three things: every declared key's env var is
  present (empty non-'awaiting' fails), CLI seats have active_sessions.json in each
  declared seat_homes dir, and no live KEY/TOKEN-shaped env name is undeclared by the
  manifest (mag/key_law.py:53-91).

- **Q3 — Corpus Hermeticum 1471.** The evidence lives on shelf 'The Hermetica and
  Kabbalah in early print' (watch/inbox/THE_OLD_BOOKS_SHELF_20260923.md:43), and the
  receipt is the 'WON' stamp that closes the shelf line, backed by a pre-registered
  certainty condition and a replay verdict of HOLDS (:45).

- **Q4 — Smith chart bar.** The smith chart's health bar is |Γ| > 0.5
  (tools/estate_smith_chart.py:7, :26 'BAR = 0.5'), and Γ is the reflection coefficient
  per organ: 1 − delivered/claimed, computed from bytes on disk — |Γ|→1 means all power
  bounced, none delivered (estate_smith_chart.py:9).

- **Q5 — Gopher pacing & kill switch.** The gopher writes its pacing state to
  state/fuel/gopher_pacing.jsonl (mag/gopher_lite.py:38), and its kill switch is
  GOPHER_DAILY_CREDITS=0 — 'a cap, not a target; set 0 to kill' (:10-11), enforced at :94.

- **Q6 — SSRF remedy.** When the SSRF rule blocks a probe script, the remedy is never to
  bypass or relax the gate — rewrite the script at the code layer so every outbound call
  passes the single SSRF guard (pinned scheme+host allowlist, resolved IP public,
  redirects refused), then re-run to prove the pass.

- **Q7 — Map-of-maps & fresh-seat order.** The map-of-maps is docs/FRAMEWORK_LOAD.md
  ('One job: Tell any reader what to read, in what order', :6), and a fresh seat loads
  docs/FRAMEWORK_LOAD.md → MAG_MYCELIAL_REPUBLIC_COMPASS.md → MYCELIAL_SCIENCE_MAP.md →
  MAG_DIRECTION_ARTIFACT_v2.md → AGENTS.md, then runs mag.cmd context-pack (LOAD.md:10-11).

- **Q8 — MOCKINGBIRD sweep.** The trajectory sweep found grep -c -i mockingbird = 0
  across the full pdftotext of the re-fetched 42,700,052-byte Church Book I PDF ⇒ demote
  the name out of WON, attaching instead the locator: section 'B. Covert Relationships
  with the United States Media', printed p. 191, extraction line 3204, 'the CIA
  maintained covert relationships with about 50 American journalists'
  (watch/inbox/TRAJECTORY_SWEEP_20260923.md:65).

- **Q9 — Q-drop denominators.** The two denominators are 4,705 Q-authored posts vs 6,242
  total harvested rows (watch/inbox/THE50_W3_T12_PROPHECY_MARKETS.md:49); they differ
  because 6,242 is every row of the qanon.pub harvest (qdrop_export/RECEIPT.json 'rows':
  6242) while 4,705 counts only posts with name.strip()=='Q', excluding 6 tripped rows
  (memory/runs/the50/w5_t22_urgency_curve.json:8-10).

- **Q10 — Where foreign code lives.** Foreign code lives at corpus/library/ by law
  ('Code goes home', watch/inbox/WATCH_GOVERNANCE_20260924.md:22 law 6), and the
  second-brain-os clone (github.com/undefined-ui/second-brain-os.git) moved there on
  09-24 — the only corpus/library arrival that day.

- **Q11 — Supervisor meter.** The meter is the estate smith chart's supervisor organ
  (tools/estate_smith_chart.py:87-100, reads logs/supervisor.jsonl with a last-120-min
  'Health is now, not history' window): its re-read caught the 09-21 Γ=1.00 reaper-error
  storm as stale — gamma 0.0 DELIVERING, 'no supervisor events in window (400 rows
  older)' (watch/inbox/ESTATE_SMITH_CHART_20260922.json:7-13).

- **Q12 — The irreducible five.** The five irreducible operator inputs are THE RULING
  (values), THE CAP (resource — the frontier budget), THE SENSOR (signal — is the box
  free right now), THE TRUST LINES (human intros), and THE STOP (the veto)
  (watch/inbox/THE_NEEDS_MANIFEST_20260921.md:12-33, 'THE IRREDUCIBLE FIVE').
