import json, sys, io

SRC = r"corpus\oral_history\marathon_body\marathon_25fbcaab_20260815_20260820.jsonl"

def probe():
    with open(SRC, "r", encoding="utf-8", errors="replace") as f:
        header = json.loads(f.readline())
    v = header["v"]
    print("top keys:", sorted(v.keys()))
    print("version:", v.get("version"), "creationDate:", v.get("creationDate"))
    print("sessionId:", v.get("sessionId"))
    reqs = v.get("requests", [])
    print("requests in header:", len(reqs))
    r0 = reqs[0]
    print("request keys:", sorted(r0.keys()))
    msg = r0.get("message")
    print("message type:", type(msg).__name__)
    if isinstance(msg, str):
        print("message len:", len(msg))
        print("message head:", msg[:300].replace("\n", " | "))
    elif isinstance(msg, list):
        print("message parts:", len(msg))
        for p in msg[:2]:
            print("  part keys:", sorted(p.keys()) if isinstance(p, dict) else type(p).__name__)
            if isinstance(p, dict):
                t = p.get("text") or p.get("value") or ""
                print("  part head:", str(t)[:200].replace("\n", " | "))
    resp = r0.get("response")
    if isinstance(resp, dict):
        print("response keys:", sorted(resp.keys()))
        rp = resp.get("response")
        if isinstance(rp, list):
            print("response parts:", len(rp))
            kinds = {}
            for p in rp:
                k = p.get("kind") if isinstance(p, dict) else type(p).__name__
                kinds[k] = kinds.get(k, 0) + 1
            print("response part kinds:", kinds)
            tc = resp.get("tool_calls") or resp.get("toolCallResults")
            print("tool_calls:", type(tc).__name__, (len(tc) if isinstance(tc, list) else ""))
            if isinstance(tc, list) and tc:
                print("toolcall keys:", sorted(tc[0].keys()))
                print("toolcall sample:", json.dumps(tc[0])[:500])
    print("result keys:", sorted(r0.get("result", {}).keys()) if isinstance(r0.get("result"), dict) else type(r0.get("result")).__name__)
    # last request in header
    rl = reqs[-1]
    ts = [r.get("timestamp") for r in reqs if r.get("timestamp")]
    print("ts first:", min(ts), "ts last:", max(ts), "count:", len(ts))

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    probe()
