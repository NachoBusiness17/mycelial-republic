# THE DESKTOP EXIT PLAN (operator order, 2026-10-11: "i just want to use linux or at least a gui in linux because i have no money and i hate giving microsoft a damn thing")

Context: Windows 10 22H2 at EOL (but actively patched per KB5126256, Sept 2026),
no money for Microsoft, moral objection to paying them. Bob has a spare Windows 11
key that could piggyback. Rejected by the operator's own preference: Linux, GUI.

## The recommendation (priced in three options)

### Option A: MINT Linux, full desktop (the recommendation)

Mint Cinnamon on the desktop as the PRIMARY OS:
- Free forever, zero Microsoft, Cinnamon GUI = the closest feel to Windows of any
  mainstream DE, and it is a garbage truck of a distro: boring, stable, huge
  community.
- EVERYTHING the fleet needs already runs on Linux natively, because we proved it
  this week: Ollama (the tailnet server ran FROM WSL/Linux all night), docker
  (the entire WoW build + database + gstd-node + mag stack), the consensus
  harness (stdlib python, Linux-first), nightcrew, pheromone, the seed MCP. The
  estate is already 90 percent Linux-shaped. Windows is the host shell, not the
  substrate.
- Migration checklist (one evening, before any wipe):
  1. GPU: Ryzen 7 3800XT is the CPU; GPU model unknown to this seat. Ollama runs
     Vulkan/ROCm/CUDA depending on card; check the card's Linux driver story
     (NVIDIA = proprietary driver install, AMD = mostly works out of box).
  2. The Windows-only programs actually used: list them honestly. The answer is
     usually a browser, and everything else is already cross-platform.
  3. TurtleWoW client: THIS is the real cost. The client is Windows. Mitigation:
     Lutris/Wine runs 1.18.1 clients well in most reports, and the SERVER is
     already a Linux container. The client is the only Windows dependency in the
     whole game stack. Test in Wine BEFORE wiping.
  4. Backup: full disk image before the move. The nothing-lost law applies to
     the host too.

### Option B: the W11 key piggyback (the fallback, and it is legitimate)

If a load-bearing program truly cannot run on Linux: install Windows 11 on BOB
using the spare key (bob is already a fleet member), keep the DESKTOP on Linux,
and the perimeter gains an OS-diverse node, which is actually better for the
coldest-vertex doctrine (a fleet that only runs one OS has untested assumptions).
The key gets used where it does the most good instead of paying Microsoft again.

### Option C: dual boot (the middle, still valid)

Linux primary + a Windows partition kept for the WoW client only. Works. The
operator's hate is for paying Microsoft, not dual-booting them: a W11 key on a
partition costs nothing extra. Least clean, least migration risk.

## The fleet implication (the real argument)

The estate already survives host death: binaries in volumes, state in containers,
memory in git + seed, the perimeter re-boots from seed onto any Linux box. The
desktop moving to Linux makes the PRIMARY OS the same OS as every container,
every build target, and the gstdbot's native habitat. Windows is currently the
least-supported surface in our own fleet. The operator's instinct and the
architecture agree.

## First move (one evening, reversible)

1. Full disk image to the 5TB cloud (the nothing-lost law).
2. Live-USB Mint session (no install): test GPU, audio, network, and the
   TurtleWoW client under Wine from the live session.
3. If the live test passes: install to the primary drive, restore the estate
   from seed, point the perimeter at the new host.
4. Windows 11 key goes to bob only if step 3 fails on a load-bearing program.

## Falsifier

If the live-USB test fails on GPU or the WoW client, Option A stays blocked.
Do not wipe on faith. The test costs one USB stick and one evening and answers
everything.
