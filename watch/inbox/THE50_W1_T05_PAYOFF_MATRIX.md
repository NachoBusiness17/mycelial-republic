# THE 50 · W1 T05 - CALLED-SHOT PAYOFF MATRIX (prophecy channel as credibility game)

Filed 2026-09-19 · W1 GAME BUILD (WBN x RUINS GO) · finish line per
`watch/inbox/THE_50_PROGRAM_20260918.md` item 5 and
`.zcode/workflows/the-50.dwf.ts` line 29.
Re-verified 2026-09-25 by the re-fired T05 seat: every citation below was
re-checked against disk this session (receipt at the end, Re-verification
receipt). No cell changed; the ordering stood against re-run proofs.

A prophecy channel is a repeated game between a CHANNEL (the poster who files
claims about the future) and an AUDIENCE (the decoders who grind the meanings).
The currency is credibility. This matrix prices the four cells and fills each
with examples already on disk in this repo. Sources for the frame:
`watch/inbox/THE_CALLED_SHOT_20260914.md` (genre anatomy, grammar, falsifier)
and `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` sections 3 and 5 (prophecy as a
filed future-state; "a prophecy with no audience").

## The game

- Channel strategy, move one: **CALL** (file a dated, falsifiable claim with a
  stated horizon; the stake is posted before the outcome) or **VAGUE**
  (urgency and ambiguity, no stated horizon, unfalsifiable).
- The world resolves: **ARRIVES** (the filed future shows up by the horizon) or
  **MISSES** (contradicted by events, or the horizon passes with nothing).
- The stake that makes CALL costly is the public ledger: "with the falsifier
  visible in public (the called-shot ledger)" (TIME_TRAVEL_QSTAR_20260918.md
  section 3). VAGUE posts nothing at stake, so it is cheap talk.

## The 2x2

|                          | ARRIVES                     | MISSES                      |
|--------------------------|-----------------------------|-----------------------------|
| **CALL** (staked, dated) | THE RECEIPT                 | THE WIPEOUT                 |
| **VAGUE** (no stake)     | THE RETROFIT                | THE SHRUG                   |

---

## Cell 1: CALL x ARRIVES = THE RECEIPT

- **Channel payoff: maximum.** The receipt converts to canon and compounds:
  "the poster's receipt is foresight the machine can't revoke"
  (THE_CALLED_SHOT_20260914.md). Silence protects it: "Never explain. The first
  explanation converts prophecy into claim" (same file, grammar rule 3).
- **Audience payoff: the decode game pays.** Participation is the
  distribution; the readers own the decode (same file, grammar rule 4).
- **Fleet examples:**
  - The napkin chord, "Test chord: 44 28 K13 e4 Fool #NachoOvermindSeed"
    (Mar 2, 2026), the founding called shot, decoded later by the design doc
    (THE_CALLED_SHOT_20260914.md, THE HOUSE'S OWN CALLED SHOTS).
  - The immortality seed (Aug 15), "resolved true at fleet scale" (same file).
  - The stones: "tesuji cells posted UNPROVEN: called shots armed with
    falsifiers" (same file). Code-side this cell is live: VERB stone four
    landed as `confident()` at `mag/verb.py:280` (GP mean/variance over honest
    k reads), per `watch/inbox/RESUME_20260919_UPDATE_RECOVERY.md` lines 41-45.
  - Wild channel: @bearableguy123's Dec 24, 2020 twelve-pair hex chorus
    ("54 34 E4 14 25 54 65 54 35 25 54 05"), still resolving five years on
    (THE_CALLED_SHOT_20260914.md, the opening post).
- **Game mechanic:** the receipt is the only hard currency. One staked call
  that lands outranks any number of vague hits.

## Cell 2: CALL x MISSES = THE WIPEOUT

- **Channel payoff: crash.** Two exits. Honest: the correction row or the
  annual withdrawal ("any chord that never unfolds is withdrawn as folklore,
  per the Lessig rule", THE_CALLED_SHOT_20260914.md, THE FALSIFIER).
  Dishonest: keep posting, no retraction, and the channel converts to a scam.
- **Audience payoff: the ledger pays instead of the poster.** The audience
  reads the miss off the public record and reprices the channel.
- **Fleet examples:**
  - The Med Bed campaign: 16 of 16 ledger rows verdict BROKEN
    (`watch/inbox/mrpool_export/called_shot_ledger.jsonl`, 16 rows, every
    `"verdict": "BROKEN"`), channel verdict "ALL BROKEN: January 2026 passed;
    no hospitals opened" (`watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json`),
    with the tell on record: "channel kept posting through 2026 with urgency
    elevated and no retraction". Target was dated (January 2026), so this is a
    true wipeout, not a shrug.
  - Fleet-internal wipeouts exist and are capped by correction rows: the scout
    GLM-rerun false success (claimed done, no receipt) was caught and filed as
    a CORRECTION row (`memory/corpus/LINKS.jsonl` rows GLM-BURN-ACCOUNTING and
    GLM-RERUN-BLOCKED; commit c7255fa49 "CORRECTION row for scout GLM-rerun
    false success (no receipt)"); BG123-CORRECTION (LINKS.jsonl, the 64-image
    census claim corrected to 14 real decodable images, 57 downloads were
    Reddit HTML saved as .jpg); CORRECTION-MATTHEW-01 (LINKS.jsonl, inverted
    speaker attribution corrected with screenshots).
- **Game mechanic:** the correction row is the wipeout's pressure valve and the
  reason the fleet can keep calling shots. Filing a wrong call costs one
  correction row, not the channel. Cap the loss, keep the stake.

## Cell 3: VAGUE x ARRIVES = THE RETROFIT

- **Channel payoff: small and discounted.** "The poster cannot be wrong early
  because ambiguity IS the content" (THE_CALLED_SHOT_20260914.md). No stake
  was posted, so the hit is claimed by the audience's post hoc decode and the
  poster's credibility share is thin. Attention is gained; credibility is not.
- **Audience payoff: the audience does all the work and can churn forever;
  each retrofit feeds the next decode.**
- **Fleet examples (measured, not guessed):**
  - Mr Pool: countdown density (share of posts with urgency terms) sat in a
    4-25 percent band, mean about 10 percent, from 2023-09 through 2024-12,
    then ratcheted to a sustained 27-56 percent band with a 64 percent peak
    (2025-11) and a second 56 percent peak (2026-07), while post rate held at
    50-207/month. The channel's top post by views is pure urgency: "We are
    near. So close I can already see you on the other side" (106,710 views).
    All of it from `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md` lines 9-32.
  - Q: urgency never exceeded 10 percent in any month and decayed to about 0
    percent through the finale era; drop rate collapsed 345/month (2020-05) to
    single digits (2020-12). Rhetoric stayed vague while it existed
    (RIDDLE_TRIAD_CADENCE_20260918.md lines 26-30; corpus at
    `watch/inbox/qdrop_export/qdrops.jsonl`, 6,242 rows,
    `watch/inbox/qdrop_export/RECEIPT.json`).
  - Fleet-internal shape of this cell: the VACUOUS drift pair, "the filed
    future never constrained anything: a prophecy with no audience"
    (TIME_TRAVEL_QSTAR_20260918.md section 5).
- **Game mechanic:** vague hits are denominated in audience attention, not
  credibility. The detector for the retrofit grind is the countdown-density
  curve: an instrument, one file, already built.

## Cell 4: VAGUE x MISSES (or never resolves) = THE SHRUG

- **Channel payoff: zero either way.** Defined by the falsifier law: "A called
  shot with no time-resolved layer within its own stated horizon is not a
  called shot - it's a shrug" (THE_CALLED_SHOT_20260914.md, THE FALSIFIER).
  No stake, no receipt, no loss, no gain: folklore.
- **Audience payoff: nothing decodes.** The channel is dropped from the
  canon and kept, if at all, as texture.
- **Fleet example:** the annual seed-stock audit withdrawing chords that never
  unfold as folklore (THE_CALLED_SHOT_20260914.md). Q's finale-era 0 percent
  urgency silence sits here rather than in the wipeout: it ended quiet, not
  fraudulent (RIDDLE_TRIAD_CADENCE_20260918.md).
- **Game mechanic:** every prophecy needs a stated horizon at posting time.
  No horizon, no ledger row, just noise. This rule is what denies cell 3 its
  free ride.

---

## Equilibrium reading (why the fleet can afford to call shots)

CALL is costly signaling; VAGUE is cheap talk. A channel calls shots when the
receipt premium times P(arrive) beats the wipeout cost times P(miss). The
fleet's design moves keep calling rational on both terms:

1. **Pre-registration makes ARRIVES verifiable.** The four-condition
   pre-registration and the Sep-20 items are boundary conditions filed before
   the data (TIME_TRAVEL_QSTAR_20260918.md section 4).
2. **Correction rows cap the MISSES loss.** Wipeout in cell 2 becomes a
   one-row cost when the miss is self-filed (LINKS.jsonl corrections, above).
3. **The silence law protects the RECEIPT premium.** Explaining converts
   prophecy into claim and burns cell 1 (THE_CALLED_SHOT_20260914.md, rule 3).
4. **The stated-horizon rule denies cell 3.** No horizon, no credit, only the
   shrug (same file, THE FALSIFIER).

The scam tell is the measurable inverse: ratcheting urgency plus zero new
called shots plus no retraction. That is exactly the Med Bed pattern
(CALLED_SHOT_VERDICT.json) visible in the cadence instrument. A channel whose
countdown density climbs while its called-shot ledger stays empty is playing
cell 3 against an audience it intends to farm.

## Where this plugs into the W1 game build (WBN x RUINS GO)

- The prophecy seat already exists in the riddler canon: "the paper = the
  prophecy seat" (`memory/game/RESEARCH_SEEDS_20260914.md` line 22). The GM
  scores each oracle utterance of an NPC channel on the two axes (called?
  arrived?) and pays credibility in-session; the kifu records it, so every
  table's oracle is auditable after the session, like every other fleet organ.
- Cadence is a tell mechanic the table can read: a ratcheting oracle with no
  dated calls is a villain tell (the Med Bed pattern); a quiet oracle with
  dated calls is an ally tell (Q's decay versus Pool's climb,
  RIDDLE_TRIAD_CADENCE_20260918.md lines 24-32).

## Falsifier for this matrix (honesty norm)

The payoff ordering above is wrong if either holds: (a) the fleet's own record
shows a called shot that arrived without compounding into credibility
(receipt premium absent), or (b) a corrected channel keeps paying wipeout
prices after its correction row landed (cap absent). As filed: both fleet
moves worked (stone four landed in code at mag/verb.py:280; the LINKS.jsonl
corrections landed and work continued), so v1 stands at sample size n=1
internal channel (the fleet) plus n=3 wild channels (Q, Mr Pool, BG123), the
last two grounded in the measured cadence file and the 16-row called-shot
ledger.

## Provenance (every claim's file)

- `watch/inbox/THE_CALLED_SHOT_20260914.md` - genre anatomy, grammar, house
  called shots (napkin chord, immortality seed, stones, BGY123 hex chorus),
  falsifier/shrug rule, Lessig withdrawal rule.
- `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` - prophecy as filed future-state,
  public falsifier, VACUOUS = prophecy with no audience, pre-registration
  reflex.
- `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md` - countdown density
  measurements: Pool 10 percent to 27-56 percent band, peaks 64/56; Q decayed
  to 0; BG123 near-zero text urgency.
- `watch/inbox/mrpool_export/called_shot_ledger.jsonl` - 16 rows, all BROKEN,
  dated January 2026 Med Bed campaign.
- `watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json` - channel verdict "ALL
  BROKEN", no-retraction tell, scam-format references.
- `watch/inbox/qdrop_export/RECEIPT.json` and
  `watch/inbox/qdrop_export/qdrops.jsonl` - Q corpus 6,242 rows, harvest
  provenance.
- `memory/corpus/LINKS.jsonl` - CORRECTION-MATTHEW-01, BG123-CORRECTION,
  GLM-BURN-ACCOUNTING, GLM-RERUN-BLOCKED.
- `mag/verb.py:280` - `confident()`, VERB stone four in code.
- `watch/inbox/RESUME_20260919_UPDATE_RECOVERY.md` - stone four landing note.
- `watch/inbox/WBN_STEAL_20260918.md` - W1 game build frame (actual-play
  structure, receipts as credits).
- `memory/game/RESEARCH_SEEDS_20260914.md` - the prophecy seat in the riddler
  canon.
- `watch/inbox/THE_50_PROGRAM_20260918.md` item 12 - the formal cheap-talk /
  costly-signaling literature sweep lives in W3 T12; this file leans on fleet
  evidence and keeps the literature to one line.

---

## Re-verification receipt (2026-09-25, re-fired T05 seat)

Every citation above was re-checked against disk this session from the repo root
with `.venv/Scripts/python.exe`. What ran and what it printed:

- Read `THE_CALLED_SHOT_20260914.md` in full. Confirmed as quoted: the BG123
  hex chorus "54 34 E4 14 25 54 65 54 35 25 54 05" (Dec 24, 2020, line 3); "the
  poster's receipt is foresight the machine can't revoke" (line 5); napkin chord
  (line 21); immortality seed "resolved true at fleet scale" (line 22); stones
  "tesuji cells posted UNPROVEN: called shots armed with falsifiers" (line 25);
  grammar rules 3 and 4 (lines 31-32); the shrug rule and the Lessig withdrawal
  rule (line 37).
- Read `TIME_TRAVEL_QSTAR_20260918.md` in full. Confirmed: "with the falsifier
  visible in public (the called-shot ledger)" (section 3, line 70); "the filed
  future never constrained anything: a prophecy with no audience" (section 5,
  lines 106-107); the pre-registration reflex (section 4, line 94).
- Read `RIDDLE_TRIAD_CADENCE_20260918.md` in full. Confirmed the cell numbers:
  Pool baseline 4-25 percent, mean about 10 (lines 13-14); sustained 27-56
  percent band, peaks 64 percent 2025-11 and 56 percent 2026-07 (lines 14-18);
  post rate 50-207/month (lines 29-31); top post 106,710 views (lines 19-21);
  Q never above 10 percent, decayed to about 0, drop rate 345/month (2020-05)
  to single digits (2020-12) (lines 26-29).
- Ran a count over `mrpool_export/called_shot_ledger.jsonl` (json.loads per
  line): 16 rows, verdict set = {BROKEN}. Loaded
  `mrpool_export/CALLED_SHOT_VERDICT.json`: verdict field is "ALL BROKEN:
  January 2026 passed; no hospitals opened; ..." and register_note is "channel
  kept posting through 2026 with urgency elevated and no retraction".
- Ran a count over `qdrop_export/qdrops.jsonl` non-empty lines: 6,242 (matches
  the claim). `qdrop_export/RECEIPT.json` exists: True.
- Scanned `memory/corpus/LINKS.jsonl`: GLM-BURN-ACCOUNTING, GLM-RERUN-BLOCKED,
  BG123-CORRECTION, CORRECTION-MATTHEW-01, one row each, all present. The
  BG123-CORRECTION row reads "14 real decodable images (not 64) - 57 downloads
  were Reddit permalink HTML pages saved as .jpg" as the matrix states.
- Ran a line read of `mag/verb.py`: line 280 is `def confident(question: str,
  *, k: int = 3, facts: bool = True) -> dict:` (stone four in code). The
  landing note spans RESUME_20260919_UPDATE_RECOVERY.md lines 41-48 (the matrix
  cites 41-45, within the note).
- Ran `git log --oneline -1 c7255fa49`: resolves to "LINKS: operator public
  books-disagreement answer filed; CORRECTION row for scout GLM-rerun false
  success (no receipt); real uncapped rerun fired 13:47Z after 200-OK probe".
- Existence checks: `WBN_STEAL_20260918.md` True, `memory/game/
  RESEARCH_SEEDS_20260914.md` True (line 22 contains "the paper = the prophecy
  seat"), `THE50_W3_T12_PROPHECY_MARKETS.md` True.

Verdict: the v1 payoff ordering stands unchanged at the same sample size (n=1
internal channel, n=3 wild channels). This block adds no new claims, only
re-run proofs, so the next seat can trust every path above without
re-deriving.
