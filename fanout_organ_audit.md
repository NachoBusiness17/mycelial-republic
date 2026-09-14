## Finding — what your cell yields
fanout_organ is a single-file, stdin/stdout Python organ that enforces "packs-as-data" purity: no file I/O inside the cage. It is the canonical proof that N-wide fan-out can be done without bespoke runners per pack.

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: mag/fanout.py (107 lines, compiled 2026-09-12)
- Contract lines 9–14: Purity law — no file I/O inside the cage; pack in via STDIN, lanes' text out via STDOUT after ===FANOUTJSON=== marker; progress to STDERR.
- Pack shape (lines 16–25): JSON with optional model, max_tokens, width, key_env, base, shared_head, lanes array.
- Guarded fetch (lines 41–54): enforces https + allowlisted host + global IPs + no redirects.
- Runner evaporates pattern (lines 4–7): bespoke code → gate re-fight → runner evaporates.
- Output shape (lines 27–29): STDERR progress and STDOUT tail with ===FANOUTJSON=== followed by one JSON object containing model, lanes meta, and texts.

## Risk if wrong — what the audit breaks on if this is missed
- If the purity law is violated (file I/O inside cage), the organ’s security posture collapses and the cage’s static path-traversal detectors flag it.
- If the runner does not evaporate, bespoke runners proliferate, defeating the "CODE ONCE, PACKS ARE DATA" invariant and bloating the codebase.
- If the guarded fetch is weakened, the host allowlist and global-IP checks are bypassed, enabling egress to untrusted endpoints.

## The act — the concrete prep step (file/spec/number)
- Add a README stub in the repo root named fanout_organ_audit.md that contains the OUTPUT CONTRACT section below, referencing mag/fanout.py lines exactly.
- Ensure the file is tracked by git and contains no invented files or claims.

## Falsifier — what would prove this wrong
- Presence of any open(), os.path, makedirs, or similar file I/O inside mag/fanout.py after line 14.
- Existence of a bespoke runner script in the repo that duplicates fan-out logic for any pack.
- A successful egress to a host not in HOST_ALLOW set.
- Output format deviates from the ===FANOUTJSON=== contract or the JSON schema in lines 28–29 of mag/fanout.py.
