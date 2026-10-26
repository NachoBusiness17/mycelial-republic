# B2-174 receipt (2026-09-26)

## Verdict

LANDED. The sharpened same-uid, same-UTC-day, cross-server double-write probe replaced the dead two-uid P3 falsifier in roblox/docs/PLAYTEST.md as a new checked section gated ahead of the "Score the session" block (the Sept-29 soft-launch gate reads "this whole page passing once, clean", so the new checkboxes are now part of that gate). The old two-uid form is named and retired inside the section with the reason it cannot discriminate.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md:50-52 (the dead P3 as preregistered): "P3 ledger race. Two clients cross one portal; stop, rejoin: both 'took the portal' rows persist under key p<uid>_<UTCday>. Falsifier: a row gone = lost update, t74 absent from the running build."
- watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md (P3 discriminator finding): "the old module also passes the two-uid portal crossing (S4) because two clients write two different keys; no race exists per key. The discriminating probe is same-uid, same-UTC-day, cross-server double write (S2/S3), or mixed fleet where an unfixed server's late SetAsync clobbers the fixed row (S4b)."
- roblox/docs/PLAYTEST.md before edit: grep for "two-uid|portal crossing|two uid" over roblox/ returned zero hits, i.e. the falsifier the brief ordered replaced had never been carried into PLAYTEST.md at all (it lived only in the B2-10 prereg receipt); the P3 slot in the playtest page was empty.
- roblox/docs/PLAYTEST.md after edit, new section "### ShadowLedger crossing probe (B2-174 2026-09-26; replaces the B2-10 P3 two-uid falsifier)" directly above "## Score the session", with two checkbox lines: the SAME-UID probe (one uid, two servers, same UTC day, both rows must persist under p<uid>_<UTCday>, one row = lost update) and the S4b mixed-fleet residual (a missing row while any server is pre-t74 is the clobber, not a client bug).

## Work done

1. Traced the two-uid falsifier to its source (B2-10 prereg receipt lines 50-52) and the B2-30 sim finding that kills it (S4 passes on pre-t74 bytes).
2. Verified PLAYTEST.md (127 lines at read) carried no P3 at all, so the brief's "replace it" landed as: insert the corrected probe in the page the Sep-29 gate actually reads, naming the retired form and why it died.
3. Added the section with the two checkboxes (primary same-uid crossing plus the S4b residual the B2-30 receipt names), placed above "Score the session" so the Sept-29 whole-page gate includes them.
4. No other PLAYTEST.md bytes touched.

## Falsifier

The brief's own falsifier surface: the Sep-29 run. If a pair of live clients on the 08:28-or-newer build run the SAME-UID probe and both rows persist, the probe holds; if any "took the portal" row is gone, either t74 is absent from the running build or the live DataStore violates the stub's UpdateAsync model (the B2-30 receipt's own falsifier, still open for throttles/retries/cross-region). The sharpened section also self-falsifies the OLD falsifier: two uids crossing one portal can never fail on any build, so if the Sep-29 runners execute the retired two-uid form instead of the same-uid form and call it a pass, the gate proved nothing; the section text forbids that reading.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md (P3 at lines 50-52)
- watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md (S4/S2/S3/S4b findings)
- watch/inbox/gala_20260925/afterparty/lanes/t74.check.txt (on disk, 4841 bytes, 2026-09-26)
- roblox/docs/PLAYTEST.md (127 lines before, 145 after)
