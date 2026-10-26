# s2-22 final step: compute live receipts (drift walk, dash scan, twin cmp, spot-check
# notes) and append the identical verification block to both twin files.
import os, io, datetime, subprocess, json

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, ".git")):
    ROOT = os.path.dirname(ROOT)
INBOX = os.path.join(ROOT, "watch", "inbox")
TWIN_A = os.path.join(HERE, "inbox-genre-census.md")
TWIN_B = os.path.join(HERE, "s2-22.md")
now = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

md = allf = 0
for dp, dns, fs in os.walk(INBOX):
    for f in fs:
        allf += 1
        if f.lower().endswith(".md"):
            md += 1
g = subprocess.run(["git", "ls-files", "--", "watch/inbox"], cwd=ROOT, capture_output=True,
                   text=True, encoding="utf-8", errors="replace",
                   creationflags=CREATE_NO_WINDOW)
tracked_md = sum(1 for l in g.stdout.splitlines() if l.lower().endswith(".md"))

def dashes(path):
    t = io.open(path, encoding="utf-8").read()
    return (t.count("\u2014"), t.count("\u2013"), t.count("\u2012"), t.count("\u2212"))

da = dashes(TWIN_A)
db = dashes(TWIN_B)
cmp_rc = subprocess.run(["cmp", os.path.basename(TWIN_A), os.path.basename(TWIN_B)],
                        cwd=HERE, capture_output=True, text=True,
                        creationflags=CREATE_NO_WINDOW).returncode

raw = json.load(io.open(os.path.join(HERE, "_s2_22_raw.json"), encoding="utf-8"))
s = raw["summary"]

block = """
## Verification receipts (appended at banking, %s)

- final drift walk at banking: %d md / %d total files under watch/inbox/ (git-tracked md: %d). Delta vs snapshot of record: %+d md in ~2 h - the census of record above is the 20:23:59 snapshot, this is the drift it was taken inside.
- em/en dash scan of both twins at banking: em %d / en %d / figure %d / minus %d (this file) and em %d / en %d / figure %d / minus %d (s2-22.md). Quoted heading text was dash-normalized at compose time (Method 10); authored text carries none.
- twin byte-identity: `cmp inbox-genre-census.md s2-22.md` exit %d (0 = identical).
- reference spot-checks (4/4 confirmed by direct grep): `tools/lattice_build.py:57` names SELF_STEAL_TEST_TIME_COMMUNICATION_20260921.md; `scripts/build_deck.py:221,240` name wave_20260916/WAVE_STATE_20260916.md; `AGENTS.md` clippy block names ENVELOPE_50W_HIT_20260926.md; `githooks/pre-push` names MICKEY17_WAVE2_QUALITY_20260925.md.
- zero-ref spot-checks caught an instrument defect: 3 stems the first rg `-o` pass called zero-ref were found by repo-wide grep in catalog/ and memory/trajectory/ - ripgrep 15.2.0 `-o` with a 2,379-pattern `-f` file silently drops matches. All reference numbers were re-derived with line-mode passes and exact python attribution (Method 5b) before banking; the corrected instruments credit %d of %d md files somewhere and %d canonically.
- the 4 zero-everywhere files: 2 are hard orphans confirmed by repo-wide grep outside the inbox (`burn_reset_20260927/flash50/_sw03_out_sw-econ-3_stealth_space-bunny-alpha.md`, `fifty_wide_20260917/FW37-42_INDEX.md`); the other 2 (`outbound/adventurelearn_packet/WHY.md`, `seed_rib_20260926/seed-rib/CHANGELOG.md`) have generic-word stems - repo-wide word greps collide with the words themselves, so their zero-ref claim is exact only under the census name-matching instruments (their names are in the GENERIC stoplist for exactly this reason).
""" % (now, md, allf, tracked_md, md - s["md_total"],
       da[0], da[1], da[2], da[3], db[0], db[1], db[2], db[3],
       cmp_rc, s["referenced_any"], s["md_total"], s["canon_union"])

assert "\u2014" not in block and "\u2013" not in block
for p in (TWIN_A, TWIN_B):
    with io.open(p, "a", encoding="utf-8", newline="\n") as f:
        f.write(block)
print("final walk", md, "md /", allf, "files / tracked-md", tracked_md)
print("dash scan A", da, "B", db, "| cmp exit before append", cmp_rc)
print("appended", len(block), "chars to both twins")
