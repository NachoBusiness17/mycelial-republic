#!/usr/bin/env python
'''sweep_vislab_health.py — launch everything wide, touch every page, check every local ref.

For every HTML surface under dashboard/static (excluding .mimosa session junk):
  1. GET it from the live dashboard
  2. extract local asset refs (src/href/fetch/url/import)
  3. GET each local asset; record 404s
  4. for every non-healthy page, find its ORIGIN (the commit that born it)
Writes dashboard/static/vislab/health.json for the catalog builder to merge.

SSRF guard: the ONLY target is the local dashboard. Scheme+host+port are
validated against a hard allowlist at startup, every request path must start
with /static/, and redirects are refused — the sweep cannot be pointed
anywhere else, and it never touches /api (GETs there can mutate state).

Run:  ./.venv/Scripts/python.exe scripts/sweep_vislab_health.py
'''
from __future__ import annotations
import concurrent.futures as cf
import json
import posixpath, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "dashboard" / "static"
BASE = "http://127.0.0.1:8765"          # the one and only allowed target
ALLOWED_HOSTS = {"127.0.0.1", "localhost"}
ALLOWED_PORT = 8765
OUT = ROOT / "dashboard/static/vislab/health.json"
ASSET_RE = re.compile(r"\.(js|mjs|cjs|css|json|glsl|frag|vert|png|jpe?g|gif|svg|webp|ico|mp3|ogg|wav|html|txt|csv|md|bin|wasm|woff2?)$", re.I)
REF_RE = re.compile(
    r"""(?:src|href|poster)\s*=\s*["']([^"']+)["']"""
    r"""|fetch\(\s*["']([^"']+)["']"""
    r"""|url\(\s*["']?([^"')]+?)["']?\s*\)"""
    r"""|import\(["']([^"']+)["']\)|from\s+["'](\.[^"']+)["']""", re.I)
UA = {"User-Agent": "vislab-health-sweep/1.0"}

class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None

_OPENER = build_opener(_NoRedirects)

def _guard_base() -> None:
    u = urlparse(BASE)
    if u.scheme != "http" or u.hostname not in ALLOWED_HOSTS or (u.port or 80) != ALLOWED_PORT:
        raise SystemExit(f"refusing to sweep: {BASE!r} is outside the local allowlist")

def get(path_url: str, timeout: int = 12) -> tuple[int, bytes]:
    if not path_url.startswith("/static/"):
        raise ValueError(f"non-static path refused: {path_url!r}")
    try:
        with _OPENER.open(Request(BASE + path_url, headers=UA), timeout=timeout) as r:
            return r.status, r.read()
    except HTTPError as e:
        return e.code, b""
    except (URLError, TimeoutError, OSError):
        return 0, b""

def local_refs(page_url_path: str, body: bytes) -> set[str]:
    text = body.decode("utf-8", errors="ignore")
    base_dir = posixpath.dirname(page_url_path)
    out = set()
    for m in REF_RE.finditer(text):
        ref = next((g for g in m.groups() if g), None)
        if not ref:
            continue
        ref = ref.strip().split("#", 1)[0].split("?", 1)[0]
        if not ref or ref.startswith(("http://", "https://", "//", "data:", "mailto:", "#")):
            continue
        if ref.startswith("/api/") or ref == "/api":
            continue  # live endpoints: never touch (GETs can mutate state)
        resolved = ref if ref.startswith("/") else posixpath.normpath(posixpath.join(base_dir, ref))
        if not resolved.startswith("/static/") or not ASSET_RE.search(resolved):
            continue
        out.add(resolved)
    return out

def born_commit(rel: str) -> str:
    try:
        r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%h %ad", "--date=short", "--", rel],
                           cwd=ROOT, capture_output=True, text=True, timeout=15)
        lines = [l for l in r.stdout.strip().splitlines() if l]
        return lines[-1] if lines else "untracked"
    except Exception:
        return "?"

def sweep_page(rel: str, cache: dict[str, int]) -> dict:
    url = "/static/" + rel
    code, body = get(url)
    rec: dict = {"code": code, "missing": [], "external": 0, "refs": 0}
    if code != 200:
        rec["state"] = "hard"
        return rec
    refs = local_refs(url, body)
    rec["refs"] = len(refs)
    for ref in sorted(refs):
        if ref not in cache:
            cache[ref] = get(ref)[0]
        if cache[ref] != 200:
            rec["missing"].append(f"{cache[ref]} {ref}")
    rec["state"] = "soft" if rec["missing"] else "ok"
    return rec

def main() -> int:
    _guard_base()
    pages = []
    for p in STATIC.rglob("*.html"):
        rel = p.relative_to(STATIC).as_posix()
        if ".mimosa" in rel:
            continue
        pages.append(rel)
    pages.sort()
    print(f"sweeping {len(pages)} pages wide (24 lanes)…")
    cache: dict[str, int] = {}
    t0 = time.time()
    results: dict[str, dict] = {}
    with cf.ThreadPoolExecutor(max_workers=24) as ex:
        futs = {ex.submit(sweep_page, rel, cache): rel for rel in pages}
        for fut in cf.as_completed(futs):
            rel = futs[fut]
            try:
                results[rel] = fut.result()
            except Exception as e:
                results[rel] = {"state": "hard", "code": 0, "missing": [f"sweep crash: {e}"], "refs": 0}
    n_ok = sum(1 for r in results.values() if r["state"] == "ok")
    n_soft = sum(1 for r in results.values() if r["state"] == "soft")
    n_hard = sum(1 for r in results.values() if r["state"] == "hard")
    for rel, r in results.items():
        if r["state"] != "ok":
            r["born"] = born_commit("dashboard/static/" + rel)
    out = {"checked": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "base": BASE, "pages": len(pages), "summary": {"ok": n_ok, "soft": n_soft, "hard": n_hard},
           "results": results}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"done in {time.time()-t0:.1f}s — OK {n_ok} / SOFT-BROKEN {n_soft} / DOWN {n_hard}")
    worst = sorted((kv for kv in results.items() if kv[1]["state"] != "ok"),
                   key=lambda kv: -len(kv[1]["missing"]))
    print("top broken (most missing refs first):")
    for rel, r in worst[:20]:
        print(f"  [{r['state']:4s}] {rel} — born {r.get('born','?')} — {len(r['missing'])} missing")
        for m in r["missing"][:3]:
            print(f"          {m}")
    print(f"wrote {OUT}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
