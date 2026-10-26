# MOONSHOT-1: THE SPORE SHARING PROBLEM (2026-10-05, ractor-engine lens)

Lens: moonshot. No sacred cows - the single-operator assumption, the .env model,
GitHub-as-surface, and shareability itself all went under the knife. Every claim
below was personally verified this sitting unless marked OWED/GIVEN.

## THE HEADLINE

The operator's GitHub push is re-litigating a decision the estate already made
on 2026-09-19, and the spore as-shaped is INVERTED: the one file the topic
calls the seed (state/GENOME.md, "The inheritable artifact",
state/GENOME.md:1-3) is gitignored, while 47k+ files of personal scar tissue
are tracked and would ride. And the remote named `github` in this repo's config
does not even point at a home for the estate: it points at the forest.

## FINDING 1 - The shareable surface is inverted: genome ignored, scars tracked

- `git check-ignore -v state/GENOME.md` returns `.gitignore:40:state/
  state/GENOME.md` (rc=0): the declared "inheritable artifact" does not ride
  any push. Meanwhile `queue/STANDING_RAILS.md` is tracked (check-ignore rc=1),
  `memory/rib/` is tracked, `corpus/canon/` (the parable) is tracked.
- The tracked tree is 56,359 files (`git ls-files | wc -l`): memory 26,749,
  watch 20,359 (watch/inbox alone 17,069 - personal receipts), dist_audit
  1,496 (a previous audit dump), plus 19 files under memory/agent_uploads/
  including the operator's stt-*.webm voice recordings (`git ls-files
  memory/agent_uploads/ | wc -l` -> 19).
- Proof the ignore is soft: `git ls-files state/` shows exactly one file,
  state/NIGHT_LOOP_20261005.md - someone force-added it past the same
  `state/**/*` rule that buries the genome. One `git add -f` away is all it
  ever was.
- Falsifier: `git check-ignore state/GENOME.md` silent AND
  `git ls-files watch/inbox/ | wc -l` near zero.
- Move (one sitting, ~30 min): whitelist the genome through the ignore
  (`!state/GENOME.md`), `git rm --cached` the 19 voice uploads and dist_audit/,
  and declare `git ls-files` the spore manifest - the de-riddle is a diff, not
  a project.

## FINDING 2 - GitHub cannot be the vessel: 14.37 GiB, 100MB+ blobs, and the
remote points at the WRONG repo

- `git count-objects -vH`: size-pack 14.37 GiB, plus 4 tmp_pack garbage files.
- The fat is still in history: `git log --oneline --all --
  dashboard/data/ractor_board.jsonl.runaway-evidence-20260903` -> 60b1bde7f
  (the 2.2 GB blob's path, named in the sync doc).
- This was already litigated: watch/inbox/TWO_MACHINE_SYNC_20260919.md -
  "GitHub private repo was evaluated and rejected... 54 blobs over GitHub's
  hard 100 MB limit... Do not push this repo's history to GitHub as-is; the
  push will be rejected and any rewrite breaks receipt hashes." The receipt-
  hash law is the deeper blocker: history surgery falsifies the commit hashes
  the fleet files as provenance (proven by the 09-30 emergency:
  watch/inbox/DAY_SYNTHESIS_20260930.md:7-12 - 7 live API keys rode
  steps.jsonl through 64 commits and were cut by filter-repo only under
  explicit operator GO).
- The configured remote is the wrong repo: `git ls-remote github` (run with
  GIT_TERMINAL_PROMPT=0) returns dc66499434b050343e81dabcb45b849c5f1fda29
  refs/heads/master; after `git fetch github master --depth=1` that commit
  reads "2026-08-20 Add the game bones to the framework" with a 225-file tree
  (src/, framework/, mycelia.cmd, scaffolds/, scrum/) that shares nothing with
  this repo - and `git cat-file -t dc664994` fails locally: unrelated lineage.
  Pushing the estate there means force-clobbering the forest or refusing.
- Key-status OWED: AG1_SECRETS_CONTAINMENT.md:25 says the 7 leaked keys
  "remain in git history... until rotation"; whether the operator ever rotated
  them at the providers is NOT verifiable from this repo.
- Falsifier: a pack under 2 GiB, zero >100 MB blobs, and a github remote whose
  master ancestry contains local main.
- Move (~2 h): stop aiming GitHub at the estate's history. Mint the spore as an
  ORPHAN BRANCH (git checkout --orphan spore) carrying code + laws + ribs +
  genome + rails + canon + regrow guide only - no history surgery, the local
  receipt-hash chain untouched - pushed as a brand-new repo. Night-loop law
  (state/NIGHT_LOOP_20261005.md:30-32: "no pushes beyond the backup pattern"
  while the operator sleeps) makes this operator-gated.

## FINDING 3 - Multi-tenant breaks at the money and the steering, not the tools

- Usage banking is party-blind: a memory/runs/hermes_burn/usage.jsonl row has
  exactly [completion_tokens, cost_usd, id, model, ok, prompt_tokens, ts,
  turn] (extracted this sitting). Two operators sharing an estate cannot
  attribute a cent.
- The steering bus is one-voice: mag/rib_bus.py:195-196 - "canonical steer
  block (frontier invariants + operator directives + domain RIBs + grokbot
  seat directives) rides on EVERY task through this ONE drop-in." At N=2,
  whose directives? No claim/lease system exists (grep over mag/rib_bus.py for
  claim/lease/lock matches only prose lines 4 and 195) - true, but under the
  fork model the bus is per-estate anyway and needs none.
- The key door is single-tenant by construction: mag/route_chat.py:61-70 reads
  os.environ then exactly ROOT/.env; providers.yaml (gitignored, 36 lanes)
  encodes ONE operator's funded accounts (nous line 150, xai line 41; the
  driving ladder's $180 Nous credits and xAI SD account are personal).
- The GPS capability ledger (tools/gps_mcp/ledger.py:10-27) keys capability by
  (model_id, task_shape) with cost_usd_per_call and NO operator column - which
  is CORRECT under forks (capability truth is universal) and meaningless under
  a shared estate. :329 admits "cost is seeded or updated by operators/
  fixtures" - humans, not parties.
- So: what breaks at N=2 is attribution and directives; what breaks at N=8 is
  every shared organ at once (one .env, one sqlite gps_ledger.db3, one rib
  bus, one arena surface). What does NOT break: laws, ribs, rails, genome,
  canon - they are already per-estate artifacts that fork cleanly.
- Falsifier: a bank row carrying an operator_id that changes spend attribution
  at N>=2 (none exists today).
- Move (~1 h): MAG_OPERATOR_ID in .env, stamped into every route_chat bank row
  and usage.jsonl append. One field. Everything else stays fork-local.

## FINDING 4 - The mycelial republic is forked estates trading sha256 receipts;
the estate already runs that protocol internally and never named it

- The receipt-trade envelope EXISTS: scripts/build_travel_kit.py:184-198 mints
  a manifest of every file + sha256; :5-6 and ARCHIVE_TIERS (:52-59) define the
  bounded pointer ("path + sha256... Ask the archive, verify the hash") for ore
  too heavy to carry. Its schema is literally named travel_kit.v1 (:185).
- Cross-party trust already runs on the same primitive: the GPS ledger's
  evidence-resolution gate recomputes evidence sha256 from bytes at append -
  "an evidence_hash is never stored on trust" (tools/gps_mcp/ledger.py:60-66
  region).
- Chains cannot merge across seats - the estate's own contract says so:
  TWO_MACHINE_SYNC_20260919.md contract item 1, "nothing can merge two .git
  dirs", one machine live at a time. Therefore a SHARED chain is out by the
  estate's own law; the only consistent shape is N forks whose trust bond is
  hash-addressed receipts. That is what the mycelial republic IS: not one
  chain, but sibling estates that exchange travel-kit-style envelopes and
  verify bytes instead of trusting reports.
- Dormancy is already the estate's native mode and needs no new mechanism:
  route_chat's dormant gates (queue/STANDING_RAILS.md line 12), the z_ai lane
  dormant in providers.yaml (state/CURRENT.md:36), Hermes "dormant but
  dispatch-capable" (AGENTS.md). A spore's subsystems stay dormant the same
  way: no key, no cron, no firing.
- Falsifier: two estates appending to one shared verkle tip without receipt
  exchange (impossible under contract item 1; if someone builds it, this
  finding is wrong).
- Move (~1 sitting): promote the travel kit manifest to the official spore
  envelope in a tracked docs/RECEIPT_TRADE.md (schema travel_kit.v1, bounded
  pointers, verify-before-trust), and write scripts/regrow.py that boots in the
  GENOME.md:69-75 order (genome -> rails -> ribs -> CURRENT -> delta register)
  and prints the dormant/subsystem table.

## FINDING 5 - The tutorial ladder already exists as config; the doc is the only
missing organ, and one promised rail cron is already un-regrowable

- providers.yaml already encodes the exact ladder the topic describes: z_ai
  "FREE cache-mined GLM... the default" (line 14), openrouter "18 lanes x
  1000/day (the big free capacity)" (line 17), deepseek "PAID fallback" (line
  37), nous/Hermes judgment tier (line 150), xai (line 41). The tracked
  .env.example already carries every key slot the tutorial needs
  (OPENROUTER_API_KEY, DEEPSEEK_API_KEY, XAI_API_KEY, GROQ_API_KEY, ...). The
  free-lanes-are-SENSING-only rule is in AGENTS.md (driving ladder). The
  "~5% of paid" cost figure is topic-given, not verified here (OWED).
- Gap: queue/STANDING_RAILS.md:43 promises "a play hour | tools/tavern.py +
  tools/dungeon.py (hourly cron)", but no tracked registration script exists:
  grep -rln "tavern" scripts/ mag/ finds only scripts/dm_tools_dual_research.py
  and .mimosa hook-state cache; the scripts/register_*.ps1 family covers
  census/corpus/day_end/endpoint_news/fts/gap_sentinel/gate_canary/improve/
  leave - not play. A live schtasks census from this shell returned no Mag rows
  (scoped instrument: `schtasks /Query /FO CSV | findstr /I "Mag"`), so the
  hourly play cron is not regrowable from the repo today.
- Also drifted from the topic's map: corpus/steal holds 32 .md files today
  (`ls corpus/steal/*.md | wc -l`), not 10; the doctrine bus holds exactly 26
  ribs (memory/rib_bus/doctrine.json, ribs dict count 26, updated
  2026-10-04T22:50Z) - that number the topic got right.
- Falsifier: a cold seat follows the tutorial to its first successful
  route_chat without touching any private receipt, and the play cron re-registers
  from a tracked script.
- Move (~1 sitting): write docs/REGROW_TUTORIAL.md generated FROM providers.yaml
  + .env.example (key order: free lanes first, deepseek second, judgment last;
  sensing-only law attached to every free lane), plus
  scripts/register_play_task.ps1 so the drop-in table's cron promise is
  regrowable.

## WHAT I COULD NOT SEE (blind spots)

- Provider-side key rotation status for the 7 leaked keys: lives in provider
  consoles, not the repo. OWED.
- Whether github.com/NachoBusiness17/mycelial-republic is public or private:
  ls-remote succeeded from this seat, but cached credentials could explain
  that; I could not distinguish cache from anonymous access. The spore's
  exposure question depends on it.
- The live scheduled-task inventory: schtasks returned nothing for "Mag" from
  this shell; the cron census above rests on the register_*.ps1 scripts, not
  the live Task Scheduler state.
- The .zcode/workflows DWF carriers (the arena's workflow side) were not
  audited for shareability - the R1 ouroboros lane owns those files tonight
  (state/NIGHT_LOOP_20261005.md:36-38 file-ownership fence).
- Whether anyone but this operator has ever cloned the estate: unknowable
  from this repo.

## THE ONE-LINE MOONSHOT

Do not share the estate. Seed it: an orphan-branch spore (code + laws + 26
doctrine ribs + genome + rails + parable + regrow guide + .env.example), a
travel_kit.v1 receipt envelope for everything too heavy to carry, an
operator_id field so N>=2 can attribute a dollar, and a tutorial generated
from the ladder the config already holds. The chain stays home; the spore
travels; the republic is the trade.
