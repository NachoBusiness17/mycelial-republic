# B2-105 close: retire the board claim, earn the pre-checked row, self-feed
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
RECEIPT = "watch/inbox/burn_wave_20260926/B2_105_mistral_surgery_20260926.md"
CLAIM_TS = "2026-09-26T18:45:16Z"

LANDING = (
    " Landed 2026-09-26 (row sat pre-checked [x] with no receipt, the B2-238 "
    "disease; this landing earns the check): both arms of the brief were "
    "already on disk from earlier lanes, verified against live bytes and one "
    "live call per id (B2_105_verify.py + B2_105_verify_results.json): the "
    "repoint arm landed in B2-61 (configs/providers.yaml:545 default_model "
    "mistral-small-latest, :542 dormant, routing lists mistral-free at "
    ":715-726) and the nameplate arm landed in B2-21 (mag/doctor.py:65 plus "
    ":333-342 zero-limit class named for the B2-04 mistral shape); live "
    "contrast 2026-09-26: mistral-small-latest 429 x-ratelimit-limit-req-minute "
    "0 code 1300 (the B2-04 zero-quota shape, byte-matches B2-61) vs "
    "mistral-large-latest still 403 tier_not_allowed code 1910, so the 403 "
    "rode the old default id and the surgery moved the default off it; doctor "
    "default path reads mistral DORMANT probe none(dormant), zero issues; "
    "estate load_providers 28 providers reads the same fields; the brief's own "
    "pointer configs/providers.yaml:473-488 was stale (post-B2-61 that range "
    "is the z_ai3/z_ai4 region, the mistral block lives at 525-553), recovered "
    "by grep and self-fed forward; zero configs/, mag/, tools/ or tests/ bytes "
    "touched by this lane; receipt " + RECEIPT + "; self-fed B2-{n1}, B2-{n2} "
    "UNCHECKED."
)

BRIEFS = [
    (
        "Burn-era line-number pointers rot same-day: B2-105's own brief cited "
        "configs/providers.yaml:473-488 for the mistral block, but B2-61's "
        "same-day roster edits moved the block to 525-553 and the cited range "
        "now names the z_ai3/z_ai4 region (B2_105_mistral_surgery_20260926.md); "
        "this lane recovered by grep, but other Open rows citing providers.yaml "
        "or other hot config line numbers may aim at moved bytes; sweep the "
        "Open section for line-number pointers into files edited during this "
        "burn wave, re-verify each target by string anchor, and re-point the "
        "drifted ones with dated annotations; falsifier: an Open row whose "
        "cited lines name a different symbol than the brief's subject; "
        "pointers watch/inbox/burn_wave_20260926/QUEUE.md Open section + "
        "configs/providers.yaml."
    ),
    (
        "Doctor class map has no 403 arm: _classify_chat_failure "
        "(mag/doctor.py:310-352) arms 402/410/401/429 but a 403 "
        "tier_not_allowed, the exact mistral-large-latest shape that spawned "
        "B2-105 (live 2026-09-26: 403 code 1910 'This model is not available "
        "in your subscription tier', B2_105_verify_results.json), falls to the "
        "generic DOWN catch-all, so a dormant-fence removal or a stale default "
        "re-add would alarm as an outage instead of the per-key tier fact it "
        "is; add a measured 403 arm fixture-first (tests/"
        "test_doctor_provider_endpoints.py pattern) with the mistral-large "
        "body as the defining byte and decide the class (AUTH-DEAD semantics: "
        "the key lists the catalog, cannot call the model, waiting never "
        "fixes it); falsifier: a MAG_PROBE_REMOTE=1 probe of a lane whose "
        "default 403s reads DOWN instead of the new class; pointers "
        "mag/doctor.py:310-352 + tests/test_doctor_provider_endpoints.py + "
        "watch/inbox/burn_wave_20260926/B2_105_verify_results.json."
    ),
]


def guard(text):
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in appended text")
    return text


def main():
    with open(QUEUE, encoding="utf-8", errors="replace") as f:
        q = f.read()

    # 1. retire the claim (CLAIM -> CLAIMED + receipt pointer)
    claim_line = None
    for line in q.splitlines():
        if line.startswith("- CLAIM B2-105 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS):
            claim_line = line
            break
    if claim_line is None:
        raise SystemExit("own CLAIM line not found on fresh bytes; rebase needed")
    retired = claim_line.replace("- CLAIM ", "- CLAIMED ", 1) + " -> " + RECEIPT
    q = q.replace(claim_line, guard(retired), 1)

    # 2. earn the pre-checked B2-105 row (append landing note to the row line)
    row_prefix = "- [x] B2-105 Mistral lane surgery:"
    hit = [l for l in q.splitlines() if l.startswith(row_prefix)]
    if len(hit) != 1:
        raise SystemExit("expected exactly one B2-105 row, found %d" % len(hit))
    nums = [int(m) for m in re.findall(r"B2-(\d+)", q)]
    n1, n2 = max(nums) + 1, max(nums) + 2
    landing = guard(LANDING.format(n1=n1, n2=n2))
    q = q.replace(hit[0], hit[0] + landing, 1)

    # 3. self-feed briefs UNCHECKED at the Open tail
    tail = "".join("\n- [ ] B2-%d %s" % (n1 + i, guard(b)) for i, b in enumerate(BRIEFS))
    if not q.endswith("\n"):
        tail = "\n" + tail
    q = q + tail + "\n"

    with open(QUEUE, "w", encoding="utf-8", newline="") as f:
        f.write(q)
    print("QUEUE closed: claim retired, B2-105 row earned, self-fed B2-%d B2-%d" % (n1, n2))

    # 4. LEDGER row
    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "slug": "B2-105-mistral-surgery",
        "verdict": "landed",
        "lane": "B2-105",
        "landing": RECEIPT,
        "one_line": guard(
            "Mistral lane surgery verified landed and closed: both brief arms "
            "already on disk (repoint arm B2-61 configs/providers.yaml:545 "
            "default_model mistral-small-latest with dormant true and "
            "mistral-free routing lists; nameplate arm B2-21 mag/doctor.py:65 "
            "429+limit-0 QUOTA-DEAD class); this lane verified against bytes "
            "plus two one-token live calls (small-latest 429 limit-req-minute "
            "0 code 1300 the B2-04 zero-quota shape vs large-latest still 403 "
            "tier_not_allowed code 1910, the 403 rode the old default id), "
            "doctor default path DORMANT zero issues, estate 28 providers "
            "consistent; brief's providers.yaml:473-488 pointer stale "
            "(mistral block at 525-553), self-fed forward; pre-checked row "
            "earned per the B2-238 treatment; zero config or code bytes "
            "touched"),
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("LEDGER row appended")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
