# B2-97 INDEX rebase after clobber: claim INDEX.json, re-apply receipt entry on current
# bytes, retire claim. Anchored, verify-before-write. Named in LEDGER erratum row.
import io, json, hashlib, sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
Q = ROOT + r"\watch\inbox\burn_wave_20260926\QUEUE.md"
IDX = ROOT + r"\watch\inbox\INDEX.json"
RECV = "watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md"
CLAIM = "- CLAIM B2-97 watch/inbox/INDEX.json 2026-09-26T18:38:30Z (B2-97 INDEX rebase: my 18:34Z receipt insert was erased by a concurrent whole-file INDEX rewrite at 18:36:52Z that kept B2-90 and B2-163 entries; re-applying one anchored item on freshly-read bytes per the claim law)"
sha = hashlib.sha256(io.open(ROOT + "\\" + RECV, "rb").read()).hexdigest().upper()

with io.open(Q, "r", encoding="utf-8") as f:
    q = f.read()
if CLAIM not in q:
    if not q.endswith("\n"):
        q += "\n"
    q += CLAIM + "\n"
    with io.open(Q, "w", encoding="utf-8", newline="") as f:
        f.write(q)
    print("claim filed")

with io.open(IDX, "r", encoding="utf-8") as f:
    idx = f.read()
if "B2_97_width15_probe_20260926.md" in idx:
    print("entry already present, skipping")
else:
    ANCHOR = '"sha256": "ED5EB8066087442806BD78C725582C2016183790BF7F34DC28ED696CE558C819"\n    }\n  ]\n}'
    if idx.count(ANCHOR) != 1:
        sys.exit("INDEX anchor fail: %d" % idx.count(ANCHOR))
    head = ANCHOR[: -len('\n  ]\n}')]
    purpose = ("B2-97 width-15 ceiling probe: precondition sweep found NO explicit operator GO for "
               "width 15 on QUEUE.md or any 2026-09-26 receipt, so per the row's own "
               "when-operator-ordered gate the wave was NOT fired; ready-to-fire card with the full "
               "harvest plan (15 Task agents one wave, metadata.json "
               "status/createdAt/totalDurationMs/totalTokens/totalToolUseCount, window + tok/h on the "
               "B2-25 convention, 1302 + 429 grep over all agent outputs, no refire inside the probe, "
               "amend-envelope-block-either-way rule) plus metadata shape byte-verified on 156 agent "
               "dirs of sess_fd5ec147; AFTERPARTY_CLOSE envelope block amended append-only naming the "
               "armed probe; ladder unchanged 3-6-10-12; first insert 18:34Z erased by the 18:36:52Z "
               "concurrent INDEX rewrite, re-landed by this rebase")
    entry = (head
             + ',\n    {\n      "path": "burn_wave_20260926/B2_97_width15_probe_20260926.md",\n'
               '      "class": "receipt",\n      "purpose": "' + purpose + '",\n'
             + '      "sha256": "' + sha + '"\n    }\n  ]\n}')
    out = idx.replace(ANCHOR, entry)
    json.loads(out)
    with io.open(IDX, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("INDEX entry re-applied, json valid")

with io.open(Q, "r", encoding="utf-8") as f:
    q2 = f.read()
if CLAIM in q2:
    q2 = q2.replace(CLAIM, CLAIM.replace("- CLAIM B2-97", "- CLAIMED B2-97", 1) + " -> " + RECV)
    with io.open(Q, "w", encoding="utf-8", newline="") as f:
        f.write(q2)
    print("claim retired")
