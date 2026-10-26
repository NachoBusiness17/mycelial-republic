"""Q-034 control: same prompt, NO video part. If the burn answer depended on
the video_url content part, the text-only bunny should now answer
CANNOT_VIEW_VIDEO (or refuse), not describe the clip. Shares PROMPT with
Q_034_video_probe.py by import so both wordings are byte-identical."""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from Q_034_video_probe import BASE, MODEL, PROMPT, env_key, http

OUT = Path(__file__).with_name("Q_034_control_raw.json")


def main() -> int:
    key = env_key("OPENROUTER_API_KEY") or env_key("OPENROUTER_API_KEY_2")
    payload = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": PROMPT}],
    }
    st, body, dt = http("POST", "/chat/completions", key, payload, 300)
    msg = (body.get("choices") or [{}])[0].get("message") or {}
    content = msg.get("content") or ""
    print(f"CONTROL status={st} dt={dt}s")
    if st != 200:
        print("ERROR BODY:", json.dumps(body)[:1500])
        OUT.write_text(json.dumps({"status": st, "body": body}, indent=1), encoding="utf-8")
        return 1
    print("USAGE:", json.dumps(body.get("usage", {})))
    print("CONTENT_START>>>" + content + "<<<CONTENT_END")
    OUT.write_text(json.dumps(
        {"request": {"model": MODEL, "video_part": None, "prompt": PROMPT},
         "response": {"status": st, "dt_s": dt, "usage": body.get("usage", {}),
                      "content": content}}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
