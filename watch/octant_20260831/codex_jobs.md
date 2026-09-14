# Codex job contracts — wave 2 (codex-brief-writer, 2026-08-31)

Two host-side codex jobs, staged from T2/T-verdicts. Schema exemplar: `/mag/jobs/reset-burn-codex/seat_contract.json` (seat_contract.v1). Precondition for BOTH: the 11 patches are applied on host (`python -m mag.openclaw_patches apply`, runbook §2). `checkpoint_schema.required` is byte-identical to the exemplar so existing validators pass; extras are optional fields.

---

## Job 1 — codex-outcome-memory

```json
{
  "schema": "seat_contract.v1",
  "job_id": "codex-outcome-memory",
  "goal": "Prove the T2 outcome-memory wire is closed: after patch 6a/6b apply, one live POST /room/spawn on the host gateway auto-records a kind:outcome row into /mag/memory/runs/ask_router/ledger.jsonl (ledger had zero rows at 10:00Z; T2 receipts all showed ledger_rows:0). Anchor row zero first via the runbook §3 pipe so the spawn row is 1+, then wire-test, then assert.",
  "invariants": [
    "host-only: run from D:\\mag with D:\\mag\\.venv\\Scripts\\python.exe or mag.cmd — never PATH python, never WSL python (vsock precedent kills .venv cage-side)",
    "step 0: discover the effective key with python -c \"import sys;sys.path.insert(0,r'D:\\mag');from mag import api_gateway;print(api_gateway.api_key())\" and use THAT value in X-API-Key (or ?key=) — default is mag-local-dev-key but MAG_API_KEY may override",
    "use the watcher preset (cheapest lane, deepseek-v4-flash, ~$0); ONE spawn, max 3 total attempts; embed the marker string 'outcome-wire-test' in the PROMPT (record_outcome stores task=prompt[:160], the thread name alone is not in the ledger row)",
    "spawn is async: poll GET /room/thread/outcome-wire-test?n=10 up to 120s for seat 'jit-watcher' event 'spawn_result' before declaring failure",
    "ledger.jsonl is append-only: never edit or delete rows; if the spawn's auto-record row does not appear, do NOT synthesize one — a manual `--record` stdin pipe is diagnostic-only evidence of cmd_record health and must be marked source=manual-fallback in the trail, not passed off as the wire test",
    "if ledger has no kind:outcome rows at all and the gateway shows the 6b code path missing, STOP — patches were not applied; report, do not self-patch"
  ],
  "forbidden_moves": [
    "hand-editing ledger.jsonl or fabricating a kind:outcome row to pass acceptance",
    "restarting mag_launch / the gateway to 'fix' a missing row — report instead",
    "touching any file outside memory/runs/ask_router/ and the trail FILE (scope is ask_router + the spawn wire; no P1/P2/P3/P4 code)",
    "more than 3 spawn attempts",
    "declaring success from the spawn_result room post alone without the ledger row (room post is not outcome memory)"
  ],
  "acceptance_commands": [
    "cd D:\\mag && .venv\\Scripts\\python.exe -c \"import sys;sys.path.insert(0,r'D:\\mag');from mag import api_gateway;print(api_gateway.api_key())\"",
    "type D:\\board\\ask_router_row0.json | D:\\mag\\.venv\\Scripts\\python.exe -m mag.ask_router --record",
    "curl.exe -s -X POST http://127.0.0.1:8001/room/spawn -H \"X-API-Key: <key-from-step-0>\" -H \"Content-Type: application/json\" -d \"{\\\"agent\\\":\\\"watcher\\\",\\\"thread\\\":\\\"outcome-wire-test\\\",\\\"prompt\\\":\\\"outcome-wire-test: reply with the single word RECEIPT and nothing else\\\"}\"",
    "curl.exe -s \"http://127.0.0.1:8001/room/thread/outcome-wire-test?n=10&key=<key-from-step-0>\"",
    ".venv\\Scripts\\python.exe -c \"import json,sys; rows=[json.loads(l) for l in open(r'D:\\mag\\memory\\runs\\ask_router\\ledger.jsonl',encoding='utf-8') if l.strip()]; wire=[r for r in rows if r.get('kind')=='outcome' and 'outcome-wire-test' in (r.get('task_head') or '')]; print(json.dumps({'ledger_total':len(rows),'wire_rows':wire},indent=2)); sys.exit(0 if wire else 1)\""
  ],
  "checkpoint_schema": {"required": ["completed", "artifacts", "failures", "budget_used_pct", "next_action_one_line"], "optional": {"ledger_rows_before": "int", "ledger_rows_after": "int", "wire_row": "the matched kind:outcome row verbatim", "spawn_ok": "bool from spawn_result text"}},
  "handoff_schema": {"required": ["done", "untested", "blocked", "resume_command"]},
  "resume_command": "read jobs/codex-outcome-memory/seat_contract.json. Run acceptance_commands in order (skip cmd 2 if a kind:outcome row already exists). If cmd 5 exits 0, FILE trail_codex_outcome_memory_1.md with the wire_row verbatim + spawn_result excerpt + ledger_rows before/after; if it exits 1, capture gateway response + thread tail and mark blocked:wire. Stop after one trail."
}
```

---

## Job 2 — codex-atlas-build

```json
{
  "schema": "seat_contract.v1",
  "job_id": "codex-atlas-build",
  "goal": "Run `python -m mag.atlas build` on the host post-apply, then compare the actual output shape (/mag/memory/runs/atlas/atlas.json, schema atlas.v1) against the spec in /board/octant_20260831/atlas_draft.md and FILE a receipts-first diff trail on /board. The draft is the SPEC, the build is the EVIDENCE; divergences are findings to emit, not bugs to fix in this job. This trail is the first /board atlas/basecamp receipt (zero exist at 10:51Z).",
  "invariants": [
    "host-only from D:\\mag with .venv python; build makes no model/network calls but imports patched code — run it AFTER `python -m mag.openclaw_patches apply` (runbook §6 order)",
    "baseline = the newest pre-existing row in /mag/memory/runs/atlas/receipts.jsonl BEFORE this build (cage-provisional: 2026-08-31T04:54:44Z, summary DECLARED 27 / INSTRUMENTED 26 / WIRED 27 / STATEFUL 25 / VERIFIED 27 / LIVE 17); the summary delta is the patch-effect evidence — report it, do not tune it",
    "compare section-by-section: atlas.v1 emits {schema, ts, scope, summary, organs, graph, law}; the draft demands 7 sections incl. per-claim receipts with sha256 + checked_at + status ladder (VERIFIED/CORRECTED/ATTESTED/INCONCLUSIVE/UNMAPPED) — emit one row per draft section: MATCHED / CONFLICT (both pointers) / UNMAPPED, per the draft's unknown-stays-unknown policy",
    "no editing atlas.py / organ_map.py / the draft — shape diff only; organ_map's ask_router wired_by still lists only afk_cadence/dogfood_audit (read-path), so post-6a/6b the map cannot see the new write-path wire: emit that as a CONFLICT/UNMAPPED row, expected finding",
    "the trail carries POINTERS into memory/runs/atlas/ (sha256 computed at build time host-side); do not copy large JSON onto /board",
    "INCONCLUSIVE stays INCONCLUSIVE with reason; absence of a draft section in output emits UNMAPPED, never a fabricated match"
  ],
  "forbidden_moves": [
    "editing atlas.py, organ_map.py, or atlas_draft.md to force a MATCHED verdict",
    "pre-computing or copying sha256 values from cage-side listings (stale hashes false-certify; hashing is build-time host work)",
    "promoting ATTESTED rows to VERIFIED without a build-time byte-check receipt",
    "running the build WSL-side or with PATH python",
    "treating a shape mismatch as job failure — the diff trail IS the deliverable; only a failed build command (exit != 0) is"
  ],
  "acceptance_commands": [
    "cd D:\\mag && .venv\\Scripts\\python.exe -m mag.atlas build",
    ".venv\\Scripts\\python.exe -m mag.atlas status",
    ".venv\\Scripts\\python.exe -c \"import json;d=json.load(open(r'D:\\mag\\memory\\runs\\atlas\\atlas.json',encoding='utf-8'));print(json.dumps({'ts':d['ts'],'scope':d['scope'],'summary':d['summary'],'organ_count':len(d['organs']),'graph_keys':sorted(d['graph'].keys()) if isinstance(d.get('graph'),dict) else type(d.get('graph')).__name__},indent=1))\"",
    ".venv\\Scripts\\python.exe -c \"import json,hashlib; p=r'D:\\mag\\memory\\runs\\atlas\\atlas.json'; print(hashlib.sha256(open(p,'rb').read()).hexdigest())\""
  ],
  "checkpoint_schema": {"required": ["completed", "artifacts", "failures", "budget_used_pct", "next_action_one_line"], "optional": {"atlas_ts": "build ts", "summary": "atlas.v1 summary dict", "baseline": "newest pre-build receipts.jsonl row", "draft_sections_matched": "x of 7", "conflict_rows": "list of CONFLICT/UNMAPPED row ids"}},
  "handoff_schema": {"required": ["done", "untested", "blocked", "resume_command"]},
  "resume_command": "read jobs/codex-atlas-build/seat_contract.json. Run acceptance_commands (all four must run; build exit 0 is the gate). Write /board/octant_20260831/atlas_build_diff.md: build ts + sha256, summary delta vs baseline receipt, 7-row section table (MATCHED/CONFLICT/UNMAPPED) with both pointers per CONFLICT, ask_router write-path wire finding, unknown-stays-unknown statement. FILE and stop."
}
```

---

### Self-attack (one pass, per charter efficiency law §2)

Weakest sentence found: acceptance cmd 2 of job 1 assumed the default API key `mag-local-dev-key` — if `MAG_API_KEY` is set on the host, every curl 401s and the job stalls on a guess. **Fix:** added invariant step 0 (discover effective key via `api_gateway.api_key()` and feed it into all curl calls). Second-weak: job 2 hardcoded the 04:54:44Z baseline as gospel; reframed as "cage-provisional baseline, re-derive newest pre-build receipt host-side." Both fixed in the JSON above.
