"""s2-19 round 3: final SUT checks for fake/model patch accuracy."""
import os, re

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def grep(pat, files):
    rx = re.compile(pat)
    for rel in files:
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            print("!! missing", rel)
            continue
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        print("--- %s :: /%s/ ---" % (rel, pat))
        for i, l in enumerate(lines, 1):
            if rx.search(l):
                print("%4d: %s" % (i, l[:150]))

grep(r"langchain", ["mag/desk_dialogue.py", "llm.py"])
grep(r"readlink", ["mag/catalog_scan.py"])
grep(r"def orchestrate|chat\(", ["mag/desk_orchestrator.py"])
grep(r"client|_call_model|model_fn|chat_provider|chat\(", ["mag/agent_cli.py"])
print()
print("--- tests/test_t1_steering.py: patches on ac ---")
lines = open(os.path.join(REPO, "tests/test_t1_steering.py"), encoding="utf-8").read().splitlines()
for i, l in enumerate(lines, 1):
    if "monkeypatch.setattr" in l and "ac" in l:
        print("%4d: %s" % (i, l[:150]))
