#!/usr/bin/env python3
"""Scene-still generator for the Living Mud (and any corpus game).

Estate instrument, xAI lane: grok-imagine-image via api.x.ai.
Security posture copied from tools/research_mine.py:
  - DEEPSEEK-style guard(): host must resolve to a PUBLIC ip (no loopback,
    no private ranges) before any connection is made.
  - http.client with literal host/port args (no f-string URL objects).
  - Key read from .env only, never logged, never hardcoded.

Usage:
  python tools/stills_xai.py                 # generate all SHOTS below
  python tools/stills_xai.py threshold valves  # generate a subset by id
"""
import base64
import ipaddress
import json
import socket
import sys
import http.client
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(r"C:\Users\foste\Documents\projects\world-games-corpus\stills")
MIRROR_DIR = ROOT / "watch" / "corpus" / "stills"

HOST = "api.x.ai"
PORT = 443
MODEL = "grok-imagine-image-2.0"

STYLE = ("Dark moody video-game concept art, painterly digital illustration, "
         "deep charcoal-navy palette with teal light accents and warm gold "
         "lamplight, atmospheric haze, cinematic wide shot, high detail, "
         "no text, no words, no watermark, no logo, no UI.")

# room id -> (filename, scene prompt)
SHOTS = {
    "hero": ("hero.jpg",
             "A colossal gate of black stone standing half-open at the end of a "
             "cavern, pale water-light spilling through the gap onto a wet stone "
             "floor, a small lone figure silhouetted before it."),
    "threshold": ("threshold.jpg",
                  "A circular stone antechamber deep underground with three heavy "
                  "carved doors, each door bearing engraved plates and old knots of "
                  "cord tied around its handle, dust motes in a single shaft of "
                  "light, a hooded archivist woman with a lantern counting knots "
                  "beside the first door."),
    "rsvp": ("rsvp.jpg",
             "A doorway framed by two engraved metal face-plates mounted back to "
             "back, one plate's lettering mirrored, two round stone pressure "
             "plates set in the floor of a narrow alcove on opposite sides, "
             "candlelight."),
    "corridor": ("corridor.jpg",
                 "A long dark corridor where a single beam of light from a crack "
                 "in the west wall bounces between two brass mirrors on ornate "
                 "stands, aimed at a small glowing crystal sensor on the east "
                 "wall, an eraser-like black stone slab resting in a side alcove."),
    "valves": ("valves.jpg",
               "An ancient water-computer chamber: three carved stone tanks "
               "stepped in height, connected by open channels of flowing water, "
               "two large brass handwheels as valves, a single wooden bucket "
               "hanging from a hook, glowing depth-gauge marks etched into the "
               "lowest tank, no people."),
    "vesper": ("vesper.jpg",
               "A cramped archive room with floor-to-ceiling shelves of neatly "
               "coiled knotted cords, one guttering oil lamp on a desk with a "
               "large open ledger, a calm hooded woman tracing a cord's knots "
               "with one finger, dust and warm lamplight."),
}


def guard():
    """Refuse to connect unless HOST resolves to a public address."""
    infos = socket.getaddrinfo(HOST, PORT, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise SystemExit("guard: %s resolved to non-public %s" % (HOST, ip))


def load_key():
    for f in (ROOT / ".env", ROOT / "hermes" / ".env"):
        try:
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line.startswith("XAI_API_KEY=") and len(line) > 20:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        except OSError:
            continue
    raise SystemExit("no XAI_API_KEY found in estate .env")


def generate(key, shot_id, prompt):
    body = json.dumps({
        "model": MODEL,
        "prompt": prompt + " " + STYLE,
        "n": 1,
        "response_format": "b64_json",
    }).encode()
    conn = http.client.HTTPSConnection(HOST, PORT, timeout=180)
    try:
        conn.request("POST", "/v1/images/generations", body=body, headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Content-Length": str(len(body)),
        })
        resp = conn.getresponse()
        raw = resp.read()
        if resp.status != 200:
            return None, "HTTP %d: %s" % (resp.status, raw[:300].decode(errors="replace"))
        data = json.loads(raw)
        item = (data.get("data") or [{}])[0]
        if item.get("b64_json"):
            return base64.b64decode(item["b64_json"]), None
        if item.get("url"):
            uconn = http.client.HTTPSConnection("api.x.ai", PORT, timeout=120)
            # image urls come back on the same host; fetch via literal path
            path = item["url"].split("api.x.ai", 1)[-1] or "/"
            uconn.request("GET", path, headers={"Authorization": "Bearer " + key})
            uresp = uconn.getresponse()
            if uresp.status != 200:
                return None, "image fetch HTTP %d" % uresp.status
            return uresp.read(), None
        return None, "no image in response: %s" % raw[:200].decode(errors="replace")
    finally:
        conn.close()


def main():
    wanted = sys.argv[1:] or list(SHOTS)
    guard()
    key = load_key()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    ok, fail = 0, 0
    for shot_id in wanted:
        if shot_id not in SHOTS:
            print("skip unknown shot:", shot_id)
            continue
        fname, prompt = SHOTS[shot_id]
        print("generating %-10s ..." % shot_id, flush=True)
        try:
            img, err = generate(key, shot_id, prompt)
        except Exception as e:  # noqa: BLE001
            img, err = None, "%s: %s" % (type(e).__name__, e)
        if img:
            (OUT_DIR / fname).write_bytes(img)
            (MIRROR_DIR / fname).write_bytes(img)
            print("  ok -> stills/%s (%d bytes)" % (fname, len(img)))
            ok += 1
        else:
            print("  FAIL:", err)
            fail += 1
    print("done: %d ok, %d failed" % (ok, fail))


if __name__ == "__main__":
    main()
