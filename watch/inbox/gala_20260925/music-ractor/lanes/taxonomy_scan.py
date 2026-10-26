# taxonomy_scan.py - lane: taxonomy (division B), gala music-ractor
# Mines C:/Users/foste/Desktop/music-ai (110 MP3s) with mutagen:
# per-artist counts, remix graph, original-vs-remix ratio, ID3 tag coverage,
# two-download-batch comparison. Writes raw output to taxonomy.check.txt.
import os
import re
import datetime
from collections import Counter, defaultdict

from mutagen.id3 import ID3

D = r'C:/Users/foste/Desktop/music-ai'
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'taxonomy.check.txt')

OUT = []

def P(*a):
    OUT.append(' '.join(str(x) for x in a))

files = sorted(f for f in os.listdir(D) if f.lower().endswith('.mp3'))
P(f'TOTAL MP3 FILES: {len(files)}')
P(f'SOURCE DIR: {D}')
P('')

# ---------- pass 1: read tags ----------
rows = []
for f in files:
    p = os.path.join(D, f)
    st = os.stat(p)
    batch = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d')
    rec = {'file': f, 'batch': batch, 'bytes': st.st_size}
    try:
        id3 = ID3(p)
    except Exception as e:  # noqa: BLE001 - record the failure, keep the row
        rec['error'] = repr(e)
        rows.append(rec)
        continue

    def g(fid):
        fr = id3.get(fid)
        if fr is None:
            return ''
        txt = getattr(fr, 'text', None)
        if txt:
            return str(txt[0])
        return ''

    rec['title'] = g('TIT2')
    rec['artist_raw'] = g('TPE1')
    rec['album'] = g('TALB')
    rec['date'] = g('TDRC') or g('TYER')
    rec['genre'] = g('TCON')
    rec['remixer_tag'] = g('TPE4')
    rec['cover'] = bool(id3.getall('APIC'))
    rec['frames'] = sorted(set(k.split(':')[0].split('::')[0] for k in id3.keys()))
    rows.append(rec)

# ---------- classification ----------
KIND_RE = re.compile(r'\b(remix|rework|bootleg|remaster(ed)?|radio edit|short edit|'
                     r'extended version|radio mix|straight mix|club mix|edit|mix|version)\b', re.I)
# a remix must carry a kind word; a bare ' - ' suffix alone is not a remix
EDIT_KINDS = ('radio edit', 'short edit', 'edit')
REMASTER_KINDS = ('remastered', 'remaster')
SELF_QUALIFIERS = ('straight', "someone else's")  # mix qualifiers, not remixer names
DISPLAY_FIX = {'Dfa': 'DFA'}  # tagger case, normalize for the graph only

def classify(title, artist_raw):
    """Return (cls, remixer, original) parsed from title suffix + TPE1 parts."""
    t = title
    parts = [s.strip() for s in artist_raw.split(',')] if artist_raw else []
    original = parts[0] if parts else t
    # candidate suffixes: after the last ' - ', and inside a trailing (...) group
    candidates = []
    if ' - ' in t:
        base, suffix = t.rsplit(' - ', 1)
        candidates.append(suffix)
    m = re.search(r'\(([^()]*)\)\s*$', t)
    if m:
        candidates.append(m.group(1))
    for suffix in candidates:
        # spotdown tagger truncates: 'Justice Remi' = 'Justice Remix'
        sfix = re.sub(r'\bRemi\s*$', 'Remix', suffix.strip(), flags=re.I)
        # VS form is its own marker, independent of the kind-word gate
        if re.search(r'\bvs\.?\b', sfix, re.I):
            left, right = re.split(r'\bvs\.?\b', sfix, flags=re.I)
            return ('VS', left.strip(), right.strip())
        km = KIND_RE.search(sfix)
        if not km:
            continue
        kind = km.group(1).lower()
        name = KIND_RE.sub('', sfix)
        name = re.sub(r'\s*\b(remix(ed)?|rework|bootleg)\b\s*', ' ', name, flags=re.I)
        name = re.sub(r'\s+\b(' + '|'.join(SELF_QUALIFIERS) + r')\s*$', ' ', name, flags=re.I)
        name = re.sub(r'\s+', ' ', name).strip(' -')
        if name.lower() in SELF_QUALIFIERS:
            name = ''
        remixer = DISPLAY_FIX.get(name, name)
        # cross-check against TPE1: parts NOT in the suffix are the original artist
        if len(parts) > 1:
            leftover = [x for x in parts if x.lower() not in suffix.lower()]
            if leftover:
                original = ', '.join(leftover)
        if kind in REMASTER_KINDS:
            return ('REMASTER', '', original)
        if kind in EDIT_KINDS or kind in ('radio mix', 'straight mix', 'club mix', 'version',
                                          'extended version'):
            if remixer and original and remixer.lower() != original.lower():
                return ('EDIT', remixer, original)  # a named artist's edit (e.g. Bangalter Short Edit)
            return ('VERSION', '', original)  # self radio edit / extended version
        # plain 'remix'
        if remixer and original and remixer.lower() == original.lower():
            return ('SELF-REMIX', remixer, original)
        return ('REMIX', remixer, original)
    return ('ORIGINAL', '', original)

for r in rows:
    if 'error' in r:
        r['cls'], r['remixer'], r['original'] = 'ERROR', '', ''
        continue
    r['cls'], r['remixer'], r['original'] = classify(r['title'], r['artist_raw'])

# ---------- tag coverage ----------
P('=' * 78)
P('ID3 TAG COVERAGE (n=%d)' % len(rows))
P('=' * 78)
fields = ['title (TIT2)', 'artist (TPE1)', 'album (TALB)', 'date (TDRC/TYER)',
          'genre (TCON)', 'remixer frame (TPE4)', 'cover art (APIC)']
keymap = {
    'title (TIT2)': lambda r: r.get('title', ''),
    'artist (TPE1)': lambda r: r.get('artist_raw', ''),
    'album (TALB)': lambda r: r.get('album', ''),
    'date (TDRC/TYER)': lambda r: r.get('date', ''),
    'genre (TCON)': lambda r: r.get('genre', ''),
    'remixer frame (TPE4)': lambda r: r.get('remixer_tag', ''),
    'cover art (APIC)': lambda r: 'yes' if r.get('cover') else '',
}
for fld in fields:
    fn = keymap[fld]
    n = sum(1 for r in rows if fn(r))
    P(f'  {fld:<24} {n:>4}/{len(rows)}  ({100.0*n/len(rows):.1f}%)')
frame_counts = Counter()
for r in rows:
    for fr in r.get('frames', []):
        frame_counts[fr] += 1
P('')
P('FRAME TYPE INVENTORY (files containing each frame):')
for fr, n in frame_counts.most_common():
    P(f'  {fr:<8} {n:>4}/{len(rows)}')
errs = [r for r in rows if 'error' in r]
P(f'  unreadable files: {len(errs)}')
for r in errs:
    P(f"    {r['file']}: {r['error']}")
P('')

# ---------- per-artist counts ----------
P('=' * 78)
P('PER-ARTIST COUNTS (primary/original artist from TPE1)')
P('=' * 78)
artist_n = Counter(r['original'] or '(unknown)' for r in rows)
remixer_n = Counter(r['remixer'] for r in rows if r['remixer'])
for a, n in artist_n.most_common():
    P(f'  {a:<34} {n:>3}')
P('')
P('REMIXER APPEARANCES (as remixer credit):')
for a, n in remixer_n.most_common():
    P(f'  {a:<34} {n:>3}')
P('')

# ---------- full table ----------
P('=' * 78)
P('FULL TABLE (file | batch | class | original artist | remixer | title | album)')
P('=' * 78)
for r in rows:
    P(f"  {r['file']}")
    P(f"      batch={r['batch']} class={r['cls']:<11} artist={r.get('artist_raw','')!r} "
      f"orig={r['original']!r} remixer={r['remixer']!r}")
    P(f"      title={r.get('title','')!r} album={r.get('album','')!r} date={r.get('date','')!r}")
P('')

# ---------- remix graph ----------
P('=' * 78)
P('REMIX GRAPH (who remixed whom)')
P('=' * 78)
graph = defaultdict(list)
for r in rows:
    if r['cls'] in ('REMIX', 'VS', 'EDIT', 'SELF-REMIX') and r['remixer']:
        graph[r['remixer']].append((r['original'], r['cls'], r['title']))
for remixer in sorted(graph, key=lambda k: (-len(graph[k]), k.lower())):
    P(f'  {remixer}  ({len(graph[remixer])} credits)')
    for orig, cls, title in sorted(graph[remixer]):
        P(f'      -> {orig}  [{cls}]  "{title}"')
P('')

# ---------- ratios ----------
P('=' * 78)
P('ORIGINAL VS REMIX RATIO')
P('=' * 78)
cls_n = Counter(r['cls'] for r in rows)
total = len(rows)
for c in ('ORIGINAL', 'REMIX', 'VS', 'EDIT', 'SELF-REMIX', 'VERSION', 'REMASTER', 'ERROR'):
    n = cls_n.get(c, 0)
    P(f'  {c:<12} {n:>4}  ({100.0*n/total:.1f}%)')
alt = cls_n.get('REMIX', 0) + cls_n.get('VS', 0) + cls_n.get('EDIT', 0)
P(f'  remix-class total (REMIX+VS+EDIT): {alt}/{total} = {100.0*alt/total:.1f}%')
P('')

# ---------- batch comparison ----------
P('=' * 78)
P('TWO DOWNLOAD BATCHES (by file mtime)')
P('=' * 78)
batches = sorted(set(r['batch'] for r in rows))
byb = {b: [r for r in rows if r['batch'] == b] for b in batches}
for b in batches:
    rs = byb[b]
    an = Counter(r['original'] or '(unknown)' for r in rs)
    xn = sum(1 for r in rs if r['cls'] in ('REMIX', 'VS', 'EDIT'))
    P(f'  BATCH {b}: {len(rs)} files, {len(an)} unique artists, remix-class share (REMIX+VS+EDIT) {xn}/{len(rs)} ({100.0*xn/len(rs):.1f}%)')
    P('    artists: ' + '; '.join(f'{a} x{n}' for a, n in an.most_common()))
def q(name):
    return f'"{name}"' if ',' in name else name

first = set(r['original'] for r in byb[batches[0]])
second = set(r['original'] for r in byb[batches[1]])
P('')
P(f'  artists only in batch 1 ({batches[0]}): ' + (', '.join(q(a) for a in sorted(first - second)) if first - second else '(none)'))
P(f'  artists only in batch 2 ({batches[1]}): ' + (', '.join(q(a) for a in sorted(second - first)) if second - first else '(none)'))
shared = sorted(first & second)
P(f'  artists in both batches: ' + (', '.join(shared) if shared else '(none)'))
# remix-class delta
for b in batches:
    rs = byb[b]
    cls_n_b = Counter(r['cls'] for r in rs)
    P(f'  batch {b} classes: ' + ', '.join(f'{k}={v}' for k, v in sorted(cls_n_b.items())))
P('')
P('=' * 78)
P('SELF-VERIFY')
P('=' * 78)
artist_sum = sum(artist_n.values())
cls_sum = sum(cls_n.values())
graph_edges = sum(len(v) for v in graph.values())
remix_rows = sum(1 for r in rows if r['cls'] in ('REMIX', 'VS', 'EDIT', 'SELF-REMIX') and r['remixer'])
P(f'  per-artist count sum = {artist_sum} (expect {len(rows)})')
P(f'  class-count sum = {cls_sum} (expect {len(rows)})')
P(f'  graph edges = {graph_edges} (expect {remix_rows})')
P(f'  table rows printed = {len(rows)}; dir mp3 count = {len(files)}')
ok = artist_sum == len(rows) == cls_sum and graph_edges == remix_rows and len(rows) == len(files)
P(f'  VERIFY: {"PASS" if ok else "FAIL"}')
P('')
P('END OF SCAN')

with open(OUT_PATH, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(OUT) + '\n')
print('wrote', OUT_PATH, len(OUT), 'lines')
