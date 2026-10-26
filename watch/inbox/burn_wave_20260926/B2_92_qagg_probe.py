# B2-92 qagg card completeness sweep probe (2026-09-26)
# Verifies against bytes, never reports: (1) live status of every ok:false row
# in watch/inbox/qdrop_export/media_register_qagg.jsonl plus 200 controls,
# (2) canonical drop existence on qalerts.app for the boundary numbers,
# (3) local file existence + size + sha256-prefix match for every ok:true row.
# Laws: no fabrication; read-only network probes; no em-dashes in output.
import urllib.request
import urllib.error
import hashlib
import json
import os
import re
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REG = os.path.join(ROOT, "watch", "inbox", "qdrop_export", "media_register_qagg.jsonl")
OUT = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "B2_92_qagg_probe_results.json")
UA = {"User-Agent": "Mozilla/5.0 (B2-92 completeness sweep; read-only HEAD probes)"}


def head(url):
    req = urllib.request.Request(url, headers=UA, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return {"status": r.status, "len": r.headers.get("Content-Length")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "len": None}
    except Exception as e:  # noqa: BLE001
        return {"status": None, "err": str(e)[:120]}


def get_text(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")


def qalerts_drop(n):
    """Return the rendered post number for drop n, or None when no post renders."""
    h = get_text("https://qalerts.app/?n=%d" % n)
    m = re.search(r"No\.\s*(\d+)", h)
    nav = re.search(r"([\d,]+) Q Posts", h)
    return {"post_no": m.group(1) if m else None,
            "nav_posts_claim": nav.group(1) if nav else None}


rows = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]
bad = [r for r in rows if not r.get("ok")]
good = [r for r in rows if r.get("ok")]

print("register rows=%d ok=%d not_ok=%d" % (len(rows), len(good), len(bad)))

# 1. live probes: every failing row plus controls
probe = {}
for r in bad:
    probe[str(r["q_num"])] = head(r["url"])
    time.sleep(0.15)
for ctrl in (873, 875, 4966):
    probe["ctrl_%d" % ctrl] = head("https://qagg.news/siteimages/qaggdropimage%d.png" % ctrl)
    time.sleep(0.15)
probe["ctrl_874"] = head("https://qagg.news/siteimages/qaggdropimage874.png")

# 2. canonical existence on qalerts
qa = {}
for n in (874, 4966, 4967, 5010):
    qa[str(n)] = qalerts_drop(n)
    time.sleep(0.15)

# 3. local verification of every ok:true row (exists, size, sha256 prefix)
media_dir = os.path.join(ROOT, "watch", "inbox", "qdrop_export", "media_full")
verify = {"checked": 0, "missing": [], "size_mismatch": [], "sha_mismatch": [],
          "bytes_total": 0}
for r in good:
    p = os.path.join(ROOT, r["file"].replace("/", os.sep))
    verify["checked"] += 1
    if not os.path.exists(p):
        verify["missing"].append(r["q_num"])
        continue
    b = open(p, "rb").read()
    verify["bytes_total"] += len(b)
    if len(b) != r["bytes"]:
        verify["size_mismatch"].append(r["q_num"])
    if hashlib.sha256(b).hexdigest()[:16] != r["sha256"]:
        verify["sha_mismatch"].append(r["q_num"])
files_on_disk = len(os.listdir(media_dir))

result = {
    "when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "register_rows": len(rows),
    "ok_rows": len(good),
    "not_ok_rows": len(bad),
    "not_ok_q_nums": [r["q_num"] for r in bad],
    "probe_404_q_nums": sorted(int(k) for k, v in probe.items()
                               if k.isdigit() and v.get("status") == 404),
    "probe_other": {k: v for k, v in probe.items() if v.get("status") != 404},
    "qalerts": qa,
    "local_verify": {
        "checked": verify["checked"],
        "missing": verify["missing"],
        "size_mismatch": verify["size_mismatch"],
        "sha_mismatch": verify["sha_mismatch"],
        "bytes_total": verify["bytes_total"],
        "files_in_media_full": files_on_disk,
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=1)
print(json.dumps(result, indent=1)[:1800])
print("WROTE", OUT)
