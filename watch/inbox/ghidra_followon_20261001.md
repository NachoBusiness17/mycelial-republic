# GHIDRA FOLLOW-ON LANDED (operator "okaygogo", 2026-10-01)

The three named follow-ons from watch/inbox/x_intel_drop_20261001.md, executed
same window. Every exit code below ran this session; no em-dash in this file.

## 1. binary_attest - the standing tool + 7 binaries PROVEN-OFFICIAL

tools/binary_attest.py (+ tests/test_binary_attest.py, 6 passed exit 0):
register-and-verify over release archives. Method: download the canonical
archive (or --archive a local one), sha256 it, extract the named member,
byte-compare. Register: configs/binary_register.json (sealed).

Security shape (Mimosa rulings, both enforced then satisfied):
- SSRF fence: https-only + host-suffix allowlist (github.com and its release
  CDNs, godotengine.org, adoptium.net), redirects re-validated per hop. The
  fence fired LIVE on first run: refused GitHub's signed redirect to
  release-assets.githubusercontent.com (my allowlist guessed
  release-artifacts...); corrected to the canonical host and noted in code.
- Path/member traversal refusal ('..' segments, absolute shapes) on local
  paths and archive members.

Rows banked (register verify: PASS, 7/7):
- tools/godot/Godot_v4.3-stable_win64.exe + _console.exe - archive sha256
  8f2c75b734bd956027ae3ca92c41f78b5d5a255dacc0f20e4e3c523c545ad410
  (godotengine/godot 4.3-stable)
- Ollama v0.34.3 (archive ollama-windows-amd64.zip, 1,460,962,639 bytes):
  ollama.exe, lib/ollama/llama-server.exe, libllama-server-impl.dll,
  ggml-base.dll, vulkan/ggml-vulkan.dll - the ENTIRE local-inference stack
  (the Vulkan path the 03:57 log proved live is now proven-official bytes).

Standing use: `python tools/binary_attest.py verify` - drift in any attested
binary (a swapped llama-server, an oiled Godot) fails loud. Ollama UPDATE
NOTE: every Ollama auto-update rewrites these files - re-run the five adds
after any update or verify will (correctly) cry DRIFT.

## 2. Ghidra 12.1.4 - vendored, JDK-solved, decompile rung PROVEN

- corpus/tools/ghidra_12.1.4_PUBLIC + Temurin 21 (gitignored via
  corpus/tools/ rule added to .gitignore). ~570MB + 190MB downloads this
  session.
- Bring-up gotchas, both root-caused and banked: (a) Ghidra 12 requires a
  FULL JDK - LaunchSupport hard-fails on a JRE with "JDK is missing javac
  executable" (string-proven from LaunchSupport.jar; my first download was a
  JRE); (b) Ghidra 12 dropped Jython - .py postScripts fail with "Ghidra was
  not started with PyGhidra"; the smoke is Java (GhidraScript compiles
  natively). JAVA_HOME_OVERRIDE pinned in support/launch.properties.
- SMOKE EXECUTED (analyzeHeadless, temp project, -deleteProject): the
  PROVEN-OFFICIAL Godot console exe -> 189 functions recovered, entry
  tls_callback_0 decompiled to readable C (589 chars, first 500 printed in
  the run transcript). Analysis + postScript + save all green.
- Estate shape: the deep rung behind the shallow one - binary_attest proves
  WHICH bytes; Ghidra answers WHAT the bytes do (firmware/binary questions,
  the DFHack-skill general form). Script pattern banked at
  corpus/tools/GhidraSmokeJava.java.

## 3. Model-mating paper dig - LANDED (sensing lane)

Pinned with high confidence: "Competition and Attraction Improve Model
Fusion" - Abrantes, Lange, Tang - arXiv:2508.16204 (GECCO 2025; code
github.com/SakanaAI/natural_niches). The tweet's ATTRACTION/CROSSOVER/
COMPETITION triad maps one-to-one onto the paper's three features. Receipt:
watch/inbox/model_mating_paper_dig_20261001.md (URL-cited, runner-up
candidates rejected with evidence). Load-bearing for the estate:
(1) attraction is computable from data we already mint (duels.jsonl per-ask
rows ARE the win/loss matrix); (2) budget is fitness-eval dominated (7B run:
~1000 evals, 24h on 4xH100 - our box's honest path is their MNIST
replication then 2.5B-class pairs, streamed SLERP into GGUF for sequential
Ollama eval); (3) implicit fitness sharing (payout capped by example
capacity, decayed by saturation) is a published anti-percolator fix for the
mates gambiter-seed exploit named in configs/mates.yaml.

## Register + commit

LINKS: no new row (this rides fix-everything-20261001). Config seal: updated
for binary_register.json. Census delta: +6 collected
(tests/test_binary_attest.py).
