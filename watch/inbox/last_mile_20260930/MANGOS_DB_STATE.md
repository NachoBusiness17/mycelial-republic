# Mangos MariaDB state receipt (2026-09-30)

Operator asked why mysqld had run 1254 minutes. Answer, byte-verified:

- `mysqld.exe` (MariaDB 13.0), PID 19748, started 2026-09-29 08:46:49 — the SRP6/realmd auth lane window.
- Data dir `C:\Program Files\MariaDB 13.0\data` holds `mangos` + `characters` — the CMaNGOS world/character databases the realmd auth tests ran against.
- Zero ESTABLISHED connections at check time; NOT a Windows service (manual start by the lane, never stopped).
- Resolved: the orphaned background task was killed 2026-09-30, process tree went with it, RAM reclaimed. Databases untouched on disk.

## The anti-forget law

Bring it back with ONE command (this is why the script exists — the estate forgets orphaned dependencies):

    scripts\start_mangos_db.cmd

Stop with: `mysqladmin -u root shutdown`. Port 127.0.0.1:3306, localhost-only. Needed only when sovereign-server lanes resume the mangos backend (realmd auth, characters persistence); the estate's own server/ (water-graph world) does NOT use it.
