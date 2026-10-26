# B2-106 close: retire the two board claims, earn the B2-106 row, self-feed
# briefs UNCHECKED at live max+1, and append the LEDGER row (json.dumps, never
# heredoc). Queue bytes are re-read at write time per the shared-file claim
# law; a foreign em-dash guard runs over everything this lane appends.
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
QUEUE = os.path.join(HERE, "QUEUE.md")
RECEIPT = "watch/inbox/burn_wave_20260926/B2_106_probe_cadence_20260926.md"
CLAIM_TS = "2026-09-26T18:57:30Z"

LANDING = (
    " Landed 2026-09-26 (spec-first docstring block, then code): weekly "
    "provider-health cadence wired into the improve scout; provider_probe_due "
    "+ run_provider_probe (mag/improve.py:398-537) gate on state key "
    "last_provider_probe vs configs/improve.yaml:299-306 provider_probe "
    ".cadence_days 7; a due scout sets MAG_PROBE_REMOTE=1 for the call "
    "(restored after, never leaks), calls doctor.check_provider_endpoints() "
    "whose triple dedupe costs one 1-token ping per unique (base_url, model, "
    "key) (11 probes over 28 providers today, not 15-28 fan-out), files "
    "memory/improve/provider_health/<day>.json + ONE candidate row (risk/new "
    "on alarms, runtime/hold on a quiet week); dry scout never probes, "
    "disabled config never probes, digest day is scrape-free not probe-free; "
    "tests 14 new in tests/test_improve_provider_probe.py, 58/58 across the "
    "four touched doctor+improve suites; live proof B2_106_cadence_live.json: "
    "first call 16.1s 11 probes (mistral now DORMANT post-B2-105 surgery, not "
    "the 403 the brief cited: the cadence exists precisely because the "
    "morning scoreboard rots same-day; new measured facts xai DOWN 400, "
    "openai DEGRADED, ollama DOWN docker-name locality trap), second call "
    "held 0.0s, in-scout gate held live, env clean; ratchet: zero NEW debt "
    "from this lane's files, the single NEW hit (mag/catalog_rescan.py "
    "file-too-long) is another lane's untracked file, not baselined; receipt "
    + RECEIPT
    + "; self-fed B2-{n1}, B2-{n2}, B2-{n3} UNCHECKED."
)

BRIEFS = [
    (
        "Provider-probe snapshots have no week-over-week differ: the cadence "
        "lands memory/improve/provider_health/<day>.json daily-when-due but "
        "nothing reads two of them together, so the exact flips the cadence "
        "exists to catch (mistral 429-zero-quota to 403-wrong-default within "
        "one day, B2-04 morning vs afternoon; mistral 403 to DORMANT after "
        "the B2-105 surgery, visible live in B2_106_cadence_live.json) have "
        "to be re-discovered by a human diffing JSON; build a small differ "
        "over the snapshot dir that prints one line per lane-status "
        "transition between the two newest snapshots (lane, old class, new "
        "class, snapshot days); falsifier: two fixture snapshots with one "
        "flipped lane must print exactly one transition naming both classes; "
        "pointers memory/improve/provider_health/ + "
        "watch/inbox/burn_wave_20260926/B2_106_cadence_live.json."
    ),
    (
        "improve --status does not surface the probe cadence: status_summary "
        "(mag/improve.py:2272-2330) returns the raw state blob where "
        "last_provider_probe is buried among keys, and last_provider_probe_"
        "summary rides along unlabeled, so at the seat you cannot tell "
        "whether the weekly lane measurement is armed or silently stale (the "
        "t33 silent-disablement disease in a new costume); add a "
        "provider_probe block to status_summary carrying last ts, "
        "cadence_days from config, and the due bool from provider_probe_due; "
        "falsifier: set state last_provider_probe to 8 days ago and "
        "status_summary()['provider_probe']['due'] must be True without any "
        "network call; pointers mag/improve.py status_summary + "
        "mag/improve.py:398-426 provider_probe_due + configs/improve.yaml "
        "provider_probe."
    ),
    (
        "Probe alarms stop at the candidates ledger: run_provider_probe "
        "(mag/improve.py:429-537) lands a kind=risk status=new row when "
        "alarm classes fire, but nothing routes it to the operator surface, "
        "so a cadence-run DOWN (today: ollama docker-name locality trap, "
        "B2_106_cadence_live.json) or QUOTA-DEAD discovered at 08:00 sits in "
        "a ranked list instead of interrupting the seat; pick ONE path and "
        "wire it: either alarm-class probe results append a [priority] line "
        "to memory/attention.md at probe time, or the row claim is fed to "
        "the existing doctor issue surface; not both (two alarm mouths is "
        "the fan-out disease); falsifier: run run_provider_probe with a "
        "fixture ALARM_RESULT and the chosen surface must gain exactly one "
        "line naming the lane and class within the same run; pointers "
        "mag/improve.py:429-537 + memory/attention.md + "
        "watch/inbox/burn_wave_20260926/B2_106_probe_cadence_20260926.md."
    ),
]


def guard(text):
    if chr(0x2014) in text:
        raise SystemExit("em-dash law violation in appended text")
    return text


def main():
    with open(QUEUE, encoding="utf-8", errors="replace") as f:
        q = f.read()

    # 1. retire both claims (CLAIM -> CLAIMED + receipt pointer)
    for path in ("watch/inbox/burn_wave_20260926/QUEUE.md", "mag/improve.py"):
        prefix = "- CLAIM B2-106 " + path + " " + CLAIM_TS
        hit = [l for l in q.splitlines() if l.startswith(prefix)]
        if len(hit) != 1:
            raise SystemExit("expected exactly one CLAIM for %s, found %d" % (path, len(hit)))
        retired = hit[0].replace("- CLAIM ", "- CLAIMED ", 1) + " -> " + RECEIPT
        q = q.replace(hit[0], guard(retired), 1)

    # 2. earn the B2-106 row (flip if still unchecked + landing note)
    hit_u = [l for l in q.splitlines() if l.startswith("- [ ] B2-106 Provider-health cadence:")]
    hit_x = [l for l in q.splitlines() if l.startswith("- [x] B2-106 Provider-health cadence:")]
    if len(hit_u) + len(hit_x) != 1:
        raise SystemExit("expected exactly one B2-106 row, found unchecked=%d checked=%d"
                         % (len(hit_u), len(hit_x)))
    pre_checked = bool(hit_x)
    row = (hit_x or hit_u)[0]
    nums = [int(m) for m in re.findall(r"B2-(\d+)", q)]
    n1, n2, n3 = max(nums) + 1, max(nums) + 2, max(nums) + 3
    landing = guard(LANDING.format(n1=n1, n2=n2, n3=n3))
    if pre_checked:
        # The row sat [x] with no receipt (the B2-222 disease): this landing
        # earns the check, and the note says so on the row itself.
        landing = guard(
            " Landed 2026-09-26; row was found PRE-CHECKED [x] with no receipt "
            "before this lane touched it (self-feed never pre-checks; this "
            "landing earns the check per the B2-222/B2-238 treatment)."
        ) + landing
    else:
        row = "- [ ]" + row[len("- [ ]"):]
    q = q.replace((hit_x or hit_u)[0], row + landing, 1)

    # 3. self-feed briefs UNCHECKED at the Open tail
    tail = "".join("\n- [ ] B2-%d %s" % (n1 + i, guard(b)) for i, b in enumerate(BRIEFS))
    if not q.endswith("\n"):
        tail = "\n" + tail
    q = q + tail + "\n"

    with open(QUEUE, "w", encoding="utf-8", newline="") as f:
        f.write(q)
    print("QUEUE closed: claims retired, B2-106 row earned, self-fed B2-%d B2-%d B2-%d" % (n1, n2, n3))

    # 4. LEDGER row
    row_json = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "slug": "B2-106-provider-probe-cadence",
        "verdict": "landed",
        "lane": "B2-106",
        "landing": RECEIPT,
        "one_line": guard(
            "Provider-health cadence landed: the first non-dry improve scout "
            "that finds last_provider_probe stale vs configs/improve.yaml "
            "cadence_days 7 runs doctor.check_provider_endpoints() under "
            "MAG_PROBE_REMOTE=1 (env set for the call and restored, triple "
            "dedupe: 11 one-token pings over 28 providers live 2026-09-26 "
            "16.1s), files memory/improve/provider_health/<day>.json + one "
            "candidate row (risk/new on alarms, runtime/hold quiet); tests "
            "14 new, 58/58 across touched doctor+improve suites; live proof "
            "second call held 0.0s and in-scout gate held with provider_"
            "probe null; live scoreboard already diverged from the morning "
            "burn wave (mistral DORMANT post-B2-105, not 403; cerebras "
            "DORMANT, not 402; new facts xai DOWN 400, openai DEGRADED, "
            "ollama DOWN docker-name locality trap), which is the brief's "
            "own thesis measured; ratchet zero NEW from this lane, the one "
            "NEW hit is another lane's untracked mag/catalog_rescan.py"),
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row_json, ensure_ascii=False) + "\n")
    print("LEDGER row appended")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
