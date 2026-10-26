# B2-31 poll-disease tripwire (2026-09-26)

## Verdict

LANDED. tools/luau_lint.py now carries two advisory grep checks for the two
cured diseases, so a t56/t63/t74 regression prints at mountain_check step 1
(the "structural lint (advisory)" line of `bash tools/mountain_check`). Spec
landed in the owning doc BEFORE the code change per build discipline. Zero new
findings on the cured tree: 43 files checked, only the 3 pre-existing
block-balance advisories, and HEAD's own lint byte-prints the same 3, so the
tripwire added no noise.

## Evidence

- tools/luau_lint.py:14-17 (docstring): "Disease tripwire (spec:
  roblox/docs/PLAYTEST.md "Headless tripwire", 2026-09-26 B2-31, filed before
  this code)".
- roblox/docs/PLAYTEST.md:26-29: "1. POLL (t56/t63 disease): a while/for loop
  body containing both a GetAttribute call and a task.wait(n) with n <= 10 at
  the same closure depth"; :33-36: "2. RMW (t74 disease): GetAsync and
  SetAsync called in the same function body".
- tools/luau_lint.py:81-83: "t56's poll fired every 1s, t63's every 10s;
  anything at or under 10s inside a loop is treated as a standing poll".
- Real-tree run: "checked 43 files, 3 with findings"; the 3 are zones_extra
  block-balance rows identical to the output of `git show
  HEAD:tools/luau_lint.py` executed from tools/ (probe deleted after run).
- Fixture proof (watch/inbox/burn_wave_20260926/B2_31_tripwire_verify.py,
  12/12 PASS): t56-shaped 1s leaderstats poll trips with "GetAttribute line 4
  rides a task.wait(1s) loop timer at line 11"; t63-shaped 10s garden poll
  trips at task.wait(10s); t74-shaped GetAsync+SetAsync in one function trips
  once (first run doubled it because task.spawn's own closure is a function
  body containing both matches; fixed with reported-span containment). Cured
  shapes stay clean: HeadMuseum split flushSoul/restoreSoul, TheAnswerBoss
  Touched-closure reads (closure depth 1) beside loop-depth task.wait(3) and
  task.wait(2), and disease keywords in comments/strings. Blanking verified
  length- and newline-preserving on ShadowLedger.luau: 3718 == 3718 chars, 92
  newlines.

## Work done

1. Read t56/t63/t74 receipts in watch/inbox/gala_20260925/afterparty/lanes/
   and calibrated against all six timed waits in the live tree (none is an
   attribute poll).
2. Spec first: PLAYTEST.md "Headless tripwire" section filed before any code
   change. tools/mountain_check already runs the lint as advisory step 1 with
   luau-lsp authoritative, so no gate script change was needed.
3. Code in tools/luau_lint.py: blank_comments_strings (offset-true strip so
   reported lines match the file), _matching_closer block walk (while/for own
   their header do), poll_disease_findings (same-closure-depth rule, nested
   loops deduped), rmw_disease_findings (function-scoped, nested bodies
   deduped), both wired into check().
4. Verified: 12/12 fixture passes, HEAD-vs-new real-tree parity, ShadowLedger
   cure intact (live store op is UpdateAsync :59 only; GetAsync/SetAsync
   survive only inside the t74 receipt comment, which blanking removes).

## Falsifier

- Reintroduce t56's poll into init.server.luau or t74's GetAsync+SetAsync
  into ShadowLedger.luau: `.venv/Scripts/python.exe tools/luau_lint.py` must
  print the named disease finding (fixture-proven above).
- If a cured-shape file (HeadMuseum, TheAnswerBoss) ever prints a disease
  finding, the closure-depth or function-scoping rule regressed.
- Advisory by design: mountain_check pipes lint with `|| true`, so findings
  surface at the gate without blocking the rojo build step.

## Bibliography closed

watch/inbox/gala_20260925/afterparty/lanes/t56.check.txt; t63.check.txt;
t74.check.txt; tools/luau_lint.py (HEAD and working copy); tools/mountain_check;
roblox/docs/PLAYTEST.md; roblox/README.md:64-70 (t74 durable write law);
byte reads of roblox/src/server/{ShadowLedger,HeadMuseum,TheAnswerBoss,
init.server,MudBasecamp,LightMazeZone,LedgerExchange,SwarmZone}.luau;
watch/inbox/burn_wave_20260926/B2_31_tripwire_verify.py. No web sources; every
claim verified against repo bytes.
