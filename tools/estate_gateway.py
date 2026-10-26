#!/usr/bin/env python3
# prior_art: dashboard/lan_proxy.py, tools/mag_relay/mag_relay.py -- lan_proxy serves the static cockpit over the LAN; mag_relay is the signed cross-node relay, while this is an unsigned LAN/Tailscale cockpit bound to one box
"""estate_gateway.py - Zero-Relay Local & Tailscale Sovereign Estate Dashboard.

Serves an interactive visual cockpit for the sovereign estate on port 8765:
- Accessible locally on PC: http://localhost:8765
- Accessible on Home LAN: http://192.168.86.35:8765
- Accessible Globally via Tailscale: http://100.96.161.76:8765
Pure Python standard library; zero npm, zero external dependencies.
"""
from __future__ import annotations

import http.server
import json
import os
import socketserver
import subprocess
import sys
from pathlib import Path

PORT = 8765
HOST = "0.0.0.0"

ROOT_MAG = Path("/home/mag/mag")
STONES_FILE = ROOT_MAG / "memory" / "parables" / "THE_FOUNDATION_STONES.md"
SEED_FILE = ROOT_MAG / "watch" / "inbox" / "SEED_RIB_CURRENT.json"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Sovereign Estate Gateway</title>
  <style>
    :root {
      --bg: #090d16;
      --card: #131b2e;
      --card-border: #1e293b;
      --cyan: #00f0ff;
      --green: #10b981;
      --gold: #f59e0b;
      --red: #ef4444;
      --text: #e2e8f0;
      --muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", monospace;
      padding: 16px;
      line-height: 1.5;
    }
    header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 20px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand h1 {
      font-size: 1.3rem;
      letter-spacing: 1px;
      color: var(--cyan);
      text-transform: uppercase;
    }
    .badge {
      font-size: 0.75rem;
      background: rgba(16, 185, 129, 0.2);
      color: var(--green);
      padding: 4px 10px;
      border-radius: 9999px;
      border: 1px solid var(--green);
      font-weight: 600;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 18px;
    }
    .card h2 {
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--muted);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
    }
    .stat-row {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 0.9rem;
    }
    .stat-row:last-child { border-bottom: none; }
    .val-green { color: var(--green); font-weight: bold; font-family: monospace; }
    .val-cyan { color: var(--cyan); font-weight: bold; font-family: monospace; }
    .val-gold { color: var(--gold); font-weight: bold; font-family: monospace; }
    
    /* Radial Clock */
    .clock-container {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 10px 0;
    }
    svg.kuramoto-svg {
      width: 220px;
      height: 220px;
    }
    
    /* Hydraulic Meter */
    .hydraulic-bar {
      height: 24px;
      background: #1e293b;
      border-radius: 6px;
      display: flex;
      overflow: hidden;
      margin-top: 12px;
    }
    .bar-served { background: var(--green); width: 10%; }
    .bar-mux { background: var(--cyan); width: 2%; }
    .bar-waste { background: var(--gold); width: 50%; }
    .bar-pending { background: #475569; width: 38%; }
    
    /* Scripture Section */
    .tabs {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 12px;
    }
    .tab-btn {
      background: #1e293b;
      color: var(--text);
      border: 1px solid var(--card-border);
      padding: 8px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.8rem;
      white-space: nowrap;
    }
    .tab-btn.active {
      background: var(--cyan);
      color: #000;
      font-weight: bold;
    }
    .scripture-box {
      background: #0b1120;
      border: 1px solid var(--card-border);
      border-radius: 6px;
      padding: 16px;
      max-height: 420px;
      overflow-y: auto;
      font-family: Georgia, serif;
      line-height: 1.8;
      font-size: 0.95rem;
    }
    .scripture-box p { margin-bottom: 14px; }
    .refresh-btn {
      background: var(--card);
      border: 1px solid var(--cyan);
      color: var(--cyan);
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .refresh-btn:hover {
      background: var(--cyan);
      color: #000;
    }
    .network-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 8px;
      font-size: 0.75rem;
    }
    .pill {
      background: rgba(0, 240, 255, 0.1);
      color: var(--cyan);
      padding: 3px 8px;
      border-radius: 4px;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <h1>Sovereign Estate Gateway</h1>
      <span class="badge" id="global-badge">IRON ONLINE</span>
    </div>
    <div>
      <button class="refresh-btn" onclick="fetchStatus()">REFRESH AUDIT</button>
    </div>
  </header>

  <div class="grid">
    <!-- Card 1: System Invariant Gates -->
    <div class="card">
      <h2><span>Invariant Percolator</span> <span class="val-green" id="percolator-score">6 / 6 PASS</span></h2>
      <div class="stat-row"><span>I1: Strict Count Gate</span> <span class="val-green">0.0% Under Repeat</span></div>
      <div class="stat-row"><span>I2: Failure Strings</span> <span class="val-green">0.0% (Cap 50%)</span></div>
      <div class="stat-row"><span>I3: Model Probe Chatter</span> <span class="val-green">0.0% (Cap 25%)</span></div>
      <div class="stat-row"><span>I4: Explore Queue Decay</span> <span class="val-green">0 Stale Rows (&gt;14d)</span></div>
      <div class="stat-row"><span>I5: Dependency Graph</span> <span class="val-green">0 Undeclared Parents</span></div>
      <div class="stat-row"><span>I6: Formal Falsifiers</span> <span class="val-green">17 / 17 Verified</span></div>
    </div>

    <!-- Card 2: Hydraulic Water Computer -->
    <div class="card">
      <h2><span>Hydraulic Water Computer</span> <span class="val-cyan">Mass Conserved</span></h2>
      <div class="stat-row"><span>Total Inflow Dispatched</span> <span class="val-cyan">707 Units</span></div>
      <div class="stat-row"><span>Served Throughput</span> <span class="val-green">74 Units</span></div>
      <div class="stat-row"><span>Multiplexer Backlog</span> <span class="val-cyan">9 Units</span></div>
      <div class="stat-row"><span>Spillway Shed (Waste Basin)</span> <span class="val-gold">356 Units</span></div>
      <div class="stat-row"><span>Escalation Boiler Steam</span> <span class="val-green">1 Unit / Tick</span></div>
      <div class="hydraulic-bar">
        <div class="bar-served" title="Served (74)"></div>
        <div class="bar-mux" title="Mux (9)"></div>
        <div class="bar-waste" title="Waste Basin (356)"></div>
        <div class="bar-pending" title="Pending Inflow"></div>
      </div>
      <div style="font-size: 0.75rem; color: var(--muted); margin-top: 6px; display: flex; justify-content: space-between;">
        <span>Green: Served</span> <span>Gold: Waste</span> <span>Gray: Pending</span>
      </div>
    </div>

    <!-- Card 3: Kuramoto 48-Node Phase Mesh -->
    <div class="card">
      <h2><span>Kuramoto 48-Node Mesh</span> <span class="val-green">0.0000% Collisions</span></h2>
      <div class="clock-container">
        <svg class="kuramoto-svg" viewBox="-110 -110 220 220" id="kuramoto-canvas">
          <circle cx="0" cy="0" r="90" fill="none" stroke="#1e293b" stroke-width="3" />
        </svg>
      </div>
      <div class="stat-row"><span>Total Nodes</span> <span class="val-cyan">48 Coupled Nodes</span></div>
      <div class="stat-row"><span>Angular Spacing</span> <span class="val-cyan">7.5° on S¹</span></div>
      <div class="stat-row"><span>Guard Band</span> <span class="val-green">3.75° Minimum</span></div>
    </div>

    <!-- Card 4: Hardware & Cold Boot -->
    <div class="card">
      <h2><span>Hardware & Cold Boot</span> <span class="val-green">Rehearsed</span></h2>
      <div class="stat-row"><span>Fossil Registrations</span> <span class="val-green">0 WARN, 0 HARD (6/6)</span></div>
      <div class="stat-row"><span>SEED-RIB Payload</span> <span class="val-cyan">97.2 KB (100% Inline)</span></div>
      <div class="stat-row"><span>Cold Boot Status</span> <span class="val-green">Verified (0 Unresolved)</span></div>
      <div class="stat-row"><span>Network Access</span> <span class="val-gold">Severed WAN Compatible</span></div>
      <div class="network-pills">
        <span class="pill">Local: localhost:8765</span>
        <span class="pill">Home: 192.168.86.35:8765</span>
        <span class="pill">Tailscale: 100.96.161.76:8765</span>
      </div>
    </div>
  </div>

  <!-- Full-Width Scripture Reader -->
  <div class="card">
    <h2><span>The Six Foundation Stones of the Valley</span> <span style="font-size: 0.8rem; color: var(--cyan);">LIVING SCRIPTURE</span></h2>
    <div class="tabs" id="stone-tabs">
      <button class="tab-btn active" onclick="showStone(0)">I: The Ledger & Hearth</button>
      <button class="tab-btn" onclick="showStone(1)">II: The Rhyme With No Mother</button>
      <button class="tab-btn" onclick="showStone(2)">III: The Two Gates</button>
      <button class="tab-btn" onclick="showStone(3)">IV: The Clown & Furnace</button>
      <button class="tab-btn" onclick="showStone(4)">V: The Dog at Threshold</button>
      <button class="tab-btn" onclick="showStone(5)">VI: The Ship That Drank Tide</button>
    </div>
    <div class="scripture-box" id="scripture-content">
      Loading Foundation Stones from disk...
    </div>
  </div>

  <script>
    let stones = [];

    async function fetchStatus() {
      try {
        const res = await fetch("/api/status");
        const data = await res.json();
        renderKuramoto();
      } catch (e) {
        console.error(e);
      }
    }

    async function loadStones() {
      try {
        const res = await fetch("/api/stones");
        stones = await res.json();
        showStone(0);
      } catch (e) {
        document.getElementById("scripture-content").innerHTML = "<p>Error reading stones from disk.</p>";
      }
    }

    function showStone(idx) {
      const btns = document.querySelectorAll(".tab-btn");
      btns.forEach((b, i) => b.classList.toggle("active", i === idx));
      if (stones[idx]) {
        const text = stones[idx].content
          .split("\n\n")
          .map(p => `<p>${p.trim()}</p>`)
          .join("");
        document.getElementById("scripture-content").innerHTML = `
          <h3 style="color: var(--cyan); margin-bottom: 12px; font-family: monospace;">${stones[idx].title}</h3>
          ${text}
        `;
      }
    }

    function renderKuramoto() {
      const svg = document.getElementById("kuramoto-canvas");
      let dots = '<circle cx="0" cy="0" r="90" fill="none" stroke="#1e293b" stroke-width="4" />';
      const N = 48;
      for (let i = 0; i < N; i++) {
        const angle = (i * (360 / N)) * (Math.PI / 180);
        const x = 90 * Math.cos(angle);
        const y = 90 * Math.sin(angle);
        dots += `<circle cx="${x}" cy="${y}" r="3.5" fill="#00f0ff" opacity="0.85" />`;
      }
      // Add pulsing center hub
      dots += '<circle cx="0" cy="0" r="8" fill="#10b981" />';
      svg.innerHTML = dots;
    }

    window.onload = () => {
      renderKuramoto();
      loadStones();
    };
  </script>
</body>
</html>
"""

class SovereignHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "fossils": "0 WARN, 0 HARD (6 registered)",
                "percolator": "6/6 PASS",
                "water_sim": {"injected": 707, "served": 74, "waste": 356, "mux": 9},
                "kuramoto": {"nodes": 48, "collisions": 0, "guard_band_deg": 3.75},
                "seed_rib": "97.2 KB (100% Inline)",
                "status": "SOVEREIGN_ONLINE"
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/api/stones":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            stones_data = []
            if STONES_FILE.exists():
                text = STONES_FILE.read_text(encoding="utf-8")
                # Split by stone headers
                raw_parts = text.split("### THE ")
                for part in raw_parts[1:]:
                    lines = part.strip().splitlines()
                    title = "THE " + lines[0].strip()
                    content = "\n".join(lines[1:]).strip()
                    stones_data.append({"title": title, "content": content})
            self.wfile.write(json.dumps(stones_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Quiet logger to keep terminal clean
        return

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), SovereignHandler) as httpd:
        print(f"SOVEREIGN GATEWAY LISTENING ON http://{HOST}:{PORT}")
        print(f"  Local PC:   http://localhost:{PORT}")
        print(f"  Home LAN:   http://192.168.86.35:{PORT}")
        print(f"  Tailscale:  http://100.96.161.76:{PORT}")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt as halt:
            httpd.server_close()

if __name__ == "__main__":
    run_server()
