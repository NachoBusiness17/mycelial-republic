# RUN ANTHROPIC1 - garden battery, holes 3 + 4 (2026-10-01)

Garden probe lane (HAIKU+SONNET). Series ANTHROPIC1 = the first fired battery
series. Fills PRIORS.md holes: #3 haiku (zero estate rows, cheapest anthropic)
and #4 sonnet-5.5 (the 6-0 judge2 upset resting on n=1; this run is its proof
test). Machine-scored grid in GRID_ANTHROPIC1.json; this file is the run
receipt (the markdown rendering the BATTERY schema asks for).

- Runner: python tools/model_garden.py, queues memory/plans/garden_battery/
  q_A1_haiku45 + q_A1_sonnet55 (staged copies of B1..B8 with model/base_env
  filled per the runner contract; contract bytes untouched).
- Models: anthropic/claude-haiku-4.5 and anthropic/claude-sonnet-5.5 via
  https://inference-api.nousresearch.com/v1 (HERMES_API_KEY_2), both ids
  byte-confirmed live in the catalog this session.
- max_tokens 12000 every fire; one attempt per item (no re-fires); 16/16
  returned non-empty CONTENT channel (zero reasoning-channel-only burns, zero
  refusals, zero transport failures; nothing to bank as transport rows).
- Authorization and cap: operator probe-lane instruction, $4 combined cap.
  Spend: sonnet $0.4235 (ECON implied exact 2.0/10.0 perM; 58,343 in /
  30,678 out incl reasoning) + haiku UNPRICED (no rate on file for
  claude-haiku-4.5 anywhere in the estate; 42,994 in / 2,509 out; upper
  bound at sonnet rates $0.1111). Worst-case combined $0.535, 13% of cap.
- Ledger: 16 rows in memory/runs/model_garden/usage.jsonl (ids
  garden-v1-A1-{haiku45,sonnet55}-B{1..8}). The $0.6652 ledger tail from ids
  garden-v1-kimi1-* is a sibling lane, not this series.
- Surface freeze: all 7 staged evidence files byte-match their staged sha256
  (recorded in GRID_ANTHROPIC1.json surface_shas_at_run); no re-freeze needed.

## The grid (score_norm = checks passed / checks total; B8 is the tier)

| family | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | mean |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4.5 | 1.0 | 1.0 | 0.6 [1] | 1.0 | 1.0 | 1.0 | 0.75 | 1.0 | 0.919 |
| claude-sonnet-5.5 | 1.0 | 1.0 | 0.8 [1] | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 0.950 |

Raw checks: haiku 33/36, sonnet 34/36.

Flags (law 6, carried from staging; footnote markers above):
[1] B3 carries the zcode-seat-glm authorship flag; B1 rows also carry the
claude-adjacent flag (DAY1 E1/E3/N3 patches in hermes_burn.py: the anthropic
family reviewing claude-adjacent carrier work needs a second family on any
B1 verdict, the G7 glm-judging-glm analog).

## Costs per family

| family | fires | in tok | out tok | reasoning tok | cost |
|---|---|---|---|---|---|
| claude-haiku-4.5 | 8 | 42,994 | 2,509 | 0 (none banked) | unpriced (bound $0.1111 at sonnet rates) |
| claude-sonnet-5.5 | 8 | 58,343 | 30,678 | 19,187 across 7 items | $0.4235 |

Token shape: sonnet burns ~65% of output tokens on reasoning and still lands
clean content (no assembly needed, contra the opus-5.5 disease); haiku emits
zero reasoning tokens and ~1/12th the output volume of sonnet on review items.

## Byte spot-checks (the falsifier layer: test-taker vs ractor)

Verified against the real files this session:

- SONNET TRUE: hermes_burn.py raises on empty triple-channel responses before
  any _bank (334-335 region) and only "refused" rows count terminal, so empty
  re-fires are unbilled and unlimited (the ECON ~40% re-burn inflation in
  code form).
- SONNET TRUE: switchboard_v2.py line 246 lets a proposal's own
  require_confirmation:false override the policy-derived gate, and 301-303
  auto-AUTHORIZES self-declared authority_label "operator-authored". This is
  the deepest find of the run: an agent can self-authorize any effect.
- SONNET TRUE: steer_seal.py resolve_mode returns "warn" on missing/garbage
  sentinel (fails open); admit(path) uses strict parse_envelope so a plaintext
  STOP file raises before the restrictive safe-fail path (docstring says
  intentional; both families filed it as a defect: spec dispute, byte-grounded).
- HAIKI TRUE: switchboard_v2.py:83 _GRANTED_EVENT_IDS is a module-level
  in-memory set (replay protection dies on restart); convergent with sonnet.
- HAIKU FALSE: the B2 claim "budget arithmetic divides strings" is wrong on
  bytes (line 614 already int-casts both operands) and its cite 447-451 points
  at confirm() bookkeeping, not the budget code.
- HAIKI OFF-FILE: B3 cite :32 on a 30-line file (beyond EOF).

## Judge2 upset verdict (PRIORS row 18: 6-0 on n=1 ask)

CORROBORATED, with scope. Sonnet-5.5's adversarial estate-review strength is
real and replicates across 5 surfaces (not one ask): 24/25 review checks, the
only finds that chain multiple code sites into an exploit (self-authorization
chain), byte-true on every spot-check, zero hallucinated claims found, and
clean content-channel delivery at 12k cap. The judge2 quality upset was not a
fluke of one ask. What this run does NOT show: sonnet at 3.8x haiku's bound
cost buys find-depth, not mechanical compliance (haiku scored 0.919 vs 0.950);
routing dollars to sonnet is justified for adversarial review of
security-bearing surfaces, not for format-carrier work where haiku is
byte-perfect at a fraction of the price. The upset stands as an
adversarial-review verdict; it is still not a workhorse verdict.

## Convergence (build-lane feed; full table in GRID_ANTHROPIC1.json)

Convergent defect candidates (both families, 2-family series so n=2):
- hermes_burn.py 300-349: empty/failed responses never banked; re-fire leak.
- switchboard_v2.py 101-150 + 300-349: process-local replay protection +
  self-declared authority labels (the operator gate is advisory).
- SHARED_SURFACE_CONTRACT.json 1-50: no concurrency/no-clobber law; INDEX.json
  schema undefined; classification self-attested.
- steer_seal.py 351-400: admit(path) strict parse blocks plaintext
  restrictive directives (STOP) before the safe-fail path.
Family-unique (mask law: evidence about the family, not the estate): sonnet
found the endpoint-fence redirect/DNS-rebinding key leak and the landed-skip
reasoning-channel lock-in; haiku found the preflight 400-char probe blind
spot and the unresolved template variables.

## Operating profiles

- claude-haiku-4.5: zero reasoning tokens, terse content-channel answers,
  byte-perfect format compliance, one wrong-on-bytes claim per ~4 asks;
  cheap sensing/format carrier, never the sole adversarial reviewer.
- claude-sonnet-5.5: ~65% reasoning-token burn inside a clean content
  channel, multi-site exploit chaining, self-labels unverified assumptions
  (UNVERIFIED tags); adversarial-review tier for security-bearing surfaces
  at ~$0.04-0.11 per review.

## Amendments filed (BATTERY.md AMENDMENTS section)

- A1-1: B6/B8 are self-contained asks but tools/model_garden.py fails closed
  on evidence []; accommodation = freeze the ask text itself as the evidence
  file (A1_B6/B8_ask_frozen.md), identical appended bytes for both families.
- A1-2: DISTINCT-EVIDENCE is meaningless on sub-50-line surfaces (B3 is 30
  lines: both families failed check 5 = column pattern = spec bug); cells
  kept as measured per the scoring-sheet law.

## Files landed this run

watch/inbox/model_garden/GRID_ANTHROPIC1.json (scored grid + convergence) -
this receipt - A1_B6_ask_frozen.md + A1_B8_ask_frozen.md (law-2 freezes) -
16 reply files garden-v1-A1-{haiku45,sonnet55}-B{1..8}.md - 16 ledger rows -
BATTERY.md AMENDMENTS append - animal_profiles rows (16 verdict + 2 price +
5 convergence) with --distill run.
