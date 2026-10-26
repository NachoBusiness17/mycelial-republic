# STEAL: steering fold delta (pass 1+2 theory vs fleet practice) 2026-09-26

Lane B2-132. Compares the steering-theory burn pass 1 (BURN_steering-theory_20260925.md)
and pass 2 (BURN_steering-theory_20260925_b.md) findings against the practice
stack: .agents/skills/memlance, .agents/skills/retrocausal-steering,
.agents/skills/mesh-comms, tools/probe20_run.py + watch/inbox/PROBE20_steering_v1.jsonl,
and the burn receipts themselves. Every "practice" claim has a byte on disk;
every "no practice" claim survived grep on 2026-09-26.

## A. Practice that already has theory

1. probe20 runner + seed (tools/probe20_run.py, PROBE20_steering_v1.jsonl,
   sha256 bfce1f28... gate) IS pass 2's build, landed: pair A conf-margin-vs-correctness,
   pair B escalate-rate-vs-overturn-rate, versioned 20-task probe, append-only
   series, noise floor + one-flip escape closed, drift_check verdicts. The
   pass-2 falsifier is executable today minus the live client (see B1).
2. retrocausal-steering + memlance (self-true rule, unprompted-citation
   witness, retire-after-take) already carry the counter-doctrine to pass 1's
   attack-surface finding (Rogue Scalpel: the steering channel itself
   compromises safety; "an unverified pack is an unscanned steering vector").
   Self-true = payload benignness gate; witness = detection; retire = payload
   expiry. The fleet built the defense shape before the literature named the
   weapon class.
3. mesh-comms chatter meter ("removing it changes a file, decision, or
   receipt within one window") is the same family as pass 2's denominator
   law: a rate without events is noise.

## B. Theory with no practice (grep-verified 2026-09-26)

1. White-box hidden-state monitor (pass 1 steal 1): no live client exists.
   ollama documents no logprobs on any endpoint (fetched pass _b);
   tools/probe20_client.py is NOT on disk; zero live cycles on any lane.
   The pass _b llama-server spec is the only bridge.
2. Pack-import steering gate (pass 1 steal 2, G05 family): no gate exists.
   .agents/skills/*.md land as plain files; nothing scans an imported pack
   for steering content; the doctrine is unenforced.
3. Kalman bias model (pass 1 item 3, G38 debt): grep -rli kalman over *.py
   returns nothing. Pure theory debt.
4. Kifu as drift track (pass 1 item 4): tools/cathedral_walk.py kifu is a
   game move record, not a metric series fed to drift_check. Untested claim.
5. memlance hit-rate tally (five lances, >= 2 unprompted hits): zero lances
   fired. grep plant_ts across memory/, watch/inbox/, corpus/ hits only the
   SKILL_FORGE doctrine text, no witness receipt.

## C. Steals filed (the delta, as canon)

1. When the pack-import gate gets built, it inherits the skill law instead of
   inventing rules: required properties = self-true (benign standalone),
   witnessed landing (receipt with both timestamps), retire path. Same gate
   family as G05's emergency-override rule: only the gate declares a payload
   safe.
2. mesh-comms metering adopts the pass-2 denominator law as its concrete
   threshold: a rate claim in a mesh row or receipt with fewer than 10
   events is filed as a count, never a rate.
3. The next owed build on this line is probe20_client.py on llama-server
   (pass _b spec a-d): it is the single seam that turns B1 from theory into
   practice. No new theory needed; build the spec that exists.

## Falsifier for this card

Any A-row whose byte disappears (runner or skill deleted) or any B-row whose
practice lands (probe20_client.py on disk, a pack gate in the repo, a
plant_ts/hit_ts witness receipt, a Kalman bias model in code) retires that
row; re-fold at next steering-theory burn. The card is falsified if any
"no practice" claim was true only of my grep: a counterexample path not
covered above reopens the fold.
