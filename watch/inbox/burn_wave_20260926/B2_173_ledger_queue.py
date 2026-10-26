# B2-173 close: flip the B2-173 row with landing pointer, self-feed briefs
# UNCHECKED at live max+1, LEDGER row (json.dumps, never heredoc), and
# index_events registration for receipt + board. Queue bytes are re-read at
# write time per the shared-file claim law; an em-dash guard runs over
# everything this lane appends. No claims were filed by this lane, so none
# are retired.
import hashlib
import json
import os
import re
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
QUEUE = os.path.join(HERE, "QUEUE.md")
EVENTS = os.path.join(REPO, "watch", "inbox", "index_events.jsonl")
RECEIPT = "watch/inbox/burn_wave_20260926/B2_173_l265_flag_20260926.md"


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def guard(text, what):
    assert "\u2014" not in text, "em-dash in lane-appended bytes: " + what


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


data = read_bytes(QUEUE)
text = data.decode("utf-8")

# 1. Flip the B2-173 row and carry the landing pointer (newline-agnostic;
#    the board mixes LF Open rows and a CRLF tail).
row_matches = re.findall(r"- \[ \] B2-173 Flag L265 silent dupe[^\r\n]*", text)
assert len(row_matches) == 1, "B2-173 unchecked row not found exactly once: %d" % len(row_matches)
row = row_matches[0]
guard(row, "b2-173 row bytes")
landing_note = (" Landed 2026-09-26 (receipt: watch/inbox/burn_wave_20260926/"
                "B2_173_l265_flag_20260926.md; premise erratum carried in that "
                "receipt and in mag/links_sha_ratchet.py: LINKS.jsonl:308 already "
                "flags L265's seq 1789736600516927 per the B2-06 append-only flag "
                "convention, so no new flag row was filed; the sha ratchet landed "
                "as mag/links_sha_ratchet.py + configs/links_sha_ratchet_baseline.json "
                "wired into shared_surface validate, 6 pre-existing rows grandfathered "
                "by content sha, zero LINKS.jsonl writes)")
guard(landing_note, "landing note")
new_row = "- [x] B2-173 " + row[len("- [ ] B2-173 "):] + landing_note
guard(new_row, "flipped row")
text = text.replace(row, new_row, 1)

# 2. Self-feed briefs UNCHECKED at live max+1 (B2-167 law: renumber at apply time).
ids = [int(m) for m in re.findall(r"B2-(\d+)", text)]
top = max(ids)
n1, n2 = top + 1, top + 2
briefs = [
    ("- [ ] B2-%d LINKS op-register rows carry no sha and slip past every gate: "
     "the 13 post-marker rows LINKS.jsonl:336-348 (op register, writers "
     "zcode-seat-20260926, zcode-sw-11-b2-144, zcode-sw-10-b2-340) carry "
     "canonical/url/title but no canonical_sha256 field, so the B2-173 same-sha "
     "ratchet (64-hex subjects only, boundary named in its spec) and the B2-06 "
     "sha signal both skip them, and L340 vs L345 are an unflagged same-canonical "
     "pair (docs.z.ai/guides/overview/pricing, filed 20:00:19 and 20:06:47 by two "
     "different lanes) nothing on the estate can see; backfill shas per the B2-26 "
     "amendment shape or extend the ratchet with a canonical-string fallback, "
     "flag or register the L340/L345 pair through the add door, and rule whether "
     "op-register is a sanctioned link schema or a fourth cohabitant that belongs "
     "in its own register per the B2-28 split law; falsifier: after the fix, "
     "appending a second same-canonical op-register row with no sha still passes "
     "validate untouched; pointers watch/inbox/LINKS.jsonl:336-348, "
     "mag/links_sha_ratchet.py scope note, mag/link_library.py add_urls, "
     "watch/inbox/burn_wave_20260926/B2_173_l265_flag_20260926.md Evidence"
     % n1),
    ("- [ ] B2-%d Erratum sweep for B2-26's Evidence bullets: its last bullet "
     "claims L265 is an unflagged silent dupe B2-06 did not flag, byte-false per "
     "LINKS.jsonl:308 naming L265's seq 1789736600516927 (correction carried in "
     "the B2-173 receipt), so the receipt's remaining byte claims earn one "
     "re-verification pass against live bytes before they are cited again: the "
     "110-row sha backfill list, the L256 png-bytes sha, the 8 collision groups' "
     "single-canonical property, and the no-cross-canonical-sha assertion; "
     "re-check each from bytes, file an erratum for any that fails, register "
     "nothing when all hold; falsifier: a B2-26 Evidence claim that differs from "
     "bytes with no erratum on file after this lane; pointers "
     "watch/inbox/burn_wave_20260926/B2_26_links_sha_backfill_20260926.md "
     "Evidence, watch/inbox/burn_wave_20260926/B2_173_l265_flag_20260926.md, "
     "watch/inbox/burn_wave_20260926/B2_06_link_dupes_20260926.md"
     % n2),
]
for b in briefs:
    guard(b, "self-feed brief")
eol = "\r\n" if "\r\n" in text[-200:] or "\r\n" in text[:200] else "\n"
text = text.rstrip("\r\n") + eol + eol + eol.join(briefs) + eol

with open(QUEUE, "wb") as f:
    f.write(text.encode("utf-8"))
print("queue: B2-173 flipped with landing pointer, self-fed B2-%d, B2-%d UNCHECKED" % (n1, n2))

# 3. LEDGER row via json.dumps.
one_line = (
    "landed: brief premise erratum carried against bytes (LINKS.jsonl:308, B2-06 "
    "flag row, already names L265's seq 1789736600516927, so no second flag row "
    "was filed; B2-26 Evidence last bullet and the brief were wrong together) plus "
    "the sha ratchet: mag/links_sha_ratchet.py (scan_same_sha_unflagged + "
    "validate-door check, spec docstring with erratum and scope boundary) + "
    "configs/links_sha_ratchet_baseline.json (6 grandfathered rows, content-sha "
    "keyed: lines 100, 184, 186, 255, 258, 265) wired into shared_surface validate "
    "after links_split_check; 10/10 new pins green, validate adds zero ratchet "
    "errors, LINKS.jsonl untouched 0/0/0; disclosed: an accidental "
    "baseline-update invocation registered 6 claims under by=operator, repaired in "
    "the same landing (5 foreign claims removed, the shared_surface file-too-long "
    "debt kept and accepted by name with cause; register 932 to 933); live foreign "
    "debt named not touched: b2-142's 4 unregistered post-marker kind rows "
    "(LINKS.jsonl:349-352 break the B2-168 real-file pin) and the sha-less "
    "op-register rows 336-348 with the unseeable L340/L345 docs.z.ai dupe "
    "(self-fed B2-%d UNCHECKED) plus the B2-26 erratum sweep (B2-%d UNCHECKED)"
    % (n1, n2)
)
guard(one_line, "ledger one_line")
row_obj = {
    "ts": now_iso(),
    "slug": "b2-173-l265-flag-sha-ratchet",
    "verdict": "LANDED",
    "landing": RECEIPT,
    "one_line": one_line,
}
guard(json.dumps(row_obj), "ledger row")
ld = read_bytes(LEDGER)
leol = b"\r\n" if ld.endswith(b"\r\n") else b"\n"
with open(LEDGER, "ab") as f:
    if ld and not ld.endswith(leol):
        f.write(leol)
    f.write((json.dumps(row_obj) + leol.decode()).encode("utf-8"))
print("ledger: row appended")

# 4. index_events registration: receipt first, then the board (post-edit sha).
def register(path, abs_path, klass, purpose):
    guard(purpose, "index purpose")
    ev = read_bytes(EVENTS)
    last = [ln for ln in ev.decode("utf-8", "replace").strip().split("\n") if ln.strip()]
    seq = int(json.loads(last[-1])["seq"]) + 1
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    entry = {
        "seq": str(seq),
        "ts": ts,
        "op": "register",
        "file": path,
        "sha256": hashlib.sha256(read_bytes(abs_path)).hexdigest().upper(),
        "class": klass,
        "purpose": purpose,
    }
    guard(json.dumps(entry), "index entry")
    eeol = b"\r\n" if ev.endswith(b"\r\n") else b"\n"
    with open(EVENTS, "ab") as f:
        if ev and not ev.endswith(eeol):
            f.write(eeol)
        f.write((json.dumps(entry) + eeol.decode()).encode("utf-8"))
    print("index: seq %s %s %s" % (seq, klass, path))


register(RECEIPT, os.path.join(REPO, RECEIPT), "RECEIPT",
         "B2-173 L265 flag verdict + same-sha ratchet: LINKS.jsonl:308 already "
         "flags L265 (erratum vs B2-26 Evidence and the brief), ratchet landed as "
         "mag/links_sha_ratchet.py + configs baseline wired into shared_surface "
         "validate, 6 rows grandfathered, LINKS.jsonl untouched, register sweep "
         "repaired")
register("watch/inbox/burn_wave_20260926/QUEUE.md", QUEUE, "BOARD",
         "B2-173 landing: row flipped with receipt pointer, self-fed 2 briefs "
         "UNCHECKED at live max+1 (op-register sha gap, B2-26 erratum sweep)")
print("close done")
