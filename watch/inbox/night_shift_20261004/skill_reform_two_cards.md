# SKILL REFORM TWO CARDS - 2026-10-04 night shift (free lane, $0)

Seat: zcode GLM-5.3 night window. Task: apply the five stolen card rules
(receipt `watch/inbox/IMAGE_BLASTER_GO_20261003.md` door 2; template
`.agents/skills/image-blast/SKILL.md`) to two of the three offenders the lane
named: agent-harness (the designated ask-template source; zero runnable
commands before) and frontier-mine (nearest to the winning shape already).

The five rules, applied: argument surface (argument-hint frontmatter); one
verb + one runnable command; gates in card text; final-response line; card
cap (both cards stay well under 100 lines; doctrine substance preserved -
nothing deleted except two em-dash characters, see card A). Plain hyphens
throughout; zero em-dashes remain in either card. Working tree only, NOT
committed.

## Card A: .agents/skills/agent-harness/SKILL.md

Counts (wc -l / wc -w): before 51 lines / 510 words -> after 80 lines /
788 words. `git diff --numstat`: 31 added / 2 deleted; the 2 deletions are
the em-dash rewrites of the frontmatter description and the H1 (same words,
dashes swapped to plain hyphens per the estate no-em-dash law), so 29 lines
are pure additions.

What was added and why:

- argument-hint: `<pasted-item | item-URL> [slug]` - the loop's input is one
  pasted item; the slug names the card file.
- One verb made explicit: SCORE - one pasted intake item end-to-end (sweep,
  5-axis score, dogfood tests 1+4, verdict card, typed room row, driver
  wire) in the SAME TURN, with a concrete trigger contract: fires when the
  operator pastes an item or an ask names exactly one item to judge; no
  paste, no score; never scores from the paste's own description of itself.
- THE one runnable invocation: the typed intake room-row append to
  `watch/room.jsonl` via the repo interpreter. Why this command: the
  harness loop is procedural - the repo has no rubric-scorer entrypoint
  (`main.py` subcommand list has no intake/room verb; grep over mag/ +
  tools/ finds only topic-index regexes for the band names), and the room
  row is the loop's only mechanical step: the claim-contention lock's
  public half and the driver's pull wire (watch/INTAKE_RUBRIC_20260903.md
  gopher loop steps 4-5, thread "intake"). Byte-tested 2026-10-04 against
  a temp file (`watch/_smoke_row.jsonl`, deleted after): written row parses
  as JSON and matches the live intake-thread row shape
  (ts/thread/seat/type/item/score/file/gist). No test row was written to
  the live room.
- Gate line in card text: GATES - (1) claim-contention lock (one card, one
  live builder; second same-card launch BLOCKED until the first returns or
  fails); (2) only operator gates defer (keys, spend, judgment); premium or
  paid judgment pass waits for the operator's in-chat go.
- Final response line: verdict card fields, card path + room-row ts as
  written, wire status (dropped to `queue/handoff/zcode/OUTBOX/` for BUILD
  NOW or held with the named gate). OUTBOX path verified on disk.
- Ask-template role made explicit: spawn prompts build from the rubric's
  self-contained-prompt law (Amendment 1, point 3); the card plus that
  receipt ARE the template - no freelanced ask shapes.

Exact added lines (verbatim from `git diff`, pure-new only; the description
and H1 rewrites repeat their old text with hyphens and are not quoted):

```text
argument-hint: <pasted-item | item-URL> [slug]
## The one verb: SCORE (trigger + the one runnable command)
- VERB: score ONE pasted intake item end-to-end - sweep, 5-axis score, dogfood
  tests 1+4, verdict card, typed room row, driver wire - in the SAME TURN.
- TRIGGER CONTRACT: fires when the operator pastes an item (or an ask names
  exactly one intake item to judge). No paste, no score; this card never
  freelances items to judge and never scores from the paste's own description.
- THE one runnable invocation (the loop's only mechanical step; the typed row
  is the contention lock's public half AND the driver's pull wire; byte-tested
  2026-10-04 - row parses, shape matches the live intake thread):

```bash
.venv/Scripts/python.exe -c "import json,datetime; row={'ts':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'thread':'intake','seat':'card-worker','type':'card','item':'<ITEM>','score':'<F:x P:x C:x W:x N:x = xx/25 BAND>','file':'watch/INTAKE_<slug>_<date>.md','gist':'<one-line gist>'}; open('watch/room.jsonl','a',encoding='utf-8').write(json.dumps(row,ensure_ascii=False)+chr(10))"
```

  The card file this row names must already exist on disk before the row is
  written (receipt-at-bytes below). Ask-template source: spawn prompts are
  built from the rubric's self-contained-prompt law (Amendment 1, point 3);
  this card plus that receipt ARE the template - no freelanced ask shapes.
- GATES: (1) claim-contention lock - one card, one live builder; a second
  same-card launch is BLOCKED until the first returns or fails. (2) Only
  operator gates defer (keys, spend, judgment); any premium or paid judgment
  pass waits for the operator's in-chat go before it fires.
Final response: the verdict card fields (NAME / SCORE F:x P:x C:x W:x N:x = xx/25 +
band / VERDICT + tri-state / DOGFOOD / FILED), the card path and room-row ts exactly
as written, and the wire status - dropped to `queue/handoff/zcode/OUTBOX/` for BUILD
NOW, or held with the named operator gate.
```

## Card B: .agents/skills/frontier-mine/SKILL.md

Counts: before 53 lines / 356 words -> after 68 lines / 480 words.
`git diff --numstat`: 15 added / 0 deleted. This card already had the one
verb + one runnable invocation (CreateWorkflow saved olm-mine, digest
2487787e949f gated) and carried the shared laws; only the three missing
rule surfaces were added:

- argument-hint: `<today YYYY-MM-DD>` - the slug arg the saved workflow
  demands (callers know the date; replayable scripts cannot read clocks).
- Burn gate (hard) in card text: the 10:00 cron firing is the standing burn
  order and needs no confirm; any OTHER firing - manual refire, off-cadence
  run, or a gala ball off the steal-map - waits for the operator's in-chat
  confirmation naming the slug. AmendWorkflow resume of an errored run is
  NOT a burn (finished steps replay from cache at zero tokens) and needs no
  gate; a blind refire where an amend would do stays banned (existing
  failure law).
- Final response line: digest receipt path, top-12 steal-map (find ->
  organ -> one falsifiable probe), fired vs held at the burn gate and why,
  banked LINKS row plus handoff line.

Exact added lines (verbatim from `git diff`):

```text
argument-hint: <today YYYY-MM-DD>
## Burn gate (hard)

The 10:00 cron firing is the standing burn order - unattended, no confirm
needed. Any OTHER firing of this card waits for the operator's in-chat
confirmation naming the slug: a manual refire, an off-cadence run, or a gala
ball off the steal-map. AmendWorkflow resume of an errored run is NOT a burn
(finished steps replay from cache at zero tokens) and needs no gate; a blind
refire where an amend would do is banned outright (failure law below).
Final response: the digest receipt path under `watch/inbox/frontier_olm_<slug>/`,
the top-12 steal-map (find -> estate organ -> one falsifiable probe each), what
fired vs what the burn gate held (and why), and the banked LINKS row plus the
handoff line.
```

## Verification

- Free lane: no paid organs fired; `.venv\Scripts\python.exe` used for the
  one byte-test (temp file, cleaned); never bare python.
- Zero em-dashes in both cards after reform (`grep -c` = 0 each).
- Paths named in new card lines verified on disk: `queue/handoff/zcode/OUTBOX`,
  `watch/room.jsonl`, `watch/INTAKE_RUBRIC_20260903.md`,
  `watch/inbox/frontier_olm_20260928/DIGEST.md`,
  `watch/inbox/48h_synth/ERRATA.md`.
- Both cards under the ~100-line cap (80 and 68); all pre-existing doctrine
  text byte-preserved except the two dash characters.
- Not committed; the third offender (operator-corrections, 403 lines, split
  into one-verb cards) remains owed as the lane receipt named it.
