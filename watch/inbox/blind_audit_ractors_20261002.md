# BLIND AUDIT: the estate's ractor runs (2026-10-02)

A complete blind audit of the three ractor runs under watch/inbox/ractor_engine/:
ractor-topic (8 lenses), 2026-10-01-dogfood-gaps (8), 2026-10-02-dogfood-48h (10).
Grading was done WITHOUT knowing which lens/run produced a finding; labels were
rejoined only after all 125 verdicts were locked (blind law: provenance
contaminates grades, proven by the hidden-ask duels).

## Method

- Corpus: 26 lens .md files, 125 findings at F-unit granularity (one claim +
  evidence cites each). Break files read only AFTER grading (calibration).
- Blind: state/blind_build_20261002.py stripped run/lens/file identity, shuffled
  with random.Random(20261002), emitted state/blind_ractor_sheet_20261002.json
  (claims + cites, numbered 1-125). Secret mapping at
  %TEMP%/blind_ractor_map_20261002.json; NEVER in this receipt.
- Instruments (live tree): git log/show/diff/ls-tree, grep/sed, .venv python
  ledger re-sums, schtasks/Get-ScheduledTaskInfo, Get-CimInstance, NTFS
  timestamps, ListSavedWorkflows, live runs of violation_ratchet,
  citation_lint, census_drift_patrol, corpus_fts_rebuild.
- Tree context: commit 56449c53b (09:00 EDT today) executed many 10-02
  findings same-day; most STALEs below name it.
- Per-finding note + cite for all 125 grades:
  state/blind_rejoin_ractor_20261002.py (rejoined verdict dict).

## Verdicts: S = SURVIVES, ST = STALE (was true, tree moved), T = THEATER

ALL: S 74, ST 46, T 5, total 125. Survival on today's tree 74/125 = 59 pct;
truth-at-filing (S+ST) 120/125 = 96 pct. No UNCHECKABLE (every claim was
checkable with local instruments; USN/WMI-class legs were few and secondary).

### Blind grade table (numbered; rejoin tag shown after verdict)

1=S(RT-accuracy1) 2=ST(D48-operations4) 3=T(D48-operations5) 4=S(G01-accuracy2) 5=S(G01-security3)
6=S(D48-lineage1) 7=S(G01-lineage3) 8=S(G01-operations3) 9=S(D48-communication5) 10=ST(G01-operations2)
11=T(D48-economics3) 12=S(RT-moonshot-24) 13=ST(RT-dogfood4) 14=S(D48-accuracy5) 15=S(G01-dogfood4)
16=ST(RT-logic1) 17=S(D48-security5) 18=ST(D48-economics5) 19=S(G01-moonshot-13) 20=S(D48-logic2)
21=ST(G01-moonshot-23) 22=S(D48-moonshot-13) 23=S(RT-moonshot-25) 24=S(G01-economics5) 25=ST(D48-lineage4)
26=S(G01-security1) 27=S(G01-operations5) 28=ST(D48-moonshot-12) 29=S(D48-accuracy1) 30=S(D48-moonshot-23)
31=S(RT-communication3) 32=ST(G01-lineage1) 33=T(RT-accuracy4) 34=ST(D48-security1) 35=S(RT-operations5)
36=ST(RT-communication1) 37=ST(G01-accuracy1) 38=ST(RT-communication4) 39=S(RT-accuracy5) 40=S(G01-security4)
41=ST(D48-operations2) 42=S(D48-moonshot-14) 43=S(D48-moonshot-25) 44=S(RT-moonshot-21) 45=ST(D48-lineage3)
46=ST(D48-dogfood3) 47=ST(D48-moonshot-22) 48=S(RT-operations3) 49=S(RT-logic3) 50=ST(RT-economics3)
51=S(RT-economics1) 52=S(G01-lineage4) 53=T(RT-dogfood3) 54=ST(D48-logic4) 55=S(D48-logic5)
56=S(RT-logic4) 57=S(D48-dogfood5) 58=S(RT-moonshot-12) 59=ST(D48-operations1) 60=ST(D48-communication4)
61=S(D48-logic1) 62=S(D48-security4) 63=S(G01-accuracy5) 64=ST(D48-logic3) 65=S(G01-dogfood2)
66=S(G01-moonshot-14) 67=S(RT-moonshot-22) 68=S(D48-moonshot-24) 69=S(RT-moonshot-11) 70=ST(G01-economics2)
71=S(RT-logic5) 72=S(G01-security2) 73=ST(G01-economics3) 74=ST(G01-moonshot-21) 75=S(RT-moonshot-23)
76=S(G01-security5) 77=ST(D48-moonshot-15) 78=S(G01-accuracy4) 79=S(RT-operations1) 80=S(G01-lineage2)
81=ST(G01-moonshot-12) 82=S(D48-accuracy4) 83=S(D48-security3) 84=S(RT-communication2) 85=S(RT-communication5)
86=S(G01-dogfood1) 87=S(RT-economics2) 88=ST(D48-economics1) 89=S(D48-communication2) 90=S(RT-moonshot-14)
91=ST(RT-accuracy3) 92=ST(RT-dogfood5) 93=ST(D48-communication1) 94=S(G01-moonshot-24) 95=S(RT-dogfood1)
96=S(G01-operations1) 97=S(G01-economics1) 98=ST(RT-operations4) 99=ST(RT-moonshot-13) 100=ST(D48-economics2)
101=S(G01-moonshot-11) 102=S(D48-dogfood2) 103=ST(RT-accuracy2) 104=S(D48-security2) 105=S(D48-lineage2)
106=S(D48-moonshot-11) 107=ST(D48-accuracy3) 108=ST(D48-economics4) 109=ST(D48-accuracy2) 110=S(G01-moonshot-15)
111=ST(RT-operations2) 112=S(G01-accuracy3) 113=ST(G01-moonshot-22) 114=S(D48-communication3) 115=S(RT-dogfood2)
116=S(G01-dogfood3) 117=ST(D48-dogfood4) 118=S(G01-economics4) 119=S(G01-dogfood5) 120=ST(G01-operations4)
121=ST(D48-operations3) 122=ST(D48-moonshot-21) 123=T(RT-economics4) 124=ST(D48-dogfood1) 125=ST(RT-logic2)

### The five THEATER verdicts (evidence did not support the claim at its own moment)

- n33 RT-accuracy4 ("sweeps 53+23 unbanked"): the ledger banked the same two
  counts reworded 47s before the receipt; exact-phrase grep missed it
  (watch/inbox/hermes_burn/TICKET_LEDGER.md:129; rerun 53 passed per break).
- n53 RT-dogfood3 ("no keyfile, mint never tripped"): key + production seal sat
  on disk from 04:07/04:10Z (state/keys/seed_seal_key;
  watch/arc_seeds/arc_seed_sess_f4ad2dcb_20261007_0026.seal, NTFS created
  10-02 00:10 EDT); the lens checked ~/.mag, the wrong directory.
- n123 RT-economics4 ("git grep finds 47.54 nowhere"): false at filing; the
  figure was tracked 90 min earlier (watch/inbox/model_garden/
  DEEPSEEK_API_DOSSIER.md:3, commit 0c9d72a06 00:18 EDT).
- n11 D48-economics3 ("ZERO .seal sidecars anywhere, no receipt names a seal"):
  the production seal and the fillball seed-seal receipt predate the run by 4-7h.
- n3 D48-operations5 ("find *.seal returns only pytest-tmp, zero production
  sidecars"): same seal; three sibling lenses in the SAME run counted it.

### What moved the 46 STALEs (one commit explains most)

56449c53b (09:00 EDT today): citation hook committed (n13/n34/n88/n117),
instance_guard claim choke in tools/hermes_burn.py:268 (n50/n59/n64/n107),
driver bounced + pidfile (n25/n41/n54/n124), census carrier refreshed per
AGENTS.md Tests bullet (n16/n91/n111), CURRENT.md refreshed (n38/n93/n98/n109),
commit-queue law ticketed DF48-CQ (n2/n60/n108), files committed + pushed
(n28/n47/n122), ratchet debt accepted (n45). Earlier same-day: fill-ball closed
the register's rows (n37/n70/n73/n74/n81), ERRATA struck 191.8M
(watch/inbox/48h_synth/ERRATA.md), patrols re-registered direct (n10/n36/n46/n99).

## Rejoined survival tables

| run | S | ST | T | survival | true-at-filing |
|---|---|---|---|---|---|
| ractor-topic (38) | 23 | 12 | 3 | 61 pct | 92 pct |
| 2026-10-01-dogfood-gaps (38) | 28 | 10 | 0 | 74 pct | 100 pct |
| 2026-10-02-dogfood-48h (49) | 23 | 24 | 2 | 47 pct | 96 pct |
| ALL (125) | 74 | 46 | 5 | 59 pct | 96 pct |

| lens | S/total | survival | | lens | S/total | survival |
|---|---|---|---|---|---|---|
| security | 9/10 | 90 pct | | moonshot-2 | 9/14 | 64 pct |
| moonshot-1 | 10/14 | 71 pct | | lineage | 5/8 | 62 pct |
| accuracy | 9/15 | 60 pct | | dogfood | 9/15 | 60 pct |
| communication | 6/10 | 60 pct | | logic | 6/10 | 60 pct |
| operations | 6/15 | 40 pct | | economics | 5/14 | 36 pct |

D48's 47 pct survival is a same-day-fix effect (its own findings executed within
3h by 56449c53b), not a quality drop: its truth-at-filing is 96 pct. G01's 100
pct truth-at-filing rode a target a sibling wave then consumed; its survivors
are mostly critiques of an unchanged document
(watch/inbox/gap_analysis_20261001/GAP_REGISTER.md, mtime 2026-10-01 18:41).

## Calibration: blind pass vs the hostile second pass

Hostile pass is genuinely load-bearing: it caught 3 of my 5 theaters at filing
time (RT-dogfood3 KILLED, RT-accuracy4 KILLED, D48-economics3 corrected) and its
WEAKENEDs (RT-accuracy1 timing, G01-accuracy4, RT-economics3 figures,
D48-economics4, D48-lineage1/F4) all match my STALE/THEATER shape.

Blind pass caught what the hostile pass missed (3 named):
1. D48-operations5: break-operations verdicted findings 1-4 only; F5 never got a
   verdict, and its false "zero production sidecars" contradiction (three
   sibling lenses counted the seal) rode into synthesis unadjudicated.
2. D48-economics3's correction was itself wrong: break-economics:37-44 asserts
   ".seal exclusively under agents/pytest-tmp, zero production seals" - also
   false at the break's own moment (seal NTFS-created 00:10 EDT that morning).
   The hostile pass propagated the truncated-census error it was correcting.
3. RT-economics4's "47.54 nowhere" leg: break-economics CONFIRMED the finding
   without re-running the grep; the tracked dossier refuted it at filing.

Hostile pass caught what my blind pass initially missed (1, corrected): n33
RT-accuracy4. I first graded SURVIVES having verified only that the exact
phrase appears nowhere; the reworded bank at TICKET_LEDGER.md:129 (instrument:
pytest -k "code_swarm or swarm" 53 passed, -k touched-module 23 passed) killed
it. Exact-phrase absence checks are blind to reworded banks. Honest banked.

Coverage census: break files verdicted ~108 of 125 findings; 17 received no
hostile verdict (RT break-communication/operations 3/5 each, break-logic 4/5;
G01 break-accuracy/moonshot-1/operations 4/5 each; D48
break-communication/economics/operations/moonshot-2 4/5 each).

Bias note: lens files are post-steering-round (they embed corrections the
hostile pass forced), so blind SURVIVES grades inherit hostile-pass work; this
audit measures the final artifact, not first-draft quality.

## Three named improvements for the ractor engine

1. RUN-CROSS-CONTRADICTION GATE: before synthesis, intersect sibling lenses'
   claims per artifact (path + predicate). D48-operations5's "zero seals" vs
   D48-dogfood5/security3/moonshot2-3's "one seal" over the identical
   watch/arc_seeds path would have died pre-synthesis, no extra sitting.
2. UNIVERSAL-CLAIM QUANTIFIER LINT: ban "zero/nowhere/never/anywhere" unless
   the cite names the enumeration command AND scope; the hostile pass must
   re-run universal censuses untruncated (find | head produced the moonshot-2
   first-draft error AND the break's own bad correction).
3. REWORD-RECHECK + FULL COVERAGE LAW: absence claims get re-grepped by
   underlying quantity, not exact phrase (53+23 vs "53 passed, 23 passed");
   and every lens finding must receive an explicit break verdict (17 of 125
   unadjudicated this window; the unadjudicated F5 was the theater).

Filed by the blind-audit seat, 2026-10-02. Seed 20261002; sheet: state/blind_ractor_sheet_20261002.json. No em-dash bytes.
