"""deep-tensor-receipts probe (READ-ONLY): measure how receipt relationships
are actually carried in the estate today, across the three real carriers:
  1. memory/burns/LEDGER.jsonl - flat rows, relations implied by repeated slugs
  2. watch/GROUNDING_WAVE.jsonl - act rows (witness/void/contest) = real edges
  3. watch/inbox/burn_reset_20260927/queue/*.md - relations encoded in PROSE
No writes anywhere; imports mag.grounding_wave for its own admission view.
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))


def jrows(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if ln:
            out.append(json.loads(ln))
    return out


print("== 1. burns LEDGER (flat rows) ==")
rows = jrows(ROOT / "memory" / "burns" / "LEDGER.jsonl")
slugs = Counter(r.get("slug", "") for r in rows)
print(f"rows={len(rows)} unique_slugs={len(slugs)}")
reps = [(s, c) for s, c in slugs.most_common() if c > 1][:6]
for s, c in reps:
    ts = [r["ts"][:10] for r in rows if r.get("slug") == s]
    print(f"  slug {s!r}: {c} rows, {ts[0]} .. {ts[-1]}  (re-supersession, prose-only)")

print()
print("== 2. grounding wave (act rows are real edges) ==")
gw = jrows(ROOT / "watch" / "GROUNDING_WAVE.jsonl")
kinds = Counter(r.get("kind", "claim") for r in gw)
print(f"rows={len(gw)} kinds={dict(kinds)}")
edges = Counter()
unresolved = []
for r in gw:
    k = r.get("kind")
    if k == "witness":
        edges["WITNESSES (signs->hash)"] += 1
        tgt = r.get("signs")
    elif k == "void":
        edges["VOIDS (voids->hash)"] += 1
        tgt = r.get("voids")
    elif k == "contest":
        edges["CONTESTS (contests->hash)"] += 1
        tgt = r.get("contests")
    else:
        continue
    if tgt and not any(x.get("hash") == tgt for x in gw) and \
            not re.fullmatch(r"line:\d+", str(tgt) or ""):
        unresolved.append((k, str(tgt)[:12]))
print(f"directed act-edges={sum(edges.values())} {dict(edges)}")
print(f"edge targets resolving to no row hash (line-anchors excepted): "
      f"{len(unresolved)} e.g. {unresolved[:3]}")

from mag import grounding_wave as gwave  # noqa: E402
adm = gwave._admission(gwave._rows())
st = Counter(adm["statuses"].values())
print(f"estate admission view: {dict(st)} propagation={len(adm['propagation'])} "
      f"pending_voids={len(adm['pending_voids'])} effective_voids={len(adm['effective_voids'])}")

print()
print("== 3. prose-encoded relations in queue receipts ==")
q = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "queue"
mds = sorted(q.glob("*.md"))
verbs = {
    "SUPERSEDED/SUPERSEDES": re.compile(r"supersed", re.I),
    "corrobor": re.compile(r"corroborat", re.I),
    "per <Q-id precedent>": re.compile(r"per Q-\d+|Q-\d+ precedent|shared-index precedent", re.I),
    "void/VOID": re.compile(r"\bVOID\b"),
    "landed-by-commit ref": re.compile(r"[0-9a-f]{9}\b"),
}
for name, rx in verbs.items():
    files = [m.name for m in mds if rx.search(m.read_text(encoding="utf-8", errors="replace"))]
    print(f"  {name}: {len(files)}/{len(mds)} receipts, e.g. {files[:4]}")

print()
print("== 4. cross-carrier pointer sample (one receipt, relations inline) ==")
rec = (q / "Q-028.md").read_text(encoding="utf-8", errors="replace")
ptrs = re.findall(r"`([\w/.\-]+\.(?:py|md|json|jsonl|js|ps1))(?::(\d+(?:-\d+)?))?", rec)
print(f"Q-028.md inline file pointers={len(ptrs)} (each a potential edge, "
      f"all currently unparsed prose)")
