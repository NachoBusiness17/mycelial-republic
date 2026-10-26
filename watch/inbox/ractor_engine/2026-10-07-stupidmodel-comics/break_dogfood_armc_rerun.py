#!/usr/bin/env python3
"""break-dogfood hostile re-fire of arm C (same probe, new output path).

Verifies reproducibility of the dogfood lens's load-bearing number: remote
free seats + response_format json_object -> high spec_valid rates. Does NOT
touch probe_dogfood_arm_c_results.json (the lens's artifact stays byte-their;
this rerun writes its own file). $0 free lanes, urllib only, no subprocess
spawns (win32 CREATE_NO_WINDOW law satisfied by construction).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import probe_dogfood_arm_c as m  # noqa: E402

m.OUT = HERE / "break_dogfood_armc_rerun_results.json"
raise SystemExit(m.main())
