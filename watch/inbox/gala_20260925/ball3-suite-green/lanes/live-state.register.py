# gala ball3 live-state lane: register the 5 unregistered post-marker x-drop
# rows (LINKS.jsonl lines 380-384, landed in commit 37036360a "SCOUT WIDE"
# 2026-09-29 09:05) into configs/links_kind_baseline.json per the B2-168
# grandfather pattern, then file ONE op=register row in
# watch/inbox/index_events.jsonl in the same critical section (the
# events-door B2-168 registration shape). LINKS.jsonl bytes are NEVER touched
# (no-erase law): registration names the debt, the ledger stays as landed.
# sha256 keys are recomputed here from LINKS.jsonl raw line bytes (trust
# bytes, not the test failure's printed values) and asserted against the
# gate's own scan before any write.
import hashlib
import json
import os
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LINKS = os.path.join(ROOT, "watch", "inbox", "LINKS.jsonl")
BASELINE = os.path.join(ROOT, "configs", "links_kind_baseline.json")
REG = os.path.join(ROOT, "watch", "inbox", "index_events.jsonl")

EXPECTED = {
    "LINKS-JEEVES": "02446bef6e611fb7f6840303ef1cdd50397ab09aa48b7e2129fdcc120cc9900b",
    "LINKS-RAVEN": "7d3c4f52cac062a9f7314c117ee88a81d3ab0c0b947abea7c2beabfe13c81b8e",
    "LINKS-OSINT-MODEL": "7d69d9199723ea9c3dfdf802998c7a102b2f8dcc864ffd31ac4b3775b1027fb9",
    "LINKS-NIXOS-SOVEREIGNTY": "31e147ad459e196a1d395011fac2497c603ceede582c2ab25472c714d86022c0",
    "LINKS-FACIAL-SCAN-FAIL": "c4098d94784ea4e19b92c017119a3b90125fe86c02fdf1fff3deb94dd5300ac6",
}

# --- 1. byte-truth scan (same algorithm as mag.links_split_gate.scan_links_kind_rows)
with open(LINKS, "rb") as fh:
    raw_links = fh.read()
assert raw_links.endswith(b"\n"), "LINKS.jsonl must end with newline"
marker_line = 0
for lineno, rline in enumerate(raw_links.decode("utf-8").splitlines(), 1):
    if not rline.strip():
        continue
    try:
        row = json.loads(rline)
    except ValueError:
        continue
    if isinstance(row, dict) and row.get("schema") == "migration-marker.v1" \
            and row.get("writer") == "b2-28-schema-split":
        marker_line = lineno
assert marker_line == 332, f"B2-28 marker moved: {marker_line}"

found = {}
for lineno, rline in enumerate(raw_links.decode("utf-8").splitlines(), 1):
    if lineno <= marker_line or not rline.strip():
        continue
    try:
        row = json.loads(rline)
    except ValueError:
        continue
    if isinstance(row, dict) and "kind" in row:
        found[row.get("id")] = {
            "line": lineno,
            "sha256": hashlib.sha256(rline.encode("utf-8")).hexdigest(),
            "kind": row.get("kind"),
            "writer": row.get("writer"),
        }
for rid, sha in EXPECTED.items():
    assert rid in found, f"{rid} not found past marker"
    assert found[rid]["sha256"] == sha, f"{rid} sha drift: {found[rid]['sha256']}"
extra = [rid for rid in found if rid not in EXPECTED]
print("other past-marker kind rows (must all be registered in step 2):", extra)
print("byte-truth scan: 5/5 x-drop rows verified against raw line bytes")

# --- 2. baseline append (contention guard, then one critical section)
with open(BASELINE, "rb") as fh:
    raw_base = fh.read()
pre_base_sha = hashlib.sha256(raw_base).hexdigest()
baseline = json.loads(raw_base)
existing = {e.get("id") for e in baseline.get("grandfathered", [])}
registered_shas = {str(e.get("sha256", "")).lower()
                   for e in baseline.get("grandfathered", [])}
for rid in EXPECTED:
    assert rid not in existing, f"{rid} already registered (double-backfill guard)"
# every kind row past the marker must be one of the 5 being registered here
# or already covered by a registered sha (the 4 pre-existing scout rows)
extra = [rid for rid, rec in found.items()
         if rid not in EXPECTED and rec["sha256"].lower() not in registered_shas]
assert not extra, f"unexpected additional UNREGISTERED kind rows: {extra}"
assert raw_base.endswith(b"\n"), "baseline must end with newline"

WHY = ("scout wide-drop x-drop row appended post-marker (commit 37036360a "
       "SCOUT WIDE 2026-09-29 09:05); legacy scout event shape the links-kind "
       "baseline never saw, named by the f-16 live-append drift class and "
       "registered by name during the ball3 suite-green live-state lane; "
       "no-erase keeps the row in LINKS.jsonl, never edited to fit")
entries = []
for rid, sha in EXPECTED.items():
    rec = found[rid]
    entries.append({
        "line": rec["line"],
        "sha256": rec["sha256"],
        "id": rid,
        "kind": rec["kind"],
        "writer": rec["writer"],
        "why": WHY,
    })
baseline["grandfathered"].extend(entries)
new_base_bytes = (json.dumps(baseline, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
with open(BASELINE, "wb") as fh:
    fh.write(new_base_bytes)
new_base_sha = hashlib.sha256(new_base_bytes).hexdigest()
new_base_size = len(new_base_bytes)
print("baseline: 4 ->", len(baseline["grandfathered"]), "grandfathered entries")

# --- 3. register row in index_events (same critical section)
now = datetime.now(timezone.utc)
reg = {
    "ts": now.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
    "op": "register",
    "file": "configs\\links_kind_baseline.json",
    "sha256": new_base_sha,
    "class": "DATA",
    "purpose": (
        "B2-168 links-kind registration (ball3 live-state): 5 unregistered "
        "post-marker x-drop rows in LINKS.jsonl lines 380-384 (LINKS-JEEVES, "
        "LINKS-RAVEN, LINKS-OSINT-MODEL, LINKS-NIXOS-SOVEREIGNTY, "
        "LINKS-FACIAL-SCAN-FAIL, commit 37036360a) registered by content "
        "sha256 in configs/links_kind_baseline.json; LINKS.jsonl bytes "
        "untouched (no-erase); 4 -> 9 grandfathered entries; sha256/size are "
        "the post-append baseline file"),
    "writer": "live-state",
    "nonce": 1,
    "seq": str(time.time_ns()),
}
assert open(REG, "rb").read().endswith(b"\n"), "register must end with newline"
with open(REG, "ab") as fh:
    fh.write(json.dumps(reg, ensure_ascii=False).encode("utf-8") + b"\n")
print("register row appended: seq", reg["seq"], "ts", reg["ts"])
print("baseline sha256:", new_base_sha)
print("baseline size  :", new_base_size)
