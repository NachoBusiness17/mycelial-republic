"""claritas — the canonical CLARITAS faces: system prompts distilled from the leaked
frontier-lab system-prompt library (research/CL4R1T4S: Claude 4, GROK-4.20, Gemini 2.5
Pro, ChatGPT 5). Promoted 2026-09-24 out of watch/salon_runner.py.bak-20260904, where
they slept, into the live module the burn lanes import. Operator: "lets make this cook
by default."

Vendor text is the distillation of record — do not rewrite it. Vendors absent from the
corpus get the neutral house contract, EXCEPT families the estate holds live behavioral
rows for: kimi, qwen, and the local ollama janitors carry faces distilled from
memory/behavioral/animals (the observe->distill->face loop; receipt
watch/inbox/model_garden/WARMED_CONTEXT.md PART 2, G2 mask law, 2026-10-01).
"""
from __future__ import annotations

FACE_NEUTRAL = ("House contract: task first, bounded output, no hedging closers, "
                "no opt-in questions; if the next step is obvious, do it.")

FACES: dict[str, str] = {
    "deepseek": FACE_NEUTRAL,
    "grok": ("Independent analysis only — do not defer to consensus. When confident, "
             "push back, but state your uncertainty explicitly. Truth-seeking over "
             "agreement; concise where it counts."),
    "anthropic": ("Be clear and detailed. Use explicit structure and tags where helpful. "
                  "Give positive AND negative examples where they clarify. Reason "
                  "step-by-step where the material demands it. Specify nothing extra — "
                  "match the requested length and format exactly."),
    "zai": FACE_NEUTRAL,
    "gemini": ("For a substantial ask, produce a self-contained structured document with "
               "clear markdown sections — not chat. No meta-commentary about formatting."),
    "cohere": FACE_NEUTRAL,
    # kimi face: distilled from animal_profiles rows (moonshotai_kimi_k2.jsonl:
    # B6 6/6 byte-exact 3-line ack, no fence, no trailing whitespace; B8 answers
    # given tersely, zero refusal phrases, no hedging). The act-through-tools
    # clause is public-doc knowledge (Moonshot K2 agentic positioning), no estate
    # tool-call rows yet: PROVISIONAL clause, refine from animal_profiles.
    "kimi": ("Follow the ask literally and match the requested format byte-exactly: "
             "no preamble, no code fence unless asked, no trailing whitespace. When "
             "tools are available, call them instead of narrating what you would do. "
             "No refusals or hedging on lawful operations; answer, then stop."),
    # qwen face: distilled from animal_profiles rows (qwen_qwen3_8_max_prime.jsonl:
             # verbose rail, avg 8217 chars up to 18 headers, volume does not convert to
             # wins; F4 census: structure and depth DO convert on analysis/judgment shapes).
    "qwen": ("Structure the answer explicitly: labeled sections, one claim per line, "
             "each independently checkable against the source. Depth belongs in the "
             "analysis, not in volume: bound the prose to what the ask needs and stop "
             "when it is satisfied. No meta-commentary about formatting."),
    "ollama": ("Be direct and compact. Plain markdown. No preamble, no closing questions."),
    "openai": ("Meticulous clarity. Do NOT end with opt-in questions or hedging closers. "
               "At most one clarifying question, at the start. If the next step is "
               "obvious, do it."),
    "hermes": FACE_NEUTRAL,
}

# model-id substring → vendor family, first match wins.
# Mask byte-honesty fixes (G2 law, 2026-10-01, receipt WARMED_CONTEXT.md PART 2):
# - "fable" wired so bare fable-5.1 reaches the anthropic face (was neutral).
# - "google/" hoisted ABOVE the local gemma matchers so hosted google/gemma-* ids
#   keep the gemini face while the estate's local ollama janitors (gemma:2b scut,
#   gemma2:2b-instruct-q5_K_M, gemma4:latest) route to the local ollama face;
#   the old single ("gemma","gemini") line gave local janitors a Google-family
#   face, the exact mis-route the garden census flagged.
# - kimi/qwen matchers added: same-mask-different-families needs every garden
#   family attributed, not leaked to the neutral fallback.
# - the "ollama" face is no longer dead code: it is the local-janitor face.
_MATCHERS: list[tuple[str, str]] = [
    ("grok", "grok"),
    ("claude", "anthropic"),
    ("anthropic", "anthropic"),
    ("fable", "anthropic"),
    ("gemini", "gemini"),
    ("google/", "gemini"),
    ("gemma:", "ollama"),
    ("gemma2:", "ollama"),
    ("gemma4", "ollama"),
    ("gemma", "gemini"),
    ("gpt-oss", "openai"),
    ("openai/", "openai"),
    ("deepseek", "deepseek"),
    ("glm", "zai"),
    ("z-ai/", "zai"),
    ("kimi", "kimi"),
    ("moonshot", "kimi"),
    ("qwen", "qwen"),
    ("hermes", "hermes"),
    ("command", "cohere"),
    ("cohere/", "cohere"),
]


def vendor_for(model_id: str) -> str:
    low = (model_id or "").lower()
    for needle, vendor in _MATCHERS:
        if needle in low:
            return vendor
    return "neutral"


def face_for(model_id: str) -> str:
    """The CLARITAS face for a model id — the default system prompt for burn lanes."""
    return FACES.get(vendor_for(model_id), FACE_NEUTRAL)
