# B2-489 close: retire the three board claims, landing note on the B2-489 row,
# self-feed briefs UNCHECKED at live max+1, LEDGER row (json.dumps, never
# heredoc), index_events registration for receipt + board. Queue bytes are
# re-read at write time per the shared-file claim law; a foreign em-dash guard
# runs over everything this lane appends.
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
RECEIPT = "watch/inbox/burn_wave_20260926/B2_489_resolver_bound_20260926.md"
CLAIM_TS = "2026-09-26T19:24:00Z"


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def guard(text, what):
    assert "\u2014" not in text, "em-dash in lane-appended bytes: " + what


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


data = read_bytes(QUEUE)
text = data.decode("utf-8")

# 1. Retire the three claim lines (exact bytes this lane appended at 19:24:00Z).
claims = [
    ("- CLAIM B2-489 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS
     + " (B2-489 resolver bound own board: claim lines, landing pointer on the pre-checked B2-489 row, self-feed briefs UNCHECKED; foreign active CLAIMs B2-104 and B2-469 on this file honored, anchored appends on freshly-read bytes, no whole-file rewrite)"),
    ("- CLAIM B2-489 mag/doctor.py " + CLAIM_TS
     + " (B2-489: _host_resolves daemon-thread hard-deadline plus module and check docstring bound paragraphs only; file is working-tree-modified by B2-107/B2-358 landed bytes, later lanes rebase on my landed bytes per the claim law)"),
    ("- CLAIM B2-489 tests/test_doctor_provider_endpoints.py " + CLAIM_TS
     + " (B2-489: append socket-level blackhole pins fixture-first; existing 20 pins untouched; re-read bytes before your edit per the claim law)"),
]
for c in claims:
    assert text.count(c) == 1, "claim line not found exactly once: " + c[:60]
    guard(c, "claim")
    text = text.replace(c, "- CLAIMED" + c[len("- CLAIM"):len(c)] + " -> " + RECEIPT)

# 2. Landing note on the pre-checked B2-489 row (B2-464 shape).
# The Open rows are LF while the tail is CRLF (mixed-ending board), so match
# the line newline-agnostically.
row_matches = re.findall(r"- \[x\] B2-489 Bound the locality getaddrinfo seam[^\r\n]*", text)
assert len(row_matches) == 1, "B2-489 row not found exactly once: %d" % len(row_matches)
note = (" (LANDED " + now_iso() + " receipt " + RECEIPT
        + "; the [x] flip predates this note on the bytes, this note is the "
        "landing lane's pointer per the B2-238 law)")
guard(note, "landing note")
text = text.replace(row_matches[0], row_matches[0] + note, 1)

# 3. Self-feed briefs UNCHECKED at live max+1 (B2-167 law: renumber at apply time).
ids = [int(m) for m in re.findall(r"B2-(\d+)", text)]
top = max(ids)
n1, n2, n3 = top + 1, top + 2, top + 3
briefs = [
    ("- [ ] B2-%d Registry ollama_tags timeout clamp is silent: ollama_tags"
     "(timeout=3.0) clamps to min(max(timeout, 0.1), 1.0) (models/registry.py"
     " hard_timeout line), so the 3.0s default actually waits at most 1.0s and"
     " callers passing larger timeouts get a silently smaller bound with no doc"
     " naming the clamp; surface the clamp in the docstring or honor the caller"
     " value with the same daemon-deadline seam doctor._host_resolves got in"
     " B2-489; falsifier: ollama_tags(timeout=3.0) against a tags server that"
     " answers at 1.5s returns before 1.5s while the signature implies 3s;"
     " pointers models/registry.py ollama_tags, mag/doctor.py"
     " _RESOLVE_TIMEOUT_S, watch/inbox/burn_wave_20260926/B2_489_resolver_bound_20260926.md"
     % n1),
    ("- [ ] B2-%d Worst-case locality stall is N deadlines and nothing counts"
     " it: each local-declared lane whose name blackholes now costs"
     " _RESOLVE_TIMEOUT_S (2.0s) sequentially in check_provider_endpoints, so"
     " configs/providers.yaml with N local-declared arms plus a blackholing DNS"
     " stalls examine() for N x 2s with no census or doc naming the linear"
     " bound; census the local-declared arms (id ollama, :11434, free_local)"
     " across configs/providers.yaml, pin the measured worst case, document or"
     " parallelize if N grows; falsifier: a fixture with 3 local-declared lanes"
     " and the 30s sleeper takes >= 6s while no doc names the linear bound;"
     " pointers mag/doctor.py _host_resolves, configs/providers.yaml ollama and"
     " mlx-cluster blocks, watch/inbox/burn_wave_20260926/B2_489_resolver_bound_20260926.md"
     % n2),
    ("- [ ] B2-%d Estate-wide unbounded name-resolution sweep: B2-489 bounded"
     " the doctor seam but every other socket.getaddrinfo / socket.gethostbyname"
     " / socket.getfqdn caller in mag/, models/ and tools/ sits on the same"
     " unbounded Windows DNS path the registry comment names; census each"
     " caller, classify bounded (timeout, daemon deadline) vs unbounded, give"
     " the unbounded ones the seam treatment or a documented why-not; falsifier:"
     " at least one caller whose resolution can block past 10s with no deadline"
     " and no doc; pointers models/registry.py:99-106, mag/doctor.py"
     " _host_resolves, watch/inbox/burn_wave_20260926/B2_489_resolver_bound_20260926.md"
     % n3),
]
for b in briefs:
    guard(b, "self-feed brief")
eol = "\r\n" if "\r\n" in text[-200:] or "\r\n" in text[:200] else "\n"
text = text.rstrip("\r\n") + eol + eol + eol.join(briefs) + eol

with open(QUEUE, "wb") as f:
    f.write(text.encode("utf-8"))
print("queue: claims retired, landing note set, self-fed B2-%d, B2-%d, B2-%d" % (n1, n2, n3))

# 4. LEDGER row via json.dumps.
row = {
    "ts": now_iso(),
    "slug": "b2-489-resolver-bound",
    "verdict": "LANDED",
    "fresh_failure_mode": True,
    "landing": RECEIPT,
    "one_line": (
        "landed: doctor locality seam _host_resolves got the registry treatment"
        " (one getaddrinfo on a daemon thread joined with _RESOLVE_TIMEOUT_S=2.0s,"
        " the check's own local-probe timeout; deadline reads unresolvable, same"
        " DOWN none(locality) classification, stranded thread dies with the"
        " process like ollama_tags), because the pre-bound falsifier reproduced"
        " the brief verbatim: monkeypatched 30s sleeper made the seam take 30.0s"
        " and check_provider_endpoints take 30.1s with zero red pins (red run 2"
        " failed / 1 passed 60.59s, fixture-first); post-fix 20/20 in"
        " tests/test_doctor_provider_endpoints.py x3 clean full passes, 66/66"
        " across the doctor-importing battery, ratchet PASS NEW=0, live trap run"
        " 4.12s DOWN none(locality); transient named: one 3 passed / 17 errors"
        " fixture-setup storm between green runs, three same-bytes reruns clean,"
        " attributed to concurrent-lane machine contention not the change;"
        " self-fed B2-%d, B2-%d, B2-%d UNCHECKED (registry timeout clamp silent,"
        " N-deadline worst-case stall uncounseled, estate-wide unbounded"
        " name-resolution sweep)" % (n1, n2, n3),
    ),
}
guard(json.dumps(row), "ledger row")
ld = read_bytes(LEDGER)
leol = b"\r\n" if ld.endswith(b"\r\n") else b"\n"
with open(LEDGER, "ab") as f:
    if ld and not ld.endswith(leol):
        f.write(leol)
    f.write((json.dumps(row) + leol.decode()).encode("utf-8"))
print("ledger: row appended")

# 5. index_events registration: receipt first, then the board (post-edit sha).
def register(path, sha_path, klass, purpose):
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
        "sha256": hashlib.sha256(sha_path_bytes(sha_path)).hexdigest().upper(),
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


def sha_path_bytes(p):
    return read_bytes(p)


register(RECEIPT, os.path.join(REPO, RECEIPT), "RECEIPT",
         "B2-489 resolver bound: locality getaddrinfo seam deadline-bounded"
         " (daemon thread + _RESOLVE_TIMEOUT_S 2.0s), 30.1s pre-bound falsifier"
         " red run, 20/20 file + 66/66 battery, ratchet NEW=0")
register("watch/inbox/burn_wave_20260926/QUEUE.md", QUEUE, "BOARD",
         "B2-489 landing: 3 claims retired to CLAIMED with receipt arrows,"
         " landing note on the pre-checked B2-489 row, self-fed B2-%d..B2-%d"
         " UNCHECKED at live max+1" % (n1, n3))
print("close done")
