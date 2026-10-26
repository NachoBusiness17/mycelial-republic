# FW-24 — Press digest: Claude Cowork merge, sama delay, DeepMind Institute

- **class:** RECEIPT · **writer:** queue-gopher2-q024 · **board:** memory/plans/fifty_wide_20260917.md §E · **date:** 2026-09-28

## What ran

Appended an "Operator digest — 2026-09-28 (FW-24)" section to memory/press/PRESS_DIGEST.md
via shell append (`cat >> memory/press/PRESS_DIGEST.md`, exit 0). File went 11 → 19 lines;
appended bytes verified by tail. Content: the three ask-named items — Claude Cowork+chat
merge (@claudeai 13143 likes), sama delay (@sama 10180 likes), DeepMind Institute
(@demishassabis 3576 likes) — each sourced to watch/X_REPLY_RADAR_20260917.md by line
(:7-12, :19-24, :43-47) plus the pattern notes (:44 +0s self-reply, :70 usage-reset
invariance). The sama item cross-references openai.com/index/gpt-6-astra (fetched this
session for FW-22), which dates the Sol/Luna expansion to Sep 22, 2026 — the delay's payoff.

## Design defect found while executing (fix-comment-carries-receipt law)

The ask says "PRESS_DIGEST.md append", but this file is **generator-owned, not an append
log**: `mag/press_digest.py` `emit()` writes the whole file with `md.write_text(...)` at
mag/press_digest.py:174 on the governor cadence (MAG_PRESS_EVERY, default ~900 ticks,
mag/press_digest.py:16). Anything appended is silently destroyed on the next emit() that has
a pressing item. The current 2026-09-28T18:00:57Z content (a "[scrum] harvest() verb" item)
is itself an emit() product. This is the same disease class as the vow-of-the-syndrome
lossy-copy bug (session-outcomes-20260916-17.md): a derived surface treated as if it held
canonical bytes. Options for the owner: (a) make emit() append below a machine-section
marker, or (b) declare PRESS_DIGEST.md a pure latest-state surface and move digest history
to an append-only PRESS_DIGEST_LOG.jsonl. NOT fixed here — the change is an owner call
(dashboard/operator_inbox consumers read this path), and this receipt + the in-file WARNING
line carry the content durably either way.

## Durability

This receipt holds the full appended text's substance; the live file holds it until the next
emit() clobber. If the section is gone from the live file, this receipt is the canonical copy
per the shared-surface law (watch/inbox is the durable write root).
