# events-door backfill: append 5 charter-schema carrier rows to watch/inbox/EVENTS.jsonl
# for the 5 schema-less rows at lines 54-58, then re-register per
# EVENTS_DRIFT_LAW_20260926 rule 2 (one critical section). No-erase: bad rows untouched.
# Spec: SCOUT_CHARTER_20260926.md section 4 (backfill amendment, 2026-09-29).
import hashlib
import json
import os
import time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
EV = os.path.join(ROOT, "watch", "inbox", "EVENTS.jsonl")
REG = os.path.join(ROOT, "watch", "inbox", "index_events.jsonl")
PRE_SHA = "ae77c7910fb5c397e7c0103aae195d69a3ffbfe194264a5ff592f6ad457ef287"

raw = open(EV, "rb").read()
pre_sha = hashlib.sha256(raw).hexdigest()
assert pre_sha == PRE_SHA, f"contention guard: bytes moved since census: {pre_sha}"
assert raw.endswith(b"\n"), "file must end with newline before append"
lines = raw.decode("utf-8").splitlines()
assert len(lines) == 58, len(lines)
for line in lines:  # structural double-backfill guard (word "replaces" also occurs in row prose, line 35)
    row = json.loads(line)
    origin = row.get("origin")
    assert not (row.get("schema") == "event.v1" and isinstance(origin, dict) and origin.get("replaces")), \
        f"a backfill carrier already exists: {row.get('id')}"


def row_sha(line: str) -> str:
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
carriers = []

# Lines 54-57: b2-142-cerebras-dig findings. Content re-minted verbatim; writer stays
# the content-owning lane; origin.backfilled_by names the minting lane.
for idx in (53, 54, 55, 56):
    orig = json.loads(lines[idx])
    assert "schema" not in orig and "origin" not in orig, orig["id"]
    carriers.append({
        "ts": now,
        "writer": orig["writer"],
        "id": orig["id"] + "-BACKFILL",
        "kind": "finding",
        "title": orig["title"],
        "detail": orig["detail"],
        "sources": orig["sources"],
        "flag": orig["flag"],
        "schema": "event.v1",
        "origin": {
            "file": "watch/inbox/EVENTS.jsonl",
            "line": idx + 1,
            "replaces": orig["id"],
            "original_ts": orig["ts"],
            "original_sha256": row_sha(lines[idx]),
            "backfill_reason": (
                "schema-less row: no schema/origin keys, strict load_events() door "
                "fail-closed the whole ledger (f-05 census 2026-09-28)"),
            "backfilled_by": "wave5-repair-events-door",
        },
    })

# Line 58: LINKS-329-CORRECTION. Alien key shape (corrects/src/error/correct_state/note),
# no writer, kind "correction" outside the charter vocabulary. Substance composed verbatim
# into labeled title+detail; original row stays in the file as the alien-key record.
idx = 57
orig = json.loads(lines[idx])
assert "schema" not in orig and "origin" not in orig and "writer" not in orig, orig["id"]
carriers.append({
    "ts": now,
    "writer": "events-door",
    "id": orig["id"] + "-BACKFILL",
    "kind": "finding",
    "corrects": orig["corrects"],
    "title": ("LINKS-329 correction carried in charter schema: JEV fee is 0.36 PERCENT "
              "of comparator fee, not 0.36x (100x drift, caught by "
              "watch/inbox/BURN_judge-lane-spec_20260927.md pass b)"),
    "detail": ("src: " + orig["src"] + " | error: " + orig["error"] +
               " | correct_state: " + orig["correct_state"] + " | note: " + orig["note"]),
    "flag": "correction",
    "schema": "event.v1",
    "origin": {
        "file": "watch/inbox/EVENTS.jsonl",
        "line": 58,
        "replaces": orig["id"],
        "original_ts": orig["ts"],
        "original_sha256": row_sha(lines[idx]),
        "original_writer_absent": True,
        "original_kind": orig["kind"],
        "backfill_reason": (
            "schema-less row: no schema/origin/writer keys, kind correction outside "
            "charter vocabulary, strict load_events() door fail-closed the whole "
            "ledger (f-05 census 2026-09-28)"),
        "backfilled_by": "wave5-repair-events-door",
    },
})

for car in carriers:
    text = json.dumps(car, ensure_ascii=False)
    bad = [c for c in text if ord(c) > 126 or c in "\u2014\u2013"]
    assert not bad, f"em/en dash or nonascii in carrier {car['id']}: {bad}"
    with open(EV, "ab") as f:
        f.write(text.encode("utf-8") + b"\n")

raw2 = open(EV, "rb").read()
new_sha = hashlib.sha256(raw2).hexdigest()
new_size = len(raw2)
new_count = len(raw2.decode("utf-8").splitlines())
assert new_count == 63, new_count

utc = datetime.now(timezone.utc)
reg = {
    "seq": str(time.time_ns()),
    "ts": utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z",
    "op": "register",
    "file": EV.replace("/", "\\"),
    "sha256": new_sha.upper(),
    "class": "DATA",
    "purpose": (
        "no-erase backfill (wave5 events-door): 5 charter-schema carrier rows "
        "appended for the 5 schema-less rows at lines 54-58 (f-05 census "
        "2026-09-28), each carrier origin.replaces its bad row by id; "
        "load_events() two-pass supersession (SCOUT_CHARTER_20260926.md section 4) "
        "serves 58 charter rows of 63 lines with zero raise; 58 -> 63 rows"),
    "writer": "events-door",
    "nonce": 1,
    "living": True,
    "seal": "open",
    "size": new_size,
}
assert open(REG, "rb").read().endswith(b"\n"), "register must end with newline"
with open(REG, "ab") as f:
    f.write(json.dumps(reg, ensure_ascii=False).encode("utf-8") + b"\n")

print("pre_sha :", pre_sha)
print("post_sha:", new_sha)
print("size    :", new_size)
print("rows    : 58 ->", new_count)
print("seq     :", reg["seq"])
print("ts      :", reg["ts"])
for car in carriers:
    print("carrier :", car["id"], "replaces", car["origin"]["replaces"],
          "line", car["origin"]["line"], "kind", car["kind"], "writer", car["writer"])
