# mag-estate (Hermes plugin v0, DRAFT)

Read-only tools over Mag organs. Install (local):
1. Copy this folder to `<HERMES_HOME>/plugins/mag-estate/` (Windows: `%LOCALAPPDATA%\hermes\plugins\mag-estate`).
2. `hermes plugins enable mag-estate`
3. Set `plugins.entries.mag-estate.settings.mag_root` to your Mag checkout (or env MAG_ROOT).
4. `hermes plugins doctor mag-estate --ci`

Tools: mag_chain_verify, mag_receipt_validate, mag_notices, mag_leases. Skills: mag-estate:mag-tri-state-receipts, mag-estate:mag-self-steal.
Requires a Mag checkout that includes the (currently untracked) organs mag/fleet_report.py and mag/leases.py; see watch/LIBRARY/STEAL_HERMES_PLUGIN_20261020.md.
