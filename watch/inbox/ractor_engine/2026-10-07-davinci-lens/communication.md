# Communication lens - da Vinci lens ractor, 2026-10-07 refire (relay audit)

- Jacket: the relay that lost the signal. I audit what actually reached the
  operator versus what the receipts claim was communicated: report contracts,
  alert channels, decision counts relayed by content not by key census.
- Moment: 2026-10-06 ~23:40 EDT (2026-10-07 ~03:40Z). Run: dwfrun-176a6b3b-4e7a-4b7e-b1a0-ed3c89e2de0b
  (this seat's own session id, matched against .zcode/workflow-runs/).
- This is the third jacket pass in this lens family on ractor runs: 10-02
  (ractor-topic fire 1), 10-06 19:58 ET second pass (ractor-topic fire 2), now.
  The 2026-10-05 Amenti pass (watch/inbox/ractor_engine/2026-10-05-amenti-diff/communication.md)
  is the direct precedent for the X-facing artifact this order builds.
- Laws held: every claim cites bytes read or commands run this sitting; absence
  claims name instrument and scope (quantifier law); no em-dashes, no en-dashes;
  nothing I could not verify is asserted (OWED otherwise); every "still true" is
  true only at my moment (B2-216 applied to relay state).

## Checks run (exact commands/reads, this session)

1. state/CURRENT.md read in full (89 lines): zero occurrences of
   leonardo/davinci/vaultmother (read, not grep).
2. Census: `grep -rli "leonardo\|vaultmother" watch/inbox --include="*.md"`
   returned exactly 5 files, all Amenti-era: AMENTI_TRANSLATION_20261005.md,
   BABEL_FISH_LILITH_THREAD_20261005.md, ractor_engine/2026-10-05-amenti-diff/
   {break-operations,communication,operations}.md. No da Vinci receipt existed
   at census moment. `grep -ic` on memory/attention.md, memory/zknot/LATEST.md,
   queue/todo.md: 0, 0, 0. `grep -ric ... state/*.md`: 0 hits on every file
   (the non-zero filter printed nothing). jsonl/json scoped grep over
   watch/inbox: 0 hits.
3. Killed-fire census: `grep -il "leonardo\|da vinci\|vaultmother"
   watch/inbox/ractor_engine/ractor-topic/*.md` returned EMPTY (zero of the 25
   .md files mention the topic the order names).
4. Script read: .zcode/workflows/ractor-engine.dwf.ts:85 (SLUG default),
   :86 (OUT path), :143 (log line), :149 and :159 (String(args.topic)
   interpolation into lens and breaker asks). Script mtime 2026-10-05 20:53:
   unchanged across all three fires.
5. Run journals: `grep -o '"topic":[^,]*'` and `grep -o '"slug":"[^"]*"'` over
   .zcode/workflow-runs/*.mjs; `grep -l "OPERATOR ORDER" .zcode/workflow-runs/*.mjs`
   returned exactly 2: dwfrun-c21d18c2-435d-4a8e-b6a4-df40f66b4955.mjs and
   dwfrun-176a6b3b (mine). Journal mtimes and slug/topic values per finding.
6. Gate rows: memory/workflows/REGISTRY.jsonl greps for
   '"name": "ractor-engine.dwf.ts"' (19 rows, ts list pulled); full G1-G8 check
   arrays byte-read from the tail rows; the 2026-10-06T22:29:05Z row reads
   verdict PASS.
7. Phantom digit: `grep -n "405,100,237,137|405100237137|erratum|ERRATUM"`
   over ractor-topic/accuracy.md hit :86 and :157; truth read at
   dashboard/data/ESTATE_INDEX.pointer.json:7 ("walk_bytes": 140510023713).
8. Sibling receipt read: watch/inbox/ractor_engine/2026-10-07-davinci-lens/accuracy.md
   head (this fire's accuracy lane, landed mid-sitting), including its door
   probes and the trigger URL carry.
9. NOT RUN: ListWorkflowRuns (capability gap: "workflow_introspection_unavailable:
   this session cannot read workflow runs"). Run lifecycle states reconstructed
   from on-disk journals instead. The settings-only-amend args-loss bug itself
   was not reproduced by me (no amend path exercised); I byte-verified only its
   downstream fingerprints.

## FINDING 1 (headline): a lost topic arg became misdirected fleet work because the ractor engine fails open, and the receipts now claim a complete relay for a topic the operator never posed

The engine coerces a missing topic instead of refusing it:
ractor-engine.dwf.ts:85 defaults the bank slug to "ractor-topic"
(`String(args.slug || "ractor-" + String(args.topic || "topic").slice(0, 24)...)`)
and :149/:159 interpolate `String(args.topic)`, which is the literal string
"undefined" when the arg is gone, into every lens and breaker ask. The killed
fires ran the full fleet on that string: their own receipts carry it
(watch/inbox/ractor_engine/ractor-topic/accuracy.md:2-3 "Topic arg arrived
undefined, so the lens rode its standing beat"; the 10-02 fire's pass said the
same at ractor-topic/communication.md:3; SYNTHESIS.md:11 names it "an engine
input defect a prior run named and nothing fixed"). My census (check 3) reads
ZERO leonardo/da vinci/vaultmother hits across all 25 ractor-topic .md files:
roughly seven hours of lens, hostile-pass, and synthesis output banked into a
folder a future reader will index as legitimate topic work, with the loss
recorded only in scattered footnotes. The signal was lost and the receipts
communicate as if it arrived.
Falsifier: any leonardo/vaultmother content in ractor-topic/*.md (instrument:
check 3), or a fail-closed topic gate anywhere in ractor-engine.dwf.ts (I read
:85, :143, :149, :159; the run proceeds to spawn on a missing topic).
Move: add a fail-closed gate at the top of the run body (throw, or log plus an
error conclusion, when args.topic is absent or the string "undefined"), then
amend the saved workflow so reruns inherit it. About 10 minutes.

## FINDING 2: the relay inverted - the fire whose args survived landed nothing, the fires whose args died banked the most, and the order text still has no inbox-grade home

Journal dwfrun-c21d18c2-435d-4a8e-b6a4-df40f66b4955.mjs (mtime 2026-10-06
19:36) carries slug "2026-10-06-davinci-lens" and the full topic text
("OPERATOR ORDER (2026-10-06): grab everything we can from Leo..."), yet
watch/inbox/ractor_engine/2026-10-06-davinci-lens/ does not exist (ls of
ractor_engine/ at open and recheck at close: only 2026-10-07-davinci-lens and
ractor-topic match "davinci"). So fire 1: signal intact, zero banked
deliverable. Fires 2 (journal dwfrun-d96545c9-d216-4295-b3d5-d7496dceb3fe.mjs,
mtime 19:38, contains "ractor-engine" but no slug and no topic key,
byte-consistent with an args-less refire two minutes after fire 1's journal
stopped): no signal, ~25 receipt files banked. Meanwhile the order text's only
durable carriers before this fire's lenses started landing were one three-line
composition bullet (watch/inbox/ROLL_SHAPE_TURING_CASTLE_20261007.md:55-57,
which names the ractor but not the order's content) and the run journals
themselves, whose retention policy I did not find (OWED). The trigger URL
x.com/TheVaultMother/status/2062263185814499652 reached the inbox only when
this fire's sibling accuracy lane banked (2026-10-07-davinci-lens/accuracy.md,
door census section).
Falsifier: a 2026-10-06-davinci-lens folder under another root, or a pre-fire
watch/inbox receipt carrying the order text (instruments: check 2's greps and
the ls census; scope: watch/inbox md/jsonl/json, memory/attention.md,
memory/zknot/LATEST.md, queue/todo.md, state/*.md).
Move: bank the operator order verbatim as
watch/inbox/OPERATOR_ORDER_DAVINCI_20261007.md (ask text, trigger URL, tri-state
examples, verified doors) so any future fire reconstructs intent from the inbox,
and salvage fire 1's journal report() rows if any exist. About 20 minutes.

## FINDING 3: the workflow gate certifies run shape, not signal, so its PASS rows cannot distinguish an order-carrying fire from an "undefined"-topic fire

The ractor rows in memory/workflows/REGISTRY.jsonl (19 rows named
ractor-engine.dwf.ts; the 2026-10-06T22:29:05Z row reads verdict PASS, byte-read
this sitting) certify exactly G1-G8: multiplicity, pass-off, steering, salvage,
deliverable, receipts, laws-in-asks, width shape. None of the eight inspects
args integrity, and the row's only fingerprint is the script digest (identical
across fires; the script did not change, mtime 2026-10-05 20:53). A gate row is
therefore byte-equivalent in decision content for fire 1 (order intact) and the
args-lost fires: the "every check registers a row" contract counted the fires
without carrying what they were about. Decision counts relayed by key census,
not by content: the exact genre this lens exists to catch.
Falsifier: a REGISTRY row field or gate check encoding topic/args presence (my
instrument: the full row JSON read in the tail pulls and the G1-G8 arrays).
Move: add a ninth gate check ("topic arg present and not the string
undefined") plus a scenario card, run
`python tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios`
after the gate change. About 30-45 minutes.

## FINDING 4: corrections ride outside the artifact they correct, so the phantom digit survives in the copy an operator actually reads

ractor-topic/accuracy.md:86 and :157 still print walk_bytes as
1,405,100,237,137 (my grep, this sitting), while the pointer truth is
140510023713 (dashboard/data/ESTATE_INDEX.pointer.json:7): exactly 10x. The
conviction lives in a different file (ractor-topic/SYNTHESIS.md:17, "shipped a
10x phantom digit inside its own evidence") and accuracy.md's own hedge
(:84-86, "asserted, not checked") never received the erratum: the file's mtime
(Oct 6 19:54) predates its hostile pass (break-accuracy.md, 21:12). A reader of
accuracy.md alone inherits a 10x number flagged only as unverified. The
publish-time re-derivation law minted from this lens family
(state/CURRENT.md:55-56) has no mechanism at the artifact; the hostile pass
runs after, in parallel files.
Falsifier: accuracy.md amended with an erratum after my read moment, or the
pointer value itself wrong (then the correction inverts and break-accuracy
needs the erratum).
Move: append an ERRATUM row to ractor-topic/accuracy.md giving the corrected
walk_bytes (140,510,023,713 per pointer:7) and naming break-accuracy plus
SYNTHESIS.md:17 as the instruments. About 5 minutes.

## FINDING 5: the downstream relay shape to TheVaultMother is proven and this fire is riding it; the two source doors that cannot answer tonight are exactly the two the receipts now name

The Amenti pass set the contract this order needs: her register on the surface,
substrate tri-state underneath, declines named (AMENTI_TRANSLATION_20261005.md
sections 2, 4, 5: REAL TERM / MODERN 1930s-40s / unmeasured, and "Lines held").
It also fixed the method for an unfetchable source: "her posted system parsed
from the operator-supplied briefing (primary posts listed there); substrate
verified by search" (:4). This fire's sibling receipt shows the same method is
required again: its curl of the trigger URL returns HTTP 200 but a React app
shell with zero thread text, and both archive.org Richter doors read 503 with
the metadata API answering "Internet Archive: Temporarily Offline"
(2026-10-07-davinci-lens/accuracy.md, instruments section; its own runs, named
as such, not re-run by me). So the thread text and the archive.org volumes are
operator-briefing-gated tonight, while the Gutenberg door is live (sibling's
probe: 200 with pg5000.txt sha256 83e79e10..., 1,433,832 bytes). The relay
finding: the channel that failed twice is upstream (args); the channel that
works (receipt in her register with lines held) has a landed precedent and is
already carrying the trigger URL durably.
Falsifier: an X fetch path returning thread text from the status URL (the
app-shell result holds at the sibling's moment), or archive.org recovering
tonight (then the kit's archive doors flip to fetchable and this finding
narrows to the X shell only).
Move: carry the Amenti method clause and the lines-held section into the lens
card's voice protocol verbatim, so the build treats operator-supplied thread
text as the parse source and independent verification as the substrate law.
About 5 minutes.

## Blind spots (this lens's own)

- No read-receipt instrument exists anywhere I searched: I verify byte
  surfaces, never consumption. A channel that is clean but unread looks
  identical to me to one that is dirty and unread.
- ListWorkflowRuns is unavailable in this session (capability gap, quoted in
  checks): fire lifecycle causes (stopped vs superseded vs provider-stopped)
  are inferred from journal mtimes and slug/topic fingerprints, not from the
  run journal API. The fire count and exact sequence are partially inferred;
  dwfrun-8cd5a845 (mtime 19:21, no ractor-engine reference) I could not
  classify at all.
- I did not reproduce the settings-only-amend args-loss bug; its mechanism is
  the run frame's account. What I byte-verified is the downstream fingerprint
  (slug default, "undefined" in receipts, zero topic content in outputs).
- Retention of .zcode/workflow-runs/ is unknown; if journals prune, finding 2's
  durability claim about the order text weakens to the ROLL_SHAPE bullet only.
- The sibling accuracy.md's door probes and Gutenberg hash are cited as that
  lane's instruments (named as such); I did not re-run the fetch or the hash.
- My own fire's gate row is presumed to be the 22:29:05Z PASS row but the row
  carries no args fingerprint to prove it (that is finding 3's point).
- I read relay surfaces only; the lens deliverables themselves (lens card,
  source kit, rebuild manifest) are sibling lanes' outputs and I do not
  adjudicate their Leonardo content.

## ERRATUM (2026-10-07, appended after the hostile second pass verdicted F1 weakened)

Two quantities in FINDING 1 were wrong; the mechanism stands. (a) "25 .md
files" is corrected to 23: `ls watch/inbox/ractor_engine/ractor-topic/*.md |
wc -l` reads 23 this sitting (20 touched during the Oct-6 sitting, 3 are
10-02-era files). (b) "roughly seven hours" is withdrawn: it was inferred from
the 22:29:05Z gate-row timestamp, a row I had already flagged as unattributable
to a specific fire in Blind spots. The byte-backed window: first Oct-6 receipt
touch 19:53:14 (accuracy_20261002_nightclose.md, the rename/touch moment), last
23:26:12 (SYNTHESIS.md) = 3h32m58s of banked output; the args-lost fire ran
from journal birth 19:38:00 (stat birth=mtime byte-read on
dwfrun-d96545c9-d216-4295-b3d5-d7496dceb3fe.mjs; fire 1's journal
dwfrun-c21d18c2 born 19:36:50) to that last receipt, about 3h48m. The census
datum survives re-run this sitting: `grep -il "leonardo\|da vinci\|vaultmother"
watch/inbox/ractor_engine/ractor-topic/*.md` returns zero of 23. The
fail-open mechanism stands with an added instrument: `grep -n "throw\|
!args\.topic\|args\.topic ===" .zcode/workflows/ractor-engine.dwf.ts` returns
only "207: throw e;" (an unrelated error re-throw), so no topic gate exists.
Move unchanged. Instruments: the commands in this paragraph, run 2026-10-07
this sitting.

## OWED (unverified, not asserted)

Fire 1's journal salvage (whether any report() rows landed before it died);
REGISTRY retention and whether the 18:53:21Z ractor row's verdict differs from
PASS; journal retention policy; whether any non-.md inbox surface (pdf, html)
carries the order; the exact mechanism line of the amend bug in the harness
(outside this repo's bytes I can read).
