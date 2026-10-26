# LINK-DROP receipt: Teknium's Hermes Workshop device catalog

- Dropped: 2026-10-06, X post https://x.com/Teknium/status/2107301976291909994 (02:48 UTC)
- Fetched: fxtwitter API (verbatim text) + direct page fetch (teknium.io/hermes-devices, 1,745,150 bytes HTML) + og image (578,317 bytes JPG), same sitting
- LINKS row: seq 1791313495095294, canonical sha256 39C65FF3297603627672E63A2CAF2179F73412651FF729B656EA96A943DD7708
- Verdict: STEAL. Independent authorship (Teknium is not the operator), so the convergence counts as evidence, not genealogy.

## What it IS (from its own bytes)

Tweet, verbatim: "Just made this cool catalog with a ton of open platform hardware, devices and more that your Hermes Agent (or any agent really) can build on, integrate with, or live inside!"

Page meta description, verbatim: "A showcase of 300+ open, hackable, API-driven devices an AI agent (Hermes) can own, program and maintain - robots, handhelds, keyboards, synths, sensors and more, each with worked-up project ideas."

Page title: "The Hermes Workshop - a showcase of hardware for an agent with hands". Section taglines read off the page: "Every gadget, one brain." / "Every device has a real local interface" / "Hermes owns, builds, maintains".

## Census (this sitting)

- ~365 section/device headings across ~40 categories: Hermes-native gadgets (M5Stack CoreS3 ~$60), MCU boards, SBC/edge AI (Pi 5, Jetson Orin Nano Super, Hailo-8L), retro/FPGA/handhelds, robots (Unitree Go2/G1, LeRobot SO-101, Reachy Mini, Stack-chan, Open Duck Mini), synths/DSP, wearables, focus/status gadgets, keyboards, LED/pixels, displays ("Hermes Paints": TRMNL BYOS, InkyPi, Inkplate), audio, voice (HA Voice PE, xiaozhi-esp32), local-first smart home, "The Control Spine" (Home Assistant MCP Server, ESPHome, Zigbee2MQTT, Mosquitto, Node-RED), network, IP-KVM "Remote Hands" (PiKVM, JetKVM), 3D printing, CNC/laser, PCB pipeline, bench instruments, radio/SDR/mesh (Meshtastic, MeshCore, Reticulum, T-Lora Pager ~$87), security tools, surveillance, covert gadgets, pocket Linux/cyberdecks (uConsole, MNT Pocket Reform, Beepy), workshop ops, plus "Firmware & Agent Projects" (Hermes Gadget SDK, Hermes Familiar, ESP-Hermes channel, Caduceus robot, hermes32, hermes-agent-iot).
- 660 h4/h5 blocks; each device card carries price, hack-depth rating, "HOW HERMES PLUGS IN" (concrete commands: SSH in and script it, drive its HTTP API, build Verilog cores via Quartus), and "USE CASES WE WORKED UP" 4-6 numbered ideas.
- Interface chip taxonomy off the screenshot: REST 112, Python 80, Serial 94, SSH 48, MQTT 40, BLE 50, Home Assistant 33, USB 28, CLI 28, Wi-Fi 26, ESPHome 23, Arduino 23, USB HID 15, WebSocket 15, ESP-IDF 15, MCP 10, I2C.

## Estate mapping

1. The interface chip bar IS task_shape-for-hardware: a coordinate system (REST/Python/SSH/MQTT/MCP/serial) an agent navigates by capability, exactly the GPS-for-problems shape the operator flow-stated 10-05. The catalog is a GPS ledger where every row is a body.
2. 4th same-week convergence on "agents get bodies": Hermes 68 profiles (cast system, 10-04), Pixel 11 body (10-02), GSTD full-dogfood plan with per-device wallets (10-05), now a vendor-grade hardware index (10-06). The estate thesis keeps being arrived at independently, from outside this time.
3. "Every device has a real local interface" + agent-owns-builds-maintains is the estate's local-first / T0-T1-stays-local law and its ARMORY doctrine (map not payload, graduated index) shipped as a public product page. The STARTER KIT's hardware page writes itself from this census.
4. "Hermes Familiar / ESP-Hermes / hermes-agent-iot" = a device-side agent runtime protocol; the estate's liquid-familiar line (Mag, Calcifer) and the GSTD node-lite/Termux phone plan are the same organ. WATCH the protocol, steal the shape.

## Steal rows (one seat one sitting each)

- S1 Control Spine, high: Home Assistant MCP Server as the actuator plane. The estate law says model text proposes and only the switchboard/effect broker authorizes effects; an HA MCP server is a broker-shaped surface with 33-odd HA-listed devices and 10 MCP-chip devices. One sitting: point a mag MCP client at a test HA instance and bank one authorized-then-executed effect with a receipt.
- S2 Remote hands, high: PiKVM/JetKVM is the hardware answer to the bob seam (bob is SMB-auth-walled, no remote exec, newest-session grabs must run on bob). One sitting: spec the bob KVM row (device, cost ~$100-150, what it unlocks: BIOS-level seat control for the second node) into the operator dawn queue; purchase stays operator-gated.
- S3 Estate dash body, medium: TRMNL BYOS / InkyPi / Inkplate e-ink ("Hermes Paints") = the dawn report and estate_walk on an always-on ~$80 screen. One sitting: InkyPi pointing at the dashboard's JSON doors; a pull-cadence law keeps it read-only.
- S4 Primer shape, medium: LilyGO T-Deck Plus ~$71 is the tangible-pocket-terminal the Diamond Age moonshot leg described (a book that talks back). One sitting: sketch the lite Mag client (context-pack read + ask door) against its SDK.
- S5 Mesh comms, medium: the radio section (Meshtastic Python CLI, MeshCore, Reticulum, T-Lora Pager ~$87) is the hardware leg of the mesh-comms skill. One sitting: map the skill's lanes onto Meshtastic CLI verbs and name the first off-grid seat.
- S6 Voice/babel-fish, low: xiaozhi-esp32 can be reflashed "so its voice loop and device-side mcp tools are backed by a server you point at hermes" (page's own bytes) - device-side MCP tools behind a voice loop. One sitting: read the xiaozhi MCP tool schema and file the door.
- S7 Fleet bench, low: "The first wave for the bench" (page's own closing heading) plus per-device worked-up use cases = a hardware fill-ball lane table. One sitting: lift the ~12 devices that match estate organs (CoreS3 flash-card body, UGV rover, Stack-chan desk body, OAK camera, RTL-SDR, Bus Pirate 6) into a WANT_REGISTER with prices.

## Watch / owed

- WATCH: hermes-agent-iot and the Hermes Gadget SDK repos (device-side protocol may converge with or undersell the estate's rib/verkle device mount; check licenses before any vendoring, GSTD NOASSERTION lesson).
- OWED: none - page, tweet and image all fetched first-hand this sitting. The catalog's 4-6 use cases per device are vendor claims and were not re-verified device-by-device; the census counts are from the page's own rendered bytes.
- Spend note: every hardware row is an L3 purchase decision (operator-gated). Nothing was ordered.
