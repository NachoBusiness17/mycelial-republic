# credrot-two: 18-credential rotation decision packet (masked surface only) 2026-09-26

Card credrot, candidate two. Operator decision packet for the B2-73 dump
exposure. Built exclusively from the masked surface: the B2_73 receipt family,
the scanner results JSON (masked fields only), the rotation policy, root .env
name+masked-head census, configs/providers.yaml, configs/keys.json, consumer
greps, and scheduled-task query. The corpus carrier files were NEVER opened
(HARD LAW held); carrier names below come from the findings JSON paths and
receipt prose only. No credential value appears in this artifact: every value
reference is a masked head already published in
`watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md` (the mask law,
6-8 char head plus length, policy section 1).

## Approach

Method, in the order run this session:

1. Read the start family: `B2_73_secret_scan_20260926.md` (verdict, census
   heads, falsifier), `SECRET_SCAN_RULESET_ROTATION_20260926.md` (the policy
   this packet executes), `B2_73_dump_census.py` (census instrument shape).
2. Verified the results JSON is value-free before aggregating it: findings
   carry only `file`, `kind`, `line`, `masked`, `entropy`; max masked length
   18 across the first 5000 rows (6 chars + "...(len=N)"). Aggregated per-head
   occurrence counts and carrier files from it.
3. Ran a root .env census printing NAME + masked head only (8-14 chars,
   values never printed): this resolves, per exposed value, whether it is the
   CURRENT rest-place value (rotation owed) or an orphan (console audit only).
4. Mapped blast radius: `configs/providers.yaml` lane blocks (env refs per
   lane), `configs/keys.json` manifest (verified value-free: 0 hits for
   sk-/gsk/32-hex/xai shapes in its 4804 bytes), per-name consumer counts
   (`grep -rw --include=*.py` over `mag/ tools/ scripts/ main.py`), alias
   names in .env, scheduled tasks (`schtasks //Query //FO CSV`).
5. Verified every verify-instrument this packet names exists:
   `tools/openrouter_free_gate.py`, `mag/doctor.py:591
   check_provider_endpoints`, `mag/key_law.py:50` (reads `os.environ` after
   `load_dotenv`, so .env is the single rest place and readers are
   value-agnostic), `B2_235_mimo_revival_20260926.md` (opencode transport).

**The load-bearing delta over the B2-73 receipt.** The receipt said the
exposed values are "plausibly the still-live rest-place entries" (line 15).
The at-rest census resolves this per value: **13 of 18 exposed heads byte-match
a current .env name (rotation owed); 5 match no current rest place (console
audit, delete if present, no .env change)**. The five orphans: Groq gsk_17bq,
Groq gsk_8LAQ (current .env holds gsk_QI6o / gsk_w2pt — both differ), ZAI
088650c6 (36 occurrences, the most-repeated ZAI value in the dump, held by no
current name), DeepSeek sk-c2bd8 (only sk-effc9 is at rest), xAI xai-gO (only
xai-68sO is at rest). Two phantom names discovered: `ANTHROPIC_API_KEY_2` and
`ZAI_API_KEY_3` have ZERO code consumers and no providers.yaml reference
(`ANTHROPIC_API_KEY_2` is not even declared in keys.json; `ZAI_API_KEY_3` is
declared alias-pool, `configs/keys.json:36-41`).

**Ordering principle.** Bank zero-blast wins first (retire phantom names,
proves the runbook), console audits second (no local change at all), live
lanes third one-per-sitting with a verify gate before revoke, and the two
coding-plan ZAI keys LAST at a window close because rotating them while z.ai
sessions are live kills tethered seats (the AGENTS.md fan-out law context;
this panel itself rides that account family). Policy trigger already fired:
event-driven immediate rotation, operator-gated (policy section 3, "a key hits
in a scan report"); this packet is that operator gate.

Common rollback chassis (R0-R3), cited per row below by reference:

- **R0 (pre-snapshot + journal):** copy `.env` to `.env.prerotation-20260926`
  (untracked: `.gitignore:19-22`; `.env` itself confirmed untracked via
  `git ls-files --error-unmatch .env` failing). Journal
  `watch/inbox/KEY_ROTATION_JOURNAL.jsonl` per policy section 2 — verified NOT
  YET EXISTING today; the first rotation creates it. Row shape: date, env
  name, old masked head, new masked head, action, verifier result.
- **R1 (mint-before-revoke):** where the provider console allows concurrent
  keys, mint the new key and place it in .env while the old key still works.
  Whether each console allows this is an operator-console fact, not verifiable
  locally (no network in this lane, per the B2-73 discipline); if a console
  forces single-key, R3 is the rollback.
- **R2 (verify gate before revoke):** one cheap call through the real consumer
  path, instrument named per row. Only after PASS does the old key get
  revoked.
- **R3 (unrecoverable-revoke fallback):** after revocation the old value is
  gone forever; recovery is still guaranteed cheap because every lane is
  value-agnostic by the KEY LAW — `mag/key_law.py:50` resolves names from
  `os.environ` at call time, so placing ANY working value under the canonical
  name restores the lane. Last resort: mark the lane `dormant: true` in
  providers.yaml and route around it (established pattern, e.g. the anthropic
  lane's own note pointing free-tier traffic at openrouter anthropic/*,
  `configs/providers.yaml:296`).
- **Retire/delete shape:** for names with 0 code consumers, removal cannot
  break any lane by construction; rollback is "re-add the name with a fresh
  mint" if a need ever appears.

Timed consumers to respect: `MagImproveDaily` 08:00 runs the weekly deep
provider probe (one-token ping per lane via `mag/doctor.py:591`, cadence-gated
at `mag/improve.py:399-457`) — it reads .env at call time, so a rotation
landed before 08:00 is invisible to it; `MagCensusPatrolDaily` 08:30 and
`MagFtsIndexDaily` 09:00 are local-only (no provider keys);
`MagMimoWatchHourly` rides the opencode client (OPENCODE keys, not in the 18).

## Moves with estate paths

### Wave 1 — zero-blast retirements (do first; banks the runbook)

| # | Credential (masked head, receipt-cited) | Rest place | Exposure | Blast radius | Action | Rollback |
|---|---|---|---|---|---|---|
| 1 | Anthropic `sk-ant-api03-IWEF...` | `.env ANTHROPIC_API_KEY_2` (14th char `I` matches IWEF head; `_NxL`'s 14th char is `_`) | codex dump copies carry both Anthropic values (receipt lines 48-50); occurrence count not quoted per key | **Zero**: 0 py consumers (`grep -rw`), no providers.yaml ref, NOT declared in keys.json (phantom name) | Revoke at Anthropic console, delete the .env line, journal | Retire shape: nothing consumes it, removal cannot break a lane; re-add with a fresh mint if a spare is ever wanted |

| # | Credential | Rest place | Exposure | Blast radius | Action | Rollback |
|---|---|---|---|---|---|---|
| 2 | ZAI `bafc5c96...` (1x) | `.env ZAI_API_KEY_3` | census 1 occurrence | **Zero**: 0 py consumers; keys.json zai_second_2 "alias-pool same_account_as_second_1" (`configs/keys.json:36-41`); no providers.yaml ref | Console delete if the key still exists; retire the name (or rotate in place if the alias-pool is wanted) | Retire shape (same as row 1) |
| 3 | Vast.ai `6881759e...` | `.env VASTAI_API_KEY` | distinct=1 in census (count not quoted) | 3 py consumers; keys.json vastai_1 "legacy live env key, boot audit 2026-09-24" (`configs/keys.json:177-182`); the providers.yaml vast lane reads `VAST_OPENAI_API_KEY` which is ABSENT from .env (that lane is dark) | Mint new vast.ai key, update the name, verify one vast_cost/doctor call, revoke old | Chassis R0-R3 |

### Wave 2 — console audits for the 5 orphans (no .env change; exposure values not at rest)

| # | Credential (masked head) | Why orphan (byte evidence) | Exposure | Action | Rollback |
|---|---|---|---|---|---|
| 4 | Groq `gsk_17bq...` | current .env `GROQ_API_KEY` head is `gsk_QI6o...` — differs | 14 rule hits / 7 files (findings JSON) | List keys in Groq console; delete 17bq if present; journal outcome; if absent the exposure row CLOSES (this is a partial hit on the B2-73 falsifier inversion 3) | Nothing local references it; deletion cannot break a lane; re-mint if ever needed |
| 5 | Groq `gsk_8LAQ...` | current `GROQ_API_KEY_2` head is `gsk_w2pt...` — differs | 14 rule hits / 7 files | Same as row 4 | Same as row 4 |
| 6 | ZAI `088650c6...` | no current .env name holds it (five ZAI names hold 3254aca9/e3c50501/bafc5c96/e18faf05/4f8ac54f) | **36 occurrences — the most-repeated ZAI value in the dump** | Console audit at z.ai; delete if the old key still exists; journal | Same orphan shape |
| 7 | DeepSeek `sk-c2bd8...` | only `DEEPSEEK_API_KEY=sk-effc9...` is at rest; `DEEPSEEK_SWARM_API_KEY` absent from .env | census 4 occurrences | Console audit; delete if present; journal | Same orphan shape |
| 8 | xAI `xai-gO...` | only `XAI_API_KEY=xai-68sO...` at rest; `XAI_API_KEY_2` absent | 2 rule hits / 2 files (grok chat_history + `prompt_history.jsonl`, the bare paste) | Console audit; delete if present; journal | Same orphan shape |

### Wave 3 — live-lane rotations, one per sitting, verify-gated (13 at-rest values minus the 3 in wave 1 = 10)

Order rationale: widest exposure and paid lanes early, widest CODE surface
scheduled into a quiet window, the failover-chain pair split across sittings,
session-bearing coding keys last.

| # | Credential (masked head) | Rest place | Exposure (instrument named) | Blast radius | Verify instrument (R2) | Rollback |
|---|---|---|---|---|---|---|
| 9 | OpenAI `sk-proj-UjAW...` | `.env OPENAI_API_KEY` | **43 occurrences (census) — widest of all 18**; 14 rule hits / 7 files (findings) | 6 py consumers; openai lane paid, quota 100 calls/mo (`configs/providers.yaml:264`) | `mag doctor` one-token ping on the openai lane | Chassis R0-R3 |
| 10 | ZAI `e18faf05...` | `.env ZAI_API_KEY_Pro` | 34 occurrences (census) | 4 py consumers; z_ai2 fleet cache-mining lane, base `/api/coding/paas/v4`, retry_overload armed | one glm flash call through the z_ai2 lane | Chassis R0-R3 |
| 11 | ZAI `4f8ac54f...` | `.env ZAI_API_KEY_Lite` | 34 occurrences (census) | 13 py consumers; z_ai3 lane, lite_guard ceiling (`configs/keys.json:25-30`) | one glm flash call through the z_ai3 lane | Chassis R0-R3 |
| 12 | xAI `xai-68sO...` | `.env XAI_API_KEY` | 21 occurrences (census); 16 rule hits / 9 files (findings) | 16 py consumers BUT keys.json marks grok_cash "PAYG_blocked_by_grok_route_law, armed-only-by-operator" (`configs/keys.json:51-56`) — real usage is operator-gated, so rotation blast is minimal | operator-armed grok call when next armed | Chassis R0-R3 |
| 13 | DeepSeek `sk-effc9...` | `.env DEEPSEEK_API_KEY` | 23 occurrences (census); 16 rule hits / 9 files (findings) | **30 py consumers — widest code surface of the 18**; workhorse paid lane (`configs/keys.json:79-83`) | `mag doctor` deepseek ping; schedule away from burn waves | Chassis R0-R3; route-around: openrouter deepseek models on the OR chain while in flight |
| 14 | OpenRouter `sk-or-v1-4167...` | `.env OPENROUTER_API_KEY` | both OR keys total 28 rule hits / 7 files (findings; 6-char mask merges the pair) | 24 py consumers; the chain's funded account (nacho) per `configs/providers.yaml:174-178` | `tools/openrouter_free_gate.py` (B2-295 instrument, PASS = HTTP 200 non-empty) | **Built-in redundancy**: the chain fails over to `_2` while key 1 is in flight (`configs/providers.yaml:178` chain comment); NEVER rotate both OR keys in one sitting |
| 15 | OpenRouter `sk-or-v1-6be0...` | `.env OPENROUTER_API_KEY_2` | as row 14 | 17 py consumers; free-tier account (fostertron/ox) | same gate, on key _2 | mirror of row 14 (key 1 carries the chain) |
| 16 | Anthropic `sk-ant-api03-_NxL...` | `.env ANTHROPIC_API_KEY` (14th char `_`) | codex dump copies (receipt lines 48-50) | 4 py consumers; anthropic_1 "legacy live env key, boot audit 2026-09-24" active (`configs/keys.json:147-152`) | `mag doctor` anthropic lane ping | Chassis R0-R3; route-around already documented in-lane (`configs/providers.yaml:296`) |

### Wave 4 — session-bearing coding keys, LAST, at a window close

| # | Credential (masked head) | Rest place | Exposure | Blast radius | Verify instrument (R2) | Rollback |
|---|---|---|---|---|---|---|
| 17 | ZAI `3254aca9...` | `.env ZAI_API_KEY` | 19 occurrences (census) | 15 py consumers; z_ai main coding-plan key, "opencode harness ONLY" (`configs/providers.yaml:541` area); **rotating while z.ai sessions are live kills tethered seats — this account family powers the current panel and opencode seats** | opencode client path (B2-235 proven transport, `watch/inbox/burn_wave_20260926/B2_235_mimo_revival_20260926.md`) | Chassis R0-R3, executed at window close when no sessions ride the key; mid-flight failure = finish window on the still-live old key, retry next close |
| 18 | ZAI `e3c50501...` | `.env ZAI_API_KEY_2` | 16 occurrences (census) | 4 py consumers; z_ai4 "coding-plan key #2 (sd Max), opencode harness ONLY" | same opencode transport on key _2 | same as row 17 |

Estate paths touched by these moves: root `.env` (the only rest place,
`mag/key_law.py:50`); `watch/inbox/KEY_ROTATION_JOURNAL.jsonl` (created on
first rotation); `configs/keys.json` (retire rows 1-2 cleanly; if the operator
keeps `ANTHROPIC_API_KEY_2` as a spare it must be DECLARED there per the KEY
LAW header, `configs/keys.json:2`); provider consoles (mint/revoke, operator
hands only — model text can propose, only the operator authorizes effects).

## Falsifier

- **Kill the at-rest mapping:** rerun the .env name+head census (the exact
  one-liner this lane ran, masked heads only) and show a mismatch where I
  claim a match, or a current name carrying one of the five orphans
  (17bq/8LAQ/088650c6/c2bd8/gO). The mapping dies with one head contradiction.
- **Kill the "zero consumer" retirements:** show any consumer of
  `ANTHROPIC_API_KEY_2` or `ZAI_API_KEY_3` my grep missed. My grep was
  `grep -rw --include=*.py` over `mag/ tools/ scripts/ main.py`; surfaces
  NOT searched are named in Owed — a hit there demotes rows 1-2 to chassis
  R0-R3 rotations, it does not kill the packet.
- **Kill the rollback chassis:** demonstrate one lane whose recovery needs
  more than "any working value under the canonical name" (e.g. a consumer
  hard-coding value fragments or a second rest place outside .env).
- **Close (not kill) wave 2:** provider-side evidence that an orphan key was
  already revoked before 2026-09-26 converts its row to CLOSED in the
  journal; that also partially lands the B2-73 receipt's own falsifier
  inversion 3 ("all exposed families already revoked").
- **Kill the rotate order:** show a wave-3 lane whose rotation must precede
  wave 1 for safety (e.g. active abuse burning credit on a paid key right
  now — that is new evidence, and the right response is to pull that one row
  forward, not to reorder the chassis).

## Owed

- **Console multi-key policy unverified** (R1): whether each provider allows
  mint-before-revoke is operator-console knowledge; no network in this lane.
  R3 covers the single-key-console case either way.
- **Orphan liveness unverifiable locally:** whether gsk_17bq / gsk_8LAQ /
  088650c6 / sk-c2bd8 / xai-gO still exist provider-side. Wave 2 exists
  precisely because this cannot be resolved from bytes here.
- **Consumer grep surface:** `*.py` in `mag/ tools/ scripts/` + `main.py`
  only. NOT searched: `.ps1`/`.cmd`/`.yaml`/`.json` consumers outside
  configs, other repositories on this machine, opencode/zcode client config
  outside the repo (B2-235 shows opencode sourcing root .env, which IS
  covered by the rest-place census).
- **The 19-file carrier census:** the B2-73 receipt's number, from the dump
  census instrument. My findings-JSON union of rule-tagged hits is 12 files;
  the 7-file delta is values classified only under ENV-ASSIGN/triage kinds
  where the stored mask hides value identity (ENV-ASSIGN masks the env NAME,
  verified this session). Exact per-file attribution for those 7 would
  require rerunning `B2_73_dump_census.py`, which opens corpus files — NOT
  done, HARD LAW.
- **keys.json cleanup decision** for the two phantom names (declare vs
  retire) is the operator's KEY LAW call; this packet recommends retire for
  `ANTHROPIC_API_KEY_2` (undeclared) and either-or for `ZAI_API_KEY_3`
  (declared alias-pool).
- **Journal does not exist yet** (`watch/inbox/KEY_ROTATION_JOURNAL.jsonl`
  absent today, verified): first rotation creates it; the row schema in R0 is
  this packet's proposal, not a filed law.
