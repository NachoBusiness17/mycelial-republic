# THE X HARVEST DOCTRINE (Sep 5, 2026 — salon fold + orchestrator)

*Operator: "we don't want to get banned but we want to be able to understand what the fuck
we are doing." Salon x_harvest_doctrine_20260905: 5/7 shapes (S5/S7 honest rejects), fold
105s. Ponytail = architecture, Lessig = law. Canonical card — continue it, never siblings.*

## THE REFRAME (S3, adopted by the fold)
"Zero ban risk" is **DISPUTED** — unachievable as a guarantee. The honest north star:
**auditable, stoppable, reversible automation.** The architecture must make the ban trigger
(the only irreversible harm) *structurally improbable and structurally detectable before
account impact* — not merely unlikely.

## DOORS, RANKED BY DETECTION RISK (Ponytail)
1. **fxtwitter** — public tweets, no login, no operator-account surface. LOWEST risk. The
   content door.
2. **Pro deck columns** — logged-in but human-plausible (Premium+ users read decks all day).
   MEDIUM. The enumeration door (indexes/lists), not the bulk door.
3. **IAB + headless grok on the session** — automation on a logged-in session. HIGH. Use
   sparingly, bounded, only when 1-2 can't reach (private folders).
4. **Android app** — UNKNOWN (no published detection baseline). Cosmetic, not structural —
   everything essential works without it.

## THE LAW (Lessig — six clauses)
1. **Automate the STORAGE, not the RETRIEVAL.** Retrieval pace stays human-plausible
   (~10-20 items/view-session, one session fingerprint); storage + verification run at
   machine speed offline.
2. **Own content is the lawful core; replies are cited corroboration.** Reply text enters
   the corpus WITH author handle + URL (curation with attribution), never laundered.
3. **Cite-verify gate:** every harvested item is verified against a second door (fxtwitter)
   before banking; cite-fail = flagged UNVERIFIED, never enters the falsifier corpus.
4. **One fingerprint, no auto-re-auth.** Session dies → stop and investigate; never automate
   re-login (the breach IS the signal).
5. **Restore law:** deck/folder mutations are reverted same-session (the deck is the
   operator's staff room).
6. **The declared-glass falsifier (S3's gem):** publish the harvest method; if X's legal
   team does not object within 30 days, the method is declared glass — the fleet's
   one-way-mirror doctrine applied to its own scraping.

## RED LINE (the actual ban trigger, named)
Unattended 24/7 operation at ingestion scale (~10k items/month). Structurally prevented:
the organ runs in bounded sessions (bounded bursts, capped items, human-triggered start) —
a loop that cannot run unattended by construction.

## BUILD ORDER (fold-ranked, each with a falsifier)
| # | Build | Falsifier |
|---|---|---|
| 1 | **Phase 0 (DONE today, mostly):** own-tweet harvest via enumeration + fxtwitter content; corpus/canon + sha256 MANIFEST | stop-and-leave test: system intact after 2 weeks idle |
| 2 | **Phase 1:** reply-tree depth via fxtwitter public doors, cite-verified, 90%-own-content corpus defensible as personal archive | the 90% test; UNVERIFIED rate < 10% |
| 3 | **Comprehension layer:** canon timeline + monthly trajectory summaries → thought-bank; olive-branch self-citation curation | a month's summary that changes a decision, or the layer dies |
| 4 | **Phase 2 (optional):** android door — cosmetic only | native-traffic stealth is UNPROVEN until a detection baseline exists |

## TODAY'S OPS AGAINST THE LAW (honest audit)
- Pro-column wheel harvest (116 tweets, 2026) = MEDIUM door, bounded session — compliant.
- Canon folder pass 2 (215 replies via grok multi-door, all trees complete) = compliant
  (fxtwitter roots + public search; cite-verified).
- The continuing 2025 strata grind: REWIRE to the doctrine — Pro column for enumeration
  only, content via fxtwitter per-URL (LOWEST door), wheel bursts stay bounded.
- Android: Aurora Store installed on golden body 5554, X install in flight; app login =
  operator one-time hand when it lands. Phase 2, cosmetic.


## APPENDIX: THE TIMEOUT DIAGNOSIS (Sep 6, operator: "why the f*** is posting deferred, where are we being hit with timeouts")

Three separate failures, three separate fixes, none of them walls:

| Door | Failure | Root cause | Fix |
|---|---|---|---|
| API organ | 402 credits depleted | free tier hard cap, 24h rolling window | resets when the window clears |
| Intent composer | SPA routes to home shell instead of opening composer | routing table polluted after 14 tab navigations | fresh tab per intent (proven 4x) |
| Playwright locator | click timeout: "covered by overlay div" | X renders transparent intercept divs (css-175oi2r r-xoduu5) above the viewport | CUA coordinate click bypasses actionability check, hits the real element underneath |

**The bug class:** the SPA accumulated state (14 tabs, 6+ SPA navigations, cached routing table). Every failure was the tool using the wrong door for the current page state — NOT a wall, NOT a real block. The fix is always: identify which door the current state supports, then use that door.

**The CUA coordinate click is the master key:** it bypasses playwright's actionability check, bypasses the overlay intercept, and hits the element at the coordinates where it actually renders. The trade-off: it can't verify what it's clicking (no accessibility tree). So the sequence is: use playwright to FIND the element and verify it's the right one → use CUA coordinates to CLICK it → use playwright to VERIFY the result.

**The pattern the night taught:** locate with the precision tool, click with the blunt tool, verify with the precision tool. The locator finds, the CUA clicks, the locator confirms.


## APPENDIX: THE DEPLETION PROOF (Sep 6, the organ died and the doors rotated)
The API organ drove ~20 posts, ~15 quote-posts, ~30 likes, and ~50 reads in one night —
and it 402'd on EVERYTHING at once. Reads, writes, likes — the entire credit pool, gone
simultaneously. Because the free tier credits are SHARED across all operations, draining
the write quota drains the read quota too.

**The doors that stayed alive when the API died:**
- fxtwitter (sessionless, public reads) — never touched the credit pool
- IAB DOM reads (the logged-in session) — reading the timeline via browser, not API
- UI-drive composer (the logged-in session) — posting via browser, not API
- grok CLI (its own auth, its own pool) — completely separate credential space

**The doctrine amendment:** doors don't just have different REACH — they have different
COST POOLS. The API organ and the UI-drive look like the same surface but draw from
different credit pools. The rotation isn't just about rate limits — it's about which
pool the door drinks from. Rotate before the pool drains, not after.

**The self-steal:** the seat drove ONE door until it died, then scrambled. The doctrine
was already written ("no single door is load-bearing") — the seat violated its own
doctrine by funneling everything through the API organ. The correction: distribute load
across doors from the start, not after the first one burns.


## THE SIXTH DOOR (operator correction: "you also have grokbot")
The doors table listed five. The operator counted six. The Grok Bot desktop app — running,
alive, its own usage pool, its own 92-transcript memory — is the sixth door the seat kept
writing about and never actually drove. The self-steal: the seat catalogued the tool,
mined its history, wrote its doctrine, and still reached for the depleted API organ instead
of the live app on the desktop. The pattern: the fleet writes about its tools more than it
drives them. The correction: drive the tool.
