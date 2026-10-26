"""Draw the verification sample from watch/LIBRARY/catalog.jsonl and print evidence (masked).
usage: python _verify_sample.py draw   -> writes verify_sample.json + prints evidence
       python _verify_sample.py mark verdicts.json  -> sets verified true/false on cards"""
import json, random, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import inbox_librarian as L
CAT = L.CATALOG
cards = [json.loads(x) for x in CAT.read_text(encoding="utf-8").splitlines() if x.strip()]
if sys.argv[1] == "draw":
    rnd = random.Random(20261017)
    def readable(c):
        name = Path(c["path"]).name
        return not L.is_sensitive(c["path"], name) and Path(name).suffix.lower() in L.TEXT_EXT and c["size"] > 0
    mf = [c for c in cards if c["tier"] == "model" and readable(c)]
    seen, mfold = set(), []
    pool = [c for c in cards if c["tier"] == "model-folder" and readable(c)]
    rnd.shuffle(pool)
    for c in pool:
        top = c["path"].split("\\")[0]
        if top not in seen:
            seen.add(top); mfold.append(c)
    rules = [c for c in cards if c["tier"] == "rule" and c["rule"] != "age>30d" and readable(c)]
    samp = rnd.sample(mf, min(30, len(mf))) + mfold[:10] + rnd.sample(rules, 20)
    Path(L.LIB / "verify_sample.json").write_text(json.dumps([c["path"] for c in samp], indent=0), encoding="utf-8")
    for i, c in enumerate(samp):
        print(f"\n##### {i} [{c['tier']}] shelf={c['shelf']} {c.get('rule') or c.get('confidence')} :: {c['path']}")
        print(f"summary: {c.get('summary')}")
        txt = L.head(L.INBOX / c["path"], 60, 2600)
        lines = [l[:140] for l in txt.splitlines() if l.strip()][:28]
        print("\n".join(lines))
elif sys.argv[1] == "mark":
    v = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    for c in cards:
        if c["path"] in v:
            c["verified"] = bool(v[c["path"]])
    tmp = CAT.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cards), encoding="utf-8")
    tmp.replace(CAT)
    print("marked", sum(1 for c in cards if c.get("verified") is not None))
