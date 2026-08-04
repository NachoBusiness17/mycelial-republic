"""Hypergraph-style vector map with Mag nodes, bonds, and external influences."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text) or {}
    # Minimal fallback is insufficient for nested YAML — require pyyaml in practice
    raise ImportError("PyYAML required: pip install pyyaml")


@dataclass
class Node:
    id: str  # e.g. A1.RopeVisibility
    anchor: str
    name: str
    mag: float
    zenith: float
    tags: list[str] = field(default_factory=list)
    measured: float | None = None  # last selftest-driven Mag

    @property
    def effective(self) -> float:
        return self.measured if self.measured is not None else self.mag


@dataclass
class Bond:
    source: str
    target: str
    stiffness: float
    protected: bool = False


@dataclass
class Influence:
    id: str
    kind: str
    couples: list[str]
    strength: float
    description: str = ""


@dataclass
class DimensionScore:
    id: str
    score: float
    weight: float
    hits: list[str] = field(default_factory=list)
    penalties: list[str] = field(default_factory=list)


class VectorMap:
    """Dual/triple-anchor lattice with surrounding influence field."""

    def __init__(
        self,
        metadata: dict[str, Any],
        nodes: dict[str, Node],
        bonds: list[Bond],
        influences: list[Influence],
        dimension_node_map: dict[str, list[str]] | None = None,
        beta: float = 3.0,
    ) -> None:
        self.metadata = metadata
        self.nodes = nodes
        self.bonds = bonds
        self.influences = influences
        self.dimension_node_map = dimension_node_map or {}
        self.beta = beta
        self.history: list[dict[str, Any]] = []

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VectorMap:
        nodes: dict[str, Node] = {}
        for aid, anchor in (data.get("anchors") or {}).items():
            for nname, nd in (anchor.get("nodes") or {}).items():
                nid = f"{aid}.{nname}"
                nodes[nid] = Node(
                    id=nid,
                    anchor=aid,
                    name=nname,
                    mag=float(nd.get("mag", 0.0)),
                    zenith=float(nd.get("zenith", 4.0)),
                    tags=list(nd.get("tags") or []),
                )
        bonds = [
            Bond(
                source=b["source"] if "." in str(b.get("source", "")) else b["source"],
                target=b["target"],
                stiffness=float(b.get("stiffness", 0.5)),
                protected=bool(b.get("protected", False)),
            )
            for b in (data.get("primordial_bonds") or [])
        ]
        # Normalize bond endpoints: allow A1 / A2 meaning anchor-level average
        influences = [
            Influence(
                id=i["id"],
                kind=i.get("kind", "external"),
                couples=list(i.get("couples") or []),
                strength=float(i.get("strength", 0.5)),
                description=i.get("description", ""),
            )
            for i in (data.get("influences") or [])
        ]
        return cls(
            metadata=dict(data.get("metadata") or {}),
            nodes=nodes,
            bonds=bonds,
            influences=influences,
            dimension_node_map=dict(data.get("dimension_node_map") or {}),
            beta=float((data.get("defaults") or {}).get("beta", 3.0)),
        )

    def anchor_mag(self, anchor_id: str) -> float:
        vals = [n.effective for n in self.nodes.values() if n.anchor == anchor_id and n.name != "Entropy"]
        return sum(vals) / len(vals) if vals else 0.0

    def _endpoint_value(self, ref: str) -> float:
        if ref in self.nodes:
            return self.nodes[ref].effective
        # Anchor-level
        if ref.startswith("A") and "." not in ref:
            return self.anchor_mag(ref)
        return 0.0

    def bond_stiffness(self, s_i: float, s_j: float, t_i: float = 1.0, t_j: float = 1.0) -> float:
        """EUT-style w_ij with β attractor."""
        t_i = max(t_i, 1e-9)
        t_j = max(t_j, 1e-9)
        # Map Mag in [0,4] loosely to entropy-like scalar via inverse: high Mag → lower disorder
        e_i = max(0.0, 4.0 - s_i) / 4.0
        e_j = max(0.0, 4.0 - s_j) / 4.0
        base = 1.0 + ((e_i - e_j) ** 2) / (t_i * t_j)
        return float(base ** (-self.beta))

    def dirichlet_energy(self) -> float:
        """E = ½ Σ w_ij (Mag_i − Mag_j)² over primordial bonds (anchor-level)."""
        energy = 0.0
        for b in self.bonds:
            mi = self._endpoint_value(b.source)
            mj = self._endpoint_value(b.target)
            # blend declared stiffness with physics w
            w = 0.5 * b.stiffness + 0.5 * self.bond_stiffness(mi, mj)
            energy += 0.5 * w * (mi - mj) ** 2
        return energy

    def influence_field(self) -> list[dict[str, Any]]:
        """Surrounding influences projected onto coupled nodes."""
        out: list[dict[str, Any]] = []
        for inf in self.influences:
            coupled_mags = []
            for c in inf.couples:
                if c in self.nodes:
                    coupled_mags.append({"node": c, "mag": self.nodes[c].effective})
            pull = inf.strength * (1.0 - (sum(x["mag"] for x in coupled_mags) / max(len(coupled_mags), 1) / 4.0))
            out.append(
                {
                    "id": inf.id,
                    "kind": inf.kind,
                    "strength": inf.strength,
                    "description": inf.description,
                    "couples": inf.couples,
                    "coupled_state": coupled_mags,
                    "pull_on_system": round(pull, 4),  # higher = more drag / entropy injection
                }
            )
        out.sort(key=lambda x: -x["pull_on_system"])
        return out

    def apply_dimension_scores(self, scores: dict[str, float], blend: float = 0.35) -> None:
        """
        Update measured Mag from dimension scores in [0,1].
        measured = (1-blend)*prior + blend*(score*zenith)
        """
        touch: dict[str, list[float]] = {}
        for dim, score in scores.items():
            for nid in self.dimension_node_map.get(dim, []):
                touch.setdefault(nid, []).append(score)
        for nid, scs in touch.items():
            if nid not in self.nodes:
                continue
            n = self.nodes[nid]
            avg = sum(scs) / len(scs)
            target = avg * n.zenith
            prior = n.effective
            n.measured = (1.0 - blend) * prior + blend * target
        self.history.append({"scores": scores, "energy": self.dirichlet_energy()})

    def snapshot(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "dirichlet_energy": round(self.dirichlet_energy(), 6),
            "anchors": {
                aid: {
                    "mean_mag": round(self.anchor_mag(aid), 4),
                    "nodes": {
                        n.name: {
                            "mag": n.mag,
                            "measured": n.measured,
                            "effective": round(n.effective, 4),
                            "zenith": n.zenith,
                            "tags": n.tags,
                        }
                        for n in self.nodes.values()
                        if n.anchor == aid
                    },
                }
                for aid in sorted({n.anchor for n in self.nodes.values()})
            },
            "bonds": [asdict(b) for b in self.bonds],
            "influences": self.influence_field(),
        }

    def to_markdown(self) -> str:
        snap = self.snapshot()
        lines = [
            f"# Vector Map — {self.metadata.get('name', 'mirror')}",
            "",
            f"**Dirichlet energy:** `{snap['dirichlet_energy']}`  ",
            f"**Physics:** {self.metadata.get('physics', '')}  ",
            f"**Locus:** {self.metadata.get('locus', '')}",
            "",
            "## Anchors",
            "",
        ]
        for aid, body in snap["anchors"].items():
            lines.append(f"### {aid} (mean Mag={body['mean_mag']})")
            lines.append("")
            lines.append("| Node | Seed Mag | Measured | Effective | Zenith |")
            lines.append("|------|----------|----------|-----------|--------|")
            for name, n in body["nodes"].items():
                m = "—" if n["measured"] is None else f"{n['measured']:.3f}"
                lines.append(
                    f"| {name} | {n['mag']:.2f} | {m} | {n['effective']:.3f} | {n['zenith']:.2f} |"
                )
            lines.append("")
        lines.append("## Surrounding influences (sorted by pull)")
        lines.append("")
        lines.append("| Id | Kind | Strength | Pull | Couples |")
        lines.append("|----|------|----------|------|---------|")
        for inf in snap["influences"]:
            lines.append(
                f"| {inf['id']} | {inf['kind']} | {inf['strength']:.2f} | "
                f"{inf['pull_on_system']:.3f} | {', '.join(inf['couples'])} |"
            )
        lines.append("")
        lines.append("## Influence notes")
        lines.append("")
        for inf in snap["influences"]:
            if inf.get("description"):
                lines.append(f"- **{inf['id']}**: {inf['description']}")
        lines.append("")
        return "\n".join(lines)

    def save_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.snapshot(), indent=2), encoding="utf-8")


def load_vector_map(path: str | Path) -> VectorMap:
    p = Path(path)
    data = _load_yaml(p)
    return VectorMap.from_dict(data)
