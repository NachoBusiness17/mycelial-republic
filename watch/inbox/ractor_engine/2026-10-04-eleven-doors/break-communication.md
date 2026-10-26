# break-communication - hostile second pass on the communication lens (2026-10-04)

Ask: byte-check the communication lens's evidence against the estate, verdict
each finding, add what it missed. Topic: the 24-wide dig's remaining build
doors and their reviser-ordered sequence. Laws honored: no em-dashes, every
claim cited as path:line or exact command output, unverifiable items marked
OWED. All checks below were run this sitting from the repo root with
`.venv/Scripts/python.exe`; no subprocess spawning beyond the shell itself.

## Verdicts

### F1 (door sequence reached git but no routing surface; GWAP next-doors line diverges from the reviser table; "11 remaining" is already 10): CONFIRMED

Every cite byte-checks:

- Commits (git show): bb0f34586 at 2026-10-04 12:23:16 -0400 (door 1),
  00cb15c77 at 12:39:31 -0400 (door 2, 16m15s later), dig receipt 0838e150e
  at 12:00:44 -0400.
- Tripwire re-run: `.venv/Scripts/python.exe -m pytest
  tests/test_arena_bench.py -q` -> 4 passed in 3.09s. Door 2 is landed and
  green, so the ask's "11 remaining" is 10.
- `.venv/Scripts/python.exe -m mag.shared_surface validate` -> exit 120,
  ok:false; unindexed_items (37 total) includes all four dig receipts:
  ARENA_BENCH_TRIPWIRE_20261004.md, GWAP_INDEPENDENT_COP_20261004.md,
  PRIMER_ADJACENT_24WIDE_20261004.md, PRIMER_ADJACENT_24WIDE_20261004_NUMBERS.md.
  INDEX.json is the contract surface (AGENTS.md boundary table; the validator
  itself flags the files), so falsifier leg 1 is dead.
- INDEX.json: 2,969 items; last row (append order; rows carry no date field,
  keys are class/path/purpose/sha256) = DRIFT_PATROL_20261004.md.
- state/CURRENT.md:8 "updated: 2026-10-04T09:30:00Z"; full 133-line grep for
  door terms returns one incidental prose hit ("env-door" at :87), zero door
  content.
- room.jsonl full scan (instrument: python line scan, term list:
  independent-cop / INDEPENDENT_COP / arena-bench / ARENA_BENCH /
  PRIMER_ADJACENT / 24-wide / 24 wide / bb0f34586 / 00cb15c77 / EG-20 /
  clippy-as-prober / night-cycle / checkpoint legs): 15,427 lines (grew +1
  since the lens's 15,426; alive to 2026-10-04T16:48:48Z), 3 hits, all
  non-door noise: lines 3758 and 3768 are a 2026-09-01 thread-cartographer
  reply containing the word "night-cycle" as a riddled label; line 14521 is
  the 2026-10-01 WAVE24 order ("going 24 wide"), a different, earlier
  24-wide. Zero door-sequence mentions confirmed.
- Divergence side-by-side: GWAP_INDEPENDENT_COP_20261004.md:82-83 lists
  "arena-bench, clippy-as-prober, night-cycle". The primer's own ranked
  order (PRIMER_ADJACENT_24WIDE_20261004.md:218-222) and table (:235-241)
  run cop -> arena-bench AND EG-20 -> night-cycle -> monoculture -> decay
  family (pheromone first, clippy third inside the family). The GWAP line
  drops EG-20 (primer :219, :237; the only door the dig carries with an
  effort figure attached at spec, ESTATE_GAP_DIG_20261004.md:79), hoists
  clippy-as-prober past its "same family schema" gate (primer :241), and
  also silently drops monoculture and pheromone-metabolism. Falsifier leg 2
  dead.
- ARENA_BENCH_TRIPWIRE_20261004.md:46-47 re-relays EG-20 ("the dig's only
  measured-effort item rides this instrument"): confirmed.

Two sharpenings the lens missed:

1. The blindness is wider than proved: memory/zknot/LATEST.md (the boot
   recap AGENTS.md orders every seat to read first) and queue/todo.md both
   grep zero for door content (only 10-03 ARENA DAY commit lines repeat in
   zknot). The sequence is invisible on every boot surface, not just
   CURRENT/room/INDEX.
2. The phrasing "no operator routing surface" is overbroad: the committed
   ARENA_BENCH receipt :3-6 quotes the operator's routing order for the
   remaining doors ("go" on the build order, then "actually ractor it out
   self steal then go", dwfrun-3b5af1ac, 8 lenses + 2 moonshots). The order
   IS banked in git; the defect is that no index or boot surface carries it
   forward and the one next-doors line that circulates (GWAP :82-83) is
   wrong against the reviser's own table. The lens's DOOR_LEDGER move
   stands, 15 min.

### F2 (door-1 counts byte-true at primary, relayed as 188 vs 196 with no census moments): CONFIRMED, falsifier dead by reconstruction

My censuses (instrument: json parse of memory/runs/gwap/arena-capability.jsonl,
append-only, seq-ordered, rows hash-chained row_sha256/prev_sha256):

- At the 613-row boundary (last ts 2026-10-04T16:09:39Z): VERIFIED_AGREE 119,
  CHALLENGE 204, DISPUTE 290, suspected_collusion 196, all 196 inside
  CHALLENGE, zero rows after the 16:23:16Z landing. Matches the lens census
  and GWAP receipt :49-51 byte for byte.
- At the 589-row boundary (the primer's census population, same file):
  VERIFIED_AGREE 115, CHALLENGE 196, DISPUTE 278, flagged 188, all inside
  CHALLENGE. Matches primer :106 byte for byte.

So both receipts are byte-true at their own moments and the lens's falsifier
(a same-moment pair making one receipt wrong) is disproven: the two censuses
read different row ranges of one append-only file. What survives is exactly
the relay defect the lens named: neither receipt stamps a census moment on
its flagship line, and the door-1 commit message carries "196 self-flagged
rows" with no denominator or moment at all. B2-216 violation in relay,
erratum owed.

New erratum the lens missed, filed as addition A1 below: the GWAP receipt's
own defect paragraph mixes the two moments in one sentence.

One scope note: the ledger is live. At my second read it held 618 rows (5
new, seq 614-618, ts 2026-10-04T17:05:30Z; verdicts now 120/205/293). The
lens's "zero rows after the landing" was moment-true and old-instrument-true,
but any future census must re-run and stamp (primer :287 already says so).

### F3 (attention.md read-blind at the boot surface): CONFIRMED, scope widened, but the lens's fix option A breaks a landed contract

Evidence all byte-checks:

- mag/context_pack.py:311-315 `_clip` returns `read_text()[:n]` (head clip);
  :687 `att = _clip(...attention.md, 600)`; :1005 `"attention_tail":
  att[:400]`. Boot packs ship the first 400 chars of the head.
- memory/attention.md (563 lines): :1-12 a 2026-10-04T03:00 session-record
  head, :13 the sentinel `<!-- attention:alerts-preserved-below -->`, :14-16
  onward the 2026-09-26 probe-alarm flood (mistral/cerebras), :526
  "[probe-alarm] provider_probe DOWN mlx-cluster,ollama,xai; QUOTA-DEAD nous
  (run 2026-10-04) -> memory/improve/provider_health/2026-10-04.json", tail
  :549-563 the 09:30 tip witness and 14:2x INSTANCE-GUARD alarms. The head
  clip ships the stale header plus flood; :526 never reaches a booting seat
  via context-pack. Confirmed.
- mag/daemon.py:91-98: "attention" is the daemon decision action with a
  daily cap (`_attention_over_cap`), not a reader of the file. Confirmed.

Falsifier resolved against narrowing, and wider than the lens proved:

- Second head-blind consumer found: mag/lanes.py:293 `"attention":
  _read("memory/attention.md", 3000)` where `_read` (:247-252) is a head
  `[:n]` clip. Lane packs get 3,000 head chars (7.5x the context-pack
  window) and still die inside the 09-26 flood, blind to :526.
- Whole-file readers exist but none on the boot path: mag/realign.py
  `parse_attention` (:150-165) reads the full text and extracts
  bracket-tagged alert lines with flood-collapse, but it backs
  `python main.py realign`, an operator-invoked surface gated on
  state/last_operator_visit.json (realign.py:1-16); mag/chronicle.py:17-19
  reads the whole file but parses session blocks. So "tail alerts never
  reach a booting seat" stands, and the carve-out is: an operator who runs
  realign does see collapsed alerts.

The break in the lens's move (see addition A3): "rotate newest alert to head
at write time" violates the landed region contract at mag/act.py:22-35
(2026-09-29, gala wave5 attention-channel lane): the head is the newest-first
RECORD FLOOD under whole-block byte-cap eviction, and the preserved alert
tail below the sentinel is never evicted precisely because head-side
eviction beheaded the 2026-09-26/09-28 patrol alerts before the contract
(act.py:27-31 names the biography.py prev[:40000] incident). Rotating alerts
into the head region re-arms that guillotine. Likewise "clear the 09-26
flood" has no sanctioned tool: tools/attention_dam.py `is_noise_block`
archives only session-record boilerplate; alert lines are signal and stay by
construction. The lawful fix is read-side only: context_pack (and lanes)
clip from the sentinel downward, or ship realign's collapsed alert list.

### F4 (republic.py append-only immutability): WEAKENED by transmission, not by bytes

The finding text arrived in the handoff truncated mid-sentence (cut at
"mag/republic.py:209-217 (save-time immutability guard). S"), so the claim
it serves is not in evidence and verdicting it would be fabrication. Its
cites do byte-check: republic.py:15-16 docstring (a retracted letter is
superseded_by another, never deleted or edited; house chain law enforced at
save time, the guard in code not prose), :114 `superseded_by ... set once,
by supersede(); never edited`, :209-217 AppendOnlyViolation guards (trail
prefix edit, supersession re-point, dangling superseder). Verdict: evidence
confirmed, finding unverifiable as passed; re-send the full text or re-derive
the claim in a follow-up lane.

## Additions (what the lens missed)

- A1. The GWAP receipt's defect paragraph mixes census moments in one
  sentence: ":15-16 196 suspected-collusion rows ... 188 of them demoting
  VERIFIED_AGREE to CHALLENGE". At the 613-row moment the demotion class is
  196, not 188: all 196 flagged rows carry agreement_score 1.0 (census this
  sitting), so every one was demoted from would-be VERIFIED_AGREE, and the
  scene-dedup count is 154 distinct scenes (also not 188). The 188 is the
  589-row moment's flag count bleeding into a 613-row sentence.
  Evidence: census outputs above. Falsifier: any flagged row with
  agreement_score below 1.0, or a distinct-scene count of 188; both
  measured, neither holds. Move: 10 min, one erratum block in the GWAP
  receipt stamping both moments (589 rows: 115/196/278, 188 flagged,
  ts-range to 16:09:39Z pre-landing census at 613) and correcting "188 of
  them demoting" to 196.
- A2. Door 1's fix is live in the banking path, not just claimed: the five
  post-landing rows (seq 614-618, ts 2026-10-04T17:05:30Z) carry the v3
  independent-cop markers, commit-bound qualifiers
  (commit=<hex>:s1:3:chatgpt), divergent intent-vs-report verbs (spoke vs
  checked on seq 614), and zero suspected_collusion flags. The old
  instrument's last row is seq 613 at 16:09:39Z; the fixed one resumed
  banking within ~42 minutes of the landing. Door-1 tests re-run green this
  sitting: `pytest tests/test_gwap_independent_cop_20261004.py -q` -> 9
  passed in 0.78s. Evidence: ledger census above. Falsifier: any post-landing
  row with free-form identical qualifiers or a self-flag; none in 614-618.
  Move: 0 min, cite this in the DOOR_LEDGER as live cure proof; the
  historical re-grade stays the operator decision the receipt :75-78 names.
- A3. The attention channel's fix must be read-side only (see F3): option A
  of the lens's move (rotate newest alert to head) re-arms the eviction
  guillotine on alerts, the exact 09-26/09-28 beheading the act.py:22-35
  contract cured; the dam cannot clear the flood (signal-by-default);
  context_pack.py:1005 and lanes.py:293 should clip from the sentinel.
  Evidence: mag/act.py:22-60, mag/context_pack.py:687/:1005,
  mag/lanes.py:247-252/:293, tools/attention_dam.py:113-130. Falsifier: an
  eviction path that spares alert blocks living in the head region;
  `evict_for_prepend` (act.py:47-60) evicts head-region blocks by cap
  regardless of content. Move: 20 min, one reader-side change (sentinel clip
  helper shipped to both consumers), plus the nous probe carried into any
  paid-dispatch door plan as the lens already ordered.
- A4. The judgment tier of the driving ladder reads dark in today's probe,
  the exact alert the boot blindness hides: memory/improve/provider_health/
  2026-10-04.json (ts 12:00:42Z) banks nous QUOTA-DEAD, xai DOWN, openai
  DEGRADED, mlx-cluster/ollama DOWN; alive: deepseek, groq, openrouter,
  together, nous_api. Nous primes are the funded judgment carrier and
  grok-4.7 rides xai (AGENTS.md driving ladder), so doors whose falsifiers
  need paid judgment dispatch (build-once calibrator's download-and-eval
  gate, judged weld-door arena runs) are carrier-gated today, which raises
  the EV-per-hour of carrier-independent doors (EG-20 column, night-cycle
  legs, monoculture proxy, clippy probes). Unresolved: which of nous vs
  nous_api the Hermes lane actually rides (the probe shows both keys with
  opposite statuses); one providers.yaml check OWED. Evidence: the JSON read
  this sitting. Falsifier: configs/providers.yaml mapping Hermes to
  nous_api with funded quota (then only xai is dark and this narrows).
  Move: 10 min, check the mapping, then one carrier-status line on the
  DOOR_LEDGER that the EV ranking cites.
- A5. shared_surface validate is red twice over, not once: exit 120, ok:false.
  Indexing the four dig receipts cures the warning class only; the errors
  list carries NEW event-kind rows in LINKS.jsonl (lines 389-391+, ids
  SCOUT-JBR001 / SCOUT-DC-SECRECY / SCOUT-ORIGAMI-MATH, writer
  free-resource-scout), a hard-fail class the error text says belongs in
  watch/inbox/EVENTS.jsonl via mag.link_library.load_events past the B2-28
  marker. Also: ESTATE_GAP_DIG_20261004.md itself is in the unindexed 37,
  so the EG-20 spec is invisible to the same contract the doors depend on.
  Evidence: validate JSON this sitting. Falsifier: validator exit 0 after
  indexing the receipts alone; it will not clear the LINKS errors. Move:
  +15 min on top of the lens's move, relocate the SCOUT rows per the
  error's own instruction or grandfather them by name under the B2-28 rule.
- A6. "EG-20, the only measured effort" is a characterization, not a byte:
  ESTATE_GAP_DIG_20261004.md:79 carries plain "2h" in an effort column whose
  rows 3 (2h), 7 (2h), and 12 (20 min) carry the same shape with no
  measured-vs-estimated mark anywhere in the table; primer :219/:237's
  "only measured figure" is the reviser's gloss relayed as fact.
  Evidence: the table read this sitting. Falsifier: ESTATE_GAPS_20261004.json
  marking the figure measured (not opened this sitting, OWED). Move: 2 min,
  the DOOR_LEDGER line should read "2h at spec (measured status per primer,
  unmarked in the spec table)".

## Blind-spot resolutions (against the lens's own honesty list)

1. Operator GO primary outside the tree: still OWED, and widened: a second
   operator order (ARENA_BENCH :3-6, "go" then "actually ractor it out self
   steal then go") also has no in-tree primary beyond the receipt quote.
2. The 529-payload new-instrument measurement: not re-run here either
   (it is an effectful backfill over playground run dirs; skipped
   deliberately); A2's five live v3 rows are independent partial evidence
   the new instrument mints the claimed shape.
3. Attention consumer classification: resolved, see F3 (grep over mag/ +
   tools/ *.py, non-test; every consumer named with its read semantics).
4. ESTATE_GAP_DIG EG-20 spec and provider_health JSON: both read this
   sitting (see F1 and A4/A6).
5. validate capture: full JSON parsed, exit code 120 recorded (see A5).
6. Confirmer structured rows: still unlocated; the primer itself admits the
   gap at :253 and :291. Unchanged, OWED.

## Instruments run this sitting

- git show -s --format for bb0f34586 / 00cb15c77 / 0838e150e (times above).
- pytest tests/test_arena_bench.py -q -> 4 passed in 3.09s.
- pytest tests/test_gwap_independent_cop_20261004.py -q -> 9 passed in 0.78s.
- python -m mag.shared_surface validate -> exit 120, ok:false, 37 unindexed,
  LINKS.jsonl errors (full JSON parsed, not tail-captured).
- python json censuses: INDEX.json (2,969 items, last row DRIFT_PATROL);
  room.jsonl (15,427 lines, full term scan); arena-capability.jsonl (613
  and 618 rows, verdict/flag/ts/scene censuses at the 589/613/618
  boundaries); attention.md structure (563 lines); provider_health JSON.
- Code reads: context_pack.py:311-315/:687/:1005, daemon.py:85-100,
  act.py:18-60/:160-175, lanes.py:247-252/:288-296, realign.py:1-30/:145-165,
  chronicle.py:12-19/:115-128, biography.py:370-382, seats.py:383-393,
  tangent.py:284-296, token_economy.py:44-56, attention_dam.py:85-130,
  republic.py:10-20/:108-120/:205-220, ESTATE_GAP_DIG_20261004.md:55-90,
  CURRENT.md (full), zknot/LATEST.md + queue/todo.md (door grep).

## OWED

- F4's full finding text (truncated in the handoff).
- The operator GO primary bytes (both orders) in the session transcript
  store outside the tree.
- nous vs nous_api mapping in configs/providers.yaml (gates A4's strength).
- ESTATE_GAPS_20261004.json check for a measured-mark on EG-20's 2h (A6).
- The 529-payload re-run (effectful; skipped by this pass by design).

Writer: break-communication (hostile second pass, ractor_engine
2026-10-04-eleven-doors). No em-dashes. No files edited outside this receipt.
