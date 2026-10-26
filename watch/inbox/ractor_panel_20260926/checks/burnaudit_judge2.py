import sys, os, json, re, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

print("\n=== JUDGE PASS 2 (targeted follow-ups), machine now:", now(), "===")

# A: burn wave QUEUE.md
QP = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "QUEUE.md")
print("\n=== A burn_wave QUEUE.md ===")
print("mtime:", datetime.datetime.fromtimestamp(os.path.getmtime(QP), datetime.timezone.utc).isoformat())
with open(QP, encoding="utf-8", errors="replace") as f:
    qlines = f.readlines()
print("total lines:", len(qlines))
for n, l in enumerate(qlines, 1):
    if ("B2-155" in l) or ("B2-475" in l) or ("B2-104" in l) or ("B2-217" in l):
        print("line %d: %s" % (n, l.rstrip()[:400]))

# B: B2_442_out_waves.json nested
print("\n=== B B2_442_out_waves.json nested fields ===")
WP = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "B2_442_out_waves.json")
txt = open(WP, encoding="utf-8", errors="replace").read()
for m in re.finditer(r'"(last_event_ts|absorbed_retries)"\s*:\s*("?[^",}]*"?)', txt):
    print("field:", m.group(0))
wj = json.loads(txt)
print("window:", json.dumps(wj.get("window"))[:300])
print("totals:", json.dumps(wj.get("totals"))[:500])
print("notes:", json.dumps(wj.get("notes"))[:400])

# C: LEDGER full row 540
print("\n=== C LEDGER row 540 full ===")
with open(os.path.join(ROOT, "memory", "burns", "LEDGER.jsonl"), encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if i == 540:
            print(line.rstrip())
            break

# D: trajectory details
print("\n=== D trajectory details ===")
TP = os.path.join(ROOT, "memory", "trajectory", "steps.jsonl")
want_full = {22388, 22455, 23456}
win = range(22483, 22492)
with open(TP, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if i in want_full:
            print("\n-- line %d full-ish --" % i)
            print(line.strip()[:2200])
        if i in win:
            try:
                j = json.loads(line)
            except Exception:
                continue
            cmd = str(j.get("command", ""))
            res = j.get("result") or {}
            out = str(res.get("output_excerpt", ""))[:220]
            print("line %d ts=%s cmd[:200]=%s" % (i, j.get("ts"), cmd[:200].replace("\n", " ")))
            print("    out[:220]:%s" % out.replace("\n", " "))
        if i > 23460:
            break
# line 22482 result excerpt full
with open(TP, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if i == 22482:
            j = json.loads(line)
            print("\nline 22482 result:", json.dumps(j.get("result"))[:500])
            break

# E: state dispatcher_fix
print("\n=== E BURN_WAVE_STATE dispatcher_fix ===")
st = json.load(open(os.path.join(ROOT, "memory", "burns", "BURN_WAVE_STATE.json"), encoding="utf-8"))
print(json.dumps(st.get("dispatcher_fix"), ensure_ascii=True)[:1200])

# F: fold receipt wired phrasing
print("\n=== F fold receipt phrasing ===")
FP = os.path.join(ROOT, "watch", "inbox", "BURN_b2-wave-fold_20260926_e.md")
t = open(FP, encoding="utf-8", errors="replace").read()
print("'wired' hits:", len(re.findall(r"wired", t)))
for m in re.finditer(r".{0,90}wired.{0,90}", t):
    print("  wired ctx:", m.group(0))
print("'adoption' hits:", len(re.findall(r"adoption", t)))
for m in re.finditer(r".{0,60}adoption.{0,90}", t):
    print("  adoption ctx:", m.group(0))

# G: width-24 contexts in GROUNDING_WAVE / GALA / FLEET_IMPRINT / LINKS / LING ref
print("\n=== G width-24 contexts ===")
for rel in (
    r"watch\GROUNDING_WAVE.md",
    r"watch\GROUNDING_WAVE.jsonl",
    r"watch\inbox\FLEET_IMPRINT_20260917.md",
    r"watch\inbox\GALA_20260925.md",
    r"watch\inbox\LINKS.jsonl",
    r"docs\ref\LING_API_REFERENCE.md",
):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print(rel, "(missing)")
        continue
    with open(p, encoding="utf-8", errors="replace") as f:
        content = f.read()
    hits = list(re.finditer(r".{0,110}(?:width-24|width 24|24-wide).{0,110}", content, re.I))
    print("%s: %d hits" % (rel, len(hits)))
    for m in hits[:3]:
        print("   ctx:", m.group(0).replace("\n", " "))

# H: B2_130_session_inputs_raw.txt nature
print("\n=== H B2_130_session_inputs_raw.txt head ===")
HP = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "B2_130_session_inputs_raw.txt")
print("size:", os.path.getsize(HP))
with open(HP, encoding="utf-8", errors="replace") as f:
    head = f.read(600)
print(repr(head[:600]))
mw = [m.group(0)[:120] for m in re.finditer(r".{0,40}width.{0,60}", open(HP, encoding='utf-8', errors='replace').read(), re.I)]
print("width mentions:", len(mw))
for s in mw[:4]:
    print("   ", s)

print("\nmachine now (end pass 2):", now())
print("=== END PASS 2 ===")
