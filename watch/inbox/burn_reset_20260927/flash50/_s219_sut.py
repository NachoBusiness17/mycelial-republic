"""s2-19: SUT-side grep - what the real code calls on each faked interface."""
import os, re

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def grep(rel, patterns, ctx=0):
    p = os.path.join(REPO, rel)
    if not os.path.exists(p):
        print("!! missing file", rel)
        return
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    print("--- %s ---" % rel)
    for i, l in enumerate(lines, 1):
        for pat in patterns:
            if re.search(pat, l):
                print("%4d: %s" % (i, l[:150]))
                break

def header(rel):
    p = os.path.join(REPO, rel)
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    print("--- imports of %s ---" % rel)
    for i, l in enumerate(lines, 1):
        if l.startswith("import ") or l.startswith("from "):
            print("%4d: %s" % (i, l[:120]))

header("tests/test_game_dm.py")
header("tests/test_t1_steering.py")
header("tests/test_zai_backoff_floor.py")
header("tests/test_perplexity_research.py")
header("tests/test_catalog_scan_junctions.py")
header("tests/test_desk_dialogue.py")
header("tests/test_arena_adapter.py")

grep("mag/agent_arena.py", [r"\bta\.", "SimpleRenderWrapper", "LLMObservationWrapper",
                            r"\.reset\(", "get_observation", r"\.step\(", r"\.close\("])
grep("mag/bones_adapter.py", [r"send_message\("])
grep("mag/desk_dialogue.py", [r"def _invoke_local_llm", "_chat_http"])
grep("mag/lifecycle.py", [r"create_connection"])
grep("mag/process_supervisor.py", [r"\btime\."])
grep("mag/orchestrator.py", [r"Popen", r"\.pid\b", r"poll\("])
grep("mag/unsloth_seat.py", [r"Popen", r"\.pid\b"])
grep("mag/game_dm.py", [r"set_state", r"_world"])
grep("mag/operator_clerk.py", [r"model\(", r"_STEER_QUEUE", r"\bmodel\b"], 0)
