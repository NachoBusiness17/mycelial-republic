# WANTS — the 24/7 drive's intake

Operator standing order (2026-09-17): the union fullsend drive runs **24/7 from this point
forward, full width on our problems — research or builds.**

How this works:

- Anyone (operator drop, any window, any lane) appends a want below. One want = one block:
  `### WANT <slug>` + a few lines. Plain language is fine.
- The **queue tender** (automation, every 2 hours) converts fresh wants into queue items in
  `queue.jsonl` (self-contained prompts, house schema), then marks the want `QUEUED` inline.
  The driver (every 20 min) drains them. Never the other way around.
- Research wants go out as digs (leads, promoted only by byte check). Build wants go out as
  draft specs / test stubs / patch designs — drafts land as receipts in `DAY_PACK.md`;
  a coding window promotes them by byte check. Model text proposes; bytes dispose.
- The drive never deletes. Appends only.

Lanes: or-union-alpha (free window, ends ~2026-09-23) + zai-lite glm-5.3-flash (law-15
paced, 10k weekly pool) + retry rotation over the other free lanes when a window dies.

---

### WANT 24-7-full-width (the standing order itself)

Keep the drive running around the clock on the fleet's real problems. Never invent filler:
when the queue runs low, the tender draws from (1) fresh wants here, (2) un-receipted
fifty-wide board tasks (FW-01..50) converted to self-contained research or build-draft
prompts, (3) the standing veins (WoW/modding/hosting research; doctrine stress tests;
X-radar steals; parable drafts; corpus primary-doc hunts). Status: **QUEUED** (this order
is the drive's constitution, not a queue item).
