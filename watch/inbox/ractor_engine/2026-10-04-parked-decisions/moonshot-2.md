# moonshot-2 lens - the two parked decisions (2026-10-04)

Lens: moonshot (no sacred cows; the 10x version; every swing grounded in one
organ). All reads and runs below are THIS sitting, cited path:line or
command:output. No em-dashes. Anything I could not verify is OWED.

Instruments run this sitting (exact commands):

1. `wc -l tools/dungeon.py mag/route_chat.py queue/STANDING_RAILS.md` ->
   771 / 273 / 53 (the ask's "756 lines" for dungeon.py is stale; the tree
   moved past the debt acceptance hours after it landed).
2. `./.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py -q -p no:cacheprovider` -> **15 passed
   in 0.95s**. The ask's "15 dungeon tests pass in under a second"
   REPRODUCES on this instrument (parser file alone = 13 tests; communication
   and operations ran that narrower instrument and read 13; suite-wide
   `-k dungeon` reads 16 per their receipts - name your denominator).
3. `./.venv/Scripts/python.exe -m pytest tests/test_route_chat.py
   tests/test_route_chat_banks.py tests/test_route_chat_depth.py
   tests/test_route_chat_fence.py -q` -> **15 passed in 2.20s**.
4. `./.venv/Scripts/python.exe tools/violation_ratchet.py check` (full tree)
   -> `scope=1405 files; hits=943; registered=942; NEW=1` + 8 GROWTH lines
   incl. `tools/dungeon.py accepted at 756 lines, now 771 (+15)` ->
   **RATCHET: FAIL** (see F5; every sibling lens read PASS/NEW=0 earlier).
5. `sed -n '1145,1160p' memory/runs/hermes_burn/usage.jsonl` -> line 1151
   byte-verified: GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003,
   z-ai/glm-5.3-prime, completion_tokens 16000, reasoning_tokens 15998,
   finish_reason "length", content_chars 1, cost_usd 0.2502604, ok true;
   line 1152 = STAGE_B re-fire, $0.2137336, finish stop, channel content.
6. `stat -c "%y %n"` on the refire trio (my own ordering, F3 below).
7. venv python census of memory/runs/route_chat/usage.jsonl -> 11 rows,
   **0 rows carry reasoning_tokens, 0 carry depth**.
8. Full read of tools/dungeon.py (all 771 lines), mag/route_chat.py (all
   273), queue/STANDING_RAILS.md (all 53), a06-sacred-cow.json,
   d4_thinking_probe.md, ds_workhorse.md, tests/test_dungeon_parser.py,
   tests/test_route_chat.py, tests/test_route_chat_depth.py (grep census),
   providers.yaml lane blocks (150-168, 215-230, 365-407),
   tools/hermes_burn.py:106-125, violation_baseline.json:5308-5316,
   PRIORS.md:20-30, the six sibling lens files, state/CURRENT.md (head).

## DECISION 1 (D3) VERDICT: explicit-off, carrier-enforced, CLOSED-LOOP

**The default thinking posture for arm-2/short-output asks: an explicit
`thinking:{type:disabled}` on the wire for every depth=mechanical ask, sent
by the carrier (route_chat, ds_workhorse, hermes_burn); the per-lane
providers.yaml flag is the capability cache, written from measurement,
defaulting to SEND on thinking-capable families; depth=design is the only ON
door and requires max_tokens >= 32000; omission is named in law as never a
posture; and the off state is VERIFIED from the response, not assumed from
the request: every route_chat row banks `depth` and `reasoning_tokens`**

The sharpening no other lens banked: the estate already measured the third
failure mode. configs/providers.yaml:219-223 (openrouter lane comment,
"verified by raw probe 2026-08-24"): "openrouter/auto routes to reasoning
models (deepseek-v4-flash-0731) and IGNORES thinking:{type:disabled} - it
thinks anyway and eats small budgets (600 -> empty, 2000 -> content)". So:

- economics/logic's verdict (unconditional explicit-off) is NECESSARY but
  NOT SUFFICIENT: on an ignore lane the request byte is a no-op and the
  posture lies. Their falsifier (a lane 400-ing on the key) targets the
  wrong failure: the measured enemy is silent ignore, not rejection.
- communication/operations/accuracy's verdict (lane-config-gated, hold the
  landed shape) leaves the $0.46 burner unswitched: the nous lane
  (providers.yaml:150-168) carries NO disable_thinking flag, and
  tools/hermes_burn.py:112-117 (my read) sends exactly {model, messages,
  max_tokens} - no thinking key exists in the carrier that produced
  usage.jsonl:1151. Lane-config-gating is measured to fail exactly where
  the money burned.
- The measured core all lenses share (I re-read it, did not re-fire it):
  d4_thinking_probe.md:53-62 - omitted key = 70 reasoning chars / 18
  reasoning tokens on a one-word ask; disabled = 2 completion tokens, no
  reasoning block; enabled = 12 reasoning tokens (the sanity arm). $0.00007.
  usage.jsonl:1151 - 15998/16000 reasoning tokens at cap, content_chars 1,
  finish length, banked ok:true pre-gate (the substance gate at
  mag/route_chat.py:238-249 now banks that row ok:false).
  a06-sacred-cow.json row e6baa31db6c0 - arm 1 (cow-, 4 asks) 4/4 clean;
  arm 2 (cow2-, 10 asks) 2/10 ok:false content_chars=0 at exactly the
  16000 cap, 7/14 cap-pinned, 0-byte deliverables vs flash 22,835/25,825.
- The 3/28 arm proves BUDGET, not posture (F3 below): the estate has never
  banked a thinking-OFF batch score, so the OFF default rests on the cost
  asymmetry plus the ON failure class. That is sufficient for mechanical
  and must not be written as if a quality A/B existed.

The closed loop is what makes the verdict survive an ignore lane: bank
`depth` + `usage.completion_tokens_details.reasoning_tokens` per row at
mag/route_chat.py:242-249 (today: 11 rows, zero and zero - my census), and
treat a mechanical row with reasoning_tokens over a small fraction of the
completion budget as a posture violation surfaced by the substance gate.
Request keys set policy; response tokens verify it.

**Falsifier (any one flips or scopes the verdict):**
(a) a judged, repeated equal-budget A/B on a mechanical shape where the
thinking-ON arm renders full material non-inferior to OFF with zero hollow
rows (flips the default for that shape);
(b) a live re-run of d4_probe.py where the omitted arm returns
reasoning_tokens 0 (a vendor flipped the default; urgency drops, the
explicit byte stays);
(c) a funded lane measured 400-ing on `thinking:{type:disabled}` (that lane
moves to banked-suppression with posture:"suppressed" rows; explicit-first
survives everywhere else);
(d) the closed-loop census showing openrouter/auto now honors the key (the
219-223 comment is stale) - the response census demotes to logging; the
wire posture is unchanged.

**Losing law surfaces + exact amendment text (append-never-rewrite):**

1. PRIORS.md:25 row 8, status cell "STILL-VALID (byte-confirmed mechanism,
   never refire thinking-on)" - the ABSOLUTE clause loses (it is confirmed
   for mechanical and falsified as absolute by arm 1's 4/4 and the d4
   probe's arm-3 both-directions control). Append to the row:

   > POST-DATUM 2026-10-04 (ractor D3; watch/inbox/go_wave_20261004/
   > d4_thinking_probe.md; memory/runs/hermes_burn/usage.jsonl:1151): the
   > mechanism is confirmed cross-family (deepseek-v4-flash probe; glm
   > prime 15998/16000 reasoning tokens at cap, content_chars 1). Row 8's
   > scope: THINKING OFF is the SENT default for mechanical/short-output
   > asks - explicit thinking:{type:disabled} on the wire by the carrier;
   > omission is NOT the off state (3-arm probe). Thinking-on is legal ONLY
   > at depth="design" with max_tokens >= 32000. The off state is verified
   > from usage reasoning_tokens, not assumed (openrouter/auto was measured
   > ignoring the key, providers.yaml:219-223). "Never refire thinking-on"
   > downgrades to: never refire thinking-on without the explicit object
   > and the design-tier budget.

2. queue/STANDING_RAILS.md law 1 (the surface the brief pointed at carries
   no depth law at all - the law lives only in mag/route_chat.py:127-141
   and :204-213; a rails law that lives in a module docstring is one
   refactor from gone). One clause appended to law 1:

   > Depth-gated thinking: depth=mechanical sends
   > thinking:{type:disabled} on the wire for thinking-capable lanes;
   > omission is not the off state (d4 probe 2026-10-04); depth=design is
   > the only enabled path and budgets 32K+; usage rows bank depth +
   > reasoning_tokens so the posture is auditable.

3. watch/inbox/go_wave_20261004/ds_workhorse.md item 6, headline
   "uncapped, thinking-off, file-backed" - the thinking-off word is false
   (F3). Append:

   > ERRATUM 2026-10-04: the v3 refire (04:38:32Z) predates both the d4
   > probe (06:00:41Z) and the ds_workhorse explicit-key fix (06:11:38Z);
   > its ask() omitted the thinking key, and the probe measured omission =
   > ON. The arm rode thinking-ON; 3/28 vs 0/26 measures the token cap.
   > No thinking-OFF batch score exists in this estate as of this erratum.

4. tests/test_route_chat_depth.py:83-89, test_lane_without_flag_omits_
   thinking - the landed test PINS omission as the no-flag contract
   ("a lane with no disable_thinking flag must not grow a thinking key").
   This is the losing test surface: under the verdict, a thinking-capable
   lane without a measured suppression MUST grow the explicit key, and a
   lane with a measured suppression banks posture:"suppressed" instead of
   silently omitting. The test flips with the code or it enforces the bug.

One-sitting move (~75 min): (a) populate disable_thinking:true on the nous
lane in providers.yaml and wire the same key behind it in
tools/hermes_burn.py's body (~$0.001 probe leg first); (b) add depth +
reasoning_tokens to the route_chat _bank dict; (c) land the two law
amendments and the ds erratum; (d) flip the depth test's no-flag contract;
(e) rerun the 15 route_chat tests.

## DECISION 2 (dungeon) VERDICT: SPLIT NOW - one seam, and bury the dead generation

**Split the pure dice-law/rules layer of tools/dungeon.py verbatim into
tools/dungeon_rules.py with re-exports from tools.dungeon; delete the three
debris artifacts in the same sitting; re-point the golden-vector scanner;
re-accept the residual carrier by name at its new count. Pre-register the
second seam (SCENES/campaign) on the majority's own triggers.**

Reviewer-derivable reasoning, all read this sitting:

1. The file carries a DEAD GENERATION in one class body: `def play` at
   tools/dungeon.py:447-449 (S0+S1 only) is silently shadowed by the second
   `def play` at :727-731 (adds campaign on --full). A reader at :447
   believes --full is a no-op. Two engines, one namespace, no marker. (This
   half is CONVERGENT with dogfood F4, economics rider, communication -
   independently re-derived on my full read.)
2. The debris discovery rate on one full read is the split argument: four
   latent artifacts, three of them in the flow layer no test exercises:
   - :623 `if self.warden_hp <= 0 or self.persuades >= 2 or True:` - the
     `or True` makes the S1-loot condition always true (my find; no sibling
     lens read this line);
   - :211 `msg.get("content") or msg.get("reasoning") or ""` - the same
     dead fallback a06-sacred-cow#3 flagged in route_chat (vendor field is
     reasoning_content); lane 1 fixed it at mag/route_chat.py:231-235 and
     the fix did not propagate to the sibling carrier (my find);
   - :297 `self.ledger_audits = getattr(self, "ledger_audits", 0) + 1`
     re-initializes what __init__:156 already sets - the author no longer
     trusts the class's own init (minor, symptomatic);
   - the dead play() above. That is ~1 artifact per 190 lines in a file
     that grew +15 lines within hours of its debt acceptance (my ratchet
     run: GROWTH af1d7045681fee89, 756 -> 771; baseline entry
     configs/violation_baseline.json:5309-5316, accepted 2026-10-04 by
     go-wave-20261004-coordinator, rule file-too-long). Standing debt here
     is not parked; it re-stamps every wave (the hourly cron is a standing
     rail, STANDING_RAILS.md:32).
3. The seam is pre-cut and cheap to verify: the pure layer (strip_and_cap
   :103-108, TAG_RE :111, extract_tag :114-130, roll :133-134,
   check_golden :137-145, ROSTER/WARDEN/INITIATIVE/SCENES/REAL_SCROLLS
   :44-101 and :454-486, the I/O-free helpers _beat_outcome/_find_scroll/
   _phantom_count/_packs_str/_wyrm_regrowth/_mimic_wipe :497-563) lifts
   verbatim, and the replay net is green on MY instrument: 15 passed in
   0.95s (parser + burn-id). Importer census (my grep, pattern
   "tools.dungeon|tools import dungeon"): exactly two module importers,
   tests/test_burn_id_uniqueness.py and tests/test_dungeon_parser.py -
   re-exports keep both green untouched. The third consumer is NOT an
   importer: tools/prepush_golden_vector.py is a token scanner over
   dungeon.py SOURCE (header :2-43, DEFAULT_TARGET="tools/dungeon.py" at
   :43), so the split silently blinds it unless the sitting re-points
   DEFAULT_TARGET (or scans both files). No other lens named this break.
4. Honest cost, adopting economics's arithmetic: one seam does NOT clear
   the >400 rule (the carrier lands ~420-440 after the deletions); the
   carrier re-accepts by name at the NEW count, which is LOWER than
   today's 771. The split's return is not the ratchet line - it is that
   the churn-prone law layer becomes a stable importable module (the dice
   law as a library: any tool can grade a verdict stream under dungeon
   law), and the dead generation is buried instead of shadowing the live
   one.
5. Deletions riding the sitting (all net-negative lines): dead play()
   :447-449; the `or True` at :623 reduced to the unconditional S1-loot
   assignment with a one-line cause comment; the dead `reasoning` fallback
   at :211 corrected to reasoning_content (convergent with the a06#3 fix
   route_chat already landed).

**Falsifier:** the verbatim move cannot keep the replay harness green in
the sitting - 14/14 logged S4 verdicts byte-identical
(tests/test_dungeon_parser.py:119-169), the burn-id pair, the re-pointed
golden-vector scanner, and one `--dry` smoke - in which case `git checkout`
the move and re-accept the debt standing with the failure named (the
verdict is reversible by its own gate). Second-seam triggers (adopted from
the majority): a second collapse-class bug within 2 waves, or the next
substantive campaign edit landing.

## Findings

**F1 (D3 core, unique to this lens).** The estate's own config measured the
third failure mode: providers.yaml:219-223 records openrouter/auto ACCEPTING
and IGNORING thinking:{type:disabled} (raw probe 2026-08-24: "600 -> empty,
2000 -> content"), so explicit-off on the wire is necessary but not
sufficient - and the route_chat ledger cannot catch an ignore lane because
it banks neither reasoning_tokens nor depth (my census: 11 rows, 0 and 0).
Evidence: providers.yaml:219-223; mag/route_chat.py:242-249; my venv census
output above. Falsifier: a live census showing openrouter/auto now honors
the key (comment stale) demotes the closed loop to logging. Move (~20 min):
add `"depth": depth` and reasoning_tokens (from usage completion_tokens_
details) to the _bank dict + one assertion in the depth test.

**F2 (D3 core).** The founding hollow row is a cross-family DOUBLE BURN on
the one lane no law reaches: usage.jsonl:1151 banked content_chars 1 at the
16000 cap with 15998 reasoning tokens at $0.2503 (ok:true pre-gate), the
STAGE_B re-fire at :1152 cost another $0.2137 - $0.464 for one judgment -
and its carrier lane (nous, providers.yaml:150-168) carries no
disable_thinking flag while tools/hermes_burn.py:112-117 sends no thinking
key. Falsifier: evidence the nous lane already carries an off switch (I
read the block; it does not). Move (~15 min + $0.001): the lane flag +
carrier key behind one probe call.

**F3 (D3 evidence hygiene, CONVERGENT with the d4 receipt consequence 1 and
three sibling lenses; mtime ordering re-run by me).** The brief's premise
"the ds re-fire ran thinking-off uncapped and scored 3/28" is false on the
wire: my stat reads frontier_delta_results_v3.jsonl 04:38:32 <
d4_probe.py 06:00:41 < tools/ds_workhorse.py fix 06:11:38, and the d4 probe
measured omission = ON - so the refire rode thinking-ON and 3/28 vs 0/26
measures the CAP. The estate has never banked a thinking-OFF batch score.
Falsifier: a send-time wire log of the v3 batch showing a thinking object
(no such log exists; the batch predates the fix), or a post-erratum refire
(~$0.13) with materially unchanged output chars. Move (~10 min): one
erratum line in ds_workhorse.md item 6 (text under D3 amendment 3).

**F4 (D2 core, debris census unique to this lens except the dead play).**
One full read of the 771-line organ surfaced four latent artifacts at ~1
per 190 lines - dead shadowed play() (:447-449 vs :727-731), the always-true
`or True` gate (:623), the dead `msg.get("reasoning")` fallback (:211, the
exact class route_chat fixed at :231-235 this wave), and the getattr
re-init (:297) - three of them in the flow layer no test exercises, in a
file that grew past its same-day debt acceptance. Evidence: line cites
above; my ratchet GROWTH line; my 15-passed/0.95s net. Falsifier: a reader
re-derives that :623's condition is live (it is not - `or True` bounds it)
or that :211's fallback can fire on the vendor's field names (reasoning is
not one). Move: the split sitting (~90 min) per the D2 verdict.

**F5 (live gate state, unique to this sitting).** The full-tree ratchet is
RED right now: my run printed NEW=1, `NEW e71ef4422e755b5e file-too-long:
tools/social_rsi.py:578 - >400 lines`, RATCHET: FAIL - the social_rsi v0
build (HEAD commit 4c4fd2b0f) landed with no baseline entry, and every
sibling lens's earlier run read PASS/NEW=0 on scope 1404 vs my 1405. The
estate's newest landing broke its own gate between sibling runs and mine.
Evidence: my command output above. Falsifier: a fresh check printing NEW=0
(would mean a baseline entry landed in between). Move (~5 min): the
operator accepts social_rsi.py by name or splits it - independent of the
dungeon decision; do not bundle.

## Blind spots (honest)

- No live API probe this sitting: omission-default, the ignore measurement,
  and the $0.46 double burn are banked receipts I re-read, not probes I
  paid for. The closed-loop census move is untested against today's
  openrouter behavior; the 219-223 comment is from 2026-08-24 and may be
  stale (falsifier d).
- I did not recount the 14-row sacred-cow manifest
  (sacred_cow_thinking_on.jsonl) or the 3/28 judge tally; arm-2 counts rest
  on a06's byte-quotes plus the receipts.
- Whether z.ai/glm (the nous lane's model) accepts the top-level thinking
  key shape is unverified; the hermes wire fix's first leg is that probe.
  If GLM takes no such key, the flag defaulting to SEND on nous is wrong
  and the lane lands in banked-suppression instead.
- I read all 771 lines but ran no runtime dungeon smoke; the D2 falsifier
  names the instruments the split sitting must run, which I did not
  rehearse.
- mtime ordering is host-clock ordering; I re-ran the stat once and it
  matches the siblings' reads, but an out-of-band touch remains possible in
  principle.
- I read the six sibling lenses before finalizing; the dead-play and
  false-label findings are flagged CONVERGENT where another lens derived
  them first, and my remaining findings (openrouter ignore, or True, dead
  reasoning fallback, ledger blind spot, golden-vector break, ratchet FAIL)
  were derived from files no sibling reported reading in full.
