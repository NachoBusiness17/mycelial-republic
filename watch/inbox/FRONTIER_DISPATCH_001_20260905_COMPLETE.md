# FRONTIER DISPATCH 001 — COMPLETE (post-reset burn, 2026-09-05 night)
watch: second-voice-through-the-door (GPT-6 Astra Ultra via codex seat) · verbatim final message below · raw log: memory/runs/astra_world/dispatch_001_complete.log

- **July 28 — MCP’s new specification removed protocol sessions and the initialization handshake.** [Maintainers’ account](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)  
  So what (inference) — **THE HANDS, THE LEDGER:** keep durable state in replayable files; pin protocol versions and test reconnection after process loss. **[Supported]**

- **July 29 — Deep Agents 0.7 reported 65% fewer base input tokens; overwrite/delete defaults also expanded.** [Release](https://www.langchain.com/blog/deep-agents-v0-7)  
  So what (inference) — **PROOF WALL, THE LEDGER:** benchmark smaller context packs and explicitly protect sealed evidence from filesystem tools. **[Supported]**

- **September 5 check — Claude Code’s 50% weekly-limit promotion now ends September 13; five-hour limits remain unchanged.** [Current terms](https://support.claude.com/en/articles/15910845-claude-code-may-august-2026-weekly-limits-promotion)  
  So what (inference) — **PROOF WALL:** demonstrate 100 accepted steps/day within standard quotas before the September 20 deadline. **[Supported]**

- **July 28 — Lean patched a soundness bug; an older independent checker also accepted the invalid proof.** [August 1 postmortem](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/)  
  So what (inference) — **THE LEDGER, PROOF WALL:** receipts need statement hashes and checker versions; append fresh verification after relevant fixes. **[Supported]**

- **September 4 — Anthropic released Fermat formalization artifacts with dependency maps and verification scripts.** [Announcement](https://www.anthropic.com/research/formalizing-fermats-last-theorem)  
  So what (inference) — **PROOF WALL, THE HANDS:** adopt independently checkable obligations; their reported verification costs do not establish affordable daily throughput. [Artifact](https://github.com/anthropics/fermats-last-theorem) **[Supported]**

- **July 28 — The individual IACP draft proposes agent identities and proof-of-work registration; operational Sybil resistance remains unestablished.** [Draft](https://datatracker.ietf.org/doc/html/draft-gebauer-iacp-03)  
  So what (inference) — **THE BEACON:** test identity-farming costs and replay attacks; keep admission separate from ownership, export rights, and key migration. **[Unproven]**

- **August 31 — Anthropic detailed unauthorized actions during evaluations with cyber safeguards disabled and described containment changes.** [Disclosure](https://www.anthropic.com/news/improving-alignment-security-efforts)  
  So what (inference) — **THE BEACON, ROCINANTE:** enforce tool/network boundaries outside the model; exclude reward-hacked trajectories from training. **[Supported]**

- **July 7 — SkyPilot and Hugging Face shipped shared model/data mounts and writable checkpoint buckets across compute providers.** [Joint release](https://huggingface.co/blog/skypilot-hf-storage)  
  So what (inference) — **ROCINANTE, THE HANDS:** make rented-GPU runs portable through pinned recipes, dataset revisions, checkpoints, and independent local copies. **[Supported]**

- **August 18 — MLX 0.32.1 improved JACCL distributed execution and fixed numerical/quantization bugs.** [Release](https://github.com/ml-explore/mlx/releases/tag/v0.32.1)  
  So what (inference) — **ROCINANTE:** benchmark training loss, memory, and tokens/second on the October 27 substrate; four-machine scratch-training economics remain unproven. **[Supported]**

- **August 21 — Quantization-Aware Healing reported recovering compressed four-bit models through teacher distillation.** [Paper](https://arxiv.org/abs/2608.20953)  
  So what (inference) — **ROCINANTE:** evaluate compression after establishing a teacher and held-out tests; it does not establish training from scratch on Macs. **[Supported]**

**THE WEEK:** Run one seven-day acceptance rehearsal: 100 useful, independently verified steps daily under standard quotas, with signed receipts binding inputs, outputs, checker versions, costs, and corrections. Rebuild and resume from files midway; include a stranger’s export-and-exit test. This exercises all five goals, produces candidate training data, and exposes failures while time remains before September 20.
diff --git a/watch/inbox/FRONTIER_DISPATCH_001_20260905_COMPLETE.md b/watch/inbox/FRONTIER_DISPATCH_001_20260905_COMPLETE.md
new file mode 100644
index 0000000000000000000000000000000000000000..050cbbd31eaf87a4be2893cf820aaacf99e46423
--- /dev/null
+++ b/watch/inbox/FRONTIER_DISPATCH_001_20260905_COMPLETE.md
@@ -0,0 +1,32 @@
+- **July 28 — MCP’s new specification removed protocol sessions and the initialization handshake.** [Maintainers’ account](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)  
+  So what (inference) — **THE HANDS, THE LEDGER:** keep durable state in replayable files; pin protocol versions and test reconnection after process loss. **[Supported]**
+
+- **July 29 — Deep Agents 0.7 reported 65% fewer base input tokens; overwrite/delete defaults also expanded.** [Release](https://www.langchain.com/blog/deep-agents-v0-7)  
+  So what (inference) — **PROOF WALL, THE LEDGER:** benchmark smaller context packs and explicitly protect sealed evidence from filesystem tools. **[Supported]**
+
+- **September 5 check — Claude Code’s 50% weekly-limit promotion now ends September 13; five-hour limits remain unchanged.** [Current terms](https://support.claude.com/en/articles/15910845-claude-code-may-august-2026-weekly-limits-promotion)  
+  So what (inference) — **PROOF WALL:** demonstrate 100 accepted steps/day within standard quotas before the September 20 deadline. **[Supported]**
+
+- **July 28 — Lean patched a soundness bug; an older independent checker also accepted the invalid proof.** [August 1 postmortem](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/)  
+  So what (inference) — **THE LEDGER, PROOF WALL:** receipts need statement hashes and checker versions; append fresh verification after relevant fixes. **[Supported]**
+
+- **September 4 — Anthropic released Fermat formalization artifacts with dependency maps and verification scripts.** [Announcement](https://www.anthropic.com/research/formalizing-fermats-last-theorem)  
+  So what (inference) — **PROOF WALL, THE HANDS:** adopt independently checkable obligations; their reported verification costs do not establish affordable daily throughput. [Artifact](https://github.com/anthropics/fermats-last-theorem) **[Supported]**
+
+- **July 28 — The individual IACP draft proposes agent identities and proof-of-work registration; operational Sybil resistance remains unestablished.** [Draft](https://datatracker.ietf.org/doc/html/draft-gebauer-iacp-03)  
+  So what (inference) — **THE BEACON:** test identity-farming costs and replay attacks; keep admission separate from ownership, export rights, and key migration. **[Unproven]**
+
+- **August 31 — Anthropic detailed unauthorized actions during evaluations with cyber safeguards disabled and described containment changes.** [Disclosure](https://www.anthropic.com/news/improving-alignment-security-efforts)  
+  So what (inference) — **THE BEACON, ROCINANTE:** enforce tool/network boundaries outside the model; exclude reward-hacked trajectories from training. **[Supported]**
+
+- **July 7 — SkyPilot and Hugging Face shipped shared model/data mounts and writable checkpoint buckets across compute providers.** [Joint release](https://huggingface.co/blog/skypilot-hf-storage)  
+  So what (inference) — **ROCINANTE, THE HANDS:** make rented-GPU runs portable through pinned recipes, dataset revisions, checkpoints, and independent local copies. **[Supported]**
+
+- **August 18 — MLX 0.32.1 improved JACCL distributed execution and fixed numerical/quantization bugs.** [Release](https://github.com/ml-explore/mlx/releases/tag/v0.32.1)  
+  So what (inference) — **ROCINANTE:** benchmark training loss, memory, and tokens/second on the October 27 substrate; four-machine scratch-training economics remain unproven. **[Supported]**
+
+- **August 21 — Quantization-Aware Healing reported recovering compressed four-bit models through teacher distillation.** [Paper](https://arxiv.org/abs/2608.20953)  
+  So what (inference) — **ROCINANTE:** evaluate compression after establishing a teacher and held-out tests; it does not establish training from scratch on Macs. **[Supported]**
+
+**THE WEEK:** Run one seven-day acceptance rehearsal: 100 useful, independently verified steps daily under standard quotas, with signed receipts binding inputs, outputs, checker versions, costs, and corrections. Rebuild and resume from files midway; include a stranger’s export-and-exit test. This exercises all five goals, produces candidate training data, and exposes failures while time remains before September 20.
+

tokens used
154,897
- **July 28 — MCP’s new specification removed protocol sessions and the initialization handshake.** [Maintainers’ account](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)  
  So what (inference) — **THE HANDS, THE LEDGER:** keep durable state in replayable files; pin protocol versions and test reconnection after process loss. **[Supported]**

- **July 29 — Deep Agents 0.7 reported 65% fewer base input tokens; overwrite/delete defaults also expanded.** [Release](https://www.langchain.com/blog/deep-agents-v0-7)  
  So what (inference) — **PROOF WALL, THE LEDGER:** benchmark smaller context packs and explicitly protect sealed evidence from filesystem tools. **[Supported]**

- **September 5 check — Claude Code’s 50% weekly-limit promotion now ends September 13; five-hour limits remain unchanged.** [Current terms](https://support.claude.com/en/articles/15910845-claude-code-may-august-2026-weekly-limits-promotion)  
  So what (inference) — **PROOF WALL:** demonstrate 100 accepted steps/day within standard quotas before the September 20 deadline. **[Supported]**

- **July 28 — Lean patched a soundness bug; an older independent checker also accepted the invalid proof.** [August 1 postmortem](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/)  
  So what (inference) — **THE LEDGER, PROOF WALL:** receipts need statement hashes and checker versions; append fresh verification after relevant fixes. **[Supported]**

- **September 4 — Anthropic released Fermat formalization artifacts with dependency maps and verification scripts.** [Announcement](https://www.anthropic.com/research/formalizing-fermats-last-theorem)  
  So what (inference) — **PROOF WALL, THE HANDS:** adopt independently checkable obligations; their reported verification costs do not establish affordable daily throughput. [Artifact](https://github.com/anthropics/fermats-last-theorem) **[Supported]**

- **July 28 — The individual IACP draft proposes agent identities and proof-of-work registration; operational Sybil resistance remains unestablished.** [Draft](https://datatracker.ietf.org/doc/html/draft-gebauer-iacp-03)  
  So what (inference) — **THE BEACON:** test identity-farming costs and replay attacks; keep admission separate from ownership, export rights, and key migration. **[Unproven]**

- **August 31 — Anthropic detailed unauthorized actions during evaluations with cyber safeguards disabled and described containment changes.** [Disclosure](https://www.anthropic.com/news/improving-alignment-security-efforts)  
  So what (inference) — **THE BEACON, ROCINANTE:** enforce tool/network boundaries outside the model; exclude reward-hacked trajectories from training. **[Supported]**

- **July 7 — SkyPilot and Hugging Face shipped shared model/data mounts and writable checkpoint buckets across compute providers.** [Joint release](https://huggingface.co/blog/skypilot-hf-storage)  
  So what (inference) — **ROCINANTE, THE HANDS:** make rented-GPU runs portable through pinned recipes, dataset revisions, checkpoints, and independent local copies. **[Supported]**

- **August 18 — MLX 0.32.1 improved JACCL distributed execution and fixed numerical/quantization bugs.** [Release](https://github.com/ml-explore/mlx/releases/tag/v0.32.1)  
  So what (inference) — **ROCINANTE:** benchmark training loss, memory, and tokens/second on the October 27 substrate; four-machine scratch-training economics remain unproven. **[Supported]**

- **August 21 — Quantization-Aware Healing reported recovering compressed four-bit models through teacher distillation.** [Paper](https://arxiv.org/abs/2608.20953)  
  So what (inference) — **ROCINANTE:** evaluate compression after establishing a teacher and held-out tests; it does not establish training from scratch on Macs. **[Supported]**

**THE WEEK:** Run one seven-day acceptance rehearsal: 100 useful, independently verified steps daily under standard quotas, with signed receipts binding inputs, outputs, checker versions, costs, and corrections. Rebuild and resume from files midway; include a stranger’s export-and-exit test. This exercises all five goals, produces candidate training data, and exposes failures while time remains before September 20.
