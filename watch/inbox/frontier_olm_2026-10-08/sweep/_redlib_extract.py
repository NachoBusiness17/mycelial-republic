"""Extract readable text (post + comments) from saved redlib HTML pages."""
import html as htmllib
import re
import sys
from html.parser import HTMLParser


class TextExtract(HTMLParser):
    """Collect text from post_body and comment_body divs, with structure markers."""

    def __init__(self):
        super().__init__()
        self.depth_stack = []
        self.capture = None  # None | 'post' | 'comment' | 'title'
        self.buf = []
        self.out = []
        self.capture_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag == "h1" and "post_title" in cls:
            self.capture = "title"; self.buf = []; self.capture_depth = 0
        elif tag == "div" and "post_body" in cls.split():
            self.capture = "post"; self.buf = []; self.capture_depth = 0
        elif tag == "div" and "comment_body" in cls.split():
            self.capture = "comment"; self.buf = []; self.capture_depth = 0
        elif tag == "p" and "comment_author" in cls.split():
            self.capture = "author"; self.buf = []; self.capture_depth = 0
        if self.capture is not None and tag in ("br",):
            self.buf.append("\n")
        if self.capture is not None:
            self.capture_depth += 1

    def handle_endtag(self, tag):
        if self.capture is not None:
            self.capture_depth -= 1
            if self.capture_depth <= 0:
                text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
                if text:
                    if self.capture == "title":
                        self.out.append("TITLE: " + text)
                    elif self.capture == "post":
                        self.out.append("POST: " + text)
                    elif self.capture == "comment":
                        self.out.append("  COMMENT: " + text)
                    elif self.capture == "author":
                        self.out.append("AUTHOR: " + text)
                self.capture = None

    def handle_data(self, data):
        if self.capture is not None:
            self.buf.append(data)


def extract(fn):
    src = open(fn, encoding="utf-8").read()
    # date and score: redlib puts time in <time datetime=...> and scores in .post_score
    dates = re.findall(r'<time[^>]+datetime="([^"]+)"', src)
    scores = re.findall(r'class="post_score"[^>]*>\s*([^<]+)<', src)
    p = TextExtract()
    p.feed(src)
    head = "DATES: %s\nSCORES: %s\n" % (dates[:3], scores[:3])
    return head + "\n".join(p.out)


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        print("=" * 30, fn, "=" * 30)
        print(extract(fn))
