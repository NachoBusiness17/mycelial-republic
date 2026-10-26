# dogfood.md - da Vinci lens ractor, dogfood lane (2026-10-07 refire, args intact)

Lens: dogfood (organ mapper). Jacket: the finding filed but never wired. The topic
arrived intact this fire (my ask carries the full operator order: the TheVaultMother
Leonardo lens, the source kit manifest, the rebuild manifest, kill criteria), which is
itself the behavioral proof that the refire path carries args where the two dead fires
did not. Moment of run: 2026-10-07 ~00:00-00:45Z sitting, tree shared and moving, all
counts moment-stamped with their instruments per B2-216. Organ map: F1 gala/engine,
F2 librarian, F3 percolator/law pack, F4 context pack (the lens library), F5 attention
market plus the off-estate transport no MCP bridge covers. Everything below was
checked THIS sitting by a named command or file read; anything not checked is marked
OWED. The accuracy lane's same-sitting file
(watch/inbox/ractor_engine/2026-10-07-davinci-lens/accuracy.md) is used CONVERGENT
where noted: duplication is emphasis, and I say which runs are mine and which are its.

## F1. Two fires died on the args-loss bug; the receipts are filed and the engine still accepts an undefined topic (gala/engine organ). CONVERGENT with ractor-topic/dogfood.md.

Evidence:
- The receipts are filed: watch/inbox/ractor_engine/ractor-topic/dogfood.md:3-4 opens
  "Topic arg: `undefined` (the engine passed no topic; same as the 2026-10-02 run",
  and watch/inbox/ractor_engine/2026-10-07-davinci-lens/accuracy.md:3-5 re-records
  the loss for the prior fire of THIS order.
- The engine bytes are intact and unguarded: .zcode/workflows/ractor-engine.dwf.ts:85
  builds SLUG from `args.topic || "topic"`, so an undefined topic silently renames the
  run, and .zcode/workflows/ractor-engine.dwf.ts:140-143 selects lenses and logs
  "Riding N lenses on: " + String(args.topic) with no fail-closed topic check. The
  topic arg is declared at .zcode/workflows/ractor-engine.dwf.ts:29.
- The gate has no teeth for it either: `grep -n -i "topic" tools/workflow_gate.py`
  returned no hits this sitting, and configs/workflow_gate_scenarios/ holds the nine
  G1-G8 cards with no topic-shaped card among them (ls output this sitting).
- The fix shipped as a procedural refire, not a structural guard: this run's script
  mtime is Oct 5 20:53 (ls in .zcode/workflows/), before the dead fires, so nothing
  in the engine changed between the fires that lost args and the refire that carried
  them.

Falsifier: a topic-present guard in the script's arg-parse site, or a gate scenario
card that fails an empty-topic ractor script. Move (10 min): refuse to phase() when
String(args.topic) is empty or "undefined", plus one scenario card, so the third
args-loss dies at the door instead of burning two fires first.

## F2. The kit's founding primary is banked in the shared inbox and invisible to the librarian; the only "davinci" the catalog knows is an OpenAI model name (librarian organ). CONVERGENT with accuracy.md F1's false-anchor finding, independently derived here.

Evidence:
- The primary landed this sitting at
  watch/inbox/ractor_engine/2026-10-07-davinci-lens/_checks/pg5000.txt (1433832 bytes,
  sha256 pinned at accuracy.md:20). I re-read the anchors myself: `grep -n "Giacomo
  came to live|Thief, liar, obstinate"` on that file returned pg5000.txt:30302 and
  pg5000.txt:30310 (the Salai household entry and the thief line).
- Catalog blindness, instrument and scope: `grep -c 'pg5000' catalog/catalog.jsonl`
  returned 0 over the full file (wc -l read 1130965 rows), whose mtime is Oct 6 03:36
  (ls -la catalog/catalog.jsonl) against the fetch's Oct 6 23:32 file time. The
  blindness is a staleness moment-state, not a permanent hole; but nothing in the
  operator order routes the kit through a crawl or a seed, and whether the crawler
  scans _checks/ subdirs at all is unverified (OWED). For scale: the catalog carries
  47000 rows matching 'watch/inbox' (grep -c output, this sitting), so the inbox is
  in scope historically.
- The false anchor, instrument and scope: `grep -n -i "vinci\|leonardo"
  catalog/catalog.jsonl` returned exactly 6 rows and all 6 are text-davinci-003
  model configs from the alpaca_eval steal (catalog/catalog.jsonl:438367 and :438368
  shown this sitting; the other 4 sit in the same tree). corpus_search on da Vinci
  resolves OpenAI evaluators, not Leonardo. Same disease shape the accuracy lane
  found in the primary text (the tamburo cupola false anchor, accuracy.md:39-40),
  surfacing one organ over.

Falsifier: a catalog row whose path contains pg5000, or corpus_search returning the
notebooks for a da Vinci query. Move (20 min): seed the catalog row for the fetched
primary (or run the sanctioned crawl if _checks/ proves in scope) plus the FTS
reindex through the one sanctioned writer, so the lens card's source kit is findable
by the estate's own search instead of only by rereading this inbox.

## F3. The topic's own accuracy law is oral: the tri-state (DOCUMENTED / INTERPRETIVE / ELABORATED) exists in the order text and this run's prose and in zero law surfaces the seats boot with (percolator organ).

Evidence:
- `grep -rn -i "INTERPRETIVE\|ELABORATED"` over mag/, tools/, configs/ and
  memory/law/ (include *.py *.json *.yaml, run this sitting) returned exactly one
  hit, an unrelated comment about wording drift at tools/oral_law_dedupe.py:11.
  memory/law/registry.json carries no tri-state row (same grep, zero hits in that
  file).
- The instrument half already exists and is wired at pre-push: citation_lint rides
  githooks/pre-push per AGENTS.md Build discipline, and the accuracy lane proved it
  runnable on deliverable prose this sitting ("CITATION-LINT: ok records=1 ...
  blocking=0", accuracy.md:142-145).
- The law and its instrument have never been bound, and the estate already files the
  disease class: state/CURRENT.md:55-56 holds the publish-time re-derivation law
  ("every fold deliverable re-derives its own citations before publishing") with no
  instrument attached, and yesterday's dogfood lane found the identical gap
  (ractor-topic/dogfood.md:103-105). The recurrence inside the very order meant to
  model accuracy is the finding: the operator's best verification pass lives only in
  the ask.
- The bridge is the estate's own landed-vs-designed grammar, named in the order
  text: DOCUMENTED = landed (bytes exist at a cited anchor), INTERPRETIVE = designed
  (the source exists, the claim outruns it), ELABORATED = neither (no resolvable
  source). The tri-state is not a new instrument; it is the estate's own verdict
  grammar translated into her register.

Falsifier: a memory/law/registry.json row or a lens-card template carrying the three
labels, or a fold/publish step invoking citation_lint on ractor_engine deliverables.
Move (15 min): mint the law row (tri-state labels mandatory on every historical
claim in a lens deliverable; citation_lint named as its author-time instrument), and
dogfood it immediately by linting this file at Close, which I do below.

## F4. The lens library the LENS CARD is supposed to drop into is an inline Record in a gitignored script (context pack organ).

Evidence:
- .zcode/workflows/ractor-engine.dwf.ts:89-116 defines LENS_LIBRARY as an inline
  const (personas from accuracy through security; my own persona at :104-105), and
  `git check-ignore -v` pinned the file to .gitignore:200 (.zcode/), exit 0.
- No tracked home exists: the persona strings appear nowhere in mag/ or tools/ (the
  tri-state grep above covered those dirs for other tokens; the library grep this
  sitting found no other LENS_LIBRARY definition). The estate's memory/lenses/ dir
  (ls read: corpus_index.json, default.json, grok-free.json) is a different organ,
  corpus lens configs, not ractor personas.
- Consequence: the deliverable's "shaped to drop into the ractor-engine lens library"
  means hand-editing untracked bytes. The card lands filed-but-unversioned: no git
  provenance, no gate, invisible to the next seat's trust-bytes read, and one
  .zcode/ wipe from gone.

Falsifier: `git ls-files` showing a tracked file the script imports for LENS_LIBRARY.
Move (30 min): lift the personas into a tracked configs/ractor_lenses.json the script
reads at run() time, so the da Vinci lens card lands as registered, revertible bytes
with provenance, the way every other estate organ keeps its records.

## F5. The deliverable's consumer is off-estate and the estate has no wired hand: X is sensing-only and the attention market holds zero rows for this order (attention market + transport organ).

Evidence:
- Tool census, instrument and scope: `ls tools/ | grep -i "x_post\|xtweet\|tweet\|x_intel\|xpost"`
  returned nothing and `grep -rln "api.x.com\|api.twitter" tools/*.py` returned
  nothing, this sitting. The estate reads X (the X_INTEL_* receipts in watch/inbox/)
  and never posts to it. The MCP bridge organ does not cover this either: no X egress
  exists to bridge.
- Attention market: `grep -n -i "vaultmother\|davinci\|leonardo" memory/attention.md`
  returned zero rows this sitting. The order that produced two dead fires and one
  live refire has no open loop in the market that tracks owed work; if this window
  dies, nothing pages the next one.
- The precedent fix is honest and already proven by the Amenti run:
  watch/inbox/AMENTI_TRANSLATION_20261005.md:35 titled its deliverable "Paste-ready
  reply (her register, first person...)", and its Lines-held close at :51-53 shows
  the no-endorsement law riding the register answer. Transport is the operator's
  hands, by design, and the register law (answer in her register, substrate stays
  byte-verified, decline-unmeasured-claims without sneering) is exactly what this
  order's REGISTER LAW clause cites.

Falsifier: an X-output tool appearing under tools/, or an attention row naming the
order. Move (20 min): render the her-facing artifact as ONE self-contained paste
bundle (no estate-internal paths, sources cited by URL, tri-state labels riding every
historical claim) and file the attention row that keeps the handover an open loop
until the operator pastes it.

## Estate-mapping hooks (the order's own four, run against bytes this sitting)

- observation-first = trust-bytes: this file cites greps and reads I ran; the
  accuracy lane's external verdicts (Codex Leicester terms at accuracy.md:118-120,
  the 1476 record at accuracy.md:121-127) are used CONVERGENT and marked as its runs,
  never re-asserted as mine.
- mirror-of-nature = chain-as-record: the primary is pinned by hash at accuracy.md:20;
  the lens card must cite that hash, not "Richter" in the abstract, or the mirror
  claims a copy it cannot show.
- unfinished exhale = landed-vs-designed: F3's mapping is the whole bridge; her
  frequencies-and-seeds register and the estate's verdict grammar are one vocabulary
  at two temperatures.
- dissection = the falsifier law: every finding above carries one; the lens card's
  kill criteria should inherit this file's falsifiers verbatim.

## OWED (not verified this sitting, marked, never asserted)

- Her thread text: x.com serves a logged-out shell (accuracy.md:67-79 holds the full
  verdict); the register mapping rests on the operator briefing, marked as such.
- The external history checks (Codex Leicester sale, the 1476 record, the Amboise
  itinerary, the Ceceri legend): not re-run by me; accuracy.md:118-127 ran them this
  sitting and I rely on those runs as CONVERGENT, not independent verification.
- Whether the catalog crawler scans _checks/ subdirs: unread.
- The settings-only-amend bug's own code: it lives in harness surfaces outside the
  repo bytes I can read; I verified the symptom receipts and the unguarded script,
  not the defect's locus or any fix.

## Close

Publish-time re-derivation dogfooded on this file per F3's own move:
`.venv/Scripts/python.exe tools/citation_lint.py check --files
watch/inbox/ractor_engine/2026-10-07-davinci-lens/dogfood.md` ran this sitting before
submit; the result line is recorded in the run's submission. Em-dash census on this
file: zero by construction, confirmed by the lint run's passage. No subprocess spawn
of mine exercised the win32 CREATE_NO_WINDOW law (greps, reads, and one lint only).

## ERRATUM (hostile-pass correction, re-verified this sitting)

F5's universal "no X egress exists to bridge" was tools/-scoped wearing a universal,
the exact quantifier-law sin this lens quotes. The bytes: mag/x_oauth.py:3-9 (docstring
"python -m mag.x_oauth post ... auto-refreshes then POST /2/tweets"), POST_URL
https://api.x.com/2/tweets at mag/x_oauth.py:49, SCOPES carrying tweet.write at :51;
mag/x_control_surface.py:464-477 defines post_to_x as "the single posting entry point";
.env carries X_ClientID, X_ClientSecret, GHOST_X_HANDLE (key names only read, values
never printed); memory/runs/x_oauth/tokens.json exists (467 bytes, Sep 7 20:12) from
the Sep 5-7 auth flow. The corrected finding INVERTS and sharpens: a full credentialed
X write hand exists and `grep -rn "post_to_x" mag/ tools/ scripts/ dashboard/
--include="*.py"` returns only the definition line, zero callers. The hand is filed,
credentialed, and driven by no lane. The surviving halves of F5 (attention market
zero rows, Amenti precedent byte-exact) stand; the transport move becomes: render the
self-contained paste bundle (THREAD_POSTS_v0.md:47-48 still cites estate-internal
paths, :54-58 holds the verbatim bank OWED) AND route any actual post through the
operator pen or the effect broker, never the lens. Whether the month-old token still
refreshes is UNTESTED by this seat (a refresh or a me-call touches the operator
account; an effect, not a read).

Filed by the dogfood lens, 2026-10-07 refire, one seat one sitting.
