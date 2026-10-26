# swarm1-kimi-mag__flight_recorder (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: JSONL write in _emit() is non-atomic (no tmp+replace), violating the known wiring violation (c) that this file already carries, but this is a NEW instance of the same pattern not at the known sites | EVIDENCE: mag/flight_recorder.py:173-180 | FIX: Write to tmp file then os.rename() to target atomically
DEFECT 2: guard_endpoint() called in api_call() but load_env() keys fetched separately create TOCTOU race between guard check and actual request | EVIDENCE: mag/flight_recorder.py:285-287 vs 289-290 | FIX: Pass endpoint and allowed_hosts to record_call wrapper and validate once at call time inside the wrapped fn
DEFECT 3: _dogfood() runner() returns time.perf_counter() - t0 as raw float but show() expects latency in seconds while record_call emits milliseconds, causing unit confusion in dogfood output | EVIDENCE: mag/flight_recorder.py:335-340 vs 343-350 | FIX: Multiply runner's latency by 1000.0 to match milliseconds convention
DEAD-CODE: math module imported but only used for _pctl() which uses ceil() and could use integer arithmetic | EVIDENCE: mag/flight_recorder.py:13
ONE-SITTING FIX: Make _emit() atomic with tmp+rename pattern | EVIDENCE: mag/flight_recorder.py:173-180
