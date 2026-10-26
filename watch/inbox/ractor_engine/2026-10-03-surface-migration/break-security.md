# break-security: hostile second pass on lens security (2026-10-03)

Pass ran 2026-10-03, census moment 2026-10-03T20:35:13Z unless a check names
another moment. Every verdict below names what was read or run THIS sitting.
Instrument note: this shell lacks POSIX coreutils; all greps, sums, and the
canary ran through `.venv/Scripts/python.exe` one-liners invoked from bash.
No secret VALUES were printed anywhere in this pass; .env was read as key
NAMES and length/boolean probes only.

## VERDICTS

### Finding 1 (no secrets fence on the paid-egress evidence pipe): CONFIRMED, upgraded; one numeric claim corrected

Byte-checks that passed:
- `tools/hermes_burn.py:134-146` is `_read_evidence`: renders any
  repo-relative path into prompt text, no denylist. (Lens cite "139-149"
  lands inside the function but misses the def at 134; minor.)
- `scripts/descent_driver.sh:33-36` byte-exact: `for q in memory/plans/hermes_burn_*`
  then fires `tools/hermes_burn.py` per dir every 45s cycle.
- `driver.beat`: cycle 1676 at 2026-10-03T19:30:08Z present as claimed; by
  this pass's moment the tail had advanced to cycle 1677 at 20:01:22Z
  (2741 beat lines total); `DRIVER_STOP` absent (checked). The driver is
  still live, which is exactly the lens's point.
- Denylist falsifier sweep over `tools/` + `mag/` (patterns: denylist,
  deny_list, forbidden, sensitive): zero hits in the hermes_burn evidence
  path. Nearest in-repo pattern is `mag/resonance.py:24,40`
  (`_FORBIDDEN_PREFIXES` on memory/briefs/, data/raw/, secrets/) - the
  copy-source for the fix.
- Git-side containment confirmed commit/trail-side only:
  `mag/trajectory_step.py:123-128` (redact) and
  `tools/precommit_secret_check.py:1-21` (commit gate, exit 1, wired at
  githooks/pre-commit). Nothing gates egress. `.env` is untracked:
  `git check-ignore .env` rc 0; `git ls-files --error-unmatch .env` rc 1;
  `.gitignore:19-21`.

THE FALSIFIER WAS EXECUTED, not just argued (in-process, zero network, no
API call, no secret bytes printed):

```
from tools.hermes_burn import _read_evidence, _assert_evidence_in_body
rendered = _read_evidence(['.env'])
# -> 5760 chars, header '=== EVIDENCE .env ===',
#    contains HERMES_API_KEY_2 and ZAI_API_KEY key lines (boolean probes)
_assert_evidence_in_body({'id':'BREAK_SECURITY_CANARY_DRY','evidence':['.env']},
                         [{'role':'user','content':'PREFIX '+rendered}])
# -> NO exception raised: evidence=['.env'] passes the door unfenced
```

The lens's falsifier ("a dry-run ask with evidence ['.env'] being refused ...
would disprove this") was run and did not fire. The lethal trifecta is
proven at function level, not inferred.

Corrected numbers (the lens's carry, not its direction):
- .env key census THIS pass: 54 keys total, 53 with non-empty values, 1
  empty (GROK_API_KEY_2); 48 after precommit_secret_check's non-secret
  names. NO instrument reproduces the lens's "44". The corrected count is
  higher; the finding is stronger; the "44 live keys" figure should be
  struck as non-reproducing.

One scope fact the lens implied but did not state: no live incident today.
Census of all 16 staged `memory/plans/hermes_burn_*` queue dirs (~90 ask
dirs) shows zero `evidence[]` entries pointing at `.env` or key-like paths.
The fence is absent; nothing has walked through it yet.

Verdict: CONFIRMED (upgraded by execution; struck "44", replace with
54/53 live at named moment).

### Finding 2 (no cumulative dollar cap on the descent path): CONFIRMED; numbers re-censused; scope extends to ds_workhorse

- `tools/hermes_burn.py` main() `:395-424` read in full: iterates ask dirs,
  banks, prints the ledger total, never gates on it. No cap.
- `scripts/descent_driver.sh` read in full: 45 lines by splitlines (lens
  said 46; off by one, substance unchanged), no cap.
- Falsifier widened past the lens's two files: `mag/inference_budget.py`
  (394 lines) is in the fire path (`plan_call` at hermes_burn.py:344);
  grep for budget_usd/cost_usd/cumulative/total/spend finds only cost
  BANKING (`:363`), no dollar gate anywhere on the path.
- Contrast byte-exact: `tools/tavern.py:15` ("hard stops: round cap,
  cumulative budget_usd") and `:133` (BUDGET CAP hard stop, family-box
  law). A third exemplar the lens missed: `tools/dungeon.py:161-162` and
  `:458-460` (`self.spend >= self.budget` hard stop) with the
  `--budget-usd` flag defaulting to 4.0 at `:553`.
- Scale, re-censused at 2026-10-03T20:35:13Z: 975 ledger rows / $25.27 for
  2026-10-03; all-time 1216 rows / $64.20. Lens read 911 / $25.11 at its
  moment on the same live append-only ledger; both are valid named-moment
  reads, the drift is the driver still firing between them.
- EXTENSION the lens missed: `descent_driver.sh:37-42` also auto-fires
  `tools/ds_workhorse.py` every cycle when pending_items.jsonl exists.
  `tools/ds_workhorse.py` (119 lines) contains ZERO budget references,
  reads `DEEPSEEK_API_KEY` from .env (`:40-45`), banks cost (`:92`). A
  port-the-cap move scoped to hermes_burn alone heals half the driver
  (the unwired-organ law, instance_guard.py:8-10).

Verdict: CONFIRMED (move: port tavern's budget_usd into hermes_burn main()
AND ds_workhorse's loop; one sitting).

### Finding 3 (opencode_only fence declared in config, unenforced at the route_chat door): CONFIRMED, mechanism traced end to end

- `configs/providers.yaml:537-543` (z_ai: `opencode_only: true` at :542;
  name line :538 declares "opencode harness ONLY" with raw-API use
  "rate-limited (1305/1302) + fence risk") and `:577-583` (z_ai4,
  `opencode_only: true` at :582). Byte-exact.
- `grep opencode mag/route_chat.py`: zero matches (re-run this pass).
- Mechanism, traced: `_load_lanes` loads providers.yaml providers
  (`mag/route_chat.py:45-49`), so z_ai/z_ai4 ARE in route_chat's lane
  table; the dormant gate `:113-115` and endpoint fence `:121` are
  byte-exact; `_keys_for` resolves ZAI_API_KEY from .env (`:52-68`; key
  present per this pass's census). `route_chat(lane='z_ai')` passes the
  dormant check (no dormant flag), passes the fence (public host), and
  fires the exact raw `/paas/v4` call the config forbids.
- Scope census, code dirs only (mag, tools, tests, scripts, server,
  docker, configs, githooks; *.py/*.yaml/*.json/*.sh/*.ps1): 6 files carry
  the string. `configs/providers.yaml:542,582` (declaration);
  `mag/doctor.py:114,616,721,723` (doctor ENFORCES the fence for its own
  probes: `:721-724` sets status=FENCED, probe="none(fenced)");
  `mag/seat_corpus.py:81,111,277` (copies the flag into rows);
  `mag/api_gateway.py:595` (a comment: _SPAWN_PRESETS route flash-class
  spawns AROUND z_ai to the deepseek lane, `:597-601`); two test files.
  NO model-call path enforces it. The lens's "none is a call path" holds;
  the sharpening is that the estate declared the fence in three places
  (config names, doctor FENCED state, api_gateway comment) and wired it
  into none of the doors that speak.
- `watch/inbox/mag_rails_plugin_spec_20261003.md:10-12` byte-exact:
  mag_route_chat is "The default model-call tool".

Verdict: CONFIRMED (move stands: one branch after lane_cfg resolution,
refuse opencode_only without operator_go; ~10 min).

### Finding 4 (no authorization layer between repo-write and paid-spend): CONFIRMED; one evidence cite is defective

- `queue/STANDING_RAILS.md:17-18` byte-exact (law 3: interrupts steer,
  never kill).
- `scripts/descent_driver.sh:25` (STOP file path) and `:29` (the while
  loop) byte-exact: the kill switch is a file any repo writer can delete
  or create. DRIVER_STOP absent at this pass's moment.
- DEFECT: the lens cites "tools/hermes_burn.py:107-109 (re-arm = ask-byte
  edit + marker removal)". Lines 107-109 are the def of `_call` and its
  URL checks. The re-arm law actually lives at `:26-29` (docstring),
  `:195-203` (`_mint_refused_marker`: "Re-arm only by editing the ask
  bytes AND deleting this marker"), and `:295-299` (REFUSED skip-on-sight).
  The claim is true; the pointer is wrong; fix the citation, not the
  finding.
- `tools/instance_guard.py:4-7` byte-exact ($25.53 of $37.76 re-fire
  excess). `:124-151` read in full: O_EXCL CLAIM at `:135`, pid-liveness
  plus freshness check `:143`, stale-steal path `:145-148`. It is a
  crash-safety race lock, exactly as the lens said, not an authorization
  system.
- No GO gate anywhere on staging-to-fire: main() `:395-424` has no
  operator_go (contrast route_chat's `operator_go` param `:90`, used only
  for dormant lanes `:113-115`). The falsifier survives.
- Sharpening the lens missed: the plugin spec's mag_stage_ask
  (`watch/inbox/mag_rails_plugin_spec_20261003.md:13-15`) makes staging a
  NATIVE tool whose asks "the descent driver eats automatically". The
  authorization gap is one tool-call away from every future seat.

Verdict: CONFIRMED (move: fail-closed GO marker, batch level, mirror of
route_chat's operator_go; one sitting).

### Finding 5: NOT VERIFIABLE (input truncated)

The material this pass received cuts off mid-evidence at
".agents/skills/memlance/SK". The finding's text, full evidence,
falsifier, and move were not delivered. Only check possible and run:
`.agents/skills/memlance/SKILL.md` exists (2270 bytes). Per the
never-fabricate law, no verdict beyond that. Blind spot 5 says Finding 5's
falsifier is the canary injection drill and that it needs paid tokens and
operator GO; it was not executed this sitting either, by the lens or by
this pass.

## BLIND SPOTS: what this pass could and could not close

1. Arena cron automation-b1ce1342 wiring: partially probed. In-repo, the
   id appears ONLY in `memory/trajectory/steps.jsonl` (13 hits, rows
   48020-48322, timestamps 2026-10-03T19:49:25Z through 20:19:28Z, i.e.,
   the ractor sitting's own rows); targeted scan of configs/, scripts/,
   queue/, memory/law/ found zero. The registration itself lives outside
   the repo (ZCode harness config); the full-tree and ~/.zcode walks were
   killed as pathological after ~15 minutes each, so the registration was
   NOT located this sitting. The lens's OWED stands; its in-repo claim is
   corroborated at the scope named.
2. api_gateway auth on :8765: partially closed. `mag/api_gateway.py` (767
   lines) probed: ZERO auth headers, tokens, or bind logic in the module;
   its /room/spawn route fires real model calls (`:639-646`). The
   dashboard default bind is 127.0.0.1 (`mag/runtime.py:97`) but the cast
   surface resolves a LAN host (`mag/runtime.py:153-164`;
   `mag/cast_launch.py:12,56` instructs "on the same Wi-Fi, open
   http://<PC-LAN-IP>:8765/voice"). Whether the cast serving path mounts
   the gateway routes was NOT traced. Remainder OWED, and it is
   migration-relevant (see addition A4).
3. opencode harness .env leak: not examined (needs the harness's own
   audit surface). OWED.
4. Windows ACLs on .env: not examined. `deploy/k8s/mag-secret.yaml`
   EXISTS (existence confirmed this pass; contents deliberately not
   read). `.env` confirmed gitignored (`.gitignore:19-21`). OWED.
5. Canary injection drill: not executed (paid tokens, operator GO). OWED.
6. ZCode-side automation permission model: not audited. OWED.

## ADDITIONS (what the lens missed)

A1. The finding-1 falsifier is cheap, safe, and now PROVEN runnable: the
    .env canary executes in-process with zero network and zero secret
    bytes printed (this pass ran it: 5760 chars rendered, preflight no
    exception). Land the same canary as `tests/test_evidence_fence.py`
    the day the denylist lands; it must flip from pass-unfenced to raise.
    Evidence: this pass's in-process run (see Finding 1). Falsifier: after
    the denylist patch, the same canary raising. Move: 15 min.

A2. ds_workhorse is the second ungated paid leg of the same driver
    (`scripts/descent_driver.sh:37-42`; `tools/ds_workhorse.py` zero
    budget references, .env key read `:40-45`). Any budget/GO work scoped
    to hermes_burn alone is half-healed. Falsifier: a budget_usd gate
    found in ds_workhorse's run path would disprove. Move: +15 min on
    finding 2's port.

A3. The plugin spec hardens the attack surface in the same stroke it
    formalizes the rails: mag_stage_ask (spec `:13-15`) gives every future
    seat, or any prompt-injected process, a NATIVE staging tool whose asks
    the driver eats automatically; the spec's key-custody line (`:47`,
    "The plugin never holds keys") covers key custody, not evidence
    custody. Order of operations flips: fence `_read_evidence` BEFORE
    wiring mag_stage_ask, else the plugin era launches the trifecta as a
    supported API. Falsifier: mag_stage_ask validating evidence_paths
    against a denylist at implementation time. Move: 10 min spec
    amendment.

A4. The :8765 surface is LAN-reachable by design on the cast side
    (`mag/cast_launch.py:12,56`; `mag/runtime.py:153-164`) while
    `mag/api_gateway.py` carries zero auth in a 767-line probe and its
    spawn route fires real lane calls (`:639-646`). The migration debate
    treats :8765 as local; a headless-primary estate promotes this
    surface to load-bearing with no auth pass on record. Falsifier: the
    cast serving path never mounts /room/* routes, or an auth middleware
    exists in it. Move: trace run_cast's route mounting, 30 min.

A5. Numeric hygiene: two lens numbers fail reproduction (44 keys; "46
    lines" vs 45 by splitlines), and the spend figures are named-moment
    reads on a live ledger (this pass: 975 rows / $25.27 at
    2026-10-03T20:35:13Z; all-time 1216 / $64.20). Any cost-per-deliverable
    table built later must re-census at its own moment and name the
    instrument, or it inherits the struck-headline disease the estate
    already lints for. Move: 0 min, use this sitting's numbers.

A6. Both fix patterns already exist in-repo, so findings 1 and 2 are
    copy-jobs of the estate's own law, not new design: budget cap
    (tavern `:15,:133`; dungeon `:161-162,:458-460,:553`) and path
    denylist (`mag/resonance.py:24,40`). This strengthens the security
    lens's actual bottom line for the migration verdict: none of these
    deltas is a migration blocker; all are one-sitting preconditions that
    should land BEFORE any headless-primary cutover, because headless
    removes the terminal-watching human who is currently the only brake
    on all three gaps (egress, ceiling, authorization).

## PASS SUMMARY

4 findings byte-checked: 4 confirmed (3 upgraded with mechanism or
execution, 1 with a corrected key count and 1 with a defective line cite
flagged), 1 not verifiable (truncated input). 2 lens numbers struck as
non-reproducing. 1 scope extension (ds_workhorse), 1 pre-migration
ordering implication (fence before mag_stage_ask), 4 blind spots partially
closed, 2 remain fully open (opencode harness leak, ZCode automation
permission model).
