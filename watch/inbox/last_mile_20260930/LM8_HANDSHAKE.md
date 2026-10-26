# LM8 — sovereign_handshake: cold-join continuity proof (2026-09-30)

Seat: builder lane, file ownership `mag/sovereign_handshake.py` (run + minimal
fixes) + this receipt.

## What the module is

The peer-web connection layer (advertise / discover / handshake / web /
connect), schema `sovereign_handshake.v1`. Grounded in
`memory/connect/peers.jsonl` + `links.jsonl`, reusing `republic_ambassador`
and `swarm_surface.route_novel`. Deterministic, $0, no network.

## The real test: does it pin pre-rewrite hashes?

**No.** Despite the name "handshake", this is not a chain-tip / ledger
module. Its only hash surfaces (verified by reading every `hashlib` use in
the file) are:

- `_anchor`: `sha256("sovereign::{system}")[:16]` over a self-chosen system
  name (e.g. `grok`) — names, not history;
- `link_id`: `sha256` over the ordered anchor pair — same names again.

Nothing reads ledger, git, verkle, or chain state, so today's history rewrite
(changing all post-09-14 hashes) has no surface to break here. Both
dependencies that DO read estate state ran clean against current bytes:
`republic_ambassador.learn()` returned the embassy row, and
`swarm_surface.route_novel` deduped (`deduped: true`, anchor
`f828bcf0150aca12`) against existing swarm state.

## Run evidence (all exit 0, `.venv/Scripts/python.exe`)

| Command | Result | Durable write |
|---|---|---|
| `status` | contract + doctrine echoed | none |
| `discover` | n_peers 2 (1 roster peer `grok` + 1 embassy summary row) | none |
| `web` | 1 peer, 1 link (republic<->grok), mesh | none |
| `advertise --system grok` | `deduped: true` | none (peers.jsonl still 1 line) |
| `handshake --a republic --b grok` | `deduped: true` | none (links.jsonl still 1 line) |
| `connect` | route ok, `deduped: true` | none (existing swarm anchor) |

Dedupe paths proven by byte counts before/after: `peers.jsonl` 1 line,
`links.jsonl` 1 line, both unchanged after the full sweep.

## Verdict: ALIVE

No code changes needed; no fixes landed. mtime refreshed 2026-09-30 14:17
EDT (was 2026-08-12) as the exercise stamp; `git status` clean for the file.

## Observations filed, not fixed (minimal-fix discipline)

1. **discover() count quirk (cosmetic):** the embassy summary row
   (`{"source": "embassy", ...}`) is appended to `peers`, so `n_peers`
   counts summary rows as peers (2 reported for 1 standing system). The
   `source` field discloses it; left as designed.
2. **advertise() dedupe echo:** on a dedupe the returned `peer` rec is built
   from the NEW call's defaults (fresh ts, default values) rather than the
   stored record. Disk is untouched and `deduped: true` discloses, but the
   echo can mislead a caller into thinking the claim updated. Not a
   continuity break; noting for any future spec owner.
3. **Line-ending finding (repo-wide, not this module):** the worktree file
   was CRLF vs index LF — `autocrlf=false`, no gitattributes, and 717 of
   mag/'s tracked files read `w/crlf` (313 `w/lf`, 49 mixed), so this is a
   latent repo-wide condition. The mtime `touch` broke this file's stat
   cache and surfaced it as a phantom ` M` (245x245 whole-file diff that
   `git diff --ignore-cr-at-eol` shows empty). Restored via
   `git checkout -- mag/sovereign_handshake.py` (byte-identical to index,
   LF, mtime survives the rewrite, status clean again). The repo-wide
   CRLF/LF split is left for an operator call, not patched file-by-file.

## Verdict line

`mag/sovereign_handshake.py`: **ALIVE** — ran end-to-end, pins no history
hashes, continuity intact through the 09-30 rewrite; zero code fixes; mtime
refreshed; receipt filed.
