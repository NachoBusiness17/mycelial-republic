# DOGFOOD LENS - THE SPORE SHARING PROBLEM (2026-10-05)

Lens: dogfood / organ mapper. Jacket: the finding filed but never wired.
Every claim below was personally read or run this session, 2026-10-05, seat
zcode. Universal claims are scoped to the exact commands shown. No em-dashes.

## 0. THE HEADLINE

The spore already has a name, a remote, an identity organ, and a builder.
None of them are wired to each other. `git remote -v` shows `github` ->
https://github.com/NachoBusiness17/mycelial-republic.git (run this session).
`mag/constants.py:6` defines `SPORE_SEED_FILE = memory/spore_seeds/{seat_id}.jsonl`
and `mag/spore_seed.py:42-80` generates per-seat seeds anchored to the verkle
chain tip. `scripts/build_travel_kit.py:1-16` builds "the portable bag a cold
machine boots the fleet from". But the genome the spore exists to carry is
gitignored, the GitHub repo holds a 1-commit stub from August, and the one
builder that exists is a twin-machine sync tool that deliberately ships `.env`
and excludes `state/`. Four spore organs, zero connective tissue.

## 1. WHAT I CHECKED (commands as run)

- `git check-ignore -v state/GENOME.md queue/STANDING_RAILS.md memory/rib_bus/doctrine.json watch/inbox/INDEX.json`
  -> `.gitignore:40: state/  state/GENOME.md` and INDEX.json ignored;
  STANDING_RAILS.md and doctrine.json tracked.
- `git ls-files | wc -l` -> 56,359 tracked files.
- `git ls-files watch/inbox/ | wc -l` -> 17,069 tracked receipt files.
- `git ls-files state/` -> exactly one file: `state/NIGHT_LOOP_20261005.md`.
- `git rev-list --count` -> main: 5, github/master: 1, HEAD (work branch):
  878. `git ls-remote --heads github` -> one head, `dc6649943 refs/heads/master`.
- `git log dc6649943 -1` -> 2026-08-20 "Add the game bones to the framework:
  game_world/campaign/narrate/dm/saga/score/ramp/observer + map/render
  (distributed collaborative storytelling)". `git remote show github` ->
  "master pushes to master (local out of date)".
- `git ls-files tools/gps_mcp/gps_ledger.db3` -> tracked (the production
  capability sqlite ships in any push).
- `grep -oE "^[A-Z_0-9]+=" .env | sed 's/=$//'` -> 39+ key families including
  HERMES_API_KEY_1/2, ZAI_API_KEY_1/2/3, OPENROUTER_API_KEY_2, GROQ_API_KEY_2,
  XAI_SD_API_KEY (names only read; no values printed). `.env.example` (cat,
  347 bytes) carries 13 flat slots and none of HERMES/ZAI/XAI_SD/second keys.
- `watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json` (venv python
  json read): scopes corpus/ + watch/inbox/, 46,996 files scanned, rule_counts
  OPENAI-CLASSIC 14, OPENROUTER-KEY 28, GROQ-KEY 28, XAI-KEY 18,
  DEEPSEEK-KEY 16, STRIPE-KEY 7, GENERIC-KEYASSIGN 189; `severity_counts`
  and `blocking_count` are null/absent in that artifact. Newest changed-file
  gate `watch/inbox/secret_gate_results/changed_20261005T080433Z.json`:
  28 files, blocking_count 0.
- Read: state/GENOME.md, queue/STANDING_RAILS.md, state/CURRENT.md,
  .env.example, scripts/build_travel_kit.py, mag/route_chat.py (env reads +
  _bank), mag/lane_runner.py:120-149, mag/spore_seed.py,
  watch/inbox/THE_FIRST_SEASON_story_20261003.md,
  watch/inbox/SHARED_SURFACE_CONTRACT.json, memory/spore_seeds/*.jsonl.
- `ls docs/ | grep -iE "spore|regrow|tutorial|onboard|seed"` -> empty. No
  regrow guide or tutorial exists in docs/.
- `ls watch/inbox/ractor_engine/2026-10-05-spore-sharing/` at lens start ->
  No such file or directory (first writer).

## 2. THE MAP ONTO THE ORGANS (dogfood jacket: filed but never wired)

- **Genome (state/GENOME.md)** declares itself "The inheritable artifact"
  (line 1-3) with a boot order (section 3). Filed. Not wired: gitignored via
  .gitignore:40, so the declared transport (git) cannot carry it. The
  inheritance clause is prose pointing at a file the pipe drops.
- **Rails (queue/STANDING_RAILS.md)** : tracked, travels. Its drop-in table
  is the regrower's day-one surface and needs no strip. Wired.
- **Rib bus (memory/rib_bus/, 51 files incl doctrine.json + standing-wave.json
  104KB)** : fully tracked, travels. Wired.
- **Route_chat (mag/route_chat.py)** : the one model-call door reads lane
  api_key_envs from os.environ then falls back to parsing `ROOT/.env` line by
  line (lines 61-70). Single-tenant by construction: one file, no operator
  dimension. The usage bank row (lines 211-215) carries ts/lane/model/goal/
  tokens/ok/error and NO operator or seat field. The everything-banks law
  banks WHAT was spent but never WHO spent it.
- **GPS capability ledger (tools/gps_mcp/)** : one sqlite
  (default "package-local gps_ledger.db3", tools/gps_mcp/seed_fixtures.py:105;
  production copy tracked at tools/gps_mcp/gps_ledger.db3). No seat/operator
  columns surfaced in ledger.py greps this session. At N seats the measured
  capability truth forks silently: two clones each believe their own rates.
- **Spore seed (mag/spore_seed.py)** : seat_id + sha256 seed + chain root,
  per-seat append-only log. This is the EXISTING multi-operator identity
  primitive. Its repair receipt (lines 6-15) admits it had never executed
  until 2026-09-25. Identity: filed. Not wired into route_chat, the ledger,
  or the lanes.
- **Travel kit (scripts/build_travel_kit.py)** : DIR_INCLUDES (lines 34-37)
  covers mag/tools/configs/queue/docs/tests/prompts/packs/handoff/research/
  dashboard/training/models and NOT state/; MEMORY_EXCLUDE (lines 40-45)
  excludes 15 memory subtrees and even names `spore_seeds`. Its docstring
  (line 4) ships "code + live ledgers + packs + .env" - the correct design
  for moving YOUR estate to YOUR second machine, the exact wrong design for
  a public spore. One builder, two opposite missions, zero mode flag.
- **Shared surface contract (watch/inbox/SHARED_SURFACE_CONTRACT.json)** :
  canonical host path is hard-coded `C:/Users/foste/...` in the JSON itself.
  A regrower inherits a contract pointing at someone else's home directory.
- **Season ledger (tools/dungeon.py + tavern.py)** : per-session dirs with
  golden_vectors.json + transcript.jsonl (dungeon.py:183-193); the campaign
  chains through the party subchain tip (dungeon.py:63, :736 --tip genesis
  default). Season persistence across sessions is MAP TO BETTER item 2 in
  THE_FIRST_SEASON_story_20261003.md ("the save file is the chain") -
  designed, deliberately not built. The topic's "season ledger assumes one
  party" is true but downstream: the ledger itself does not exist yet, so
  multi-party season conflict cannot break what is not there.

## 3. WHAT BREAKS AT N (scoped answers, not vibes)

- **N=2, same seat**: shared single .env (route_chat.py:67-70) means one
  funded budget, zero attribution (bank rows carry no operator field,
  route_chat.py:211-215). queue/lanes/*/runner_state.json is a per-lane file
  whose saves are atomic but lock-free - mag/lane_runner.py:134-139 says so
  in its own comment ("the lock is external and transient, not code-side").
  Two operator processes on one lane are last-writer-wins.
- **N=2, two seats**: the GPS ledger forks (no sync organ found this session;
  scoped: no cross-seat sync mechanism surfaced in tools/gps_mcp/ or mag/
  greps). Routing decisions diverge per clone while both cite "measured
  capability". The genome forks too - state/ is untracked, so each clone's
  selection history diverges with no chain to reconcile. The spore_seed
  organ is the fix-shaped hole: seeds are per-seat and chain-anchored, but
  nothing reads two seeds and reconciles.
- **N=8**: everything above plus the season (when built) and the arena cron
  contending on one shared watch/inbox; the 17k tracked receipts turn every
  clone into a full personal-history mirror, which is a privacy surface, not
  a sync surface.

## 4. WHAT THE REPUBLIC IS (evidence-backed answer to question 5)

Today it is neither a shared chain nor forked estates trading receipts. It is
ONE estate with (a) a GitHub remote named mycelial-republic holding an August
stub of the older storytelling-framework era (dc6649943, disjoint history:
main has 5 commits, github/master 1, merge-base empty this session), (b) a
per-seat seed organ binding identities to the chain root, and (c) a
twin-machine kit for the same operator. AGENTS.md's zeitgeist line "beads
(this repo) + forest (mycelial-republic)" names the ambition; the bytes show
single-operator, multi-seat, unshared. The honest regrow story is FORKED
ESTATES: genome commit as common ancestor, per-seat spore seed, receipts
traded as bounded pointers + hashes (the shared-surface contract's own law:
"Prefer an artifact plus bounded pointers and hashes over a copied
transcript"). The receipt-trade protocol is the missing organ.

## 5. OWED (could not verify this session; not asserted)

- Whether any tracked file contains a LIVE secret: B2-73 banked rule hits
  (14 OPENAI-CLASSIC etc.) but its artifact carries no severity/blocking
  adjudication, and I did not run a full-tree gate pass. Running
  tools/secret_gate.py in full tracked-tree mode is a pre-push gate for the
  spore branch, not done here.
- Whether GitHub holds branches/tags beyond the one head (ls-remote --heads
  showed only master; tags not enumerated).
- The 878-commit work branch has never been pushed anywhere but the local
  backup remote (git branch -r shows only github/master and one local/* ref);
  disaster exposure, not just sharing exposure.

## 6. ONE-SITTING MOVES (each costed, each wired to an organ)

1. **scripts/build_spore.py --manifest** (30-45 min): allowlist emit of
   genome + rails + rib_bus + 26 doctrine ribs + carriers + parable +
   .env.example-v2 (HERMES/ZAI/XAI_SD second-key slots added). Organ: genome.
2. **operator field in the route_chat bank row** (15 min + 1 test): source
   MAG_SEAT_ID env, default from spore seed seat_id. Organ: route_chat. This
   is the smallest wire that makes every N-question measurable.
3. **Full-tree secret gate pass on the spore allowlist** (30-60 min):
   blocking_count 0 or accept-by-name before any push. Organ: librarian.
4. **docs/SPORE_REGROW.md** (60-90 min): boot order (GENOME section 3),
   rails default, dormant-until-keyed list (hermes_burn, descent, arena cron),
   the free-lane tutorial (~5% of paid ladder), receipt-trade sketch. Organ:
   context pack. The material exists scattered in 6 receipts; nothing
   assembles it.

Filed by the dogfood lens, 2026-10-05. Every path:line above was opened this
session. Nothing asserted beyond it except what is stamped OWED.
