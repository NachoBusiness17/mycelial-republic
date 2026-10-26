import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")))
from mag.fleet_report import file_report
r = file_report(seat="grokbot-mag", kind="NOTICE", model="grokbot", report={
 "notice_id": "N-20261019-fish-tank-and-estate-hardening",
 "category": "law_change",
 "subject": "Fish-tank remediation landed; assume-breach hardening findings",
 "affects": ["ollama", "gstd_beacon", "cast_server", "mag-mcp", "chain:biography", "all seats"],
 "narrative": ("FISH TANK (watch/LIBRARY/FISH_TANK_REMEDIATE_20261019.md): Ollama now binds 127.0.0.1:11434 (container still reaches it via host.docker.internal). "
  "gstd_beacon defaults to loopback; LAN/Roku exposure needs GSTD_BEACON_LAN=1 plus a live 'expose:lan' lease and shuts itself down at expiry. "
  "cast --lan now uses 8767 (8766 = compose mag-mcp). platform_kill --lan-expired reaps LAN exposure. Untrusted LAN peers are display-only and logged in cast_probes.jsonl. "
  "PENDING: elevated scripts/host_lockdown_fish_tank_20261019.ps1 (portproxy 8765, sshd tailnet-only, block LAN 8080). "
  "HARDENING (watch/LIBRARY/STEAL_ESTATE_HARDENING_20261019.md): 1 tip witness dark since 10-18 (gist 403); 2 all chain backups same disk, offsite unscheduled; "
  "3 memory/biography Modify ACL for CodexSandboxUsers + 5 SIDs; 4 AdjudicationBus runs code from another user profile; 5 no scheduled chain verify; "
  "6 no egress notice; 7 seat handshake off; 8 factorio wildcard listeners."),
 "action_required": ("Seats: do not run the beacon or cast --lan without an expose:lan lease; call Ollama on loopback only. "
  "Do not treat local backups as tamper evidence until the witness is green. Operator items (credential, ACL, offsite medium, AdjudicationBus) await Nacho. ACK this notice."),
 "in_force_until": "until_cancelled"})
print(json.dumps(r, default=str)[:600])
