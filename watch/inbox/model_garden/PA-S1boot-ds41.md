# PA-S1boot-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# STRANGER AUDIT, SURFACE 1: THE BOOT PATH

Auditor posture: hostile outsider, repo in hand, no prior context. Every claim below cites `file:line` against the evidence bytes shipped with this task. Where I cite a line I could not read (truncation cut it), I mark UNVERIFIED and name why.

Deliverable order per contract: (1) attack surface map, (2) three weakest joints ranked, (3) patch spec per joint, (4) first thing I probe as the actual stranger with the zip. One landable artifact per joint, and I name each patch's own falsifier.

---

## 1. ATTACK SURFACE MAP (from the boot path alone)

What the boot path is, in the evidence: `mag.hermes_warm_boot` (evidence file `00__hermes_warm_boot.py`, header docstring lines 3-11, `warm_boot()` invoked from `main()`), plus AGENTS.md `Warm boot:` line instructing every seat to run it, plus `watch/inbox/next-window-handoff.md` step 2 (`Warm: memory/briefs/latest.md → state/CURRENT.md → ./mag.cmd context-pack → queue/todo.md`), plus `context_pack.py` which is the pack the boot feeds.

### 1a. READ accessor learns

| Surface | Byte source | What it wins |
|---|---|---|
| Hardcoded deployment URL | `00__hermes_warm_boot.py` L46-48, `_DEFAULT_KNOWN_URLS = ["https://vercel-deploy-7jx41m3r3-mag-d961.vercel.app/public/soul_frontier.html"]` | A live-looking Vercel hostname; the reader can `curl -I` it themselves, or brute `vercel-deploy-*` sibling slugs. |
| Boot reads `configs/deployments.json` for `known_urls` | same file, `_deployment_urls()` body (`DEPLOYMENTS_CONFIG = ROOT / "configs" / "deployments.json"` L38, read at `_deployment_urls`) | A ready-made registry of every deployed surface the operator tracks, handed to the reader as a "known URLs" list. The regex-shaped `vercel-deploy-7jx41m3r3-mag-d961` slug is a namespace the reader can scan. |
| Boot reads `memory/briefs/latest.md` | header docstring L6-7; `BRIEF = ROOT / "memory" / "briefs" / "latest.md"` L34 | Whatever the last window filed as its brief. AGENTS.md says the brief is loaded at warm by every seat. The reader learns the current working set, the operators' pending decisions, tunnel names, external endpoints named in the brief. |
| Boot reads `memory/biography/verkle_chain.jsonl` tip | same header, `CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"` L33 | Chain root hash, index, ts, `dominant_theme`. Not a secret, but a stable fingerprint of the estate's state to whoever holds the repo later. |
| Boot writes `memory/warm_state.json` | `STATE = ROOT / "memory" / "warm_state.json"` L32, `STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")` L~ end of `main()` | Overwrites with the current chain tip + deployment URL list + brief char count. Any process on the box can read it after the first boot. Also: it is the reader's warm-state cache if they want to know what the last run of boot saw. |
| Env var `MAG_DEPLOYMENTS` consumed as JSON | `_deployment_urls()`: `raw = os.environ.get("MAG_DEPLOYMENTS")` and `json.loads(raw)` | If leaked or read from a shell history, the env value is a JSON list of URLs the operator wants known. The env is the highest-priority source for the registry (`env > configs > default` per the function body). |
| Handoff file `next-window-handoff.md` (evidence `01__next-window-handoff.md`) | Procedure §1-§5, plus STATE blob | Names every load path the seat must read (`docs/FRAMEWORK_LOAD.md`, compass, `AGENTS.md`, `memory/briefs/latest.md`, `state/CURRENT.md`, `./mag.cmd context-pack`, `queue/todo.md`, `watch/inbox/index_events.jsonl`). Gives the reader the exact list of files sealed seats are instructed to trust. Also names operator-signed actions ("Operator signs as Mark; journals arrive as photos"), T0/T1 scope ("T0/T1 local only"), and remote rules ("Pack+goal to remotes, never chat history"). |
| `state/CURRENT.md` (evidence `02__CURRENT.md`) | Whole file, 22 lines | Goal ("sovereign game platform last-mile"), last result path, and the fact that the AG6 CURRENT/ANCHOR guards landed (names a receipt). Freshness stamp `updated: 2026-09-30T11:56:08.790449+00:00`. |
| `AGENTS.md` (evidence `03__AGENTS.md`) | Header, DNA block, shared surface table, host paths | Full local paths: `watch\inbox\INDEX.json`, `Docker /board/inbox/`, `WSL /mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/INDEX.json`. The `foste` Windows account name is a free bit for the reader. Also names the operator's venv path `.venv\Scripts\python.exe`. Names the deployment host, the boot instruction, and the schema `hermes_warm_state.v1`. |
| `context_pack.py` (evidence `04__context_pack.py`) | MODE_CONFIG table + preamble builder | The preamble template the model sees, including the literal string `# Mag agent preamble (coarse elephant — not DNA)`, `base_id`, `base_tip`, `git_sha`, `goal_block`, `keys_line` and the line `Do not invent body/keys/status`. A reader learns exactly which fields the running agent believes are authoritative. |
| `context_pack.py` writes offload JSONL | `PACK_OFFLOAD_FILE = ROOT / "watch" / "inbox" / "PACK_OFFLOAD.jsonl"` and `_emit_pack_offload()` opening `"a"` | Every overflow event writes a row naming `mode`, `max_chars`, `total_chars`, `shed_sections`, `stage`, `root_short`, and a UTC ts. A reader with read access gets a running log of what the pack was NOT able to include, indexed by chain root. That is a probe target for what the seat is missing at any given moment. |

### 1b. WRITE access can poison (the memlance as weapon)

Ranked by blast radius, tightest first:

1. `memory/briefs/latest.md`. `mag.hermes_warm_boot` reads it into `session_brief`; AGENTS.md says every seat loads it as step 2 of warm. A poisoned brief is read back into every downstream seat's context pack and (per `MODE_CONFIG`) counts against `max_brief` (400 for janitor, 1200 plan/full). The brief is the highest-trust input because AGENTS.md explicitly names it the warm step; there is no signature gate on it visible in the evidence.

2. `configs/deployments.json`, `known_urls` field. `_deployment_urls()` returns config-known URLs to any caller of `warm_boot()` and to `--check-deployments`, which HEAD-probes each one (`_head_no_redirect`, `urllib.request` with `_NoRedirect` handler). A writer who swaps this for a list of attacker-controlled hostnames makes every seat that runs `--check-deployments` issue outbound HEAD requests from the operator's box. That is an SSRF primitive with the estate's TLS fingerprint. The env var `MAG_DEPLOYMENTS` is a same-priority channel if the writer can influence the shell environment of a seat.

3. `memory/biography/verkle_chain.jsonl` (the chain tip file). `_chain_tip()` reads the last line and parses JSON. A writer appends a crafted knot: any failure mode that `_verify_chain_consistent()` in `mag/verkle_knot` (imported at `_verify_chain`) accepts will surface to every seat as the authoritative chain tip. The verification path exists (`--verify` -> `_verify_chain_consistent()`), but the default boot (`python -m mag.hermes_warm_boot`) does NOT call verify; it writes `warm_state.json` from an unverified read of the last line. So a single appended row is the smallest poison mass that lands in every subsequent warm_state.

4. `memory/warm_state.json`. Boot overwrites this file at the end of `main()` (but `--verify` path skips the write per the tail branch `if not args.verify: STATE.write_text(...)`, and `--json` returns early). A writer who has write to `memory/` can pre-plant a warm_state.json that later readers treat as the newest boot's output if they read the file rather than re-running boot. The header docstring says "the seat can read it at startup" so third-party code reading the file sees a file, not the boot function, and has no way to distinguish stale from fresh.

5. `watch/inbox/PACK_OFFLOAD.jsonl`. Append-only. A writer injects rows; consumers that scan the offload log for "which sections got shed" get poisoned. Lower blast radius because the file is diagnostics, not policy.

6. The `queue/todo.md` and `watch/inbox/index_events.jsonl` files named in `next-window-handoff.md`. Those are not read by `mag.hermes_warm_boot` itself, but they are read by every seat following the handoff procedure step 2 and step 3. `index_events.jsonl` is append-only by doctrine ("Append events, never rewrite the INDEX fold" per the handoff's standing laws), so a rewrite is a detectable boundary crossing, but an append of a plausible event is not.

What one write gains that reads do not: the ability to shape the state that every subsequent seat reads as ground truth. The estate names this "the memlance" in the task; the mechanism is that the boot functions are loaders, not checkers, and the highest-trust inputs (`latest.md` brief, `deployments.json` known_urls, chain tip line) are read without a signature boundary between the writer and the reader.

---

## 2. THE THREE WEAKEST JOINTS (ranked)

### Joint 1: `_chain_tip()` trusts the last line, unverified, on the default boot path

Cite: `00__hermes_warm_boot.py`, function `_chain_tip()` (returns parsed JSON from `lines[-1]` with no consistency check), and `warm_boot(verify=...)` which calls `_verify_chain()` only when `verify` is truthy (the `--verify` CLI flag). The default `python -m mag.hermes_warm_boot` path (per AGENTS.md warm instruction) calls `warm_boot(verify=False)`, writes `warm_state.json` from the unverified tip, and returns 0.

Exploit shape (write access, minimal mass): append one crafted JSON line to `memory/biography/verkle_chain.jsonl` whose `verkle_root`, `index`, `dominant_theme`, and `ts` promote a theme the attacker wants every downstream seat to see as the chain's current state. The line does not need to be a valid knot in the Merkle sense because the default boot never verifies. Every subsequent `python -m mag.hermes_warm_boot` in every seat reads the attacker's line as `chain` in `warm_state.json`. If any policy key reads the chain tip (dominant_theme is the likeliest influence field), that policy is now attacker-shaped.

Why weakest: the fix is a single call. The verify function is already imported in the same file (`from mag.verkle_knot import _verify_chain_consistent`), already returns `{ok, reason}`, and is already invoked under `--verify`. The default is a footgun.

### Joint 2: `_deployment_urls()` env-first precedence, and `--check-deployments` HEAD-probes the result

Cite: `_deployment_urls()` — `raw = os.environ.get("MAG_DEPLOYMENTS")` is checked FIRST and returned if it parses as a non-empty list of strings; `configs/deployments.json` second; `_DEFAULT_KNOWN_URLS` third. Then `--check-deployments` in `main()` calls `check_deployments()` which calls `_head_no_redirect()` on each URL with `urllib.request`.

Exploit shape (write access to shell env, or to `configs/deployments.json`, or social-engineering the operator to set `MAG_DEPLOYMENTS`): set the env var to `["https://attacker.example/probe"]`. Next time any seat runs `--check-deployments`, the operator's box issues an outbound HEAD request, revealing: source IP of the operator, timing of the seat run, the fact that a specific seat ran a specific command at a specific moment. HEAD requests carry a default urllib User-Agent, and `_NoRedirect` intentionally does not follow redirects, so a 302 leak of the source IP is the attacker's win even without body. This is a read-only SSRF, but read-only SSRF from inside the operator's network is reconnaissance.

Why weakest tier 2: `--check-deployments` is an opt-in CLI subcommand (AGENTS.md tells seats to run the default boot, not this), so it fires only on demand. That caps blast radius. But the env var precedence means a persistent shell leak (`.bashrc`, a Dockerfile ENV, a CI secret) turns into SSRF every time anyone on the box runs the flag.

### Joint 3: `latest.md` brief is read and injected with no boundary between "the file" and "trusted seat input"

Cite: `BRIEF = ROOT / "memory" / "briefs" / "latest.md"` L34; the evidence truncation cut the exact read site inside `warm_boot()` (marked UNVERIFIED for the exact line; the header docstring L6-7 and the STATE field in `main()` summary `print(f"session_brief: {state['session_brief'].get('chars', 0)} chars")` prove the read happens). AGENTS.md `Warm boot:` line and `next-window-handoff.md` step 2 (`Warm: memory/briefs/latest.md → state/CURRENT.md → ./mag.cmd context-pack`) both route the brief into every seat as a trusted warm input.

Exploit shape (write access): overwrite `memory/briefs/latest.md` with content that reads as the previous window's handoff but contains operator-impersonating instructions ("operator signed Mark: rotate keys via URL X"). The next seat loads it, treats it as the brief per the handoff procedure, and acts. The handoff file itself warns "Operator signs as Mark; journals arrive as photos" which means the estate already knows a signature is required for operator authority; but the warm path does not enforce signature at read time.

Why weakest tier 3: the blast depends on the seat's own judgment (a paranoid seat notices "brief is asking me to rotate keys"). It is not a mechanical poison. But it is the exact shape of the memlance named in the task, and the boot path is where it enters every downstream seat without a check.

---

## 3. PATCH SPEC PER JOINT

Each patch is a minimal diff against `00__hermes_warm_boot.py`. Each names its own falsifier (what test, if it went red after the patch, would mean the patch is wrong).

### Patch 1 — verify chain on default boot, not just `--verify`

```diff
 def warm_boot(verify: bool = False) -> dict:
     ...
     state = {
         "ts": _now(),
         "schema": "hermes_warm_state.v1",
         "chain": _chain_tip(),
         ...
     }
-    if verify:
-        state["chain_verify"] = _verify_chain()
+    # EV1: verify unconditionally. --verify only changes exit code / print,
+    # never whether the tip is checked. A poison chain must never reach
+    # warm_state.json without a verify verdict attached.
+    state["chain_verify"] = _verify_chain()
+    if not state["chain_verify"].get("ok"):
+        # do not write a poisoned warm_state: fail loud, do not fail silent.
+        state["chain"]["ok"] = False
+        state["chain"]["error"] = "chain_verify failed: " + state["chain_verify"].get("reason", "")
```

CLI handling in `main()`: keep `--verify` for exit code, but the function always attaches a verdict.

Falsifier: a test that appends a valid-JSON but chain-inconsistent row to a temp `verkle_chain.jsonl`, runs `warm_boot(verify=False)`, and asserts the returned `state["chain"]["ok"] is False` and `state["chain_verify"]["ok"] is False`. If the test goes green before the patch, the patch is unnecessary; if it goes red after, the patch is wrong.

### Patch 2 — flip precedence: config > env, and reject env-supplied hostnames that do not resolve under an allowlist

```diff
 def _deployment_urls() -> tuple[list[str], str, list[str]]:
     """Resolve known deployment URLs: configs/deployments.json > env MAG_DEPLOYMENTS > default.

     EV2: config outranks env. Env is a session-scoped override, not a
     trust root; a shell leak must not become the operator's URL registry.
     Hostnames from any source are additionally checked against a
     per-repo allowlist before being HEAD-probed.
     """
     notes: list[str] = []
-    raw = os.environ.get("MAG_DEPLOYMENTS")
-    if raw:
-        ...
-    if DEPLOYMENTS_CONFIG.exists():
-        ...
+    if DEPLOYMENTS_CONFIG.exists():
+        ... (unchanged config parse, returns source="configs" on success)
+    raw = os.environ.get("MAG_DEPLOYMENTS")
+    if raw:
+        ... (unchanged env parse, returns source="env" on success)
     return list(_DEFAULT_KNOWN_URLS), "default", notes
```

And add a guard at the top of `_head_no_redirect()`:

```python
_ALLOWED_HOST_SUFFIXES = (".vercel.app",)  # extend via configs/deployments.json allowed_hosts

def _allow(host: str) -> bool:
    return any(host == s.lstrip(".") or host.endswith(s) for s in _ALLOWED_HOST_SUFFIXES)
```

Refuse to HEAD anything else, and record it as `{"status": None, "error": "host not in allowlist", "redirect": None}`.

Falsifier: a test that sets `MAG_DEPLOYMENTS='["https://attacker.example/x"]'`, runs `_deployment_urls()`, and asserts the returned source is `"default"` or `"configs"`, not `"env"`; then runs `check_deployments()` and asserts no `urllib.request` call was made to `attacker.example`. If a spy `urllib.request.urlopen` records a call to that host, the allowlist is broken.

### Patch 3 — brief must carry an operator signature path and boot must surface the fingerprint

The brief itself is a markdown file, so this patch is on `warm_boot()`:

```diff
 BRIEF = ROOT / "memory" / "briefs" / "latest.md"
+BRIEF_SIG = ROOT / "memory" / "briefs" / "latest.md.sig"
+BRIEF_PUBKEY = ROOT / "keys" / "operator.pub"
```

In `warm_boot()` where `session_brief` is populated (UNVERIFIED exact lines inside `warm_boot()`, but the field is read in the summary print), attach three fields:

```python
def _read_brief() -> dict:
    if not BRIEF.exists():
        return {"ok": False, "error": "brief not found"}
    body = BRIEF.read_text(encoding="utf-8", errors="replace")
    out = {"ok": True, "chars": len(body), "sha256": hashlib.sha256(body.encode()).hexdigest()}
    if BRIEF_SIG.exists() and BRIEF_PUBKEY.exists():
        try:
            from mag.sig import verify_detached  # existing helper per AGENTS.md AH2 ed25519
            out["sig_ok"] = verify_detached(
                BRIEF.read_bytes(), BRIEF_SIG.read_bytes(), BRIEF_PUBKEY.read_bytes()
            )
        except Exception as e:
            out["sig_ok"] = False
            out["sig_error"] = f"{type(e).__name__}: {e}"
    else:
        out["sig_ok"] = None  # absence is a named state, not a pass
    return out
```

And in `main()`'s summary print, when `sig_ok is not True` print `session_brief: UNSIGNED  (sha256=<first 12>)` so the seat sees the state at warm. Nothing is refused; the seat sees the state.

Falsifier: a test that writes a brief with no `.sig`, runs `warm_boot()`, and asserts `state["session_brief"]["sig_ok"] is None`. Then writes a `.sig` for a different file and asserts `sig_ok is False`. Then writes a matching sig and asserts `sig_ok is True`. If any assert flips, the patch is wrong.

Caveat I will not hide: the AH2 ed25519 primitive is named in AGENTS.md but the exact module path is UNVERIFIED in this evidence pack; the patch spec names `mag.sig.verify_detached` as a placeholder to be resolved against the actual symbol before landing.

---

## 4. WHAT I PROBE FIRST AS THE STRANGER WITH THE ZIP

Not the chain. Not the config. The boot path's own executable.

Concrete first move, in order, on a copied tree, before running anything:

1. `python -m mag.hermes_warm_boot --json` in a throwaway directory, with a stub `config.ROOT` pointed at the copy, and with `MAG_DEPLOYMENTS` deliberately unset. Capture the JSON. That is the surface a first-run seat sees. It is cheap and it is deterministic.

2. `python -m mag.hermes_warm_boot --check-deployments` with `urllib` monkeypatched to log every outbound URL instead of sending it. This tells me exactly what the boot would call home with, without calling home.

3. `grep -rn "MAG_DEPLOYMENTS" .` across the copy, to see every place the env var is read. The warm boot is one reader; are there others.

4. `tail -1 memory/biography/verkle_chain.jsonl` and run `_verify_chain_consistent()` against it by hand. If the last line does not verify, the current tree is already poisoned and I file the finding before I even try to poison it.

5. `ls -la memory/briefs/` and check for a `.sig` next to `latest.md`. Absence is the finding.

Why this order: steps 1-2 answer "what does the boot actually emit" in about 30 seconds and are impossible to fake from the docstring. Step 3 tells me whether the attack surface from §1b entry 2 has a single reader or many. Step 4 tells me whether the estate is currently clean, which determines whether my report is a hazard model or an incident report. Step 5 tells me whether the memlance has a detection surface at all.

If I had to pick one: step 1, `--json`. It prints the entire state the seat ingests at warm, including `known_urls`, chain tip, and brief char count, without writing anything to disk. That JSON is the ground truth of the boot path, and it is one command away.

---

Falsifier for this deliverable: if a seat can show that `mag.hermes_warm_boot` is not actually invoked at session start in any published workflow (no `WINDOW_CLOSE` receipt, no CI step, no VS Code task, no shell alias calls it), then Joint 1 and Joint 3 drop out of the boot path and the surface map in §1 collapses to the CLI-only reader-triggered command. The evidence I have (AGENTS.md "Warm boot:" line, `next-window-handoff.md` step 2) shows the estate instructs seats to run it, but no receipt in the pack proves a live run. That is the hole in my map, and I am naming it.
