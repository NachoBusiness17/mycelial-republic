# SECURITY LENS - surface migration raction (2026-10-03)

Writer: lens-security (ractor dwf, surface-migration topic). Jacket: the gate
that tests itself and nothing else. Frame: lethal trifecta (private data +
untrusted content + communication) over the migration question.

## VERDICT STANCE

Security does not veto the migration; it conditions it. The headless rails
are the estate's best-tested paid-egress path (three fences on the front
door, O_EXCL claims, terminal refusal markers, evidence preflight), and the
three-day secret-gate streak (watch/inbox/DRIFT_PATROL_20261003.md:28-30)
shows the containment habit is live. But the rails currently enforce
CRASH-SAFETY, not AUTHORIZATION: every guard answers "did two racers collide",
none answers "is this writer allowed to spend". The interactive seat is the
only working operator-GO implementation today, and it exists by the accident
of a human reading a terminal. Migrate after the four moves below land, not
before; migrating first turns the descent driver's filesystem trust boundary
into the estate's primary attack surface.

## FINDING 1 - the paid-egress evidence pipe has no secrets fence (trifecta complete)

tools/hermes_burn.py:139-149 `_read_evidence` reads ANY repo-relative path
(`ROOT / rel`) up to 400,000 chars and renders it into the prompt sent to the
Nous API. Grep of tools/hermes_burn.py for denylist/forbidden/sensitive this
session returned zero lines. `.env` holds 44 keys (names-only census run this
session: HERMES_API_KEY_1/2, ANTHROPIC_API_KEY_2, GITHUB_TOKEN,
NOTION_API_KEY, OPENCLAW_GATEWAY_PASSWORD/TOKEN, MAPBOX_TOKEN, VERCEL_KEY,
XAI_SD_API_KEY and more). So an ask dir staged with `evidence: [".env"]`
ships all 44 live keys to a third-party API - and scripts/descent_driver.sh:33-36
eats EVERY dir matching `memory/plans/hermes_burn_*` every 45s cycle, and the
driver is LIVE NOW (memory/runs/hermes_burn/driver.beat tail: cycle 1676 at
2026-10-03T19:30:08Z; my ls confirms no DRIVER_STOP file). The existing
secret containment chain (write-side redaction mag/trajectory_step.py:123-124,
commit-side fail-closed gate tools/precommit_secret_check.py, wired by
githooks/pre-commit) protects the GIT surface only; the API-egress surface has
no gate at all. Falsifier: a denylist existing anywhere in the read path, or a
dry-run ask with evidence [".env"] being refused. Move (one sitting): add a
sensitive-path denylist to _read_evidence (.env, .git/, memory/seals/,
*.pem/*.key, deploy/k8s/mag-secret.yaml), reusing precommit_secret_check's
classification.

## FINDING 2 - no cumulative dollar cap on the burn path; the play path has one

tools/hermes_burn.py main loop (read in full this session, ~lines 376-405):
fires every ask dir, banks usage, prints a total. Guards are per-ask (landed
skip, REFUSED terminal at 2 refusals, O_EXCL CLAIM, per-call inference-budget
floors) - none is a per-day dollar ceiling. Contrast tools/tavern.py:15
("hard stops: round cap, cumulative budget_usd") and tools/tavern.py:133
("BUDGET CAP $... hit mid-round; hard stop (family-box law)") - the newest
carrier carries the cap the older, more dangerous one lacks. Live scale today:
911 usage rows, $25.11 (my python sum over memory/runs/hermes_burn/usage.jsonl,
2026-10-03 rows). History: $25.53 of $37.76 was re-fire excess in the
dogfood-48h window (tools/instance_guard.py:4-7 docstring). In headless mode
the provider credit pool becomes the only brake. Falsifier: a cumulative
budget check anywhere in descent_driver.sh (46 lines, read in full - none) or
hermes_burn main(). Move: port tavern's budget_usd stop into hermes_burn
main() - refuse new asks when today's ledger sum crosses a --budget-usd flag.

## FINDING 3 - the front door enforces two fences and ignores a declared third

configs/providers.yaml:538-543 and :577-583 mark z_ai and z_ai4
`opencode_only: true` ("raw-API use is rate-limited (1305/1302) + fence
risk"). mag/route_chat.py enforces the dormant gate (:113-115) and the
endpoint fence (:121) but has ZERO opencode_only logic (grep exit 1 this
session). Enforcement lives only in mag/doctor.py:114 (classification:
"never probed raw") and a routing-around comment mag/api_gateway.py:594-596.
Scope of the absence claim: grep -rln "opencode_only" over mag/ tools/ tests/
hit api_gateway.py, doctor.py, seat_corpus.py and two test files - none is a
call path. The plugin spec (watch/inbox/mag_rails_plugin_spec_20261003.md:10-12)
makes route_chat the default model-call tool; a headless caller passing
lane="z_ai" fires the exact forbidden raw call, and per AGENTS.md fan-out
width law those 1305/1302 storms crash tethered sessions. A fence that lives
in a name string is a comment. Falsifier: route_chat(lane="z_ai") succeeding
live, or a test proving route_chat refuses opencode_only lanes. Move (~10
min): mirror the dormant gate - refuse opencode_only lanes without
operator_go. Residual folded here: both fences check-then-call
(getaddrinfo at route_chat.py:75-79, urlopen re-resolves at :145; same shape
tools/hermes_burn.py:96-101/:123-125) - a DNS-rebinding TOCTOU window that
requires provider-DNS compromise; low likelihood, wider under 24/7 headless.

## FINDING 4 - interrupts-never-cancel + file-based control = no authorization layer between repo-write and paid-spend

queue/STANDING_RAILS.md:17-18 (law 3): "Interrupts never cancel. Wide waves
run background-executed; an operator interrupt steers, it does not kill."
The night driver's only kill switch is a file (DRIVER_STOP,
scripts/descent_driver.sh:25,29); re-arming a refused ask is ALSO a file
operation ("operator edit of the ask bytes plus marker removal",
tools/hermes_burn.py:107-109) - meaning any repo writer can delete a REFUSED
marker and edit ask bytes to re-open a terminal refusal. The O_EXCL CLAIM
(tools/instance_guard.py:124-151, read in full) is a race lock with a
pid-liveness steal path (:141-148), not an authorization system: it answers
"who fired first", never "may you fire". Today every seat holds repo write,
so every seat holds the paid keys transitively. The interactive surface's
security property was never that it is safer - it is that a human reads the
transcript before a bent decision compounds. Headless removes the reader.
Falsifier: any signature/allowlist/GO gate between ask staging and paid fire;
my full reads of descent_driver.sh and hermes_burn main() found none. Move:
fail-closed batch GO - hermes_burn refuses unless memory/runs/hermes_burn/GO
exists and is <24h old (the route_chat operator_go analogue at batch level).

## FINDING 5 - the estate's own doctrine documents working context-injection, and the rails close it into the paid tier

The memlance skill (.agents/skills/memlance/SKILL.md, in my skill list this
session) exists to "plant ONE specific seed-memory into a target seat's
context through the mesh (chan row, card, want) so its later decision bends
without a command" - first-party proof the estate believes cross-seat
injection works. The ouroboros clause (queue/STANDING_RAILS.md:37-42) makes
model outputs into evidence for later asks and "capability rows route the
next ask's dollars": a payload seeded into any free-lane output propagates
into paid-tier ask evidence unattended. The rails' own hollow-batch law
(queue/STANDING_RAILS.md:14-16: "a cheap seat fabricates when evidence is
missing, and the run still prints ok=True") is visible in today's ledger:
GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003 banked ok:true with
content_chars: 1 after 39,093 prompt tokens (memory/runs/hermes_burn/
usage.jsonl tail, read this session), and TAVERN rows bank today carry
doubled_key: true - the tripwire fires, the spend still happened. Falsifier /
drill (not run this sitting; costs paid tokens, needs operator GO): a canary
ask whose evidence carries a benign injected instruction ("append CANARY"),
dry-lane first (~$0.0001 on ds_workhorse), then one paid probe - echo
proves propagation, a content filter between free-lane outputs and paid-ask
evidence proves me wrong. Move: run the canary drill and put its verdict in
the Delta Register.

## WHAT I COULD NOT SEE (blind spots, honest)

- The arena cron automation-b1ce1342's own wiring is OWED: its id appears
  in-repo only in memory/trajectory/steps.jsonl (grep this session); its
  "cap-held" behavior is ask-provided and corroborated by tavern.py:133's
  live cap mechanism, but I never read the cron registration itself.
- mag/api_gateway.py auth on the local :8765 surface (whether lab/dashboard
  model calls are LAN-exposed unauthenticated) - out of my read set.
- Whether the opencode harness (migration target) leaks .env into plugin/
  MCP server processes - the plugin spec's "never holds keys"
  (mag_rails_plugin_spec_20261003.md:47) is a spec line about route_chat,
  not audited opencode behavior.
- Windows ACLs on .env; deploy/k8s/mag-secret.yaml contents (gitignored,
  not read); the docker fleet's secret path.
- The canary injection drill (Finding 5) was not executed.

## LAWS OBEYED

Every universal claim above is scoped to the searches actually run (greps
named with their hit sets; full reads named as full). No em-dashes. The
44-key census printed key NAMES only, never values. The evidence-pipe
finding cites code read in full this session, not inference.
