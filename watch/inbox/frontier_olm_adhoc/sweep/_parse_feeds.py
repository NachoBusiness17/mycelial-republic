"""Parse Reddit RSS Atom feeds dumped by the frontier sweep into dated candidate lists.

Seat: sweep-open-local-models-reddit (frontier_olm_adhoc), 2026-10-11.
Reads /tmp/feed_<sub>.xml for four subreddits, prints date, title, link per entry.
"""
import os
import xml.etree.ElementTree as ET
import html

NS = {'a': 'http://www.w3.org/2005/Atom'}
SUBS = ['LocalLLaMA', 'LocalLLM', 'ollama', 'MachineLearning']
TMP = os.path.expandvars(r'%LOCALAPPDATA%\Temp')

for sub in SUBS:
    path = os.path.join(TMP, f'feed_{sub}.xml')
    try:
        tree = ET.parse(path)
    except Exception as exc:
        print(f'== r/{sub}: PARSE FAIL {exc}')
        continue
    root = tree.getroot()
    upd = root.find('a:updated', NS)
    entries = root.findall('a:entry', NS)
    print(f'== r/{sub} feed_updated={upd.text if upd is not None else "?"} entries={len(entries)}')
    for entry in entries:
        title_el = entry.find('a:title', NS)
        link_el = entry.find('a:link', NS)
        upd_el = entry.find('a:updated', NS)
        title = html.unescape(title_el.text) if title_el is not None and title_el.text else '?'
        link = link_el.get('href') if link_el is not None else '?'
        date = upd_el.text[:10] if upd_el is not None and upd_el.text else '?'
        print(f'{date}\t{title}\t{link}')
    print()
