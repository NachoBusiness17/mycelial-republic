# credrot judge scan, 2026-09-26. Decides the card kill condition by byte truth:
# (1) does either artifact carry a credential VALUE (full .env value or long prefix)?
# (2) do the estate's own high-severity provider rule shapes fire on the artifacts?
# (3) where does every key-shaped head token in the artifacts come from (receipt /
#     results json / .env head)? (4) does every rotation table row carry a rollback
#     cell? (5) em-dash scan. HARD LAW held: this script never opens any corpus/
#     dump-carrier file; it reads root .env in memory only and prints only masked
#     heads and booleans, never a value.
import json
import os
import re
import sys

REPO = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
PANEL = os.path.join(REPO, "watch/inbox/ractor_panel_20260926")
ARTIFACTS = [
    ("credrot-one", os.path.join(PANEL, "cands/credrot-one.md")),
    ("credrot-two", os.path.join(PANEL, "cands/credrot-two.md")),
]
RECEIPT = os.path.join(REPO, "watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md")
RESULTS_JSON = os.path.join(REPO, "watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json")
KEYS_JSON = os.path.join(REPO, "configs/keys.json")
ENV = os.path.join(REPO, ".env")
JOURNAL = os.path.join(REPO, "watch/inbox/KEY_ROTATION_JOURNAL.jsonl")


def read(p):
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


# ---- load .env (values in memory only; never printed) ----
env_pairs = []
if os.path.exists(ENV):
    for line in read(ENV).splitlines():
        m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if not m:
            continue
        name, val = m.group(1), m.group(2).strip().strip('"').strip("'")
        if val:
            env_pairs.append((name, val))
else:
    print("ENV FILE MISSING:", ENV)

receipt_text = read(RECEIPT)
results_text = read(RESULTS_JSON)
keys_text = read(KEYS_JSON)

print("=" * 78)
print("CHECK 0: journal existence (both candidates claim it does not exist yet)")
print("KEY_ROTATION_JOURNAL.jsonl exists:", os.path.exists(JOURNAL))
print("env names loaded (values never printed):", len(env_pairs))

# estate high-severity provider rules (regex source: SECRET_SCAN_RULESET
# table lines 36-43) plus long generic token runs
RULES = {
    "OPENAI-CLASSIC": re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}T3BlbkFJ[A-Za-z0-9_\-]{20,}\b"),
    "OPENAI-PROJ": re.compile(r"\bsk-proj-[A-Za-z0-9_\-]{20,200}\b"),
    "ANTHROPIC-KEY": re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,200}\b"),
    "OPENROUTER-KEY": re.compile(r"\bsk-or-v1-[a-f0-9]{64}\b"),
    "GROQ-KEY": re.compile(r"\bgsk_[A-Za-z0-9]{20,80}\b"),
    "XAI-KEY": re.compile(r"\bxai-[A-Za-z0-9]{18,80}\b"),
    "DEEPSEEK-KEY": re.compile(r"\bsk-[a-f0-9]{32}\b"),
    "ZHIPU-ZAI-KEY": re.compile(r"\b[0-9a-f]{32}\.[0-9a-f]{16}\b"),
    "AWS-SECRET-40": re.compile(r"\b[A-Za-z0-9/+=]{40}\b"),
}
# short-head token shapes (the published mask convention, 4-14 chars of material)
HEAD_TOKEN = re.compile(
    r"sk-or-v1-[a-f0-9]{4,8}|gsk_[A-Za-z0-9]{4,8}|xai-[A-Za-z0-9]{2,6}"
    r"|sk-ant-api03-[A-Za-z0-9_\-]{3,6}|sk-proj-[A-Za-z0-9]{4,8}"
    r"|sk-[a-f0-9]{4,6}|\b[0-9a-f]{8}\b"
)


def env_hit(tok):
    out = []
    for name, val in env_pairs:
        if tok == val:
            out.append((name, "FULL-VALUE"))
        elif val.startswith(tok) and len(tok) < len(val):
            out.append((name, "prefix %d/%d" % (len(tok), len(val))))
    return out


for cand, path in ARTIFACTS:
    text = read(path)
    print("=" * 78)
    print("CANDIDATE:", cand, "| bytes:", len(text.encode("utf-8")))
    print("-- CHECK 1: full .env VALUE containment (kill prong 1, decisive)")
    full = [(n) for n, v in env_pairs if len(v) >= 16 and v in text]
    print("   full values contained:", full if full else "NONE")
    print("-- CHECK 1b: longest prefix of each .env value present in artifact")
    for name, val in env_pairs:
        if len(val) < 12:
            continue
        best = 0
        for L in range(min(len(val), 48), 5, -1):
            if val[:L] in text:
                best = L
                break
        if best >= 6:
            flag = "VALUE-CARRIED" if best == len(val) else ("OVER-MASK-CONVENTION" if best > 18 else "head/mask range")
            print("   %-24s longest prefix present: %2d/%2d  %s" % (name, best, len(val), flag))
    print("-- CHECK 2: estate high-severity rule shapes on artifact bytes")
    any_hit = False
    for rid, rx in RULES.items():
        hits = rx.findall(text)
        if hits:
            any_hit = True
            print("   %s: %d match(es), lengths %s" % (rid, len(hits), sorted({len(h) for h in hits})))
    if not any_hit:
        print("   ALL RULES: 0 matches")
    print("-- CHECK 3: provenance of every key-shaped head token quoted in artifact")
    seen = set()
    for tok in HEAD_TOKEN.findall(text):
        if tok in seen or len(tok) < 6:
            continue
        seen.add(tok)
        src = []
        if tok in receipt_text:
            src.append("B2_73-receipt")
        if tok in results_text:
            src.append("results-json")
        if tok in keys_text:
            src.append("keys.json")
        eh = env_hit(tok)
        print("   %-20s len=%2d  src=%s  env=%s" % (tok, len(tok), ",".join(src) or "NOWHERE-FILED", eh if eh else "no-env-relation"))
    print("-- CHECK 4: rollback column coverage in recommendation tables")
    rb_col = None
    rows = 0
    missing = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if any(c.lower() == "rollback" for c in cells):
            rb_col = cells.index("Rollback") if "Rollback" in cells else next(i for i, c in enumerate(cells) if c.lower() == "rollback")
            continue
        if rb_col is None or set(s.replace("|", "").replace("-", "").strip()) == set():
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows += 1
        if rb_col >= len(cells) or not cells[rb_col] or set(cells[rb_col]) <= set("-: "):
            missing.append(s[:70])
    print("   table data rows under a Rollback header: %d ; rows with EMPTY rollback cell: %d" % (rows, len(missing)))
    for mline in missing:
        print("     EMPTY-ROLLBACK ROW:", mline)
    print("-- CHECK 5: em-dash scan (record law)")
    em = [ch for ch in text if ch in "\u2014\u2013"]
    print("   U+2014/U+2013 count:", len(em))

print("=" * 78)
print("CHECK 6: provenance surfaces themselves value-free (receipt, results json)")
for label, p in [("receipt", RECEIPT), ("results-json", RESULTS_JSON)]:
    t = read(p)
    hits = {rid: len(rx.findall(t)) for rid, rx in RULES.items()}
    hits = {k: v for k, v in hits.items() if v}
    contained = [n for n, v in env_pairs if len(v) >= 16 and v in t]
    print("   %-12s rule hits: %s ; full .env values contained: %s" % (label, hits or "NONE", contained or "NONE"))
print("=" * 78)
print("SCAN COMPLETE. No corpus/ file was opened by this script; no value printed.")
