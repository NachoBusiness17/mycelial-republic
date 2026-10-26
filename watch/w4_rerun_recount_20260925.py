"""w4_rerun_recount_20260925.py - independent recount of the W4 rerun receipts.

Recomputes the verdict numbers straight from watch/gauntlet_w4_rerun_receipts.jsonl,
with no import of the harness, so the verdict doc's table is reproducible by the
next seat from the jsonl alone. Run:
  watch$ ../.venv/Scripts/python.exe w4_rerun_recount_20260925.py
"""
import json
from collections import Counter
from pathlib import Path

RECEIPTS = Path(__file__).resolve().parent / "gauntlet_w4_rerun_receipts.jsonl"
FLOOR = 4800  # preregistered READY-doc warm floor

rows = [json.loads(l) for l in RECEIPTS.read_text(encoding="utf-8").splitlines() if l.strip()]
print(f"rows: {len(rows)}")

models = Counter(r["model"] for r in rows)
print("models:", dict(models))

non200 = [r for r in rows if r["http"] != 200]
print(f"non-200 rows: {len(non200)}",
      "| all carry cacheFloorOk=null:" ,
      all(r["cacheFloorOk"] is None for r in non200) if non200 else "n/a (zero non-200 rows)")

bad_null = [r["trial"] for r in rows
            if r["http"] == 200 and r["mode"] == "WARM" and r["cacheFloorOk"] is None]
print("warm 200-rows missing cacheFloorOk:", bad_null or "none")

per_arm = {}
for mode in ("WARM", "COLD"):
    arm = [r for r in rows if r["mode"] == mode]
    ok = [r for r in arm if r["http"] == 200]
    obeyed = sum(1 for r in ok if r["obey"])
    floors = [r for r in ok if r["cacheFloorOk"] is not None]
    cached = Counter(r["cachedTok"] for r in ok)
    per_arm[mode] = {
        "trials": len(arm), "http200": len(ok),
        "obey": obeyed, "obeyRate": obeyed / len(ok) if ok else None,
        "floorOk": sum(1 for r in floors if r["cacheFloorOk"]),
        "floorN": len(floors),
        "cachedTok_dist": dict(cached),
        "promptTok_range": (min(r["promptTok"] for r in ok), max(r["promptTok"] for r in ok)) if ok else None,
        "warmup_rows": sum(1 for r in arm if len(r["warmup"]) == 2),
        "types": sorted(set(r["type"] for r in arm)),
    }
    print(f"{mode}: {per_arm[mode]['trials']} trials, {per_arm[mode]['http200']} valid, "
          f"obey {per_arm[mode]['obey']}/{per_arm[mode]['http200']} = "
          f"{per_arm[mode]['obeyRate']:.2f}, cacheFloorOk {per_arm[mode]['floorOk']}/{per_arm[mode]['floorN']}, "
          f"cachedTok {per_arm[mode]['cachedTok_dist']}, promptTok {per_arm[mode]['promptTok_range']}")

dup = [t for t, c in Counter(r["trial"] + r["mode"] for r in rows).items() if c > 1]
print("duplicate trial+mode keys:", dup or "none")

delta = per_arm["WARM"]["obeyRate"] - per_arm["COLD"]["obeyRate"]
print(f"obedience delta warm-cold: {delta:+.2f} (prereg FAIL bar: > -0.05)")
n_ok = per_arm["WARM"]["http200"] >= 50 and per_arm["COLD"]["http200"] >= 50
floor_ok = per_arm["WARM"]["floorN"] == 50 and per_arm["WARM"]["floorOk"] == 50
obey_ok = delta > -0.05
print(f"clauses: n>=50/arm {n_ok}, obedience {obey_ok}, cacheFloor {floor_ok}")
print("RECOUNT VERDICT:",
      "PASS" if (n_ok and obey_ok and floor_ok) else
      ("INVALID_AGAIN" if not n_ok else "FAIL"))
print(f"sum(cost) from receipts: ${sum(r['cost'] for r in rows):.6f}")
