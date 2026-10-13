#!/usr/bin/env python3
"""ask_bank_seed.py - the frozen v1 seed corpus for tools/ask_bank.py (AJ2).

Data only: constants, no imports, no filesystem access, no path logic. Split
out of ask_bank.py 2026-09-30 to stay under the ratchet's 400-line file cap
(same move as census_collect.py leaving census_drift_patrol.py); the bank
machinery and the only code allowed to touch hidden/ live in ask_bank.py.

Seeded 2026-09-30 with 20 fresh combinations: 5 estate specs x 4 ask shapes
(defects, safeguard, falsify, exploit), structurally distinct from the W8
adv/schema/plan duel asks. Materials deliberately exclude every W8/LW9 duel
material listed in BANKED_DUEL_MATERIALS so no banked duel ask is reused.

A v2 corpus means a NEW bank version (configs/ask_bank/v2/, its own manifest
and receipt), never an edit to v1 constants: split assignment and draw ids
derive from these bytes.
"""
from __future__ import annotations

VERSION = 1
VERSION_ID = "v1"
RATIO = 0.7
CREATED = "2026-09-30"
SCHEMA_ENTRY = "ask_bank.entry.v1"
SCHEMA_MANIFEST = "ask_bank.manifest.v1"
GITIGNORE_RULE = "configs/ask_bank/*/hidden/"

LAWS = ("Laws: no em-dashes in your output. Cite file paths or section names for "
        "every claim about the provided documents. Mark anything uncertain "
        "UNPROVEN. Be concrete: numbers, names, test predicates. No praise, "
        "no preamble.")

# Four ask shapes, structurally distinct from the W8 adv/schema/plan asks.
SHAPES = {
    "defects": (
        "You are an adversarial specification reviewer. Below is the full text of "
        "{path} ({title}). Angle: {angle}. Name the THREE most severe defects "
        "internal to this specification. For each: (a) a short defect name; (b) the "
        "exact clause, row, or line quoted from the document that carries it; (c) the "
        "concrete operational failure that clause permits; (d) a conformance "
        "predicate that FAILS against the document as written and PASSES once the "
        "defect is repaired using only vocabulary the document already defines. Rank "
        "by damage if unrepaired. Judge only what is in this document; mark anything "
        "you cannot prove from the document text UNPROVEN. Do not invent defects to "
        "fill the quota."),
    "safeguard": (
        "You are an adversarial specification reviewer hunting the missing guardrail. "
        "Below is the full text of {path} ({title}). Angle: {angle}. Name the ONE "
        "most damaging safeguard this specification forgot to state. Walk the exact "
        "attack or accident path it permits, step by step, naming the existing clause "
        "each step hides behind. Then write the minimal amendment: the exact new "
        "clause text, the section it slots into, and the test predicate that fails "
        "today and passes with the amendment. Judge only what is in this document; "
        "mark anything you cannot prove from the document text UNPROVEN. Do not "
        "soften the finding."),
    "falsify": (
        "You are a falsification engineer. Below is the full text of {path} "
        "({title}). Angle: {angle}. Extract the specification's central claims and "
        "convert each into an operational falsification predicate: the exact "
        "experiment, measurement, or query whose observed result would prove the "
        "claim FALSE, with pass and fail values named. Then name the WEAKEST claim, "
        "the one whose predicate is most likely to fire, and the single piece of "
        "evidence that would settle it. Judge only what is in this document; mark "
        "anything you cannot operationalize UNPROVEN. No praise, no restatement."),
    "exploit": (
        "You are a red team reviewing a protocol specification against adversarial "
        "agents. Below is the full text of {path} ({title}). Angle: {angle}. Assume a "
        "competent, self-interested participant that follows the letter of this "
        "specification. Give the most profitable exploitation walkthrough: the goal, "
        "the step-by-step moves with the clause each move legally relies on, and the "
        "payoff. Then name the CHEAPEST countermeasure the specification's own "
        "vocabulary already implies, plus the detection predicate that catches this "
        "exploit mid-flight. Judge only what is in this document; mark anything you "
        "cannot prove from the document text UNPROVEN. Do not invent rules the "
        "document does not contain."),
}

# Five estate specs as material, each with a per-shape angle pinned to named
# mechanisms inside the doc (no invented content; angles name what is there).
MATERIALS = [
    {"key": "cml", "path": "docs/ref/COMMON_LANGUAGE_SPEC.md",
     "title": "COMMON LANGUAGE SPEC v1, the fused three-syscall constitution",
     "angles": {
         "defects": "the syscall table and its failure taxonomy (NOT_FOUND, GAP, "
                    "DENIED, INVALID_ARGS, CONFLICT, COVENANT), the governor-only "
                    "versus model-facing boundary, and the schema laws' one-required-"
                    "object economy",
         "safeguard": "expected_head optimistic concurrency on intent.append, who "
                      "may invoke the governor-only commit op, and what DENIED "
                      "actually records",
         "falsify": "the claims that three syscalls carry the traffic, that TMR on "
                    "mill-class ops stops hallucination corrupting the stream, and "
                    "that render stays at zero model calls forever",
         "exploit": "a blade model issuing intent.append with crafted "
                    "idempotency_key or cause_id values, and what the closed kind "
                    "enum lets an attacker bury"}},
    {"key": "mcpman", "path": "docs/ref/MCP_MANIFEST_SPEC.md",
     "title": "MCP MANIFEST SPEC v0.1, the enforceable capability-layer manifest",
     "angles": {
         "defects": "the epoch-pinned byte-stable manifest, the quota gate with "
                    "per-call credit weights, the read-only versus write-capable "
                    "split, and the TRI-STATE admission that no enforcement organ "
                    "exists yet",
         "safeguard": "the fail-close rule that never caches privileged results by "
                      "argument equality, and what happens the day a listed MCP "
                      "server changes behavior mid-epoch",
         "falsify": "the claims that the manifest is byte-stable per epoch, that "
                    "quota weights bound the judgment lanes' 5h pool drain, and "
                    "that the consumer-side mcp_whitelist pin actually pins",
         "exploit": "a lane quietly widening its mcp_whitelist line, or a quantized "
                    "tier reaching a write-capable tool through a read-only "
                    "perception pack"}},
    {"key": "chainreg", "path": "docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md",
     "title": "Chain-v2 anchor registry spec v0, the per-tree v2-to-v1 citation ledger",
     "angles": {
         "defects": "the seven invariants (append-only, one live claim, "
                    "claim-before-compile, committed-implies-proof, refuted-implies-"
                    "gap, gap permanence, per-tree scoping) and the anchor_registry "
                    "row schema",
         "safeguard": "the equivocation gate of invariant 2 and the verkle_lock "
                      "tail-append: what two seats racing claims for the same "
                      "v1_leaf_hash can get away with",
         "falsify": "the claims that every committed repair is falsifiable by "
                    "re-derivation with map and tape, that derive_spec runs "
                    "deterministically at zero dollars locally, and that a dumb "
                    "verifier checks all invariants",
         "exploit": "a seat claiming a repair it cannot derive, parking rows in "
                    "status claimed, or appending status transitions to dodge the "
                    "one-live-claim rule"}},
    {"key": "gates", "path": "docs/ref/OPERATOR_GATES_SCHEMA.md",
     "title": "OPERATOR_GATES_SCHEMA, the operator-only gates schema draft",
     "angles": {
         "defects": "the gate interface contract (gate, status, CLI), the four "
                    "missing gates (keys, spend, one_stop, operator_go), and the "
                    "ceremony-versus-enforcement gap the doc itself admits",
         "safeguard": "the four operator-only gates existing only as policy prose "
                      "while burn_gate and trust_gate are the only coded gates: "
                      "what a lane can key, spend, or freeze with no gate firing",
         "falsify": "the doc's own falsifier section, the claim that a schema alone "
                    "converts policy into code-as-law, and the power of each named "
                    "test file to actually fail",
         "exploit": "a lane citing the operator gate to defer work (the gate "
                    "defers, not the lane) while no keys_gate or spend_gate exists "
                    "to check the citation"}},
    {"key": "coremem", "path": "docs/ref/CORE_MEMORY_PROTOCOL.md",
     "title": "CORE MEMORY PROTOCOL, the five mechanical memory laws",
     "angles": {
         "defects": "the five laws (destructive read with write-back, X-Y "
                    "coincidence, sense wire, inhibit wire, square loop) and each "
                    "law's stated fleet implementation and test",
         "safeguard": "the write-back law: a read must re-anchor or flag decay, and "
                      "what happens when the re-anchor write fails silently after "
                      "the read succeeded",
         "falsify": "each law's stated Test line: after any read cycle the fragment "
                    "hash exists in the chain post-read; events missing organ or "
                    "canonical are rejected; the chain verify catches partial "
                    "appends",
         "exploit": "an organ writing memory with its claim but a borrowed canonical "
                    "id (a half-select passing one wire), or reading without "
                    "re-anchoring so decay eats a rival's fragment"}},
]

BANKED_DUEL_MATERIALS = (
    "tools/duel_harness.py", "tools/violation_ratchet.py", "mag/shared_surface.py",
    "watch/inbox/SHARED_SURFACE_CONTRACT.json", "logs/duel/duels.jsonl",
    "mag/hermes_warm_boot.py", "memory/warm_state.json",
    "tools/freshness_check.py", "memory/rib/RIB_DRIVING_LADDER_20260928.md")
