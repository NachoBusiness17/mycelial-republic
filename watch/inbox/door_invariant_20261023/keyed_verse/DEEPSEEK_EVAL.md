# DEEPSEEK_EVAL (keyed verse): one direct call, key via tools.ds_workhorse.load_key, not Hermes
```json
{
 "model_req": "deepseek-reasoner",
 "max_tokens": 65536,
 "start": "2026-10-23T12:14:23.134887-04:00",
 "end": "2026-10-23T12:15:51.047361-04:00",
 "attempts": [
  "ok"
 ],
 "model": "deepseek-flash",
 "usage": {
  "prompt_tokens": 6874,
  "completion_tokens": 14689,
  "total_tokens": 21563,
  "prompt_tokens_details": {
   "cached_tokens": 0
  },
  "completion_tokens_details": {
   "reasoning_tokens": 13112
  },
  "prompt_cache_hit_tokens": 0,
  "prompt_cache_miss_tokens": 6874
 },
 "finish": "stop"
}```
I requested deepseek-reasoner and the API served deepseek-flash. One pre-flight attempt crashed locally on a UTF-16 input file before any API request was made, so it wasn't a call.

**Audit scale:** E=exact core, P=partial, M=miss; “P+/P−” are executor’s modifiers. L2/L4 are unreached, so no score cells are auditable.

### Score-cell audit vs lane text

**L1 Fostertron MAX**
- P1 E→E, slight over-credit: gets “Sandboxes / processes with no access to each other” + “identical initial code or weights” + cleanup sweeps, but not exactly “identical prompt.” Still core P1.
- P2 E→E: “outputs align” and “six voices reduced to unison” match blind convergence/invariant.
- P3 P+→P: over-credit. It has gate/weighing, C–G hum, rest→wide arpeggio, but no standing-wave, small-model/Moto, cheap triage, or buffer-before-wide-fan-out.
- P4 P→P: “log vs law / narrative vs statute” is there; “rules hidden in story” is not.
- Cont HELD→HELD; Form KEPT→KEPT; Key 2.5→2.5.

**L3 agy bob**
- P1 E→E: “isolated processes,” “same program or rules,” brooms sweep “time or noise” survives. Minor over on prompt equivalence.
- P2 E→E: “agreement without coordination” + six voices to one pitch is exact.
- P3 P→P: score defensible, but executor’s “order reversed” critique is shaky; L3 does say gate “then checks that answer,” while key’s wide fan-out ordering is what is missed. Missing standing-wave/Moto/cheap triage/buffer.
- P4 P+→P+: mildly generous but defensible: “narrative that binds” + descent as “rule set being read out.” Still not explicit parable-as-spec.
- Cont HELD→HELD, though “thread/said” is slant; Form MOSTLY→MOSTLY; Key 2.5→2.5.

**L4sub qwen2.5**
- P1 P→weak P/M: over-credit. “isolation and separation” + “shared task or purpose” only; no identical input, no broom-as-noise sweep.
- P2 P→weak P/M: over-credit. Gets “common thread” but not blind invariant/unison.
- P3 M→M: “motor = progress or change” misses gate/standing-wave/triage entirely.
- P4 P→P: “rules or laws governing the narrative” is partial story-vs-law.
- Cont BROKEN→BROKEN; Form BROKEN→BROKEN; Key ~1→~0.75–1.

**L5 OpenCode**
- P1 E→E: “six workers, one program, no communication, one identical result”; broom “resets the room / garbage collection.”
- P2 E→E: “Agreement without communication” + “six voices literally speaking in unison.”
- P3 P→P, possibly under-credited on musical subfeatures: it decodes C4–G4 “motor’s hum,” rest as wide hall, rest→C-major arpeggio. Still misses standing-wave, Moto, cheap triage, buffered wide fan-out.
- P4 P→P+: under-credit. It says “stepwise descent, the ‘story told’ walking down the scale line by line, statutes recited” — closer to descent-across-told/hold than bare partial.
- Cont WEAK-HELD→WEAK-HELD; Form KEPT→KEPT; Key 2.5→2.5–2.75.

**L6 local gemma4**
- P1 P→weak P/M: over-credit. “six isolated lives or fates” / “threads of destiny” does not reach six-lane run, identical prompt, or lane-noise sweep.
- P2 P→weak P/M: over-credit. “weave blindly” + “reveal their truth” is mystery/revelation, not invariant/unison.
- P3 M→M: “motor… passage of time or systematic judgment” misses gate triage/standing wave.
- P4 P→P: “Narrative vs Constraint” is partial story/law.
- Cont BROKEN→BROKEN; Form LOOSE→LOOSE; Key ~1→~0.75–1.

### What made pointers hold/fracture
- **P1 held** on strong lanes because of TEXT-GROUNDED “Six strangers were locked in six rooms,” “same folded looms,” “brooms,” plus the identical `D4…C5 | G4h` lines. Small lanes drifted to INTERPRETIVE “fates/destiny” and lost the run/input/sweep structure.
- **P2 held** because TEXT-GROUNDED “without peeking” + “all came out speaking” + `G4×6 | G4h` unison made blind convergence legible. Small lanes read “peeking/speaking” as INTERPRETIVE mystery/revelation rather than invariant.
- **P3 fractured** at TEXT-GROUNDED “small motor’s hum stood at the gate,” fixed `C4/G4` oscillation, and “wide hall lay quiet in wait” + rest→wide arpeggio. Strong lanes got gate/hum/weighing, but “stood” did not cue standing wave; “small motor” did not cue Moto/cheap small-model triage; “wide hall” did not cue buffered wide fan-out. Lanes often read the gate as post-hoc validator (INTERPRETIVE).
- **P4 stayed partial**: TEXT-GROUNDED “The story it told / Had statutes to hold” + descending scale across `told`/`hold` gave narrative-vs-law. Lanes missed the stronger INTERPRETIVE point: the story itself carries the spec/rules.

### Did any lane reconstruct more than scored?
No lane reached the full key. The clearest under-score is **L5**: its P4 musical decode (“story told” descending/statutes recited) and P3 musical decode (C–G hum, rest→arpeggio) justify maybe P3 P+ and P4 P+. L1/L3 add unplanned musical insights (“C major minus G,” G→C cadence), but not hidden-key content. L4sub/L6 are over-credited, not under-credited.

### Redesign weakest pointer P3
INTERPRETIVE fixes, without naming the concept:
- Make fixedness visible: replace “hum stood” with “its hum held one place / a two-note loop at the gate” to cue standing wave by image.
- Add cheap-triage cue: “light freight went first through a narrow slot” or “small loads passed cheap; heavy loads wait.”
- Add buffered wide fan-out: final line “six wide doors lay queued in wait” instead of only “wide hall lay quiet in wait.”
- Notation: hold the `C4–G4` pair as a repeated fixed dyad/fermata, add a clear rest/buffer bar, then the six-note wide `C4…G5→C6w` arpeggio. Avoid relying on the Moto pun; it did not survive blind reading.