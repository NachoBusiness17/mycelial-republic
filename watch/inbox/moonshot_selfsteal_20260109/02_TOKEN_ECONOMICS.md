# 02 TOKEN ECONOMICS - Lane 2 moonshot self-steal wave (2026-10-08/09)

Tokens as the unit of burn, budget, and value. Every number names its instrument and file. No web; all bytes ours.

## What it IS

One phenomenon, three instruments: money leaves (cost ledger), judgment
lands or not (verdict ledger), matter accumulates (disk exhaust as
physical token residue). LESSONS.md L1: the growth curve IS the burn
ledger in physical form; smith deltas are a token-throughput proxy. The
operator coinage (L11): our retention + budget layer is the provider's
rolling 5-hour compute window stolen to our side - except ours is
tokens-as-disk, readable in our own ledger, rolling by construction (7d
retention = width, free-space floor = edge).

## What we HOLD

The three ledgers:
- memory/runs/hermes_burn/usage.jsonl - per-call cost (tokens, cost_usd,
  channel); carrier tools/hermes_burn.py. Census this lane: 3,038 rows,
  cost_usd summed 94.74 USD (scripted sum, moment 2026-10-08).
- memory/burns/LEDGER.jsonl - verdict ledger: every burn graded (verdict,
  fresh_failure_mode, landing receipt, conditions). Census this lane: 705
  rows; clean tokens steal 210 / green 22 / vacuous 8; the rest free-text
  landings (vocab pollution - see SELF-STEAL).
- Physical residue: watch/inbox/disk_audit_20261009/evidence_pack/digest.md
  (11,079 files, 309.12GiB, purge prize 81.22GiB at 7d+) and live now:
  tools/disk_smith.py + logs/disk_smith.jsonl on MagDiskSmithDaily 08:50.

The laws:
- memory/rib/RIB_STANDING_WAVE_BUDGET_20261009.md - tokens are disk; five
  invariants: no unbounded sink, burns declare exhaust, recipe not mass.
- memory/rib/RIB_DRIVING_LADDER_20260928.md - the tier ladder: what money
  buys what judgment; the one-bug law (no verdict without conditions).
- memory/rib/RIB_INFERENCE_BUDGET_20261001.md + mag/inference_budget.py -
  the class-kill for the empty-content burn.
- watch/inbox/disk_audit_20261009/LAW_PACK.md - the retention contract
  {max_age_days 7, per-file cap, fleet budget, keep-free floor}.

## STATE

- Alive but unjoined: no organ emits the per-burn row (cost + verdict + GB/day delta).
- The one-bug is priced: descent day 1, $20.53 of $29.91 was re-fire
  theater (47 re-fires changed nothing) - the vacuous class, measured.
- The smith already governs: first two sweeps (2026-10-09T00:48Z, 02:16Z)
  show zcode_cache 335.33 -> 100.42GB, hf_cache 65.37 -> 9.11GB; the rib
  still awaits its mag/rib_boot.py VAULT_RIBS mount; tail risk stays the
  jewels (167GB free, no off-box copy, LESSONS.md L8).

## COMPOSITION

With the WoW machinery (play-as-work, GWAP scores as burn-quality): THE
ARENA v2 already runs it - persistent-role models play real-stakes
scenes, every beat banked as a chain-verified agreement payload scored
by cross-family juries, feeding a ledger that routes real dollars
(watch/inbox/ARENA_V2_DESIGN_20261004.md: 266+ gwap rows feeding 259 GPS
verdicts; dice law agreement 1.0 over 10 sessions). Play IS a burn, the
agreement score IS burn-quality - the SUBSTANCE GATE (hollow = ok false)
is the one-bug guard in a game jacket.

With the 5h compute window (the window IS the token budget shape): the
stolen window and our budget are the same organ (LESSONS.md L11) -
theirs opaque and host-run, ours readable: 7d retention as width,
free-space floor as edge, GB/day deltas as meter. Flywheel: burn ->
exhaust -> measure -> delta-vs-budget -> tune; burn orders declare a
GB/day class (invariant 3), the smith adjudicates, the window rolls.

With the mesh (token accounting across devices, who earned what): every
mesh message (.agents/skills/mesh-comms/SKILL.md: chan rows on
watch/room.jsonl, rib_bus, panels, wants) is a paid micro-burn.
usage.jsonl attributes cost to call ids, LEDGER.jsonl attributes
verdicts to slugs; the join gives each lane a per-day earned-what row:
tokens spent, verdicts landed, receipts on the shared inbox
(watch/inbox/INDEX.json as the proof-of-work surface).

With GSTD (tokens as the internal unit GSTD settles externally): the
incorporation draft seats our instruments at GSTD's four boundaries -
evidence-hashed submit, consensus + immune critics at quorum, the GPS
ledger at routing, verkle receipts making payouts auditable at
settlement (docs/ref/GSTD_INCORPORATION_DRAFT.md section 1). GSTD settles
externally (chain dormant: totalSettled=0, 79d, byte-proven in
memory/burns/LEDGER.jsonl), but what it settles FOR is internally metered
as tokens/$ /GB per green verdict - that exchange rate is what the three
ledgers exist to quote.

## MOONSHOT

Exhaust becomes the price signal - join the three ledgers into one
internal exchange and let the waste product set prices. (1) Emit the
per-burn row (ts join: cost_usd + verdict class + GB/day delta);
descent day 1 proves the method - a vacuous class priced at $20.53 in
one afternoon. (2) Publish the price list: a green-sealed receipt costs
N tokens / M dollars / K GB of residue; a vacuous burn costs 10x with
zero yield. (3) Make the window the money supply: retention width +
free-space floor cap supply; burn orders declaring a GB/day class
upgrade into burn orders bidding tokens; when GB/day rises without
verdict-quality rising, the price of autonomy rises automatically - the
exhaust curve becomes the market's heartbeat. (4) GSTD settles externally
against our internal quote, verkle-receipted: the estate becomes market
maker between its own burn and the world's money; a green verdict
unquotable from joined bytes = theater.

## SELF-STEAL

- Stolen from ourselves: L1's one-phenomenon-three-instruments corollary
  is the join's blueprint; L11's flywheel is the exchange's control loop;
  the arena substance gate and mag/inference_budget.py are one kill on two
  surfaces (one bug, many jackets, run forwards).
- New byte-backed state minted this lane: the usage.jsonl sum (3,038
  rows, $94.74) and LEDGER census (steal 210 / green 22 / vacuous 8) had
  no prior carrier - computed, not hand-copied.
- Honest debts: LEDGER.jsonl verdict vocabulary is polluted (free-text
  strings defeat joins - normalize, never tolerate); usage.jsonl rows
  carry no landing path, so cost joins to verdicts only by id/slug.

## FALSIFIER + PROBE

Falsifier: if the three ledgers cannot be joined into one per-burn/
per-day row (cost + verdict + residue) in a single sitting, "tokens are
disk" is poetry, not plumbing - strike the composition claim. Secondary
(the rib's own): a monster regrown behind a landed cap, no organ catching.

Probe (cheapest executable step): a ~30-line one-shot script, no new
infrastructure, runs in seconds: read memory/runs/hermes_burn/usage.jsonl
+ memory/burns/LEDGER.jsonl + logs/disk_smith.jsonl, join by UTC day,
emit one table - cost_usd, verdict counts by class, GB/day residue
delta - and print the first internal price row: dollars per green
verdict vs dollars per vacuous day. A missing column is itself the
finding. Receipt the output here; mint no tool until the join is proven.
