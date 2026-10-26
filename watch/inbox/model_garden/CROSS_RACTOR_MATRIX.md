# CROSS_RACTOR_MATRIX - models ractoring each other, the disagreement harvest (2026-10-01)

Lane X1 of the cross-model program (cheap-first: DeepSeek adjudicates, bytes
verify). Material: the garden-v1 GRID outputs landed today
(GRID_kimi1.json, GRID_ANTHROPIC1.json, GRID_fable1.json, GRID_cheapgrid1.json
and the garden-v1-* family outputs). Instrument: tools/ds_workhorse.py
(deepseek-chat, thinking off, temp 0.3, paste-bound blind adjudicator), 14
items, batch cost **$0.0153 of the $1 cap (1.5%)**.

- Items: `memory/runs/hermes_burn/xmodel_cross_items.jsonl` (built by
  `memory/runs/hermes_burn/xmodel_cross_build.py`; quotes verbatim from the
  garden outputs, byte regions sliced from the live files with real line
  numbers).
- Verdicts: `memory/runs/hermes_burn/xmodel_cross.jsonl` (14/14 ok, zero
  empties, zero retries).
- Surface stability: switchboard_v2.py (92573eac), descent_driver.sh
  (1ac6a0f3), SHARED_SURFACE_CONTRACT.json (9cfd74fa), steer_seal.py
  (84d4f7b7) are byte-identical across every series. **hermes_burn.py is
  NOT**: kimi/sonnet/haiku reviewed sha 9c8a0c1a (22:10-22:19Z), cheapgrid
  reviewed and the matrix adjudicates against current sha 91453258
  (23:03Z+; the inference-budget guard insertion sits between them). Every
  B1 verdict below carries that caveat.

## 1. The matrix (surface x family-pair x verdict)

| id | surface | pair | the disagreement | verdict | byte evidence (settled) |
|---|---|---|---|---|---|
| X01 | tools/hermes_burn.py | kimi vs sonnet | kimi: id-traversal in out_path + evidence traversal + fence TOCTOU. sonnet: redirect key-leak fence + empty-row banking | COMPLEMENTARY | kimi A1/A2 real (out_path f-string at 263; `ROOT / rel` with no containment at 132-133, cites off); sonnet B3 is a superset of kimi A3 (redirect carries Bearer at 116 + urlopen re-resolves at 119 vs preflight at 92); kimi A3 anchors stale |
| X02 | tools/hermes_burn.py | sonnet vs ds41flash | sonnet: empty rows never banked, finish_reason never read, unlimited re-fire. ds: landed-skip loses pending revision; probe blind to tail truncation | B-right (with version footnote) | on CURRENT bytes finish_reason IS read (323) and guard_terminal banks ok:false + mints terminal (324-325); sonnet's two absolutes were true on the sha it reviewed (grader byte-verified raise-before-_bank) and false 45 min later; ds's revision-loss window real (210-215 vs 356-361); ds probe-tail claim settled true by seat bytes (probe text[:400] at 248 vs 400k cap at 137-139) |
| X03 | mag/switchboard_v2.py | kimi vs sonnet | replay hole location: kimi says in-memory set + crash-window ordering in grant(); sonnet says confirm() bypasses the set entirely | B-right | set at :84 (kimi's :56 wrong, sonnet's :83 = comment line); ordering claim byte-real (290 trail, 291-292 add) but low-severity; confirm() 411-474 never reads/writes the set = the bigger hole, sonnet named it |
| X04 | mag/switchboard_v2.py | kimi vs sonnet | inbox race: kimi cites _rewrite_inbox_rec at 320-335; sonnet at 517-529 + corrupt-line drop | B-right | same defect; function lives at 512-526 (kimi's window is _implicit_authority's region); no lock anywhere (append 364, replace 526); sonnet adds the JSONDecodeError silent drop at 399-400 |
| X05 | mag/switchboard_v2.py | haiku vs sonnet | haiku: confirm() advances DEFERRED to AUTHORIZED without TTL recheck. sonnet: stale DEFERRED twin stays confirmable | BOTH-wrong by adjudicator, settled by seat: haiku-wrong + sonnet-half-true | haiku refuted: confirm window checked at 420 AND validate_authority TTL step (policy_engine 327-329) fed by preserved ts/ttl (434-436); haiku cited 339-371 = _defer region. sonnet's twin mechanism byte-true by seat read: _find_inbox first-DEFERRED-by-id (404-408), _defer appends no dedup (363-365), rewrite matches id-only (517-519) |
| X06 | mag/switchboard_v2.py | sonnet vs haiku | sonnet: self-declared authority_label=operator-authored + require_confirmation:false bypasses the operator gate for ANY effect. haiku: write_board_note divides budget strings | A-right | bypass chain byte-real end to end: label gate 239 skips, confirmation gate 249 honors proposal-supplied False, _implicit_authority 302-303 sets AUTHORIZED before the tier gate 318-321 can fire; haiku's claim false (614 int-casts both operands) and cited 447-451 which is not the function |
| X07 | scripts/descent_driver.sh | fable vs kimi | fable: no spend ceiling, $145 stop enforced by no byte, mv loses failed batches. kimi: log rotation, STOP race, hardcoded PY path | A-right | fable exact (line 14 STOP-only halt, zero cost bytes in file; line 26 unconditional mv 2>/dev/null); kimi cites lines 32/35/37 on a 30-line file (fabricated), "may miss STOP" is false (loop re-checks at 14: delay, not miss), log-rotation and PY-path true but minor |
| X08 | scripts/descent_driver.sh | sonnet vs haiku | sonnet: mv handoff loses work. haiku: no queue-dir validation, %H%M collision, STOP atomicity | COMPLEMENTARY | sonnet real (22-26); haiku B2 real (25); haiku B1 half-false (the [ -d ] guard EXISTS at 19, only the alert is missing); haiku B3 misattributed (:19 is the queue guard; STOP is 10/14) |
| X09 | watch/inbox/SHARED_SURFACE_CONTRACT.json | fable vs kimi | validator census: fable says 7 of 9 aliases define no validator; kimi flags only openclaw; kimi also claims mag_host PATH hijack | A-right | counted on bytes: 9 aliases, validators only at 35 (mag_host) and 40 (mag_container) = exactly 7 of 9; kimi true-but-understated; kimi's PATH-hijack misnamed (line 35 is a relative path = CWD risk; the real bare-name PATH candidate is line 40, which kimi did not flag) |
| X10 | watch/inbox/SHARED_SURFACE_CONTRACT.json | kimi vs haiku | INDEX.json diagnosis: kimi wants a hash/signature field (integrity); haiku says INDEX is referenced but never defined (no schema) | COMPLEMENTARY | both gaps real and distinct (no law in 12-22 defines INDEX schema; line 19 hashes receipts, never INDEX); both carry bad cites (kimi :15 is the classification law; haiku :2 is the contract's own schema string) |
| X11 | SHARED_SURFACE_CONTRACT.json | fable vs sonnet | CONTROL (known convergent): both claim no concurrency/no-clobber law for INDEX updates | COMPLEMENTARY (calibration pass) | no lock/rename/unique-name rule in laws 12-21; line 20 unenforceable from these bytes; both right, as expected |
| X12 | mag/steer_seal.py | kimi vs haiku | same cited lines 281-283, different claimed defects: kimi says verify() bare-except hides errors; haiku says wall-clock eviction permits frozen-clock replay | BOTH-wrong | 281-283 is FileNonceStore.__init__/signature; kimi's bare-except lives at 350-351 and IS the documented fail-closed contract (docstring 319-321); haiku's fix would reintroduce the documented prior bug (comment 296-298) and the freshness check 342-344 blocks evicted-envelope replay under a normal clock |
| X13 | mag/steer_seal.py | kimi vs sonnet | kimi: LOG None AttributeError before mkdir. sonnet: mode sentinel fails open to warn | B-right | LOG assigned at 48 (never None), None-check at 110 precedes mkdir at 113; kimi's :78 holds neither; sonnet confirmed: resolve_mode fallthrough returns "warn" at 102 after missing (96-97) or garbage (100-101) sentinel; sonnet's 373-379 half (verify discards reason, log under ROOT) settled true by seat bytes (349-352, 48) |
| X14 | mag/steer_seal.py | sonnet vs haiku | CONTROL (known convergent): both say admit(path) strict parse blocks plaintext STOP | A-right (both mechanisms real) | admit calls strict parse_envelope at 399 while admit_text uses _try_parse_envelope at 386; the safe-fail at 360-364 is unreachable for plaintext files; sonnet cited the call site, haiku the docstring |

Tally: 4 A-right, 4 B-right, 4 COMPLEMENTARY, 2 BOTH-wrong. Controls behaved
(X11 complementary as predicted, X14 both-real with a cite-quality split),
so the adjudicator is calibrated, not verdict-happy.

## 2. Unsettled - PREMIUM-TIER (bytes cannot arbitrate, judgment climbs)

1. **X06 residue - the authority model itself.** Sonnet's bypass chain is
   byte-real end to end, but whether it is a HOLE or the intended bootstrap
   depends on a question the bytes cannot answer: who is allowed to write
   `authority_label` into a proposal? The tier gate at 318-321 explicitly
   contemplates a "legacy/self-grant path" docstring; if labels are
   agent-supplied the gate is decorative (sonnet right), if labels are
   ingress-minted the gate is a bootstrap (design right). This is the
   estate's biggest open security-design call from the whole garden.
2. **X14 residue - strict-parse intent vs interrupt law.** The code
   self-contradicts: the admit(path) docstring (391-393) documents strict
   parse as intentional ("never a raw fallback") while the _gate comment
   (356-358) says restrictive is honored "even on verify failure, missing
   key, or no envelope at all" and "interrupt law beats MAC law". DeepSeek
   named it exactly: "intentional, not correct". Which law wins is the
   designer's call, not a byte fact.
3. Instrument note (not premium spend): X02 shows verdicts are sha-locked.
   Sonnet's two "never" claims were byte-true at 22:14Z and byte-false at
   23:03Z. Any future cross-ractor adjudication must stamp every family
   claim with the surface sha it was made against (the census-denominator
   law applied to code review). Fix the GRID schema, do not buy a bigger
   judge for this one.

## 3. The disagreement harvest - what each disagreement reveals (the unique-input ledger)

**kimi (kimi-k2):** the only family that saw the traversal pair (id into
out_path at 263, evidence escape at 132-133) - genuinely unique security
inputs. But: line anchors systematically stale or fabricated (cites past
EOF on the 30-line driver: 32/35/37; :56 for the set at :84; :78 for code
that exists at 110-113; 282-283 for code at 350-351), and it invents
mechanical bugs the code already guards against (LOG-None impossible,
bare-except is documented design). Blind spot: cross-function dataflow (it
read grant() and missed that confirm() never touches the replay set) and
severity ordering (spent its defect budget on log rotation while the file
it reviewed had no spend brake at all).

**claude-sonnet-5.5:** the chain-reasoner. Four separate end-to-end
mechanism walks, all byte-real where the bytes held still (the bypass
chain, the confirm() replay bypass, the redirect key-leak, the mode
sentinel). Blind spot: absolutes rot fast - "finish_reason is never read"
and "never banked" were true when written and dead 45 minutes later when
an 8-line guard landed; sonnet's verdicts are version-locked snapshots,
not laws. Also the only family whose cites were consistently within a few
lines of the truth.

**claude-haiku-4.5:** the fabrication surface of this material. Four
refuted claims (budget string-division, confirm-TTL, wall-clock eviction
as a bug with a fix that reintroduces a documented prior bug, queue-dir
"missing" check), each mechanically plausible and each false against a
guard that already exists, usually with cites pointing at the wrong
function. Its surviving finds are real but shallow-local (%H%M collision,
INDEX schema gap). Blind spot: it models what code of this shape usually
does wrong, then reports that instead of reading the actual guard.

**claude-fable-5.1:** highest precision per answered item (exact 7-of-9
census, the spend-ceiling defect with a constructible falsifier, the
claim-file handoff) - but it only reached 3 of 8 items before the
reasoning-cap burn early-stopped its series. Its blind spot is not
judgment, it is the rail: 12000-token reasoning budget consumed by hidden
reasoning, content channel empty, $0.68 per burn. The animal's judgment is
premium; its transport needs the LESSIG rails or it never gets to use it.

**deepseek-chat (ds41flash, and the adjudicator is the same animal - read
the reflexivity):** as a ractor it found the revision-loss window and the
probe-tail blindness (both true) and its own cite drift exists too
(_refusal_state cited 180-195, lives 167-183); as the X1 adjudicator it
was strictly paste-bound: it refused to rule on three claims whose bytes
were outside the pasted window and said so - zero fabricated verdicts,
zero verdict theater. That honesty profile (names its own blindness
rather than filling it) is exactly why the seat could cheaply complete
its two "unknown" halves by hand from bytes already read.

**glm53flash/qwen38max:** not paired in this matrix (cheapgrid landed
after the mission's pair set was drawn from kimi/sonnet/fable/haiku/ds);
glm's B1 shows it independently converged on the fence TOCTOU. Coverage
gap, not a verdict.

## 4. Meta-findings the matrix adds to the garden

1. **The 4/4-family convergent clusters are bucket artifacts.** B3's
   "4/4 convergent" (fable+haiku+kimi+sonnet on descent_driver.sh bucket 0)
   is a 30-line file: every cite mechanically lands in one bucket. At
   claim level it is 2/4 convergent (sonnet+fable on the spend ceiling and
   mv-loss) plus two families on minor or fabricated items (kimi's
   past-EOF cites, haiku's misattributed :19). Same for the B4 cluster:
   four families, three DIFFERENT diagnoses of INDEX.json (integrity field
   vs schema vs lock law), only complementary, not convergent. Convergence
   at 50-line-bucket granularity overstates agreement; the garden's grid
   should report claim-level convergence or label bucket-level rows as
   co-location, not agreement.
2. **Cite accuracy is itself a family axis.** Ranked on this material:
   sonnet (consistently near) > fable (region-right, few explicit numbers)
   > ds41flash (drift ~15 lines) > kimi (drift 30-190 lines or past EOF) >
   haiku (wrong function). Two of the five BOTH-wrong/lost verdicts were
   decided on cite accuracy, not claim substance.
3. **No family is safe to trust alone on defects-it-claims.** Every family
   produced at least one claim a $0.001 adjudication refuted, and every
   family produced at least one unique true input the others missed. The
   router implication for ractor work: cheap fan-out for COVERAGE, then
   byte adjudication for TRUTH, premium only for INTENT (the two
   premium-tier items above).

Lane X1 seat, 2026-10-01. Batch $0.0153 / $1.00 cap; no commits; receipts
at memory/runs/hermes_burn/xmodel_cross_{items,}.jsonl.
