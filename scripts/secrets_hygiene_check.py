#!/usr/bin/env python3
import os, re, subprocess, sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
print(f"repo_root: {repo_root}")

candidates = [repo_root / '.env', Path.home() / 'AppData' / 'Local' / 'hermes' / '.env']

def parse_env(p):
    if not p.exists():
        return None
    keys = []
    for line in p.read_text(errors='ignore').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        k,v = line.split('=',1)
        k=k.strip(); v=v.strip()
        keys.append((k, len(v), v[-4:] if len(v)>=4 else v))
    return keys

found = {}
for p in candidates:
    keys = parse_env(p)
    if keys is not None:
        found[str(p)] = keys

print('\n.env findings:')
if not found:
    print('  none of the standard .env locations exist')
else:
    for path, keys in found.items():
        print(f'  {path}: {len(keys)} entries')
        for k,l,last4 in keys:
            print(f'    {k} — len={l} — last4={last4}')

# git ignore check
gitignore = repo_root / '.gitignore'
if gitignore.exists():
    gi = gitignore.read_text(errors='ignore')
    contains_env = any(line.strip().startswith('.env') for line in gi.splitlines())
    print(f"\n.gitignore present: {gitignore} — .env ignored: {contains_env}")
else:
    print('\n.gitignore not present')

# check if .env is tracked
def is_tracked(relpath):
    try:
        subprocess.run(['git','ls-files','--error-unmatch', relpath], cwd=str(repo_root), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

print('\nGit tracking checks:')
for p in ['.env', 'AppData/Local/hermes/.env']:
    tracked = is_tracked(p)
    print(f'  {p} tracked in git: {tracked}')

# lightweight grep for likely secrets in tracked files
print('\nScanning tracked files for API_KEY/SECRET/TOKEN/PASSWORD (git grep) — listing files with hits:')
try:
    r = subprocess.run(['git','grep','-nE','API_KEY|SECRET|TOKEN|PASSWORD'], cwd=str(repo_root), capture_output=True, text=True)
    out = r.stdout.strip()
    if not out:
        print('  no matches in tracked files')
    else:
        files = set()
        for line in out.splitlines():
            file = line.split(':',1)[0]
            files.add(file)
        for f in sorted(files):
            print('  ', f)
except Exception as e:
    print('  git grep failed:', e)

# exit status: 0 if safe (env exists and not tracked and no matches), 1 otherwise
safe = True
if found:
    # if any found and tracked -> unsafe
    for path in found:
        rel = os.path.relpath(path, start=str(repo_root))
        if is_tracked(rel):
            safe = False

# if grep found matches -> unsafe
try:
    r = subprocess.run(['git','grep','-nE','API_KEY|SECRET|TOKEN|PASSWORD'], cwd=str(repo_root), capture_output=True, text=True)
    if r.stdout.strip():
        safe = False
except Exception:
    pass

print('\nOverall verdict:')
print('  OK — secrets hygiene pass' if safe else '  FAIL — secrets hygiene issue(s) found')
sys.exit(0 if safe else 2)
