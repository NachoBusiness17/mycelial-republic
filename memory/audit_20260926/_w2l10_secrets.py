"""Lane 10 part 3: does the shared surface leak secrets? (extends lane 9)"""
import json, os, re
from pathlib import Path

INBOX = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox")

# High-signal patterns only. Never print the secret value - only file + line + pattern name.
PATS = [
    ("OPENAI_STYLE_KEY", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}")),
    ("ANTHROPIC_STYLE_KEY", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("XAI_STYLE_KEY", re.compile(r"\bxai-[A-Za-z0-9]{20,}")),
    ("GOOGLE_API_KEY", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("AWS_ACCESS_KEY_ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GITHUB_TOKEN", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}")),
    ("SLACK_TOKEN", re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("PRIVATE_KEY_BLOCK", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("BEARER_LONGLIVED", re.compile(r"(?i)authorization\s*[:=]\s*[\"']?bearer\s+[A-Za-z0-9_\-\.]{24,}")),
    ("ZAI_STYLE", re.compile(r"\b[0-9a-f]{8}\.[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{12}\b")),
    ("CURLYPASS_ASSIGN", re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']")),
]
TEXT_EXT = {".md", ".json", ".jsonl", ".txt", ".py", ".js", ".mjs", ".sh", ".yaml", ".yml",
            ".env", ".cfg", ".ini", ".html", ".csv", ".toml", ".log", ".receipt", ""}

hits = []
scanned = 0
skipped_binary = 0
for dirpath, dirnames, filenames in os.walk(INBOX):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".mimosa")]
    for fn in filenames:
        f = Path(dirpath) / fn
        ext = f.suffix.lower()
        if ext not in TEXT_EXT and ext not in (".png", ".pdf", ".jpg", ".gif", ".zip"):
            continue
        if ext in (".png", ".pdf", ".jpg", ".gif", ".zip"):
            skipped_binary += 1
            continue
        try:
            if f.stat().st_size > 8_000_000:
                continue
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        for lineno, line in enumerate(txt.splitlines(), 1):
            for name, rx in PATS:
                if rx.search(line):
                    hits.append({
                        "pattern": name,
                        "file": str(f.relative_to(INBOX)).replace("\\", "/"),
                        "line": lineno,
                        "len": len(line.strip()),
                    })
                    break

from collections import Counter
by_pat = Counter(h["pattern"] for h in hits)
by_file = Counter(h["file"] for h in hits)
print("files scanned:", scanned, "| binary skipped:", skipped_binary)
print("TOTAL SECRET-SHAPED HITS:", len(hits))
print("\nby pattern:", dict(by_pat.most_common()))
print("\ntop files:")
for k, v in by_file.most_common(25):
    print(f"  {v:4d}  {k}")

# Are any of these files in git? (tracked => durable leak surface; untracked => still on disk)
res = {
    "files_scanned": scanned,
    "binary_skipped": skipped_binary,
    "total_hits": len(hits),
    "by_pattern": dict(by_pat),
    "top_files": by_file.most_common(40),
    "all_hits": hits[:400],
}
Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/memory/audit_20260926/_w2l10_secrets.json").write_text(
    json.dumps(res, indent=2), encoding="utf-8")
