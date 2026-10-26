import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
DEST = ROOT / "canon" / "riddler_corpus" / "esoteric_wave"
DEST.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (mag-corpus-harvest)"}
HOSTS_OK = {"archive.org", "gutenberg.org", "www.gutenberg.org"}

def guarded_get(u, to=120):
    p = urllib.parse.urlparse(u)
    if p.scheme not in ("http", "https") or p.hostname not in HOSTS_OK:
        raise ValueError("host not allowed: " + str(p.hostname))
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=to) as r:
        return r.read()

TARGETS = [
 ("secret_doctrine_v1", "The Secret Doctrine Blavatsky"),
 ("isis_unveiled_v1", "Isis Unveiled Blavatsky volume 1"),
 ("crowley_magick", "Magick in Theory and Practice Crowley"),
 ("crowley_liber_al", "Liber AL vel Legis Crowley"),
 ("crowley_book_thoth", "The Book of Thoth Crowley"),
 ("steiner_higher_worlds", "How to Know Higher Worlds Steiner"),
 ("steiner_occult_science", "Occult Science An Outline Steiner"),
 ("pike_morals_dogma", "Morals and Dogma Pike"),
 ("duncans_ritual", "Duncan's Masonic Ritual and Monitor"),
 ("book_of_mormon", "The Book of Mormon"),
 ("rodkinson_talmud", "New Edition of the Babylonian Talmud Rodkinson"),
 ("eliphas_levi", "Transcendental Magic Levi"),
 ("dion_fortune_qabalah", "Mystical Qabalah Fortune"),
 ("blavatsky_vedas_key", "The Key to Theosophy Blavatsky"),
]

def ia_search(q):
    u = ("https://archive.org/advancedsearch.php?q=" + urllib.parse.quote(q) +
         "&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=mediatype&rows=8&output=json")
    d = json.loads(guarded_get(u, to=30))
    for x in d.get("response", {}).get("docs", []):
        if x.get("mediatype") in ("texts",):
            return x.get("identifier"), x.get("title")
    return None, None

def ia_text_file(ident):
    d = json.loads(guarded_get("https://archive.org/metadata/" + ident, to=30))
    best = None
    for x in d.get("files", []):
        n = x.get("name", "")
        f = (x.get("format") or "").lower()
        sz = int(x.get("size") or 0)
        if sz > 120 * 1024 * 1024:
            continue
        if "text" in f or n.endswith((".txt", "_djvu.txt")):
            if best is None or sz > best[1]:
                best = (n, sz)
    return best

manifest = []
for key, q in TARGETS:
    try:
        ident, title = ia_search(q)
        if not ident:
            print("MISS", key, flush=True)
            manifest.append({"key": key, "status": "no_ia_text_hit", "query": q})
            continue
        best = ia_text_file(ident)
        if not best:
            print("NOFILE", key, ident, flush=True)
            manifest.append({"key": key, "status": "no_text_file", "ident": ident})
            continue
        name, sz = best
        u = "https://archive.org/download/" + ident + "/" + urllib.parse.quote(name)
        data = guarded_get(u, to=300)
        dest = DEST / (key + "__" + name.replace("/", "_"))
        dest.write_bytes(data)
        manifest.append({"key": key, "status": "ok", "ident": ident, "title": title,
                         "file": str(dest), "bytes": len(data)})
        print("OK", key, ident, len(data), flush=True)
    except Exception as e:
        manifest.append({"key": key, "status": "error", "error": str(e)[:90]})
        print("ERR", key, str(e)[:70], flush=True)
    time.sleep(1.2)

# Gutenberg bonus: Book of Mormon pg17
try:
    data = guarded_get("https://www.gutenberg.org/cache/epub/17/pg17.txt", to=120)
    dest = DEST / "book_of_mormon__pg17.txt"
    dest.write_bytes(data)
    manifest.append({"key": "book_of_mormon_gutenberg", "status": "ok", "bytes": len(data)})
    print("OK gutenberg bom", len(data), flush=True)
except Exception as e:
    print("ERR gutenberg", str(e)[:70], flush=True)

(DEST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print("WAVE DONE", sum(1 for m in manifest if m.get("status") == "ok"), "of", len(manifest), flush=True)
