# PA-DG1-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

### (1) THE DOOR - Mated-Model-as-MoE Export

**Verdict:** An ensemble in disguise. It is not a genuine MoE export format because it defeats the core efficiency promise of sparsity.

**Explanation:** A genuine MoE model uses a router to sparsely activate only $k$ experts out of $N$ total experts ($k \ll N$). A "mated" model resulting from population fusion is a single, dense checkpoint. If this parent model is converted into $N$ experts ($E_1, \dots, E_N$), and the router simply learns to reconstruct the original dense function, the network is operating as a fully connected, dense ensemble using learned gating, not as a sparse MoE [evidence: moe-mating-connection:2].

**Conditions for Success (The Edge Case):**
The mechanism only wins (achieving true sparsity) under one specific condition:
*   **Expert Capacity:** The experts must be tiny (e.g., $<1$ billion parameters) and the input stream must be so sparse that the router is performing per-capability routing (e.g., routing based on domain knowledge or specific function calls, not merely token identity). In this case, the parent-model weights are used only for initialization guidance, not as the final expert weights.

**Kill First:** The concept *fails* because a single dense source (the parent) cannot inherently encode the conditional, sparse routing structure required for a true MoE computation without introducing massive complexity and weight redundancy, resulting in performance closer to a single massive expert than to a true sparse ensemble.
***
### (2) THE DESIGN - Minimal Export Format and Runtime

**Deliverable:** Export Format $\text{Parent} \to \text{Experts}$.

**Export Format: Multi-Component Weight Dump (MCWD)**
The format must enable the runtime to treat the converged, dense parent model as the initialization source for $N$ distinct, non-interacting expert blocks.

1.  **Header/Metadata Component ($\text{Meta}$):**
    *   `ModelRoot`: Pointer/shard ID of the original parent weights.
    *   `ExpertCount`: $N$.
    *   `ExpertAssignmentIndices`: An iterable defining block-wise mapping $E_i \leftarrow \text{Parent}(w_{i, \text{offset to } i})$.
    *   `RouterWeights`: The $\text{W}_g$ gate layer weights (must survive the merge process and be trained separately, or, if trained jointly, must be the top layer of the merge).

2.  **Expert Weights Component ($\text{Experts}$):**
    *   A single tensor block containing all $N$ expert weight matrices. The weights are copied and *frozen* per expert block, $W_{\text{expert}, i}$.
    *   $W_{\text{expert}, i}$ is initialized via layer-wise linear mapping or simple block-wise slicing of the parent tensor $\text{Parent}(W)$.

3.  **Shared Component ($\text{Shared}$):**
    *   Shared projection layers (e.g., Input/Output Embeddings, Normalization layers) must be explicitly identified and retained, as these represent the consistent interface across all $N$ experts.

**Runtime Environment:** DeepGEMM (or a sufficiently advanced custom kernel library targeting the same patterns).

**Justification:** DeepGEMM's implementation of Grouped GEMM [evidence: deepgemm-mechanics:12] is crucial because it assumes the experts are already laid out in a contiguous or indexable memory block. MCWD provides this sequential block structure, allowing the runtime's persistent threadblocks to pull expert weights and execute the grouped matrix multiplication efficiently.

***
### (3) THE FALSIFIER - CPU/6GB-AMD Benchmark

**Deliverable:** A direct, executable benchmark procedure using standard open-source tools.

**Goal:** Determine if the memory overhead and computational pathing of the MCWD format can achieve a throughput benchmark close to established sparse MoE models (like Mixtral).

**Setup:**
*   **Hardware:** AMD Ryzen/Radeon (RDNA1/2), 6GB VRAM.
*   **Tooling:** `llama.cpp` compiled with ROCm support (or a custom Vulkan/hipBLASLt binding built as a prototype).
*   **Model:** Use a 2B-7B model (e.g. Llama-2 7B Q4\_K\_M).

**Experiment Protocol (The Load):**
1.  **Preparation:** Take a baseline 7B Q4\_K\_M model (A) and a smaller 2B Q4\_K\_M model (B).
2.  **Fusion Simulation:** Use the MCWD format logic (parent $\to$ experts) to synthesize a 7B model replica ($M_{sim}$) that simulates merging A and B into a single sparse MoE structure (i.e., $M_{sim}$ is trained/initialized as $A$ with $B$'s weights injected into a subset of $A$'s experts). The resulting weight file size must be measured.
3.  **Benchmark:** Run standard character-per-second inference loop (e.g., 100 tokens generated) on $M_{sim}$ using the grouped GEMM path in llama.cpp's Vulkan backend.
4.  **Measurement Point:** Measure $\text{Tokens/second}$ and the runtime memory allocation/eviction pattern on the 6GB VRAM.

**Success Condition (Feeds it):** If the generated $M_{sim}$ achieves $>50\%$ of the tokens/second of the original monolithic 7B model (A) when the routing is actively used, the hypothesis of "Viable Ensemble" is supported. This suggests the MCWD format is computationally sound.

**Failure Condition (Kills it):** If the $M_{sim}$ throughput is significantly worse (e.g., $<20\%$ of A's baseline) *or* the required run-time peak memory usage consistently exceeds 6GB VRAM during initial grouped matrix assembly, the hypothesis is killed. This failure confirms that the inherent memory access patterns of the dense parent model are anti-climactic to the performance gains promised by true sparse MoE routing.
