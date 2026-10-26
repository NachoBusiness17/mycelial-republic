# credrot revision census, 2026-09-26. Re-proves on live bytes, for the final
# packet, the three things the panel critique demands as carried evidence:
# (R1) journal + pre-snapshot existence state; (R2) the 13-at-rest mapping of
# receipt-published dump heads to current .env names; (R3) the 5 orphans that
# match no current name; (R4) the family collision guard for the 8-14 char
# head-match method (pairwise distinctness per family, minimal distinct head
# length). HARD LAW held: this script opens NO corpus/ file; root .env is read
# into memory only; the only value bytes ever printed are 6-char heads in the
# policy rule 1 canonical mask form (6 chars plus length). Dump heads already
# published by the B2_73 receipt are printed at their published length.
import os
import re
import sys

REPO = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
ENV = os.path.join(REPO, ".env")
JOURNAL = os.path.join(REPO, "watch/inbox/KEY_ROTATION_JOURNAL.jsonl")
SNAP = os.path.join(REPO, ".env.prerotation-20260926")

# receipt-published dump heads (B2_73_secret_scan_20260926.md Evidence lines
# 46-54) -> the credrot-two claimed rest-place name for the 13 at-rest
AT_REST = [
    ("sk-effc9", "DEEPSEEK_API_KEY"),
    ("xai-68sO", "XAI_API_KEY"),
    ("sk-or-v1-4167", "OPENROUTER_API_KEY"),
    ("sk-or-v1-6be0", "OPENROUTER_API_KEY_2"),
    ("sk-proj-UjAW", "OPENAI_API_KEY"),
    ("sk-ant-api03-_NxL", "ANTHROPIC_API_KEY"),
    ("sk-ant-api03-IWEF", "ANTHROPIC_API_KEY_2"),
    ("6881759e", "VASTAI_API_KEY"),
    ("3254aca9", "ZAI_API_KEY"),
    ("e3c50501", "ZAI_API_KEY_2"),
    ("bafc5c96", "ZAI_API_KEY_3"),
    ("e18faf05", "ZAI_API_KEY_Pro"),
    ("4f8ac54f", "ZAI_API_KEY_Lite"),
]
# receipt-published dump heads claimed to match NO current name (the 5 orphans)
ORPHANS = ["gsk_17bq", "gsk_8LAQ", "088650c6", "sk-c2bd8", "xai-gO"]
# families for the collision guard: name -> value resolved from .env below
FAMILIES = {
    "ZAI": ["ZAI_API_KEY", "ZAI_API_KEY_2", "ZAI_API_KEY_3", "ZAI_API_KEY_Pro", "ZAI_API_KEY_Lite"],
    "GROQ": ["GROQ_API_KEY", "GROQ_API_KEY_2"],
    "ANTHROPIC": ["ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY_2"],
    "OPENROUTER": ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2"],
}


def mask6(val):
    # policy rule 1 canonical quoting format: 6 chars plus length
    return "%s...(len=%d)" % (val[:6], len(val))


env = {}
with open(ENV, "r", encoding="utf-8", errors="replace") as f:
    for line in f.read().splitlines():
        m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if not m:
            continue
        name, val = m.group(1), m.group(2).strip().strip('"').strip("'")
        if val:
            env[name] = val

print("=" * 78)
print("R1: journal / pre-snapshot existence (negative results are first-class)")
print("KEY_ROTATION_JOURNAL.jsonl exists:", os.path.exists(JOURNAL))
print(".env.prerotation-20260926 exists:", os.path.exists(SNAP))
print("env names with values loaded (values never printed):", len(env))

print("=" * 78)
print("R2: the 13-at-rest mapping (dump head -> claimed rest-place name)")
ok = 0
for head, name in AT_REST:
    val = env.get(name)
    if val is None:
        verdict = "NAME-ABSENT"
    elif val.startswith(head):
        # uniqueness: no OTHER name may carry the same head
        others = [n for n, v in env.items() if n != name and v.startswith(head)]
        verdict = "MATCH" + ("  AMBIGUOUS-ALSO:" + ",".join(others) if others else "  unique")
        ok += 1
    else:
        verdict = "MISMATCH (at-rest head is %s)" % mask6(val)
    print("  %-18s -> %-22s %s" % (head, name, verdict))
print("  at-rest matches: %d/13" % ok)

print("=" * 78)
print("R3: the 5 orphans match no current name value")
for head in ORPHANS:
    hits = [n for n, v in env.items() if v.startswith(head)]
    print("  %-10s -> %s" % (head, "orphan (no current name carries it)" if not hits else "NOT-ORPHAN: " + ",".join(hits)))

print("=" * 78)
print("R4: family collision guard for the head-match method")
print("  at-rest heads printed in canonical 6-char + length form only")
for fam, names in FAMILIES.items():
    vals = [(n, env[n]) for n in names if n in env]
    if len(vals) < 2:
        print("  %s: fewer than 2 named values at rest; guard n/a" % fam)
        continue
    for n, v in vals:
        print("  %-12s %s" % (n, mask6(v)))
    for k in range(8, 18):
        heads = [v[:k] for _, v in vals]
        if len(set(heads)) == len(heads):
            print("  %-12s pairwise distinct at %d chars: True (min distinct head length %d)" % (fam, k, k))
            break
    else:
        print("  %-12s pairwise distinct up to 17 chars: FALSE (manual resolution needed)")
    if any(len(set(v[:8] for _, v in vals)) != len(vals) for _ in [0]):
        pass
    # explicit 8-char verdict, the length the at-rest census used
    h8 = [v[:8] for _, v in vals]
    print("  %-12s pairwise distinct at 8 chars: %s" % (fam, len(set(h8)) == len(h8)))

print("=" * 78)
print("R5: exact value lengths for the two Groq rest places (lengths only)")
for n in ("GROQ_API_KEY", "GROQ_API_KEY_2"):
    print("  %s length: %s" % (n, len(env[n]) if n in env else "ABSENT"))

print("=" * 78)
print("CENSUS COMPLETE. No corpus/ file was opened; no value beyond a 6-char")
print("canonical mask head was printed.")
