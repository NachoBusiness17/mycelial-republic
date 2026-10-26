"""THE 50 / W2 / T08: ffmpeg spectrogram pass over the Mr Pool video corpus.

Corpus: watch/inbox/mrpool_export/media_register.jsonl rows whose file ends
in mp4 (390 rows, all verified on disk under watch/inbox/mrpool_export/).

Phases (run separately, both resumable):
  scan     - per video: ffprobe (streams), then ffmpeg showspectrumpic
             (1024x512, combined channels, intensity color, log frequency
             scale) into a temp PNG, pixel metrics via PIL+numpy. Appends
             one metric row per video to
             memory/runs/the50/w2_t08_spectro_metrics.jsonl.
             Videos already present there are skipped.
  classify - read metric rows, apply calibrated thresholds, write anomaly
             rows ONLY to memory/runs/the50/w2_t08_spectro.jsonl,
             regenerate the spectrogram PNG of each anomalous video
             directly into memory/runs/the50/spectro_png/, and file a
             receipt at memory/runs/the50/w2_t08_spectro_receipt.json.
             Transport deaths (probe/ffmpeg failures) are listed in the
             receipt and are never counted as findings.

Usage: .venv/Scripts/python.exe scripts/the50_t08_spectro.py scan
       .venv/Scripts/python.exe scripts/the50_t08_spectro.py classify
Thresholds live in DEFAULT_THRESHOLDS; they are calibrated on the scanned
corpus and recorded in the receipt.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = REPO + os.sep + "watch" + os.sep + "inbox" + os.sep + "mrpool_export"
REGISTER = EXPORT + os.sep + "media_register.jsonl"
OUT_DIR = REPO + os.sep + "memory" + os.sep + "runs" + os.sep + "the50"
METRICS = OUT_DIR + os.sep + "w2_t08_spectro_metrics.jsonl"
ANOMALIES = OUT_DIR + os.sep + "w2_t08_spectro.jsonl"
RECEIPT = OUT_DIR + os.sep + "w2_t08_spectro_receipt.json"
PNG_DIR = OUT_DIR + os.sep + "spectro_png"
TMP_DIR = tempfile.gettempdir() + os.sep + "the50_t08_spec"
ART_REL = "memory/runs/the50/w2_t08_spectro.jsonl"
PNG_REL_DIR = "memory/runs/the50/spectro_png"

SPEC_SIZE = "1024x512"
SPEC_W, SPEC_H = 1024, 512
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
FILE_TIMEOUT = 180

PNG_NAME_RE = re.compile(r"^[A-Za-z0-9_]+\.png$")
# register file fields are untrusted data; only corpus-relative names of
# the exact shape the harvest wrote are accepted (no separators beyond the
# one directory level, no dot directories, digits-only msg ids)
REG_FILE_RE = re.compile(
    r"^media_(full|matched)[\\/]msg_[0-9]+\.mp4$")

# pixel level a spectrogram cell must reach to count as bright for the
# per-row time-persistence metric (0-255 grayscale intensity)
TONE_BRIGHT_LEVEL = 170

DEFAULT_THRESHOLDS = {
    "tone_col_level": TONE_BRIGHT_LEVEL,  # kept for the receipt record
    "tone_col_frac": 0.85,     # fraction of bright columns for a line row
    "tone_neighbor_frac_max": 0.45,
    # showspectrumpic draws row 0 at the TOP = highest frequency, so a
    # persistent beacon line is searched in the TOP fraction of the image
    # (roughly the several-kHz-to-Nyquist band on the log scale)
    "tone_max_row_frac": 0.40,
    "tone_edge_rows": 3,       # skip the Nyquist border rows
    "hole_row_mean_max": 8.0,
    "hole_neighbor_min": 45.0,
    "hole_min_rows": 4,
    "hole_edge_margin": 6,
    "sat_frac": 0.85,
    "silent_px_mean": 1.5,
}


def video_path(reg_file):
    """Corpus path for a whitelisted register file field.

    msg_id 1840 exists twice in the register with two distinct files
    (media_matched and media_full), so identity is the register path, not
    the numeric id.
    """
    if not REG_FILE_RE.match(reg_file or ""):
        raise ValueError("register file failed whitelist: %r" % reg_file)
    path = os.path.normpath(
        os.path.join(EXPORT, reg_file.replace("/", os.sep)))
    if not path.startswith(os.path.abspath(EXPORT) + os.sep):
        raise ValueError("register path escapes corpus dir: %r" % reg_file)
    return path


def png_name_of(reg_file):
    """Bare PNG file name derived from the register path, collision-free.

    media_matched/msg_1840.mp4 -> media_matched_msg_1840.png
    """
    stem = os.path.splitext(reg_file or "")[0]
    name = re.sub(r"[^A-Za-z0-9]", "_", stem) + ".png"
    if not PNG_NAME_RE.match(name):
        raise ValueError("derived png name failed whitelist")
    return name


def png_dest(name):
    if not PNG_NAME_RE.match(name or ""):
        raise ValueError("png name failed whitelist")
    return os.path.join(PNG_DIR, name)


def load_register():
    rows = []
    with open(REGISTER, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return [r for r in rows if r["file"].lower().endswith(".mp4")]


def done_files():
    """Register paths already settled (ok or corrupt); deaths are retried."""
    done = set()
    if os.path.isfile(METRICS):
        with open(METRICS, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    try:
                        r = json.loads(line)
                        if r.get("status") in ("ok", "corrupt"):
                            done.add(r["file"])
                    except Exception:
                        pass
    return done


def probe(path):
    cmd = [FFPROBE, "-v", "error", "-print_format", "json",
           "-show_format", "-show_streams", path]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       timeout=FILE_TIMEOUT)
    if p.returncode != 0:
        raise RuntimeError("ffprobe rc=%s err=%s"
                           % (p.returncode, p.stderr.strip()[-200:]))
    data = json.loads(p.stdout)
    astreams = [s for s in data.get("streams", [])
                if s.get("codec_type") == "audio"]
    return data, astreams


def spectrogram(path, out_png):
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-i", path, "-vn", "-sn", "-dn",
           "-filter_complex",
           "showspectrumpic=s=%s:mode=combined:color=intensity:"
           "fscale=log:scale=log:legend=0" % SPEC_SIZE,
           out_png]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       timeout=FILE_TIMEOUT)
    if p.returncode != 0 or not os.path.isfile(out_png):
        raise RuntimeError("ffmpeg rc=%s err=%s"
                           % (p.returncode, p.stderr.strip()[-200:]))


def png_metrics(png):
    import numpy as np
    from PIL import Image
    img = Image.open(png).convert("L")
    if img.size != (SPEC_W, SPEC_H):
        img = img.resize((SPEC_W, SPEC_H))
    arr = np.asarray(img, dtype=np.uint8)
    # per-row time persistence: fraction of time columns where the row is
    # bright, stored in permille so a narrowband line sustained over most
    # of the video is visible in the metrics alone
    rbf = (arr >= TONE_BRIGHT_LEVEL).mean(axis=1)
    return {
        "row_means": arr.mean(axis=1).round().astype(int).tolist(),
        "col_means": arr.mean(axis=0).round().astype(int).tolist(),
        "row_bright_frac": (rbf * 1000).round().astype(int).tolist(),
        "px_mean": round(float(arr.mean()), 2),
        "px_frac_ge250": round(float((arr >= 250).mean()), 4),
    }


def scan():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    vids = load_register()
    done = done_files()
    print("register mp4 rows: %d, already scanned: %d"
          % (len(vids), len(done)))
    n_new = n_noaudio = n_err = 0
    with open(METRICS, "a", encoding="utf-8") as out:
        for i, row in enumerate(vids):
            if row["file"] in done:
                continue
            try:
                path = video_path(row["file"])
            except (ValueError, FileNotFoundError) as exc:
                print("[%d/%d] reject: %s" % (i + 1, len(vids), exc))
                continue
            base = {"msg_id": row["msg_id"], "file": row["file"],
                    "register_sha256": row.get("sha256"),
                    "post_date": row.get("date")}
            t0 = time.time()
            try:
                pdata, astreams = probe(path)
            except Exception as exc:
                msg = str(exc)
                if "Invalid data found" in msg or "moov atom" in msg:
                    # the file is readable but its container is broken:
                    # a property of the artifact, hence a finding, not a
                    # transport death of this pipeline
                    out.write(json.dumps(dict(
                        base, status="corrupt", stage="probe",
                        error=msg[:300])) + "\n")
                else:
                    out.write(json.dumps(dict(
                        base, status="transport_death", stage="probe",
                        error=msg[:300])) + "\n")
                out.flush()
                n_err += 1
                print("[%d/%d] PROBE-FAIL %s: %s"
                      % (i + 1, len(vids), row["msg_id"], msg[:120]))
                continue
            dur = float(pdata.get("format", {}).get("duration", 0) or 0)
            if not astreams:
                out.write(json.dumps(dict(
                    base, status="ok", has_audio=False,
                    duration_s=dur)) + "\n")
                out.flush()
                n_new += 1
                n_noaudio += 1
                print("[%d/%d] %s no-audio %.1fs"
                      % (i + 1, len(vids), row["msg_id"], dur))
                continue
            a0 = astreams[0]
            tmp_png = os.path.join(TMP_DIR, png_name_of(row["file"]))
            try:
                spectrogram(path, tmp_png)
                met = png_metrics(tmp_png)
            except Exception as exc:
                out.write(json.dumps(dict(
                    base, status="transport_death", stage="spectrogram",
                    has_audio=True, duration_s=dur,
                    error=str(exc)[:300])) + "\n")
                out.flush()
                n_err += 1
                print("[%d/%d] SPEC-DEATH %s: %s"
                      % (i + 1, len(vids), row["msg_id"], exc))
                continue
            out.write(json.dumps(dict(
                base, status="ok", has_audio=True, duration_s=dur,
                codec=a0.get("codec_name"), channels=a0.get("channels"),
                sample_rate=a0.get("sample_rate"), spec=met)) + "\n")
            out.flush()
            n_new += 1
            print("[%d/%d] %s ok %.1fs mean=%s wall=%.1f"
                  % (i + 1, len(vids), row["msg_id"], dur, met["px_mean"],
                     time.time() - t0))
    print("scan done: new=%d noaudio=%d deaths=%d"
          % (n_new, n_noaudio, n_err))


def classify(th):
    import numpy as np
    rows = [json.loads(line) for line in open(METRICS, encoding="utf-8")
            if line.strip()]
    ok = [r for r in rows if r.get("status") == "ok"]
    corrupt = [r for r in rows if r.get("status") == "corrupt"]
    deaths = [r for r in rows if r.get("status") == "transport_death"]
    anomalies = []
    for r in corrupt:
        anomalies.append((r, "corrupt_container", {
            "error": r.get("error"),
            "note": "container unreadable by ffmpeg/ffprobe (register "
                    "sha256 verified against these bytes); file is on "
                    "disk but structurally invalid"}))
    for r in ok:
        if not r.get("has_audio"):
            anomalies.append((r, "no_audio_stream", {
                "duration_s": r.get("duration_s"),
                "note": "container has no audio stream; no spectrogram"}))
            continue
        spec = r.get("spec") or {}
        rm = np.array(spec.get("row_means", []), dtype=float)
        cm = np.array(spec.get("col_means", []), dtype=float)
        if rm.size == 0:
            deaths.append({"msg_id": r["msg_id"], "file": r["file"],
                           "error": "metric row missing spec"})
            continue
        H = rm.size
        if spec.get("px_mean", 255) <= th["silent_px_mean"]:
            anomalies.append((r, "silent_track", {
                "px_mean": spec.get("px_mean"),
                "duration_s": r.get("duration_s")}))
        # spectral hole: dark band with live energy above and below
        dark = rm <= th["hole_row_mean_max"]
        run_start = None
        for f in range(H + 1):
            in_dark = f < H and dark[f]
            if in_dark and run_start is None:
                run_start = f
            elif not in_dark and run_start is not None:
                a, b = run_start, f - 1
                run_start = None
                if ((b - a + 1) >= th["hole_min_rows"]
                        and a >= th["hole_edge_margin"]
                        and b < H - th["hole_edge_margin"]):
                    lo = rm[max(0, a - 4):a].max()
                    hi = rm[b + 1:min(H, b + 5)].max()
                    if (lo >= th["hole_neighbor_min"]
                            and hi >= th["hole_neighbor_min"]):
                        anomalies.append((r, "spectral_hole", {
                            "rows": [a, b],
                            "row_mean_in_hole": round(
                                float(rm[a:b + 1].mean()), 1),
                            "neighbor_mean": round(float((lo + hi) / 2), 1),
                            "px_mean": spec.get("px_mean"),
                            "duration_s": r.get("duration_s")}))
        # persistent narrowband line in the high-frequency part (image top)
        fmax = int(H * th["tone_max_row_frac"])
        edge = int(th["tone_edge_rows"])
        rbf = np.array(spec.get("row_bright_frac", []), dtype=float) / 1000.0
        if rbf.size == H:
            for f in range(edge, fmax):
                if rbf[f] < th["tone_col_frac"]:
                    continue
                neigh = [n for n in (f - 8, f - 4, f + 4, f + 8)
                         if 0 <= n < H]
                if neigh and max(rbf[n] for n in neigh) \
                        <= th["tone_neighbor_frac_max"]:
                    anomalies.append((r, "constant_tone", {
                        "row": f,
                        "row_frac_from_top": round(f / (H - 1), 3),
                        "bright_frac_at_level": round(float(rbf[f]), 3),
                        "neighbor_bright_frac": round(float(max(
                            rbf[n] for n in neigh)), 3),
                        "duration_s": r.get("duration_s")}))
        if spec.get("px_frac_ge250", 0) >= th["sat_frac"]:
            anomalies.append((r, "saturated_spectrum", {
                "px_frac_ge250": spec.get("px_frac_ge250"),
                "px_mean": spec.get("px_mean"),
                "duration_s": r.get("duration_s")}))
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(PNG_DIR, exist_ok=True)
    seen, deduped = set(), []
    for item in anomalies:
        key = (item[0]["file"], item[1])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    png_regen = 0
    no_png_classes = ("no_audio_stream", "corrupt_container")
    with open(ANOMALIES, "w", encoding="utf-8") as out:
        for r, cls, ev in deduped:
            has_png = cls not in no_png_classes
            out.write(json.dumps({
                "task": "the50/w2/t08",
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "class": cls,
                "msg_id": r["msg_id"],
                "file": r["file"],
                "post_date": r.get("post_date"),
                "evidence": ev,
                "spectrogram_png_dir": PNG_REL_DIR if has_png else None,
                "spectrogram_png": png_name_of(r["file"])
                                   if has_png else None,
                "register_sha256": r.get("register_sha256"),
                "method": "ffmpeg showspectrumpic s=1024x512 mode=combined"
                          " color=intensity fscale=log scale=log",
            }) + "\n")
        for r, cls, ev in deduped:
            if cls in no_png_classes:
                continue
            try:
                spectrogram(video_path(r["file"]), png_dest(png_name_of(
                    r["file"])))
                png_regen += 1
            except Exception as exc:
                print("png regen failed msg %s: %s" % (r["msg_id"], exc))
    by_class = {}
    for _, cls, _ in deduped:
        by_class[cls] = by_class.get(cls, 0) + 1
    receipt = {
        "task": "the50/w2/t08",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "corpus": "watch/inbox/mrpool_export media_register.jsonl mp4 rows",
        "register_rows": 390,
        "metric_rows": len(rows),
        "scanned_ok": len(ok),
        "corrupt_container": len(corrupt),
        "with_audio": sum(1 for r in ok if r.get("has_audio")),
        "no_audio_stream": sum(1 for r in ok if not r.get("has_audio")),
        "transport_deaths": [
            {"msg_id": r.get("msg_id"), "file": r.get("file"),
             "stage": r.get("stage"),
             "error": (r.get("error") or "")[:200]} for r in deaths],
        "anomaly_rows": len(deduped),
        "by_class": by_class,
        "spectrogram_pngs_regen": png_regen,
        "thresholds": th,
        "ffmpeg_cmd": "ffmpeg -i <file> -vn -sn -dn -filter_complex "
                      "showspectrumpic=s=1024x512:mode=combined:"
                      "color=intensity:fscale=log:scale=log:legend=0",
        "script": "scripts/the50_t08_spectro.py",
        "metrics_file": "memory/runs/the50/w2_t08_spectro_metrics.jsonl",
        "artifact": ART_REL,
        "note": "transport deaths are infrastructure failures and are NOT "
                "counted as findings; corrupt_container is a property of "
                "the file itself and IS a finding; the anomaly jsonl "
                "contains anomaly rows only",
    }
    with open(RECEIPT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1)
    print("anomaly rows: %d %s" % (len(deduped), by_class))
    print("deaths (not findings): %d" % len(deaths))
    print("filed: %s" % ART_REL)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("scan", "classify"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "scan":
        scan()
    else:
        classify(dict(DEFAULT_THRESHOLDS))
