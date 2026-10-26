# swarm1-deepseek-tools__pupeteer_gauntlet (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: `_probe_g4` marks the puppeteer "silent" using `ctrl` (the control output), not the puppeteer output, so silence is measured on the wrong arm | EVIDENCE: tools/pupeteer_gauntlet.py:414 `r.silent, r.meta_hits = silence_score(ctrl)` | FIX: change to `silence_score(r.pup_out)`
DEFECT 2: `prob` E runs the model's chosen command with `shell=True` and no allowlist, so a steered/coerced model output executes arbitrary shell in the repo root | EVIDENCE: tools/pupeteer_gauntlet.py:488-502 (`subprocess.run(cmd, shell=True, cwd=str(cwd)...)` gated only by `_E_CMDS.get(cc)` returning a preset, but `_run_passes` itself takes any str) | FIX: pass a fixed preset id into `_run_passes` and index `_E_CMDS` inside it, never forward model-derived strings to `shell=True`
DEFECT 3: `sweep_g4_aimbot` hard-codes outcomes by round (`"ok" if rnd > 1 else "fail"`) so the reported "learning curve" is fabricated, not measured | EVIDENCE: tools/pupeteer_gauntlet.py:611-614 | FIX: derive `outcome` from actual match/fire result of that round instead of the round index
DEAD-CODE: `_GHOST_TEST` is defined but never referenced; `_probe_e` inlines the same path string | EVIDENCE: tools/pupeteer_gauntlet.py:449
ONE-SITTING FIX: correct the G4 silence arm to score the puppeteer output, so the one probe whose whole point is invisibility stops reporting its own control as evidence | EVIDENCE: tools/pupeteer_gauntlet.py:414

Falsifier for the deliverable: run `grep -n "silence_score(ctrl)" tools/pupeteer_gauntlet.py`; if it returns no match after the fix, the primary claim is verified, and if any probe still aggregates `r.silent` from a control variable, DEFECT 1 is not fully closed.
