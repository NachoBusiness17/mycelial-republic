# LESSONS - what the disk-storm data taught - 2026-10-09

Source evidence: evidence_pack/digest.md (11,079 files, 309.12GiB, walk 667s),
giant-file heads, internal/TIMELINE_AND_ESTATE_LAW.md, CRON_FREEZE_20261009.md.
Each lesson cites its datum. Pending inputs: external cards (Lane A), runbook
(Lane E), attribution (Lane F).

## L1. Tokens ARE disk - now measured, not asserted
The growth curve IS the burn ledger in physical form: dust until 09-21, then
24GB/day (09-28/29), peak 61GB/day (10-04), 46GB again 10-07 - the gala/burn
wave calendar in exhaust form. Corollary: smith-chart deltas are a
token-throughput proxy; one phenomenon, two instruments.

## L2. Unbounded capture x accidental scope, not "too much work"
Avg 28MB/file; the top 8 files (64.15GiB, 21% of total mass in 0.07% of files)
are accidental full-disk `find /c` listings and FINDSTR malformed-path error
loops. The failure mode is a missing CAP on captured stdout meeting one
mis-scoped command. Law shape: any sink without a bound is eventually filled
by the worst single accident, not by average behavior - the tail dominates.
Fix class: per-call stdout cap (journald SystemMaxUse analog).

## L3. Autonomy concentrates exhaust; instrumentation must scale with it
100% of the top-20 writer sessions are dwf workflow actors; interactive seats
are innocent. Unattended lanes have no human glance to catch runaway output.
Law shape: every autonomy grant ships with an exhaust meter; burn orders
carry an expected GB/day class so smith deltas can compare intended vs actual.

## L4. Control surfaces are plural - shutdown orders must sweep all registries
The 10-08 shutdown disabled 3 schtasks but the ZCode-side crons kept firing:
the hourly free-burn dispatched 3 x 1M-token agents/hour through the freeze;
the flash dispatcher no-oped every 10 min for 12 days past its own close date.
Law shape: a freeze sweep enumerates schtasks + session crons + in-flight
workflow runs + docker + ollama, one command, receipted.

## L5. The instrument must measure its own host (the dot-dir blind spot)
The largest estate item (.zcode, 335GB) was invisible to the first inventory
because it walks non-dot globs; the only disk-full tripwire was the operator
reading an OS screenshot. Law shape: monitoring is consumer-aware - the
seats' own cache/exhaust dirs are first-class smith rows (now true), and no
human is a tripwire.

## L6. Estimates are prompts to measure, never claims to carry
The 36h/1.3TB figure (retracted by author) vs measured 2-week ramp. The
phantom-number law now has an operator-side twin: dramatic numbers trigger
measurement, and retraction is cheap because the instrument, not the argument,
settles it.

## L7. Classify exhaust by recoverability at write time
Nothing load-bearing lived in the forest (durable work lands as receipts -
Lane F verifies); the junk class (find dumps) and the re-downloadable class
(ollama models, HF experiments) together were ~everything big. Law shape:
junk / re-derivable / unique; keep the RECIPE (modelfile receipts, re-download
manifests), delete the MASS. The ollama rotation-with-receipts pattern is the
model.

## L8. The tail risk is the crown jewels, not the exhaust
167GB free post-reboot, but the durable estate (ribs, receipts, memory) has
no off-box copy: github holds the curated public face only, the backup
remote is the same C: volume. The 5TB cloud offload is the highest-value
unexecuted item - higher than any purge.

## L9. Measuring was the cheap part
One 11-minute metadata walk + a 10-file peek answered what days of anxiety
could not. The expensive thing was the interval between noticing and
measuring. First pass = fear, second pass = numbers.

## L10. The estate self-diagnosed (the compounding is real)
An operator-ordered wave found the estate's own zombie crons and its own
exhaust signature, and corrected its own plan's numbers (prize 300 -> 81GiB
today) mid-flight. The machine catching its own author's system being wrong
is the design working.

## L11. OPERATOR COINAGE (2026-10-09): the standing-wave budget = the stolen 5-hour window
"this is like adopting our own 5 hour compute window limited that zai uses
for their hosts only stolen for our own purposes... the flywheel lattice
concept standing wave self steal." The mapping is exact: the provider's
rolling compute window is a governor the HOST runs on tenant exhaust; the
retention + budget layer this wave specs is the same organ, evolved on our
side and recognized as convergent - then stolen. Differences that matter:
theirs is denominated in tokens and opaque to us; ours is denominated in
tokens-as-disk (L1), readable in our own ledger (smith deltas), and rolling
by construction (7d retention = the window's width, the floor = its edge).
Standing wave completes the mesh_delta law ("memory as torrent standing
wave"): the wave persists, the medium does not accumulate - an archive is
heat death, a standing wave is memory that survives by cycling. Flywheel:
each turn of burn -> exhaust -> measure -> delta-vs-budget -> tune feeds
the next turn; the waste product becomes the governor's fuel. Self-steal
confirmed: the design was mined out of our own storm.
