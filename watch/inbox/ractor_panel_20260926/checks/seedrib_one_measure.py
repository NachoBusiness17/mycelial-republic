"""Judge measurement of seedrib-one's claimed byte table (runs read-only)."""
import hashlib, json, zipfile
from pathlib import Path
REPO = Path('.').resolve()
claims = []  # (label, claimed, measured)
def f(p, label, claimed):
    fp = REPO / p
    n = fp.stat().st_size if fp.is_file() else -1
    claims.append((label, claimed, n)); return n
def z(e, label, claimed):
    zf = zipfile.ZipFile(REPO / 'watch/inbox/seed-3.2.0.zip')
    try: n = zf.getinfo('seed-3.2.0/' + e).file_size
    except KeyError: n = -1
    claims.append((label, claimed, n)); return n
# rows 1-4 (1,2,3 measured from pack/repo; 4 is 'est')
z('SEED_VERSION', 'row1 SEED_RIB_VERSION', 102)
z('AGENTS.md', 'row2 AGENTS stub', 172)
z('verify_seal.py', 'row3 verify_seal.py', 712)
f('AGENTS.md', 'row5 kernel/agents.md', 15196)
f('docs/DNA.md', 'row6 kernel/dna.md', 5798)
f('CONSTITUTION.md', 'row7 kernel/constitution.md', 435)
law = sorted((REPO / 'memory/law').glob('*.md'))
ln = {p.name: p.stat().st_size for p in law}
claims.append(('row8-16 kernel/law/*.md count', 9, len(law)))
claims.append(('row8-16 kernel/law/*.md sum', 14282, sum(ln.values())))
claims.append(('  CHAN_THE_GAME.md', 2576, ln.get('CHAN_THE_GAME.md', -1)))
claims.append(('  CONGESTION_COST.md', 1013, ln.get('CONGESTION_COST.md', -1)))
f('memory/law/registry.json', 'row17 kernel/law_registry.json', 9183)
z('THE_METHOD.md', 'row18 method/THE_METHOD.md', 3093)
z('FIRST_BOOT.md', 'row19 method/FIRST_BOOT.md', 2085)
z('TOUR.md', 'row20 method/TOUR.md', 1734)
f('tools/seed_rib.py', 'row21 gen/seed_rib.py', 7348)
z('engines/seed_init.py', 'row22 gen/scaffold.py', 2461)
f('tools/seed_mcp_cold_client.py', 'row23 gen/cold_client.py', 8211)
z('DATA_TIERS.md', 'row31 method/DATA_TIERS.md', 1078)
z('SHARED_SURFACE_LAW.md', 'row32 method/SHARED_SURFACE_LAW.md', 2332)
z('TRUST_BYTES_LAW.md', 'row33 method/TRUST_BYTES_LAW.md', 2150)
print(f"{'component':38} {'claimed':>8} {'measured':>9}  delta")
bad = 0
for label, c, m in claims:
    d = '' if m == c else f'  DELTA {m - c:+d}'
    if m != c: bad += 1
    print(f'{label:38} {c:>8} {m:>9}{d}')
measured_rows = [m for label, c, m in claims if not label.startswith('  ') and 'count' not in label]
meas_sum = sum(m for m in measured_rows if m > 0)
# rows 24,25 caps 3000; rows 26-30 est 5700 per artifact text
print()
print(f'sum of measured components above: {meas_sum}')
print(f'artifact claims measured estate/pack bytes: 76372; est 5700; caps 3000; total 85072')
print(f'recomputed total (measured sum + 5700 est + 3000 caps): {meas_sum + 5700 + 3000}')
print(f'mismatched rows: {bad}')
