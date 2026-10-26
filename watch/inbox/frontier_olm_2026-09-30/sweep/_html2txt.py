"""Strip an arXiv HTML full-text page (LaTeXML output) to readable plain text.

Usage: python _html2txt.py <in.html> <out.txt>
Keeps section headings and paragraph breaks; drops scripts, styles, math annotations.
"""
import html
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
raw = open(src, encoding="utf-8", errors="replace").read()
raw = re.sub(r"(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>", " ", raw)
raw = re.sub(r'(?is)<math[^>]*alttext="([^"]*)".*?</math>', r" \1 ", raw)
# headings and paragraph boundaries become newlines
raw = re.sub(r"(?i)</(h[1-6]|p|div|li|section|figcaption)>", "\n", raw)
raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
raw = re.sub(r"(?s)<[^>]+>", " ", raw)
txt = html.unescape(raw)
txt = re.sub(r"[ \t]+", " ", txt)
txt = re.sub(r"\n\s*\n+", "\n\n", txt)
open(dst, "w", encoding="utf-8").write(txt.strip())
print("wrote", dst, len(txt), "chars")
