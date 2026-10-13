import re, html, sys

def extract(path):
    raw = open(path, encoding='utf-8', errors='ignore').read()
    raw = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S|re.I)
    raw = re.sub(r'<style.*?</style>', ' ', raw, flags=re.S|re.I)
    raw = re.sub(r'</t[dh]>', ' | ', raw, flags=re.I)
    raw = re.sub(r'</tr>', '\n', raw, flags=re.I)
    raw = re.sub(r'<(p|div|h1|h2|h3|h4|h5|li|br|table)[^>]*>', '\n', raw, flags=re.I)
    text = re.sub(r'<[^>]+>', '', raw)
    text = html.unescape(text)
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in text.splitlines()]
    return [l for l in lines if l]

if __name__ == '__main__':
    body = extract(sys.argv[1])
    # drop the giant nav: find the page title occurrence near "Talk" markers
    # heuristic: start after the line 'Talk (0)' or after last 'View Mobile Site' of nav; end before 'Community content is available'
    start = 0
    for i, l in enumerate(body):
        if l.startswith('Talk ('):
            start = i + 1
            break
    end = len(body)
    for i, l in enumerate(body):
        if 'Community content is available' in l:
            end = i
            break
    print('\n'.join(body[start:end]))
