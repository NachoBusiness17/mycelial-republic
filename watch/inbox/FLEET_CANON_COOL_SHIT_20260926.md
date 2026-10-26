# Fleet canon: cool-shit people finder, top 10 (B2-183, 2026-09-26)

People and teams doing the coolest things with free compute and agent fleets
right now. Every link curl-verified this lane (curl -I / -IL, status quoted).
Attribution notes: person-project pairings marked canonical are stable public
knowledge; denominators and steals are this estate's analysis, not quotes.

1. codeaashu — https://github.com/codeaashu/free-claude-code (200). Built: a
   proxy that routes Claude Code's Anthropic-shaped calls to free backends
   (NVIDIA NIM at 40 req/min free, OpenRouter free models, DeepSeek direct).
   Denominator: free request-rate tiers bridged into a paid-tool harness.
   Steal: point the estate's night batch lanes at NIM's 40/min instead of
   burning scarce specialist quota.

2. exo labs (Alex Cheema, canonical) — https://github.com/exo-explore/exo
   (200). Built: cluster ordinary devices (Macs, phones) into one inference
   runtime over peer-to-peer RPC. Denominator: idle household silicon.
   Steal: the estate's janitor tier could span the operator's idle laptops
   the same way instead of one-box Ollama.

3. Peter Steinberger (@steipete) — https://github.com/steipete (200),
   https://github.com/steipete/openclaw (200). Built: OpenClaw, the
   local-first personal agent gateway wired to chat surfaces (the estate
   already runs it in docker at /board). Denominator: local-first agent +
   commodity chat apps as UI. Steal: give the swarm a Telegram-wired OpenClaw
   face so the operator drives lanes from a phone.

4. Simon Willison — https://simonwillison.net (200). Built: the llm CLI plus
   a decade of git-scraped, dated write-ups cataloging which models are free
   or nearly free this week. Denominator: free API tiers, documented as they
   appear. Steal: adopt his log-every-tier-with-a-date habit: our LINKS/
   EVENTS rows should name the tier and its rate cap the day we first ride it.

5. Georgi Gerganov (canonical) — https://github.com/ggml-org/llama.cpp
   (200). Built: CPU/edge inference that made the janitor tier possible at
   all. Denominator: zero-GPU inference, free forever. Steal: llama-server
   parallel slots let one box serve several janitor seats at once; our
   gemma:2b scut lane is leaving that on the table.

6. Daniel and Michael Han (canonical) — https://github.com/unslothai/unsloth
   (200), https://docs.unsloth.ai (200). Built: free Colab-tuned QLoRA
   notebooks that fine-tune real models on Google's free T4s. Denominator:
   free Colab GPU sessions. Steal: the B2-326 100-step QLoRA smoke can run
   on their notebook shape when the local 12-24GB GPU is mid-job, same
   receipt bands (0.5-1.0 good, below 0.2 overfit tripwire).

7. Paul Gauthier (canonical) — https://github.com/Aider-AI/aider (200).
   Built: aider, the pair-programmer that proved a modest model plus a smart
   repo map beats a big model blind. Denominator: BYO-key and local models.
   Steal: aider's repo-map ranking is the same problem as our catalog FTS
   relevance (B2-102/B2-466); steal the ranked-tree heuristic for query
   planning.

8. All-Hands-AI — https://github.com/All-Hands-AI/OpenHands (200). Built:
   OpenHands (the open Devin), a full agent developer runnable against any
   backend including free ones. Denominator: OSS harness, model-agnostic.
   Steal: their event-stream architecture (every agent action a replayable
   event) is the same shape as our index_events law; steal their replay UI
   pattern for the orchestrator trails.

9. Max Headbox (builder name not published in my bytes; project verified) —
   https://hackaday.com/2025/09/28/fully-local-ai-agent-runs-on-raspberry-pi-with-a-little-patience
   (301 to live article). Built: a fully local agent on a Raspberry Pi that
   loops tool calls autonomously, no cloud. Denominator: patience over
   tokens. Steal: the estate's "flash-off or local" law has a working
   exemplar; the loop-until-done pattern with tiny local models is proven
   on 1GB-class RAM.

10. The free-model proxy crowd (unnamed in my bytes; pattern verified by
    search) — Cloudflare Worker proxies exposing Claude-Code-shaped APIs over
    free endpoints (MiniMax M2.5, Nemotron 3 class models). Denominator:
    Cloudflare's free worker tier plus free model endpoints. Steal: a 30-line
    Worker is enough to serve our own harness shape from any free endpoint;
    if we ever outgrow direct z.ai/gemini/groq lanes, this is the seam.

Search provenance: this lane's WebSearch hits (partial, the account's 1302
rate cap ate several queries) surfaced rows 1, 9, 10; rows 2-8 are canonical
estate-adjacent projects, links curl-verified above. Geoffrey Huntley's
ralph-loop was considered and dropped this lane: personal site unreachable
from this box (curl 000), no verified link, no-fabrication law.

Canon registration owed: corpus/canon/MANIFEST.sha256 seals the canon dir, so
this page lands on the shared inbox (watch/inbox/) instead of corpus/canon/
until the operator registers it (baseline-update-style, by name).
