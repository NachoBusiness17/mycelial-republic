## Finding — what your cell yields
hermes_organs (bay_organs.py) is **Supported**: the organ-table CLI delivers a coherent, win32-atomic claim organ, writer locks, and atomic state writes that downstream organs (e.g., window_throttle.py) depend on. The repo shape shows a single, focused implementation with measured win32 probes and a documented CAS discipline (temp-write + os.rename; FileExistsError = CAS).

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: mag/bay_organs.py (14,336 B, 339 lines) — stdlib-only, $0 runtime.
- Core contract: atomic claim via temp-write + os.rename (win32 FileExistsError = CAS); token-checked _tomb_move_if_same stale takeover; OpenProcess pid probe measured on this host (win32, Python 3.11.15).
- Writer locks: {pid, seat, ts} JSON lockfiles; atomic overwrite via os.replace; legacy int-pid locks still parse.
- Atomic state writes: temp-write + os.replace for in-place state/lock files.
- Usage evidence: downstream organ mag/window_throttle.py imports pid_alive and CAS discipline from bay_organs; builder trail documents the adoption and a lease-law fix derived from bay_organs’ discipline (watch/SELF_STEAL_GROK_ORPHANS_20260904.md, builder trail rows 3–8).
- INBOX law enforcement: structural via pointers and capability-checked inboxes (LAW-031, LAW-046 in queue/lanes/law_lattice.json).
- Zombie-cron falsifiers: documented in builder trails and law_lattice.json entries (scope: claim leases; enforcement: structural; consumer: bay_organs.py, window_throttle.py; disposition: FOLDED after fixes).

## Risk if wrong — what the audit breaks on if this is missed
- **False positive**: claiming the organ is “merely plumbing” and not a correctness-critical path. The audit would miss that the CAS discipline and pid probe are measured on THIS host and that downstream organs depend on the exact semantics exported by bay_organs.py. Missing this risks mis-scoping the organ’s correctness envelope.
- **False negative**: not recognizing that the organ’s atomicity guarantees (CAS via FileExistsError, token-checked tomb-move) are the foundation for the fleet’s queue discipline and window throttling, which in turn underpin the INBOX law’s structural enforcement.

## The act — the concrete prep step (file/spec/number)
Create a one-page audit-ready spec at docs/audit/hermes_organs.md with:
- Purpose and contract (three organs, stdlib-only, $0 runtime).
- CAS discipline (temp-write + os.rename; win32 FileExistsError = CAS; token-checked _tomb_move_if_same).
- Measured win32 probe reference (ctypes OpenProcess + GetExitCodeProcess; STILL_ACTIVE = 259).
- Writer lock schema ({pid, seat, ts}) and atomic overwrite via os.replace.
- Downstream dependency map (window_throttle.py, race_harness.py) and the lease-law fix lineage.
- INBOX law linkage (LAW-031, LAW-046) and capability-checked inboxes.
- Zombie-cron falsifiers summary (builder trail rows 3–8; law_lattice.json entries 109–123).

File path: docs/audit/hermes_organs.md
Size target: ≤ 800 words; include code blocks for the CAS and pid probe snippets.

## Falsifier — what would prove this wrong
- A measured win32 probe showing os.kill(pid, 0) works on this host (it does not; probe is ctypes-based).
- Evidence that downstream organs do not use bay_organs primitives (they do: window_throttle.py imports pid_alive and CAS discipline).
- A live claim file that violates the token-checked tomb-move discipline (no such violation exists in the repo).
