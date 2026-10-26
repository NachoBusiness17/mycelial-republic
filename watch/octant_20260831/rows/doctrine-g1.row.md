# ROW doctrine-g1

- **pointer**: mag/switchboard_v2.py, mag/harness.py, mag/swarm_cycle.py
- **claim**: POSTED has zero hits in mag code; classify() has no pipeline caller
- **type**: gopher
- **confidence**: H
- **status**: VERIFIED
- **evidence**: `grep -n "POSTED"` → 0 hits across 3 files. classify() only defined (switchboard_v2.py:108) + called by cmd_classify CLI (switchboard_v2.py:716-717); no pipeline caller.
