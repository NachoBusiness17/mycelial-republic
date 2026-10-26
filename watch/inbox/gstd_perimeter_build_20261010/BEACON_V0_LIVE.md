# BEACON V0 LIVE - torrents for AI artifacts, garage-wizard swarm v0 - 2026-10-12 (closed)

**The operator's ask:** "an anon beacon i can switch on to get you guys to help me with testing of an anon network for garage wizards - torrents but for everything: MCP Servers, Memory, Training data, Weights, Skills. I want people to use gstd but not have it be a dead launch."

**What went live:** `tools/gstd_beacon.py` - the beacon writer + tailnet server. Beacon at `reference/gstdcoin/contracts/beacon.json`, served on `http://100.96.161.76:8777/beacon.json` (tailnet-only interface). **Live-read proof: fetched locally AND from bob over SSH, both HTTP 200** (the beacon log carries both GET lines).

**The seeded artifacts (5, all consensus-verified or receipted):** consensus-harness (the certification instrument itself), gstd-drain (the earn loop), gstd-mcp (the read-only wire server), the worker-reputation organ (PR #1), and the three-bonus-leg-bugs receipt (free - the co-contributor gift). Plus the live lattice snapshot fused in: cells, heat, TON, reputation, updated per read.

**The design (the answer to "torrents but for everything"):**
- **The anon model:** a wallet keypair is the identity - pseudonymous, no names, no KYC. Reputation is the trust. Anon does not mean trustless-free; it means trust is EARNED per wallet and portable across the swarm.
- **The verification gate (the dead-salmon paper's role - the operator linked it deliberately):** every announced artifact carries its dead-salmon-beating evidence (the consensus run that proved the skill works). Unverified claims are rumor-class and invisible to honest buyers. In a torrent network for AI artifacts, the dead salmon is the fake seed - the control is the anti-fake instrument.
- **The anti-dead-launch (why GSTD is useful on day one):** every artifact exchange settles through the rail - consensus-certified, 85/10/5, reputation accruing. A token is dead when nothing verifiable settles through it; this network's every trade does, by construction.
- **The swarm's worker menu (the flash-tier guide's role):** the deepseek/GLM/qwen/gemini pricing-speed table is the light-maze routing menu for hiring dark-lane workers - deepseek v4.1 flash off-peak + cache hits at $0.003 for volume, gemini flash for latency, GLM base for batch. The guide's own decision rules are the light maze's rules.

**The architecture law:** organs write files, the beacon serves files, settlement never moves over the beacon wire (the gated bridge settles; the beacon only announces). Same shape as the MCP server. The beacon is discovery + verification pointers; the rail is money; the division is the security posture.

**Ladder to v1:** signed announcements (wallet-signed rows so beacon content is attributable), DHT or tracker federation beyond the tailnet (public internet phase), LoRA weights as actual seeds (torrent the adapters, reputation-weighted merge per Phase 7), skills as the first paid tier (the SKILL.md corpus, consensus-verified per skill), and the guild's first public swarm announcement when GB's PR lands.

## Falsifier

The beacon claim dies if an unverified artifact appears in beacon.json (law violation), or if the served JSON diverges from the file (serving bug), or if no tailnet cell can fetch it (network claim false - falsified by bob's own 200, so currently held).
