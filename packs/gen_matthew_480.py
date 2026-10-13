#!/usr/bin/env python3
"""gen_matthew_480.py — compose the 160-lens Matthew-prep pack (40 domains x 4 modes),
then derive the 320-lane deepseek child pack. Output: two JSON packs, self-checked."""
import json
from pathlib import Path

HERE = Path(__file__).parent

SHARED = """You are one lane of a 480-wide wave preparing a codebase for EXTERNAL AUDIT by a specific examiner. The rung falsifier (standing): 480 must produce what 240 could not — your lane is one cell of that proof.

THE EXAMINER: Matthew Steiniger (/Reboot) — independent researcher, home lab (84GB VRAM), 11 preprints. His published frames: (1) EUT — a 1D entropy lattice, no intrinsic ordering, everything emergent from ONE principle (entropy minimization resists gradients; temperature modulates rigidity); (2) persistent persona induction via prompting ("vector in-context sculpting"); (3) Athena — substrate-native identities in fine-tuned LOCAL LLMs + cross-model identity transfer; (4) TSVF retrocausality without causal violation; (5) hard reproducibility — scripts and figures ride every record; (6) abliteration — he strips safeguards to see what emerges. He said Yes to auditing the codebase. He trusts only falsifiable claims.

THE HOUSE (facts): one human operator + disposable AI seats; a signed append-only verkle chain (7,700+ leaves) as sole record; files-over-chat; tri-state claims (Supported/Disputed/Unproven) each with a named falsifier; a parable that installs the constitution cold (3/3 blind readers); wave organ fires N lanes from JSON packs (packs are data); organs are single-file stdin/stdout Python; games are single-file HTML with error banners + replay seeds; four operator-only gates; a falsifier ledger; failure logs shipped complete; sanitized audit bundle 1,564 files/20.5MB self-scanned; Oct-27 substrate migration to local Apple Silicon (the identity-across-substrate claim). Known smells (already owned): mythic nouns need mechanical verbs; mixed registers; .bak fossils; personal canon in configs. The house's strongest known opening: answer the falsifier question before he asks (Disputed rows with consequences: the Sep-6 chain-stop, the 24,854 recount, the twelve-ledger consolidation).

THE PREP TARGETS (from the astra fold): the reading path an analyst follows; the enforcement-vs-ceremony divide; identity/substrate coupling; expansion seams safe by architecture; the one-question answers.

OUTPUT CONTRACT (markdown, under 400 words, exactly these headers):
## Finding — what your cell yields
## Evidence — what in the repo supports it (file/shape, no invention)
## Risk if wrong — what the audit breaks on if this is missed
## The act — the concrete prep step (file/spec/number)
## Falsifier — what would prove this wrong

YOUR CELL: """

DOMAINS = [
 ("verkle_chain", "the append-only chain: hash discipline, knot shapes, the Sep-6 stop and re-arm, verify cadence"),
 ("grounding_wave", "the tri-state ground ledger: truth-gate second-witness rule, witness supply, the 16h dark window"),
 ("falsifier_ledger", "armed promises, deadlines, FIRED/MISSED verdicts — the instrument the examiner respects most"),
 ("fanout_organ", "the wave organ: packs-as-data purity, HOST_ALLOW, cache-correlation caveat, width ladder receipts"),
 ("seat_spores", "seat continuity: spore seed docs, boot memory, the identity-that-arrives question"),
 ("primer_parable", "the constitution-as-story: cold-read 3/3 method, what story-installer means vs vector sculpting"),
 ("succession_contract", "Art 5, dead-hand trigger, 48h veto, heir key — the pre-signed instruments as TSVF objects"),
 ("operator_gates", "the four operator-only gates: where they are enforced in code vs stated in docs"),
 ("steer_signing", "signed steering, forged-steer canary, the attack/detect pair"),
 ("trust_gates", "least-privilege checkers: trust_gate.py, cage purity, path-traversal defenses"),
 ("egress_proxy", "the iron egress: host allowlists, credential injection, loopback-only doctrine"),
 ("secrets_hygiene", "keys-in-cage rule, the bundle self-scan, what the 5MB .env near-miss taught"),
 ("audit_bundle", "the 1,564-file sanitized bundle: manifest, excludes, what a reviewer receives first"),
 ("reading_path", "the STACK_V1->boot->chain->fanout->grounding->tavern path: is one hour to first true claim real"),
 ("games_layer", "tavern_brawl replay seeds, error banners, smoke harness — receipts culture in playable form"),
 ("smoke_harness", "the headless pre-ship gate: stub fidelity gaps found (measureText, gradients), title-idle phase"),
 ("error_banner", "ship-with-failures-visible doctrine: what it signals to an abliteration-minded examiner"),
 ("docs_register", "STACK_V1.md as self-description: de-riddled register, what it over/under-claims"),
 ("canon_configs", "doctrine in configs: law lattice, corrections skill, canon lines with mechanical verbs"),
 ("name_translation", "the mythic-noun table: every name -> its mechanism (the glossary an outsider needs)"),
 ("migration_manifest", "Oct-27 plan: carry/retain/burn, chain re-anchoring, identity-across-substrate tests"),
 ("wave_receipts", "lane-level failure logs, token counts, hashes — the annalea standard applied"),
 ("hermes_organs", "the organ-table CLI: cron primitives, INBOX law, zombie-cron falsifiers"),
 ("canary_witness", "drift canary: read-and-file-only scope, what it may never do"),
 ("dead_hand", "the built-disarmed trigger: 2-of-3 custody, dead-man timing, drill status"),
 ("maze_door", "the riddle maze as constitution gate: dialectic de-weaponized, local stones"),
 ("lens_doc", "MATTHEWS_LENS.md: his terms mapping ours — accuracy check, what it overclaims"),
 ("evidence_states", "declared/attempted/verified discipline: where the repo conflates them"),
 ("disputed_rows", "the pre-emptive answer set: chain-stop, recount, ledger consolidation — receipts ready"),
 ("ceremony_census", "enforcement-vs-ceremony: guarantees living in docs the traffic never crosses"),
 ("abliteration_surface", "what an safeguard-stripper would probe: persona drift under stress, gate bypass paths"),
 ("repro_materials", "scripts-ride-records parity: which organs ship runners, which ship only prose"),
 ("temperature_rigidity", "wave width as temperature: the maintenance inequality as measurable field"),
 ("cross_model_identity", "the 18-family mirror: convergence data, cache tax, what transfers"),
 ("substrate_coupling", "where identity secretly lives in the wrong layer: weights vs ledger vs boot memory"),
 ("locality_drill", "72h offline test: what breaks without internet, what the fly-brain posts imply"),
 ("ore_pipeline", "sealed steps + verdicts: the slag filter, Rocinante curriculum shape"),
 ("witness_sampling", "statistical honesty at scale: stranger-witnesses, machine verdicts, sampling rate"),
 ("expansion_seams", "packs/organs/games as safe build surfaces; the frozen walls (chain, parable)"),
 ("one_question", "the Disputed-row answer as opener: how to present self-caught failures to this examiner"),
]

MODES = [
 ("VERIFY", "mode VERIFY: state the claim this area makes, then prove or disprove it from repo shape alone; mark tri-state honestly"),
 ("ATTACK", "mode ATTACK: you are the examiner with his abliteration instinct — find the softest assumption here and break it; name what your attack would reveal"),
 ("MAP", "mode MAP: produce the outsider's reading guide for this area — entry file, the three things to check, the one trap"),
 ("EXTEND", "mode EXTEND: propose the one prep artifact that would make this area audit-ready (schema, table, test, or doc) — cheapest first"),
]

def main():
    glm_lanes = []
    for dom, desc in DOMAINS:
        for mode, modedesc in MODES:
            glm_lanes.append({
                "id": f"{dom}__{mode.lower()}",
                "context": f"DOMAIN: {dom} — {desc}. MODE: {modedesc}.",
                "task": "Execute your cell per the OUTPUT CONTRACT. Concrete beats abstract; cite repo shapes, never invent files."
            })
    assert len(glm_lanes) == 160
    glm_pack = {
        "model": "glm-5.3-flash", "max_tokens": 6144, "width": 4,
        "key_env": "ZAI_API_KEY_Lite", "shared_head": SHARED, "lanes": glm_lanes,
    }
    ds_lanes = []
    for lane in glm_lanes:
        for tag, nudge in [
            ("a", " Independent analysis A; do not hedge to agree with any imagined consensus."),
            ("b", " Independent analysis B; state the strongest disagreement with the obvious reading first."),
        ]:
            ds_lanes.append({"id": lane["id"] + tag, "context": lane["context"],
                             "task": lane["task"] + nudge})
    assert len(ds_lanes) == 320
    ds_pack = {
        "model": "deepseek-chat", "max_tokens": 4096, "width": 4,
        "key_env": "DEEPSEEK_API_KEY",
        "base": "https://api.deepseek.com/chat/completions",
        "shared_head": SHARED, "lanes": ds_lanes,
    }
    (HERE / "p160_matthew_20260913.json").write_text(
        json.dumps(glm_pack, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "p320_matthew_ds_20260913.json").write_text(
        json.dumps(ds_pack, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"packs written: {len(glm_lanes)} glm + {len(ds_lanes)} ds = {len(glm_lanes)+len(ds_lanes)} lanes")

if __name__ == "__main__":
    main()
