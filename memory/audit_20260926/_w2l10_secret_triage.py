"""Lane 10 part 3b: are the 3 secret-shaped hits real or placeholders? No values echoed."""
import hashlib, re
from pathlib import Path

INBOX = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox")
targets = [
    ("ADAM_ONBOARDING_FULL_20260924.md", "CURLYPASS_ASSIGN"),
    ("audit_20260926/LANE0_PARENT_INTEGRATOR.md", "PRIVATE_KEY_BLOCK"),
    ("burn_wave_20260926/B2_73_secret_scan.py", "AWS_ACCESS_KEY_ID"),
]
REDACT = re.compile(r"(?i)\b(redact|example|placeholder|dummy|fake|sample|not\s+a\s+real|"
                    r"your[_-]?key|xxxx|\.\.\.|<[^>]+>|\*{3,}|masked|scrubbed|sanitiz)", )
for rel, pat in targets:
    f = INBOX / rel
    txt = f.read_text(encoding="utf-8", errors="ignore")
    print(f"\n=== {rel}  [{pat}]  tracked-in-git-file={f.exists()}")
    for i, line in enumerate(txt.splitlines(), 1):
        if pat == "CURLYPASS_ASSIGN" and not re.search(r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']", line):
            continue
        if pat == "PRIVATE_KEY_BLOCK" and "PRIVATE KEY" not in line:
            continue
        if pat == "AWS_ACCESS_KEY_ID" and not re.search(r"AKIA[0-9A-Z]{16}", line):
            continue
        # print a REDACTED view: keep structure, mask the value
        masked = re.sub(r"(AKIA)[0-9A-Z]{4}([0-9A-Z]{4})([0-9A-Z]{4})([0-9A-Z]{4})",
                        r"\1***\2***\3***\4[REDACTED-AWS-KEYID]", line)
        masked = re.sub(r"([\"'])([^\"']{12,})([\"'])",
                        lambda m: m.group(1) + m.group(2)[:4] + f"...<{len(m.group(2))}ch>" + m.group(3), masked)
        flag = "LOOKS-REDACTED/EXAMPLE" if REDACT.search(line) else "LOOKS-LIVE"
        print(f"  L{i}  [{flag}]  {masked.strip()[:190]}")
