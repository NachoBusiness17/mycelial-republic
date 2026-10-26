"""s2-19 round 2: exact SUT call shapes for each fake + dead-patch hunt."""
import os, re

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def show(rel, a, b):
    p = os.path.join(REPO, rel)
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    print("--- %s [%d-%d] ---" % (rel, a, b))
    for i in range(a - 1, min(b, len(lines))):
        print("%4d: %s" % (i + 1, lines[i]))

def grep(pat, files, show_files=False):
    rx = re.compile(pat)
    for rel in files:
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            print("!! missing", rel)
            continue
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        hits = [(i, l) for i, l in enumerate(lines, 1) if rx.search(l)]
        if hits or show_files:
            print("--- %s :: /%s/ ---" % (rel, pat))
            for i, l in hits:
                print("%4d: %s" % (i, l[:150]))

show("mag/arena_adapter.py", 1, 40)
grep(r"\bta\b\.|SimpleRender|LLMObservation|\.reset\(|get_observation|\.step\(|\.close\(", ["mag/arena_adapter.py"])
show("mag/bones_adapter.py", 150, 168)
show("mag/desk_dialogue.py", 177, 232)
print()
grep(r"_chat_http", ["llm.py", "mag/desk_dialogue.py", "mag/desk_orchestrator.py", "mag/coding_session_loop.py", "main.py"])
grep(r"def reparse_record|st_reparse_tag|st_mode", ["mag/catalog_scan.py"])
grep(r"_OPENER", ["mag/perplexity_research.py"])
grep(r"urlopen", ["models/providers.py"])
grep(r"model\(|resp\[|resp\.get|tool_calls", ["mag/agent_cli.py"])
print()
print("--- tests/test_desk_orchestrator.py header ---")
lines = open(os.path.join(REPO, "tests/test_desk_orchestrator.py"), encoding="utf-8").read().splitlines()
for i, l in enumerate(lines, 1):
    if l.startswith(("import ", "from ")) or 25 <= i <= 45:
        print("%4d: %s" % (i, l[:140]))
