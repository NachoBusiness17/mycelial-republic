import json
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
DEST = ROOT / "canon" / "riddler_corpus" / "esoteric_wave" / "open_copies"
DEST.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (mag-corpus-harvest)"}
OK_HOSTS = {"www.sacred-texts.com", "sacred-texts.com", "rsarchive.org"}

def get(u, to=45):
    p = urllib.parse.urlparse(u)
    if p.scheme != "https" or p.hostname not in OK_HOSTS:
        raise ValueError("host not allowed: " + str(p.hostname))
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=to) as r:
        return r.read().decode("utf-8", errors="replace")

def strip(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", h)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

BOOKS = {
    "pike_morals_dogma": {"base": "https://www.sacred-texts.com/mas/md/md{n:02d}.htm",
                          "chapters": list(range(1, 33))},
    "duncans_ritual": {"base": "https://www.sacred-texts.com/sro/duncan/dr{n:02d}.htm",
                       "chapters": list(range(1, 5))},
    "steiner_higher_worlds": {"base": "https://rsarchive.org/Books/GA010/English/1967/GA010_c{n:02d}.html",
                              "chapters": list(range(1, 19))},
    "crowley_magick_aba": {"base": "https://www.sacred-texts.com/oto/aba/aba{n}.htm",
                           "chapters": [1, 2, 3, 4, 5, 6, 7]},
}

manifest = {}
for key, cfg in BOOKS.items():
    parts = []
    good = 0
    for n in cfg["chapters"]:
        u = cfg["base"].format(n=n)
        try:
            h = get(u)
            t = strip(h)
            if len(t) > 800:
                parts.append("\n\n=== CHAPTER %d ===\n\n" % n + t)
                good += 1
        except Exception as e:
            print(key, n, "ERR", str(e)[:60], flush=True)
        time.sleep(0.7)
    if parts:
        dest = DEST / (key + ".txt")
        dest.write_text("\n".join(parts), encoding="utf-8")
    manifest[key] = {"chapters_ok": good, "chapters_tried": len(cfg["chapters"]),
                     "chars": sum(len(p) for p in parts)}
    print(key, "chapters ok:", good, "of", len(cfg["chapters"]), "chars:", sum(len(p) for p in parts), flush=True)

(DEST / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
print("OPEN COPIES DONE", flush=True)
