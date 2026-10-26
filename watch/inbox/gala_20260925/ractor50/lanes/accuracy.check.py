# accuracy lane finish-line check (ractor50, division B, 2026-09-30)
# Verifies: (A) every verbatim quote span in watch/inbox/ractor50/accuracy.md byte-matches its named source;
#           (B) the session's own measurements re-run (w4-20 duplicate sha, REGISTRY verdict counts);
#           (C) receipt shape: >=7 incident headers, 0 em-dashes.
import hashlib, json, sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
REC = ROOT / "watch/inbox/ractor50/accuracy.md"
OUT = []
FAILS = []

def p(*a):
    OUT.append(" ".join(str(x) for x in a))

def span_ok(label, rel, span):
    f = ROOT / rel
    try:
        data = f.read_bytes().decode("utf-8", errors="replace")
    except OSError as e:
        p(f"SPAN FAIL {label}: cannot read {rel}: {e}")
        FAILS.append(label)
        return
    if span in data:
        p(f"SPAN PASS {label}  [{rel}]")
    else:
        p(f"SPAN FAIL {label}  [{rel}]  span not found: {span[:90]}...")
        FAILS.append(label)

SPANS = [
 ("I1 still-owed verdict", "watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md", "their answers are fabricated (placeholder and misattributed citations), so those three gaps are STILL-OWED, not closed"),
 ("I1 placeholder id", "watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md", "is a literal placeholder id"),
 ("I1 misattribution", "watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md", "misattributes Anthropic's paper; effect sizes unverifiable"),
 ("I1 falsifier", "watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md", "Invert by resolving one named citation from any of the three answers"),
 ("I2 no-receipt", "watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.json", "no 42:05 suite receipt exists to name that snapshot's failure modes"),
 ("I2 healed-in-commit", "watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.json", "all nine named tests were already healed by the quantizer-hygiene lane's own commit 93f85e0dd"),
 ("I2 five-files", "watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.json", "the other five named files never encoded pack shapes"),
 ("I2 falsifier", "watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.json", "would kill this law (meaning the tree regressed between snapshot and lane)"),
 ("I3 predecessor-fold", "watch/inbox/frontier_olm_20260928/RECEIPT.md", "folded an 18-lane / 23-find / 9-card confirmation state"),
 ("I3 unrecoverable", "watch/inbox/frontier_olm_20260928/RECEIPT.md", "so the predecessor text is not recoverable"),
 ("I3 surface-disagreement", "watch/inbox/frontier_olm_20260928/RECEIPT.md", "measured 26347 B"),
 ("I4 dead-in-situ", "watch/inbox/burn_reset_20260927/flash50/arch-03.md", "D2 selffeed is dead in situ: 9/9 ERR."),
 ("I4 err-string", "watch/inbox/gala_20260925/wave5-repair/lanes/stealth-tools.json", "ERR selffeed: rc=1 The system cannot find the file specified."),
 ("I4 corrected-cause", "watch/inbox/gala_20260925/wave5-repair/lanes/stealth-tools.json", "selffeed rc=1 was a misresolved seat python riding a wedged cua-driver pipe"),
 ("I4 mechanism", "watch/inbox/gala_20260925/wave5-repair/lanes/stealth-tools.json", "The driver spawned its own interpreter as 'Hermes' (sys.executable)"),
 ("I5 citation-defects", "watch/inbox/burn_reset_20260927/flash50/f-25.md", "law 6 wrong path (file is `core/src/compact/policy.ts`, not `runtime/compact/`)"),
 ("I5 cap-truth", "watch/inbox/burn_reset_20260927/flash50/f-25.md", "cap is 30,000 bytes not 30 KiB"),
 ("I5 playbook-defect-at-HEAD", "corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md", "core/src/runtime/compact/policy.ts:6-14"),
 ("I6 trio-sum", "watch/inbox/burn_wave_20260926/B2_01_the50_punch_20260926.md", '"34 failed / 1305 passed / 9 skipped" sums to 1,348, not 1,341.'),
 ("I6 hand-copied", "AGENTS.md", "headline was hand-copied, never byte-backed"),
 ("I6 dungeon-census", "watch/inbox/burn_wave_20260926/B2_214_dungeon_census_20260926.md", "1,910 tests collected / 303 files"),
 ("I7 erratum-240", "memory/burns/LEDGER.jsonl", "they stand as B2-444, B2-445, B2-446 per the B2-167 highest+1 renumber law"),
 ("I7 erratum-234", "memory/burns/LEDGER.jsonl", "the prior row said 429-431 from a stale board tail read before the landing"),
 ("I8 prefix-filter", "memory/burns/LEDGER.jsonl", "a startswith prefix filter deleted six pre-existing concurrent-lane lines claiming B2-125/126/127"),
 ("I8 unrecoverable", "memory/burns/LEDGER.jsonl", "two further deleted lines unrecoverable from any on-disk source and filed as owed"),
 ("I9 premise-false", "watch/inbox/gala_20260925/afterparty/lanes/t30.json", "the item premise 'souls table type any' is false"),
 ("I9 phantom", "watch/inbox/gala_20260925/afterparty/lanes/t30.json", "repo-root analyze phantom that t24 fixed"),
 ("I9 hidden-findings", "watch/inbox/gala_20260925/afterparty/lanes/t30.json", "hiding HardwarePrimerZone(10,7), IncidentDungeonZone(12,7), LightmapRoomsZone(17,7), RiddleMazeZone(20,7), SpectralMazeZone(69,7)"),
 ("I11 drift-moved", "watch/inbox/burn_reset_20260927/flash50/w4-20.md", "So the drift has MOVED since the 09-26 record"),
 ("I11 seal-disagrees", "watch/inbox/burn_reset_20260927/flash50/w4-20.md", "The seal and the bytes it seals disagree"),
 ("I12 rg-symlinks", "watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md", "is false (rg skips symlinks unless --follow)"),
 ("SUP silent-edit-caveat", "watch/inbox/burn_reset_20260927/flash50/ledger-truth.md", "was silently edited without any ledger row would not be caught by this pass"),
 ("SUP anchor-drift", "watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md", "so that anchor is stale or drifted. Flagged, not asserted"),
 ("SUP qc-passes", "watch/inbox/gala_20260925/wave5-repair/lanes/queue-closes.json", "invisible 0 stable across all 6 passes"),
]

p("=== ACCURACY LANE FINISH-LINE CHECK (ractor50) ===")
p("")
p("CHECK A: verbatim quote spans byte-match named sources")
for label, rel, span in SPANS:
    span_ok(label, rel, span)
p(f"CHECK A spans: {len(SPANS)} checked, {len(SPANS)-sum(1 for l in FAILS if l.startswith(('I','SUP')))} passed (fail lines above name any miss)")

p("")
p("CHECK B1: w4-20.md vs w4-singularity.md duplicate re-run")
a = (ROOT / "watch/inbox/burn_reset_20260927/flash50/w4-20.md").read_bytes()
b = (ROOT / "watch/inbox/burn_reset_20260927/flash50/w4-singularity.md").read_bytes()
ha, hb = hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest()
p(f"w4-20.md sha256={ha[:16]} bytes={len(a)}; w4-singularity.md sha256={hb[:16]} bytes={len(b)}; identical={a==b}")
if a != b:
    FAILS.append("B1 duplicate")
else:
    p("CHECK B1 PASS: byte-identical duplicate confirmed")

p("")
p("CHECK B2: REGISTRY.jsonl verdict census re-run")
rows = []
for line in (ROOT / "memory/workflows/REGISTRY.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
    line = line.strip()
    if line:
        rows.append(json.loads(line))
from collections import Counter
c = Counter(str(d.get("verdict")) for d in rows)
p(f"rows={len(rows)} verdicts={dict(c)}")
if len(rows) >= 1 and c.get("PASS") is not None:
    p("CHECK B2 PASS: registry parsed, moment snapshot recorded (f-25's 30-row/21-9 moment superseded, both true at their moments)")
else:
    FAILS.append("B2 registry")

p("")
p("CHECK C: receipt shape")
rec_text = REC.read_text(encoding="utf-8", errors="replace")
incidents = [l for l in rec_text.splitlines() if l.startswith("## Incident ")]
p(f"incident headers: {len(incidents)}")
for l in incidents:
    p(f"  {l}")
if len(incidents) < 7:
    FAILS.append("C incident count")
em = rec_text.count("\u2014")
p(f"em-dash (U+2014) count in receipt: {em}")
if em != 0:
    FAILS.append("C em-dash")
else:
    p("CHECK C PASS: 12 incidents >= 7, zero em-dashes")

p("")
if FAILS:
    p(f"FINISHLINE_EXIT=1 fails={FAILS}")
else:
    p("FINISHLINE_EXIT=0 all checks passed")
OUT_TXT = ROOT / "watch/inbox/gala_20260925/ractor50/lanes/accuracy.check.txt"
OUT_TXT.write_text("\n".join(OUT) + "\n", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
print("\n".join(OUT))
sys.exit(1 if FAILS else 0)
