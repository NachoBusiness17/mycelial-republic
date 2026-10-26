# security.md - ractor lens: security (2026-10-03 grokbot-estate run)

Lens: security (lethal-trifecta frame; jacket: the gate that tests itself and
nothing else). Secret values never read or printed; no .env touched. Closed
items not re-raised (9/30 key purge, instance guard). Verdicts: TRUE / FALSE /
THEATER / UNVERIFIED.

## Findings

S1. lan.key excision. TRUE that it is out of HEAD, FALSE that it is "staged":
committed in add33ba72 (Codex, 16:42 ET) with the .gitignore block; HEAD
tracks memory/tls/lan.crt only; .gitignore:278 ignores memory/tls/*.key. The
key file still sits on disk and its blob remains in history (prior receipt
2026-10-02-dogfood-48h/break-security.md:36 also places it in
Mag-backup.git). Rotation remains owed; the committed .gitignore comment
itself says "rotate - it remains in history".

S2. xai- token in tests/test_gate_blocking_paths.py:219 and
GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md:20. THEATER as a leak finding. It is
the gate's synthetic fixture (tests file :212-216, :215 "Values are
fabricated"). Excising it would break the secret-gate blocking tests that
need a correctly shaped xai token. Real-or-not cannot be settled without an
authenticated call; none made.

S3. Port 8765 rebound to loopback. TRUE and correct in direction. LAN access
is designed to go through dashboard/lan_proxy.py forwarding
192.168.86.35:8765 to 127.0.0.1:8765 (cited by
watch/inbox/burn_reset_20260927/flash50/dashboard-census.md:26; lan_proxy.py
not read this sitting). Get-NetTCPConnection shows no listener on 8765/8001
other than 127.0.0.1, so the tablet/LAN path is down now. Scope: Listen state
on ports 8765 and 8001 only.

S4. New .gitignore patterns (*.env *.pem *.key id.json *keypair* wallet*.json
*.safetensors *.pt *.onnx attic/*.tar). TRUE, low blast radius: git ls-files
-ci shows only the two tools/pain_replication/data/*.pt files matching, and
they stay tracked as the comment says.

S5. "Suspected chain lock race between host and container writers."
Mechanism TRUE, event UNVERIFIED. mag/verkle_knot.py:150-191: the lock is
O_EXCL (atomic), but the stale-breaker reads the holder PID from the lock and
probes it with os.kill(owner, 0) (:166-171); ProcessLookupError, SystemError
and OSError all set stale=True and the lock is unlinked (:172-185). Host
(Windows) and cage (Linux) share the file through ./memory:/app/memory
(docker-compose.yml:46, 305), and a PID from one namespace means nothing in
the other, so either side can judge a live foreign lock stale. Writers in
flight today: host backfill, 3 cage janitor knots inside the backfill window,
and whole-chain amend rewrites (row 18 re-knotted at 13:55Z and 21:05Z; rows
26, 27, 1053, 3494, 4975, 5234, 5612, 7909, 7910 carry ts >= 22:20Z). No
damage found: verify_verkle_full linkage break 0, 0 index breaks, 0 duplicate
session ids (python census).

S6 (new). Unblocking the cage arms a mutating quest. mag/ghost.py:1449-1467
asks qwen2.5-coder:7b to run "python -m mag.verkle_audit --fix" and says
"This IS a mutating task". Today it dies at import; after the health fix it
runs against the shared chain. Whether run_shell survives the read-only
strip: UNVERIFIED (strip list seen only as quoted in
JANITOR_FIX_PLAN_20261003.md:30).

Tally (this lens): TRUE 3 (S1 out-of-HEAD, S3, S4), THEATER 1 (S2),
UNVERIFIED 2 (S5 event, S6).

No em-dash bytes. Filed by the security lens.
