---
name: frontier-mine
description: Daily frontier research burn - fire the olm-mine workflow, fold the digest, steal-map the top 12 finds onto estate organs
argument-hint: <today YYYY-MM-DD>
---

# FRONTIER MINE - the daily frontier research burn

The estate's standing research intake: 8 frontier areas x 4 sources
(arXiv, HN, Reddit, X), lens-first (our own corpus read before the sweep),
dedupe against the catalog, independent confirmation of the top 24, steal
cards mapped to real organs, digest banked with a receipt.

## The ritual (one command, one fold)

1. FIRE: `CreateWorkflow` with `saved: {name: "olm-mine", args: {slug:
   "<today YYYY-MM-DD>"}}`. The caller knows the date; replayable workflow
   scripts cannot read clocks. Do not inline the script - the saved one is
   gated (digest 2487787e949f) and reruns are amendments.
2. FOLD on completion: present findings with evidence. Then steal-map the
   TOP 12 confirmed finds onto estate organs, one falsifiable probe each -
   the funded judgment's law is steal-map 12 with evals, never all 123.
   Fire the highest-leverage ports as a gala ball when the standing burn
   order is active.
3. BANK: digest LINKS row (writer olm-mine-cron), steal summary appended to
   the next-window handoff, receipt checked under
   `watch/inbox/frontier_olm_<slug>/`.

## The cadence

`EstateWalkDaily` 09:15 bakes the tapestry; this mine fires 10:00 daily via
cron (automation-cac38363). Same fossil-in-feed logic as every other organ:
research intake that has no cadence dies silently.

## Burn gate (hard)

The 10:00 cron firing is the standing burn order - unattended, no confirm
needed. Any OTHER firing of this card waits for the operator's in-chat
confirmation naming the slug: a manual refire, an off-cadence run, or a gala
ball off the steal-map. AmendWorkflow resume of an errored run is NOT a burn
(finished steps replay from cache at zero tokens) and needs no gate; a blind
refire where an amend would do is banned outright (failure law below).

## Laws carried in the asks

Never fabricate (anything unverified is OWED, never asserted), no em-dashes,
cite every claim as path:line or URL, CREATE_NO_WINDOW on win32 spawns,
and every find dedupes against `catalog/catalog.jsonl` + `memory/` before
banking - re-banking known work is waste.

## Failure law

If the mine errors: root-cause the script and `AmendWorkflow` with `path`
(cache imports every finished step at zero tokens). Never refire blind -
the 09-29 lineage died twice (journal order nondeterminism, then a world-
read glob) and both fixes live in the saved script.

## Lineage

2026-09-29: [191.8M tokens STRUCK 2026-10-01 per watch/inbox/48h_synth/ERRATA.md; the named digest carries no token total], 32/32 miners, 21/24 confirmed, 5 organ-mapped
steal cards (digest: watch/inbox/frontier_olm_20260928/DIGEST.md). Sharpest
card: the dormant paired-blind promote gate at mag/seed_percolator.py:7-12
plus REUSE-style decision-only acceptance - wiring, not building.

Final response: the digest receipt path under `watch/inbox/frontier_olm_<slug>/`,
the top-12 steal-map (find -> estate organ -> one falsifiable probe each), what
fired vs what the burn gate held (and why), and the banked LINKS row plus the
handoff line.

## X-door recipe (2026-10-04 port: fetch-before-bank)

Stolen from the day-4 mine, open-and-local-language-models steal card; the
instrumented door health it rode is banked at
watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md:15-35.

- site:x.com is dead on the z.ai backend (ignored on every query); phrase
  queries as quoted-"x.com" <topic> instead: 6 real status IDs vs 0.
- Batch at 2-3 queries; a 4-wide batch hit two 1302 rate storms.
- Date every status ID by snowflake epoch in the repo venv, never by
  snippet date: ts_ms = (id >> 22) + 1288834974657.
- Resolve through api.fxtwitter.com (3/3 that session: verbatim text,
  author, created_at, engagement).
- Profile-level x.com/<handle> results carry no status IDs: snippet-grade.
- FETCH-BEFORE-BANK: a source exists only after its primary URL is fetched
  and read; a fetch KILL banks as a first-class find so no later seat
  re-mines the same fabrication.
