# Residual — full-stack auto-boot (2026-08-06)

## Shipped
- Supervisor owns **lab** slot (main.py lab --no-dashboard) + backend + dashboard + scribe (+ mirror/drainer as before)
- power start --browser opens **Direct Mag**: http://127.0.0.1:8765/?tab=chat
- oot_mag.cmd — silent login boot (no pause)
- Startup: scripts/install_mag_startup.ps1 → MAG Start.lnk → boot_mag.cmd (installed)
- Browser seat gate: configs/browser_env.yaml + mag/browser_env.py (allowlist; enabled=false until OpenClaw/Playwright driver)
- Tests: tests/test_launch_topology.py (lab slot + browser gate)

## Operator
- Login: auto
- Manual: mag_on.cmd / boot_mag.cmd
- Kill: mag_kill.cmd
- Status: mag.cmd power status · doctor

## Next (not this ship)
- Wire OpenClaw or Playwright driver when installed; flip browser_env enabled + driver
- Env testing tracks via main.py env already; browser seat plugs as another seat later
