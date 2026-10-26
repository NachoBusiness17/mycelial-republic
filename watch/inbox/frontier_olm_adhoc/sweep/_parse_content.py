"""Extract post selftext (content HTML) from the four listing RSS dumps already on disk.

Seat: sweep-open-local-models-reddit (frontier_olm_adhoc), 2026-10-11.
Prints feed, title, and the text-stripped content for selected threads of interest.
"""
import os
import re
import html
import xml.etree.ElementTree as ET

NS = {'a': 'http://www.w3.org/2005/Atom'}
TMP = os.path.expandvars(r'%LOCALAPPDATA%\Temp')
WANT = [
    '1x0duco', '1x0gdc1', '1x2b9f6', '1wl13eu', '1ws6e9p', '1x0i6b5', '1wmlaqu',
]

TAG_RE = re.compile(r'<[^>]+>')


def strip(raw):
    txt = TAG_RE.sub(' ', raw or '')
    txt = html.unescape(txt)
    return re.sub(r'\s+', ' ', txt).strip()


for sub in ['LocalLLaMA', 'LocalLLM', 'ollama', 'MachineLearning']:
    path = os.path.join(TMP, f'feed_{sub}.xml')
    root = ET.parse(path).getroot()
    for entry in root.findall('a:entry', NS):
        link_el = entry.find('a:link', NS)
        link = link_el.get('href') if link_el is not None else ''
        if not any(want in link for want in WANT):
            continue
        title_el = entry.find('a:title', NS)
        content_el = entry.find('a:content', NS)
        upd_el = entry.find('a:updated', NS)
        author_el = entry.find('a:author/a:name', NS)
        print(f"### r/{sub} | {title_el.text if title_el is not None else '?'}")
        print(f"link: {link}")
        print(f"updated: {upd_el.text if upd_el is not None else '?'} author: {author_el.text if author_el is not None else '?'}")
        print(f"content: {strip(content_el.text if content_el is not None else '')[:2500]}")
        print()
