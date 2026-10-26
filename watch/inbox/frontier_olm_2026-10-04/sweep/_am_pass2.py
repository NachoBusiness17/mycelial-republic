import json, urllib.request, urllib.parse, os, sys, re, html

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9'}
OUT = os.path.dirname(os.path.abspath(__file__))

def get(url, binary=False, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode('utf-8', 'replace')

def item_api(oid):
    return get(f'https://hn.algolia.com/api/v1/items/{oid}')

def top_comments(oid, n=12):
    url = f'https://hn.algolia.com/api/v1/search?tags=comment,story_{oid}&hitsPerPage={n}'
    return get(url)

def strip_html(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

def fetch_page(url, oid, tag):
    """Fetch primary page, save raw bytes, return (status, text_head, saved_path)."""
    safe = re.sub(r'[^a-zA-Z0-9]+', '_', url)[:70]
    path = os.path.join(OUT, f'_am_page_{oid}_{tag}_{safe[:40]}.txt')
    try:
        raw = get(url, binary=True)
        with open(path, 'wb') as f:
            f.write(raw)
        txt = raw.decode('utf-8', 'replace')
        txt = re.sub(r'<script[^>]*>.*?</script>', ' ', txt, flags=re.S | re.I)
        txt = re.sub(r'<style[^>]*>.*?</style>', ' ', txt, flags=re.S | re.I)
        txt = strip_html(txt)
        return f'OK {len(raw)}B saved={os.path.basename(path)}', txt[:3500], path
    except Exception as e:
        return f'FAIL {type(e).__name__}: {e}', '', path

def run(oid, page_url=None, tag='p', max_comments=8):
    print('=' * 100)
    print(f'ITEM {oid}  page={page_url}')
    try:
        it = json.loads(item_api(oid))
    except Exception as e:
        print(f'  items API FAIL: {e}')
        return
    print(f"  title: {it.get('title')}")
    print(f"  author: {it.get('author')}  url: {it.get('url')}  points: {it.get('points')}")
    story_text = strip_html(it.get('text') or '')
    if story_text:
        print(f"  story text: {story_text[:1200]}")
    def walk(ch, depth=0, acc=None):
        acc = acc if acc is not None else []
        for c in ch or []:
            t = strip_html(c.get('text') or '')
            if t:
                acc.append((depth, c.get('author'), t))
            walk(c.get('children'), depth + 1, acc)
        return acc
    flat = walk(it.get('children'))
    print(f'  comment tree: {len(flat)} comments with text')
    for d, a, t in flat[:max_comments]:
        print(f'    [{"-"*d}]{a}: {t[:700]}')
    try:
        tc = json.loads(top_comments(oid))
        print('  top-voted comments (by points):')
        for h in tc.get('hits', [])[:5]:
            print(f"    {h.get('points')}p {h.get('author')}: {strip_html(h.get('comment_text'))[:500]}")
    except Exception as e:
        print(f'  comment search FAIL: {e}')
    if page_url:
        st, head, path = fetch_page(page_url, oid, tag)
        print(f'  PAGE FETCH: {st}')
        if head:
            print(f'  PAGE HEAD: {head[:3000]}')

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'batch1'
    if which == 'page':
        st, head, path = fetch_page(sys.argv[2], sys.argv[3], sys.argv[4])
        print('PAGE FETCH:', st)
        print(head[:6000])
    elif which == 'items':
        for oid in sys.argv[2:]:
            run(oid)
