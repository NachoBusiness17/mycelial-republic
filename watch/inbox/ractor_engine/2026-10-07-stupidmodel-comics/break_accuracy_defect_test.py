"""Defect unit test v2: 3-panel payloads so the bubbles loop is actually reached."""
from pathlib import Path

DIR = Path(__file__).resolve().parent
src = (DIR / "probe_panel_spec.py").read_text(encoding="utf-8")
ns: dict = {"__file__": str(DIR / "probe_panel_spec.py"), "__name__": "probe_mod"}
exec(compile(src, str(DIR / "probe_panel_spec.py"), "exec"), ns)
score = ns["score"]

good_panel = '{"caption":"c","characters":["a"],"bubbles":[{"who":"a","text":"hi"}]}'
null_panel = '{"caption":"c","characters":["a"],"bubbles":null}'
payload_null = '{"title":"T","panels":[' + ",".join([good_panel, null_panel, good_panel]) + "]}"
payload_ok = '{"title":"T","panels":[' + ",".join([good_panel] * 3) + "]}"

for name, p in (("3-panel bubbles:null", payload_null), ("3-panel well-formed", payload_ok)):
    try:
        out = score(p)
        print(f"{name}: spec_valid={out['spec_valid']} (no crash)")
    except TypeError as e:
        print(f"{name}: RAISES TypeError: {e}")

# fixed scorer: guard the loop, same payloads
import re as _re
fixed = src.replace("                for b in bub:", "                for b in (bub if isinstance(bub, list) else []):")
ns2: dict = {"__file__": str(DIR / "probe_panel_spec.py"), "__name__": "probe_mod"}
exec(compile(fixed, "fixed", "exec"), ns2)
for name, p in (("FIXED 3-panel bubbles:null", payload_null), ("FIXED 3-panel well-formed", payload_ok)):
    out = ns2["score"](p)
    print(f"{name}: parses={out['parses']} spec_valid={out['spec_valid']}")
