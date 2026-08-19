"""nest_hygiene — temperature as parasite control on the Verkle nest.

The knot is the bird's nest (history, hatch, flight). Parasites are unverified
flesh that cannot survive a change of conditions. Freeze (T=0) overnight in
foil: no new knots, no LLM, hash-only. Cook (heat) is distill.boil: novelty
against the invariant corpus, never add. Learn from both piles.

Reuse: session_freeze, holographic_q, vram_memory.cook, distill.boil,
party_subchain, temperature_stack cold.
Schema: mag_nest_hygiene.v1
"""
from __future__ import annotations

from typing import Any

SCHEMA = "mag_nest_hygiene.v1"


def freeze_nest() -> dict[str, Any]:
    """Put the nest in the freezer. T=0. Conditions parasites cannot live in."""
    parasites: list[dict[str, str]] = []
    soil: list[dict[str, str]] = []

    freeze: dict[str, Any] = {}
    try:
        from mag.session_freeze import freeze_session_snapshot
        freeze = freeze_session_snapshot(include_system_health=False) or {}
    except Exception as e:
        freeze = {"error": str(e)[:120]}

    fh = str(freeze.get("content_hash") or freeze.get("hash") or "").strip()
    if len(fh) >= 12 and fh.lower() not in ("true", "false", "ok"):
        soil.append({"id": "session_freeze", "why": "content-addressed snapshot " + fh[:16]})
    else:
        parasites.append({"id": "session_freeze", "why": "freeze did not hash"})

    try:
        from mag.holographic_q import q_status
        qs = q_status()
        latest = qs.get("latest_q_knot") or {}
        if not (latest.get("verkle_root") or "").strip():
            parasites.append({
                "id": "q_empty_root",
                "why": "Q knots last " + str(latest.get("ts") or "?") + " verkle_root empty / simulated parent",
            })
        else:
            soil.append({"id": "q_proven", "why": str(latest.get("verkle_root"))[:16]})
    except Exception as e:
        parasites.append({"id": "q_status", "why": str(e)[:120]})

    try:
        from mag.vram_memory import cook
        c = cook()
        hl = c.get("hot_lattice") or c
        ollama = hl.get("ollama") or {}
        gpu = c.get("gpu") or hl.get("gpu") or {}
        stage = str(c.get("stage") or "")
        if c.get("ok") and (gpu.get("vram_used_pct") is not None or int(ollama.get("n_resident") or 0) > 0):
            soil.append({"id": "cook", "why": "stage=" + (stage or "vram") + " resident=" + str(ollama.get("n_resident"))})
        else:
            # Honest RAM stage is soil-as-truth, not a parasite-as-lie.
            soil.append({
                "id": "cook_ram",
                "why": "ok=false stage=" + (stage or "ram") + " — lattice not claimed as VRAM",
            })
    except Exception as e:
        parasites.append({"id": "cook", "why": str(e)[:120]})

    try:
        from mag import party_subchain
        st = party_subchain.status()
        if st.get("verified"):
            soil.append({"id": "subchain", "why": "n=" + str(st.get("n")) + " verified"})
        else:
            parasites.append({"id": "subchain", "why": "unverified"})
    except Exception as e:
        parasites.append({"id": "subchain", "why": str(e)[:120]})

    boil = {}
    try:
        from mag.distill import boil
        boil = boil({"freeze": fh, "parasites": [p["id"] for p in parasites], "soil": [s["id"] for s in soil]})
    except Exception as e:
        boil = {"error": str(e)[:120]}

    return {
        "ok": True,
        "schema": SCHEMA,
        "temperature": 0.0,
        "stack": "cold",
        "foil": "session_freeze + no append + no LLM",
        "parasites": parasites,
        "soil": soil,
        "boil": boil,
        "note": "freeze changes conditions; parasites die; soil remains; heat=distill.boil novelty vs corpus",
    }
