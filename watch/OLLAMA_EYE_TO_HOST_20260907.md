# OLLAMA EYE → HOST MIGRATION (2026-09-07)

**Verdict:** EXECUTED + VERIFIED end-to-end. The eye now lives on the host, survives
Docker Desktop restarts, and every consumer reaches it. Container retired behind a
compose profile, not deleted.

## The question the operator asked

"Why does everyone keep losing ollama? I put it in Docker as a test — stateless,
off the desktop — and it worked, but it keeps dying."

## Root cause (read from bytes, not pattern)

`docker inspect mag-ollama`: **RestartPolicy: no**, ExitCode 0, OOM false.
Deaths: Sep-4 23:33Z, Sep-6 14:14:14Z — both clean exits. The container had no
restart policy, so every Docker Desktop restart/update (VM lifecycle, not ollama's
own failure) swept it away and nothing revived it. The rest of the fleet survived
the same events because those services carry `restart: unless-stopped`. The eye was
the only orphan in the family.

The "stateless test" was never stateless: the compose bind-mounted the HOST model
store (`C:/Users/foste/.ollama/models`, ~39GB) — comment on record: "Reuse the
existing native ollama model store instead of re-downloading." The models always
belonged to the desktop; the container was a fragile wrapper around the operator's
own files.

## Lineage (not a new idea)

- 2026-09-06 audit (project-ollama-native-drift): premise audited dead — k8s has
  ZERO ollama refs; **container retirement = permanent-until-k8s-consumer; host
  ollama = the eye; Startup Ollama.lnk = the sanctioned front door.**
- Operator feedback row (operator-state-is-a-row): the seat once SHRUGGED at the
  operator's "ollama on the desktop" — his machine-state reports are rows to read.
  Today's migration executes the row the seat should have read then.

## What changed (backups: *.bak-eyemig)

1. `docker-compose.yml`:
   - `ollama` service → `profiles: ["retired-eye"]` + retirement note. Resurrect:
     `docker compose --profile retired-eye up -d ollama`.
   - mag: `OLLAMA_HOST` → `http://host.docker.internal:11434/v1`; dropped
     `depends_on: ollama`.
   - worker: same endpoint swap; dropped `depends_on: ollama`.
   - openclaw: `OLLAMA_HOST` → `http://host.docker.internal:11434`.
   - tailscale-openclaw sidecar: + `extra_hosts: host.docker.internal:host-gateway`
     (openclaw shares its netns).
2. `config.py` `ollama_base()` no-env default → `http://127.0.0.1:11434` (host
   loopback). Cage services always set OLLAMA_HOST explicitly, so the default only
   serves bare-metal callers.
3. Runtime: `mag-ollama` stopped (state + named volume `mag_ollama_data` preserved);
   host Ollama app started (`Ollama.lnk` already in Startup = survives reboot).

## Receipts (all read from probes, 2026-09-07 ~09:3xZ)

- Host API: `/api/version` = 0.32.7; `/api/tags` = **13 models** (incl. qwen2.5vl:3b
  vision, maze-keeper, gemma4 family, nomic-embed).
- Real inference: gemma:2b generate → response OK, eval 0.04s.
- Cage → host door: sovereign OK (13 models), worker OK (13), openclaw OK (13,
  env confirmed `http://host.docker.internal:11434`).
- Census after recreation: 6/6 up healthy (F1 intact, control-plane still out by
  design). Dashboard `/api/home` 200 in 0.33s. MCP door 8001 = 401 (auth wall up).
- `python -m py_compile config.py` PASS.

## Law citations (LAW-13 teeth)

- **Loopback-only:** upheld — host ollama binds 127.0.0.1:11434 only; the cage
  reaches it through Docker Desktop's host.docker.internal proxy (the same proven
  path Bionic/LM Studio already rode).
- **Not a scheduled task:** `Ollama.lnk` in the Startup folder is the sanctioned
  front door per the 09-06 audit — an on-record exemption, cited here.
- **Fleet services in Docker:** the fleet stays in Docker; the eye is now a host
  service BY AUDIT EXEMPTION (09-06, operator's own machine-state row), not by
  seat improvisation.

## Falsifier

If the eye dies again, the migration is DISPUTED and diagnosis reopens — but the
failure surface changed shape: the eye no longer rides the Docker VM lifecycle, so
a Docker Desktop restart is no longer a death sentence. Next natural test: the next
operator reboot (eye should come back on its own via Startup lnk while the fleet
waits for Docker).

## Dogfood pass (2026-09-07 ~09:5xZ) — the eye driven, not just probed

Every real consumption path exercised post-migration, receipts from runs:

1. **L0 probe** (fleet's own instrument, `models/probe.py`): `ok: true`, "PONG",
   local chat roundtrip through `llm.py`.
2. **Multi-smoke** (`models/multi_smoke.py`): PASS `dual_local: true` — clerk
   gemma:2b routes, worker qwen2.5-coder:7b writes a brief, critic qwen-desk
   critiques. Receipt: `logs/multi_smoke_latest.json`.
3. **Vision reads fleet art**: qwen2.5vl:3b on `dashboard/static/art/blind_gate.png`
   → "A person holding a lantern stands before an enormous clock that serves as a
   door to golden light" (28.2s incl. cold load). The blind gate, seen.
4. **Cage-side chat through the fleet's own code**: `docker exec mag-sovereign` →
   `config.ollama_base()` resolves `http://host.docker.internal:11434` → `llm.chat`
   round-trips (usage.jsonl row). The model's literal refusal to claim sight is the
   model being honest; the PATH is the thing proven.
5. **Heavy weights**: maze-keeper:latest (19GB) cold-loaded in 44.7s, spoke one
   file-fed in-character line off `state/keeper_world/world.json`: "Files are the
   body. The dream came first, shaping paths unseen." (Unprompted, it quoted the
   fleet's own law.)
6. **Usage ledger**: rows landing in `logs/usage.jsonl` (ok: true) at each call.

## Residual debt

- `mag_ollama_data` named volume kept (sacred cow; may hold pre-bind junk — never
  audited). Prune only with operator GO.
- If `OLLAMA_ORIGINS` matters for any browser-side caller later, host env can set it;
  no consumer needed it today.
