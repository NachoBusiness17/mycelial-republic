# GEMINI WARM PACK - the launcher that makes the web seat launch aware (2026-10-16)

Classification: RECEIPT (tool landed + graded an external draft)
Producer: zcode-seat-20261016
Deliverable: `scripts/gemini_warm_pack.ps1` - one command refreshes the verkle
tip (`mag.hermes_warm_boot` -> memory/warm_state.json), extracts the newest
SOAK_BEACON Position section, stamps the fixed estate-law block, puts the
paste-ready pack on the clipboard. Rehearsed twice 2026-10-16/17 (stdout path
and clipboard path both verified: pack present, 2,226 chars, tip index 12072).

## Why it exists

Operator: "it isn't loading the verkle i need to have tis shit just launch and
be aware." The warm rib (claritas face + estate laws) carries law but no chain
tip or live state, so the Gemini desktop seat launched cold. The web seat
cannot mount host bytes - it can only receive pasted text - so awareness is
composed HOST-SIDE and pasted in. The launch-receipt clause (first reply
recites index + verkle_root prefix) makes "did it load" verifiable per session.

## The Gemini-notebook draft, graded (Launch-LatestVerkle.ps1)

Its measurement discipline is real (instrument/moment/assumptions, falsifier
section, honest "host bytes UNVERIFIED" admission, secret-exclusion instinct)
and its core verdict is correct in spirit: the notebook cannot load verkle
bytes; a host bootstrap must compose them. But the bootstrap it returned is
scaffolded against a repo that does not exist. Fabrications, verified against
bytes 2026-10-16:

1. `python -m local_sovereign_agent` - no such module; real entrypoints are
   `mag.cmd` / `.venv\Scripts\python.exe main.py <cmd>` / `python -m mag.hermes_warm_boot`.
2. `pyproject.toml` / `Cargo.toml` runtime detection - neither exists; its own
   script would throw ESTATE_FAULT on this machine every run.
3. `--boot-source "mag" --verkle-state ... --no-secrets` - zero hits in main.py
   or mag/; invented flags.
4. `MAG_EXCLUDE_SECRETS` / `MAG_VERKLE_STATE_PATH` / `MAG_VERKLE_SHA256` - zero
   hits repo-wide; invented env vars.
5. watch/ glob for "verkle artifacts" - watch/ holds no chain state (matches
   are prose receipts: AUDIT_C_VERKLE_20260901.md, grave exports); the
   `.json` extension clause would crown an arbitrary receipt file as "the
   verkle state" by mtime. The tip lives in the verkle chain, surfaced only
   through `mag.hermes_warm_boot` -> memory/warm_state.json.
6. The "CAGE ROW 2026-10-16T20:00:09Z" anchor exists in the repo only as
   day-ledger/feed pheromone lines (attic/kill_list, memory/feed) - not a
   boot anchor; it anchored the manifest to a pasted snippet.

Verdict per the sensing law: banked as findings, never run as-is. The landed
launcher keeps its three good instincts (host-side composition, secret
exclusion, falsifier) and replaces every fabricated mechanism: secret
exclusion is BY CONSTRUCTION (the script reads exactly two known paths, globs
nothing), and the tip is read from the sanctioned writer's output, not
discovered by pattern.

## Use

```text
powershell -ExecutionPolicy Bypass -File scripts\gemini_warm_pack.ps1
```

Pack lands on the clipboard; paste as the FIRST message into the Gemini
session; expect the launch receipt (chain tip recited) before any ask.
