# B2-153 external steal dig for SEED-RIB 2026-09-26

## Verdict

Dug. Nine idea classes surveyed for prior art against the seed pack's core moves (kilobyte-reconstructible estate, self-describing agent structures). Seven are STEAL in part, two are internal pointers this lane cannot verify externally; nothing found does the whole job. The composite nobody ships: a sealed, hash-pinned, kilobyte-scale pack where LAWS SHIP AS CONFIG and RECEIPTS SHIP AS BYTES and a cold agent rehydrates into an operator-equivalent seat with its habit-bindings intact. Per-idea verdicts below.

## Evidence (idea class, verdict, citation)

1. Reproducible-build manifests (.buildinfo / reproducible-builds.org): STEAL (input-hash discipline, bit-for-bit rebuild goal). Limit: rebuilds software from pinned inputs, carries no state, no memory, no laws. https://reproducible-builds.org/docs/definition/
2. Nix derivations + closures (.drv build descriptions, nix-copy-closure): STEAL, the strongest one: a small text derivation describes the whole buildable world and the closure IS the kilobyte-manifests-a-usable-whole idea. Limit: reconstructs packages, never workstate, narrative, or operator habit; no sealed narrative layer. https://nixos.org/manual/nix/stable/ (derivations, closures)
3. Git bundles (git bundle create --all; single-file repo): STEAL for whole-history-in-one-file plus prerequisite-commit verification (git bundle verify). Limit: carries EVERYTHING, no salience bound (no verkle-tip notion), no schema, no laws-as-config. https://git-scm.com/docs/git-bundle
4. in-toto attestations / SLSA provenance / Cosign-signed SBOMs: STEAL for receipts-as-signed-bytes (our register/INDEX seal law already matches the shape). Limit: attests a build process, does not rehydrate a working agent seat. https://slsa.dev, in-toto ITE-6/7 attestations
5. Model cards (Mitchell et al. 2019, arXiv:1810.03993) and datasheets (Gebru et al.): STEAL for the self-describing-artifact arm (intended use, limits, evaluation fields). Limit: documentation ABOUT a model, inert; vacuous for reconstruction. https://arxiv.org/abs/1810.03993
6. A2A Agent Card (.well-known/agent-card.json, skills/capabilities/securitySchemes): STEAL for the discovery arm of self-describing agents; the documented caveat that a card is a discovery primitive NOT a trust primitive is exactly our seal-vs-claim distinction, already enforced harder here (hash seals + register law). https://a2a-protocol.org (Agent Card spec)
7. MCP registries / server manifests: STEAL for the tool-manifest arm (name a tool, its inputs, where it runs). Limit: no estate state, no history, no receipts. https://modelcontextprotocol.io
8. Stego seeds (Fauvel): UNVERIFIED-INTERNAL pointer; no external citation reachable this lane, so no steal verdict is filed (would be fabrication). Treated as estate-internal until a citable artifact lands.
9. Called-shot compression (Mr Pool): UNVERIFIED-INTERNAL pointer; same treatment. The 27/314 exact-size-match census (B2-88) is the closest in-house byte evidence for compression-by-reference, not his method itself.

## Work done

What we invent that nobody found shipping (the delta SEED-RIB owns): (a) the verkle-knotted rope: habit and residual state committed into a hash-bound tip so the NEXT session cannot boot without loading them (Clippy block is the working instance); (b) residual + registry + leaf = filed workdays as the reconstructible DNA of an agent's output, not of a build; (c) one 102KB sealed pack (57 files, seal 56/56, cold boot 12 PASS / 2 readable / 0 crashes measured 2026-09-26) that carries laws as config and receipts as bytes so a cold seat rehydrates to operator-equivalence; (d) deliberate-ask RIB discipline: system+bootloader+manifest+verkle tip as a payable context unit. Closest external composite is Nix closure + git bundle + in-toto; none carries the law/memory/habit layer, and none binds the next session to its own history.

## Falsifier

Dies if: (a) someone demonstrates a shipped artifact that reconstructs an agent seat (state + laws + receipts + habit bindings) from a kilobyte-scale sealed pack with byte-verified cold boot, naming the delta above as already-published; (b) the two UNVERIFIED-INTERNAL pointers produce citable external artifacts that predate and duplicate the delta (verdicts flip from vacuous-pointer to steal); (c) any citation above rots (dead URL or misquoted claim) without this card being amended.

## Bibliography closed

Live searches 2026-09-26: Nix derivations/closures, git bundle, A2A agent card, model cards Mitchell 2019, in-toto/SLSA/Cosign SBOM (search provider rate-limited twice mid-dig, 429/1302 family; the five surviving result sets are cited in-line). Estate pointers read: the B2-153 brief row; B2-88 exact-size census named from its receipt. Fauvel and Mr Pool items deliberately NOT cited externally (no reachable source). Nothing synthesized; unverifiable claims marked UNVERIFIED-INTERNAL instead of verdicts.
