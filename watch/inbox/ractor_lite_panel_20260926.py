import ipaddress
import json
import os
import re
import socket
import sys
import threading
import time
import urllib.parse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.getcwd())
from models.env_load import load_dotenv  # noqa: E402

load_dotenv()

OUT_FILE = "logs/ractor_lite_panel_20260926.jsonl"

THESIS = ("THESIS UNDER TEST (operator, from live use today): the z.ai lite/start plan lane works as the fleet's FLYWHEEL: "
 "a cheap, fast-access staff lane for flash fan-outs (wide, shallow, parallel dispatch) that owns the concurrency spread "
 "without taxing the heavy lane. Context: today we moved two starved 30-game dig veins onto the lite lane at 10-wide and they "
 "resumed from cache instantly; the heavy lane kept the deep veins; the fleet also holds Hermes/Nous credits as a second engine family, "
 "free API lanes (OpenRouter/Mistral/Cohere/DeepSeek), and offpeak gophers. Prior art in fleet canon: a retired 'flywheel' concept "
 "(speed + cheap access + router), the tier ladder (ollama -> free tiers -> flash -> pro, only judgment climbs), the sovereignty doctrine "
 "(external tools are couriers not government), and the enhance-not-bypass rule (engine output must land in an organ or it bypasses).")

SEATS = [
 ("von-neumann", "You are von Neumann's voice (minimax, game theory, stored-program architecture). Judge the lite-lane-as-flywheel thesis through your life work: is a cheap parallel lane a mixed-strategy optimum? Where does it sit in the architecture?"),
 ("ellul", "You are Jacques Ellul's voice (The Technological Society, technique absorbs everything). Judge the thesis: does a cheap fast lane become self-justifying technique? What does the flywheel absorb?"),
 ("le-guin", "You are Ursula K. Le Guin's voice (The Dispossessed, walls and boundaries). Judge the thesis: is the lite lane Anarres or Urras? What wall does it live on either side of?"),
 ("pascal", "You are Pascal's voice (the wager, divertissement). Judge the thesis: what is the fleet wagering by treating the cheap lane as staff? What is priced and what is free?"),
 ("goedel", "You are Goedel's voice (incompleteness, provability). Judge the thesis: what can the lite lane never prove about itself from inside? What enters at its unprovable edge?"),
 ("crowley", "You are Crowley's voice (The Equinox, the method of science). Judge the thesis as an experiment: what would the journal entry record, and what is the success proof?"),
 ("hall", "You are Manly P. Hall's voice (the secret teachings, initiation as curriculum). Judge the thesis: is the lite lane an initiation grade? What does a seat learn on the cheap lane before it earns the heavy lane?"),
]

ASK = (" Answer in exactly four parts: (1) VERDICT on the flywheel thesis: sound / partly-sound / unsound, one sentence why. "
 "(2) The sharpest tear at it through your lens. (3) The sharpest gift: what the fleet should DO with the insight. "
 "(4) One falsifier the fleet can measure. No em-dashes. Never fabricate: reason from the thesis text, no external claims needing sources.")

LANES = [
    {"lane": "openrouter", "base": "https://openrouter.ai/api/v1", "keys": [os.environ.get("OPENROUTER_API_KEY"), os.environ.get("OPENROUTER_API_KEY_2")], "models": ["fireworks/ember-1", "aion-labs/aion-3.5-mini", "typesafe/jev-router"]},
    {"lane": "mistral", "base": "https://api.mistral.ai/v1", "keys": [os.environ.get("MISTRAL_API_KEY"), os.environ.get("MISTRAL_API_KEY_2")], "models": ["mistral-small-latest", "magistral-small-latest"]},
    {"lane": "cohere", "base": "https://api.cohere.com/compatibility/v1", "keys": [os.environ.get("COHERE_API_KEY_FREE")], "models": ["command-a-03-2025", "command-a-plus-05-2026"]},
    {"lane": "deepseek", "base": "https://api.deepseek.com/v1", "keys": [os.environ.get("DEEPSEEK_API_KEY")], "models": ["deepseek-chat"]},
    {"lane": "nous", "base": "https://inference-api.nousresearch.com/v1", "keys": [os.environ.get("HERMES_API_KEY_1"), os.environ.get("HERMES_API_KEY_2")], "models": ["z-ai/glm-5.3-prime", "qwen/qwen3.8-max-prime"]},
]
LANES = [l for l in LANES if any(l["keys"])]
for l in LANES:
    l["keys"] = [k for k in l["keys"] if k]
HOSTS = {urllib.parse.urlparse(l["base"]).hostname for l in LANES}

print_lock = threading.Lock()


def guarded_open(req, timeout):
    parsed = urllib.parse.urlparse(req.full_url)
    if parsed.scheme != "https" or parsed.hostname not in HOSTS:
        raise ValueError("host not allowed: " + str(parsed.hostname))
    for info in socket.getaddrinfo(parsed.hostname, 443):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise ValueError("resolved to blocked address")
    return urllib.request.build_opener().open(req, timeout=timeout)


def call(lane, model, prompt, key):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 4000, "temperature": 0.6}).encode("utf-8")
    req = urllib.request.Request(lane["base"] + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with guarded_open(req, timeout=300) as r:
        return json.loads(r.read())


def run_seat(seat):
    name, persona = seat
    prompt = THESIS + "\n\nYOUR SEAT: " + persona + ASK
    for attempt in range(1, 7):
        lane = LANES[(attempt - 1) % len(LANES)]
        model = lane["models"][(attempt - 1) % len(lane["models"])]
        key = lane["keys"][(attempt - 1) % len(lane["keys"])]
        try:
            d = call(lane, model, prompt, key)
            content = d.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = d.get("usage", {})
            result = {"seat": name, "lane": lane["lane"], "model": model, "ok": True, "content": content,
                      "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens")}
            with print_lock:
                with open(OUT_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
            print("seat ok:", name, "on", lane["lane"], model, flush=True)
            return 1
        except urllib.error.HTTPError as e:
            err = "HTTP " + str(e.code)
        except Exception as e:
            err = type(e).__name__ + ": " + str(e)[:120]
        with print_lock:
            with open(OUT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"seat": name, "ok": False, "attempt": attempt,
                                    "lane": lane["lane"], "error": err}) + "\n")
        time.sleep(15 * attempt)
    print("seat FAILED all attempts:", name, flush=True)
    return 0


def main():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    print("panel seats:", len(SEATS), "lanes:", [l["lane"] for l in LANES], flush=True)
    ok = 0
    with ThreadPoolExecutor(max_workers=7) as pool:
        for res in pool.map(run_seat, SEATS):
            ok += res
    print("COMPLETE. seats ok:", ok, "/", len(SEATS), flush=True)


if __name__ == "__main__":
    main()
