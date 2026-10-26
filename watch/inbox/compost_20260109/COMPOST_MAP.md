# COMPOST MAP - the graveyard read for patterns (2026-10-09)

Companion to `COMPOST_LEDGER.jsonl` (34 rows, same directory). The ledger is the
graveyard of killed WANTS (ideas, projects, asks, models, claims, tools); the belief-side
demotion register lives separately at `memory/fold_history/SUPERSEDED.md` (referenced
here, never duplicated - conclusions there, wants here; a few phantoms appear on both
sides because a dead claim is both a belief and a want).

Method: `git log --all --oneline --grep` over KILLED / STRUCK / STOPPED / PARKED /
DECLINED / RETIRED / VOID / SUPERSEDED / VERDICT (top ~25 bodies read), kill-marker greps
over `watch/inbox/*.md`, the `memory/zknot/LATEST.md` prompt trail, and per-starter byte
verification. Every ledger row cites its `killer_bytes`; rows that could not be verified
are in the Unverified rumors section below, not the ledger. Counts computed with
`.venv/Scripts/python.exe`.

## 1. Deaths by cause (34 rows)

| cause | count | share | rows |
|---|---|---|---|
| OWN-FALSIFIER | 9 | 26 pct | gps-embed-substrate, blind-sweep-pooled-review, doctrine-owed-chase, overmind-hour, model-mating-door, zai-24wide-lane, reasoning-burn-question, salon-ess-replicate, upcycle-linear-conversion |
| RESOURCE-DEATH | 6 | 18 pct | ollama-ling-3-0-flash, ollama-maze-keeper, ollama-qwen25-32b, zombie-42364, mangos-mysqld, llama-server-idle-8 |
| EXTERNAL-KILL | 6 | 18 pct | census-headline-1341, waffle-2-expanse-tweet, metr-shitpost-v1, playhouse-dependency, spikingbrain-100x, phantom-191m |
| BUDGET | 4 | 12 pct | xai-card-reissue, city-generator-v2, lite-lane-mates, gemma4-seat |
| OPERATOR-STOP | 3 | 9 pct | olm-mine-day8, roblox-lane, verkle-compaction |
| SUPERSEDED-BY | 2 | 6 pct | dashboard-frozen-copy, weave-router-steal |
| ETHICS-DECLINE | 1 | 3 pct | ao3-author-scan |
| AGED-OUT | 1 | 3 pct | hermes-premium-rung |
| CLAIM-RETRACTED | 1 | 3 pct | growth-700gb-claim |
| DRIFT-STALE | 1 | 3 pct | kill-list-unreferenced-0908 |

By class: model 8, tool 7, claim 7, idea 6, ask 3, project 3.

Note the disk cluster: 5 of the 6 RESOURCE-DEATH rows and both disk-pressure causes of
the BUDGET family land inside one week (2026-10-03 through 10-08, the C-drive crisis).
The graveyard is season-shaped: crisis weeks mint resource rows, burn weeks mint
falsifier rows.

## 2. What dies young vs old

- Young deaths (born and killed inside 24-72h): gps-embed-substrate (one sitting),
  blind-sweep-pooled-review (same sitting as its card), overmind-hour,
  model-mating-door, zai-24wide-lane, reasoning-burn-question (one burn night),
  waffle-2-expanse-tweet (minutes), metr-shitpost-v1 (same day), city-generator-v2
  (gated at banking), gemma4-seat (dark on arrival), weave-router-steal (struck by the
  mine's own round 2). Cause profile of young deaths: overwhelmingly OWN-FALSIFIER and
  EXTERNAL-KILL. This is the deliberate-ask economy working - a trial is born with its
  death clause attached, so it dies fast and cheap when the numbers say no.
- Old deaths (weeks-old at death): the ollama cold models (3+ weeks cold, one with zero
  usage rows its whole life), kill-list-unreferenced (unreferenced >3wk), zombie-42364
  (72.4 CPU-hrs), mangos-mysqld (21h orphaned), hermes-premium-rung (4 weeks of credits
  burning down), census-headline-1341 and phantom-191m (claims that roamed for days
  before the audit caught them), roblox-lane and verkle-compaction (sacred cows that
  needed a summons). Cause profile of old deaths: RESOURCE-DEATH, DRIFT-STALE, AGED-OUT,
  and the operator-ruled parks. Things that die old die of accumulation and neglect -
  nothing re-checked them until a crisis or an audit did.

The age split is the map's sharpest line: young death is designed (falsifiers filed at
birth), old death is discovered (watch lists, audits, crisis inventories). If you want
fewer surprise deaths, move kills from the second column to the first by pre-registering
death clauses on anything with a cost.

## 3. Which causes are healthy vs unhealthy

- Healthy (the design working):
  - OWN-FALSIFIER (9): the top cause and the estate's best one. Every row here killed
    itself on numbers it agreed to in advance - the cleanest was GPS-EMBED, the
    operator's own 3am idea pulled, wired, measured and killed in one sitting with the
    model banked for the retry.
  - EXTERNAL-KILL by primary fetch (waffle-2-expanse-tweet, spikingbrain-100x,
    phantom-191m, census-headline-1341): fabrication caught is the trust machinery
    passing its own tests. The failures would have compounded silently otherwise.
  - OPERATOR-STOP with named conditions (verkle-compaction, olm-mine-day8): a park that
    files its re-raise conditions and salvage inventory is a healthy death.
  - DRIFT-STALE (kill-list-unreferenced): the healthiest tool death - the string-ref
    recheck proved nothing wanted it, and the move was reversible with sha16 proof.
  - CLAIM-RETRACTED (growth-700gb-claim): the author killed his own number in under a
    day; no forensics needed.
- Unhealthy (watch for these):
  - RESOURCE-DEATH by crisis (the 10-08 disk cluster): kills decided by a 100 pct-full
    drive are forced, not chosen. The floor tripwire (15GB) and the smith chart exist
    now precisely because this class was allowed to accumulate.
  - AGED-OUT (hermes-premium-rung) and BUDGET rows without stop-asking markers
    (xai-card-reissue burned operator corrections before the park marker landed): silent
    depletion - the estate kept asking a dead lane for work.
  - Zombie-adjacent rows (zombie-42364, doctrine-owed-chase, llama-server-idle-8): things
    that lie about being alive. CPU-hours without output, 25 cron refires with 22 stale,
    8 servers holding one port with zero traffic. The unhealthy part is not the kill, it
    is how long they ran undetected - each one exposed a blind spot in a watch list.
  - ETHICS-DECLINE (1 row only, and it is a healthy refusal): the AO3 decline was the
    seat working; it is listed unhealthy-adjacent only because the ask arrived at all.

## 4. Top-5 compost lessons (the reusable organs)

1. File the death clause at birth and the kill costs one sitting. GPS-EMBED,
   salon-ess-replicate and the model-garden kills (overmind, mating door, zai-24wide)
   all died on pre-registered numbers with full receipts and banked revival kits. The
   falsifier is not bureaucracy - it is what makes killing cheap enough to do fast.
2. A caught fabrication is the best fertilizer in the repo. The 191.8M phantom became
   the citation-lint gate's founding fixture plus a SUPERSEDED row; the 1,341 headline
   became the census-carrier grammar a patrol parses; the Waffle-2 catch became the
   standing demo of the primary-fetch law. Three phantoms, three standing instruments.
3. Bank the organs of the kill before the kill. Modelfiles before `ollama rm`
   (maze-keeper's 15KB modelfile IS the resurrection), starter scripts the day the
   daemon dies (mangos law), moved-not-deleted with sha16 (kill list), sha-addressed
   stubs with a proved restore door (the 2.52GB dashboard copy). Reversibility is a
   pre-kill act, never a post-kill scramble.
4. Classify the death or you file one fact as two. The mates/lite lane burned a
   correction cycle because "given-away lane" and "exhausted quota" were the same fact
   filed separately; gemma-4's 429-with-valid-key needed the shared-pool diagnosis to
   point at the console instead of the code. Diagnosis class precedes cure.
5. Zombies are an instrument problem, not a character problem. Doctrine-owed-chase
   refired 25 times in a day on a cron with no novelty accounting; 8 llama-servers sat a
   day at 45GB under a watch list that did not know their name; zombie-42364 ran 72.4
   CPU-hrs with zero output contract. Each cure was a watch list, a usage row, or an
   output contract - all three are cheap; none were present at spawn.

## 5. The 3 revival conditions worth pre-warming now

1. GPS-EMBED cold-start leg. The trial banked a real 2.84 pct vs 0 pct advantage on
   never-seen shapes and a one-command rerun; it dies only until shape diversity grows.
   Pre-warm: a distinct-task_shapes counter over the gps ledger with a tripwire (e.g.
   25+ shapes with winner clustering) that pages the operator to rerun
   `python -m tools.gps_mcp.gps_embed_trial`. The substrate is dead, the sidecar is not.
2. The starter-script sweep (generalize the mangos law). Every re-pullable kill should
   have its one-liner written now, while the context is fresh: ling-3.0-flash re-pull
   command, maze-keeper create-from-modelfile, qwen2.5:32b pull, gemma-4 console
   re-provision steps, xai reissue steps (money-exists gate). Pre-warm: one
   REVIVAL_CARDS page in this directory or the extension of each ledger row's
   revival_condition into a copy-paste command - the graveyard becomes a catalog.
3. The ddr3-body weekend door (upcycle survivor). The upcycle hope died but its own
   autopsy named the only viable conversion: depth-prune 20-35 pct of a 7B + QLoRA-heal
   5000 steps on 328M tokens, zero GPU spend, one estate weekend. Pre-warm: freeze the
   recipe card (model choice, prune ratio, heal steps, eval bar vs SWA+4-sinks) so the
   next idle weekend runs it instead of re-deriving it - that is the descent protocol's
   prior-art sweep applied to our own compost.

Counter-example worth remembering: revivals already happen same-day when the condition
is human - the 8765 dashboard port was UNPARKED the same evening the operator deleted
the portproxy rule. Parks with named conditions are not graves; they are queues.

## 6. Held, not dead (explicitly NOT ledger rows)

- athena-class (32GB ollama blob): zero usage rows, but the FROM-blob is local with no
  known registry source - deletion may be unreconstructible, so it is HELD for operator
  ruling (watch/inbox/DISK_INVENTORY_20261008.md, "Held for operator ruling"). Not a
  death until the ruling lands; if it lands, it rows here.
- HF cache dead experiments (~60GB: gemma-4-31B, saelis-31b, Qwen3-8B, tabfm): listed
  as relief-on-the-table, re-downloadable - proposed, not executed. Rows when the purge
  fires.
- Gero-4B calibrator: honestly gated (no published evals + GB-class download), operator
  sitting to define the battery target. Gated, not killed.

## 7. Unverified rumors (checked, could not byte-verify - kept OUT of the ledger)

- Cerebras provider line "decided-PARKED": cited second-hand in the f-30 todo triage
  (git 7d5e2e37e: "providers.yaml:699 dormant") - the audit commit is banked bytes for
  the claim, but the providers.yaml line was not re-verified this sitting. Row it at the
  next closeout after reading the config.
- Shitpost desk v3 "killed pompous" (git 5ef7c5986: "v3 killed ... same bug different
  jacket: confidently wrong"): real strike, but the register-law class is already
  carried by the METR v1 row; folded into the pattern analysis instead of the ledger.
- The 42-test phantom STRUCK from the model-garden carrier (git 56449c53b: "collect
  reads 19, instrument named"): same fabrication class as phantom-191m and
  census-headline-1341; the class row exists, the specific row would be redundant.
- The RUN CLOSEOUT REGISTER's 21 dispositioned runs (git 6edc796f8: 3 quota-wall, 8
  provider-stopped, 13 errored, VOIDs): those are run dispositions, not killed wants -
  the minted rule ("zero-token deaths are admission tickets not lost work") is banked
  there and referenced here.

## 8. How this ledger grows

Append-only at closeouts: whenever a lane kills a want, its closeout receipt lands one
row here with `killer_bytes` pointing at the receipt or commit that proves the death
(same amend-never-rewrite law as SUPERSEDED.md). A death that cannot cite bytes goes to
section 7 of this map, never the ledger. The compost field is the point - the graveyard
is only useful if every corpse carries what it feeds.

Falsifier for this instrument: a month where kills land in receipts (STRUCK / KILLED /
PARKED markers in commits and inbox) but this ledger gains no rows - then the compost
path is sibling memory again and the closeout rule, not the archaeology, needs the fix.
