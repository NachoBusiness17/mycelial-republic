# GSTD CODEBASE AUDIT - Lane A, the bones X-rayed - 2026-10-09

Clone: reference/gstdcoin/gstdbot @ e0bbe48 (READ-ONLY). web clone @ 4184e7e is a
Next.js marketing site only - no platform backend is public, so platform-side
behavior is marked unobservable throughout. Counts via .venv python byte-walk:
81 TS files, 28,944 lines in src/; 151 gateway routes, 36 guarded.

## 1. Module map (src/, size = lines incl. co-located tests)

| module | size | purpose (one line) | deps | bone verdict + evidence |
|---|---|---|---|---|
| gateway | 5,688 | Node HTTP surface: 151 routes (server.ts:483-4568), PIN auth, rate limit, task push, dashboard | router, peers, wallet, platform-link | WORKABLE. server.ts is a 4,854-line monolith; auth is per-route manual (36 requireNodeAuth sites of 151 routes, grep count), so coverage is inconsistent by construction |
| gateway/router.ts | 543 | 5-tier inference routing (cache, platform queue, local Ollama, P2P peer, fallback) + SmartMix paid councils | platform HTTP, Ollama, peers | WORKABLE-BRITTLE. Cache key defect (below); tiers honest and ordered; platform URL env-overridable (router.ts:184) |
| channels | 4,673 | Telegram bots (telegram 1,696, gstdai 1,092, guardian 617) + Mini App backend (miniapp 1,268) | router, platform | WORKABLE. miniapp validates Telegram WebAppData HMAC (miniapp.ts:662-666); the node webhook route does not (below) |
| swarm | 2,194 | Task processing agent: poll, compute, quorum gate, signed completion, retry queues (agent.ts:941-1043) | platform, p2p, wallet, memory | SOLID core. Best-engineered file in the repo: NaN-safe reward accounting (agent.ts:876-886), pending-report and pending-settlement queues (agent.ts:789-871), quorum gate that forfeits reward rather than lying (agent.ts:957-967) |
| p2p | 1,907 | libp2p mesh (node.ts:797) + HTTP gossip peer manager (peers.ts:450) + ed25519 attestation/quorum (attestation.ts, quorum-coordinator.ts) | libp2p, @ton/crypto | SOLID design, honest limits. 2-way cross-signing quorum with local re-verify (quorum-coordinator.ts:76-99); peer table admits metadata spoofing is ungated beyond a liveness ping (peers.ts:27-35, UNVERIFIED_LATENCY_MS peers.ts:37) |
| naas | 1,861 | Multi-chain RPC proxy, per-key GSTD billing via platform /rpc/charge (rpc_proxy.ts:52-58, 167-196) | local chain nodes, platform | WORKABLE. Off by default (index.ts:377-383); auth is the platform charge call |
| core | 1,311 | platform-link (heartbeat/register/commands, 330 ln), event-bus WS, model failover, scheduler, diagnostics | platform | WORKABLE. Signed platform commands verified vs baked pubkey (platform-auth.ts:44-52); heartbeat itself has no node signature (below) |
| wallet | 971 | TON wallet: address public, seed encrypted at rest (wallet.ts:42-69), external-wallet link | @ton | WORKABLE. Real ed25519 keypair now (wallet.ts:94-103, old unspendable-address bug documented in place); at-rest key is machine-derived (below) |
| node-lite | 199 | Minimal node: register, heartbeat, tunnel, proxy | platform, Ollama | BRITTLE. Proxies the WHOLE Ollama API through an unauthenticated quick tunnel (below) |
| other (~5,900) | - | apps, network, storage, training, validators, cli, dashboard, lib, security, odysseus | misc | Not deep-audited; apps routes PIN-guarded (server.ts:2131+); nothing republic-load-bearing found beyond the URL table below |

## 2. Security surface

Listeners: gateway HTTP 0.0.0.0 (server.ts:4725) + optional HTTPS (server.ts:4811);
WS /ws/events on same server (server.ts:4729-4733); fastify sidecar with
trustProxy:true (fastify.ts:23, 99-102); libp2p TCP 4001 + WS (p2p/node.ts:285-300);
node-lite proxy (node-lite/index.ts:175); naas rpc_proxy (naas/rpc_proxy.ts:216).

Auth boundaries (full list): global rate limit 120/min per socket IP, in-memory
(server.ts:452-480); dashboard PIN with 5-try lockout (server.ts:1239-1283,
242-265) + 24h bearer tokens (server.ts:154-170) + requireNodeAuth on destructive
routes (server.ts:177-184, no local bypass by design, comment server.ts:171-176);
peer ed25519 headers with 60s replay window (server.ts:203-240); platform
commands ed25519 vs baked PLATFORM_PUBKEY_HEX (platform-auth.ts:10, 44-71;
enforced platform-link.ts:222-242, server.ts:186-201); free API keys balance-gated
sha256 in memory (server.ts:311-312, 1119-1153); Mini App Telegram HMAC
(miniapp.ts:662-666); wallet-link shared secret (lib/wallet-link-headers.ts).
Node-to-platform: NONE - X-Wallet-Address + X-Node-Id headers only
(platform-link.ts:107-112, 162-168; agent.ts apiCall 1356-1361).

Task lifecycle trust: anyone can submit (the router itself uses the public
/api/v1/tasks/submit, router.ts:257-262); the node claims by self-declared node_id
(platform-link.ts:263); verification is the platform's M5 hash compare
(server.ts:4597-4613) - unobservable platform-side; nothing at node level stops forgery (known defect 3).

## 3. Findings

ALREADY-KNOWN (tonight's 4, re-confirmed at bytes):
1. L1 cache prefix collision - router.ts:147-150 keys on first 200 lowercased
   chars of last user message.
2. Param drop - handler destructures model/messages/stream only (server.ts:878);
   queue path sends neither temperature nor max_tokens (platform-link.ts:278-283).
3. Unauthenticated /api/v1/tasks/push - server.ts:4568-4630, zero auth,
   self-declared node_id (server.ts:4603, 4609).
4. Shared-IP rate bucket - req.ip with no trust-proxy (server.ts:457).

NEW-CONFIRMED (mine):
5. Push-endpoint callback hijack: platform_url comes from the REQUEST BODY and
   becomes the completion target (server.ts:4569, 4581, 4604-4617). Anyone who
   can reach the node points its results + node_id at any URL. PR-sized fix:
   ignore platform_url, use env only.
6. Cache key omits the model: makeKey reads only the message (router.ts:147-150),
   so a hit serves a response generated by a DIFFERENT model than requested even
   for unique prompts; cache.set is shared by all three compute tiers
   (router.ts:190, 201, 214).
7. Unauthenticated /api/telegram/webhook: no Telegram secret_token check; the only
   gate is knowing the linked chatId (server.ts:1427-1435). /restart does
   process.exit(0) (server.ts:1464-1466) and /update runs git reset --hard +
   git pull + npm install (server.ts:1469-1476) - remote DoS and forced self-update
   by chatId knowledge.
8. Wallet/earnings disclosure on any exposed node: /api/node/wallet returns address,
   balances, owner binding unauthenticated (server.ts:1707-1747); same for
   /api/node/earnings (server.ts:1691-1704); ~115 of 151 routes carry no auth
   (grep count server.ts).
9. node-lite is an open AI proxy: every non-/health request is forwarded to local
   Ollama verbatim (node-lite/index.ts:124-144, 173), published through an
   unauthenticated Cloudflare quick tunnel (node-lite/index.ts:100-121) with CORS
   * (node-lite/index.ts:136) - the tunnel-URL holder can run, pull, delete models.
10. At-rest key hygiene: wallet seed encrypted under a machine-derived key
    (/etc/machine-id, predictable homedir fallback, no passphrase - wallet.ts:42-52)
    and the P2P attestor seed is PLAINTEXT seedHex (identity.ts:47-53): any
    same-user process gets both.
11. Auth-by-address platform class: register/heartbeat/complete carry no signature
    (platform-link.ts:107-130, 287-297); /api/wallet/claim authenticates to the
    platform with X-Wallet-Address only (server.ts:2523-2534) - node identity is a
    knowable string, not a key possession.
12. Two completion lanes diverge on attestation: the swarm lane signs result_hash +
    node_sig and can reach 2-of-3 quorum (agent.ts:701-787, 989-1010), but the
    production-default lanes submit unsigned: push sends result_hash with no
    signature (server.ts:4604-4617) and poll sends no hash at all
    (platform-link.ts:287-297). Our dogfood traffic rode the unsigned lane.
13. Paid SmartMix sells renamed local models: expert modelIds like
    openai/gpt-oss-120b silently map to local Ollama models (router.ts:62-74,
    325-332), so a 0.50 GSTD "Swarm of 7" can be 7 calls to the same local llama
    with different system prompts (router.ts:377-399).

DESIGN-QUESTIONS (no verdict claimed): rate limiter is in-memory per process,
restart-clearable, multi-instance blind (server.ts:453); requireNodeAuth accepts
tokens from req.query/req.body (server.ts:178), leaking into logs/proxies; peer
scoring trusts self-reported capabilities + one liveness ping (peers.ts:249-296,
honestly flagged peers.ts:27-35); result_hash binds output only - the prompt is
never hashed into the signed message (attestation.ts:46-51), so an attestation
proves "someone signed this blob", not "this blob answers that ask".

## 4. Missing-for-republic list

(a) Verifiable/attested task results. Gap: the signed path exists but is not the
default; nothing binds outputs to inputs. Evidence: agent.ts:989-1009 vs
platform-link.ts:287-297 and server.ts:4604-4617; attestation.ts:46-51. Smallest
close: PR - push/poll lanes include node_sig exactly as agent.ts:991-995 does.
Full fix (bind prompt hash + params into the signed message) is spec-sized
(touches SettlementMaster.tact verifyQuorum per attestation.ts:5-17).
(b) Reputation semantics. Gap: node-side there is no reputation code at all -
only display of a platform-provided reputation_score (gstdai.ts:761, 879,
913-920); what 51->59 measures is unobservable (platform Workers code not public;
web clone is marketing). Heartbeats feed tasks/uptime/latency
(platform-link.ts:169-182); ARCHITECTURE.md:189 concedes "No quality signal".
Close: spec-sized - publish the formula; PR-sized node-side - log deltas per
completion to reverse-engineer it (our dogfood moved +8 on 9 tasks).
(c) Peer verification vs platform-trust-all. Gap: two trust regimes coexist; the
platform lane trusts strings (finding 11), the P2P lane does real cross-signing
(quorum-coordinator.ts:1-29). Close: PR - require node_pubkey at registration
(the field already exists, platform-link.ts:120) and verify completions; the
requirePeerAuth pattern (server.ts:203-240) is the template.
(d) Sovereignty tiers. Gap: CENTRAL_DEPENDENCIES.md:8-13 admits 5 CRITICAL
platform calls; offline the node degrades to a local chatbot with no earning and
no settlement (402 DEPLOYMENT_DISABLED handling platform-link.ts:131-137,
189-196). Partial queue-then-settle exists for reports and quorum proofs
(agent.ts:789-871) but not for task acquisition. Close: spec-sized - offline flag
plus a local settlement ledger that replays on reconnect (our frozen-tape replay
is the shape).
(e) Fork-equality mechanics. Gap: 88 gstdtoken.com references in src (grep
count); most are env-overridable (index.ts:264, server.ts:54) but at least 7
hard-code the URL with no override: server.ts:1684, 2670,
dashboard/server.ts:238-293, cli/index.ts:418, 781, router.ts:530. The deeper
asymmetry: PLATFORM_PUBKEY_HEX is baked into every release (platform-auth.ts:5-10),
so the platform operator alone signs remote commands and updates - a fork must
ship its own pubkey or inherit the crown. Close: PR (env the 7 URLs), spec
(pubkey rotation/pinning policy per fork).

## 5. Verdict - cookability

Cookable, with an asterisk. The rare bones are real: a cryptographically serious
attestation/quorum lane, ed25519-signed platform commands with replay windows, an
honestly-documented security posture (disabled forgeable wallet-auth
server.ts:2550-2563; self-critical comments peers.ts:27-35, agent.ts:698-700).
But production traffic rides the UNSIGNED lane and settlement trust is entirely
the platform's. Must land first, ranked:
1. Unify completions on the signed path (finding 12; PR-sized, machinery exists).
2. Auth the push endpoint with the existing peer-signature pattern (findings 3/5;
   server.ts:4568 + server.ts:203-240).
3. Cache key = full-prompt hash + model (findings 1/6; PR-sized).
4. node-lite proxy: tunnel off by default + path allowlist (finding 9).
5. Rate limiter proxy-header trust (finding 4; fastify.ts:23 already shows it).
6. Publish reputation semantics (b) - without it every payout is faith.

Inputs: AUDIT_PLAN.md, DOGFOOD_DATA.md, GSTD_FORENSICS_20260918.md (its contract-side verdicts re-anchored at node-side bytes: the authority spine it named is findings 11 + 12 + the baked pubkey).
