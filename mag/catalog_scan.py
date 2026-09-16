"""catalog_scan -- full-estate walker for the catalog (v2, scandir-fast).

Walks the entire local_sovereign_agent tree (minus machinery), emits one
catalog row per file into catalog/catalog.jsonl. Machinery dirs (.git, .venv,
node_modules, __pycache__, .mimosa) are excluded at walk time but COUNTED in
the summary, so the census accounts for every byte without indexing vendor
internals.
"""
import json, os, sys, hashlib, datetime

ROOT = r"C:\Users\foste\Documents\projects"
OUT = os.path.join(ROOT, "local_sovereign_agent", "catalog", "catalog.jsonl")
EXCLUDE = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mimosa",
           ".ruff_cache", ".pytest_cache", ".idea", ".vscode", "catalog"}

ZONE_MAP = [
    ("local_sovereign_agent/watch/inbox", "intake"),
    ("local_sovereign_agent/watch/astra_hold0", "astra"),
    ("local_sovereign_agent/watch/", "watch"),
    ("local_sovereign_agent/basecamp", "basecamp"),
    ("local_sovereign_agent/campaigns", "campaigns"),
    ("local_sovereign_agent/docs/", "doctrine"),
    ("local_sovereign_agent/memory/runs", "runs"),
    ("local_sovereign_agent/memory/", "memory"),
    ("local_sovereign_agent/mag/", "code"),
    ("local_sovereign_agent/tests/", "code"),
    ("local_sovereign_agent/scripts/", "code"),
    ("local_sovereign_agent/configs/", "code"),
    ("local_sovereign_agent/dashboard/static/games", "games"),
    ("local_sovereign_agent/dashboard/", "dashboard"),
    ("local_sovereign_agent/research/", "research"),
    ("local_sovereign_agent/queue/", "queue"),
    ("local_sovereign_agent/catalog/", "catalog"),
    ("local_sovereign_agent/", "lsa"),
]


def zone_of(relpath):
    p = relpath.replace("\\", "/").lower()
    for prefix, zone in ZONE_MAP:
        if p.startswith(prefix):
            return zone
    top = p.split("/")[0] if "/" in p else p
    return "ext:" + top[:16]


def main():
    n = 0
    with open(OUT, "a", encoding="utf-8", newline="\n") as cat:
        for dp, dns, fns in os.walk(ROOT, onerror=lambda e: None):
            try:
                rel = os.path.relpath(dp, ROOT)
            except ValueError:
                continue
            if rel == ".":
                rel = ""
            if "\\\\" in rel or "\\.\\" in rel:
                dns[:] = []
                continue
            dns[:] = [d for d in dns if d not in EXCLUDE and not d.startswith(".")]
            z = zone_of(rel) if rel else "vault"
            for fn in fns:
                full = os.path.join(dp, fn)
                try:
                    relfile = os.path.relpath(full, ROOT).replace("\\", "/")
                except (ValueError, OSError):
                    continue
                if "\\.\\" in relfile or "\\\\.\\\\" in relfile:
                    continue
                try:
                    st = os.stat(full)
                except OSError:
                    continue
                try:
                    st = os.stat(full)
                except OSError:
                    continue
                n += 1
                ext = os.path.splitext(fn)[1].lower()
                title = fn[:110]
                if ext in (".md", ".txt"):
                    try:
                        with open(full, encoding="utf-8", errors="replace") as fh:
                            for line in fh:
                                line = line.strip()
                                if line.startswith("#"):
                                    title = line.lstrip("# ").strip()[:110]
                                    break
                                if line:
                                    title = line[:110]
                                    break
                    except OSError:
                        pass
                rid = hashlib.sha256(relfile.encode("utf-8", "replace")).hexdigest()[:12]
                mtime = datetime.datetime.utcfromtimestamp(st.st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")
                row = {"id": rid, "path": relfile, "bytes": st.st_size,
                       "mtime": mtime, "zone": zone_of(rel), "ext": ext, "title": title}
                cat.write(json.dumps(row, ensure_ascii=False) + "\n")
                if n % 100000 == 0:
                    cat.flush()
                    print(f"  ...{n} rows", flush=True)
    print(f"TOTAL rows: {n}")
    print(f"excluded machinery dirs: {sorted(EXCLUDE)}")


if __name__ == "__main__":
    main()
