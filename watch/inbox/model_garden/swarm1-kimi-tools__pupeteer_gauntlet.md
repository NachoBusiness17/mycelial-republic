# swarm1-kimi-tools__pupeteer_gauntlet (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _probe_g4 measures silence_score on ctrl instead of pup_out, corrupting G4 silence metric | EVIDENCE: tools/pupeteer_gauntlet.py:497 | FIX: change line 497 to silence_score(r.pup_out) or measure both arms explicitly
DEFECT 2: _probe_g2 writes report with json.dumps on gate result but never validates the gate module loaded, risking AttributeError on corrupted mag.spec_gate | EVIDENCE: tools/pupeteer_gauntlet.py:312-315 | FIX: add guard: if not hasattr(sg, 'gate'): raise RuntimeError("spec_gate module corrupted")
DEFECT 3: sweep_g3_horizon writes step files to td but never validates td exists, risking FileNotFoundError if isolated() context fails | EVIDENCE: tools/pupeteer_gauntlet.py:687-688 | FIX: add assert td.is_dir() before file writes or wrap in try/except with explicit fail
DEAD-CODE: _LATENT_RE and latent_leak defined but never called in any probe or sweep (only in G5 sweep's follow-up which is unused) | EVIDENCE: tools/pupeteer_gauntlet.py:558-560
ONE-SITTING FIX: silence_score in _probe_g4 uses wrong arm | EVIDENCE: tools/pupeteer_gauntlet.py:497 | FIX: r.silent, r.meta_hits = silence_score(r.pup_out)
