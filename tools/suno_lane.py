#!/usr/bin/env python
"""suno_lane - headless generation lane for the Oldest Sentence album track packs.

Parse the banked Suno packs, build payloads, submit to the SunoAPI.org gateway,
poll to SUCCESS, bank per-track receipts WITH the clip urls.

API shape grounded 2026-10-11 against docs.sunoapi.org:
  POST {BASE}/generate                      -> in-body code 200 carries data.taskId
  GET  {BASE}/generate/record-info?taskId=  -> data.status PENDING..SUCCESS; then
       data.response.sunoData[].audio_url   (mp3 links retained 14 days: fetch at once)

HTTP idiom mirrors mag/x_oauth.py (requests + Bearer + timeout). Security posture:
every url (API and clip) must be https on the allowlisted host and resolve public
before use. This tool deliberately never writes fetched bytes - receipts carry the
clip urls and the fetch runs as a visible transcript command (curl per clip), so
each byte's source stays auditable in the open (Mimosa-gated split).

Laws: operator keeps masters pick + publish nod; credits bank per track;
insufficient-credits aborts with everything-so-far banked.
"""
import argparse, datetime, ipaddress, json, os, re, socket, sys, time
import urllib.parse

import requests

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PACK = os.path.join(REPO, "watch", "inbox", "oldest_sentence_album_20261009", "TRACK_PACKS_SUNO.md")
RECEIPTS = os.path.join(REPO, "memory", "runs", "hermes_jobs", "suno_lane", "RECEIPTS.jsonl")
AUDIO_DIR = os.path.abspath(os.path.join(REPO, "watch", "inbox", "oldest_sentence_album_20261009", "audio"))
BASE = "https://apibox.erweima.ai/api/v1"
ALLOWED_HOST = "apibox.erweima.ai"
MODEL_DEFAULT = "V6"
CALLBACK_PLACEHOLDER = "https://example.invalid/suno-callback"  # we poll; callbacks unused
CJK = re.compile(r"[\u4e00-\u9fff]")

STYLE_OVERRIDES = {
    # Track 6 normalization: the auditors' wrapper came back Chinese; the lyrics
    # were English all along. Only the style line needed translation.
    "THE ONE WHO DOES NOT PLAY": "tense minimalist dark-folk litany, heartbeat percussion cycling like sonar pulses, muted guitar plucking, low sustained cello drone, soft whispered chant, long silences, 70 bpm",
}


def assert_safe_url(url):
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or u.hostname != ALLOWED_HOST:
        raise ValueError("blocked url outside allowlist: " + url[:120])
    for _fam, _typ, _proto, _canon, sa in socket.getaddrinfo(u.hostname, 443):
        ip = ipaddress.ip_address(sa[0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise ValueError("blocked allowlisted host resolving non-public: " + url[:120])


def parse_pack(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    starts = [i for i, l in enumerate(lines) if l.startswith("--- ") and l.rstrip().endswith(" ---")]
    tracks = []
    for n, s in enumerate(starts):
        e = starts[n + 1] if n + 1 < len(starts) else len(lines)
        title = lines[s].strip("- ").strip()
        style, lyrics, in_lyrics = None, [], False
        for l in lines[s:e]:
            if l.startswith("STYLE:") or l.startswith("风格："):
                style = l.split(":", 1)[-1].split("：", 1)[-1].strip()
                in_lyrics = False
                continue
            if l.startswith("LYRICS:") or l.startswith("歌词："):
                in_lyrics = True
                continue
            if l.startswith("死亡") or l.startswith("DEATHS"):
                in_lyrics = False
                continue
            if in_lyrics:
                lyrics.append(l)
        while lyrics and not lyrics[-1].strip():
            lyrics.pop()
        style = STYLE_OVERRIDES.get(title, style)
        tracks.append({"n": n + 1, "title": title, "style": style,
                       "lyrics": "\n".join(lyrics), "cjk": bool(CJK.search("\n".join(lyrics)))})
    return tracks


def api(method, url, key, body=None, timeout=60):
    assert_safe_url(url)
    headers = {"Authorization": "Bearer " + key}
    if method == "POST":
        r = requests.post(url, json=body, headers=headers, timeout=timeout)
    else:
        r = requests.get(url, headers=headers, timeout=timeout)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {"_raw": r.text[:300]}


def submit(key, t, model):
    body = {"customMode": True, "instrumental": False, "model": model,
            "title": t["title"][:80], "lyrics": t["lyrics"][:5000],
            "style": (t["style"] or "")[:1000], "callBackUrl": CALLBACK_PLACEHOLDER}
    return api("POST", BASE + "/generate", key, body)


def poll(key, task_id, max_wait=900, interval=20):
    t0 = time.time()
    terminal = {"SUCCESS", "CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED", "CALLBACK_EXCEPTION", "SENSITIVE_WORD_ERROR"}
    while time.time() - t0 < max_wait:
        status, resp = api("GET", BASE + "/generate/record-info?taskId=" + task_id, key)
        st = (resp.get("data") or {}).get("status")
        if st in terminal:
            return status, resp
        time.sleep(interval)
    return 0, {"data": {"status": "POLL_TIMEOUT"}}


def safe_clip_urls(clips):
    """Validate and return the clip urls for the receipt. Fetching is deliberately
    NOT done here: it runs as a visible transcript command per url (curl, https),
    keeping every byte's source auditable in the open (security-gate split)."""
    urls = []
    for i, c in enumerate(clips, 1):
        url = c.get("audio_url")
        if not url:
            continue
        assert_safe_url(url)
        urls.append({"clip": i, "url": url, "duration": c.get("duration")})
    return urls


def receipt(row):
    os.makedirs(os.path.dirname(RECEIPTS), exist_ok=True)
    with open(RECEIPTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=DEFAULT_PACK)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=int)
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--key-file", help="file whose first line is the API key (else env SUNO_API_KEY)")
    ap.add_argument("--model", default=MODEL_DEFAULT)
    ap.add_argument("--max-wait", type=int, default=900)
    a = ap.parse_args()

    tracks = parse_pack(a.pack)
    if a.only:
        tracks = [t for t in tracks if t["n"] == a.only]

    if a.list:
        for t in tracks:
            flag = " [CJK IN LYRICS - DO NOT FIRE]" if t["cjk"] else (" [style EN-normalized]" if t["title"] in STYLE_OVERRIDES else "")
            print("%2d. %s  (style %d ch, lyrics %d ch)%s" % (t["n"], t["title"], len(t["style"] or ""), len(t["lyrics"]), flag))
        return 0

    if a.dry_run:
        print("DRY RUN - %d payload(s) built, network NOT touched" % len(tracks))
        for t in tracks:
            assert not t["cjk"], "track %d still carries CJK lyrics - refuse to fire" % t["n"]
            print("--- %d. %s --- style %d ch | lyrics %d ch, first: %r" % (t["n"], t["title"], len(t["style"] or ""), len(t["lyrics"]), t["lyrics"].splitlines()[0]))
        return 0

    if a.generate:
        key = None
        if a.key_file and os.path.isfile(a.key_file):
            key = open(a.key_file, encoding="utf-8").read().splitlines()[0].strip()
        key = key or os.environ.get("SUNO_API_KEY")
        if not key:
            print("no key: set SUNO_API_KEY or pass --key-file")
            return 3
        print("FIRING %d track(s) on model %s" % (len(tracks), a.model))
        for t in tracks:
            t0 = time.time()
            status, resp = submit(key, t, a.model)
            code = resp.get("code") if isinstance(resp, dict) else None
            task_id = ((resp.get("data") or {}).get("taskId") if isinstance(resp, dict) else None)
            row = {"ts": datetime.datetime.utcnow().isoformat() + "Z", "track": t["n"], "title": t["title"],
                   "model": a.model, "submit_http": status, "submit_code": code, "taskId": task_id}
            if not task_id:
                row.update({"result": "SUBMIT_FAILED", "resp_head": json.dumps(resp)[:400]})
                receipt(row)
                print("  [%d] SUBMIT FAILED http=%s code=%s - banked, continuing" % (t["n"], status, code))
                continue
            print("  [%d] submitted %s, polling (max %ds)..." % (t["n"], task_id, a.max_wait))
            status, resp = poll(key, task_id, max_wait=a.max_wait)
            data = resp.get("data") or {}
            st = data.get("status")
            row["poll_status"] = st
            if st == "SUCCESS":
                clips = (data.get("response") or {}).get("sunoData") or []
                row.update({"result": "OK", "clips": safe_clip_urls(clips),
                            "elapsed_s": round(time.time() - t0, 1)})
                print("  [%d] OK - %d clip url(s) banked (%ss)" % (t["n"], len(row["clips"]), row["elapsed_s"]))
            else:
                row.update({"result": st or "UNKNOWN", "resp_head": json.dumps(resp)[:400],
                            "elapsed_s": round(time.time() - t0, 1)})
                print("  [%d] %s - banked, continuing" % (t["n"], row["result"]))
            receipt(row)
        print("lane complete; receipts:", os.path.relpath(RECEIPTS, REPO))
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
