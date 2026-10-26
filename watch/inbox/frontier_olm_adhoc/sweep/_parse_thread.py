"""Dump a thread comments RSS (.rss) as readable text: original post plus comments.

Seat: sweep-open-local-models-reddit (frontier_olm_adhoc), 2026-10-11.
Usage: python _parse_thread.py <path-to-xml>
"""
import os
import re
import html
import sys
import xml.etree.ElementTree as ET

NS = {'a': 'http://www.w3.org/2005/Atom'}
TAG_RE = re.compile(r'<[^>]+>')


def strip(raw):
    txt = TAG_RE.sub(' ', raw or '')
    txt = html.unescape(txt)
    return re.sub(r'\s+', ' ', txt).strip()


path = sys.argv[1]
root = ET.parse(path).getroot()
entries = root.findall('a:entry', NS)
print(f'entries={len(entries)}')
for i, entry in enumerate(entries):
    title_el = entry.find('a:title', NS)
    author_el = entry.find('a:author/a:name', NS)
    content_el = entry.find('a:content', NS)
    upd_el = entry.find('a:updated', NS)
    title = strip(title_el.text if title_el is not None else '')
    author = author_el.text if author_el is not None else '?'
    body = strip(content_el.text if content_el is not None else '')
    date = upd_el.text[:16] if upd_el is not None and upd_el.text else '?'
    print(f'--- [{i}] {date} {author} | {title[:80]}')
    print(body[:1200])
