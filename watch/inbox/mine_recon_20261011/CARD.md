# MINE RECON (sibling seat report, banked 2026-10-11; six read-only arms, five still out)

Source: sibling seat's recon turn, pasted to the main seat. Recon-first shape: 14 dirs,
2,535 files, ~238 MB, frontier_olm_adhoc live-writing. Three byte-backed findings plus
one instrument bug caught before it banked:

1. THE MINE'S RETRIEVAL INDEX HAS NOT FOLDED IN 40 DAYS. research-lens --status:
   corpus 107 docs, ZERO lens edges, last_fold 2026-08-31 (default 08-09). Six weeks
   of mining into a shelf its retrieval stopped reading. Produced-but-never-folded
   class, byte-confirmed. FIX CLASS: fold the corpus (the librarian/FTS organs exist).
2. frontier_help SEES ZERO JOURNAL SIGNALS BECAUSE IT SAMPLES 30 OF 216,799 EVENTS
   (mag/frontier_help.py:79 tail=30). Window-read-as-census disease (fake_success
   class). FIX: census read or window labeled in output.
3. THE ASKS IT SURFACES ARE TWO MONTHS OLD: HELP_WANTED.md stack asks stamped
   2026-08-09. Stale-signal disease; same fix family.
4. UNITS BUG CAUGHT (LAW-064 class, third this week: seconds printed as days):
   arm's "234.9d ago" was 234.9 SECONDS - every "oldest never-read" file was
   freshest-in-tree, written during the scan. The catch method is the steal: two
   independent runs minutes apart showing a "70-day" spread = 70 seconds = units.
   Also: atime==mtime proxy is self-contaminating (measurement bumps atime) and
   unreliable on Windows - the never-read hunt must use zero-reference-by-name +
   never-folded-anywhere as evidence class instead.
5. Honest sweep result: 404 never-read of 99,599 files (0.4%), and those are empty
   log stubs + .gitkeep markers. The estate is 99.6% read; no unread-knowledge
   hoard exists.

Reconciliation owed when that seat's five remaining arms land (not this seat's to
restate). gap-map contradiction (route 2,315 calls @ 0.243 vs audit 3 @ 0.000)
measured twice on separate days, still open.
