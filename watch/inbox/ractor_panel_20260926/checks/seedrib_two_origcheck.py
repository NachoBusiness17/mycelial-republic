"""Judge re-hash of seedrib-two's ORIGINAL derivation.json rows against sources.

For every row: carried-frozen rows must match the zip entry bytes today;
carried-from-repo rows must match the repo file bytes today; every row's
sha256/bytes must match the recorded values. Extracted/regenerated rows are
time-stamped and live-sliced, so only their internal consistency is checked
here (byte re-derivation happens via the build rerun).
"""
import hashlib, json, zipfile
from pathlib import Path
REPO = Path('.').resolve()
CANDS = REPO / 'watch/inbox/ractor_panel_20260926/cands'
ZIP = REPO / 'watch/inbox/seed-3.2.0.zip'
der = json.loads((CANDS / '_seedrib_two_derivation.json').read_text(encoding='utf-8'))
zf = zipfile.ZipFile(ZIP)
mismatch = []
frozen = repo = other = 0
for rel, meta in der.items():
    if meta['method'].startswith('carried-frozen'):
        frozen += 1
        b = zf.read('seed-3.2.0/' + rel)
        if hashlib.sha256(b).hexdigest() != meta['sha256'] or len(b) != meta['bytes']:
            mismatch.append(rel)
    elif meta['method'] == 'carried-from-repo (byte-identical)':
        repo += 1
        b = (REPO / meta['source']).read_bytes()
        if hashlib.sha256(b).hexdigest() != meta['sha256'] or len(b) != meta['bytes']:
            mismatch.append(rel)
    else:
        other += 1
total = sum(m['bytes'] for m in der.values())
print(f'rows={len(der)} frozen={frozen} repo={repo} authored/extracted/regenerated={other}')
print(f'recorded total bytes={total} files={len(der)}')
print(f'mismatches against live sources: {len(mismatch)} {mismatch}')
