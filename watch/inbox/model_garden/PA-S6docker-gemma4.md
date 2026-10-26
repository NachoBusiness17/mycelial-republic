# PA-S6docker-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

### Attacker Analysis

(1) **LAN Access Vector (3 Moves)**
The surface is largely restricted by loopback binding (`127.0.0.1`) (Evidence: `2.0.0.0: 127.0.0.1:8765:8765` in `docker-compose.yml` lines 26, 54, 135). An attacker on the LAN must compromise a running service *that binds to 0.0.0.0* or finds an unexposed management port. The most critical, although still constrained, entry point is the `openclaw` service (Evidence: `docker-compose.yml` lines 101-116), as it shares a network namespace and runs a Gateway. Attack progression:
1.  **Recon:** Port scanning for exposed internal services (e.g., redis/6379, mcp/8766).
2.  **Compromise:** Exploit a potential vulnerability in a mounted binary or web service (e.g., via a vulnerable model or library within the `mag` container).
3.  **Lateral Movement:** Leverage the common `mag_net` bridge network to pivot, especially if the attacker gains root inside a container, allowing access to other service pods (e.g., `mcp` or `redis`) which are also on `mag_net` (Evidence: `docker-compose.yml` lines 21, 59, 129).

(2) **Secrets, Volume Mounts, and Overmounting**
**Secrets:** The reliance on `.env` files (Evidence: `docker-compose.yml` lines 17, 101) is a security risk. Any file readable by the container runtime can leak secrets. API keys like `COHERE_API_KEY` are managed via variables (Evidence: `docker-compose.yml` line 107), which is superior but still requires careful CI/CD management.
**Volume Mounts:** The system uses extensive bind mounting (Evidence: `docker-compose.yml` lines 33-48), granting the container full read-write access to host directories (`./logs`, `./state`, `./queue`). This breaks isolation if the container is compromised.
**Overmounting:** The primary issue is the broad grant of capabilities (RW access) by the bind mounts, rather than a single directory mount. The `watch` directory is mounted to both `mag` and `openclaw` (Evidence: `docker-compose.yml` lines 43, 112) –
