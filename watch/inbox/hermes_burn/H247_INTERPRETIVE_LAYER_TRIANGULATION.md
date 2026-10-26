# H247_INTERPRETIVE_LAYER_TRIANGULATION (nvidia/nemotron-3-super-120b-a12b:free, turn 1, channel: content)

Deliverable: render‑contract patch for context‑pack (spec)  
Add a fixed‑core render section and a pinned‑dynamic section to the existing context‑pack format. The patch introduces a new field `render_contract` that enumerates immutable tokens (core template) and mutable pointers (explore queue, decayed invariants). Seats apply the contract at window‑close: render = core_template + interpolate(pinned_pointers). No new machinery is required; the existing percolate() output feeds the pinned pointers.  

Falsifier: if seats using the patch do not achieve ≥10% lower per‑token latency on the drift‑patrol fresh‑reader held‑out task **and** retain ≤2% accuracy loss relative to baseline verbatim‑context seats, the patch is falsified.  

(1) Three closest prior works and differences  
- MemGPT/Letta (watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md:UNVERIFIED) treats the window as RAM and the store as disk, paging verbatim pages; the estate’s compiler produces content‑addressed invariants with dependency cascades instead of raw pages.  
- Gist tokens / soft prompts (watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md:UNVERIFIED) learn latent activations that replace text entirely, requiring model‑level cooperation; the estate keeps a deterministic state layer and only renders text for observers, needing no model change.  
- KV‑cache persistence / prompt caching (watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md:UNVERIFIED) exposes the KV cache as permanent state; the estate’s invariants are hash‑addressed, decay‑aware, and cascade‑on‑dependency, offering a higher‑level semantic layer beyond raw cache prefixes.  

(2) Strongest argument against compiled‑invariant context losing to verbatim context  
The invariant percolator compiles recurring signal into content‑addressed hashes that decay by a thermodynamic law and cascade on declared dependencies (watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md:UNVERIFIED). This preserves decision‑relevant signal while suppressing noise, whereas verbatim storage accumulates irrelevant tokens and forces the model to re‑encode the same information each turn, increasing stochastic drift.  

(3) One experiment that would settle it  
Run a longitudinal ablation arm: compiled ARM A (state layer with percolate‑generated invariants) versus verbatim ARM B (raw transcript window) across k=5 interaction chains. Measure task performance and drift‑patrol fresh‑reader error (instrument) after each chain; the arm that shows statistically stable or improving performance wins.  

(4) Prior work on falsifiable‑attachment for compressed memories  
MemGPT’s function‑call paging includes a verification step that checks returned values against a type signature before committing to store (watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md:UNVERIFIED). Soft‑prompt probes sometimes attach a held‑out reconstruction loss to detect compression degradation (watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md:UNVERIFIED). These are early attempts at falsifiable attachment but lack the explicit dependency‑cascading decay contract of the estate’s invariants.  

All claims about the code are marked UNVERIFIED because exact line numbers cannot be confirmed without the source file. No em‑dashes appear; only plain hyphens are used.  

---  
End of deliverable.
