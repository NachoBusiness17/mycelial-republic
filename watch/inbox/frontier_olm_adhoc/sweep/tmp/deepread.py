"""Pass 2 deep read: fetch full post + comment tree for selected thread ids."""
import json
import time
import urllib.request

IDS = [
    "1wjieap",  # Jev open-source model RLCD
    "1wouby6",  # JEV almost dead: CLM vs JEV
    "1wgii3h",  # DeepSeek engineer reflections on RSI
    "1wnyf0o",  # Laya came first, why only Jev
    "1wrzoej",  # Laya typed abstention decisions
    "1wy9q9e",  # small models write tests+code, 77% rejection
    "1wuz83t",  # Qwen3.8-27B executor 6 phases
    "1x357dq",  # standard evals can't tell quants apart
    "1wjgthj",  # pre-execution gate [P]
    "1wm4wu2",  # 1000+ telemetry events 38 deployments
]
DIR = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep\tmp"
UA = {"User-Agent": "mag-frontier-sweep/1.0"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


posts = get("https://arctic-shift.photon-reddit.com/api/posts/ids?ids=" + ",".join(IDS))
with open(DIR + r"\deep_posts.json", "w", encoding="utf-8") as fh:
    json.dump(posts, fh, ensure_ascii=False, indent=1)
print(f"posts fetched: {len(posts.get('data', []))}")
time.sleep(5)

for pid in IDS:
    try:
        page = get(
            f"https://arctic-shift.photon-reddit.com/api/comments/search?link_id={pid}&limit=100"
        )
        rows = page.get("data", [])
        with open(DIR + rf"\comments_{pid}.json", "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
        print(f"{pid}: {len(rows)} comments")
    except Exception as exc:  # noqa: BLE001
        print(f"{pid}: ERR {exc}")
    time.sleep(5)
