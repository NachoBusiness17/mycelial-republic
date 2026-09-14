# INTAKE — jackvial89 thread: "Microduck's sim2real special sauce = servo friction models"

**ONE-LINE VERDICT: CALIBRATE — 12/25. A robotics practitioner attributes a $399 biped's sim2real
success to an extended-friction-models paper; the paper validates torque-fitting accuracy on a
bench, not task transfer, Microduck's own docs name no mechanism, and a prominent sim2real voice
flatly disputes the abstract. Zero robotics build fits any fleet lane; two calibration rows and
one hardware-radar datum fall out for $0.**

Date: 2026-09-04 | Evaluator: intake sub-agent (research-socratic genome, background spawn per Amendment 1)

## ITEM
https://x.com/jackvial89/status/2095550189255774284 (Jack Vial @jackvial89, Sep 3 2026 16:31Z).
Verbatim spine (root + 3 follow-ups fetched via webReader, no 403):
1. Root: "some of the special sauce behind Microduck's impressive sim2real transfer" + image
   (image content NOT viewed — crop).
2. Same account: cites "Extended Friction Models for the Physics Simulation of Servo Actuators —
   Marc Duclusaud, Grégoire Passault, Vincent Padois, Olivier Ly — arxiv.org/pdf/2410.08650".
3. Same account: "there's a lot to learn from Microduck that can be used to improve sim2real
   transfer for manipulation, especially on cheaper arms like the so101".
4. @yacineMTB reply: "The claim that the abstract leads with is totally false".

## CONTEXT CHECK (operator's linkage question)
- Post author IS the robotics Jack Vial: "Building robots and neural nets", Ohio, jackvial.com,
  participant in huggingface/lerobot RL-stack refactoring issue #3076 — an open-source robotics
  practitioner who cites his sources. Consistent with receipts culture; mild positive.
- The claimed linkage to the seveibar/tscircuit card: our filed card (INTAKE_SEVEIBAR_TSCIRCUIT_
  ASTRA_20260904.md) names the top reply as **Michael W. @Michaelskywal**, not jackvial. No
  jackvial reply appears in the card's receipts. Linkage UNPROVEN — no interest adjustment made.
- Scored on content alone, per the standing rule.

## RECEIPTS
- Full thread fetched via webReader: root + 3 follow-ups + yacineMTB reply. No 403.
- MEASURE 1 (ran, $0): paper abstract pulled. Lead sentence: "Accurate physical simulation is
  crucial for the development and validation of control algorithms in robotic systems." The
  paper validates extended friction models on a pendulum test bench + four servo actuators + 2R
  manipulators, beating Coulomb-Viscous on accuracy. It contains NO end-to-end sim2real policy
  or task-transfer experiment; RL appears only as motivation.
- MEASURE 2 (ran, $0): Pollen Robotics "Meet Microduck" page fetched. Microduck = 25 cm, 15-motor,
  $399 open-source biped with a working sim2real pipeline. The page names NO transfer mechanism
  (no domain randomization, no actuator net, no system identification, no friction models);
  technical details explicitly deferred to future posts.
- MEASURE 3 (ran, $0): WebSearch — Microduck identity corroborated (pollen-robotics.com intro,
  "Microduck Sim 2 Real" YouTube, r/robotics thread). No public receipt links Microduck's
  pipeline to Duclusaud et al. Search passes partially rate-limited (1302) — absence is weak.
- Corpus sweep: memory index (full read) + watch/ shelf. "sim2real", "so101", "lerobot",
  "jackvial" — all corpus-absent. Nearest kin: HARDWARE_RADAR_20260901.md (cheap-hardware shelf),
  the claim-without-metric attack class (Fable51 09-03, seveibar 09-04 — this is the third
  instance in ~24h), and RIB doctrine (expensive derivation → dumb body).

## SCORE
F:2 P:2 C:5 W:1 N:2 = 12/25 — CALIBRATE band
- FIT 2: transferable kernels are real but thin — "sim is where derivation is free; the dumb
  body only runs the compiled artifact" is RIB with servos, already owned; the receipts-law
  echo is a re-find. The domain itself (robot manipulation) has no fleet substrate.
- PULL 2: feeds the claim-without-metric calibration ledger (third instance, three domains) and
  one hardware-radar datum (sub-$400 RL-first biped). Touches no live campaign.
- COST 5: $0 fetches, one premium socratic pass, zero build.
- WINDOW 1: no starved lane consumes sim2real robotics; someday-docket at best.
- NOVELTY 2: new domain to corpus, but the load-bearing content is our own law re-found
  (falsifiability, benchmark-must-look-like-the-work) plus a radar datum.

## READ
[SOCRATIC] Assumption attacked: that "special sauce" attribution and "totally false" rebuttal
are two opinions of equal evidential weight. Instrument used: paper abstract + Microduck docs +
identity pulls, all $0. What survives: the dispute is real and live, but NEITHER side currently
holds a receipt — and the paper's own validation scope is narrower than both sides assume.

Steel-man of the central claim (jackvial89's, stated so he'd accept it): *a large share of
cheap-actuator sim2real failure is unmodeled servo friction, and the extended friction models
of Duclusaud et al. are an underused, high-leverage fix — applicable beyond walking, down to
cheap manipulation arms like the SO-101.* Yacine's steel-man: *the abstract's lead claim —
accurate physical simulation is crucial — is false as sim2real practice; transfer in the field
is carried by domain randomization and real-world adaptation, not model fidelity.*

ATTACK (strongest counter-case, two named causes):
1. Attribution failure — the "special sauce" claim has no chain of evidence. The cited paper
   never runs task transfer (bench torque accuracy only); Microduck's announcement names no
   mechanism and defers technical posts; nothing public ties the two. The whole thread is
   inference atop an image we cannot see. (Evidence: arXiv abstract scope vs thread claim;
   pollen-robotics.com page — zero mechanism named.)
2. Both camps argue doctrine, not data — "totally false" is itself unfalsified until a
   head-to-head exists: identified-friction-models vs domain-randomization vs actuator-net on
   the SAME cheap arm, metric = real task success rate. Nobody in the thread runs it. This is
   the claim-without-metric class, third domain in 24h (EDA, CAD, now robotics) — the class is
   load-bearing across disciplines, which is the actual finding.
Mitigation: neither failure touches the practical kernel — for anyone running cheap servos,
friction identification is a plausible cheap win worth benching.

## TRI-STATE
- Microduck = Pollen Robotics' open-source $399 biped with working sim2real pipeline — SUPPORTED
  (pollen-robotics.com + YouTube + r/robotics corroboration).
- Paper 2410.08650 validates extended friction models beating Coulomb-Viscous on actuator
  accuracy — SUPPORTED (abstract; scope = bench + servos + 2R manipulators, no task transfer).
- "Friction models are the special sauce behind Microduck's sim2real transfer" — UNPROVEN
  (no public linkage; attribution rides an unviewed image; Microduck docs name no mechanism).
- "The abstract's lead claim (accurate sim is crucial) is totally false" (yacineMTB) — UNPROVEN
  as stated (a flat practitioner dispute; no benchmark offered either way; admissible only as a
  signal that the sim2real field itself divides on this).
- jackvial89 = robotics/LeRobot practitioner (receipts-culture plausible) — SUPPORTED;
  jackvial89 was the top reply on the seveibar card — UNPROVEN (card receipts name
  @Michaelskywal; jackvial appears nowhere in that card).
- Design-law transfer ("the paper's benchmark doesn't look like the work") — SUPPORTED as
  structural identity with flight-recorder benchmark-must-look-like-the-work law.

## VERDICT
CALIBRATE (12/25) — no wire, no build, no spend. Three rows fall out:
1. Calibration row: claim-without-metric is now 3-for-3 across EDA/CAD/robotics in 24h — the
   class generalizes; cite in the intake rubric as a standing attack (check: does the cited
   artifact validate the thing the claim says, or a narrower proxy?).
2. Radar row: HARDWARE_RADAR_20260901.md gains a datum — sub-$400 open-source RL-first biped
   (Microduck) exists; cheap-arm sim2real (SO-101) is an active community conversation.
3. Doctrine footnote: RIB ("derive expensive in sim, deploy dumb artifact on the body") has an
   independent witness in robotics' whole sim2real discipline.

## ROUTE (no wire)
1. One line appended to HARDWARE_RADAR_20260901.md: Microduck datum (09-03/04).
2. One calibration row to the intake rubric: "proxy-validation" check added to the
   claim-without-metric attack (does the receipt measure the claim or its shadow?).
3. Kill condition WRITTEN for the next seat ($0-ish, executable cold): read the microduck /
   microduck_rl repos (open source) — if transfer ships via domain randomization or an actuator
   network with no friction identification, jackvial89's attribution DIES; if it cites
   Duclusaud et al. or ships identified friction parameters, attribution becomes SUPPORTED and
   this card upgrades to a citation row in any future cheap-robot arc.
4. Yacine-side kill condition: a head-to-head on one SO-101 (identified-friction sim vs
   domain-randomized sim vs actuator net), metric = real-world pick success rate. Nobody has
   run it; whoever runs it owns the dispute. Fleet will not be that someone (no robot body).
5. No engine, no queue, no salon, no spend.

## TWO COUNTERS (L0)
- FORBIDS: filing any future "X's special sauce is paper Y" claim into the corpus on
  attribution alone without checking whether Y validates X's phenomenon; and any robotics
  hardware spend under this card.
- PAID RENT: one radar datum + one generalized attack check (proxy-validation) + a written
  falsifier pair, for $0.

## THE CROP
This pass did not see: the root post's image (the load-bearing artifact of the attribution —
needs a vision seat), the microduck_rl source (the attribution's only decisive receipt — left
as the written kill condition), the rest of the reply section (thread depth beyond yacineMTB's
rebuttal), and any Pollen technical follow-up posts. Next lens: vision chair on the image is
the cheapest upgrade; a hands seat with GitHub access should run ROUTE-3 cold before anyone
repeats this attribution.

Typed room row:
`intake.card{slug:"jackvial_sim2real_friction",verdict:"CALIBRATE",score:12,route:"hardware-radar.row+proxy-validation.check+kill-conditions.owed"}`
