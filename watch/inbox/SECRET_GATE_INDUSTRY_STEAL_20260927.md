# SECRET GATE INDUSTRY STEAL CARD 2026-09-27

Class: BRIEF · Writer: zcode seat · Operator order: "do an external steal to
enhance this mechanism to fit industry standards and steal what they have
filtered through our needs" · Target: tools/secret_gate.py + githooks gate 10
· Status: research and distillation LANDED, implementation staged (never rush
edits into a live enforcement gate at 02:00; five amendments land next window
with parity tests).

## The steal, filtered through fleet needs

ADOPT (five amendments, in priority order):

1. gitleaks inline allow marker, the exact industry string: a line carrying
   `gitleaks:allow` suppresses its own finding. Kills the birth-certificate
   class (our own receipt quoting a synthetic fixture blocked a scan).
   Fleet filter: kept verbatim for ecosystem compatibility.
2. Path+rule scoped baseline entries (gitleaks [allowlist] paths shape):
   accepted entries keyed by rule + path regex with accepted_by + reason,
   surviving line churn where the line-fingerprint key does not (the CDX
   crawl-digest acceptance breaks on every file regen otherwise).
3. Keyword/structural line prefilter (truffleHog keyword-index steal):
   skip lines with no rule literal and no 16+ char token run before the
   combined regex fires. Target: --changed from ~157s under the pack's 60s
   stop line. Gate: mandatory parity test, prefilter vs no-prefilter
   identical findings over a real corpus sample, prefilter disabled if any
   rule lacks a derivable literal.
4. --history mode (gitleaks git-history scan shape): one git log -p pass
   through the same rule engine, deduped, outputting the purge target list.
   Feeds the operator-gated filter-repo step directly (lan.key, the cookbook
   ipynb key, the dead telegram token are the known first three rows).
5. Push-protection UX (GitHub shape): the BLOCK output names the exact
   operator response (excise/rotate, or accept by name with reason), so the
   block teaches instead of just stopping.

DECLINE (named, with reasons):

- Live provider verification in-tool (truffleHog's core move): sending found
  keys to their issuers belongs to the operator-gated rotation lane (the
  credrot card owns liveness adjudication), never to a push hook.
- SARIF output: no GitHub code-scanning consumer exists in this estate.
- pre-commit framework conversion: the raw hook is the estate idiom, churning
  it buys nothing.
- 800-detector expansion: 31 rules cover the fleet's actual provider surface.

## Bibliography (closed)

- gitleaks allowlist + gitleaks:allow + baseline mechanics: gitleaks docs and
  deepwiki.com/gitleaks/gitleaks detection-engine summary (search-verified
  2026-09-27)
- truffleHog 800+ detectors, keyword+regex architecture with live
  verification: arXiv "Keys on Doormats" methodology using truffleHog v3.90.8
- GitHub push protection response UX (source-fetched knowledge domain)
