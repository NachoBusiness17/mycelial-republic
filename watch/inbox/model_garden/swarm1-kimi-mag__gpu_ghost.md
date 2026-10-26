# swarm1-kimi-mag__gpu_ghost (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: TRAINING_ROWS.JSONL append is non-atomic (no tmp+replace) | EVIDENCE: mag/gpu_ghost.py:277-279 | FIX: write to temp file then atomic rename to target
DEFECT 2: _ollama_generate and _ollama_models use urllib without User-Agent header | EVIDENCE: mag/gpu_ghost.py:218-223,230-234 | FIX: add headers={"Content-Type": "application/json", "User-Agent": "Mag/1.0"} to both Request calls
DEFECT 3: afk_train fires LLM calls without importing mag.inference_budget | EVIDENCE: mag/gpu_ghost.py:247-260 | FIX: import mag.inference_budget and check budget before calling _ollama_generate
DEAD-CODE: shutil imported twice (line 4 and line 82) | EVIDENCE: mag/gpu_ghost.py:82 | FIX: remove duplicate import inside _nvidia_smi
ONE-SITTING FIX: make TRAINING_ROWS.jsonl write atomic with tmp+replace pattern | EVIDENCE: mag/gpu_ghost.py:277-279
