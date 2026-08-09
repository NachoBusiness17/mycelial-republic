"""steal_gdrive — yoink a link-shared Google Drive folder corpus without auth.

The trick (verified 2026-08-08):
  * Drive renders the file list of a shared folder SERVER-SIDE in the folder HTML as
    `<tr data-id="FILE_ID" data-target="TYPE" ...>`, so we can enumerate with a plain
    HTTP GET — no browser, no OAuth, no gdown.
  * Link-shared Google Docs export to plain text via
        https://docs.google.com/document/d/<ID>/export?format=txt
    and binary files via
        https://drive.google.com/uc?export=download&id=<ID>

This walks the folder tree recursively, parses IDs/types/names, downloads every
document/file, writes a manifest, and is idempotent (skips files already saved).

Usage:
  python -m tools.steal_gdrive <folder_id> --out <dir> [--depth N] [--manifest M.json]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

import httpx

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# data-target value -> (ext, download fn)
_PROGRESS_PATH: Path | None = None


def _progress(**kw) -> None:
    """Append one JSON progress line (thread-safe-ish; single walker)."""
    if _PROGRESS_PATH is None:
        return
    import json as _json
    from datetime import datetime, timezone

    rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), **kw}
    try:
        with _PROGRESS_PATH.open("a", encoding="utf-8") as fh:
            fh.write(_json.dumps(rec, default=str) + "\n")
    except OSError:
        pass


def _progress_summary(path: Path) -> str:
    """Human-readable tail of a progress file (for monitoring)."""
    if not path.is_file():
        return "no progress file yet"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    ok = sum(1 for l in lines if '"ok"' in l and '"skipped": true' not in l)
    skip = sum(1 for l in lines if '"skipped": true' in l)
    err = sum(1 for l in lines if '"error"' in l)
    return f"{len(lines)} events | ok~{ok} skip={skip} err={err}"


TYPE_EXT = {
    "doc": (".txt", "doc"),
    "document": (".txt", "doc"),
    "spreadsheet": (".csv", "sheet"),
    "sheet": (".csv", "sheet"),
    "presentation": (".txt", "slides"),
    "slides": (".txt", "slides"),
    "folder": (None, "folder"),
}
KNOWN_TYPES = ("Google Docs", "Google Sheets", "Google Slides", "Folder", "PDF")


def _fetch(url: str, timeout: float = 30.0) -> httpx.Response:
    with httpx.Client(follow_redirects=True, timeout=timeout, headers=HEADERS) as c:
        return c.get(url)


def _clean_name(label: str) -> str:
    s = html.unescape((label or "").strip())
    s = re.sub(r"\s+Shared\s*folder\s*$", "", s, flags=re.I)
    s = re.sub(r"\s+Shared\s*$", "", s)
    for t in KNOWN_TYPES:
        s = re.sub(rf"\s+{re.escape(t)}\s*$", "", s, flags=re.I)
    return s.strip()


def parse_folder(folder_id: str) -> dict:
    """Fetch one folder's HTML and return {'folder': id, 'entries': [{id,type,name}]}.

    Drive marks folders NOT by `data-target="folder"` (that value never appears);
    instead every item lives in a `JxSEve` div carrying `aria-label="<name> Shared
    folder"` + `ssk='5:<tok>:<ID>-0-16'`. Folders are detected by the label ending
    in "folder". File rows additionally carry `data-target` (doc/sheet/slides/pdf).
    """
    html = _fetch(f"https://drive.google.com/drive/folders/{folder_id}").text
    # id -> data-target for file rows
    target_map: dict[str, str] = {}
    for m in re.finditer(r'<tr[^>]*data-id="([^"]+)"[^>]*data-target="([^"]+)"', html):
        target_map.setdefault(m.group(1), m.group(2))
    # every item (file or folder): label + id from the JxSEve div
    raw: dict[str, dict] = {}
    for m in re.finditer(
        r'aria-label="([^"]+)"[^>]*data-handled-by-drag-and-drop="true"\s+ssk=\'5:[^:]*:([A-Za-z0-9_-]+)-0-16\'',
        html,
    ):
        label, fid = m.group(1), m.group(2)
        if fid not in raw:
            raw[fid] = {"label": label, "id": fid}
    entries: list[dict] = []
    for fid, info in raw.items():
        label = info["label"]
        is_folder = bool(re.search(r"folder\s*$", label, re.I))
        if is_folder:
            entries.append({"id": fid, "type": "folder", "name": _clean_name(label)})
            continue
        ftype = target_map.get(fid, "doc")
        entries.append({"id": fid, "type": ftype, "name": _clean_name(label)})
    return {"folder": folder_id, "entries": entries}


def download_entry(entry: dict, dest: Path) -> dict:
    fid, ftype, name = entry["id"], entry["type"], entry["name"]
    ext, kind = TYPE_EXT.get(ftype, (None, "file"))
    safe = "".join(c for c in name if c not in '\\/:*?"<>|').strip() or fid
    if kind == "folder":
        return {"id": fid, "kind": "folder", "name": name, "path": str(dest)}
    target = dest / (safe + (ext or ".bin"))
    if target.is_file() and target.stat().st_size > 0:
        return {"id": fid, "kind": kind, "name": name, "path": str(target), "skipped": True}
    try:
        if kind == "doc":
            r = _fetch(f"https://docs.google.com/document/d/{fid}/export?format=txt")
            if r.status_code >= 400:
                r = _fetch(f"https://drive.google.com/uc?export=download&id={fid}")
        elif kind == "sheet":
            r = _fetch(f"https://docs.google.com/spreadsheets/d/{fid}/export?format=csv")
            if r.status_code >= 400:
                r = _fetch(f"https://drive.google.com/uc?export=download&id={fid}")
        elif kind == "slides":
            r = _fetch(f"https://docs.google.com/presentation/d/{fid}/export?format=txt")
            if r.status_code >= 400:
                r = _fetch(f"https://drive.google.com/uc?export=download&id={fid}")
        else:
            r = _fetch(f"https://drive.google.com/uc?export=download&id={fid}")
        if r.status_code >= 400:
            return {"id": fid, "kind": kind, "name": name, "error": f"http {r.status_code}"}
        target.write_bytes(r.content)
        return {"id": fid, "kind": kind, "name": name, "path": str(target), "bytes": len(r.content)}
    except Exception as e:  # noqa: BLE001
        return {"id": fid, "kind": kind, "name": name, "error": str(e)}


def walk(folder_id: str, dest: Path, depth: int, max_depth: int, manifest: dict) -> None:
    if depth > max_depth:
        return
    info = parse_folder(folder_id)
    dest.mkdir(parents=True, exist_ok=True)
    _progress(event="folder", folder=folder_id, path=str(dest))
    for entry in info["entries"]:
        ftype = entry["type"]
        if ftype == "folder":
            fname = "".join(c for c in (entry["name"] or entry["id"]) if c not in '\\/:*?"<>|').strip() or entry["id"]
            sub = dest / fname
            manifest["folders"].append({"id": entry["id"], "name": entry["name"], "path": str(sub)})
            walk(entry["id"], sub, depth + 1, max_depth, manifest)
        else:
            res = download_entry(entry, dest)
            manifest["files"].append(res)
            status = "skip" if res.get("skipped") else ("ERR " + str(res.get("error")) if res.get("error") else f"ok {res.get('bytes',0)}B")
            _progress(event="file", name=entry["name"], status=status, bytes=res.get("bytes"), error=res.get("error"))
            print(f"  [{status}] {entry['name']}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder_id")
    ap.add_argument("--out", required=True)
    ap.add_argument("--depth", type=int, default=10)
    ap.add_argument("--manifest", default="")
    ap.add_argument("--progress", default="")
    args = ap.parse_args()

    out = Path(args.out)
    manifest = {"schema": "steal_gdrive.v1", "root": args.folder_id, "folders": [], "files": []}
    global _PROGRESS_PATH
    _PROGRESS_PATH = Path(args.progress) if args.progress else (out / "_progress.jsonl")
    print(f"Walking {args.folder_id} -> {out}", flush=True)
    walk(args.folder_id, out, 0, args.depth, manifest)

    mp = Path(args.manifest) if args.manifest else out / "_manifest.json"
    mp.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    n_ok = sum(1 for f in manifest["files"] if f.get("bytes"))
    n_skip = sum(1 for f in manifest["files"] if f.get("skipped"))
    n_err = sum(1 for f in manifest["files"] if f.get("error"))
    print(f"\nDONE: folders={len(manifest['folders'])} files={len(manifest['files'])} "
          f"(ok={n_ok} skip={n_skip} err={n_err}) manifest={mp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
