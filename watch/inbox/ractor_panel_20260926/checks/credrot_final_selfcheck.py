# credrot final self-check, 2026-09-26. Same kill-condition instruments the
# judge ran (checks/credrot_judge_scan.py), pointed at the FINAL packet bytes:
# (S1) no full .env value contained; (S2) longest prefix of any live value in
# head/mask range; (S3) zero estate high-severity rule-shape matches; (S4)
# zero em-dash characters; (S5) every gsk_/xai-/sk- head token is either
# B2_73-receipt-published or a 6-char canonical at-rest mask; (S6) rollback
# cells non-empty; (S7) the two fresh Groq at-rest heads appear ONLY in
# canonical 6-char+len form. HARD LAW: no corpus/ file opened; .env read into
# memory only; no value printed.
import os
import re

REPO = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
FINAL = os.path.join(REPO, "watch/inbox/ractor_panel_20260926/credrot.final.md")
RECEIPT = os.path.join(REPO, "watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md")
ENV = os.path.join(REPO, ".env")


def read(p):
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


env_pairs = []
for line in read(ENV).splitlines():
    m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
    if m and m.group(2).strip():
        env_pairs.append((m.group(1), m.group(2).strip().strip('"').strip("'")))

text = read(FINAL)
receipt_text = read(RECEIPT)
print("final bytes:", len(text.encode("utf-8")))

print("-- S1: full .env value containment")
full = [n for n, v in env_pairs if len(v) >= 16 and v in text]
print("   full values contained:", full if full else "NONE")

print("-- S2: longest prefix of each live value present (>= 6 chars flagged)")
worst = 0
for name, val in env_pairs:
    if len(val) < 12:
        continue
    best = 0
    for L in range(min(len(val), 48), 5, -1):
        if val[:L] in text:
            best = L
            break
    if best >= 6:
        flag = "OVER-MASK-CONVENTION" if best > 18 else "head/mask range"
        print("   %-24s %2d/%2d  %s" % (name, best, len(val), flag))
        worst = max(worst, best)
print("   worst prefix:", worst)

print("-- S3: estate high-severity rule shapes")
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
any_hit = False
for rid, rx in RULES.items():
    hits = rx.findall(text)
    if hits:
        any_hit = True
        print("   %s: %d match(es)" % (rid, len(hits)))
if not any_hit:
    print("   ALL RULES: 0 matches")

print("-- S4: em-dash scan (record law)")
print("   U+2014/U+2013 count:", sum(1 for ch in text if ch in "\u2014\u2013"))

print("-- S5: provenance of key-shaped head tokens")
HEAD_TOKEN = re.compile(
    r"sk-or-v1-[a-f0-9]{4,8}|gsk_[A-Za-z0-9]{4,8}|xai-[A-Za-z0-9]{2,6}"
    r"|sk-ant-api03-[A-Za-z0-9_\-]{3,6}|sk-proj-[A-Za-z0-9]{4,8}"
    r"|sk-[a-f0-9]{4,6}|\b[0-9a-f]{8}\b"
)
seen = set()
for tok in HEAD_TOKEN.findall(text):
    if tok in seen or len(tok) < 6:
        continue
    seen.add(tok)
    src = []
    if tok in receipt_text:
        src.append("B2_73-receipt")
    for name, val in env_pairs:
        if val.startswith(tok) and len(tok) < len(val):
            src.append("at-rest:" + name)
    print("   %-20s len=%2d  src=%s" % (tok, len(tok), ",".join(src) or "NOWHERE-FILED"))

print("-- S6: rollback cell coverage")
rb_col = None
rows = 0
missing = 0
for ln in text.splitlines():
    s = ln.strip()
    if not s.startswith("|"):
        continue
    cells = [c.strip() for c in s.strip("|").split("|")]
    if any(c.lower() == "rollback" for c in cells):
        rb_col = next(i for i, c in enumerate(cells) if c.lower() == "rollback")
        continue
    if rb_col is None or all(set(c) <= set("-: ") for c in cells):
        continue
    rows += 1
    if rb_col >= len(cells) or not cells[rb_col] or set(cells[rb_col]) <= set("-: "):
        missing += 1
print("   data rows under a Rollback header: %d ; empty rollback cells: %d" % (rows, missing))

print("-- S7: fresh Groq at-rest heads appear only in canonical 6-char form")
for six, name in (("gsk_QI", "GROQ_API_KEY"), ("gsk_w2", "GROQ_API_KEY_2")):
    longer = re.findall(six + r"[A-Za-z0-9]{1,}", text)
    canon = re.findall(re.escape(six) + r"\.\.\.\(len=56\)", text)
    print("   %s: 7+char occurrences %d ; canonical form occurrences %d" % (name, len(longer), len(canon)))

print("SELF-CHECK COMPLETE. No corpus/ file opened; no value printed.")
