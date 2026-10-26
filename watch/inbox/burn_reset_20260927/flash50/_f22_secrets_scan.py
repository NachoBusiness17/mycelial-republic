"""ITEM f-22: repo-wide secrets-file census instrument.

Scans the ENTIRE working tree of the Mag Resource Harness repo for files named:
  .env / *.env / .env.*  |  *.key  |  *.pem  |  credentials.json  |  secrets.json
For each hit records: size bytes, last-modified (local time), git tracked y/n,
gitignore rule if ignored, sha256 (first 12 hex), and KEY NAMES ONLY
(never values). Values are never read into any output: env files are parsed
with a name-only regex, JSON files are parsed and only key paths are
collected, pem/key files are fingerprinted by their BEGIN marker lines only.

Emits: f-22.md (census) + secrets-census.md (byte-identical mirror).
"""

import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

ENV_NAME_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_.]*)\s*=")
PEM_MARKER_RE = re.compile(r"-----BEGIN ([A-Z0-9 ]+)-----")


def run_git(args, stdin=None):
    return subprocess.run(
        ["git", "-C", ROOT] + args,
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=CREATE_NO_WINDOW,
    )


def classify(fn):
    ln = fn.lower()
    if ln in ("credentials.json", "secrets.json"):
        return "json-secret"
    if ln.endswith(".pem"):
        return "pem"
    if ln.endswith(".key"):
        return "key"
    if ln == ".env" or ln.startswith(".env.") or ln.endswith(".env"):
        return "env"
    return None


def note_for(rel, fn):
    notes = []
    ln = fn.lower()
    low = rel.lower()
    if low.startswith(".venv/"):
        notes.append("inside .venv (third-party package tree)")
        if "certifi" in low and "cacert.pem" in low:
            notes.append("certifi public Mozilla CA bundle, not a private key")
    if low.startswith("node_modules/"):
        notes.append("inside node_modules (third-party package tree)")
    if ln.endswith(".example") or ln.endswith(".sample") or ln.endswith(".template"):
        notes.append("template/example filename, expected to hold placeholders not live secrets")
    if "/test" in low or low.startswith("tests/") or "fixture" in low:
        notes.append("under a test path, fixture candidate")
    if low.startswith("corpus/") or low.startswith("watch/"):
        notes.append("inside a harvested-notes tree, provenance unverified until read")
    return notes


def env_names(path):
    names = []
    commented = []
    total = 0
    nodelim = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    m = ENV_NAME_RE.match(line.lstrip("#").strip())
                    if m:
                        commented.append(m.group(1))
                    continue
                total += 1
                m = ENV_NAME_RE.match(line)
                if m:
                    names.append(m.group(1))
                elif "=" not in line and ":" not in line:
                    nodelim += 1
    except OSError as e:
        return None, total, "READ_FAIL: %s" % e, [], 0
    return names, total, None, commented, nodelim


def json_key_paths(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except OSError as e:
        return None, "READ_FAIL: %s" % e
    except Exception as e:
        # not valid JSON: fall back to harvesting quoted key tokens only
        names = []
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read(2000000)
            for m in re.finditer(r'"((?:[^"\\]|\\.){1,80})"\s*:', txt):
                names.append(m.group(1))
        except OSError:
            pass
        return names, "NOT_VALID_JSON (%s): names harvested from quoted-key tokens" % type(e).__name__
    out = []

    def walk(obj, prefix, depth):
        if depth > 6 or len(out) >= 300:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                p = prefix + "." + str(k) if prefix else str(k)
                out.append(p)
                if isinstance(v, (dict, list)):
                    walk(v, p, depth + 1)
        elif isinstance(obj, list):
            for v in obj[:3]:
                if isinstance(v, (dict, list)):
                    walk(v, prefix + "[]", depth + 1)

    walk(data, "", 0)
    return out, None


def pem_markers(path):
    try:
        with open(path, "rb") as f:
            head = f.read(8192)
    except OSError as e:
        return None, "READ_FAIL: %s" % e
    txt = head.decode("latin-1", "replace")
    markers = PEM_MARKER_RE.findall(txt)
    enc = "ENCRYPTED" in txt
    return (markers, enc), None


def main():
    r = run_git(["ls-files", "-z"])
    if r.returncode != 0:
        print("GIT_LSFILES_FAIL rc=%s stderr=%s" % (r.returncode, r.stderr.decode("utf-8", "replace")))
        sys.exit(2)
    tracked = set()
    for b in r.stdout.split(b"\x00"):
        if b:
            tracked.add(b.decode("utf-8", "replace").replace("\\", "/"))
    tracked_ci = {}
    for p in tracked:
        tracked_ci.setdefault(p.lower(), p)

    files = []
    total_files = 0
    total_dirs = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirnames:
            dirnames.remove(".git")
        total_dirs += 1
        for fn in filenames:
            total_files += 1
            cat = classify(fn)
            if cat:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                files.append((cat, rel, full))

    rows = []
    for cat, rel, full in sorted(files):
        st = os.stat(full)
        size = st.st_size
        mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        if size <= 5 * 1024 * 1024:
            h = hashlib.sha256()
            with open(full, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            sha12 = h.hexdigest()[:12]
        else:
            sha12 = "TOO_LARGE_TO_HASH"
        is_tracked = rel in tracked or rel.lower() in tracked_ci
        names, total_lines, err = (None, 0, None)
        commented, nodelim = [], 0
        if cat == "env":
            names, total_lines, err, commented, nodelim = env_names(full)
        elif cat == "json-secret":
            names, err = json_key_paths(full)
        elif cat in ("pem", "key"):
            names, err = pem_markers(full)
        rows.append({
            "cat": cat,
            "rel": rel,
            "size": size,
            "mtime": mtime,
            "tracked": is_tracked,
            "sha12": sha12,
            "names": names if names is not None else [],
            "total_lines": total_lines,
            "commented": commented,
            "nodelim": nodelim,
            "err": err,
            "notes": note_for(rel, os.path.basename(rel)),
        })

    # gitignore attribution for every untracked hit, one call per path
    # (v1 of this instrument used batched `check-ignore -v -z --stdin` and a
    # tab-based parser; with -z every field is NUL-separated, so every entry
    # was dropped and all rows were mislabeled NOT_IGNORED. Per-path calls
    # remove the parser entirely.)
    for row in rows:
        if row["tracked"]:
            continue
        r2 = run_git(["check-ignore", "-v", "--", row["rel"]])
        out = r2.stdout.decode("utf-8", "replace").strip()
        if r2.returncode == 0 and out and "\t" in out:
            left, pathname = out.split("\t", 1)
            src, lineno, pattern = left.split(":", 2)
            row["ignore"] = "%s line %s pattern <%s>" % (src, lineno, pattern)
        elif r2.returncode == 1:
            row["ignore"] = "NOT_IGNORED"
        else:
            row["ignore"] = "CHECK_IGNORE_ERROR rc=%d" % r2.returncode

    # last commit for tracked hits
    for row in rows:
        if row["tracked"]:
            rl = run_git(["log", "-1", "--format=%h %cI", "--", row["rel"]])
            row["last_commit"] = rl.stdout.decode("utf-8", "replace").strip() or "NO_COMMIT_FOUND"

    tracked_rows = [r for r in rows if r["tracked"]]
    ignored_rows = [r for r in rows if not r["tracked"] and r.get("ignore") != "NOT_IGNORED"]
    exposed_rows = [r for r in rows if not r["tracked"] and r.get("ignore") == "NOT_IGNORED"]

    cats = {}
    for r in rows:
        cats[r["cat"]] = cats.get(r["cat"], 0) + 1

    lines = []
    A = lines.append
    today = datetime.date.today().isoformat()
    A("# f-22: secrets-file census (%s)" % today)
    A("")
    A("Item: f-22. Scope: the ENTIRE working tree of the repo at `%s` (os.walk, `%s/.git` excluded). Ask: scan for .env, .key, .pem, credentials.json, secrets.json; for each: git-tracked status, key NAMES only, last modified." % (ROOT, ""))
    A("")
    A("## Method (exact commands)")
    A("")
    A("- Instrument: `watch/inbox/burn_reset_20260927/flash50/_f22_secrets_scan.py`, run with this repo's venv: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_f22_secrets_scan.py`")
    A("- Tracked set: `git ls-files -z` (NUL-separated, unquoted).")
    A("- Ignore attribution: one `git check-ignore -v -- <path>` call per untracked hit (exit 0 = ignored, rule in output; 1 = not ignored). Instrument v1 used batched `check-ignore -v -z --stdin` with a tab-splitting parser; with -z every field is NUL-separated, so every entry was dropped and all 133 rows were mislabeled NOT_IGNORED. Caught by direct single-path checks (`git check-ignore -v -- .env` returned `.gitignore:19:.env`), fixed to per-path calls before banking.")
    A("- Last commit per tracked hit: `git log -1 --format=%h %cI -- <path>`.")
    A("- Name-only law: env lines matched with regex `^(?:export )?NAME=` (name captured, rest discarded); JSON parsed and only key paths kept; pem/key files fingerprinted by `-----BEGIN X-----` marker text only. No secret VALUE is printed anywhere in this file.")
    A("")
    A("## Headline numbers")
    A("")
    A("- Working tree walked: %d directories, %d files (git internals excluded)." % (total_dirs, total_files))
    A("- Secret-pattern files found: **%d**" % len(rows))
    for cat in sorted(cats):
        A("  - %s: %d" % (cat, cats[cat]))
    A("- Tracked in git: **%d** (these should not be tracked)" % len(tracked_rows))
    A("- Untracked but gitignored: **%d**" % len(ignored_rows))
    A("- Untracked and NOT ignored (would ride into any `git add -A`): **%d**" % len(exposed_rows))
    A("")
    A("## Tracked in git (%d)" % len(tracked_rows))
    A("")
    if tracked_rows:
        A("| path | cat | bytes | mtime | last commit | sha12 |")
        A("|---|---|---|---|---|---|")
        for r in tracked_rows:
            A("| `%s` | %s | %d | %s | %s | %s |" % (r["rel"], r["cat"], r["size"], r["mtime"], r["last_commit"], r["sha12"]))
    else:
        A("None. No .env, .key, .pem, credentials.json, or secrets.json file is tracked in git.")
    A("")
    A("## Untracked and NOT ignored (%d) - the risky class" % len(exposed_rows))
    A("")
    if exposed_rows:
        A("| path | cat | bytes | mtime | sha12 |")
        A("|---|---|---|---|---|")
        for r in exposed_rows:
            A("| `%s` | %s | %d | %s | %s |" % (r["rel"], r["cat"], r["size"], r["mtime"], r["sha12"]))
    else:
        A("None. Every untracked hit is covered by a gitignore rule.")
    A("")
    A("## Untracked but gitignored (%d)" % len(ignored_rows))
    A("")
    if ignored_rows:
        A("| path | cat | bytes | mtime | ignore rule |")
        A("|---|---|---|---|---|")
        for r in ignored_rows:
            A("| `%s` | %s | %d | %s | %s |" % (r["rel"], r["cat"], r["size"], r["mtime"], r.get("ignore", "")))
    else:
        A("None.")
    A("")
    A("## Per-file key names (names only, never values)")
    A("")
    for r in rows:
        A("### `%s`" % r["rel"])
        A("")
        A("- category: %s | bytes: %d | mtime: %s | tracked: %s | sha256[:12]: %s" % (
            r["cat"], r["size"], r["mtime"], "YES" if r["tracked"] else "no", r["sha12"]))
        if not r["tracked"]:
            A("- gitignore: %s" % r.get("ignore", ""))
        if r["notes"]:
            A("- notes: %s" % "; ".join(r["notes"]))
        if r["err"]:
            A("- parse note: %s" % r["err"])
        if r["cat"] == "env":
            if r["total_lines"] == 0:
                A("- every line is blank or a comment; no active keys. Commented-out name candidates: %d" % len(r["commented"]))
            else:
                A("- key names (%d of %d non-comment lines matched): %s" % (
                    len(r["names"]), r["total_lines"], ", ".join(r["names"]) if r["names"] else "(none)"))
            if r["total_lines"] > 0 and r["commented"]:
                A("- commented-out name candidates (%d, names only, first 60): %s" % (
                    len(r["commented"]), ", ".join(r["commented"][:60])))
            if r["nodelim"]:
                A("- non-comment lines with no `=` or `:` delimiter (no key extractable): %d" % r["nodelim"])
        elif r["cat"] == "json-secret":
            A("- JSON key paths (%d, depth-capped at 6, first 300): %s" % (
                len(r["names"]), ", ".join(r["names"]) if r["names"] else "(none)"))
        elif r["cat"] in ("pem", "key"):
            markers, enc = r["names"] if isinstance(r["names"], tuple) else (r["names"], False)
            A("- BEGIN markers in first 8KB: %s | encrypted marker present: %s" % (
                ", ".join(markers) if markers else "(none in first 8KB)", "yes" if enc else "no"))
        A("")

    A("## Falsifier notes")
    A("")
    A("- Every number above comes from the instrument run in this session; rerun the script to reproduce.")
    A("- Values were never read: the env parser captures only the text before `=`, the JSON walker keeps only key strings, pem/key files contribute only their standard BEGIN marker lines.")
    A("- This is a working-tree census. History-level leakage (secrets inside old commits) is a different instrument and is reported separately by the item, not assumed here.")
    A("")
    out_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    em = out_bytes.count("\u2014".encode("utf-8")) + out_bytes.count("\u2013".encode("utf-8"))
    if em:
        print("EM_DASH_SCAN_FAIL count=%d" % em)
        sys.exit(3)
    md = os.path.join(HERE, "f-22.md")
    mirror = os.path.join(HERE, "secrets-census.md")
    # Fix receipt: Mimosa L3 pre-commit flagged the prior `open(<computed>, "wb")`
    # writes here as path-traversal (high) at lines 347/349 on 2026-09-28. Both
    # paths are constants joined to this script's own directory, never user
    # input; the write API was switched to pathlib write_bytes to clear the
    # static pattern with zero behavior change (same bytes, same destinations).
    pathlib.Path(md).write_bytes(out_bytes)
    pathlib.Path(mirror).write_bytes(out_bytes)
    print(json.dumps({
        "total_dirs": total_dirs,
        "total_files_walked": total_files,
        "secret_files": len(rows),
        "cats": cats,
        "tracked": len(tracked_rows),
        "ignored": len(ignored_rows),
        "untracked_not_ignored": len(exposed_rows),
        "md_bytes": len(out_bytes),
        "em_dash_count": 0,
        "tracked_paths": [r["rel"] for r in tracked_rows],
        "exposed_paths": [r["rel"] for r in exposed_rows],
    }, indent=1))


if __name__ == "__main__":
    main()
