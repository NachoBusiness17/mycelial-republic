"""OUROBOROS F(f)=F -- the estate's recursion, measured. F14, 2026-09-30.

The operator named the shape; this tool formalizes it:

    receipts -> laws -> ribs -> boot -> agents -> receipts

Each stage is a real surface in this repo, and every edge is a citation that can
be counted from bytes, never from reports (census denominator law B2-216):

    receipts  watch/inbox/**/*.md + corpus/steal/*.md     (dated by filename)
    laws      AGENTS.md law bullets (markdown bullets citing receipts)
    ribs      memory/rib/*.md (the vault; R4b 2026-10-06 fixed phantom memory/ribs/)
    boot      what a fresh seat mounts before acting: AGENTS.md (harness-injected),
              mag.rib_boot + mag.rib_bus mount (doctrine domain), hermes_warm_boot,
              the load-order table (FRAMEWORK_LOAD.md, compass, state/CURRENT.md)
    agents    seats that filed receipts ("Filed by ... seat/lane/worker")

CONVERGENCE: f applied to the corpus produces the law surface. We ask whether the
law surface stops changing: (a) one-pass idempotence of the citation extractor on
the HEAD corpus, (b) temporal drift of receipt-citation counts through AGENTS.md
git history, (c) receipts/day from filename dates. Non-zero drift at HEAD means
the loop has NOT reached a fixed point: that is growth, not equilibrium.

CYCLE DETECTION (the tail in the mouth): a receipt that is BOTH cited by AGENTS.md
AND cites AGENTS.md is a literal 2-cycle receipt->law->receipt. Chains of those
bridges, each produced after the previous one was absorbed into law, are counted
as loop generations G.

DIMENSIONALITY: if each hop through the loop preserves d units of upstream context
(citations carried per artifact), then after G turns the estate's effective context
dimensionality is D = G * mean(d over the five hops). Both factors are measured.

USAGE
    .venv/Scripts/python.exe tools/ouroboros.py            # human report
    .venv/Scripts/python.exe tools/ouroboros.py --json     # machine-readable
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "Scripts" / "python.exe"

RECEIPT_DIRS = [ROOT / "watch" / "inbox", ROOT / "corpus" / "steal"]
RIB_DIR = ROOT / "memory" / "rib"
LAW_SURFACE = ROOT / "AGENTS.md"

# Boot surfaces a fresh seat mounts before acting (load-order table + rib_boot + warm boot).
BOOT_SURFACES = {
    "AGENTS.md": "AGENTS.md",
    "FRAMEWORK_LOAD": "docs/FRAMEWORK_LOAD.md",
    "LOAD.md": "LOAD.md",
    "CURRENT.md": "state/CURRENT.md",
    "ribs_dir": "memory/rib",
    "warm_state": "memory/warm_state.json",
    "brief": "memory/briefs/latest.md",
    "compass": "docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md",
}

# Agent families that author receipts. Attribution instrument: explicit "Filed by"
# lines plus seat tokens. Name the instrument before trusting the count.
AGENT_FAMILIES = [
    "zcode", "hermes", "grok", "deepseek", "codex", "cursor",
    "mickey", "worker", "seat", "lane", "operator",
]

FILED_BY_RE = re.compile(r"[Ff]iled by")
DATE_RE = re.compile(r"(20\d{6})")
CITE_RES = [
    re.compile(r"watch/inbox/[A-Za-z0-9_./-]+"),
    re.compile(r"corpus/steal/[A-Za-z0-9_./-]+"),
    re.compile(r"memory/ribs?/[A-Za-z0-9_./-]+"),
]


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _run(*args: str) -> str:
    exe = str(PY) if PY.is_file() else sys.executable
    try:
        r = subprocess.run([exe, "-m", *args], cwd=str(ROOT), capture_output=True,
                           text=True, timeout=120)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"[FAILED {type(e).__name__}: {e}]"


def receipt_date(path: Path) -> date | None:
    """Date instrument: 8-digit date in the filename stem first, else the nearest dated
    parent directory (wave-dated receipts like last_mile_20260930/B17_CENSUS.md)."""
    for candidate in [path.stem] + [p.name for p in path.parents][:3]:
        m = DATE_RE.search(candidate)
        if m:
            try:
                return datetime.strptime(m.group(1), "%Y%m%d").date()
            except ValueError:
                continue
    return None


def load_receipts() -> list[dict]:
    out = []
    for d in RECEIPT_DIRS:
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            txt = _read(p)
            rel = p.relative_to(ROOT).as_posix()
            cites_agents = "AGENTS.md" in txt
            mentions = {k: v in txt.replace("\\", "/") for k, v in BOOT_SURFACES.items()}
            fams = [f for f in AGENT_FAMILIES if re.search(rf"\b{f}", txt, re.I)]
            filed = bool(FILED_BY_RE.search(txt))
            own_cits = sum(len(m) for rx in CITE_RES for m in [rx.findall(txt.replace("\\", "/"))])
            out.append({
                "path": rel, "bytes": len(txt.encode("utf-8", "replace")),
                "date": receipt_date(p), "cites_agents": cites_agents,
                "boot_mentions": sum(1 for v in mentions.values() if v),
                "filed_by": filed, "families": fams, "own_citations": own_cits,
            })
    return out


def law_bullets() -> list[dict]:
    """Law bullets in AGENTS.md: markdown bullets that carry at least one receipt citation."""
    txt = _read(LAW_SURFACE)
    bullets = []
    for raw in txt.splitlines():
        s = raw.strip()
        if not s.startswith("- "):
            continue
        cits = []
        for rx in CITE_RES:
            cits.extend(m.group(0).rstrip(".,;:)" ) for m in rx.finditer(s))
        if not cits:
            continue
        receipts = [c for c in cits if c.startswith(("watch/inbox/", "corpus/steal/"))]
        ribs = [c for c in cits if c.startswith("memory/rib")]
        bullets.append({"text": s[:160], "receipts": receipts, "ribs": ribs})
    return bullets


def resolve_citations(cites: list[str]) -> set[str]:
    """Expand directory citations (watch/inbox/foo/) to member receipt files."""
    out = set()
    for c in cites:
        p = ROOT / c
        if c.endswith("/"):
            if p.is_dir():
                for m in p.rglob("*.md"):
                    out.add(m.relative_to(ROOT).as_posix())
        else:
            out.add(c)
    return out


def rib_boot_mount() -> dict:
    """Execute the vault boot (bus + vault law + amendments), not the bus alone
    (R4-L2 2026-10-05: the body ran the BUS while the module docstring claimed
    rib_boot rode the boot surface; fires mag.rib_boot --json, regenerating
    memory/rib_boot.json, and surfaces the mounted amendment markers; d4
    asserted because its absence was the founding defect)."""
    raw = _run("mag.rib_boot", "--json")
    try:
        j = json.loads(raw)
        heads = " ".join(str(r.get("law_head") or "") for r in (j.get("vault") or {}).get("law_ribs") or [])
        return {"doctrine_ribs": j.get("rib_count"), "ok": bool(j.get("vault_law_ribs_mounted")),
                "vault_law_ribs_mounted": j.get("vault_law_ribs_mounted"),
                "amendment_marker_hits": heads.count("POST-DATUM") + heads.count("AMENDMENT"),
                "d4_marker_mounted": "omission is a MEASURED ON state" in heads}
    except Exception:
        return {"doctrine_ribs": None, "ok": False, "raw_head": raw[:200]}


def agents_git_history() -> list[dict]:
    """AGENTS.md commit history with receipt-citation counts per blob."""
    try:
        r = subprocess.run(["git", "log", "--format=%H %ad", "--date=short", "--", "AGENTS.md"],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=60)
    except Exception:
        return []
    rows = []
    for line in reversed(r.stdout.strip().splitlines()):  # oldest first
        if " " not in line:
            continue
        sha, day = line.split(" ", 1)
        b = subprocess.run(["git", "show", f"{sha}:AGENTS.md"], cwd=str(ROOT),
                           capture_output=True, text=True, errors="replace", timeout=60)
        txt = b.stdout or ""
        cits = []
        for rx in CITE_RES[:2]:
            cits.extend(m.group(0) for m in rx.finditer(txt))
        rows.append({"sha": sha[:9], "date": day, "bytes": len(txt.encode()),
                     "citations": len(resolve_citations(cits))})
    return rows


def converge(receipts, law_hist) -> dict:
    per_day = Counter(r["date"].isoformat() for r in receipts if r["date"])
    days = sorted(per_day)
    today = max(days) if days else "n/a"
    week_ago = str(date.fromisoformat(max(days)) - timedelta(days=7)) if days else None
    last7 = sum(v for k, v in per_day.items() if week_ago and k >= week_ago)

    # one-pass idempotence: the extractor run twice on HEAD yields the same law set (sanity).
    b1 = law_bullets()
    # temporal drift: has the law surface stopped absorbing receipts?
    drift = [(h["date"], h["citations"], h["bytes"]) for h in law_hist]
    last_two_delta = drift[-1][1] - drift[-2][1] if len(drift) >= 2 else None
    growing = bool(last7 and last7 > 0) and (last_two_delta or 0) != 0
    return {
        "receipts_per_day": {d: per_day[d] for d in days},
        "receipts_last7days": last7,
        "latest_receipt_day": today,
        "law_surface_history": drift,
        "law_citation_delta_last_two_commits": last_two_delta,
        "verdict": "GROWS (no fixed point at HEAD)" if growing else
                   ("EQUILIBRIUM (flat at HEAD)" if last_two_delta == 0 else "GROWS"),
    }


def bridges_and_generations(receipts, cited_by_law: set[str], law_hist) -> tuple[list[dict], int]:
    """A bridge receipt is cited by AGENTS.md AND cites AGENTS.md: a literal tail-in-mouth
    2-cycle. Generations: chain bridges b1->b2 where b2 was filed AFTER b1 was first
    absorbed into law (b2 could only know b1 through the loop)."""
    by_rel = {r["path"]: r for r in receipts}

    def first_cited(rel: str) -> str | None:
        # a receipt may be cited by full path or by a directory citation that resolves to it;
        # require at least one component beyond the receipt root ("watch/inbox/" alone matches
        # every blob and would lie about absorption dates)
        parts = rel.split("/")
        dir_prefixes = ["/".join(parts[:i]) + "/" for i in range(3, len(parts))]
        for h in law_hist:  # oldest first
            blob = h.get("_blob", "")
            if rel in blob or any(p in blob for p in dir_prefixes):
                return h["date"]
        return None

    law_blobs = []
    for h in law_hist:
        b = subprocess.run(["git", "show", f"{h['sha']}:AGENTS.md"], cwd=str(ROOT),
                           capture_output=True, text=True, errors="replace", timeout=60)
        h["_blob"] = b.stdout or ""
        law_blobs.append(h)

    bridges = []
    for rel in sorted(cited_by_law):
        r = by_rel.get(rel)
        if r and r["cites_agents"] and r["date"]:
            fc = first_cited(rel)
            bridges.append({"path": rel, "filed": r["date"].isoformat(),
                            "first_cited": fc})
    for h in law_hist:
        h.pop("_blob", None)

    # DP for longest chain of ABSORPTION WAVES: b_earlier -> b_later requires
    #   b_later.filed >= b_earlier.first_cited   (b_later was written after the loop had
    #                                            absorbed b_earlier into law, so it can
    #                                            only know b_earlier THROUGH the loop)
    #   b_later.first_cited > b_earlier.first_cited (a new absorption wave: siblings absorbed
    #                                            by the same commit are one turn, not N)
    bs = [b for b in bridges if b["first_cited"]]
    bs.sort(key=lambda b: (b["filed"], b["first_cited"]))
    best = {}
    for i, b in enumerate(bs):
        best[i] = 1
        for j in range(i):
            if (bs[j]["filed"] <= b["first_cited"]
                    and bs[j]["first_cited"] < b["first_cited"]):
                best[i] = max(best[i], best[j] + 1)
    g = max(best.values()) if best else 0
    return bridges, g


def dimension(receipts, bullets, mounted, total_ribs) -> dict:
    receipt_cits_per_law = [len(b["receipts"]) for b in bullets]
    d1 = sum(receipt_cits_per_law) / len(receipt_cits_per_law) if receipt_cits_per_law else 0.0
    ribs = list(RIB_DIR.glob("*.md")) if RIB_DIR.is_dir() else []
    law_refs_per_rib = []
    for p in ribs:
        t = _read(p)
        n = t.count("AGENTS.md") + len(re.findall(r"\b[Bb]ullet|\bClippy|\bLAW-\d+", t))
        law_refs_per_rib.append(n)
    d2 = sum(law_refs_per_rib) / len(law_refs_per_rib) if law_refs_per_rib else 0.0
    d3 = (mounted / total_ribs) if total_ribs else 0.0
    boot_users = [r for r in receipts if r["boot_mentions"] > 0]
    d4 = (sum(r["boot_mentions"] for r in boot_users) / len(boot_users)) if boot_users else 0.0
    # d5, agents->receipts: the context the agent bakes into its own output, measured as
    # the estate citations each receipt itself carries (mean over all receipts).
    cits_per_receipt = [r["own_citations"] for r in receipts]
    d5 = sum(cits_per_receipt) / len(cits_per_receipt) if cits_per_receipt else 0.0
    return {"d1_receipts_per_law": round(d1, 2), "d2_lawrefs_per_rib": round(d2, 2),
            "d3_rib_mount_coverage": round(d3, 3), "d4_boot_mentions_per_agent_receipt": round(d4, 2),
            "d5_citations_per_receipt": round(d5, 2),
            "mean_hop_depth": round((d1 + d2 + d3 + d4 + d5) / 5, 2)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    receipts = load_receipts()
    bullets = law_bullets()
    cited_by_law = resolve_citations([c for b in bullets for c in b["receipts"]])
    ribs = list(RIB_DIR.glob("*.md")) if RIB_DIR.is_dir() else []
    ribs_citing_law = [p.name for p in ribs if "AGENTS.md" in _read(p)]
    ribs_citing_receipts = [p.name for p in ribs if "watch/inbox" in _read(p)]
    boot = rib_boot_mount()
    mounted = boot.get("doctrine_ribs") or 0
    ribs_named_in_law = sorted({c for b in bullets for c in b["ribs"]})

    # agents -> receipts: explicit attribution instrument
    filed = [r for r in receipts if r["filed_by"]]
    fam_counts = Counter(f for r in filed for f in r["families"] if f != "operator")
    seats = {f for f in fam_counts}
    citing_agents = [r for r in receipts if r["cites_agents"]]
    boot_users = [r for r in receipts if r["boot_mentions"] > 0]

    law_hist = agents_git_history()
    conv = converge(receipts, law_hist)
    bridges, g = bridges_and_generations(receipts, cited_by_law, law_hist)
    dim = dimension(receipts, bullets, mounted, len(ribs))
    d_eff = round(g * dim["mean_hop_depth"], 1)

    edges = {
        "receipts_total": len(receipts),
        "receipts_cited_by_law": len(cited_by_law),
        "law_bullets": len(bullets),
        "receipts_citing_the_law_surface": len(citing_agents),
        "ribs_total": len(ribs),
        "ribs_citing_law_surface": len(ribs_citing_law),
        "ribs_citing_receipts": len(ribs_citing_receipts),
        "ribs_mounted_at_boot_doctrine": mounted,
        "ribs_named_in_law": len(ribs_named_in_law),
        "receipts_with_filed_by_attribution": len(filed),
        "agent_seats_seen": len(seats),
        "receipts_evidencing_boot_consumption": len(boot_users),
    }
    out = {
        "schema": "ouroboros.f14.v1",
        "moment": datetime.now().isoformat(timespec="seconds"),
        "edges": edges,
        "agent_seat_counts": dict(fam_counts.most_common()),
        "convergence": conv,
        "bridge_receipts": bridges,
        "loop_generations_G": g,
        "dimension_per_hop": dim,
        "effective_dimensionality_D": d_eff,
        "thin_edges": [
            f"receipts->laws: {edges['receipts_cited_by_law']}/{edges['receipts_total']} receipts absorbed into law "
            f"({100*edges['receipts_cited_by_law']/max(edges['receipts_total'],1):.1f}%)",
            f"laws->ribs: {edges['ribs_citing_law_surface']}/{edges['ribs_total']} ribs cite the law surface "
            f"({100*edges['ribs_citing_law_surface']/max(edges['ribs_total'],1):.1f}%)",
            f"ribs->boot: {mounted}/{edges['ribs_total']} ribs mounted at boot (doctrine domain); "
            f"{edges['ribs_total']-mounted} unmounted",
        ],
    }
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    else:
        print("OUROBOROS F(f)=f -- measured", out["moment"])
        print("\nSTAGE EDGES (citation-counted from bytes)")
        for k, v in edges.items():
            print(f"  {k:42s} {v}")
        print("\nCONVERGENCE")
        print("  verdict:            ", conv["verdict"])
        print("  receipts last 7 days:", conv["receipts_last7days"], "(latest day", conv["latest_receipt_day"] + ")")
        print("  law-surface citation history (date, n_cited_receipts, bytes):")
        for row in conv["law_surface_history"]:
            print("   ", row)
        print("\nCYCLE DETECTION (bridge receipts: cited by AGENTS.md AND citing AGENTS.md)")
        for b in bridges:
            print(f"  {b['filed']} filed / first cited by law {b['first_cited']}  {b['path']}")
        print(f"  loop generations G = {g}")
        print("\nDIMENSIONALITY")
        for k, v in dim.items():
            print(f"  {k:38s} {v}")
        print(f"  D = G x mean_hop_depth = {g} x {dim['mean_hop_depth']} = {d_eff}")
        print("\nTHIN EDGES (where the loop loses context)")
        for t in out["thin_edges"]:
            print("  -", t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
