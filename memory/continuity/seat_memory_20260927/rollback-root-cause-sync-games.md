---
name: rollback-root-cause-sync-games
description: Rollback incident root cause — build_vislab_catalog.py sync_games()
  copied dist→games backward (mtime-preserving), fired 2×; permanently inverted
  + drift guard
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

Rollback incident root cause FOUND and PERMANENTLY FIXED (2026-09-16, commit b93c7521b):

`scripts/build_vislab_catalog.py::sync_games()` copied `site/dist/games/*.html →
dashboard/static/games/` via `shutil.copy2` mtime-preserving — derived→canonical. Fired
twice (17:14 and 22:50, pinned by catalog.json mtime), destroying FX4/W5/N9/N10/W1A game
work. The earlier lane's receipt (FX2_SURFACE_RECONCILE.md) had documented the backward
direction as "by-design" — wrong doctrine, now corrected.

**The fix:** sync_games() inverted to canonical→derived; drift guard added (dist
newer+different = refuse and name both files; newer+identical = lockstep skip). Verified:
builder run 3×, canonical zero modifications, drift guard demonstrated live. Law now in
code: canonical flows to derived, never backward.

**Also fixed:** rounds_real.json same backward flow; legacy intra-canonical mirror removed
(never writes into canonical at all now).

Related: [[wave-20260916-night]], [[incident-rollback-20260916]]
