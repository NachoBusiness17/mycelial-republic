# ROKU IGNITION - the Republic on the TV (the unused Roku)

**What's built:** `roku_channel/` + `republic_channel.zip` (the estate tree) - a SceneGraph channel that renders the live beacon on the TV: the lattice cells (heat, money, reputation), then the artifact board (skills, mcp-servers, organs, receipts, prices in GSTD). It refreshes every 60 seconds from `http://192.168.86.35:8777/beacon.json` (the beacon now serves on ALL interfaces: LAN + tailnet, both verified serving).

**The hard truth, scoped:** a Roku is a TERMINAL, not a node. BrightScript sandbox, no shell, no python - the harness will never run on it. But the install base is planetary (tens of millions of sticks), and a channel that renders the Republic's live economy is the distribution surface: every Roku on earth is one Channel Store approval away from showing the swarm.

**What needs hands (10 seconds, the unused Roku's remote):**

1. Wake the unused Roku. Press on its remote: **Home x3, Up x2, Right, Left, Right, Up, Right** -> the Developer Settings screen appears.
2. Select "Enable installer and restart", set the web password to: **gstd**
3. Note the Roku's name/IP it shows (or tell me which of the three is unused: Ultra .52, Premiere+ .53, Stick .85).

**Then I sideload from the desktop (no further hands):**

```
curl --user rokudev:gstd -F "mysubmit=Install" -F "archive=@republic_channel.zip" http://<roku-ip>/plugin_install
```

The channel installs, launches, and the TV renders the Republic live: THE DISTRIBUTED REPUBLIC - the beacon - the lattice - the artifact board - refreshed every minute.

**Model note:** all three (Ultra, Premiere+, Stick) run Roku OS with SceneGraph support; the Stick is the weakest render target but the layout is plain labels - it renders on anything.

## Falsifier

The sideload claim dies if the dev installer rejects the package (a BrightScript syntax error shows as a compile error in the installer response - the channel is written to minimum-common-denominator SceneGraph to avoid this). The render claim dies if the Roku cannot reach 192.168.86.35:8777 (same LAN - it can).
