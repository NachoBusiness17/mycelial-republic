# swarm1-glm-flash-mag__recreation_rib (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: render() crashes with an uncaught ImportError instead of returning the honest "renderer down" result, because `from mag.tool_manifest import JSON_OUT` sits outside the try block | EVIDENCE: mag/recreation_rib.py:166 | FIX: move the tool_manifest import inside the try (line 185) or wrap it in its own try with tool_names staying "tool-list-unavailable"
DEFECT 2: render() silently rebuilds a missing RIB file, so a render can succeed against a scene the operator never built or approved, breaking the no-unclaimed-artifact honesty chain | EVIDENCE: mag/recreation_rib.py:161-162 | FIX: return {"ok": False, "provenance_note": "RIB not built; run build first"} instead of calling build()
DEFECT 3: tool-name join emits the literal string "None" into the prompt when a manifest entry lacks "name", polluting the renderer's tool list | EVIDENCE: mag/recreation_rib.py:170 | FIX: `", ".join(str(t["name"]) for t in tm.get("tools", [])[:80] if t.get("name"))`
DEAD-CODE: STEAL_DIR, TRAIN_DIR, GRAPH constants are defined but never referenced anywhere in the module | EVIDENCE: mag/recreation_rib.py:49-52
ONE-SITTING FIX: move the `from mag.tool_manifest import JSON_OUT` import into the existing try block so render() degrades to a valid ok:False result rather than raising | EVIDENCE: mag/recreation_rib.py:166
Falsifier: run `python -m mag.recreation_rib render` with mag/tool_manifest.py absent; if it prints the ok:False provenance_note JSON instead of a traceback, DEFECT 1 is false.
