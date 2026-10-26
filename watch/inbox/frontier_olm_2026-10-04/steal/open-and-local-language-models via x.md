# STEAL CARD: open-and-local-language-models via x (round 1, 2026-10-04)

Find (negative, confirmed): daymora.com is a flat-rate vendor landing page, NOT the search
layer's "AI API Rate Limits Explained (Sep 2026)" article. Fetched and read by the sweep seat
this session; banked as item 6 at
watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md:162-174
(the daymora page read itself is ask-carried; this ask's own checks are the dedupe greps,
the register read, and the organ file reads listed at the bottom). The page carries zero
published RPM/RPD/TPM/TPD numbers, no reset windows, billing-only token talk, and
"(c) 2026 Daymora" where an article date should be; the only free offering is Daymora's own
"50 free demo requests" (sweep :163-168).

## The mechanism (what the estate steals)

FETCH-BEFORE-BANK, with negatives banked as first-class finds. The search layer fabricated
an article title, a September 2026 date, and RPM/TPM framing that the fetched page does not
contain; the fetch layer does not fabricate (sweep :172-174, caution verbatim). One
un-fetched snippet was one RQ4 evidence row away from entering the estate's rate-limit base.
The steal is the pair: (a) no snippet-only source enters any RQ evidence base - a source
exists when its primary URL has been fetched and read; (b) when the fetch kills the source,
the KILL banks like a positive find, so no future seat re-mines the same fabrication.

The negative cost pennies because door health was instrumented (sweep :15-35):
site:x.com is dead on the z.ai backend (ignored on every query), the quoted-"x.com" phrasing
surfaced six real status IDs where the filter surfaced zero (:22-25), 4-wide query batches
hit two 1302 rate storms while 2-3-wide ran clean (:17-21), snowflake-epoch dating
(id >> 22) + 1288834974657 dated all six surfaced IDs in the repo venv without trusting
snippet dates (:26-32), and fxtwitter resolved 3/3 (:33-35).

Why this is a steal and not genre: the estate's standing intake runs 8 areas x 4 sources
daily with dedupe-then-bank (.agents/skills/frontier-mine/SKILL.md:9-12, :44-49), so every
seat is one snippet away from this failure mode, and RQ4 is exactly the question the
fabricated article was about. The published-bound set for the grid-192 free-lane
contradiction is UNCHANGED by this door (sweep :169-171): it remains the reddit sibling's
banked rows (watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-reddit.md:225-235:
OpenRouter 20 RPM request-count, 50 RPD below ~10 lifetime credits / 1000 RPD above, counter
via GET /api/v1/key; Groq per-model RPM/RPD/TPM/TPD with cached tokens uncounted, the
qwen3.8-27b row 30 RPM / 1K RPD / 8K TPM / 200K TPD at :201; Google dashboard-gated,
explicitly not guaranteed). The Groq row dedupes to the 10-03 register row 16, verified this
ask (watch/inbox/frontier_olm_2026-10-03/register.jsonl, 42 rows, row 16 = the
console.groq.com/docs/rate-limits mechanism row, "first primary mechanism source banked").

## Estate map (organ -> concrete port move)

1. PERCOLATOR (primary organ). The organ's own law: "raw signal in; noise/theater stripped;
   repeatables compiled to invariants", SIGNAL vs THEATER vs NOISE classification, false
   positives "logged, never carried forward as truth" (mag/percolator.py:1-22); mine digests
   ingest into the REVIEW PASS as candidates, promoted=False, promotion only through the
   standing percolate() path (mag/percolator.py:23-27). Port move: snippet-only sourcing is
   THEATER-class input - a candidate whose evidence exists only in search-snippet rendering
   classifies THEATER until a primary fetch lands; a fetch-kill like daymora banks as a
   SIGNAL candidate row (the kill is repeatable knowledge), promoted=False under the
   alpha-budget promote gate, and the invariant ("an article with a date is not a source
   until fetched") compiles only if the kill pattern recurs. Named, not executed this ask;
   organ writes are the promote gate's business.
2. GOPHER FLEET sensing lanes. The idle-key gopher is the right chassis for this recipe:
   deterministic chores, own pacing gate, every call metered (mag/gopher_lite.py:10-16).
   Port move: land the X-door recipe block (quoted-"x.com" phrasing, 2-3 queries per batch,
   snowflake dating, fxtwitter resolution; sweep :15-35) into this carrier's lens/doors.md,
   which today scores the four standing doors named at
   .agents/skills/frontier-mine/SKILL.md:9-10 and carries fxtwitter-WORKS
   (watch/inbox/frontier_olm_2026-10-04/lens/doors.md:61-76) but NO X-discovery recipe -
   the next fleet seat inherits a proven door instead of re-learning the 1302 storm.
3. CONTEXT PACK. mag/context_pack.py:1 packs minimum-token briefs ("never full chat"),
   pack modes at :16. Port move: one standing caution row on the route/audit pack faces,
   the sweep's caution verbatim ("a search-result article with a date is not a source until
   fetched; the search layer fabricates framing, the fetch layer does not", sweep :172-174).
   One sentence; stops the next seat absorbing snippet framing anywhere.
4. QUANTIZER: no port. mag/auto_quantize.py and mag/state_quantizer.py quantize model and
   state bytes; the find mints zero new rate-limit numbers (published set unchanged,
   sweep :169-171), so there is nothing to quantize. No-port labeled per house convention
   (watch/inbox/frontier_olm_2026-10-04/steal/inference-efficiency via arxiv.md:48-53).
5. SOVEREIGN MIRROR: no port claimed this round. RQ4's force-free-vs-funded decision is rib
   property (memory/rib/RIB_DRIVING_LADDER_20260928.md); if the probe below lands, the
   grid-192 update routes through a rib row, not through configs/mirrors.json - this ask
   read no rate-limit surface in the mirror organ and claims none.
6. WATER GRAPH: no port, named to block a bad metaphor. mag/water_graph.py is the
   hydrology/game engine ground truth (docs/ref/LANE_ASK_TEMPLATE.md:21;
   tools/ldt_nearmiss.py:4), not a quota/water ledger.

## Falsifiable probe (cheap, this week, on-box; NOT fired this ask)

Fire the estate-side key-counter logger - the exact instrument the find names as missing
("the estate-side key-counter logger is still the missing instrument"; same fold at
sweep :195-198 and reddit sibling :235). One small python script, one offpeak hour, zero
paid tokens beyond the N free requests: load the OpenRouter key from .env via
mag.flight_recorder.load_env, key never printed (method precedent
watch/inbox/physical_computing/receipts/U8_UNION_TECH_INTEL.md:5), poll
GET https://openrouter.ai/api/v1/key every 60s into a log, fire N >= 10 :free-suffixed
model requests through that same key inside the window, then diff
data.free_model_daily_requests.used across the window. Prediction (published bounds):
used increments exactly +1 per :free request, limit reads 50 or 1000 per the
all-time-credits tier, and the counter refills at the daily boundary (bounds re-verified
09-26: watch/inbox/EVENTS.jsonl:37 and watch/inbox/LINKS.jsonl:317; point-in-time shape
already receipted: watch/inbox/burn_wave_20260926/B2_128_keymeta_results.json:30,71 and
memory/runs/quote_audit_wide_20260925/inbox_concat.txt:235 show used 13/1000 and 2/1000;
the counter demonstrably moves day over day: 88/1000 on 09-16 at
U8_UNION_TECH_INTEL.md:44). Falsifier: delta(used) != N inside the window, or limit reads
neither published bound, or no refill at the boundary - then the published bounds cannot
carry the grid-192 lane math (the 18-lane x 1000/day arithmetic at EVENTS.jsonl:37 dies as
planning arithmetic), RQ4 stays open with published data demoted to priors under the
instruments-only law (RIB_MODEL_GARDEN_ROUTING.md:47-53, cited via sweep :95-96), and
free-lane forcing goes behavioral-only (the U8 route: no rate-limit headers on the wire,
Retry-After plus backoff, treat 429 as exceptional).

## Checks run this ask

1. daymora dedupe: `git grep --no-index -n -i "daymora" -- catalog memory/frontier docs
   corpus/steal state watch/monitor_lane.state` -> zero hits. `git grep --no-index -l -i
   daymora -- catalog watch memory/rib memory/attention.md memory/game memory/press
   memory/law docs` -> exactly one hit: the sweep's own negative bank
   (watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md). The
   find's "no estate holding names daymora" holds on every checked surface. An unbounded
   whole-tree grep was started and then stopped unfinished (memory/trajectory is huge);
   absence beyond the checked surfaces is not claimed by this ask.
2. Register row 16: PowerShell Get-Content of
   watch/inbox/frontier_olm_2026-10-03/register.jsonl -> 42 rows; row 16 is the Groq
   rate-limits docs row (url console.groq.com/docs/rate-limits). The find's
   dedupe-to-row-16 claim verified.
3. Reddit sibling Groq bounds: `git grep --no-index -n -i -e "groq" -e "key.counter" -e
   "free_model" -- watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-reddit.md`
   -> :56-64 (OpenRouter page constants FREE_MODEL_RATE_LIMIT_RPM=20, FREE_MODEL_NO_CREDITS_RPD=50,
   FREE_MODEL_HAS_CREDITS_RPD=1000, threshold 10 lifetime credits; Groq free-plan table),
   :201 (qwen3.8-27b: 30 RPM / 1K RPD / 8K TPM / 200K TPD), :225-235 (RQ4 published half
   plus the grid-192 consequence). The find's echo numbers dedupe exactly as claimed.
4. Reads end to end this ask: the sweep file (18,763 bytes, matching the find's byte
   claim), the sibling steal card for house format, lens/doors.md (85 lines), and the
   grid-192 grounding lines reddit :195-239.
5. Organ reads with line numbers: mag/percolator.py:1-27, mag/gopher_lite.py:1-17,
   mag/context_pack.py:1-17, .agents/skills/frontier-mine/SKILL.md:1-68,
   watch/inbox/EVENTS.jsonl:37, watch/inbox/LINKS.jsonl:317,
   watch/inbox/burn_wave_20260926/B2_128_keymeta_results.json:30,71,
   memory/runs/quote_audit_wide_20260925/inbox_concat.txt:235,
   watch/inbox/physical_computing/receipts/U8_UNION_TECH_INTEL.md:5,44.
6. Not run: daymora.com was NOT re-fetched this ask (ask-carried confirmed find; the sweep
   seat fetched it this session). The probe was NOT fired: zero HTTP calls to
   openrouter.ai, zero models run, zero organ writes.

## OWED / not run

- The key-counter logger probe: designed above, not fired.
- lens/doors.md recipe append: port move named, not executed.
- Percolator candidate row for the daymora kill: named, not executed (the promote gate
  owns writes into memory/percolator/candidates.jsonl).
- daymora re-fetch: not done; the negative rides the sweep seat's same-session fetch
  (sweep :162-174).
- Whole-tree daymora absence: not claimed; surfaces checked are those in check 1.

No em-dashes anywhere in this file.
