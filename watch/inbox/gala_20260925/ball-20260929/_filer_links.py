# estate-filer, ball-20260929 fold: append GALA LINKS rows to memory/corpus/LINKS.jsonl
# Laws: sequential single-writer append only; dedupe by src before appending;
# no em-dashes in filed text; never fabricate (texts below are verbatim from the
# lane JSONs read this session, bare-spawn decision from the ask's summary
# corroborated by lanes/bare-spawn-descent.json baseline_update/conversions).
import json, sys, datetime, io

LEDGER = r"C:\Users\foste\Documents\projects\local_sovereign_agent\memory\corpus\LINKS.jsonl"
SLUG = "ball-20260929"
SRC_BASE = "watch/inbox/gala_20260925/ball-20260929/lanes/"
LANE_TAG = "gala-20260925/ball-20260929/"

def dec(text):
    return text

ROWS = [
    {
        "lane": "fold-gate", "division": "B",
        "title": dec("gala fold arithmetic is now script-written end to end: fold_gate.sh prints the ballroom danced/refired/buried count (was hand-computed by the filer per the wave5 completion finding) and counts decisions under all three observed key names (10 -> 12, matching the filer's verified hand count); wrong-bash invocations fail loud rc 2 instead of the silent 127."),
        "decision": dec("gala fold arithmetic is now script-written end to end: fold_gate.sh prints the ballroom danced/refired/buried count (was hand-computed by the filer per the wave5 completion finding) and counts decisions under all three observed key names (10 -> 12, matching the filer's verified hand count); wrong-bash invocations fail loud rc 2 instead of the silent 127."),
        "load_bearing": [],
        "note": "receipt watch/inbox/ball2/fold-gate.md; lane JSON + check evidence in src",
    },
    {
        "lane": "driver-v2", "division": "B",
        "title": dec("sensed-never-done is closed: the work queue now drains through funded verification (lib-belady-1966 flipped done_ts 2026-09-29T15:18:30Z after a real OWED-then-DONE verify pair), and the selffeed never-drains-it-grows doctrine is replaced by the bounded loop (trigger gate, hourly spacing, cap 20, depth 2, dedupe, m%03d ids, 24h ttl, breaker)"),
        "decision": dec("sensed-never-done is closed: the work queue now drains through funded verification (lib-belady-1966 flipped done_ts 2026-09-29T15:18:30Z after a real OWED-then-DONE verify pair), and the selffeed never-drains-it-grows doctrine is replaced by the bounded loop (trigger gate, hourly spacing, cap 20, depth 2, dedupe, m%03d ids, 24h ttl, breaker)"),
        "load_bearing": [],
        "note": "receipt watch/inbox/ball2/driver-v2.md; lane JSON + check evidence in src",
    },
    {
        "lane": "quantizer-hygiene", "division": "B",
        "title": dec("The compiled-law decay relation is now ONE named constant (PACK_STALE_DAYS=7, mag/constants.py) imported by producer, consumer and boot meter: the w4-27 L3 subsumption gap ('stale at 24h for its compiler, fresh to 7d for its readers') is closed in code, and kept-but-unpacked law is now a loud compile-time linker error instead of a silent 283-law census finding"),
        "decision": dec("The compiled-law decay relation is now ONE named constant (PACK_STALE_DAYS=7, mag/constants.py) imported by producer, consumer and boot meter: the w4-27 L3 subsumption gap ('stale at 24h for its compiler, fresh to 7d for its readers') is closed in code, and kept-but-unpacked law is now a loud compile-time linker error instead of a silent 283-law census finding"),
        "load_bearing": [],
        "note": "receipt watch/inbox/ball2/quantizer-hygiene.md; lane JSON + check evidence in src",
    },
    {
        "lane": "abliterate-p1", "division": "B",
        "title": "gemma-2b-friction-is-capability-shaped",
        "decision": dec("Closes: ABLITERATUS probe P1 baseline (owed from the drop). Changes: the P2 decision input - gemma:2b friction on the fleet's own scut shapes is capability-shaped (0/60 safety refusals, 11/60 file-reference capability declinations), not safety-refusal-shaped; the $0 counter-move (attach cited-file content to scut prompts, or tool-wire the janitor) is registered as first remediation before any weight change, and the P2 gate reads the capability/safety split from this exact battery unchanged."),
        "load_bearing": ["gemma-2b-friction-is-capability-shaped"],
        "note": "receipt watch/inbox/ball2/abliterate-p1.md; lane JSON + check evidence in src",
    },
    {
        "lane": "mcp-bridge-r1", "division": "B",
        "title": "isError in-band, never protocol-level",
        "decision": dec("mcp-bridge R1 closed: estate compute moved from zero tools on the live MCP surface to five verbs / six tools any MCP client can call over stdio, with the standing decision now in force that chain repair, dirac bank, driver control words and provider keys are never exposed (R2-R5 unstarted per the design's rollout order)."),
        "load_bearing": ["isError in-band, never protocol-level"],
        "note": "receipt watch/inbox/ball2/mcp-bridge-r1.md; lane JSON + check evidence in src",
    },
    {
        "lane": "bare-spawn-descent", "division": "B",
        "title": dec("bare-spawn debt under the headless law: tests/ descended to zero bare spawn sites and the accepted register lowered 41 -> 22 (live 43 at lane start), so any new tests/ spawn without creationflags now goes red with zero tests/ headroom; runtime half was already sealed by the conftest default, this closed the static half"),
        "decision": dec("bare-spawn debt under the headless law: tests/ descended to zero bare spawn sites and the accepted register lowered 41 -> 22 (live 43 at lane start), so any new tests/ spawn without creationflags now goes red with zero tests/ headroom; runtime half was already sealed by the conftest default, this closed the static half"),
        "load_bearing": [],
        "note": "receipt watch/inbox/ball2/bare-spawn-descent.md; lane JSON + check evidence in src (lane JSON carries the decision under baseline_update/conversions, not a decision_changed key)",
    },
    {
        "lane": "attention-ledger", "division": "B",
        "title": dec("Attention-market wiring decision: the trade ledger (memory/attention_feedback.jsonl) went from ABSENT/zero-trades-uninformative (w4-03, w4-37 T2: you could not tell apathy from broken rails) to proven rails with the market's first two settled trades; POST casts settle once in the five-signal vocabulary and the next ranking pass provably consumes them, so future zero-trade readings are honest demand signals."),
        "decision": dec("Attention-market wiring decision: the trade ledger (memory/attention_feedback.jsonl) went from ABSENT/zero-trades-uninformative (w4-03, w4-37 T2: you could not tell apathy from broken rails) to proven rails with the market's first two settled trades; POST casts settle once in the five-signal vocabulary and the next ranking pass provably consumes them, so future zero-trade readings are honest demand signals."),
        "load_bearing": [],
        "note": "receipt watch/inbox/ball2/attention-ledger.md; lane JSON + check evidence in src",
    },
    {
        "lane": "heads-abliteratus", "division": "A",
        "title": "verify-after-modify with a named battery",
        "decision": dec("Janitor-ladder probe order: try P3 (reversible inference-time steering vectors, no weight mutation, hot-swappable) before P2 (permanent weight projection) for the local-janitor refusal-friction fix, both gated on the P1 refusal-census baseline and the named capability battery from row 1, and adopt the verification stage regardless of whether the ablation itself is adopted; second-order change from row 2: violation classes excised by the ratchet keep their downstream detectors enabled instead of closing the watch when the fix lands."),
        "load_bearing": ["verify-after-modify with a named battery"],
        "note": "no ball2 receipt on disk (ls verified 2026-09-29); lane JSON + check evidence in src (heads-abliteratus.check.txt)",
    },
]

# em/en-dash guard over every field we are about to file
BAD = {"\u2014", "\u2013", "\u2212"}
def scan(obj, path):
    if isinstance(obj, str):
        for ch in obj:
            if ch in BAD:
                print("EMDASH FOUND at %s: %r" % (path, ch)); sys.exit(3)
    elif isinstance(obj, list):
        for i, v in enumerate(obj): scan(v, "%s[%d]" % (path, i))
    elif isinstance(obj, dict):
        for k, v in obj.items(): scan(v, "%s.%s" % (path, k))

for r in ROWS: scan(r, r["lane"])

src = SRC_BASE
with io.open(LEDGER, "r", encoding="utf-8") as fh:
    existing = fh.readlines()

prior_srcs = set()
prior_ids = set()
for ln in existing:
    ln = ln.strip()
    if not ln: continue
    j = json.loads(ln)
    prior_srcs.add(j.get("src"))
    prior_ids.add(j.get("id"))

before = len([l for l in existing if l.strip()])
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
appended, skipped = [], []
with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as fh:
    if existing and not existing[-1].endswith("\n"):
        fh.write("\n")
    for r in ROWS:
        src = SRC_BASE + r["lane"] + ".json"
        rid = "GALA-%s-%s" % (SLUG, r["lane"])
        if src in prior_srcs or rid in prior_ids:
            skipped.append(rid); continue
        row = {
            "ts": now,
            "id": rid,
            "kind": "gala",
            "src": src,
            "author": "gala lane %s (%s, division %s)" % (r["lane"], SLUG, r["division"]),
            "title": r["title"],
            "load_bearing": r["load_bearing"],
            "decision_changed": r["decision"],
            "lane": LANE_TAG + r["division"],
            "note": r["note"],
        }
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        appended.append(rid)
        prior_srcs.add(src); prior_ids.add(rid)

# whole-ledger re-parse
with io.open(LEDGER, "r", encoding="utf-8") as fh:
    lines = [l for l in fh if l.strip()]
parsed = [json.loads(l) for l in lines]
print("before_rows: %d" % before)
print("appended: %d %s" % (len(appended), appended))
print("skipped_dupe: %d %s" % (len(skipped), skipped))
print("after_rows: %d (re-parsed OK)" % len(parsed))
gala_ball = [p["id"] for p in parsed if p.get("kind") == "gala" and SLUG in str(p.get("src", ""))]
print("gala_%s rows in ledger: %d" % (SLUG, len(gala_ball)))
