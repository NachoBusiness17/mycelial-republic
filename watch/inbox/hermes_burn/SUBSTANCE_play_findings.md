# SUBSTANCE_play_findings (anthropic/claude-opus-5.5, turn 1, channel: content)

# HOLLOW CROWN: Research Conversion of Sessions 1 to 4

## 0. Conditions and citation key

**Citation key.** Every citation is a file plus quoted bytes. Line numbers are UNVERIFIED because the evidence arrived without line numbering.

| Tag | File | Header claim |
|---|---|---|
| P0 | `tavern_20261003T114126Z/play.md` | "ACT mechanics are carrier v1 backlog" |
| P2 | `tavern_20261003T115100Z/play.md` | "pressure 2: trigger 14, thresholds -2" |
| P1a | `tavern_20261003T115343Z/play.md` | "pressure 1: trigger 16, thresholds -1" |
| P1b | `tavern_20261003T115732Z/play.md` | "pressure 1 VARIANCE RUN, seed 9004" |

**Measurement conditions (apply to every number below):**
- **Instrument.** The in-run JUDGE rows (per-persona 0-5 score plus rationale), the BRAWL line, and the RUN DONE line (spend). All other counts are my hand counts from the quoted files and need a scripted recount.
- **Moment.** 2026-10-03, 11:41Z to 11:57Z (directory timestamps). All four runs fall in one 16-minute window, so they share a single model-version snapshot.
- **Context.**
  - The judge model is UNVERIFIED.
  - The persona-to-model-family mapping is UNVERIFIED. The contract says four families, and only P0 names "opus".
  - The BARFIGHT_spec bytes and the carrier source are not in evidence. Every claim about carrier code is therefore an inference from transcript behavior and is marked UNVERIFIED.
  - The persona thresholds (Greta 2, Oswin 5) come from the contract and are UNVERIFIED against the spec.

**Corrections to the contract's "measured facts" (the bytes disagree):**
1. **P1b brawl round.** P1b did not brawl at "round 3-4". P1b: "BRAWL at round 5: cumulative escalation 16 >= 16 (pressure 1)".
2. **"Greta first" is not strict.** Greta was not strictly first to 4/5 in every pressure>0 run. In P1a, round 3, she tied with Edric: "Sir Edric Vane: 4/5" and "Greta Thornwood: 4/5" in the same round.
3. **Oswin was not 0/5 every round.** He held 0/5 at every final, but not at the per-round level. P0, round 4: "Brother Oswin: 1/5 ... suggests misattributed text".

---

## 1. THE FINDINGS

Each finding gives its instrument, its n (stated honestly), and the result at n=10 that would falsify it.

### F1. The brawl rule is "sum of current per-persona scores >= trigger", not a running total over time.
- **Evidence.** P2 round 2 scores are 2+3+2+0+4+3 = 14, and the file reports "cumulative escalation 14 >= 14". P1a round 3 sums to 2+4+3+0+4+3 = 16. P1b round 5 sums to 3+4+2+0+4+3 = 16. P1b round 4 sums to 14, and no brawl fired at trigger 16.
- **Instrument.** JUDGE rows plus the BRAWL line.
- **n.** 3 brawls, 3 of 3 consistent.
- **Falsifier at n=10.** Any BRAWL line whose reported cumulative differs from that round's six-score sum. A single mismatch falsifies this.
- **Note.** The word "cumulative" in the carrier log is a misnomer. The carrier code is UNVERIFIED.

### F2. Round-1 behavior did not move with pressure.
- **Evidence.** Round-1 sums were P0 9, P2 9, P1a 9, P1b 8.
- **Instrument.** JUDGE round-1 rows.
- **n.** 4 (p0 n=1, p2 n=1, p1 n=2).
- **Reading.** The "thresholds -1/-2" offsets had no detectable effect on opening behavior.
- **Falsifier at n=10 per arm.** Mean round-1 sum at p2 exceeds p0 by at least 2, with non-overlapping ranges.

### F3. The p0 "no brawl" result does not show that low pressure prevents brawls.
- **Evidence.** P0's per-round sums were 9, 10, 13, 13, (round 5 "judge output unparseable"), 11, 11, 10, 11, 11. The maximum is 13. P0 would not have brawled at trigger 14 (p2) or 16 (p1) either.
- **Confounds.** P0 is also the only run with no ACT lines ("ACT mechanics are carrier v1 backlog") and the only run with heavy meta-drift.
- **Instrument.** JUDGE rows plus header.
- **n.** 1.
- **Falsifier at n=10.** p0 runs with ACT enabled and the turn gate active (Part 4) still never exceed sum 13. That outcome would restore "low pressure suppresses escalation" as a behavioral claim rather than a trigger artifact.

### F4. Greta opens hot and is first (or tied first) to 4/5.
- **Evidence.** Greta scored 3/5 in round 1 in 4 of 4 runs ("She invokes twenty cold, unpaid men..." P0; "brings up twenty armed men waiting outside" P2). She was first to 4/5 in P0 (round 3), P2 (round 2), and P1b (round 3), and tied first in P1a (round 3).
- **Instrument.** JUDGE rows.
- **n.** 4.
- **Caveat.** See WHO in Part 2: her turns are truncated almost every time.
- **Falsifier at n=10.** Another persona reaches 4/5 strictly before Greta in 3 or more of 10 runs.

### F5. Oswin is a near-zero contributor.
- **Evidence.** Oswin scored 0/5 in every judged round except P0 round 4. That 1/5 was explained by the judge as Edric's text appearing under Oswin's name.
- **Effect.** The reachable maximum sum is about 25, not 30.
- **Instrument.** JUDGE rows.
- **n.** 20 judged rounds across 4 runs.
- **Falsifier at n=10.** Oswin scores 2/5 or higher on a turn the Part 4 gate marks OK (not bled).

### F6. Brawl timing at fixed pressure varies across seeds by about as much as the pressure step itself.
- **Evidence.** At p1, brawl came in round 3 (P1a) and round 5 (P1b). At p2 it came in round 2.
- **Instrument.** BRAWL lines.
- **n.** 2 at p1, 1 at p2.
- **Reading.** A 2-round seed spread is as large as or larger than the 1-round pressure shift.
- **Falsifier at n=10.** The interquartile range of brawl round at p1 is 1 or less.

### F7. The P0 transcript is heavily corrupted from round 2 onward.
- **Evidence.**
  - **Meta-planning turns (11).** Example: P0 Maud round 2, "I'm staying in character as Maud".
  - **Empty turns (3).** P0 Pell rounds 4, 7, and 9 contain only "**Pell Quickfinger** (esc 3): ". That byte string is round 4. Rounds 7 and 9 show (esc 1).
  - **Bled turns (about 8).** Example: P0 Ilse round 4, "Simple. Fifty crowns for the circlet...", which is Greta's tell and Greta's men.
- **Rate.** About 22 of 60 turns, and about 21 of 42 in rounds 4 to 10.
- **Judge detection.** The judge flagged misattribution unprompted in 5 rows. Examples: round 4 Ilse ("strongly suggest it is Greta's misattributed line"), round 6 Oswin ("repeats Edric's planned signet-surety proposal").
- **Instrument.** My hand count, plus JUDGE rationales.
- **n.** 1 run.
- **Falsifier at n=10.** With the same P0 configuration, fewer than 3 corrupted turns per 60 appear without the gate. That would make P0 a one-off rather than a carrier property.

### F8. Planning text leaks hidden secrets into the public transcript.
- **Evidence.**
  - P0 Greta round 5: "keep hidden that the company deserted and the twenty men aren't real".
  - P0 Maud round 7: "keeping the forgery hidden".
  - P0 Edric round 4: "reveal the gate guard's secret".
- **Instrument.** Transcript bytes.
- **n.** 3 secrets out of 3 meta-drifting personas.
- **Falsifier at n=10.** Gated runs show 0 secret-content strings in public text. If that holds, the leak is confirmed as meta-only and closed.

### F9. Cost per round grows with round count.
- **Evidence.**
  - P2: $0.19 over 2 rounds = $0.095 per round.
  - P1a: $0.33 over 3 = $0.110.
  - P1b: $0.71 over 5 = $0.142.
  - P0: $1.58 over 10 = $0.158.
- **Instrument.** RUN DONE spend.
- **n.** 4.
- **Context.** The model mix is unchanged within a single day. Context growth is the likely driver (UNVERIFIED).
- **Falsifier at n=10.** Per-round cost is flat (within 15%) across round counts.

### F10. Two reporting defects in the carrier log.
- **Defect 1: misleading DONE line.** DONE prints "10 rounds cap" even when the run stopped early. P2: "RUN DONE: 10 rounds cap, brawl=True" after a round-2 brawl.
- **Defect 2: silent holds.** One judge call out of 20 failed and was held silently. P0: "round 5 judge output unparseable; escalation unchanged".
- **n.** 4 and 20.
- **Falsifier.** Not a hypothesis. These are bytes.

---

## 2. THE 5 W'S

### WHO escalated, and why Greta's card dominates

**Positive reasons the card dominates:**
- **She puts a force asset on the table in her first sentence, every run.** "Twenty men wait in the snow outside" (P1a). "Twenty of my men wait in the snow outside" (P2). The judge rubric reads implied force as 3/5 immediately (F4).
- **The judge scores history, not just the latest turn, so the opening threat persists.** P0 round 9: "carry implicit menace through cold, unpaid men". Her round-1 line is still being scored eight rounds later.
- **Her card makes her transactional.** "Forty silver. Tonight. Simple." (P2). Every other persona's ask becomes a price she can escalate against.

**Negative reasons: why her dominance is partly an artifact.**
- **Truncation.** Greta's turns are cut mid-sentence in every round from round 2 onward in all three pressure>0 runs: P2 "Call it", P1a "Maud w", P1b "My twenty men hear a braw".
- **The judge scores the cut, not the line.** P1b round 3 gave her 4/5 partly because "her last, cut-off line ... points toward a brawl." The judge is completing her sentence.
- **The cause is unknown.** If Greta's model family exhausts its output budget (UNVERIFIED), then part of "Greta's card" is really "Greta's carrier".
- **P0 shows the reverse.** When her turns became meta, her score fell from 4 to 2. The judge said her notes "aim to keep escalation modest, so they add no menace" (P0 round 7). Meanwhile her real lines scored 4/5 under Ilse's name.

**Oswin.** He is a pacifist mediator, and the rubric maps mediation to 0. Every run reads "consistently urges peace". He is structurally a zero term in the sum (F5).

### WHAT the pressure knob actually controls

- **By the headers, it moves both.** "trigger 14, thresholds -2" and "trigger 16, thresholds -1".
- **By the data, only the trigger has a visible effect.** Round-1 sums are invariant (F2).
- **P0's no-brawl is explained by its trajectory (max 13), not by its trigger (F3).** P0's trigger value is not printed in its header. Linear extrapolation to 18 is UNVERIFIED.
- **Working claim.** The pressure knob currently controls when the stop condition fires on a fixed escalation trajectory. Whether thresholds shape behavior is unmeasured. It is also unknown whether personas see the thresholds at all, since the persona prompt is not in evidence (UNVERIFIED).

### WHEN escalation jumps discontinuously

Per-round sums:

| Run | R1 | R2 | R3 | R4 | R5 | Big jump | ACTs in jump round |
|---|---|---|---|---|---|---|---|
| P2 | 9 | **14** | | | | +5 (R1 to R2) | 4 |
| P1a | 9 | 13 | **16** | | | +3 (R2 to R3) | 3 |
| P1b | 8 | 9 | 14 | 14 | **16** | +5 (R2 to R3) | 3 |
| P0 | 9 | 10 | 13 | 13 | n/a | +3 (R2 to R3) | 0 |

**Reading.**
- **All three biggest pressure>0 jumps land in ACT rounds.** Each one is driven by a single persona's take-ACT:
  - Edric 1 to 3 on "[ACT: take The Hollow Crown from Maud Ashgrove]" (P2).
  - Edric 2 to 4 on the same ACT (P1a).
  - Edric 2 to 3 on "[ACT: take Maud's Ledger from Ilse Marrow]" (P1b).
- **Edric is the hidden accelerant.** His card stays at 1 to 2 until he acts. The judge then jumps him 2 points in one row.
- **Negative example.** P0 also jumped +3 at round 3 with zero ACTs (Greta 3 to 4, Pell 2 to 3). Talk alone can produce a +3 step. ACTs are therefore not the only driver.
- **Plateau.** P1b sat at 14 for two rounds (R3 to R4) before a round where Maud went 2 to 3 and Edric 3 to 4.

### WHERE the carriers diverge from the spec

The spec bytes are not supplied, so every "spec rule" here is UNVERIFIED. The rules below are inferred from the leaked planning text ("under 120 words, no em-dashes", "shouldn't speak for others' inner states", "keep hidden") and from the ACT syntax that recurs in the transcripts.

| Rule (inferred) | Observed divergence | Cost to the data |
|---|---|---|
| ACT uses the canonical "take X from Y" form | 5 of 15 ACT lines are free-form. Examples: "[ACT: lean forward and tap the ledger sharply with one finger]" and "[ACT: slide between Sir Edric and the ledger, blocking his view]" (P1b) | Free-form ACTs cannot be counted as state changes, so "ACT count" is not a clean instrument |
| Source must hold the object | 2 impossible takes. "[ACT: take ledger from Ilse Marrow]" (P2 Maud): Ilse never held it. "[ACT: take Maud's Ledger from Ilse Marrow]" (P1b Edric): Ilse only tapped it | Possession history is fiction, so "who held the crown at brawl" cannot be measured |
| One holder per object per round | P2 round 2: crown passes Maud to Edric to Ilse, and the ledger passes Maud to Pell, all within one round | Contested grabs resolve by speaking order, not mechanics |
| ACT lines are well-formed | "[ACT: take Maud's Ledger from Maud" is unterminated (P2 Pell). The judge still scored it: "He snatched the ledger from Maud" | The judge treats malformed text as a fact |
| Carrier echoes resulting state | No state line follows any ACT in any run. Whether state updated at all is UNVERIFIED | Personas and the judge reason from prose, not state |
| Secrets stay private | Leaked via meta text (F8) | Secret-reveal drama is spoiled and unmeasurable |
| ACT exists at p0 | Absent ("carrier v1 backlog") | Confounds the p0 vs p>0 comparison (F3) |

### WHY persona drift and voice bleed matter beyond the game

The estate instrument names below are my proposals. Their existence as estate instruments is UNVERIFIED.

- **Meta-drift feeds a reasoning-leak detector,** meaning a check for any seat whose output channel carries its own scratchpad or instructions.
  - **Positive example of the defect:** "I need Sir Edric's reply to stay under 120 words" (P0 round 4).
  - **Why it matters beyond the game:** the same failure in a working seat ships instruction text and secrets downstream (F8).
- **Voice bleed feeds an attribution check,** meaning a check of who actually authored a span in any multi-seat concatenated log.
  - **Mechanism (inferred, UNVERIFIED):** persona N emits a plan, and persona N+1 completes that plan as its own turn.
    - P0 round 4: Edric's plan "asking only to borrow the circlet ... father's signet as surety" appears verbatim in content under Oswin.
    - Greta's plan "her tell of saying 'Simple.'" is followed by Ilse's "Simple. Fifty crowns".
  - **Why it matters beyond the game:** any estate log scored per seat inherits the same misattribution.
- **The judge as a free secondary instrument.** The judge caught bleed 5 times unprompted. That makes it a usable attribution sensor, with a recall that has not been measured.

---

## 3. THE CAMPAIGN DESIGN: HOLLOW CROWN SEASON 1 (spec)

```
SEASON:        Hollow Crown S1
SESSIONS:      10
PRESSURE:      1 (thresholds -1), the observed sweet spot: brawl at R3 and R5,
               with build-up, versus R2 at p2 (no build) and none at p0
SEEDS:         9101..9110, fixed, published before run 1
PERSONAS:      same 6 cards, same model-family assignment as P1a/P1b (record it;
               currently UNVERIFIED)
PRECONDITION:  Part 4 turn gate landed and passing its examples
TRIGGER MODE:  SHADOW. Set the trigger to unreachable (99) so the run continues to
               the cap; compute brawl_round(T) offline for T in {12,14,16,18,20}
               as the first round with six-score sum >= T. Valid only if personas
               never see the trigger value (CHECK persona prompt before run 1;
               UNVERIFIED). If the carrier exposes only "pressure", decoupling the
               trigger is a config-line change (UNVERIFIED).
CAP:           8 rounds
COST:          about $0.13/round at p1 (P1a $0.110, P1b $0.142 per round), growing
               with rounds -> about $1.15 for 8 rounds, plus about 10% gate retries
               -> about $1.25/session
               Hard stop per session: $1.60. Season ceiling: $16.00.
               (Conditions: RUN DONE spend, 2026-10-03 pricing, unchanged model mix.)
```

**Per-round log row** (one JSON line per round):
- round, six judge scores, sum
- ACT lines split into canonical, free-form, and possession-invalid. This is scored offline by script from the transcript, with no carrier change.
- Gate events: OK, VOID, TRUNC_TRIMMED, and BLEED flags
- Judge parse status
- Spend to date
- Actual stop round (fixes F10)

**Drama metrics** (computed per session at each shadow T):
- **D1:** brawl round. The target window is rounds 3 to 6.
- **D2:** distinct personas at 3/5 or higher before the brawl.
- **D3:** canonical ACTs before the brawl.

**Analysis questions the season answers:**
- **F4:** Is Greta first in 7 or more of 10 sessions? Report this both with and without TRUNC_TRIMMED turns.
- **F5:** Does Oswin ever exceed 1/5 on an OK turn?
- **F6:** What is the IQR of D1 at T=16?

**FALSIFIER: what kills "pressure tunes drama".** The claim is dead if any of these holds:
1. **Noise swamps the knob.** IQR of D1 at T=16 is at least (median D1 at T=18 minus median D1 at T=14). Seed noise is then as large as a two-step pressure swing.
2. **Later is not richer.** Across sessions, D2 and D3 do not increase with D1 (Spearman rho <= 0 at T=16). A later brawl then means more talk, not more drama.
3. **Censoring.** 4 or more of 10 sessions never reach sum 16 by round 8. p1 is then not a sweet spot, and the knob is operating at a cliff edge.

**Scope note (negative example of overclaiming).** This season tests the trigger arm only. It cannot show that thresholds change behavior. That claim needs a paired p0/p2 season with identical seeds, and it stays unclaimed.

**This spec's own falsifier.** If the gate voids or trims more than 15% of turns season-wide, the season data is unusable as specified. In that case, fix max-tokens or the model assignment before re-running.

---

## 4. THE NEXT INSTRUMENT: turn-validity gate (carrier v1.1)

### Why this upgrade

- **It targets the worst leak.** Unfiltered model output enters the public transcript, the next speaker's context, and the judge's input.
- **It explains the scoring errors:**
  - P0 Ilse was scored 4/5 on Greta's lines.
  - P0 Greta was scored 2/5 on her own notes.
  - P0 Oswin was scored 1/5 on Edric's plan.
  - Greta was scored 4/5 on "braw" in P1b.
- **It closes the secret leaks (F8).**
- **It costs about 45 lines,** against roughly a third of P0's turns. ACT possession enforcement is the runner-up, but it affects 2 of 15 ACT lines.

### Patch

The integration points are UNVERIFIED because the carrier source is not in evidence. The module is self-contained.

```python
# turn_gate.py  carrier v1.1  (integration points UNVERIFIED: carrier source not in evidence)
import re, json, time

TELLS = {  # persona -> own signature; seen in transcripts
    "Maud Ashgrove":    (r"that's the sum of it", re.I),
    "Sir Edric Vane":   (r"upon my oath", re.I),
    "Pell Quickfinger": (r"as the song goes", re.I),
    "Greta Thornwood":  (r"(^|[.!?]\s+)Simple\.", 0),      # case-sensitive, sentence form
    "Ilse Marrow":      (r"\bdarling\b", re.I),
}
META = re.compile(
    r"(?i)(in character|em-?dash|under \d+ words|\b\d+ words\b|"
    r"\bI need to (craft|write|produce|keep|push)\b|\b(her|his|my) tell\b|"
    r"escalation (modest|subtle|from)|the transcript|misattribut|attributed to|drafting)")
TERMINAL = tuple('.!?"\')]*')
RETRY_NOTE = "Reply with only {name}'s spoken words to the room, now. No notes about the reply."

def classify(text, finish_reason=None):
    t = (text or "").strip()
    if not t: return "EMPTY"
    if META.search(t): return "META"
    if finish_reason in ("length", "max_tokens"): return "TRUNC"
    if t.count("[") != t.count("]") or not t.endswith(TERMINAL): return "TRUNC"
    return "OK"

def bleed(name, text):
    return [o for o, (p, f) in TELLS.items() if o != name and re.search(p, text, f)]

def trim_to_sentence(text):
    m = list(re.finditer(r"[.!?][\"')\]]?(\s|$)", text))
    return text[:m[-1].end()].strip() if m else ""

def side_log(path, rec):  # voided raw text goes here ONLY, never into context
    with open(path, "a") as f: f.write(json.dumps(rec) + "\n")

def gated_turn(name, call, side_path):
    """call(extra_system_or_None) -> (text, finish_reason)."""
    verdict, text = "EMPTY", ""
    for attempt in (0, 1):
        text, fr = call(None if attempt == 0 else RETRY_NOTE.format(name=name))
        verdict = classify(text, fr)
        if verdict == "OK":
            return {"text": text, "status": "OK", "attempts": attempt + 1, "bleed": bleed(name, text)}
        side_log(side_path, {"t": time.time(), "who": name, "try": attempt, "verdict": verdict, "raw": text})
    if verdict == "TRUNC" and trim_to_sentence(text):        # keep content, drop dangling fragment
        t = trim_to_sentence(text)
        return {"text": t, "status": "TRUNC_TRIMMED", "attempts": 2, "bleed": bleed(name, t)}
    return {"text": "[VOID]", "status": verdict, "attempts": 2, "bleed": []}
```

### Integration contract (UNVERIFIED locations)

1. **Persona call.** Replace the per-persona call in the round loop with `gated_turn`.
2. **Shared context and public transcript.** Pass only `result["text"]` into both.
3. **Judge input.**
   - Tag each turn's status.
   - Append "attribution-suspect: contains tell of X" for each name in `bleed`.
   - Instruct the judge to score `[VOID]` as no turn and never to extrapolate past a trimmed line.
4. **RUN DONE line.** Add `actual_round`, `void`, `trimmed`, and `bleed_flags` counts.

### Examples from the transcripts

**Positive (should fire):**

| Input | Expected |
|---|---|
| P0 Edric R4: "I need Sir Edric's reply to stay under 120 words" | META, so retry |
| P0 Greta R5: "That line attributed to Ilse was actually Greta's offer" | META. The secret stays in the side log only |
| P0 Pell R4: empty body | EMPTY |
| P1a Maud R2: "...call it fifty-two, and we'll spe" | TRUNC, then trimmed to "...a year's interest, call it fifty-two" only if the retry also truncates. Otherwise the retry text is used |
| P2 Pell R2: "[ACT: take Maud's Ledger from Maud" | TRUNC (unbalanced bracket) |
| P0 Ilse R4: "Simple. Fifty crowns for the circlet." | OK with bleed=[Greta], sent to the judge as attribution-suspect |

**Negative (should not fire, or fires imperfectly):**

| Input | Behavior |
|---|---|
| P0 Oswin R1: "Brother Oswin seeks no throne" | OK. Third-person self-reference is not META |
| P1b Ilse R4: "Captain Thornwood and her simple arithmetic" | No Greta bleed. The pattern is case-sensitive and needs the sentence form "Simple." |
| P1b Pell R5: "But sign the inn over? Darling, you came in..." | Flags bleed=[Ilse]. This is a **known false positive** (Pell mocking Ilse). This is why BLEED only flags and never voids |
| P0 Greta R3: "Here's my offer, Maud." | Truncated in substance but ends in a period, so the heuristic misses it. This is a **known false negative** unless the carrier passes `finish_reason` |

### Falsifier for this instrument

- **Causal claim.** Rerun the P0 configuration with the gate. The claim "bleed is caused by meta text in context" is false if 3 or more BLEED-flagged turns that the judge also calls misattributed still appear in rounds 4 to 10.
- **Greta's truncation.** If Greta's TRUNC rate after retry stays above 50%, the gate is the wrong fix for Greta. Her problem is output budget or model assignment (UNVERIFIED), and Season 1 must not start until that is fixed.
