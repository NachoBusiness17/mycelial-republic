"""R1 wave_20260916 — bounded swarm-research pass via mag.research_fanout (fallback path).

Falls back from `main.py swarm` (hardwired provider=deepseek, ghost-queue, paid-entangled).
Overrides the module BATTERY with a 12-question myco-memory battery; probe-first; live
lanes only; free lanes only ($0). Outputs land in the wave dir, not the WoW research log.
Run with .venv\\Scripts\\python.exe ONLY.
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
WAVE = ROOT / "watch" / "inbox" / "wave_20260916"
sys.path.insert(0, str(ROOT))

from mag import research_fanout as rf  # noqa: E402

MYCO_12 = [
    ("M01", "myco-memory",
     "Electrical impulse propagation in fungal mycelium: which species and which papers "
     "(e.g. Adamatzky and colleagues) report measured action-potential-like spikes in mycelium? "
     "Give concrete numbers: spike amplitude range (mV), duration (ms), propagation velocity, "
     "frequency of firing. What amplifier and electrode setup recorded them?"),
    ("M02", "myco-memory",
     "Habituation and sensitization in fungi and slime molds: what are the measured timescales "
     "of behavioral habituation (repeat-stimulus experiments) in Physarum polycephalum and in "
     "higher fungi? What do those latencies imply for achievable read/modify latencies of a "
     "biological memory element? Cite specific experiments and numbers."),
    ("M03", "myco-memory",
     "Reservoir computing on physical substrates: how is a physical/biological substrate used as "
     "a reservoir (input encoding, readout layer training, benchmark tasks like NARMA or XOR)? "
     "What has been demonstrated specifically with slime mold or fungal substrates as reservoirs, "
     "and what readout hardware/software was used? Cite papers and numbers."),
    ("M04", "myco-memory",
     "Physarum transport-network adaptation: what is the measured timescale for network "
     "reconfiguration (hours?), what is the reinforcement rule (tube thickening with flux), and "
     "what is the shortest reported adaptation time? Design what an experiment would look like "
     "in a confined 3D substrate cube with embedded electrodes to use this as rewritable memory."),
    ("M05", "myco-memory",
     "Fungal and organic memristors: describe the resistive-switching mechanism reported for "
     "fungal/fruit-body memristors (Adamatzky) and for OhmSh/phase-change style organic memristors. "
     "Concrete numbers: write voltage, set/reset pulse widths, on/off ratio, retention time, "
     "endurance cycles. What is physically storing the bit?"),
    ("M06", "myco-memory",
     "Organic electrochemical transistors (OECTs) as living-tissue interfaces: how do PEDOT:PSS "
     "OECTs transduce ionic currents into electronic currents? Operating voltages, response time, "
     "transconductance, and reported uses for recording from living biological systems. What would "
     "integrating OECT probes into a fungal substrate require?"),
    ("M07", "myco-memory",
     "Extracellular recording instrumentation for bio substrates: which electrode materials and "
     "geometries (Ag/AgCl, Pt, stainless steel, silicone-embedded) are used for mycelium/slime-mold "
     "electrophysiology, with how many channels, and what noise floor (uVrms) do hobbyist vs lab "
     "amplifiers achieve? Name specific rigs (Backyard Brains SpikerBox, OpenBCI, Intan)."),
    ("M08", "myco-memory",
     "Evidence of short-term vs long-term memory in slime molds and fungi: habituation lasting "
     "days-weeks, Physarum memory imprinting of resource location via tube architecture (trained "
     "tubes experiments). For each: how long does the memory persist, and what physical medium "
     "stores it (cytoplasmic flow history, hyphal topology, metabolite gradients)?"),
    ("M09", "myco-memory",
     "Proposed coding schemes for fungal electrical signals: spike-train frequency coding, "
     "amplitude coding, Adamatzky's 'fungi language' word/ sentence length analysis. What "
     "statistical critiques apply to linguistic-structure claims on such data, and what control "
     "experiments would separate structure from noise? Cite both the claims and the critiques."),
    ("M10", "myco-memory",
     "Growth-rate control as rewritable structural memory: measured hyphal growth rates (mm/day) "
     "for common cube species (Pleurotus ostreatus, Ganoderma, oyster/ reishi), and how moisture, "
     "temperature, nutrients, light, and physical barriers measurably redirect growth within days. "
     "What imaging (time-lapse, transparent substrate) captures topology as a state variable?"),
    ("M11", "myco-memory",
     "Cheapest open hardware for multi-channel bio-electrical recording: Backyard Brains, OpenBCI "
     "Ganglion/Cyton, Intan RHD, ADS1299 boards. For a 10 cm mycelium cube instrumented at ~1 kHz "
     "with 8-16 electrodes: what exact stack, total BOM cost, and sampling specs? Include the "
     "software stack for streaming/ logging."),
    ("M12", "myco-memory",
     "Compare candidate read/write mechanisms for a mycelium memory cube by concrete numbers: "
     "(a) extracellular spike readout, (b) impedance spectroscopy of hyphal network, (c) growth-"
     "topology imaging, (d) hybrid OECT/memristor interface. For each: bandwidth, latency, "
     "durability, invasiveness, maturity. Which write+read PAIRS are physically plausible today, "
     "and which are speculative? Be blunt."),
]

rf.SYSTEM = (
    "You are a research digger for a bio-hardware project (an instrumented mycelium cube used as "
    "a memory hierarchy). Answer with CONCRETE, checkable material: names, authors/papers, "
    "numbers (voltages, ms, mm/day, cycles, dollars), materials, and vendor/stack names. Cite "
    "mechanisms, not visions. If you do not know a number, write UNKNOWN rather than inventing it."
)

rf.BATTERY = MYCO_12
# keep the WoW research log clean: redirect outputs into the wave dir
rf.OUT = WAVE / "r1_fanout_runs"
rf.RAW = rf.OUT / "raw.jsonl"
rf.PACK = rf.OUT / "pack.md"

probe = rf.probe_lanes()
print("PROBE live:", probe.get("live"), "dead:", probe.get("dead"), flush=True)
live_ids = set(probe.get("live") or [])
rf.LANES = [l for l in rf.LANES if l["id"] in live_ids]

if live_ids:
    run = rf.run(workers=6, timeout=150)
else:
    run = {"ok": False, "error": "all lanes dead at probe"}

out = {"probe": probe, "run": run,
       "battery": [{"id": i, "theme": t, "q": q} for i, t, q in MYCO_12]}
dest = WAVE / "r1_swarm_research_out.json"
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print("WROTE", dest, flush=True)
print("ANSWERED:", run.get("answered"), "FAILED:", run.get("failed"),
      "LANES:", run.get("lanes_used"), flush=True)
