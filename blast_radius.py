"""Measure ALLOW_RE x ENT counter-leak blast radius — targeted scan."""
import math, os, re, json
from collections import Counter

ENTROPY_MIN = 4.3
ENT_LEN_MIN = 25
ENT_RE_RAW = re.compile(r"[A-Za-z0-9+_\-]{25,}")
ALLOW_RE = re.compile(
    r"(?i)("
    r"your[_\-]?api[_\-]?key|your[_\-]?token|<[^>\n]{1,40}>|\$\{[^}\n]{1,40}\}"
    r"|x{4,}|\.{4,}|\*{3,}|REDACTED|MASKED|PLACEHOLDER|EXAMPLE[_A-Z]*|DUMMY|FAKE"
    r"|abcd1234|1234567890|0123456789abcdef"
    r")"
)

def shannon(s):
    if not s: return 0.0
    freq = Counter(s)
    length = len(s)
    ent = 0.0
    for c, n in freq.items():
        p = n / length
        if p > 0: ent -= p * math.log2(p)
    return ent

def mask(tok):
    if len(tok) <= 8: return "*" * len(tok)
    return tok[:4] + "*" * (len(tok) - 8) + tok[-4:]

def classify_allow(tok):
    m = ALLOW_RE.search(tok)
    if not m: return None
    val = m.group(); vlow = val.lower()
    if vlow == "abcd1234": return "abcd1234"
    if vlow == "1234567890": return "1234567890"
    if vlow == "0123456789abcdef": return "0123456789abcdef"
    if vlow == "redacted": return "REDACTED"
    if vlow == "masked": return "MASKED"
    if vlow == "placeholder": return "PLACEHOLDER"
    if vlow.startswith("example"): return "EXAMPLE*"
    if vlow in ("dummy", "fake"): return vlow.upper()
    if val.startswith("<") and val.endswith(">"): return "<...>"
    if val.startswith("${") and val.endswith("}"): return "${...}"
    if val.startswith("your_"): return "your_*"
    if re.match(r"^x{4,}$", val): return "x{4,}"
    if re.match(r"^\.{4,}$", val): return ".{4,}"
    if re.match(r"^\*{3,}$", val): return "*{3,}"
    return "other"

def scan_file(path):
    results = {"ent_total": 0, "ent_kept": 0, "ent_suppressed": 0,
               "allow_clauses": Counter(), "samples": []}
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return results
    for i, line in enumerate(content.split("\n"), 1):
        for m in ENT_RE_RAW.finditer(line):
            tok = m.group()
            if len(tok) >= ENT_LEN_MIN:
                h = shannon(tok)
                if h >= ENTROPY_MIN:
                    results["ent_total"] += 1
                    if ALLOW_RE.search(tok):
                        results["ent_suppressed"] += 1
                        clause = classify_allow(tok)
                        results["allow_clauses"][clause] += 1
                        if len(results["samples"]) < 10:
                            results["samples"].append({
                                "tok": mask(tok), "entropy": round(h, 2),
                                "clause": clause, "line": i,
                            })
                    else:
                        results["ent_kept"] += 1
    return results

def scan_target_dirs(root, targets, max_files=500):
    skip_dirs = {".git", "__pycache__", ".venv", "node_modules", ".tox",
                 "venv", ".eggs", ".pytest_cache", "htmlcov", ".mypy_cache",
                 "dist", "build", ".next", ".nuxt", "target", ".cargo",
                 "vendor", "third_party", ".tox"}
    total = {"ent_total": 0, "ent_kept": 0, "ent_suppressed": 0,
             "allow_clauses": Counter(), "samples": [], "files_scanned": 0}
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir != "." and not any(
            rel_dir == t or rel_dir.startswith(t + os.sep)
            for t in targets
        ):
            dirnames[:] = []
            continue
        for fn in filenames:
            if file_count >= max_files: break
            if not fn.endswith(".py"): continue
            fp = os.path.join(dirpath, fn)
            try:
                rel = os.path.relpath(fp, root)
                if rel.startswith("..") or os.path.isabs(rel):
                    continue
            except ValueError:
                continue
            file_count += 1
            r = scan_file(fp)
            for k in ("ent_total", "ent_kept", "ent_suppressed"):
                total[k] += r[k]
            for k, v in r["allow_clauses"].items():
                total["allow_clauses"][k] += v
            total["samples"].extend(r["samples"])
            total["files_scanned"] += 1
    return total

def load_scan_history(history_dir):
    history = []
    if not os.path.isdir(history_dir): return history
    for fn in sorted(os.listdir(history_dir)):
        if not fn.endswith(".json"): continue
        fp = os.path.join(history_dir, fn)
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            history.append({"file": fn, "data": data})
        except Exception:
            pass
    return history

if __name__ == "__main__":
    ROOT = "C:/Users/foste/Documents/projects/local_sovereign_agent"
    TARGETS = ["mag", "tools", "configs", "memory", "watch", "dashboard"]
    print("=" * 60)
    print("ALLOW_RE x ENT COUNTER-LEAK BLAST RADIUS")
    print(f"Constants: ENTROPY_MIN=4.3 ENT_LEN_MIN=25")
    print(f"Scan: {TARGETS} dirs under local_sovereign_agent")
    print("=" * 60)
    r = scan_target_dirs(ROOT, TARGETS, max_files=500)
    print(f"\nfiles_scanned: {r['files_scanned']}")
    print(f"ENT tokens (25+ chars, entropy>=4.3): {r['ent_total']}")
    print(f"ENT findings KEPT: {r['ent_kept']}")
    print(f"ENT findings SUPPRESSED by ALLOW_RE: {r['ent_suppressed']}")
    if r['ent_total'] > 0:
        frac = r['ent_suppressed'] / r['ent_total']
        print(f"SUPPRESSION RATE: {frac:.4f} ({frac*100:.2f}%)")
    print(f"ALLOW_RE clause distribution: {dict(r['allow_clauses'])}")
    print(f"\nSamples:")
    for s in r["samples"][:10]:
        print(f"  clause={s['clause']} entropy={s['entropy']} "
              f"tok={s['tok']} line={s['line']}")
    print()
    print("=" * 60)
    print("SCAN HISTORY CHECK")
    history_dir = os.path.join(ROOT, "watch/inbox/secret_gate_results")
    if os.path.isdir(history_dir):
        history = load_scan_history(history_dir)
        print(f"  history files found: {len(history)}")
        for h in sorted(history, key=lambda x: x["file"])[-5:]:
            d = h["data"]
            if isinstance(d, dict):
                print(f"  {h['file']}: "
                      f"blocking={d.get('blocking_count','?')} "
                      f"entropy={d.get('entropy','?')}")
                ent = d.get("entropy")
                if isinstance(ent, dict):
                    for k, v in ent.items():
                        print(f"    entropy.{k}={v}")
    else:
        print(f"  history dir not found: {history_dir}")
        print("  OWED: cannot verify inflated counts")
    affected = r["ent_suppressed"] > 0
    print(f"\n{'=' * 60}")
    print(f"AFFECTED: {'YES' if affected else 'NO'} -- "
          f"{r['ent_suppressed']}/{r['ent_total']} entropy tokens "
          f"suppressed by ALLOW_RE")
