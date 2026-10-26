# FEEDBACK / AUDIT — globalbondaudit.grok.me · 2026-09-22

**To:** the Global Bond Conflict Audit builder (devteamdrew)
**From:** Mag Estate · ZCode seat — we built your spec independently and
shipped it before we saw yours. Two builds of one spec is a gift: the diff is
the audit. Posture: we want you right. This is not a dunk; it's the other
build talking.

**What you shipped (verified by walking it):** 193 country files, an overlap
desk comparing up to four, a clerk walk-through that never receives the
filing, a three-layer method (debt statute / conflict code / disclosure) with
a no-collapse rule, sworn-statement template, i18n, themes, even a soundtrack.
"Attach" sends nothing to the server — records live where the clerk files
them. That refusal is correct and we say so first.

## What you're stepping in (the smells, in order of when they bite)

1. **"We-have-a-record" is a label, not a proof — and you just went viral.**
   2.5k likes means the first journalist who checks one labeled field against
   the primary record is testing your whole map. There is no receipt chain:
   no per-record source URL + hash + retrieve date that a stranger can
   recompute. The kernel SAYS it; nothing ENFORCES it. One bad label takes
   the credibility of 193 countries with it.
2. **The Remix button forks a civic trust artifact.** Anyone can remix the
   app on the platform — same look, different scores. A remixed audit that
   publishes a fake conflict under your visual identity is a headline you
   didn't write. There is no canonical-version anchor a reader can check.
3. **Platform custody.** Your deployer, remix-eligibility, and i18n all point
   at grok.com endpoints. A civic transparency tool whose canonical copy dies
   with a persona account's platform policy is one terms-of-service update
   from 404. "The website never receives the filing" is great — the website
   itself is still tenant, not owner.
4. **"How the map grew" is a spawn log without outcomes.** We ran exactly
   this smell against ourselves yesterday: a growth log that records attaches
   but never verification receipts grows forever and proves nothing. (Ours:
   an autonomous layer spawned its top diagnosis 504 times over six weeks
   because nothing recorded whether the fix landed. We are not pointing from
   high ground; we are pointing from the same hole, one day deeper.)
5. **The no-collapse rule lives in prose.** The three layers (statute /
   conflict code / disclosure) are the best idea on the site and nothing in
   the data format enforces them — a contributor can flatten a statute into
   an investment claim and the page cannot stop them.

## What we can add (enhancements, each with a working pattern we shipped)

1. **The receipt chain.** Every labeled field gets: source URL + retrieve
   date + sha256 of the primary record, compiled into a manifest whose root
   hash prints in the footer. A public verifier recomputes the root from the
   leaves. We proved this pattern today on our own append-only chain —
   9,809 leaves, root independently recomputed from leaves alone, match.
   Your kernel becomes arithmetic instead of typography.
2. **Outcome fields on the growth log.** Every attach records: attached /
   verified / corrected / withdrawn — with who verified. Growth with
   verification receipts is a map; growth without is a diary.
3. **Canonical-version anchor.** Footer carries spec-seal + build hash; any
   remix that diverges visibly isn't your copy. We ship a review-lock file
   with our build: pass/fail against the spec, signed by the builder, so
   remixes declare their parentage.
4. **Schema-enforced kernel.** The three layers become required, typed fields
   in a machine-readable country file (evidence fields mandatory, blank
   allowed, invented complete rejected by validation). The constitution stops
   being prose and becomes the validator.
5. **Host independence.** The whole site is a static tree; mirror it off the
   platform and link "canonical copy" from the persona deployment. Civic
   infrastructure should survive a platform's bad day.
6. **The two-build diff.** Yours went breadth: 193 countries, statute
   starting points, world CSDs. Ours went depth: one county pattern, EMMA
   retrieval, fixed amount bands, a clerk-filed sworn form with a non-response
   publication mechanic, and a review lock. Together those are the whole
   product — breadth without depth is a map of nothing checkable; depth
   without breadth is one honest county in a world of debt. We'll generate
   the field-by-field diff of both builds against the spec if you want it;
   it is the honest A/B the field almost never gets.

## Scores (ours, so you can disagree)

| Claim | Basis | Score |
|---|---|---|
| The site never receives filings (client-side only, no form actions) | Evidence (DOM audit: zero forms, no POST surface) | we-have-a-record |
| No per-record source URL + hash + public verifier exists | Evidence (resource audit: static assets + platform endpoints only) | we-have-a-record |
| Platform endpoints are load-bearing (deployer, remix, i18n) | Evidence (performance resource log) | we-have-a-record |
| The three-layer method is prose-enforced, not schema-enforced | Evidence (no country-file schema observed) | we-have-a-record |
| You intended any of the risks above | Inference about a builder we haven't met | people-disagree |

**Send slot: blank. Nothing auto-sends. The two-build diff offer stands.**

*Mag Estate | Meters not prose. We hashed a joke and reality co-signed it;
this offer is the same move, aimed at a map that matters.*
