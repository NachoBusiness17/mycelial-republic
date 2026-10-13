"""audio_channel — the shadertoy audio input for PRIVLIDGE.

Reads pre-decoded WAVs of the drop zone (game_roblox/audio), measures BPM +
per-step energy curves, uploads to Roblox via Open Cloud when a key exists,
and emits src/shared/AudioManifest.luau which rojo syncs into the game.

The game (SwarmMain) reads the manifest and binds whatever landed — no
hand-pasted asset IDs, no hardcoded BPM.

Flow when a new song is dropped:
  1. bash game_roblox/audio_channel.sh      (decode + this tool)
  2. rojo pushes the regenerated manifest; Studio syncs on connect
Upload requires configs/keys.json entry:
  "roblox_opencloud": {"api_key": "...", "user_id": 123456}
Create the key at create.roblox.com/open-cloud -> API Keys with Asset write.
Without it the manifest is emitted with assetId = 0 (game stays silent) and
the next run after the key lands uploads everything pending.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception as exc:  # 2026-09-25 ratchet debt cleared: silent pass hid why emoji/BPM glyphs could mojibake on redirected stdout; valueless consoles keep default encoding, now named on stderr
    print(f"[audio_channel] stdout reconfigure skipped: {exc}", file=sys.stderr)

from mag import lite_guard  # noqa: E402
from tools.track_bpm import load_mono, onset_envelope, detect_bpm  # noqa: E402

PCM_DIR = ROOT / "state" / "fuel" / "audio_channel_pcm"
CATALOG_PCM_DIR = ROOT / "state" / "fuel" / "catalog_pcm"
MANIFEST_OUT = ROOT / "game_roblox" / "src" / "shared" / "AudioManifest.luau"
KEYS = ROOT / "configs" / "keys.json"
ENERGY_STEPS = 1024  # 8th-note steps of energy curve (~3.5 min at 122bpm)
API_BASE = "https://apis.roblox.com/assets/v1"

# Licensed catalog tracks: already live on Roblox under Roblox's official
# music publishers (APMOfficial / DistrokidOfficial) — usable in any
# experience, no upload needed. stem -> display name.
CATALOG_SEEDS = {
    "1839246734": "Euro Techno (APM)",
    "1845397447": "Technobeat (APM)",
    "1846612949": "Techno Metal A (APM)",
    "1836935697": "Test Facility (APM)",
    "1837472332": "Deep Space (APM)",
    "134434412138800": "MEGAPHONK (DK)",
    "117750981589358": "Technozen Catalog (DK)",
}


def energy_curve(onset: list[float], bpm: float) -> list[int]:
    """Aggregate the 20ms onset envelope into per-8th-note-step energy 0..255."""
    frames_per_sec = 1000.0 / 20
    step_secs = 60.0 / bpm / 2
    frames_per_step = max(1, int(round(frames_per_sec * step_secs)))
    n_steps = min(ENERGY_STEPS, len(onset) // frames_per_step)
    curve: list[int] = []
    for s in range(n_steps):
        chunk = onset[s * frames_per_step:(s + 1) * frames_per_step]
        v = sum(chunk) / len(chunk) if chunk else 0.0
        curve.append(v)
    peak = max(curve) or 1.0
    return [min(255, int(c / peak * 255)) for c in curve]


def roblox_creds() -> dict | None:
    try:
        d = json.loads(KEYS.read_text(encoding="utf-8"))
    except Exception:
        return None
    c = d.get("roblox_opencloud")
    if isinstance(c, dict) and c.get("api_key") and c.get("user_id"):
        return c
    return None


def _guarded_open(url: str, timeout: int):
    """Open a URL only after lite_guard + host pin validation."""
    if not url.startswith(API_BASE):
        raise ValueError("refusing non-API url: " + url[:100])
    if not lite_guard._safe_https_url(url):
        raise ValueError("lite_guard blocked url: " + url[:100])
    return lite_guard._OPENER.open(urllib.request.Request(url), timeout=timeout)


def upload_audio(creds: dict, path: Path) -> int:
    """Upload one track via Open Cloud assets API. Returns the asset id."""
    boundary = "PRIVLIDGEaudiochannel7d1"
    request_meta = json.dumps({
        "assetType": "Audio",
        "displayName": path.stem[:50],
        "description": "PRIVLIDGE soundtrack via estate audio channel",
        "creationContext": {"creator": {"userId": int(creds["user_id"])}},
    })
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="request"\r\n\r\n'
        f"{request_meta}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="fileContent"; filename="{path.name}"\r\n'
        f"Content-Type: audio/mpeg\r\n\r\n"
    ).encode("utf-8")
    body += path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")

    if not lite_guard._safe_https_url(API_BASE):
        raise ValueError("lite_guard blocked API base")
    req = urllib.request.Request(API_BASE + "/assets", data=body, method="POST", headers={
        "x-api-key": creds["api_key"],
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    with lite_guard._OPENER.open(req, timeout=120) as r:
        op = json.loads(r.read().decode())
    # Response is an operation; poll until done (upload + moderation)
    deadline = time.time() + 180
    while not op.get("done") and time.time() < deadline:
        time.sleep(3)
        p = op.get("path") or ""
        # Only ever poll operation paths under the pinned API base
        if not p.startswith("operations/"):
            break
        with _guarded_open(API_BASE + "/" + p, 60) as r:
            op = json.loads(r.read().decode())
    if op.get("done") and op.get("response", {}).get("assetId"):
        return int(op["response"]["assetId"])
    raise RuntimeError("upload did not complete: " + json.dumps(op)[:200])


def emit_manifest(tracks: list[dict]) -> None:
    lines = [
        "-- GENERATED by tools/audio_channel.py — do not edit by hand.",
        "-- Drop zone: game_roblox/audio/. Rerun game_roblox/audio_channel.ps1 (or .sh)",
        "-- after dropping a track; rojo pushes this into the game.",
        "-- assetId ~= 0 is playable NOW. assetId == 0 = measured, awaiting upload",
        "-- (arm uploads with roblox_opencloud in configs/keys.json).",
        "return {",
    ]
    for t in tracks:
        energy = ",".join(str(v) for v in t["energy"])
        lines.append(
            "\t{ name = %s, assetId = %d, bpm = %s, energy = {%s} },"
            % (json.dumps(t["name"]), t["assetId"], t["bpm"], energy)
        )
    lines.append("}")
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    creds = roblox_creds()
    if creds:
        print("roblox_opencloud key found: uploads enabled")
    else:
        print("no roblox_opencloud key in configs/keys.json — emitting manifest with assetId 0")

    tracks = []
    for wav in sorted(PCM_DIR.glob("*.wav")):
        stem = wav.stem
        if stem.isdigit():
            continue  # catalog-leg artifacts; they belong to CATALOG_PCM_DIR
        mp3 = Path.home() / "Desktop" / "music-ai" / (stem + ".mp3")
        source = mp3 if mp3.exists() else None
        try:
            onset = onset_envelope(load_mono(wav))
            bpm, _conf = detect_bpm(onset)
            if 0 < bpm < 90:
                bpm = round(bpm * 2, 1)  # half-time octave correction
            energy = energy_curve(onset, bpm)
            name = stem
            asset_id = 0
            if creds and source:
                try:
                    asset_id = upload_audio(creds, source)
                    print("uploaded: %s -> asset %d (%.1f BPM)" % (name[:50], asset_id, bpm))
                except Exception as e:
                    print("upload FAILED for %s: %s" % (name[:50], str(e)[:120]))
            tracks.append({"name": name, "assetId": asset_id, "bpm": bpm, "energy": energy})
            print("%-52s %6.1f BPM  %d steps of energy" % (name[:52], bpm, len(energy)), flush=True)
        except Exception as e:
            print("%-52s FAIL %s" % (stem[:52], type(e).__name__), flush=True)

    # Catalog leg: Roblox-licensed tracks measured from pre-fetched audio.
    # Their assetId IS their catalog id — playable the moment the manifest
    # lands, no upload, no key.
    for wav in sorted(CATALOG_PCM_DIR.glob("*.wav")):
        stem = wav.stem
        if stem not in CATALOG_SEEDS:
            continue
        try:
            onset = onset_envelope(load_mono(wav))
            bpm, _conf = detect_bpm(onset)
            if 0 < bpm < 90:
                bpm = round(bpm * 2, 1)
            energy = energy_curve(onset, bpm)
            tracks.append({"name": CATALOG_SEEDS[stem], "assetId": int(stem),
                           "bpm": bpm, "energy": energy, "catalog": True})
            print("[catalog] %-44s %6.1f BPM  asset %d" % (CATALOG_SEEDS[stem][:44], bpm, int(stem)), flush=True)
        except Exception as e:
            print("[catalog] %-44s FAIL %s" % (stem[:44], type(e).__name__), flush=True)

    emit_manifest(tracks)
    print(json.dumps({"tracks": len(tracks), "manifest": str(MANIFEST_OUT),
                      "uploaded": sum(1 for t in tracks if t["assetId"])}, indent=1))


if __name__ == "__main__":
    main()
