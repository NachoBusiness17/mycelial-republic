# swarm1-glm-flash-mag__desk_model_probe (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: report_path is added to the report dict only after the file is written, so the persisted JSON at desk_model_probe.json never contains its own path key | EVIDENCE: mag/desk_model_probe.py:206-223 | FIX: set `report["report_path"] = str(REPORT_PATH)` before the `REPORT_PATH.write_text` call at line 206
DEFECT 2: ensure_qwen_desk unconditionally builds the Modelfile FROM qwen2.5:3b-instruct, so with pull=False and base absent the create call fails with an opaque ollama error instead of a guard | EVIDENCE: mag/desk_model_probe.py:36-79 | FIX: return `{"ok": False, "error": "base model missing"}` when pull is False and `_has_model(base, tags)` is False (line 40)
DEFECT 3: gpu_pct is sampled after generation completes, so it reflects post-eval residency under keep_alive=2m rather than GPU share during the timed run, skewing the winner's third sort key | EVIDENCE: mag/desk_model_probe.py:88-104,131 | FIX: sample /api/ps inside _bench_model immediately before t0 and report that snapshot alongside elapsed_ms
DEAD-CODE: urllib.error imported and never referenced | EVIDENCE: mag/desk_model_probe.py:11
ONE-SITTING FIX: move the report_path assignment above the write_text so the on-disk artifact is self-describing, a 2-line edit with no behavioral risk | EVIDENCE: mag/desk_model_probe.py:205-207

Falsifier for DEFECT 1: run run_probe and read memory/working/desk_model_probe.json; if the file contains a "report_path" key, the defect claim is wrong.
