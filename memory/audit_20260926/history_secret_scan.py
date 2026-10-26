"""Git-HISTORY secret scan — parent seat, replacing wave-2 lane 7's failed run.

Lane 7's history scanner died on its own harness bug
(`git() got an unexpected keyword argument 'input'`) AFTER successfully
enumerating 64,816 blobs. No history result exists. A key deleted from the
working tree is still in the object store, and `memory/tls/lan.key` proves
objects persist here (its blob is in Mag-backup.git across 39 refs).

Method: `git cat-file --batch` over every blob reachable from all refs, in
chunks, checking each blob's bytes for provider key shapes. Reports
path/commit + masked token only. NEVER prints a full secret.

Run: .venv/Scripts/python.exe memory/audit_20260926/history_secret_scan.py
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
CHUNK = 400

# High-confidence provider shapes only. No generic KEY=value (99.5% FP rate).
RULES = {
    "openai-key":     re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    "xai-key":        re.compile(rb"xai-[A-Za-z0-9]{20,}"),
    "anthropic-key":  re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}"),
    "gh-token":       re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    "github-pat":     re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    "google-api":     re.compile(rb"AIza[A-Za-z0-9_-]{30,}"),
    "aws-akid":       re.compile(rb"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    "telegram-bot":   re.compile(rb"\b8[0-9]{8,10}:[A-Za-z0-9_-]{30,}"),
    "hf-token":       re.compile(rb"hf_[A-Za-z0-9]{30,}"),
    "pem-private":    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY"),
}
# A token containing literal dots was redacted by a human — not a live secret.
DOTS = re.compile(rb"\.\.\.")


def mask(tok: bytes) -> str:
    try:
        s = tok.decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return "undecodable"
    if "..." in s:
        return "MASKED_BY_HUMAN(dots)"
    return f"len={len(s)} head={s[:7]}...tail={s[-3:]}"


def main():
    print("enumerating all blobs reachable from all refs...", flush=True)
    p = subprocess.run(["git", "-C", str(REPO), "rev-list", "--objects", "--all"],
                       capture_output=True, timeout=600)
    if p.returncode != 0:
        print("  rev-list failed:", p.stderr.decode("utf-8", "replace")[:300])
        return 2
    lines = p.stdout.split(b"\n")
    pairs = []
    for ln in lines:
        if not ln.strip():
            continue
        parts = ln.split(b" ", 1)
        sha = parts[0].decode("ascii", "replace")
        name = parts[1].decode("utf-8", "replace") if len(parts) > 1 else "(no path)"
        if len(sha) == 40:
            pairs.append((sha, name))
    print(f"  objects: {len(pairs):,}", flush=True)

    # Keep only paths that look like text sources (skip obvious binaries early).
    cand = [(s, n) for s, n in pairs
            if n.endswith((".py", ".md", ".json", ".jsonl", ".txt", ".yaml", ".yml",
                           ".cfg", ".ini", ".sh", ".ps1", ".env", ".js", ".ts"))]
    print(f"  text-candidate blobs: {len(cand):,}", flush=True)

    findings = []
    for i in range(0, len(cand), CHUNK):
        chunk = cand[i:i + CHUNK]
        inp = "\n".join(s for s, _ in chunk).encode() + b"\n"
        q = subprocess.run(["git", "-C", str(REPO), "cat-file", "--batch"],
                           input=inp, capture_output=True, timeout=600)
        out = q.stdout
        pos = 0
        for sha, name in chunk:
            nl = out.find(b"\n", pos)
            if nl < 0:
                break
            header = out[pos:nl].split()
            if len(header) < 3:
                pos = nl + 1
                continue
            size = int(header[2])
            body = out[nl + 1: nl + 1 + size]
            pos = nl + 1 + size + 1
            if size > 8_000_000 or size == 0:
                continue
            for rule, rx in RULES.items():
                for m in rx.finditer(body):
                    tok = m.group(0)
                    if rule == "pem-private":
                        findings.append((rule, name, sha, "PRIVATE KEY BLOCK"))
                    else:
                        mk = mask(tok)
                        if mk.startswith("MASKED"):
                            continue
                        findings.append((rule, name, sha, mk))
        if (i // CHUNK) % 20 == 0:
            print(f"   ...{i:,}/{len(cand):,}  findings={len(findings)}", flush=True)

    print(f"\nHISTORY SCAN COMPLETE: {len(findings)} raw findings")
    by_rule = {}
    for r, *_ in findings:
        by_rule[r] = by_rule.get(r, 0) + 1
    print("by rule:", by_rule)

    # dedupe by (rule, masked-shape) so we count DISTINCT secrets, not repeats
    distinct = {}
    for rule, name, sha, mk in findings:
        key = (rule, mk)
        distinct.setdefault(key, []).append((name, sha))
    print(f"\ndistinct secret shapes: {len(distinct)}")
    for (rule, mk), locs in sorted(distinct.items(), key=lambda kv: -len(kv[1])):
        print(f"  {rule:16} {mk:34} x{len(locs):<4} e.g. {locs[0][0][:60]}")

    import json
    outp = REPO / "memory" / "audit_20260926" / "history_secrets.json"
    outp.write_text(json.dumps({
        "raw_findings": len(findings),
        "by_rule": by_rule,
        "distinct": [{"rule": r, "masked": m, "count": len(l),
                      "paths": sorted({p for p, _ in v})[:6]}
                     for (r, m), v in distinct.items()],
    }, indent=1), encoding="utf-8")
    print(f"\nwrote {outp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
