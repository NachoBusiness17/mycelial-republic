# swarm1-deepseek-mag__gpu_ghost (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: afk_train() appends training rows with plain open("a") to a shared jsonl surface, the exact non-atomic write the contract forbade, and only this one of the three jsonl sites is unguarded here | EVIDENCE: mag/gpu_ghost.py:266-269 | FIX: write rows to a tmp file then Path.replace() onto memory/pile/training_rows.jsonl.
DEFECT 2: _ollama_generate reads response data with no size cap and json.loads on unbounded body, so a runaway local model response can exhaust memory | EVIDENCE: mag/gpu_ghost.py:229-231 | FIX: cap r.read() bytes (e.g. read(1<<20)) before json.loads.
DEFECT 3: partition() dispatches local batch even when gpu.get("free") is None (telemetry unavailable), since None is falsy only checked via .get("free") truthiness, so unreachable-GPU still enqueues | EVIDENCE: mag/gpu_ghost.py:186 | FIX: gate on gpu.get("free") is True, not truthy, or log a skipped reason when free is None.
DEAD-CODE: _seed_prompts third-and-later seeds never survive slicing to n<6 but list is hardcoded to 6 so the [:n] slice is dead for default callers | EVIDENCE: mag/gpu_ghost.py:248-257
ONE-SITTING FIX: make the training_rows.jsonl append atomic via tmp+replace to satisfy the estate-wide write law | EVIDENCE: mag/gpu_ghost.py:266-269

FALSIFIER for DEFECT 1: if memory/pile/training_rows.jsonl is written only by a single serialized writer process with no concurrent readers, the atomicity harm is unproven; grep writers to confirm concurrent append.
