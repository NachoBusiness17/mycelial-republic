# lineage.md - the lineage lens on THE SPORE SHARING PROBLEM (2026-10-05)

Run: spore-sharing ractor, lens lineage. Job: mine the estate's own prior ractors,
salons and design docs for what was already asked, already built, already ruled,
and never delivered, on the topic of pushing the estate to
github.com/NachoBusiness17/mycelial-republic so a second operator can regrow it.

Instruments this sitting: Read on named files; `git remote -v`; `git branch -r`;
`git log github/master -1 --format=...`; `git rev-list --count github/master..HEAD`;
`git check-ignore -v`; `git ls-files` counts; `git config core.hooksPath`; scoped
greps (each scope named inline); redacted token scan via
`.venv/Scripts/python.exe -c` (counts and lengths only, no secret values printed).
Absence claims name their scope. No em-dashes. Anything unverifiable is OWED.

## The headline: this is not a greenfield share, it is a stalled re-seed

The remote is already wired: `git remote -v` returns
`github https://github.com/NachoBusiness17/mycelial-republic.git` (fetch+push)
plus a same-disk `local` bare backup. The remote branch is `github/master`, tip
`dc66499434b050343e81dabcb45b849c5f1fda29` 2026-08-20 11:28:57 -0400 ("Add the
game bones to the framework"). The sibling checkout `../mycelial-republic` sits at
the same commit and its tree is the OLD product shape: 225 tracked files
(`git ls-tree -r github/master --name-only | wc -l` = 225) with `framework/`,
`scaffolds/`, `scrum/`, `mycelia.cmd` - a different skeleton from today's estate.
`git rev-list --count github/master..HEAD` = **878**. So the operator's ask lands
on a 46-day-stalled push across a structural divergence: the public tree and the
estate no longer share a shape, and the push is effectively a re-seed of the
forest with the fortress's current body. One safety fact verified: hooks are live
(`git config core.hooksPath` = `githooks`), so a push today runs the pre-push
stack including the enforcing secret gate (`githooks/pre-push:400-407`, exit 1 on
provider-shaped secrets, fail-closed on scanner error) - the 2026-08-20 push
predated that gate (gate built 2026-09-27 per the hook's own comment block,
`watch/inbox/PACK_SECRET_GATE_20260926.md`).

## Finding 1 - the spore's first boot file is gitignored: the genome cannot regrow from a clone

`git check-ignore -v state/GENOME.md` returns `.gitignore:40:state/` - the entire
`state/` tree is ignored, and `git ls-files state/` tracks exactly ONE file
(`state/NIGHT_LOOP_20261005.md`, a today exception). state/GENOME.md declares
itself "The inheritable artifact" (line 1-6) and puts itself at step 1 of its own
boot order (GENOME.md:69-75: "1. This file. 2. queue/STANDING_RAILS.md. 3. The
ribs (memory/rib/). 4. state/CURRENT.md..."). The laws and rails underneath DO
ship: `git ls-files memory/rib/ | wc -l` = 55, all of `memory/rib_bus/` is
tracked (52+ files including doctrine.json, whose rib count I censused at
exactly 26 `"invariant"` entries - the topic's "26 doctrine ribs" confirmed), and
`queue/STANDING_RAILS.md` is tracked. But the file that ORDERS the cold boot is
untracked by the same .gitignore line that (correctly) keeps state/keys and
live state out. A GitHub clone regrows laws with no genome to sequence them.
Also lost to the same ignore: state/CURRENT.md (live truth, step 4 of boot).
Falsifier: if a tracked copy or a .gitignore negation for the genome already
exists elsewhere, this finding shrinks (my scope: check-ignore + ls-files on
state/, plus the tracked-file list above). Move (one edit, minutes): lift
GENOME.md (and a frozen CURRENT template) to a tracked path (`docs/spore/` or a
`!state/GENOME.md` negation), leaving live state ignored.

## Finding 2 - the strip law already exists three times over; the estate keeps re-deriving its own spore (SELF-STEAL, CONVERGENT)

Three prior generations answered "what gets stripped" and none was applied to
the real estate:
1. The doctrine line: docs/archive/ZEITGEIST.md non-negotiables, era 003:
   "ship code/practice, not residual by default" (Spine table). The compass
   pillar table goes further - "You can fork the repo and run :8765 without our
   permission" (docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md:40) and ".env secrets
   stay local" (:41). That IS the strip rule: code and law ship, residual stays.
2. The public-pack discipline: watch/inbox/SEED_PUBLIC_PACK_20260925.md - the
   seed-3.2.0/3.3.0 zips caught the build-junk author-path leak ("3 __pycache__
   .pyc files... contained C:\Users\foste\Documents\... Public share would have
   leaked the username + layout", :15-19), resealed 52/52, secret-grepped the
   round trip, MIT licensed, keys.json as an awaiting-operator template (:11-12).
3. The kernel format: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md - schema
   seed_rib.v0 with inline/pointer carriers, sha256 seals, <100KB budget,
   "a pointer is a promise with a hash, never a hand-wave" (:46-49),
   never-invent-bytes rebuild verifier (:64-76), dogfooded same day (:87-93)
   via tools/seed_rib.py. Its role taxonomy (law/doctrine/boot/receipt/ledger/
   pointer, :36-41) is literally the spore's manifest grammar.
Meanwhile the default push surface is the opposite of the doctrine: `git ls-files
watch/inbox/ | wc -l` = **17,069** tracked receipt files - personal receipts,
session trails, one tracked key-name receipt
(watch/inbox/burn_wave_20260926/B2_296_mistral_keys_20260926.md) - all of which
a normal `git push github` ships. Key hygiene checked, not assumed: `.env` was
NEVER committed on any ref (`git log --all --diff-filter=A -- .env` = empty),
`configs/keys.json` is tracked but its 28+ char strings are all status/role/law
prose (redacted scan: 3 long tokens, max 35 chars, all env-NAME references per
the file's own `_law` header "one key, one canonical name... Readers use
mag.key_law.get(name)"), and route_chat reads keys from env names then the
single ROOT/.env (mag/route_chat.py:66-71). The dormant-until-needed mechanism
the topic asks for is also already coded: providers.yaml lanes carry
`dormant: true` with "operator GO flips this" (e.g. :486, :571, :658, :706) and
route_chat's dormant gate refuses ungated lanes (mag/route_chat.py docstring
:14-15). Move (one sitting): assemble the spore as a seed_rib.v0 build whose
inline set is laws+ribs+genome(lifted per Finding 1)+rails+compass+constitution
pointer and whose pointer set is every ledger (gps_ledger.db3, usage.jsonl,
gwap chain), then run `tools/secret_gate.py` fulltree over the resulting tree -
the last fulltree run on record is watch/inbox/secret_gate_results/
fulltree_20260927.json (not re-run this sitting: OWED).

## Finding 3 - the N=2 break points are byte-verified; N=8 breaks on law consensus, not plumbing

Verified in code this sitting:
- GPS capability ledger: `CREATE TABLE capability (... PRIMARY KEY (model_id,
  task_shape))` with NO operator/seat/owner column anywhere in the schema
  (tools/gps_mcp/ledger.py:133-146). Two estates feeding one ledger collide on
  the same (model_id, task_shape) row; one operator's measured 7-fail streak
  (the D7 slashing case) would re-route the OTHER operator's dollars. And a
  forked pair cannot even pool receipts: no merge instrument exists (scoped
  grep for "merge" in tools/gps_mcp/ledger.py: zero hits; tools/gps_mcp/
  listing shows ledger/metabolism/router/coverage/providers/server only).
- Rib bus: `_save_store` is a full-file `write_text` over the domain JSON
  (mag/rib_bus.py:78-83) - last-writer-wins. The module's whole API surface is
  publish_rib/mount/inject_for/machine_lower/status (grep of `^def |^class `,
  mag/rib_bus.py:54-252); no claim, lease, or ownership primitive exists
  (scoped grep claim|lease|lock in that file returned prose lines 4 and 195
  only). Two operators mounting one cloned rib bus overwrite each other's ribs
  with no conflict signal; the verkle fold (AH19 minute-pin, :86-110) will even
  dedupe the collision into silence.
- Money: route_chat's key chain resolves from lane `api_key_envs` then the ONE
  repo-root .env (mag/route_chat.py:56-72); the descent ladder's funded budget
  is one operator's Nous credits plus XAI_SD (AGENTS driving-ladder block).
  N operators either share one keyring (one party pays for all, one 429-storm
  punishes all - the fan-out width law's envelope is per-account, AGENTS) or
  fork .env with no receipt-trade path between forks.
So: at N=2 the breaks are attribution, money, and write races. At N=8 the break
is law itself: doctrine ribs are published by an operator hand
(memory/rib_bus/doctrine.json entries carry source "foundational"/"instance:",
no quorum, no supersede vote; mag/republic.py's set-once superseded_by pattern
at :114 exists but has no live caller - confirmed by the eleven-doors lineage
lens, watch/inbox/ractor_engine/2026-10-04-eleven-doors/lineage.md:75-77, and
not re-grepped beyond that cite this sitting: OWED). The honest shape the
constitution already implies: per-estate ledgers (forks), receipts exchanged as
sealed artifacts, capability tables MERGED BY THE ROUTER at ask time instead of
shared at write time.
Falsifier: an operator_id/claim column or a ledger merge tool landing anywhere
would shrink this finding; my scopes (ledger.py schema, rib_bus.py API, gps_mcp
file listing) found none. Move (one sitting): add an `operator_id` column plus
per-operator unique index to the GPS schema (migration + test), and a
`--owner` field on rib publish rows - attribution before merge, the cheapest
honest multi-tenant step.

## Finding 4 - "what is the republic" was ruled on disk in August: forked estates over a shared frozen world, and the receipt-trade organ already exists as a dormant play

docs/ref/FORTRESS_AND_REPUBLIC.md (2026-08-09): the project runs "Fortress Mode
(Mag) inside a fork-equal civ (the Mycelial Republic - no canonical core, no
rank, anti-capture)" (:7-10); "the fortress (Mag) is one fort among many, all
fork-equal, joined by voluntary mycelial interconnect - not the 'true' world"
(:36-38); the shared world is "the common constitution + protocol + byte-anchored
state" (:60-63). The sibling constitution confirms it directly
(../mycelial-republic/docs/CONSTITUTION.md:15-22): "fork without begging a
core", §1.1 "No mirror, node, operator, or repo is canonical core", §1.4
interconnect must not hard-code a privileged registry. So the topic's three
options resolve as the second one plus a protocol: NOT one shared chain, NOT a
monorepo - forked estates trading SEALED RECEIPTS over a shared protocol
(constitution + seed_rib seals + verkle envelope shapes). And the estate even
built the trade organ's genre and left it dormant: mag/republic.py is a
correspondence engine - letters persisted APPEND-ONLY at
state/republic_letters.json, "a retracted letter is superseded_by another,
never deleted or edited" (docstring :14-17), forward() copies with
forwarded-from provenance (:19-21) - the Mersenne mailbox is exactly
receipt-trade between fork-equal citizens, currently a play organ (Fermat
letters, state/republic_letters.json head verified). The lineage irony: the
spore's transport protocol was built as theater before it was needed as law.
Move (one sitting, mostly prose): declare letters (or their schema) the
interconnect v0 - a receipt envelope = seed_rib pointer + signature - and name
it in the spore's regrow guide, instead of inventing a new exchange format.

## Finding 5 - the tutorial and regrow genres exist; the ask is assembly, not authorship

The tutorial mold: watch/inbox/ADAM_ONBOARDING_FULL_20260924.md - an 18-step
guide, each step with exact command, why, verification, gotcha, live-verified on
the target machine, with honest NOT-RUN reporting and the key discipline stated
in the text ("keys NOUS_SDD_API_KEY / NOUS_NACHO_API_KEY verified present in
.env - names only, I never read the values"). The ladder content the topic wants
already lives in law: the driving ladder rib (memory/rib/
RIB_DRIVING_LADDER_20260928.md, cited in AGENTS) plus providers.yaml lanes for
exactly the asked providers - deepseek (:359), openrouter (:170), the z_ai
family (:537-584, incl. dormant z_ai3) - and the dormant-GO mechanic (:486 etc.)
is the tutorial's real lesson: a new operator boots strongest with most lanes
dormant and three keys in .env. The regrow guide is GENOME.md section 3's boot
order (ribs -> rails -> CURRENT -> delta register) which the seed_rib v0.1
directory carrier already knows how to seal and rebuild. Nothing new must be
designed; two docs must be WRITTEN FROM existing bytes. Falsifier: if
providers.yaml lane names or the dormant-GO contract change before the tutorial
lands, its step list goes stale (it cites lanes by name). Move (one sitting):
draft `docs/spore/REGROW.md` and the Hermes ladder tutorial strictly as
pointers-plus-commands over existing lanes and the ADAM mold, no new mechanism.

## The topic term I could not find (honest absence, instruments named)

"Season ledger" / "season chain": no file, table, or doc by those names
surfaced in the scopes I ran - `grep -rn season` over mag/*.py (prose hits
only: bard.py:925, water_computer.py:444,571 et al.), tools/*.py top level
(dungeon.py:715 "the season continues" is a play verdict), memory/*.md top
level (none), the 2026-10-05 ouroboros synthesis (none), and directory
listings of state/, memory/, queue/, docs/, tools/. Closest real organs: the
GPS capability ledger (tools/gps_mcp/gps_ledger.db3), the gwap SessionLedger
"arena-capability" (tools/arena_gwap.py:29,57), state/organ_vitals_chain.json,
memory/seed_chain/seeds.jsonl, and state/republic_letters.json. The topic's
single-party assumption is TRUE of all of these (none carries an operator
column - verified for the GPS schema; OWED for organ_vitals_chain and
seed_chain, whose schemas I did not open). If "season ledger" names one of
these under a private register, the N-operator analysis above transfers
unchanged; if it names a byte I never opened, that row is OWED.

## What the current wave dropped between generations (the lineage ledger)

- 2026-09-25/26: the seed line (SEED_PUBLIC_PACK, seed_rib v0, tools/seed_rib.py,
  tools/build_seed.py, tools/cold_boot_test.py per the subsystems map,
  watch/inbox/subsystems_map_20261002.md:62) - built, dogfooded, then dropped;
  the estate kept growing while the spore stayed 3.3.0, 102KB, a different tree.
- 2026-08-20: the forest push stalled at dc66499; nothing since references a
  sync cadence (scoped: docs/ files mentioning mycelial-republic are design
  docs, not runbooks - AUDIT.md, ORG_ROADMAP.md, CONTAINER.md, DOCTRINE_MAP.md,
  FORTRESS_AND_REPUBLIC.md, GSTDCOIN_REPOS_INDEX.md heads seen in a filename
  grep only: OWED on their contents except FORTRESS_AND_REPUBLIC, read here).
- 2026-10-04 eleven-doors ractor: its lineage lens flagged queue staleness and
  the republic.py dormant supersede pattern (lineage.md:75-96) - the exact
  primitives a multi-operator spore needs - and the wave spent its budget on
  doors D5-D7/D6/EG-20 (per the commit log), leaving interconnect unbuilt.
- Tonight's NIGHT_LOOP (state/NIGHT_LOOP_20261005.md:31-32): "Operator asleep:
  no operator-gated action fires (no pushes beyond the backup pattern)" - the
  actual push is operator-gated and must NOT fire tonight; this lens stages,
  it does not push.

## One-sitting order (cheapest first)

1. (minutes, Finding 1) Track the genome: negation or docs/spore/ copy.
2. (one sitting, Finding 5) Write REGROW.md + the ladder tutorial from
   existing bytes, ADAM mold, lanes by name.
3. (one sitting, Finding 2) Author the spore manifest as seed_rib.v0
   (inline: laws/ribs/rails/genome/compass; pointer: every ledger and the
   inbox), run the fulltree secret gate on the result.
4. (one sitting, Finding 3) GPS operator_id column + rib publish --owner:
   attribution first, merge later.
5. (operator-gated) The push itself: a spore branch force-re-pointed at the
   225-file forest, or a fresh forest repo - the constitution's own anti-
   canonical rule (§1.1) says the old 225-file tree is not sacred.
