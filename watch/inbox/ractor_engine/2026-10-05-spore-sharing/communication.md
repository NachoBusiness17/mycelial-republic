# SPORE SHARING - THE COMMUNICATION LENS (2026-10-05)

Lens frame: communication is judged at the RECEIVER. For a spore the receiver
is a cold second operator and the channel is the GitHub repo; the estate's own
rule is that every act banks a receipt (state/GENOME.md:28-29, queue/STANDING_RAILS.md:30-31).
I checked what the channel actually carries and what the receipts actually say,
against what the topic claims the spore is. Every claim below cites a file I
read or a command I ran this session; anything I could not verify is OWED.

## F1. THE CHANNEL CARRIES THE PRE-GENOME MACHINE

github.com/NachoBusiness17/mycelial-republic is live (git ls-remote github:
refs/heads/master at dc66499, the only branch; 13 commits per the web view).
Its tip is NOT in this repo's history (git log dc66499 fails locally): it is
pushed from the sibling checkout C:/Users/foste/Documents/projects/mycelial-republic
(its origin remote is the same URL, its log tip is dc66499 "Add the game bones
to the framework"). What master ships: framework/mag/ = 43 old-core modules
(game_dm.py, game_ramp.py, ghost.py, verkle_knot.py, rib_bus.py, swarm_worker.py,
memweave.py), framework/configs/ = cost_rates/data_tiers/features/lanes/mag/
modules/releases/router_policy YAMLs, plus the mirror-training project (README
Phase 0 Seed Mirror, src/mycelial_republic data prep, QLoRA stub).

What it does NOT ship (find over the sibling tree for *GENOME* / *STANDING_RAILS*
/ *parable* / *.env* returned nothing; ls framework/mag/ has no route_chat.py,
no arena_gwap.py, no ds_workhorse.py, no tavern/dungeon/grok_burn, no gps_mcp;
ls framework/configs/ has no providers.yaml): the 2026-10-03 rails day, the
genome, the doctrine ribs, the carriers, the GPS routing. framework/README.md
says it outright: "Private, never here: the runtime memory (memory/), the
persona, the biography, providers.yaml, mag-secret.yaml".

The break is concrete: shipped framework/mag/rib_bus.py:48 points RIB_DIR at
ROOT / "memory" / "rib_bus", and no memory/ ships, so mount() on any fork loads
ZERO ribs. The topic's premise (genome + rails + carriers + ribs as the seed)
and the channel's contents are different machines. The regrow guide cannot be
written against this tree: the only boot order that exists (state/GENOME.md:69-75,
section 3) lives in a file the repo does not carry, and the sibling's docs/
FIRST_STEPS.md walks the mirror-training quickstart, not the estate boot.

Falsifier: a second branch or unlisted subdir carries the genome (ls-remote
showed exactly one branch; I listed framework/ and docs/ roots directly).
Move (one sitting, ~45 min): a SPORE_MANIFEST.md diff - the topic's
strip/stay/dormant table checked line-by-line against the shipped tree, naming
every promised organ that is absent.

## F2. THE SHARE ITSELF IS UNBANKED

grep -ril "spore|mycelial-republic|NachoBusiness17" over watch/inbox/ matched
only AEOLIPILE_SPORE_20260922.md and .mimosa hook-state baseline snapshots; no
receipt in the estate's shared inbox names the push, the secret scan, or the
dc66499 tip. memory/zknot/LATEST.md and state/*.md are likewise silent on the
push act (state/_astra_triangulation.md references the republic as a concept,
never the push). The estate's law 4, "if it ran, it banks" (state/GENOME.md:28-29;
queue/STANDING_RAILS.md:30-31), is violated by the single most outward-facing
act in the estate's history: the core went public, and the only record is a
commit message in a sibling repo that estate audits never read.

Because no scan receipt exists, I re-ran a scan myself this session over the
sibling working tree: 5 key-shaped patterns (sk-, xai-, AIza, Bearer + long
token, API_KEY="...") across py/yaml/md/json/txt/cmd/ps1 returned zero matches;
sibling .gitignore:41-42 blocks .env and .env.*; providers.yaml and
mag-secret.yaml are absent from framework/configs/ (ls). Caveat: that covers
the working tree only, not the 13 commits' history (old-commit leak scan: OWED).
Also checked the estate side: configs/keys.json IS tracked in local git, but it
is a key LEDGER not a secret store (fields env/provider/role/ceiling; zero
credential-shaped values per grep -c; zai_lite entry = {env, provider, role,
ceiling}); the raw keys live in .env which is untracked (git ls-files shows
.env.example only). So a naive future push of THIS repo leaks ceilings and key
roles, not raw keys.

Falsifier: a receipt exists in corpus/, memory/rib/, or dashboard/ that my
inbox-and-zknot grep did not cover. Move (15 min): land SPORE_PUSH_RECEIPT.md
naming the tip (dc66499), the scan instrument and result, and what was
deliberately excluded.

## F3. THE N-OPERATOR SEAMS ARE CONCRETE ON SHARED ESTATES, MERGE-SHAPED ACROSS FORKS

Four seams read from code this session:

(a) The rib bus write is a bare overwrite: mag/rib_bus.py:81 is
f.write_text(json.dumps(store...)) with no lock, no temp+rename. Two operators
publishing to one domain on one estate lose rows or tear the JSON.

(b) Lane runners hold claimless file-offset cursors: queue/lanes/builder/
runner_state.json is {"inbox_offset": 13, "seat": "builder"} - no owner, no
lease. Two runners on one lane double-consume and clobber each other's offset.
The topic's "rib bus has no claim system" generalizes: the lane layer has none
either.

(c) The wallet is single-tenant: route_chat resolves every lane's key from
os.environ then ROOT/.env only (mag/route_chat.py:56-72, the _keys_for chain)
and banks usage to one per-lane file, memory/runs/route_chat/usage.jsonl
(mag/route_chat.py:46), with no operator field. Eight operators on one checkout
share one wallet and no per-operator metering. providers.yaml confirms the
chain shape: api_key_envs lists like [HERMES_API_KEY_1, HERMES_API_KEY_2]
(providers.yaml:158), ZAI_API_KEY_Lite (:575) - names, not namespaces.

(d) The GPS capability ledger collapses parties: upsert_measurement conflicts
on (model_id, task_shape) alone (tools/gps_mcp/ledger.py:598-612, ON CONFLICT
DO UPDATE, no operator_id column) - two estates' measurements of the same pair
merge last-writer-wins.

Shape law this implies: at N=2 on SEPARATE forks, seams (a)-(c) vanish (each
clone owns its .env, its db3, its rib_bus) and what breaks is (d) plus receipt
exchange, which has no mechanism at all (F5). At N=2 on ONE shared estate,
(a)-(d) all fire. The shareable design should therefore target the fork shape
and treat the shared estate as the special case needing a claim system, not the
other way round.

Falsifier: a lock or lease exists in the publish/runner paths I did not read,
or usage.jsonl gains an operator column written elsewhere. Move (~40 min): one
design row - operator_id on usage + capability rows, atomic write for rib_bus -
in the same register the ractor already runs.

## F4. THE TUTORIAL IS A COMPILATION JOB; ITS PRICE CLAIM IS OWED

The ladder's bytes all exist, scattered: watch/inbox/burn_reset_20260927/flash50/
free-lane-map.md (census 2026-09-28: 28 provider blocks, 62 model rows, 13 ":free"
ids, and the header law at configs/providers.yaml:4-6 that free tiers do not
expose remaining-until-reset so Mag tracks local period+limits), the lane env
chains in configs/providers.yaml, the drop-in table in queue/STANDING_RAILS.md:33-46,
the driving-ladder and descent laws, and the z.ai-lite state line
(state/CURRENT.md:34-38: z_ai3 dormant, .env key commented). No single
cold-operator boot doc exists: grep for z.ai-lite/tutorial surfaces across docs/
and watch/inbox/ returns only the census docs, and the sibling's FIRST_STEPS.md
is the mirror-training quickstart, not a keys-to-rails boot.

The topic's "~5% of paid" figure for the free-lane ladder: OWED. No receipt I
found prices it; I ran no lane this session and will not assert a number.
Free-lane-map.md itself models the honesty: "anything I did not measure is
labeled as a recorded claim, not a live verdict."

Falsifier: a priced boot tutorial already exists somewhere outside docs/ and
watch/inbox/. Move (60 min): SPORE_TUTORIAL.md as a citation-dense compile -
keys, z.ai-lite monthly, OpenRouter, free lanes, then route_chat as the one
door - with the price table marked OWED until a first measured month banks.

## F5. THE REPUBLIC'S SHAPE IS ALREADY DECIDED IN-STATE; THE TRADE EDGE IS UNBUILT

The topic asks what the mycelial republic IS. The estate has answered this
before: state/_astra_triangulation.md:1389 "Federalism: Mag (private office) +
mycelial-republic (public fork)"; :756 "Forest | mycelial-republic | Public
law, fork, optional republic train". The sibling README: "Spores replicate.
Nodes interconnect." The sibling framework/README: "Steal the mechanism, never
the content." So the intended shape is neither a shared chain nor a metaphor:
it is forked estates, local verkle chains, trading receipts as tribute. The
doctrine ribs say the same in invariant form (memory/rib_bus/doctrine.json,
7538cbc5: seats coordinated by deterministic instructions on crypto primitives
every seat trusts).

But the trade edge does not exist. The only edge today is the one-way push; ls
scripts/ | grep for sync/pull/republic/spore/mirror/push returns only unrelated
pull_* scripts for other projects; no cross-repo receipt xref mechanism exists.
Worse, the in-state pointer at state/_astra_triangulation.md:1252 still cites
the OLD URL github.com/NachoBusiness17/Mag while the live repo is
NachoBusiness17/mycelial-republic (ls-remote verified this session): the estate's
own map of the republic points at a dead address. A republic of estates that
cannot pull each other's receipts is a directory of solo estates with a shared
birth certificate.

Falsifier: a republic-sync organ exists as a mag/ module or cron task outside
scripts/. Move (45 min): name the trade protocol in one row - receipt xref
format (estate-id + chain tip + path) and a pull cadence - and fix the stale
URL, before a second operator exists to need it.

## ANSWERS TO THE FIVE QUESTIONS (lens-qualified)

1. De-riddled share: the strip list is real and mostly enforced (.env untracked,
   sibling .gitignore blocks .env.*, providers.yaml/mag-secret.yaml withheld,
   keys.json is a metadata ledger with zero credential values - all verified
   this session). But the stay list is NOT in the channel: genome, rails, ribs,
   carriers, parable, GPS are absent from master (F1). Dormant-until-needed
   subsystems would land as code without their ribs, which is how the hollow
   batch was born the first time.
2. N operators: fork shape survives N=2..8 with the wallet and claim seams
   dormant per-estate (F3); the shared estate breaks at N=2 on four named seams;
   the cross-estate trade breaks at any N because the edge is unbuilt (F5).
3. Tutorial: compile task, price OWED (F4).
4. Regrow guide: cannot be written against master as shipped; GENOME section 3
   (state/GENOME.md:69-75) is the in-state boot order that never made the spore.
5. Republic: federalism of forked estates trading receipts, decided in-state,
   unbuilt at the edge (F5).

## BLIND SPOTS (honest)

- I priced nothing and fired no lane: every cost statement is a citation, and
  the "~5% of paid" figure stays OWED.
- My secret scan covered the sibling working tree, not its 13-commit history;
  an old-commit leak scan is OWED (git log -p | scan in one sitting).
- The topic statement is my only source for the operator's intent; I cannot
  read the operator, and other lenses may hold direct quotes I lack.
- I read the four named organs plus targeted greps, not the full ~700-module
  mag/ tree: other T0/T1 surfaces (dossier .md files, biography, trails) may
  ride in tracked paths I never enumerated for export.
- The seams in F3 are read from code paths, not reproduced live with two
  concurrent writers; a 2-operator chaos test is not run.
- Non-code receiver surfaces (dashboard UI, lan_proxy, the game client) were
  out of lens; a new operator might reach the estate through doors I never
  opened.

Filed by the communication lens, 2026-10-05. Instrument note: all greps ran
untruncated over the named scopes; absence claims above name their grep and
scope. No em-dashes. Anything unverified is marked OWED, not asserted.

## ERRATA (2026-10-05, hostile second pass: F1/F2/F4 verdicted weakened; re-verified this session)

The lens audited the WRONG CHANNEL and one grep was instrument-broken. What
the re-check found, every line from a command run this session:

1. The account carries FOUR repos (gh repo list NachoBusiness17): mag-sovereign-seed
   (PUBLIC, "The Mag Seed ... constitution, organs, manual, and stories", pushed
   2026-10-04T23:40:58Z, main cbda4d82, tag v1.0.0, 1,798 tree entries per
   gh api .../git-trees/main?recursive=1), mycelial-republic (the 08-20 practice
   surface, dc66499), the-mountain (private), embassy-aos (public). F1/F4's
   absence claims were re-proven against the SEED tree, not just the sibling:
   the only "GENOME" matches in all 1,798 paths are docs/ref/verb_genomes/*;
   zero matches for route_chat, providers.yaml, STANDING_RAILS, rib_bus
   doctrine.json, gps_mcp, arena_gwap, ds_workhorse, grok_burn,
   FIELD_AND_THE_STONES; zero .env/providers paths (grep rc=1). The mount-zero
   claim transfers: fetched mag/rib_bus.py:48 = RIB_DIR = ROOT / "memory" /
   "rib_bus", and the shipped memory/ = MEMORY.md, briefs/, doctrine/ only.
2. Root cause surfaced: seed PROVENANCE.md (in-repo, fetched) anchors the export
   2026-09-30 (verkle tip 00e374bd..., 8,692 leaves) - the genome day (10-03)
   and rails day postdate the export by 3 days. The seed is stale against its
   own push date; the strongest version is in NEITHER public repo.
3. F2 withdrawn in its strong form. The push and scan ARE banked:
   watch/inbox/audit_20260926/LANE4B_UNVERSIONED_RISK.md table row
   "mycelial-republic | dc66499 | 2026-08-20"; corpus/oral_history/marathon_body/
   marathon_25fbcaab_20260815_20260820.jsonl (3 hits of dc66499 incl
   "3da416c..dc66499 master -> master ... No pyc staged");
   watch/inbox/full_width_fold_20261002.md:~74 ("mag-sovereign-seed repo LIVE
   (four-repo estate under NachoBusiness17)"); watch/inbox/STARTER_KIT_50WIDE_20261004.md
   (long-form estate receipt: shippable-with-fixes, 15 release blockers); and the
   seed's own PROVENANCE.md carries the full three-tier secrets audit with
   instrument, hit counts (7/14/8), dispositions, "zero live secret values".
   My original grep claim ("matched only AEOLIPILE + .mimosa") was FALSE as an
   instrument statement: the tool output was silently truncated. Re-run counts
   (recursive watch/inbox, .mimosa excluded): 38 files match NachoBusiness17,
   99 match mycelial-republic. Surviving kernel: no single estate receipt names
   the 10-04 SEED push with tip cbda4d82 and links the PROVENANCE audit; and no
   receipt flags the 09-30-anchor vs 10-04-push staleness gap.
4. F1 nits conceded: sibling framework/mag has 44 .py files (ls | wc -l), not 43;
   dc66499 IS a local object now (git rev-parse --verify dc66499^{commit} rc=0,
   cat-file = commit, merge-base --is-ancestor HEAD rc=1, i.e. dangling) though
   my first identical git log call failed with "unknown revision" earlier this
   session - unreconstructable (plausibly a sibling seat fetched between calls;
   multi-seat estate, runner states ticking), reported as two moments, current
   byte-truth standing.
5. F4 corrected: the tutorial EXISTS - starter-kit/tutorial/TUTORIAL.md (three
   lessons, fetched and read) + INSTALL.md (free-tier ladder: OpenRouter 50/day,
   $10 credit lifts to 1,000/day; Groq ~200K tok/day; Gemini free; one-.env key
   law at step 4) + integrations/hermes/README.md - and the estate already
   50-wide-dogfooded it (STARTER_KIT receipt). "No single cold-operator boot doc
   exists" is withdrawn. Surviving: the PAID ladder (DeepSeek keys, z.ai-lite
   monthly, descent-protocol judgment spend) is absent from the kit (deepseek/
   zai/descent: 0 hits in SUBSYSTEMS.md, integrations/hermes/README.md, BOOT.md;
   1 hit in INSTALL.md = the OpenRouter free line), the "~5% of paid" figure
   stays OWED, and the dogfood's blocker-fix state on current main is OWED
   (tree now shows starter-kit/skills/*/SKILL.md, so dogfood blocker D1's
   empty-dirs state is not what ships now; other blockers unverified).
   Discrepancy logged, unresolved: the dogfood cites starter-kit/.env.example:10-12;
   the current main tree lists no .env.example (my grep rc=1) - one of the two
   instruments is stale and I cannot tell which from here.

