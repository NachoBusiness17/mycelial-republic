# FLEET SURFACE INVENTORY + DRIVING CONTRACT (2026-10-23)

Operator order: "let's do an inventory and let's start driving them
correctly." All findings byte-backed tonight; the organ (mesh_router.py
map) now reads THREE OF FOUR CELLS UP and writes device_map.json.

## The fleet map (organ's own view, 2026-10-23)

| body | state | the bytes |
|---|---|---|
| bob | UP, gates PASS | 100.125.103.60 via ssh config (etfag + estate_to_bob), 495MB free RAM, 16.4GB stor, 105 invariants. scrcpy+adb INSTALLED tonight via winget. NO Android device is USB-ADB-connected: the "phone connected to bob" enumerates as BLUETOOTH audio only (moto g 5G + Pixel 11 Pro BT profiles, no ADB interface) |
| desktop | UP, gates PASS (after key-path fix) | 31GB free RAM, 229.7GB stor, 111 invariants, 0.44s - the 10-19 receipt's key-path drift (etfag Documents) was real; BODIES now points at ~/.ssh/adam_laptop_key |
| pixel-11-pro | UP, gates PASS | ssh u0_a354@100.79.122.101:8022 with the SEAT DEFAULT id_ed25519 (KEY-AUTH-OK probed live; the configured pixel_lane key never existed - BODIES fixed). Android 17, arm64, 15GB RAM / 5.9GB free, 915GB storage / 838GB FREE, battery 85% health GOOD cycle-count 14, up 16h40m, Termux with node+python+sshd+git, 141 pkg, ~/.gstdmesh provisioned (ribs, invariant_manifest.json) |
| t90 | DOWN, reachable-only | Termux sshd LISTENING on 100.72.38.3:8022 but auth dead: t90_lane_key did not exist on any clone. MINTED tonight at repo root; provisioning paste owed (below) |

## Not yet cells (honest inventory)

## AMENDMENT 1 (2026-10-23, operator correction): t90 IS THE TABLET

This receipt's "the tablet: NOT on the tailnet" line was WRONG - the
operator: "t90 is the tablet we've been over this." t90 (100.72.38.3,
Android 16, aarch64, provisioned tonight, 102 invariants, beacon live)
has been the tablet all along. The device map is:

- t90 = the TABLET (medium tier, Termux cell, continuous beacon)
- pixel-11-pro = the big phone (outstanding tier, 838GB storage cell)
- moto-g-5g-2024 = the phone cabled/BT-paired to bob (unprovisioned)
- the broken phone = not visible anywhere (retire or parts)

The original (wrong) text is preserved below the correct map per the
tombstone law. No BODIES change needed - t90 was already a body; the
error was only in this receipt's prose and the session's todos.

---

- **moto-g-5g-2024** (100.122.34.118): on the tailnet, nothing serving
  (8022/22/5555 closed), BT-paired to bob. Likely the phone just
  "connected to bob". Needs Termux + sshd + pubkey to become a body.
- **the tablet**: NOT on the tailnet - invisible to the fleet. Needs
  Tailscale + Termux + the provisioning paste, then it joins BODIES.
  >> STRUCK 2026-10-23: see Amendment 1 - the tablet is t90, already
  provisioned and UP when this line was written.
- **the broken phone**: invisible everywhere. If its board runs,
  headless-over-usb is its role; else it retires to parts.
- mag-openclaw (100.122.55.63): tailnet-linux, offline 45 days.

## Changes made tonight (all receipted here)

1. mesh_router.py BODIES: pixel key path -> ~/.ssh/id_ed25519 (dead
   pixel_lane removed); desktop key path -> ~/.ssh/adam_laptop_key
   (drift fix). Receipt-comments in source.
2. t90_lane_key + .pub minted at repo root (ed25519,
   zcode-seat-t90-lane-20261023). BODIES already expects this path.
3. bob: scrcpy installed (winget; bundles adb). Bob can adb/scrcpy the
   moment a phone has USB debugging on.

## THE OPERATOR'S 30 SECONDS (three pastes, then the fleet is five)

1. **t90** - in Termux, one line:
   mkdir -p ~/.ssh && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIebyxWDcfi/ajZ+qt4gcy90QBh9C+ut0KHjLF+dQVBu zcode-seat-t90-lane-20261023" >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
2. **phone cabled to bob** - Settings: enable Developer Options + USB
   debugging, then accept bob's RSA fingerprint prompt once. (Bob's
   adb is ready now.)
3. **tablet** - install Tailscale + Termux, join the tailnet, enable
   sshd (sshd in Termux), paste the same line with a fresh key (I
   mint tablet_lane_key on request), then tell me its tailnet name.

## DRIVING CONTRACT (the correct way, from tonight forward)

1. Drive bodies through mesh_router.py (map / route / fire / have /
   burn) - the organ gates battery (>30% or charging), RAM, load, and
   never routes sealed shapes (location/camera/sms). Ad hoc ssh is for
   provisioning and repair only.
2. Battery discipline: pixel is at cycle 14 - keep it plugged during
   heavy drives (torrent seeding, invariant syncs), screens off, sshd
   as the only always-on surface. A phone dies of screen-on automation,
   not of node work.
3. Storage roles: pixel's 838GB free makes it the torrent-memory node
   candidate (MCP epistemic mesh pattern, SIBIL guardrails) and the
   invariant replica; bob stays primary; desktop stays bench.
4. New bodies join by: tailscale + termux + pubkey paste + one BODIES
   entry. Never by adb-over-network-first (the tailnet is the wire).
5. Wall-clock honesty per the GPU long-read: lane timings from phones
   are thermal/battery-governor artifacts; cite battery pct + charging
   state with any phone perf claim.

## First workloads (assigned now, firing as keys land)

- pixel-11-pro: invariant HAVE sync vs desktop's 111 (it holds 1 - the
  seed is owed), then the torrent-memory pilot when the unmounted
  volume question resolves. Firing next organ pass.
- t90: resume the standing continuous beacon the moment the paste
  lands (its 10-19 commission stands).
- moto + tablet: onboarding per the paste list, then sensor roles
  (moto = the X-For-You candidate harvester; tablet = the
  glance-and-star GUI surface).

Consumer: the free-ask mesh, the cell-drive program, the reef publish.
Verifier: mesh_router.py map is the live truth; this receipt's table
regenerates from it on every pass.
