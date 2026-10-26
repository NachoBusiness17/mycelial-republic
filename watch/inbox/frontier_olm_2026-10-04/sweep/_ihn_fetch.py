# one-shot HN sweep helper: fetch url or HN item tree to a text file (CREATE_NO_WINDOW law respected by not spawning windows)
import sys, json, urllib.request, re, html

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    return s

mode, target, out = sys.argv[1], sys.argv[2], sys.argv[3]
req = urllib.request.Request(target, headers={'User-Agent': 'Mozilla/5.0 (research sweep)'})
with urllib.request.urlopen(req, timeout=45) as r:
    raw = r.read().decode('utf-8', 'replace')
if mode == 'item':
    d = json.loads(raw)
    lines = []
    def walk(n, depth=0):
        t = strip_tags(n.get('text') or '')
        a = n.get('author') or ''
        if t.strip():
            lines.append(f"--- comment by {a} depth {depth} ---\n{t.strip()}")
        for c in n.get('children') or []:
            walk(c, depth + 1)
    lines.append(f"TITLE: {d.get('title')}")
    lines.append(f"URL: {d.get('url')}")
    lines.append(f"POINTS: {d.get('points')} CREATED: {d.get('created_at')}")
    txt = strip_tags(d.get('text') or '')
    if txt.strip():
        lines.append(f"STORY TEXT:\n{txt.strip()}")
    for c in d.get('children') or []:
        walk(c)
    body = '\n'.join(lines)
else:
    body = strip_tags(raw)
with open(out, 'w', encoding='utf-8') as f:
    f.write(body)
print(f"WROTE {out} {len(body)} chars")
