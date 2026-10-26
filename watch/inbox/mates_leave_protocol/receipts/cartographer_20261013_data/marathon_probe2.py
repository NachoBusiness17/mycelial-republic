import json, sys, io
from datetime import datetime, timezone

SRC = r"corpus\oral_history\marathon_body\marathon_25fbcaab_20260815_20260820.jsonl"

def ts_str(ms):
    if not ms:
        return ""
    return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def probe2():
    with open(SRC, "r", encoding="utf-8", errors="replace") as f:
        header = json.loads(f.readline())
    v = header["v"]
    reqs = v.get("requests", [])
    print("creationDate:", ts_str(v.get("creationDate")))
    r0 = reqs[0]
    msg = r0.get("message")
    print("message dict keys:", sorted(msg.keys()))
    for k in msg:
        val = msg[k]
        print("  %s: %s" % (k, type(val).__name__))
        if isinstance(val, list) and val:
            p0 = val[0]
            if isinstance(p0, dict):
                print("    part0 keys:", sorted(p0.keys()))
                t = p0.get("text") or p0.get("value") or p0.get("content") or ""
                print("    part0 head:", str(t)[:250].replace("\n", " | "))
    resp = r0.get("response")
    print("response type:", type(resp).__name__)
    if isinstance(resp, dict):
        print("response keys:", sorted(resp.keys()))
        rp = resp.get("response")
        if isinstance(rp, list):
            kinds = {}
            for p in rp:
                k = p.get("kind") if isinstance(p, dict) else type(p).__name__
                kinds[k] = kinds.get(k, 0) + 1
            print("response part kinds:", kinds)
        for p in rp[:3]:
            if isinstance(p, dict):
                print("  part keys:", sorted(p.keys()))
                if p.get("kind") == "markdownContent":
                    print("  md head:", str(p.get("content", {}).get("value", ""))[:200].replace("\n", " | "))
        tc = resp.get("tool_calls")
        print("tool_calls:", type(tc).__name__, (len(tc) if isinstance(tc, list) else ""))
        if isinstance(tc, list) and tc:
            print("toolcall keys:", sorted(tc[0].keys()))
            print("toolcall sample:", json.dumps(tc[0])[:600])
            tc0p = tc[0].get("parameters")
            print("parameters type:", type(tc0p).__name__)
            if isinstance(tc0p, dict):
                print("parameters keys:", sorted(tc0p.keys()))
            tc0r = tc[0].get("result")
            print("result type:", type(tc0r).__name__)
            if isinstance(tc0r, dict):
                print("result keys:", sorted(tc0r.keys()))
    print("modelId:", r0.get("modelId"))
    print("request ts:", ts_str(r0.get("timestamp")), "response ts:", ts_str(r0.get("responseTimestamp")))
    # kind-2 append count check
    with open(SRC, "r", encoding="utf-8", errors="replace") as f:
        n_appended = 0
        appended_sample_keys = None
        for line in f:
            if len(line) < 200:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("kind") == 2 and rec.get("k") == ["requests"]:
                n_appended += 1
                if appended_sample_keys is None:
                    appended_sample_keys = sorted(rec["v"].keys())
        print("kind-2 request appends:", n_appended)
        print("append keys:", appended_sample_keys)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    probe2()
