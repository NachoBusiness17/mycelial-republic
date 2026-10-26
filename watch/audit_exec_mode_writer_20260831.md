# Audit: Who wrote `tools.exec.mode` (2026-08-31 ~01:33Z)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the illegal `exec.mode` write came from an out-of-band non-gateway writer, not any logged agent session — SUPPORTED (audit log never appended, zero session hits, empty 01:18-01:33 window) · falsifier: a named logged session or migration script found that authored the write

## Verdict
**Attribution inconclusive / unresolved.** The write that added the illegal `exec.mode` to agent `main` is **not attributable to any logged agent session or audited config path**. Evidence points to an **out-of-band (non-gateway-CLI) writer** that both bypassed the `config-io` audit hook and left no session log — most plausibly a config-migration tool/script executing a pre-planned "overseer" setup.

Confidence of "no logged agent wrote it": **high**. Confidence of "external/migration tool wrote it": **moderate**.

## Evidence (path, timestamp, quote)

1. **`logs/config-audit.jsonl`** — last audited write **2026-08-30T03:58:44** (`event":"config.write"`, argv `config set agents.defaults.memorySearch.provider none`). File mtime **2026-08-30 23:09:45** — **never appended during/after the 01:33 incident**. The illegal write was never recorded by the audit instrumentation.
   `{"ts":"2026-08-30T03:58:44.077Z","event":"config.write",...argv:["...","config","set","agents.defaults.memorySearch.provider","none"]}`

2. **`logs/stability/*`** — 7 failures 01:33:17→01:34:07, all with the exact error:
   `"Invalid config at /root/.openclaw/openclaw.json: agents.list.0.tools.exec.mode: tools.exec.mode cannot be combined with tools.exec.security or tools.exec.ask"` (e.g. `openclaw-stability-2026-08-31T01-33-17-057Z`, `crash_loop_breaker 01:33:41` = "3 unclean boot(s) within 300000ms").

3. **`agents/main/sessions/*.jsonl` (01:00–01:18)** — all session files active before the crash were grepped; **`exec.mode` count = 0** in every one (raw + trajectory). The last session touching config was `7dbfa286` (01:13) doing `config set gateway.bind lan` / `config set gateway.tailscale.mode serve` — unrelated, non-exec keys. **No session ran 01:18–01:33** (empty window). Only `4ec2740f` ends 01:18:58.

4. **`openclaw.json.pre-overseer-20260831T020000Z`** — mtime **01:32:35** (~40s before first failure), snapshot of config with **agents as object (only `defaults`, no `agents.list`)** and **no `exec` block** — a pre-migration schema. Its existence/name ("pre-overseer") indicates a tool snapshotted config immediately before applying an "overseer" agent setup that introduced `exec.security`+`exec.ask` and (illegally) `exec.mode`.

5. **`openclaw.json`/`openclaw.json.last-good`** — healed 03:42, byte-identical, `agents.list[0].tools.exec = {host,security:"full",ask:"on-miss",timeoutSec:300}` (no `mode`). `.bak` (03:58, 8411B) predates incident.

## Explicit unknowns
- **Identified writer**: not found. No session authored the write; no shell/proc audit trails beyond `config-audit.jsonl` (which lacks it), `commands.log` (no entry 01:2x–01:4x), and `room.jsonl` (no seat events during 01:2x–01:33 — gateway was in crash loop).
- **Exact command/mechanism**: unknown — direct file edit, migration script, or `openclaw config` run with the audit hook detached are all possible.
- **The mechanism that created `pre-overseer` snapshot** (script name, invocation) is not recorded in available logs.

## Recommendation
Instrument `config-audit` on raw `openclaw.json` inode changes (not just CLI `config`), and correlate the `pre-overseer` snapshot creator to a named script before the next "overseer"-style apply.
