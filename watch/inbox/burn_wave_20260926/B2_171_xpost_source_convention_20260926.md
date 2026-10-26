# B2-171 x-post-source convention spec (SW-07, 2026-09-26)

## Verdict

LANDED. The two-field convention (canonical = the resource, url = the X post it was surfaced from) is now written into the mag/link_library.py spec, and a new `convention` subcommand classifies every canonical-vs-url host mismatch as x_post_source (sanctioned shape) or HOST_DRIFT (real drift, exit 1) instead of leaving the shape unnamed.

## Evidence file:line quotes

- QUEUE.md row: "32 LINKS rows (post-B2-26 shas) store the resource in canonical and the source post in url (LINKS.jsonl:31 arxiv-vs-omarsar0 is the shape)"
- watch/inbox/LINKS.jsonl:31: `"canonical":"https://arxiv.org/abs/2609.15983","url":"https://x.com/omarsar0/status/2099924717704732699"` -- the archetype.
- Fresh census on current bytes: 33 rows carry the x-post-source shape (the brief's 32 plus one landed since the brief was filed); 305 rows are host-matches; 0 rows are unclassifiable host drift.
- mag/link_library.py new docstring block: "x-post-source convention (B2-171, 2026-09-26): a filed row MAY carry two different hosts by design ... This is NOT host drift: the convention is 'canonical = what to open, url = where it was found'."

## Work done

- mag/link_library.py: spec section "x-post-source convention (B2-171, 2026-09-26)" added to the module docstring, naming the two fields and the 33-row population.
- mag/link_library.py: X_SOURCE_HOSTS constant, _host() helper, classify_host_mismatch() (returns match | x_post_source | HOST_DRIFT), convention_report() scanning the whole ledger.
- New CLI subcommand: `python -m mag.link_library convention` prints counts plus every classified row; exit 1 iff HOST_DRIFT > 0.
- Live run: match 305 / x_post_source 33 / HOST_DRIFT 0, exit 0.
- Classification probes: arxiv-vs-x.com -> x_post_source; identical hosts -> match; arxiv-vs-github -> HOST_DRIFT. All pass.

## Falsifier

The brief's failure mode: the shape left unnamed, indistinguishable from real drift. Falsified: the convention command names every such row and any future cross-host row that is not the X-source shape exits 1 as HOST_DRIFT. Residual falsifier for the next reader: run `python -m mag.link_library convention`; a HOST_DRIFT line or a non-zero exit reopens this brief for triage.

## Bibliography closed

Read: mag/link_library.py (full), watch/inbox/LINKS.jsonl (line 31 quote + full-scan census), watch/inbox/burn_wave_20260926/B2_26_links_sha_backfill_20260926.md referenced via the row (drift section context), QUEUE.md B2-171 row. No external sources needed.
