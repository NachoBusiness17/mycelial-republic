# DFDIALS candidate two: fix-taxonomy enablement dials for the violation ratchet

2026-09-26 · lane dfdials-two · sources read: `corpus/df_mine/DFHACK_THESIS.md`,
`corpus/df_mine/dfhack_fixes.json` (+`dfhack_fixes_FOLD.md`), `configs/violation_baseline.json`,
`tools/violation_ratchet.py`, `githooks/pre-push`. All counts below were computed this
session against the live bytes; raw tierer output saved at
`watch/inbox/ractor_panel_20260926/cands/dfdials-two_tierer_check.txt`.

## Approach

DFHack ships every cure with an enablement mode; our register ships every claim with none.
The steal is the mode field, not any single fix. `dfhack_fixes.json` carries `mode` on all
47 entries; populations verified by script this session: always-on 2 (both `quickfix.*`,
`dfhack_fixes.json:296-307`), default-on 4 (dry-buckets `:103-109`, empty-wheelbarrows
`:112-118`, general-strike `:130-136`, stuck-squad `:238-244`), opt-in 5 (noexert-exhaustion
`:148-154`, ownership `:165-172`, protect-nicks `:183-190`, stuck-worship `:247-253`,
wildlife `:283-289`), manual-only 36; plus 6 retired-upstream receipts `:454-461`. The FOLD
already names the move: "every registered debt names whether a gate may auto-fix it or
whether auto-fix destroys signal" (`dfhack_fixes_FOLD.md:26`) and "every baseline row needs
an upstream condition ('delete when X')" (`:28`).

The dial describes WHO MAY ACT on a claim, and every dial owns exactly one delete-when-X
whose receipt makes the claim's departure a ledger fact. Two actions are separate and must
stay separate: the FIX dial governs who may edit the code; the REAP path (prune, already
machine-authorized for scanner-domain claims, `tools/violation_ratchet.py:304-330`) only
fires after the disease is gone from bytes, so it never conflicts with a manual fix dial.

Why the dial keys on cure shape, not disease family: DF's most common family stuck-flags
(8/47, `dfhack_fixes_FOLD.md:7`) spans manual (drop-webs, occupancy, stuckdoors), default-on
(dry-buckets, general-strike); family does not predict mode. Our rules each name one cure
class, so rule → dial is deterministic and total.

## The four dials, DF exemplar → ratchet rows → delete-when-X

Dial assignment is a decision tree over row fields only (rule, note), evaluated in fixed
order with FIRST MATCH WINS. Verified over all 933 claims: exactly one dial per fingerprint
(asserted in the script), sum 933.

| Dial | DF exemplar (mode bytes) | Semantics | Ratchet rows (count, verified) | Delete-when-X + receipt |
|---|---|---|---|---|
| ALWAYS-ON | quickfix.set_entity_race_references "automatic on load (always)" `dfhack_fixes.json:296`; repair_site_id `:305` | Deterministic cure, one right answer, no signal choice; actor runs with zero consent | `todo-undated` (1: mag/max_distill.py) + `cwd-relative-path` (3) = 4. Cure is a one-line deterministic edit: date the comment; anchor the Path literal to ESTATE_ROOT (rule only fires on relative literals, `violation_ratchet.py:189-192`) | Delete when a full scan stops deriving the fingerprint. Machine: `prune`. Receipt: prune stdout `fixed-debt-removed=N` + baseline diff in the healing commit. Machine-certified, no human name |
| DEFAULT-ON | dry-buckets / general-strike "automatic (periodic, default-enabled via gui/control-panel)" `:108,:135` | Periodic, disableable, safe for the overwhelming majority; defect re-accumulates | `file-too-long` = 194. Splits are routine named-lane work (burn waves), and the disease regrows (B2-273 observed 427→453 same-day, `violation_ratchet.py:73-77`); the GROWTH line `:260-272` is the always-on monitor that surfaces which rows need this cure | Delete when the scan stops deriving AND a named split receipt exists (burn-wave/replace receipt naming the file). Receipt: prune line + the split receipt. The growth law already demands re-audit by name (`:79-80`) |
| OPT-IN | wildlife "manual or opt-in automatic (NOT default: some players keep wildlife captive)" `:288`; ownership, protect-nicks, stuck-worship | Cure exists as automation but destroys state somebody may want; only a named enabling act may run it | `except-pass` (652) + `bare-except` (1) + `env-key-read` (22) + `shell-true` (3) = 678. Silence may be load-bearing; key routing is a Key Law decision (sanctioned surface = exempt list `violation_ratchet.py:122`); shell surface likewise. Our #1 family except-pass mirrors DF's #1 stuck-flags: state cached and later trusted (`dfhack_fixes_FOLD.md:24`) | Delete when the scan stops deriving AND the enabling ask receipt exists (the by-name task that authorized touching that file). Receipt: prune line + enabling receipt. Auto-fix without it is the wildlife violation |
| MANUAL-ONLY | stuck-merchants "must not run while merchants are on-map; not repeat-safe" `:233-235`; occupancy dry-run `:162` | Not repeat-safe, needs a human scope, or the defect IS the design | All `mimosa-*` rules = 57 (29 ssrf + 25 path-traversal + 2 code-injection + 1 command-injection), underivable by construction (B2-95, `violation_ratchet.py:10-17`), PLUS any row whose note says by-design (2 today, both inside the 57; tier_probe's exec IS the scoring contract) | Delete when an explicit re-triage commit names the claim fingerprint + reason. The scanner can never certify these. Receipt: the re-triage commit; this law is already in force (`:12-15`) |

Counts cross-checked by rule x dial in the raw output; 57 + 678 + 194 + 4 = 933 = register size.

## Tiebreak rule (kill prong 1)

A row matching two dial predicates takes the LEAST AUTOMATED dial. Evaluation order:
manual-only → opt-in → default-on → always-on, first match wins.

Grounds in DF bytes: 10 of the 11 automatic entries also carry "+ manual" (multi-mode is
the norm, not the exception), and when both modes are documented the safety-governing side
is the manual one: wildlife could be automatic and is still opt-in because it destroys
captive-wildlife state (`:288`); stuck-merchants is manual-only because not repeat-safe
(`:233`). Grounds in our bytes: a future by-design `shell-true` row (a tool whose contract
IS the shell call, the pupeteer_gauntlet shape) satisfies both the opt-in rule shape and
the manual-only by-design predicate; the order sends it to manual-only. Today 0
scanner-domain rows carry by-design notes (verified), so no live row exercises the
cross-tier tiebreak; disjointness is what holds the register today and the tiebreak is the
stated law for the row that will.

Row-level, not file-level: 152 files carry claims in more than one dial (verified; e.g.
mag/knowledge_graph.py has one default-on and one opt-in claim). No row is double-assigned
because fingerprints are per (rule, file) (`violation_ratchet.py:19-21,205-213`); the file
is dial-ambiguous, its claims are not.

## Retirement machinery already wired (kill prong 2)

Every dial above names its delete-when-X AND its receipt, so no dial is receipt-less. Two
supports already exist in the machine and one live case proves the path works:

1. `prune` (`:304-330`) reaps only scanner-domain claims a full scan cannot re-derive:
   the always-on/default-on/opt-in retirement executor.
2. `expires` (`:228-234`) rots an accepted exception into a FAILING violation on date
   pass (`:248,273-275`), the enforcement hook for time-boxed re-triage. Currently 0 of
   933 rows use it (verified); stamping it belongs to the landing move, not this card.
3. Live case: claim `1f4834fca1771fc1` (except-pass, mag/icon_drop.py, accepted
   2026-09-25) is underivable on today's bytes (verified); its opt-in delete-when-X is
   satisfied pending the enabling receipt, then prune retires it.

## Moves with estate paths

1. Stamp the dial into the register: derive `dial` per claim with the tierer above at
   `baseline-update` time (`violation_ratchet.py:288-296` builds entries; add one derived
   field, never hand-written) into `configs/violation_baseline.json`. Rules text:
   `AGENTS.md` build-discipline section.
2. File the tiebreak + delete-when-X table as the register's usage law beside the existing
   B2-95/B2-273 comments in `tools/violation_ratchet.py:10-17,73-80`.
3. Retirement executor: keep `prune` as the machine-certified death for scanner-domain
   dials; re-triage-by-name stays the only exit for manual-only (`:315-324` already keeps
   them). No code change needed for reaping; the receipt condition is a commit-discipline
   ask, enforced by review like `--by WHO` already is (`githooks/pre-push:5,10`).
4. Retire the ready claim: enabling receipt for mag/icon_drop.py except-pass, then `prune`.
5. Dogfood first wave at the 7 NEW hits from today's check (see Falsifier): the tierer
   classifies 2 file-too-long (default-on), 4 except-pass (opt-in), 1 cwd-relative-path
   (always-on); each fixes or registers under its dial's rules.

## Falsifier

Checks run this session (commands verbatim, raw output at
`dfdials-two_tierer_check.txt`):

- `python tools/violation_ratchet.py check` → `scope=1188 files (all); hits=882;
  registered=875; NEW=7; expired-exceptions=0`. PASS prong of the machine: the register
  tracks bytes. The 7 NEW: tools/census_drift_patrol.py:403 and tools/probe20_run.py:421
  file-too-long; except-pass in tools/ledger_lock.py:125, tools/openrouter_free_gate.py:84,
  tools/transport_precheck.py:134, tools/visor.py:131; cwd-relative-path
  tools/queue_dupes_check.py:33.
- Tierer script (imported the real `violation_ratchet.scanner_domain` and
  `SCANNER_RULES`, walked all 933 claims, asserted one dial per fingerprint): always-on 4,
  default-on 194, opt-in 678, manual-only 57, sum 933. No row double-assigned (assertion
  plus first-match tree make double assignment impossible).
- Dead-claim census: exactly 1 scanner-domain claim underivable today (mag/icon_drop.py);
  57 external claims underivable by construction.
- Phantom-claim census (claims whose file is scanner-domain-true but outside the
  non-recursive glob `:88-95`): 0 today.

Kill-condition self-test, both prongs: (a) no row fits two tiers: the tree is disjoint by
construction and the tiebreak law (least-automation-wins, order fixed) covers any row whose
predicates overlap; (b) every dial carries one delete-when-X with a named receipt (see
table). If the judge finds a row the tree cannot classify (a rule outside SCANNER_RULES
that is not mimosa-*, or a new rule added without a dial slot), that is a genuine kill:
the tierer must be extended in the same commit that adds the rule.

## Owed

1. The 7 NEW unregistered hits above: register is 7 rows behind the tree as of this run;
   each needs fix-or-register-by-name under its dial.
2. mag/icon_drop.py claim retirement needs its enabling receipt (opt-in dial) before prune.
3. Latent gap inherited, not introduced: `scanner_domain` uses `startswith(root+"/")
   (`:64-68`) while `iter_py_files` globs non-recursively (`:88-95`); a future claim under
   mag/sub/ or tools/sub/ would be domain-true but never scanned, so prune would silently
   reap it. 0 such rows today (verified); aligning the two is a one-line operator call.
4. `expires` is machine-read but unused (0/933); wiring it into manual-only re-triages
   with horizons is a landing decision, not this card's claim.
5. DF mode strings are cited from the mined `dfhack_fixes.json` bytes; I did not re-open
   the `corpus/dfhack_full` clone to re-verify the control-panel defaults themselves.
