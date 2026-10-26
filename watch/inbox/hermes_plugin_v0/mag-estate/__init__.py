"""mag-estate Hermes plugin v0: registration only."""
from __future__ import annotations

from pathlib import Path

from . import schemas, tools

_PAIRS = (
    (schemas.CHAIN_VERIFY, tools.mag_chain_verify),
    (schemas.RECEIPT_VALIDATE, tools.mag_receipt_validate),
    (schemas.NOTICES, tools.mag_notices),
    (schemas.LEASES, tools.mag_leases),
)


def register(ctx):
    try:
        root = ctx.get_config("mag_root", default="")
    except Exception:
        root = ""
    tools.configure(root)
    for schema, handler in _PAIRS:
        ctx.register_tool(name=schema["name"], toolset="mag_estate", schema=schema, handler=handler)
    skills_dir = Path(__file__).parent / "skills"
    if skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            md = child / "SKILL.md"
            if child.is_dir() and md.exists():
                ctx.register_skill(child.name, md)
