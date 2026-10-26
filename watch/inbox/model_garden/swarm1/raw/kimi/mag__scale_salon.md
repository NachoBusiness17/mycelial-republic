# swarm1-kimi-mag__scale_salon (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: TOCTOU race in _guard: socket.getaddrinfo resolves after allowlist check, allowing DNS rebinding attacks | EVIDENCE: mag/scale_salon.py:62-75 | FIX: Pin resolved IPs at allowlist time and cache per-process; reject any resolution that changes between check and use
DEFECT 2: raw.write_text is non-atomic: concurrent runs or crashes corrupt jsonl | EVIDENCE: mag/scale_salon.py:238 | FIX: Write to tmpfile then os.replace(raw, tmpfile)
DEFECT 3: ThreadPoolExecutor max_workers=len(jobs) unbounded: large job lists exhaust handles/threads | EVIDENCE: mag/scale_salon.py:225 | FIX: Cap max_workers at os.cpu_count()*2 or 8
DEAD-CODE: HTTP-Referer header set to invalid URI (https://local-sovereign-agent.invalid) serves no purpose | EVIDENCE: mag/scale_salon.py:156
ONE-SITTING FIX: Atomic write for raw.jsonl | EVIDENCE: mag/scale_salon.py:238
