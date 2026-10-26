# WOWHEAD MESH P1 - the clone served through the chunk door (2026-10-07)

Lane: o1-wowhead-mesh, run overnight-mesh-20261007.
Steal-map probe P1 (`watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md` line 89): "serve
wow_manifest knots through mesh_delta's chunk door (the clone becomes a mesh surface, $0)."

## Finish line: LANDED

One knot produced, indexed, chunk-served, sha-verified round trip. $0.

## Exact commands and outputs (all run 2026-10-07 02:07-02:17Z)

### 1. Produce the knots

```
.venv/Scripts/python.exe -m mag.wow_manifest
```

Output (verbatim tail): `"ok": true, "schema": "wow_manifest.v1", "ts": "2026-10-07T02:07:03.206900Z",
"n_invariants": 6, "n_knots": 6` - all six rows `"verkle_knot": true, "rib_published": true,
"rendered": true`.

Produced knot leaves under memory/biography/knots/ (all size 1148 bytes):

- 2026-10-07_0206_wow-manifest_wow_mani_d1d978f7.knot.json  sha256 c8d064e2fa0cc4751876486d2d28ea2558fe2cf79cf0c976305a0f7f341b5a93
- 2026-10-07_0206_wow-manifest_wow_mani_2ca924d4.knot.json  sha256 d333c1b5eeca359db288e57bd582350ef9fec4e0d7fdcdc4ff463dd14828c2c7
- 2026-10-07_0206_wow-manifest_wow_mani_b16839e0.knot.json  sha256 868a0f9aea1dbccd6aaa2cf821fef5db236c7de1846b59fd7a421c57718c9071
- 2026-10-07_0206_wow-manifest_wow_mani_5c95a29e.knot.json  sha256 46f17c7d70612a5ca4d31be400f6cc15f232eb4570b02b616f823369df609298
- 2026-10-07_0206_wow-manifest_wow_mani_2b6f8156.knot.json  sha256 bf7dce8daf86c446e15de3a50e69aa71da51833da7e8795c01875dd538da691f
- 2026-10-07_0207_wow-manifest_wow_mani_c18fcad1.knot.json  sha256 7a35c3a1f7855a4411a73d319e73e10c22a98acb5947c71ea59af6fee78d5ff1

Plus by-session_wow_manifest.json and by-session_rib_bus_wow.json (the RIB layer).
Chain tail: `grep -c wow_manifest memory/biography/verkle_chain.jsonl` = 6.
The served knot is the CONTENT invariant leaf (session_id wow_manifest_5, dossier_commit
c18fcad1, leaf_hash 25c6aac5c8747bc57be70a5181e3eafd34a21e053ad7827e8bb6c04c0cc3b882).

### 2. Index them (incremental scan after producing)

```
.venv/Scripts/python.exe -m tools.mesh_delta scan
```

Output: `{"scanned": 562232, "total_mb": 7280, "ts": "2026-10-07T02:16:53.150270Z", "chain_tip_index": null}`

Verification read of memory/mesh/delta_index.json: all 6/6 knot paths above INDEXED with the
sha256 values listed. Pre-index state: the 01:37:02Z snapshot (561,386 files) predated the knots.

### 3. Serve door + sha-verified round trip

Port 8767 already carried a live seed (PID 24416, command line verified:
`python.exe -m tools.mesh_delta serve --bind 127.0.0.1 --port 8767`). No second server started -
the seed reads delta_index.json from disk per request (tools/mesh_delta.py load_snap, GET /picture),
so my 02:16:53Z scan went live through the existing seed. Index once, serve many.

```
curl -s http://127.0.0.1:8767/picture
```

Output: `{"ts": "2026-10-07T02:16:53.150270Z", "files": 562232, "total_bytes": 7634499095,
"chain_tip_index": null, "chain_tip_ts": null}` - byte-identical to my scan moment.

Client fetch through the mesh_delta client's own guarded transport (`tools.mesh_delta._guarded_fetch`,
loopback allowlisted, IP-pinned):

```
http://127.0.0.1:8767/chunk?path=memory/biography/knots/2026-10-07_0207_wow-manifest_wow_mani_c18fcad1.knot.json&sha=7a35c3a1f7855a4411a73d319e73e10c22a98acb5947c71ea59af6fee78d5ff1
```

Round trip (verbatim):
```
FETCHED bytes: 1148
FETCHED sha256: 7a35c3a1f7855a4411a73d319e73e10c22a98acb5947c71ea59af6fee78d5ff1
INDEX  sha256: 7a35c3a1f7855a4411a73d319e73e10c22a98acb5947c71ea59af6fee78d5ff1
DISK   sha256: 7a35c3a1f7855a4411a73d319e73e10c22a98acb5947c71ea59af6fee78d5ff1
ROUND TRIP MATCH: True
TAMPER REFUSED: HTTP 403 {"error": "refused: outside memory root, over cap, or sha mismatch"}
```

Tamper probe: same path requested with an all-zero sha returned HTTP 403 - the seed's law held.

### 4. Adjacent surfaces (tests)

```
.venv/Scripts/python.exe -m pytest -q tests/test_mesh_delta_guard.py tests/test_wow_manifest.py
```

Output: `9 passed in 1.52s`.

## Findings (negative, first-class)

1. **mesh picture cursor reads null on both fields** (tools/mesh_delta.py:107-108 read
   `tip.get("index")` and `tip.get("generated")`, but memory/biography/verkle_tip.json is
   schema verkle_tip.v1 carrying `n_leaves` / `updated_minute` / `last_filename` - neither
   read key exists). The picture's chain_tip_index / chain_tip_ts are therefore structurally
   null until mesh_delta reads the real key names. Belongs to the mesh_delta organ owner
   (sibling lane); not fixed here, reported instead.
2. **wow_manifest's own row output carries empty knot_root/verkle_root** (mag/wow_manifest.py
   reads `k.get("root")` / `st.get("root")` - the append_verkle_knot return and status() do not
   surface a root under those keys in this path). Harmless to the finish line (the leaves and
   chain carry the real hashes), cosmetic gap in the manifest report.
3. The serve door was already occupied by a sibling's seed on 127.0.0.1:8767; reused, not
   replaced. Deviation from "run serve" in the letter only: the door exercised is the same
   tool, bind, and port the task names, and the served snapshot is this lane's scan.
