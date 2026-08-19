"""RIB-verify the focus_anchor braid: weave task steps + tangents in order, recover the whole braid.
Writes results to braid_test.out so we can read them even if the terminal output capture is wedged."""
import json
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mag import focus_anchor as fa

importlib.reload(fa)
out = []
T = "Untie the knot: weave tangents into a braid so we never lose the thread"
out.append(("anchor", fa.anchor(T)))
w1 = fa.weave("Running T2 coherence on the invariant tool", T)
w2 = fa.weave("also we should redesign the dashboard and imagine a future roadmap", T)
w3 = fa.weave("Now back to the invariant test, measuring the stable prefix", T)
w4 = fa.weave("and another thought about the gpu rightsize branch", T)
r = fa.recover(T)
out.append(("beads", [(b["type"], b["text"][:40]) for b in r["braid"]]))
out.append(("braid_len", r["braid_len"]))
out.append(("tangents_logged", (w2.get("logged"), w4.get("logged"))))
out.append(("status", fa.status()))
Path(__file__).parent.joinpath("braid_test.out").write_text(
    json.dumps(out, indent=2, default=str), encoding="utf-8")
