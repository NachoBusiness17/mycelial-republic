"""B2-73 UF-129 redo: local gitleaks-pattern regex + entropy secret scan.

Scope: corpus/ and watch/inbox/ (recursive), text files only.
Local python only, no network, no model calls. Values are never written in
full anywhere: report rows carry a masked head (first 6 chars) plus length.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_73_secret_scan.py
Output: watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json
"""
import json
import math
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# ROOT = repo root (script lives in watch/inbox/burn_wave_20260926/)
SCOPES = [os.path.join(ROOT, "corpus"), os.path.join(ROOT, "watch", "inbox")]
RESULTS = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "B2_73_secret_scan_results.json")

MAX_FILE_BYTES = 10 * 1024 * 1024      # skip single files above 10MB, counted
MAX_FINDINGS_PER_RULE = 60000          # stored rows per rule; counts stay exact
MAX_ENT_STORED = 20000                 # stored entropy rows; counts stay exact
SNIFF_BYTES = 8192

# --- gitleaks-derived provider rules (concrete token shapes) ----------------
RULES = [
    ("AWS-ACCESS-KID", "high", r"\bAKIA[0-9A-Z]{16}\b"),
    ("AWS-SECRET-40", "high", r"\b(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"),
    ("GOOGLE-API-KEY", "high", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("GOOGLE-OAUTH-AQ", "high", r"\bAQ[a-zA-Z0-9_\-]{30,}\b"),
    ("GITHUB-TOKEN", "high", r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),
    ("GITHUB-FINEGRAIN", "high", r"\bgithub_pat_[A-Za-z0-9_]{20,255}\b"),
    ("GITLAB-PAT", "high", r"\bglpat-[A-Za-z0-9_\-]{20,}\b"),
    ("OPENAI-CLASSIC", "high", r"\bsk-[A-Za-z0-9_\-]{20,}T3BlbkFJ[A-Za-z0-9_\-]{20,}\b"),
    ("OPENAI-PROJ", "high", r"\bsk-proj-[A-Za-z0-9_\-]{20,200}\b"),
    ("ANTHROPIC-KEY", "high", r"\bsk-ant-[A-Za-z0-9_\-]{20,200}\b"),
    ("OPENROUTER-KEY", "high", r"\bsk-or-v1-[a-f0-9]{64}\b"),
    ("GROQ-KEY", "high", r"\bgsk_[A-Za-z0-9]{20,80}\b"),
    ("XAI-KEY", "high", r"\bxai-[A-Za-z0-9]{18,80}\b"),
    ("DEEPSEEK-KEY", "high", r"\bsk-[a-f0-9]{32}\b"),
    ("ZHIPU-ZAI-KEY", "high", r"\b[0-9a-f]{32}\.[0-9a-f]{16}\b"),
    ("SLACK-TOKEN", "high", r"\bxox[abposr]-[A-Za-z0-9\-]{10,250}\b"),
    ("STRIPE-KEY", "high", r"\b(?:sk|pk|rk)_(?:live|test)_[0-9a-zA-Z]{10,}\b"),
    ("SENDGRID-KEY", "high", r"\bSG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}\b"),
    ("TELEGRAM-BOT", "high", r"\b[0-9]{8,10}:AA[A-Za-z0-9_\-]{33}\b"),
    ("TWILIO-SID", "medium", r"\b(?:SK|AC)[0-9a-f]{32}\b"),
    ("MAILGUN-KEY", "high", r"\bkey-[a-f0-9]{32}\b"),
    ("NPM-TOKEN", "high", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("PYPI-TOKEN", "high", r"\bpypi-[A-Za-z0-9_\-]{50,}\b"),
    ("VERCEL-TOKEN", "high", r"\bvercel_[A-Za-z0-9]{24}\b"),
    ("JWT-TRIPLE", "medium", r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"),
    ("PRIVATE-KEY-BLOCK", "critical", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY(?: BLOCK)?-----"),
    ("CONNSTRING-CRED", "high", r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s:@/]+:[^\s@/]+@"),
    ("GENERIC-KEYASSIGN", "medium", r"(?i:\b(?:api[_\-]?key|apikey|secret|access[_\-]?token|auth[_\-]?token|password|passwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9+/_\-]{16,})"),
    ("ENV-ASSIGN", "low", r"^[A-Z][A-Z0-9_]{3,}\s*=\s*['\"]?[^\s'\"]{8,}"),
    ("HEROKU-API", "medium", r"\bHRKU-[0-9a-fA-F\-]{36}\b"),
    ("GENERIC-BEARER", "medium", r"(?i:\bbearer\s+[A-Za-z0-9_\-\.=+/]{20,})"),
]

# entropy branch runs last so concrete rules win their positions
ENT_RE_RAW = r"[A-Za-z0-9+/_\-]{25,}"

ALLOW_RE = re.compile(
    r"(?i)("
    r"your[_\-]?api[_\-]?key|your[_\-]?token|<[^>\n]{1,40}>|\$\{[^}\n]{1,40}\}"
    r"|x{4,}|\.{4,}|\*{3,}|REDACTED|MASKED|PLACEHOLDER|EXAMPLE[_A-Z]*|DUMMY|FAKE"
    r"|abcd1234|1234567890|0123456789abcdef"
    r")"
)

COMBINED = re.compile(
    "|".join("(%s)" % pat for _rid, _sev, pat in RULES)
    + "|(" + ENT_RE_RAW + ")"
)
RULE_SEV = {rid: sev for rid, sev, _p in RULES}
RULE_NAMES = [rid for rid, _s, _p in RULES]
assert COMBINED.groups == len(RULES) + 1, (
    "group count drift: %d compiled vs %d expected (stray capture group)"
    % (COMBINED.groups, len(RULES) + 1)
)
_probe = COMBINED.search("AKIAIOSFODNN7EXAMPLE")
assert _probe and RULE_NAMES[_probe.lastindex - 1] == "AWS-ACCESS-KID", (
    "routing self-check failed")

SKIP_DIR_PARTS = {".git", "node_modules", "__pycache__", ".venv"}

ENTROPY_MIN = 4.3
ENT_LEN_MIN = 25


def shannon(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def is_binary(chunk):
    if b"\x00" in chunk:
        return True
    if not chunk:
        return True
    textish = sum(1 for b in chunk if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return textish / len(chunk) < 0.85


def mask(tok):
    head = tok[:6]
    return head + "..." + "(len=%d)" % len(tok)


def iter_files():
    for scope in SCOPES:
        for dirpath, dirnames, filenames in os.walk(scope):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS]
            for fn in filenames:
                yield os.path.join(dirpath, fn)


def main():
    t0 = time.time()
    census = {
        "files_seen": 0, "scanned": 0, "binary_skipped": 0, "large_skipped": 0,
        "read_error": 0, "bytes_scanned": 0,
    }
    findings = []           # capped rows
    rule_counts = {rid: 0 for rid in RULE_NAMES}
    ent_counts = {"total": 0, "stored": 0}
    files_with_hits = set()
    ent_files = set()

    with open(RESULTS, "w", encoding="utf-8", newline="\n") as out:
        out.write("[]")  # placeholder replaced at end

    for path in iter_files():
        census["files_seen"] += 1
        base = os.path.basename(path)
        if path.endswith(("B2_73_secret_scan.py", "B2_73_secret_scan_results.json")):
            continue
        try:
            size = os.path.getsize(path)
        except OSError:
            census["read_error"] += 1
            continue
        if size > MAX_FILE_BYTES:
            census["large_skipped"] += 1
            continue
        try:
            with open(path, "rb") as fh:
                chunk = fh.read(SNIFF_BYTES)
                if is_binary(chunk):
                    census["binary_skipped"] += 1
                    continue
                fh.seek(0)
                data = fh.read(MAX_FILE_BYTES)
        except OSError:
            census["read_error"] += 1
            continue
        census["scanned"] += 1
        census["bytes_scanned"] += len(data)
        text = data.decode("utf-8", errors="ignore")
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        for i, line in enumerate(text.splitlines(), 1):
            if not line or len(line) > 4000:
                continue
            for m in COMBINED.finditer(line):
                idx = m.lastindex
                if idx is None:
                    continue
                if idx > len(RULES):
                    kind = "ENT"
                else:
                    kind = RULE_NAMES[idx - 1]
                tok = m.group()
                if kind == "ENT":
                    if len(tok) >= ENT_LEN_MIN:
                        h = shannon(tok)
                        if h >= ENTROPY_MIN:
                            ent_counts["total"] += 1
                            if ALLOW_RE.search(tok):
                                continue
                            ent_files.add(rel)
                            if ent_counts["stored"] < MAX_ENT_STORED:
                                ent_counts["stored"] += 1
                                findings.append({
                                    "kind": "entropy", "file": rel, "line": i,
                                    "entropy": round(h, 2), "masked": mask(tok),
                                })
                    continue
                if ALLOW_RE.search(tok) or ALLOW_RE.search(line[:120]):
                    continue
                rule_counts[kind] += 1
                files_with_hits.add(rel)
                if rule_counts[kind] <= MAX_FINDINGS_PER_RULE:
                    findings.append({
                        "kind": kind, "severity": RULE_SEV[kind],
                        "file": rel, "line": i, "masked": mask(tok),
                    })

    result = {
        "lane": "B2-73",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scopes": ["corpus/", "watch/inbox/"],
        "census": census,
        "runtime_sec": round(time.time() - t0, 1),
        "rule_counts": {k: v for k, v in rule_counts.items() if v},
        "files_with_rule_hits": sorted(files_with_hits),
        "entropy": ent_counts,
        "entropy_files": sorted(ent_files)[:200],
        "findings_stored": findings,
        "thresholds": {"entropy_min": ENTROPY_MIN, "ent_len_min": ENT_LEN_MIN,
                        "max_file_bytes": MAX_FILE_BYTES},
    }
    with open(RESULTS, "w", encoding="utf-8", newline="\n") as out:
        json.dump(result, out, indent=1)

    print("runtime_sec", result["runtime_sec"])
    print("census", json.dumps(census))
    print("rule_counts", json.dumps(result["rule_counts"]))
    print("files_with_rule_hits", len(files_with_hits))
    print("entropy_candidates", ent_counts["total"], "stored", ent_counts["stored"])
    print("results", RESULTS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
