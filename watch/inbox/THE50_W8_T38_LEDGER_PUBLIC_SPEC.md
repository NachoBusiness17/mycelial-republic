# THE 50 · W8 T38 - CALLED-SHOT LEDGER AS PUBLIC ARTIFACT SPEC

Filed 2026-09-19 · finish line per `watch/inbox/THE_50_PROGRAM_20260918.md`
line 59: "38. Called-shot ledger as public artifact spec [QUEUED]".

**This is a spec, not a publication.** Nothing leaves the machine by this file.
Publishing is an OPERATOR-class gate (THE 50 launch law, line 78: OPERATOR items
are the gates; data-tier law governs what may leave, `docs/FRAMEWORK_LOAD.md`
line 28 "T0/T1 never remote", `docs/PLATFORM_AGNOSTIC_OPERATING_PROTOCOL.md`
line 20 "T0/T1 never leave the machine"). This file answers one question: if the
operator says publish, what exactly goes out the door, and what never does.

## 1. What exists today (measured in this ask, not guessed)

Census command run for this spec:

```
.venv/Scripts/python.exe -c "<json.loads over the two ledgers, print counts>"
```

Output, verbatim facts:

- `watch/inbox/mrpool_export/called_shot_ledger.jsonl` - the scored ledger v1.
  16 rows, every `"verdict": "BROKEN"`, 12 distinct source videos
  (msg_2927 through msg_3095), post dates 2025-09-24 to 2025-10-20, targets
  2026-01-01 (15 rows) and 2026-01-06 (1 row, the "100 days away" video),
  kinds `month_year` and `days_away`, views 6,816 to 9,804, no duplicate rows,
  fields per row: `msg_file, post_date, target_date, kind, views, context,
  verdict, note`. No em-dash appears in any context quote (checked).
- `watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json` - the channel verdict:
  16 rows, 1 unique claim, verdict "ALL BROKEN: January 2026 passed; no
  hospitals opened", campaign window 2025-09-24 to 2025-10-20, plus the
  no-retraction tell on record.
- `watch/inbox/mrpool_export/called_shot_ledger_captions.jsonl` - the UNSCORED
  pool: 107 caption rows, 65 distinct messages, post dates 2024-04-22 to
  2026-09-07, target horizons 2025-01-01 through **2028-03-01**, and no
  `verdict` field on any row. Some of these horizons are still in the future:
  live PENDING rows exist.
- Raw harvest that stays private (below): `ledger.jsonl` (2.0 MB),
  `ledger_full.jsonl` (5.8 MB), `media_register.jsonl` (980 KB),
  `transcriptions.jsonl` (911 KB), `cache_index.jsonl` (1.1 MB), `media/`,
  `media_full/`, `media_matched/` (3.64 GB recovered, per
  `watch/inbox/mrpool_export/HARVEST_COMPLETE.json`).

## 2. Why publish it at all (the point on file)

- The public ledger is the stake that makes CALL costly: "with the falsifier
  visible in public (the called-shot ledger)"
  (`watch/inbox/TIME_TRAVEL_QSTAR_20260918.md:70`). A ledger only the house can
  see stakes nothing.
- Cell 2 of the payoff matrix: when a call misses, "the audience reads the miss
  off the public record and reprices the channel"
  (`watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md:68`, corrected 2026-09-25 from
  the stale cite 64-65). Publication is what
  turns the Med Bed wipeout from a fleet note into a public receipt.
- The scam tell needs a public yardstick: "A channel whose countdown density
  climbs while its called-shot ledger stays empty is playing cell 3 against an
  audience it intends to farm" (same file, lines 155-156, corrected
  2026-09-25 from the stale cite 149-153). Publishing our
  filled ledger against the wild channels is the instrument the wild machines
  lack (TIME_TRAVEL_QSTAR_20260918.md:70-71, cite re-verified 2026-09-25).

## 3. The public artifact, in one paragraph (what a reader sees)

One static page, plain English, readable on a phone in one pass. A title, one
line of method, then the table: for each call, what was claimed (verbatim quote
from the channel), when it was posted, the stated horizon ("open hospitals by
January 2026"), what actually happened, and the verdict. Then the campaign
summary (16 of 16 broken, no retraction), the scoring method, the disclaimer,
and a provenance footer. No login, no scripts, no tracking, no comments. A
machine-readable twin (`ledger.json`) carries the same rows for anyone who
wants to audit or extend it.

## 4. Shape and generation

- Build script (named here, built only when the gate opens):
  `scripts/the50_t38_ledger_public.py`, following the house convention of the
  other THE 50 scripts (see the header of
  `scripts/the50_t21_q_caption_ledger.py` for the pattern: read internal files,
  deterministic transform, write artifacts, run with
  `.venv/Scripts/python.exe`).
- Inputs: the three files in section 1, nothing else.
- Outputs: `ledger.html` (the page) and `ledger.json` (the rows), one command,
  byte-reproducible from the same inputs. The script also prints the sha256 of
  both outputs so the published copies can be checked against the build.
- Hand-editing the public page is forbidden: if a row is wrong, fix the
  internal ledger, file a correction, rebuild.

### Public row schema (internal -> public)

| Internal field | Public field | Rule |
|---|---|---|
| (new) | `id` | Stable public id `CSL-001`..`CSL-016`, ordered by post_date then target_date |
| `msg_file` | `source` | The bare Telegram message number only: `msg_2927.mp4` becomes `Mr Pool msg 2927` |
| `post_date` | `posted` | Keep exactly (ISO date) |
| `context` | `claim` | Verbatim words, trimmed to the sentence(s) carrying the dated claim, max 320 chars at a sentence boundary (the T21 convention) |
| `target_date` | `by` | Keep exactly |
| `kind` | `precision` | `month_year` -> `month`, `days_away` -> `day` |
| `views` | `reach` | Bucketed to the nearest thousand: 6816 -> "about 7k views" |
| `verdict` | `verdict` | Keep exactly: BROKEN |
| `note` | `verdict_basis` | Rewritten plain English; see redaction rule R4 |
| (new) | `row_sha256` | sha256 over the public row, so edits are detectable |

Worked example, row 1 of 16 (from `called_shot_ledger.jsonl` line 1):

```json
{"id": "CSL-001", "source": "Mr Pool msg 2927", "posted": "2025-09-24",
 "claim": "But in January, 2026, the future begins and the key is in your
 hands. The Med Bed Card is more than a card. It is your personal entry to
 America's most advanced hospitals",
 "by": "2026-01-01", "precision": "month", "reach": "about 7k views",
 "verdict": "BROKEN",
 "verdict_basis": "The stated date passed. No hospital opened. The card sales
 match the publicly documented Med Bed scam format: paid priority cards for a
 facility that never materialized."}
```

## 5. THE REDACTION LIST (the core of this spec)

Decisions: KEEP (ships as is), TRANSFORM (ships in changed form), BUCKET
(coarsened on purpose), DROP (field or value never ships), NEVER (whole file or
class of content never ships).

| # | Item | Decision | Why |
|---|---|---|---|
| R1 | `msg_file` internal names (`msg_2927.mp4`) | TRANSFORM to bare message number | The `.mp4` name is our harvest layout, not public fact. The bare number is how anyone finds the message in the public channel and checks the quote. |
| R2 | `context` quotes | TRANSFORM: trim to the dated-claim sentence, words verbatim | The claim is the evidence and ships; the surrounding sales pitch beyond it does not. Trimming is mechanical, not editorial. |
| R3 | `views` exact counters | BUCKET to nearest 1,000 | Exact counts fingerprint the harvest day (Telegram counters move); the verdict needs magnitude, not precision. |
| R4 | `note` third-party references ("Skye Prince", "Marilyn J. Williams", "McGill OSS") | DROP any name that does not ship with a public source URL in the same field | Naming private or semi-private people without a checkable link is the one defamation trap in this dataset. McGill OSS (a public university office) and a published exposé can ship WITH links the operator approves. Anything unlinked ships genericized: "publicly documented scam-format references on file". |
| R5 | Row identity | TRANSFORM: public ids `CSL-nnn` + `row_sha256` | Internal line numbers are meaningless outside the repo; hashes make the public artifact tamper-evident. |
| R6 | Channel label | KEEP: "Mr Pool" | It is the channel's own public name (used throughout `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md`). An anonymous label would make every row unverifiable. |
| R7 | The impersonated public figure ("President Trump promised...") | KEEP inside verbatim quotes only, plus one page-level disclaimer | The quotes are the channel's own videos impersonating a public figure; they are evidence of the scam, not statements by that figure. The disclaimer says exactly that, once, at the top: "Quotes are from the channel's own videos, which imitate public figures. They are not statements by those figures." |
| R8 | Dates, horizons, verdicts | KEEP exactly | This is the game itself. Redacting a horizon or verdict would gut the artifact. |
| R9 | `ledger.jsonl`, `ledger_full.jsonl`, `transcriptions.jsonl`, `cache_index.jsonl` | NEVER | Full raw channel harvests; the public ledger needs 16 trimmed quotes, not 3,663 messages. |
| R10 | `media_register.jsonl` and all `media/` trees | NEVER | The register carries per-user reaction ledgers including paid tips (`HARVEST_COMPLETE.json`, register_note line): third-party personal data of channel readers. The 3.64 GB of media also stays: no rehosting, copyright, and text quotes are the artifact. |
| R11 | The 107-row unscored caption pool | NEVER in v1 | No `verdict` field on any row; horizons run to 2028-03-01. Rows ship only once scored. This is the "no horizon, no ledger row" discipline pointed the other way: no verdict, no public row. |
| R12 | Fleet internals: repo name, machine paths (`watch/inbox/...`), operator identity, usernames, seat names, fleet jargon (fleet, lane, seat, verkle, mag) | NEVER on the public face | The public face is one-pass plain English by law (`watch/salon_source_moon_speak_20260911.md`; commits e56a190f8 and c7255fa49: "public gets the one-pass version, no fleet jargon"). Export law: nothing prohibited by the data tier leaves (`docs/CROSS_AGENT_VERKLE_HANDOFF.md:12`). |
| R13 | Credentials, endpoints, keys | NEVER | Static artifact only; nothing that could route back into the machine. |

## 6. Method page (ships as part of the artifact)

Short, plain, four paragraphs:

1. What a called shot is: a dated, checkable claim posted before its horizon
   (the two-axis scoring of `THE50_W1_T05_PAYOFF_MATRIX.md`: called? arrived?).
2. The verdict classes: BROKEN (horizon passed, stated future did not arrive),
   ARRIVED (it did), PENDING (horizon still ahead), WITHDRAWN (the claim is
   retired as folklore, the Lessig rule in `THE_CALLED_SHOT_20260914.md`,
   THE FALSIFIER).
3. The shrug rule: a post with no stated horizon gets no row at all
   (THE_CALLED_SHOT_20260914.md: "a called shot with no time-resolved layer
   within its own stated horizon is not a called shot - it's a shrug").
4. How rows change: append-only. A verdict change appends a revision row, it
   never edits history. Mistakes get correction rows, the house precedent being
   `memory/corpus/LINKS.jsonl` (BG123-CORRECTION, CORRECTION-MATTHEW-01 rows
   verified present in this ask).

## 7. Update protocol after publication

- New channel claims are scored into the internal ledger first, then batched
  into public rebuilds; the public artifact always regenerates from disk in one
  command.
- PENDING rows may ship (marked PENDING) once scored; the 2028 horizons in the
  pool are real future rows, which is exactly the honest state a public ledger
  should show.
- The annual seed-stock audit (THE_CALLED_SHOT_20260914.md, THE FALSIFIER)
  applies to our own calls too: if the fleet ever posts called shots publicly,
  its own ledger page carries the same WITHDRAWN class. Symmetry or the
  artifact is propaganda.

## 8. Publish path options and the gate

All options are static files, no server, no keys:

- a) The operator posts `ledger.html` + `ledger.json` anywhere a file can live
  (a gist, a personal page, a static host).
- b) A public mirror repo containing only the two files plus the method page.
- c) An existing public surface the operator already controls.

The gate: **the operator decides if and where**. This spec files the design;
per THE 50 launch law (line 78) and the data-tier law, no seat publishes. The
build script is written and run only on an operator order to prepare a
candidate bundle, and the bundle still waits for the operator's hand to ship.

## 9. Checks actually run for this spec (this ask)

Command and output (both ledger files, exact numbers used above):

```
.venv/Scripts/python.exe -c "<census over called_shot_ledger.jsonl +
called_shot_ledger_captions.jsonl>"
```

- scored ledger: 16 rows / 16 BROKEN / 12 distinct msg_file / post range
  2025-09-24 to 2025-10-20 / targets {2026-01-01, 2026-01-06} / kinds
  {month_year, days_away} / views 6816..9804 / no duplicate rows / no em-dash
  in any context / fields confirmed.
- caption pool: 107 rows / 65 distinct msg_id / post range 2024-04-22 to
  2026-09-07 / target range 2025-01-01 to 2028-03-01 / verdict field absent.
- `BG123-CORRECTION` and `CORRECTION-MATTHEW-01` confirmed present in
  `memory/corpus/LINKS.jsonl` (grep count).
- Not run (honest gaps): no build script exists yet (section 4 names it; the
  gate in section 8 precedes it), no public page was generated, no hosting was
  touched.

### 9a. Re-verified 2026-09-25 (second ask)

Re-ran the full census with `.venv/Scripts/python.exe` over both jsonl files in
this ask. Every number in section 1 holds unchanged: scored ledger 16 rows /
16 BROKEN / 12 distinct msg_file / post range 2025-09-24..2025-10-20 / targets
{2026-01-01, 2026-01-06} / kinds {days_away, month_year} / views 6816..9804 /
msg range msg_2927..msg_3095 / 0 duplicate rows / 0 em-dashes in any context /
the 8 fields confirmed. Caption pool: 107 rows / 65 distinct msg_id / post
range 2024-04-22..2026-09-07 / `target_date` range 2025-01-01..2028-03-01 /
`verdict` field absent on all 107 rows (the pool field name is `target_date`).
Also re-confirmed this ask: row 1 of `called_shot_ledger.jsonl` carries exactly
the inputs of the section 4 worked example (msg_2927.mp4, 2025-09-24,
2026-01-01, month_year, 6816 views, verbatim Med Bed Card quote, BROKEN, and
the internal note the example's verdict_basis rewrites per R4);
`BG123-CORRECTION` and `CORRECTION-MATTHEW-01` each present in
`memory/corpus/LINKS.jsonl` (grep count 1 each); all files cited in section 10
exist on disk; `THE_50_PROGRAM_20260918.md` line 59 is still task 38 and line
78 still carries the OPERATOR gate; zero em-dashes in this file (grep count 0).
Two citation drifts found and fixed in place (see sections 2 and 10). Post-
filing state check: no file in `mrpool_export/` changed after this spec was
filed (all still dated 2026-09-18/19); `THE_UNDENIABLE_LEDGER_20260923.md` and
`UNDENIABLE_LEDGER_ADDENDUM_20260923.md` are a different artifact (dossier
fact-check families) and name no called-shot, Mr Pool, or Med Bed matter (grep:
zero hits), so the ledger state this spec describes is current as of 2026-09-25.
Still not run: no build script exists, no public page generated, no hosting
touched; the section 8 operator gate is unchanged.

## 10. Provenance (every claim's file)

- `watch/inbox/THE_50_PROGRAM_20260918.md:59` - the task; line 78 - OPERATOR
  items are the gates.
- `watch/inbox/mrpool_export/called_shot_ledger.jsonl` - the 16-row scored
  ledger (read in full this ask).
- `watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json` - channel verdict, ALL
  BROKEN, no-retraction tell.
- `watch/inbox/mrpool_export/called_shot_ledger_captions.jsonl` - the 107-row
  unscored pool, horizons to 2028-03-01.
- `watch/inbox/mrpool_export/HARVEST_COMPLETE.json` - harvest size (2,375 of
  2,377, 3.64 GB) and the register's reaction/paid-tip fields.
- `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md:70` - "the falsifier visible in
  public (the called-shot ledger)".
- `watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md` - the 2x2, cell 2 audience
  repricing (line 68), scam tell (lines 155-156); cites corrected 2026-09-25.
- `watch/inbox/THE_CALLED_SHOT_20260914.md` - falsifier/shrug rule, Lessig
  withdrawal rule, the silence law.
- `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md` - the channel's public name
  and cadence measurements.
- `memory/corpus/LINKS.jsonl` - correction-row precedent (BG123-CORRECTION,
  CORRECTION-MATTHEW-01, verified present).
- `watch/salon_source_moon_speak_20260911.md` + commits e56a190f8, c7255fa49 -
  the plain-English public-voice law.
- `docs/FRAMEWORK_LOAD.md:28`, `docs/PLATFORM_AGNOSTIC_OPERATING_PROTOCOL.md:20`,
  `docs/CROSS_AGENT_VERKLE_HANDOFF.md:12` - the export/tier law.
- `scripts/the50_t21_q_caption_ledger.py` - the THE 50 build-script convention
  and the 320-char claim trim rule.
- `watch/inbox/SHARED_SURFACE_CONTRACT.json` - receipt and classification laws
  this filing follows.

## 11. Falsifier for this spec

This spec fails its own bar if any of these hold:

1. A public field in the section 4 table cannot be produced by the one-command
   deterministic transform from files on disk.
2. Any third-party name ships without a source link (R4 violated).
3. Any R9-R13 item appears on the public face (one leak kills the artifact).
4. The page needs more than one pass to read (moon-speak regression).

If the operator orders publication and the built page passes 1-4 plus a leak
grep for `foste|watch/inbox|local_sovereign_agent|mag`, v1 ships as specified.
