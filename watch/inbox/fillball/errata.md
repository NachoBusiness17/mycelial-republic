# ERRATA RECEIPT: the 191.8M phantom struck (fillball-1001, lane fill-191m-errata)

Receipt written 2026-10-01. Division B fill for GAP_REGISTER rank 4 / fill spec 4
(a08-r2). The errata itself lives at watch/inbox/48h_synth/ERRATA.md (append-only
file, ERRATA 001). Byte evidence for every line below is in
watch/inbox/gala_20260925/fillball-1001/lanes/fill-191m-errata.check.txt
(checks 1 to 10, all run this sitting on this host).

## What was owed

STORY.md:240 carried "191.8M tokens spent" citing
watch/inbox/frontier_olm_20260928/DIGEST.md as its named source; the named
source has zero "191" hits and no aggregate token total (measure lane flagged
it UNVERIFIED in-window, audit lane a08-48h-synth re-confirmed it, gap
register rank 4 owed the errata: "bind to workflow REGISTRY rows or cut the
number").

## What was done

1. STRIKE, STORY.md:240 (in-place single-line edit, line count unchanged at
   386, every existing pointer to line 240 lands on the strike): the phantom
   clause replaced by a bracketed ERRATA marker naming ERRATA.md and the
   REGISTRY-row truth. CHECK 5.
2. STRIKE, .agents/skills/frontier-mine/SKILL.md:50 (Lineage section, tracked,
   read before every daily mine fire): "191.8M tokens" struck with a bracketed
   pointer to ERRATA.md; sibling counts kept (they byte-check in the DIGEST).
   CHECK 7.
3. ERRATA NOTE, watch/inbox/48h_synth/ERRATA.md: new append-only file, ERRATA
   001, carrying the four byte reasons, both strikes, the full carrier census
   and the falsifier. CHECK 10 (ascii law).
4. ESTATE GREP for other carriers (the ask's third leg): git grep over the
   tracked tree plus a bounded text sweep over watch/ memory/ queue/ state/
   docs/ tools/ mag/ scripts/ tests/ .agents/. Exactly two LIVE carriers of
   the number as fact existed; both struck (STORY.md:240, SKILL.md:50). All
   remaining hits are record carriers left untouched on purpose (measure.md,
   48h-synthesis_RECEIPT.md, GAP_REGISTER.md, a08/a15 lane JSONs, measure.json,
   MICKEY17_V2_RUN_SPEC_ADDENDUM.md, ractor50/selfsteal.md:240,
   MASTER_MICKEY17_V2.md:82, ractor_engine dogfood lenses, the sibling
   citation_lint lane's embedded fixture) or non-carriers (PDF coordinates,
   unix-timestamp and latency substrings, trajectory command logs). Census:
   CHECK 8; raw pre-edit sweep:
   watch/inbox/gala_20260925/fillball-1001/lanes/_191_8_grep_raw.txt (118
   lines, saved mid-flight by this lane before the strikes).

## Why STRUCK and not re-bound

No binding surface exists: DIGEST.md has no total (CHECK 1/2);
memory/workflows/REGISTRY.jsonl carries seven frontier-olm-mine PASS rows
(lines 31-35, 38 for the 09-29 window, line 40 the 09-30 registration) and
zero "tokens" fields (CHECK 3); the a08-named run journal
(.zcode/workflow-runs/dwfrun-c41194a8-...mjs, 31,822 bytes) is a compiled
payload whose one "token" hit is prompt-law text and which has zero "191.8"
(CHECK 4). The register's alternative (re-bind to REGISTRY rows) is therefore
unavailable; the number is cut, per the register's own "or cut the number".

## Sibling coordination

The same fillball's citation-lint lane embedded the founding paragraph
(STORY.md:225-243 verbatim) inside tools/citation_lint.py by design so this
errata could not break its suite (its own comment at :542 anticipates the
strike). Proven this sitting: tools/citation_lint.py --selftest = 15/15 PASS,
exit 0 (CHECK 9). Note filed honestly: tests/test_citation_lint.py, named in
the linter's header, does NOT exist on disk (pytest exit 4, CHECK 9); the
sibling lane's JSON carries checks: []; that gap belongs to the citation-lint
lane, not this one.

## Ratchet

Not run: no file under mag/ or tools/ was touched by this lane (the ask's
ratchet clause is conditional on touching code there). Touched: STORY.md,
SKILL.md, ERRATA.md, this receipt, the lanes dir files.

## Falsifier

Any future surface asserting an aggregate token total for the 09-29
frontier-olm-mine run must cite a receipt that carries the number (usage
ledger row, run journal field, REGISTRY row) or it inherits this phantom.
