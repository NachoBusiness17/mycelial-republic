import json, sys, io, collections

SRC = r"corpus\oral_history\marathon_body\marathon_25fbcaab_20260815_20260820.jsonl"

def resp_parts(resp):
    if resp is None:
        return []
    if isinstance(resp, list):
        return resp
    if isinstance(resp, dict):
        rp = resp.get("response")
        return rp if isinstance(rp, list) else []
    return []

def main():
    reqs = []
    with open(SRC, "r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f):
            if line_no == 0:
                header = json.loads(line)
                reqs = header["v"].get("requests", [])
                continue
            if len(line) < 40:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("kind") == 2 and rec.get("k") == ["requests"]:
                v = rec["v"]
                if isinstance(v, list):
                    reqs.extend(v)
    kinds = collections.Counter()
    sample = {}
    for r in reqs:
        for p in resp_parts(r.get("response")):
            if not isinstance(p, dict):
                kinds[type(p).__name__] += 1
                continue
            k = p.get("kind", "?")
            kinds[k] += 1
            if k not in sample:
                sample[k] = json.dumps(p)[:700]
    print("part kinds:", dict(kinds.most_common()))
    for k, s in sample.items():
        print("---", k, "---")
        print(s)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
