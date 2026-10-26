# break-operations: hostile second pass on the spore-sharing lens (2026-10-05)

Pass type: byte-check + falsifier execution against the 4-finding spore-sharing lens.
Every check below was executed in this sitting unless marked OWED. Instruments: git
remote/branch/log/count-objects/ls-tree/ls-files/check-ignore/ls-tree(github-master),
grep censuses, Read of cited sources, and an EXECUTED two-process gwap append race on
a temp store. Windows law honored: the race's subprocess spawns carried
creationflags=CREATE_NO_WINDOW (0x08000000). No estate files were edited; the race
wrote only to C:\Users\foste\AppData\Local\Temp\spore_falsifier\store.
(Sitting incident, disclosed: one of my own early commands ran GNU find over the whole
tree into a harness log; killed it, deleted the 1.6 GB log, re-ran with scoped tools.
No repo state touched.)

## Verdict 1: push mechanically dead since 2026-08-20. CONFIRMED, two count corrections.

Byte-exact: remote github = https://github.com/NachoBusiness17/mycelial-republic.git;
github tip = dc66499434b050343e81dabcb45b849c5f1fda29, Date Thu Aug 20 11:28:57 2026
-0400; `git ls-tree -r -l HEAD` census = 56,361 paths / 18,922.7 MB (recomputed from
the dump, identical); watch/inbox = 17,070 files / 4,665.6 MB (identical); every named
oversized size reproduced exactly: ESTATE_INDEX 2406.1 MB x2, attic
hook-state_stale_baselines.tar 2210.9, runaway-evidence 2129.3, ractor_board 677.4,
training/events.jsonl 340.6, tokyo mp4 255.6, catalog.jsonl 235.1. GitHub's rule
confirmed against docs.github.com (about-large-files-on-github): blocks files larger
than 100 MiB, warns over 50 MiB.

Corrections:
1. QUANTIFIER LAW: "seven paths over the cap" is a truncated census. Recensused
   untruncated: 19 paths exceed 100 MiB, adding catalog/tags.jsonl 191.8 MB,
   attic biography_backup tar 181.0, attic leak_reports tar 149.4, kpi gz 126.8,
   tools/godot/Godot_v4.3-stable_win64.exe 126.8, and six watch/inbox/mrpool_export
   media_full mp4s (130.3/124.7/114.4/112.7/108.3/107.6). Direction strengthens the
   finding; the stated count was wrong.
2. The falsifier's self-caveat ("my 18.9 GB double-counts ESTATE_INDEX, tracked
   twice") is false: 0 duplicate paths in ls-tree; the two 2406.1 MB entries are
   DISTINCT paths (dashboard/data/ESTATE_INDEX.jsonl and
   watch/ESTATE_INDEX/ESTATE_INDEX.jsonl). 18,922.7 MB is a clean per-path total.
3. The evidence misquotes `git branch -r`: it prints TWO remote branches
   (github/master AND local/run-beta1-factory-audit-20260914 on a second remote,
   local = C:\Users\foste\Documents\projects\Mag-backup.git) that the lens omitted.
   "Exactly one tracking ref" is true only scoped to the github remote.
4. Falsifier's named instrument run: `git count-objects -vH` = in-pack 160,692,
   size-pack 14.37 GiB (4 temp-pack garbage warnings). Matches sibling moonshot-1's
   14.37 GiB; pack size vs the 18.9 GB uncompressed-HEAD census measure different
   things; both are far past any practical push.

Not run (OWED, same as lens): an actual push of HEAD to a scratch GitHub repo. I will
not provision external repos from a subagent. The 19-over-cap census plus GitHub's
documented 100 MiB block makes the GH001 outcome deterministic on paper; the live
confirmation remains owed.
Move stands: orphan-root allowlist repo, decision written into the regrow guide. ~30 min.

## Verdict 2: spore strips its own DNA. CONFIRMED, instrument upgraded, two cite defects.

Upgraded instrument (the lens had only ignore status, which cannot distinguish
"ignored" from "ignored and already tracked"): `git ls-files` returns NONE of
state/GENOME.md, configs/providers.yaml, watch/inbox/INDEX.json (only .env.example).
They are genuinely untracked; a fresh clone of HEAD lacks all three.
Byte-exact: .gitignore:40 `state/`, :24 `configs/providers.yaml` (comment: "live
provider/mesh credentials - never commit (tracked fix 2026-08-20)"), :249
`watch/inbox/INDEX.json`; route_chat.py:51 providers.yaml read_text inside
_load_lanes(), :67 literal ROOT/.env; _load_lanes() is called at route_chat.py:224,
which precedes the dormant gate (:241-243) and the fence (:249), so a missing
providers.yaml raises FileNotFoundError on the chat door before fence or dormant
gates run (nuance: call-time, not import-time; other entrypoints like doctor are
outside this claim's scope). configs/*.example: none exist. memory/rib = 55 tracked,
memory/rib_bus = 51, exactly as claimed. .env.example = exactly 13 `=` vars
(XAI_API_KEY, XAI_MODEL, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
GROQ_API_KEY, DEEPSEEK_API_KEY, DEEPSEEK_OVERMIND_API_KEY, GEMINI_API_KEY,
TOGETHER_API_KEY, VAST_API_KEY, VAST_OPENAI_BASE_URL, VAST_OPENAI_API_KEY); grep for
HERMES_API_KEY_1/2, XAI_SD_API_KEY, ZAI_API_KEY_Pro, OPENROUTER_API_KEY_2, OR_API_KEY,
GROQ_API_KEY_2, DEEPSEEK_SWARM_API_KEY: zero hits.

Cite defects (conclusion unaffected):
1. providers.yaml:503 does NOT read XAI_SD_API_KEY. Line 503 is the xai lane chain
   `[XAI_API_KEY, XAI_API_KEY_2, GROK_API_KEY, GROK_API_KEY_2]` (block starts :496).
   XAI_SD_API_KEY appears NOWHERE in providers.yaml (grep -i, zero hits); it is an
   AGENTS.md/rib-level name (funded xAI SD account).
2. OPENROUTER_API_KEY_2 / OR_API_KEY sit at providers.yaml:177-178, not :546.
   The remaining five line cites (154, 158, 304, 366, 553) are exact.
Also wider than claimed: the z_ai family ZAI_API_KEY :541, ZAI_API_KEY_Pro :553,
ZAI_API_KEY_Lite :575, ZAI_API_KEY_2 :588 are all absent from .env.example too.
Not run (OWED): the fresh-clone boot repro (no clone made this sitting; the :224 ->
:51 ordering is the evidence).
Move stands, now mechanical: regenerate .env.example by walking providers.yaml's
api_key_env/api_key_envs names; whitelist !state/GENOME.md and !watch/inbox/INDEX.json;
emit providers.example.yaml with values stripped, structure kept. ~45 min.

## Verdict 3: no identity dimension at N=2. CONFIRMED, falsifier EXECUTED this sitting.

Byte-exact: ledger.py SCHEMA_SQL :132-158 verbatim; capability PK (model_id,
task_shape) at :141; verdict_log :143-152 carries no identity column; grep
operator|owner|seat_id|host_id over ledger.py = 6 hits, all prose (:78, :95, :329,
:358, :588, :590); gps_ledger.db3 IS tracked at 782,336 bytes (lens said 0.7 MB,
exact), plus a tracked tools/gps_mcp/gps_ledger.db3.bak_pre_D2_20260930 (32,768
bytes) the lens missed; gwap_payload.py:123 _ROW_KEYS, :704-710 seq==index + prev
chain, :761-763 append refuses broken chain, :93 STORE = memory/runs/gwap (gitignored
via .gitignore:102 `memory/runs/**`; ls-files memory/runs = README.md only);
route_chat.py:301-311 usage row fields verbatim (ts, lane, model, goal, key_env,
prompt_tokens, completion_tokens, content_chars, finish_reason, depth, thinking_sent,
reasoning_tokens, ok), no operator; queue/lanes/research/runner_state.json read:
inbox_offset 14, seat "research", rotation_epoch 249 (seat is the LANE name, not an
operator identity, so "bare single-consumer cursor" holds); mycelium.py:197-227
reinforce is full-file read-modify-write via _rewrite_edges (:226), :243-277 rewrite
with open("w") and no lock anywhere.

Falsifier EXECUTED (the lens only reasoned it): two OS processes, both constructed
SessionLedger("arena-capability") on one TEMP store, barrier-released into the same
second, each append({"schema": "mag_gwap_payload.v1", ...}) with
CREATE_NO_WINDOW spawns. Result: both appended seq 1; file holds 2 rows both seq 1;
verify fails at row 2; and the lockout is CONSTRUCTION-FATAL: a fresh
SessionLedger on the file raises GwapError "arena-capability.jsonl fails verification
at row 2" from __init__ -> _read_rows (gwap_payload.py:730-739) before verify_chain()
can even be called. Sharper than the lens predicted: the store is not just locked
out, it is poisoned until a human edits or deletes rows; there is no self-heal path.
Because append() writes via open("a") (:779) there is no silent clobber, only poison.
Move stands with an amendment: estate_id stamping at an export boundary is necessary
but not sufficient; the chain needs graft semantics (see Addition 5). ~20 min + spec.

## Verdict 4: regrow path exists in bytes but is host-bound. CONFIRMED, one correction.

Byte-exact: 13 register*.ps1 in scripts/ (lens said ~12; the 13th is
register_x_radar_task.ps1), named list otherwise matches; configs/providers.yaml:64
and :486 both `dormant: true` with live-measured cause comments (Saelis 0-use +
refused local default; B2-61 generation 401-dead); route_chat.py:241-243 dormant
refusal verbatim ("lane {lane} is DORMANT (B2-133 gate); operator GO required");
ledger.py:329 "cost is seeded or updated by operators/fixtures" EXACT; no REGROW.md
tracked or on disk (git ls-files and ls, both rc=1); capability-table INSERT sites
census: ledger.py:423 and :600 only, with the fixture/operator direct-write path
upsert_measurement at :588-590; seed_fixtures referenced by gps_mcp README, ledger.py,
tests only (git grep -l seed_fixtures), no alternate tooling seeder found in
tools/gps_mcp (router.py/server.py: no seed refs). Correction: "genome boot order in
tracked bytes" is wrong as written; state/GENOME.md is UNTRACKED (finding 2). Its
"## 3. BOOT ORDER for a cold seat" exists at state/GENOME.md:69 but rides nothing
until the finding-2 whitelist lands. Ordering the lens never stated: finding 2's
whitelist is a PREREQUISITE of finding 4's REGROW.md. Also sharper than "season chain
starts at seq 0 on any clone": the chain does not ship at all (memory/runs/** ignored,
README only), so the regrow guide must say the chain is born empty, and the descent
spend ledger (memory/runs/hermes_burn/usage.jsonl) likewise does not ride.
Move stands: REGROW.md with boot order, genome load, rails default, arena cron,
season chain, plus the prerequisite whitelist step.

## Additions (what the lens missed)

A1. THE PUSH IS A SECRETS LAW, NOT JUST A SIZE LAW, and the estate's own .gitignore
says so. .gitignore:31: "7 live .env values were committed in it (audit 2026-09-30
finding #1)" (memory/trajectory/steps.jsonl, untracked, "history left intact per
operator (no rewrite)"); .gitignore:271: "lan.key untracked same day; rotate - it
remains in history"; :23-27: providers.yaml is "live provider/mesh credentials",
untracked from index 2026-08-20, history intact. I verified the remote TIP is clean
(git ls-tree github/master: no providers.yaml, no state/, no .env, no trajectory),
but older commits on either remote were not audited. Falsifier: a full history sweep
of github/master and local/Mag-backup.git for pre-untrack secret blobs comes back
empty. Move: the regrow guide's first law is "history is radioactive; spore is
orphan-root or nothing", plus a one-sitting history sweep of both remotes. ~40 min.

A2. THE ESTATE'S SECRET GATE IS CHANGED-SCOPE ONLY, so "the tracked tree is clean" is
not in evidence. Today's gate run (watch/inbox/secret_gate_results/
changed_20261005T112735Z.json) scanned 31 changed files, 0 blocking, 10 MB/file cap.
My scoped format census (git grep over tracked *.md/*.txt/*.py/*.yaml/*.yml/*.toml
for sk-or-v1-/sk-ant-api/sk-proj-/xai-/gsk_/Bearer-shape strings) hit ~30 tracked
files; inspection of the hit list shows mostly the gate's own tooling, tests, and
receipts-about-secrets (tools/secret_gate_rules.py, tests/test_gate_blocking_paths.py,
watch/inbox/burn_wave_20260926/B2_73_secret_scan*.md et al). Live-vs-synthetic was
NOT determined (I did not dump key-shaped bytes). OWED: a whole-tree secret census
over all tracked text before the allowlist freezes; the instrument exists
(tools/secret_gate.py, needs a full-tree mode). ~30 min.

A3. OPERATOR ECONOMICS RIDE THE RIBS. The lens cheered "ribs DO ride, good" without
reading what ribs carry: memory/rib/RIB_DRIVING_LADDER_20260928.md,
RIB_DEEPSEEK_ELDER_SEAT.md, and RIB_MODEL_GARDEN_ROUTING.md (all tracked) match
XAI_SD_API_KEY / Nous credits / XAI SD (grep). "Laws stay" ships funding amounts,
account identities, and lane economics to a public repo. Falsifier: the operator
declares ribs public-as-is. Move: a redaction pass or an explicit operator tradeoff
decision recorded in the spore manifest. ~45 min.

A4. THE RECEIPTS SHIP WITHOUT THEIR INDEX. 17,070 tracked watch/inbox files
(4,665.6 MB) ride, but watch/inbox/INDEX.json is gitignored (:249) and untracked, and
AGENTS.md's shared-surface contract says every client reads INDEX.json first. A fresh
spore clone is a 4.66 GB unindexed pile: the estate's own read path is broken on day
one even for content that DID ride. Falsifier: the spore also drops the receipts
(then this becomes moot). Move: whitelist the index (and index_events.jsonl) or
explicitly scope receipts out of the spore. ~10 min.

A5. CHAIN GRAFTING ACROSS ESTATES IS MECHANICALLY IMPOSSIBLE WITHOUT A MERGE PROTOCOL,
so finding 3's export-envelope move is underspecified. Rows chain on prev_sha256 from
a single 64-zero genesis with seq==index enforced (gwap_payload.py:695-711); my
executed race shows even same-estate concurrency poisons the file construction-fatally.
Appending a foreign estate's envelope onto a native chain breaks verification at the
graft row; importing means rewrite, which contradicts append-only. The envelope
{estate_id, exported_at, rows} needs defined semantics: per-estate chain FILES
(estate_id in the filename, zero shared writes) or fork-with-genesis, plus a trust
root exchange (who signed the foreign genesis). Falsifier: two estates graft rows
into one chain file and verify_chain stays green (it cannot, by :704). Move: 30 min
of spec in the regrow guide before any envelope code is written.

A6. LANE KEY INVENTORY IS THE RIGHT SPINE FOR THE TUTORIAL, and it is derivable:
providers.yaml carries api_key_env/api_key_envs per lane (hermes :154/:158, openrouter
family :177-178, groq :304, deepseek :366, z_ai family :541/:553/:575/:588, xai chain
:500-503), dormant flags with measured causes (:64, :486), and the dormant gate plus
operator_go already implement "dormant until needed" (route_chat.py:241-243). The
tutorial and providers.example.yaml should be GENERATED from this one source, not
hand-written, or the ladder doc drifts from the config the way .env.example already
has (13 vars vs at least 20 live names). Falsifier: every api_key_env name in
providers.yaml resolves from the regenerated .env.example. Move: fold into finding
2's sitting; +10 min.

## OWED (not run here, never asserted)

1. Live push of a HEAD-containing ref to a scratch GitHub repo (finding 1 falsifier).
2. Fresh-clone repro of the route_chat FileNotFoundError (finding 2 falsifier).
3. Whole-tree live-secret determination over all 56,361 tracked paths (A2 scope).
4. History sweep of both remotes for pre-untrack secret blobs (A1).
5. providers.yaml:503 "0.7 MB" adjacent claims beyond those re-measured: all sizes
   re-verified here came from the spool of `git ls-tree -r -l HEAD` this sitting.

## Carrier

Banked: watch/inbox/ractor_engine/2026-10-05-spore-sharing/break-operations.md.
Instruments available for re-run: C:\Users\foste\AppData\Local\Temp\spore_lstree.txt,
spore_lsfiles.txt, spore_census.py, spore_falsify_gwap.py.
