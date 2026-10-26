"""THE BOOT THAT MOUNTS WHAT THE SEAT FORGETS -- stolen from the verkle chain, not invented.

OPERATOR (2026-09-30): "self steal your mag boot from verkle so you stop forgetting."

WHAT WAS MEASURED FIRST, because there are ALREADY a dozen boot modules in mag/ and the doctrine
is to borrow, never to volunteer a build:
    boot.py               8,446B   0 rib mounts, 0 brief, 0 verkle
    boot_check.py         6,780B   0 rib mounts, 0 brief, 2 verkle mentions
    tripartite_boot.py   18,218B   0 rib mounts, 0 brief, 0 verkle
    ghost_cold_boot.py    7,074B   0 rib mounts, 0 brief, 0 verkle
    hermes_warm_boot.py  10,558B   0 rib mounts, 0 brief, 8 verkle mentions
  So five modules boot the PROCESS and none of them mounts the DOCTRINE. That is the actual gap,
  and it is why a seat can run for a whole night, land 40+ files, produce four receipts, and still
  not have read the vault's frozen ribs that say what the system is FOR. It is not a memory
  failure. It is a missing mount, and it has been missing this entire time.
  (COUNT NOTE, r06#3d 2026-10-05: this docstring once hard-coded "the 51 frozen ribs" and the
  constant went stale -- corpus/steal/MASTER_READ_ESTATE.md measured the vault at 52 or 53 .md
  depending on instrument and moment, stale under both. The count is no longer stated in prose
  anywhere: mount_vault() below counts memory/rib/*.md live at every boot and records the number
  with its moment. A census is a snapshot of one tree at one moment, never a constant.)

THE LAWS THIS MOUNTS, verbatim from the ribs rather than from memory:
    "The invariant: a deterministic instruction set, anchored on shared cryptographic primitives,
     explains navigable paths through stochastic environments. The relation (the frozen spec) is
     what persists; the model is interchangeable; the chain is the ground truth."
    "chain=record, window=reasoning surface. Down seats stay records. Never store window as truth."
    "RIB-DEBUG every finished piece (trust bytes, not reports)."
    "Do not prompt the operator for permission to run framework ops."
    "T0 secrets never remote; T1 private never train-on-input; T2 public remote OK; T3 irreversible
     human L3 seal."

READ-ONLY BY LAW. mount() on the rib bus is read-only. publish() FOLDS A VERKLE KNOT and is
therefore never called here -- not once, not behind a flag. The chain is read-only per the
operator's standing ruling of 2026-09-07. This module can only read, and that is enforced in code
rather than promised in a comment.

USAGE
    python -m mag.rib_boot              # full mount, printed
    python -m mag.rib_boot --domain doctrine
    python -m mag.rib_boot --json       # machine-readable, for a seat to ingest

VAULT MOUNT (r06#3a, 2026-10-05, corpus/steal/MASTER_READ_ESTATE.md row 2): beside the bus mount
this module now mounts the vault itself -- memory/rib/ -- which it never did while its own
docstring indicted exactly that gap. The five law ribs named by the r06 lane row mount as law
content (head bytes, not title lines); the full vault is censused live so no count can rot again.

AMENDMENT TAILS (R4-L2, 2026-10-05 memory fold, ouroboros): the 1200-char head cut every
POST-DATUM/AMENDMENT section off the mounted law (byte-measured: the amendment blocks sat at
normalized chars 5905/6397/2836 on the three amended ribs, all beyond the cut), so the only
law-byte surface in the estate served PRE-amendment doctrine -- the d4 thinking law and the
10-05 free-usage verdict were invisible to the one organ built to carry them. Cure: the head
stays, every amendment section rides AFTER it (amend-never-rewrite applied to the mount: the
pre-amendment law stays readable, the deltas ride behind it), and each rib also carries its
amendments as a separate list so consumers (mag/context_pack.py) can render deltas without
re-splitting the head. The demotion register memory/fold_history/SUPERSEDED.md is pointed at
in every mounted artifact and printout.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

WARM = ROOT / "memory" / "warm_state.json"
BRIEF = ROOT / "memory" / "briefs" / "latest.md"
OUT = ROOT / "memory" / "rib_boot.json"
VAULT = ROOT / "memory" / "rib"
TIP = ROOT / "memory" / "biography" / "verkle_tip.json"
SUPERSEDED = ROOT / "memory" / "fold_history" / "SUPERSEDED.md"

# The law ribs mounted as head+amendment bytes. The original five were named by the
# r06 lane row by staleness class (r06#3 steal sentence):
# "top-N ribs by staleness class: DRIVING_LADDER, MODEL_GATES, INFERENCE_BUDGET,
# FREE_USAGE_POLICY, DESCENT_PROTOCOL". Carried as filenames so a rename fails loud here
# instead of mounting silently nothing.
# R4b (2026-10-05, ouroboros R4 synthesis move 6, consumer-or-strike): the behavior-cards
# deck rides as a sixth mount. Its rib promised "the seat warms it at boot" while the
# consumer census found only the miner (tools/behavior_cards_x.py); the mount makes the
# claim true, and the deck's dated CARD INDEX amendment (appended to the rib this same
# night) is the slice that rides: the 1200-char head alone would cut off mid first card,
# so the index amendment carries all nine card names at the right boot-time size.
VAULT_RIBS = [
    "RIB_HANDOFF_20261015.md",
    "RIB_WHALE_LAUNCH_20261019.md",
    "RIB_BOB_PRIMARY_20261017.md",
    "RIB_DRIVING_LADDER_20260928.md",
    "RIB_MODEL_GATES_20261001.md",
    "RIB_INFERENCE_BUDGET_20261001.md",
    "RIB_FREE_USAGE_POLICY_20260823.md",
    "RIB_THE_DESCENT_PROTOCOL_20261001.md",
    "RIB_BEHAVIOR_CARDS_20260928.md",
    "RIB_MARATHON_DISORIENTATION.md",
    "RIB_LIGHT_MAZE_20261012.md",
]
LAW_HEAD_CHARS = 1200

# Age bar for the chain-tip anchor: under a live estate the tail moves every few
# minutes (autonomous janitors fold leaves hourly or faster); a tip older than
# this at boot is DEBT, printed and served as such, never silent (R4-L2).
TIP_DEBT_MINUTES = 60

_HEADER_RE = re.compile(r"(?m)^##\s")


def _amendment_sections(t: str) -> list[str]:
    """Every POST-DATUM/AMENDMENT section of a rib, whitespace-normalized, in
    file order. R4-L2 (2026-10-05): the estate's amendment convention wraps
    long headers across consecutive '## ' lines (see
    RIB_INFERENCE_BUDGET_20261001.md:119-120,
    RIB_MODEL_GATES_20261001.md:108-110,
    RIB_FREE_USAGE_POLICY_20260823.md:47-48), so a header-only section merges
    with the section that follows before the marker test runs -- otherwise the
    d4 amendment body would sit under an unmarked continuation header and the
    mount would drop exactly the bytes this exists to carry."""
    marks = [m.start() for m in _HEADER_RE.finditer(t)]
    if not marks:
        return []
    bounds = marks + [len(t)]
    out: list[str] = []
    i = 0
    while i < len(marks):
        lines = t[bounds[i]:bounds[i + 1]].splitlines()
        header = lines[0]
        body = "\n".join(lines[1:]).strip()
        while not body and i + 1 < len(marks):
            # wrapped header: this '## ' line carries no body of its own, the
            # next '## ' line is its continuation, not a fresh section
            i += 1
            nxt = t[bounds[i]:bounds[i + 1]].splitlines()
            header += " " + nxt[0].lstrip("#").strip()
            body = "\n".join(nxt[1:]).strip()
        if "POST-DATUM" in header or "AMENDMENT" in header:
            out.append(" ".join((header + " " + body).split()))
        i += 1
    return out


def mount_vault() -> dict:
    """READ the vault. The boot-order finding (r06, 2026-10-04): this module mounted the
    rib BUS (25 doctrine invariants) and ZERO files from memory/rib/ while 50 of 53 ribs
    carried law content in no boot surface. Cure: count the vault live (the hard-coded
    '51' in the old docstring drifted; never hard-code a census again) and mount the five
    named law ribs as bytes. Read-only like everything else in this module."""
    census = sorted(p.name for p in VAULT.glob("*.md")) if VAULT.is_dir() else []
    laws = []
    for name in VAULT_RIBS:
        f = VAULT / name
        if not f.is_file():
            laws.append({"file": name, "mounted": False,
                         "note": "named law rib missing from the vault -- fails loud on purpose"})
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        head = " ".join(t.split())[:LAW_HEAD_CHARS]
        amendments = _amendment_sections(t)
        if amendments:
            head = " ".join([head] + amendments)
        laws.append({"file": name, "mounted": True, "bytes": len(t.encode("utf-8")),
                     "amendment_count": len(amendments),
                     "law_amendments": amendments,
                     "law_head": head})
    return {"dir": str(VAULT.relative_to(ROOT)), "md_count": len(census),
            "census_moment": datetime.now(timezone.utc).isoformat(),
            "law_ribs": laws, "mounted_count": sum(1 for l in laws if l.get("mounted")),
            "amendments_mounted": sum(l.get("amendment_count", 0) for l in laws
                                      if l.get("mounted"))}


# The laws that matter most when a seat is mid-task and about to over-claim. Carried as data so
# they survive a summary, which is exactly how they were lost tonight.
CORE_LAWS = [
    ("chain-is-truth", "chain=record, window=reasoning. Never store the window as truth."),
    ("model-interchangeable", "The model is a visitor with a pack; the frozen relation persists."),
    ("trust-bytes", "RIB-DEBUG every finished piece. Trust bytes, not reports."),
    ("dont-ask-permission", "Do not prompt the operator to run framework ops."),
    ("rightsized", "cheap-first; frontier scarce; human L3 on irreversible."),
    ("artifact-over-transcript", "DNA: residual + card + content_commit + chain_leaf = filed."),
    ("residual-on-disk", "Residual on disk is truth; chat is heat."),
    ("no-second-scheduler", "Async work to the QUEUE; deterministic must-be-now via tools."),
    ("diesel-over-think", "When in doubt, code the game."),
]


def lawpack_amendment_rows(now: float) -> tuple[dict[str, dict], dict]:
    """The mounted law amendments as lawpack compile rows (R4b move 1,
    2026-10-06, ouroboros R4 fold row 1): the bridge merging the vault's
    POST-DATUM law into tools/thought_quantizer.py's compile input beside
    memory/percolator/invariants.json - before it the two law stacks never
    met and a fresh compile stamp rode over pre-round doctrine (fold S1).
    Reads mount_vault() LIVE, so pack law and boot law cannot fork. Fails
    loud (SystemExit) when a named law rib does not mount: packing silently
    without the vault is the disease this feed cures. Exact-text dedupe
    here; signature-level dedupe still happens compile-side.
    """
    vault = mount_vault()
    laws = vault.get("law_ribs", [])
    unmounted = sorted(str(l.get("file")) for l in laws if not l.get("mounted"))
    if unmounted:
        raise SystemExit(
            "input error: rib vault law ribs failed to mount: "
            + ", ".join(unmounted)
            + " (VAULT_RIBS fails loud on a rename; fix the list or restore "
              "the rib - the compile refuses to pack without the vault)")
    rows: dict[str, dict] = {}
    seen: set[str] = set()
    iso_now = datetime.fromtimestamp(now, tz=timezone.utc).isoformat()
    idx = 0
    for law in laws:
        stem = Path(str(law.get("file"))).stem
        for i, text in enumerate(law.get("law_amendments", []) or []):
            # strip the leading "## " header marks: packs carry law prose,
            # not markdown structure; 25 = the compiler's fragment floor
            text = " ".join(str(text).split()).lstrip("#").strip()
            if len(text) < 25 or text in seen:
                continue
            seen.add(text)
            # key[:12] is the pack id: the ribNN prefix keeps two amendments
            # off one rib from colliding the way bare filenames would
            key = f"rib{idx}:{stem}#{i + 1}"
            idx += 1
            rows[key] = {"text": text, "count": 0, "last_seen": iso_now,
                         "vault_amendment": True}
    feed = {"source": "mag.rib_boot.mount_vault", "dir": "memory/rib",
            "law_ribs_mounted": vault.get("mounted_count"),
            "amendments_mounted": vault.get("amendments_mounted"),
            "rows": len(rows)}
    return rows, feed


def _run(*args: str) -> str:
    py = str(ROOT / ".venv" / "Scripts" / "python.exe")
    exe = py if Path(py).is_file() else sys.executable
    try:
        # R4b (2026-10-06, ouroboros R4 fold S10): HEADLESS law -- this mount runs
        # inside GUI seats (VS Code, z.code), so the venv spawn must carry
        # CREATE_NO_WINDOW on win32 or every boot pops a console on the operator's
        # desktop. Same pattern as mag/boot_regen.py:101 and mag/cost_enforcer.py:363.
        r = subprocess.run([exe, "-m", *args], cwd=str(ROOT), capture_output=True,
                           text=True, timeout=240,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
                           if sys.platform == "win32" else 0)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:                                   # the mount must never kill the seat
        return f"[MOUNT-FAILED: {type(e).__name__}: {e}]"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="doctrine")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    # 1. the chain tip -- READ ONLY. No knot, no append, no publish(). R4-L2
    #    (2026-10-05 memory fold): this block used to read warm_state.json, a
    #    GENERATED snapshot that trailed the live tip by 5 leaves mid-round
    #    tonight, so the boot stamped a stale root as if it were the tail.
    #    Anchor at the chain tail itself (memory/biography/verkle_tip.json)
    #    and serve an age-debt line: tip staleness is visible, never silent.
    chain = {}
    if TIP.is_file():
        try:
            v = json.loads(TIP.read_text(encoding="utf-8"))
            gen = str(v.get("updated_minute") or "")
            age_min = None
            try:
                age_min = round((datetime.now(timezone.utc)
                                 - datetime.fromisoformat(gen)).total_seconds() / 60.0, 1)
            except ValueError:
                age_min = None  # unknown age is itself the debt verdict below
            debt = (f"tip {age_min:.0f} min old at boot" if age_min is not None
                    else "tip age unknown (bad updated_minute)")
            if age_min is not None and age_min > TIP_DEBT_MINUTES:
                debt += (f" -- AGE DEBT over {TIP_DEBT_MINUTES:.0f} min: warm boot owed "
                         "(python -m mag.hermes_warm_boot)")
            chain = {"ok": True, "anchor": "memory/biography/verkle_tip.json",
                     "verkle_root": v.get("root"), "index": v.get("n_leaves"),
                     "last_filename": v.get("last_filename"),
                     "last_session_id": v.get("last_session_id"),
                     "generated": gen, "age_min": age_min, "age_debt": debt}
        except Exception as e:
            chain = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    else:
        chain = {"ok": False,
                 "error": "memory/biography/verkle_tip.json missing -- cannot anchor the boot"}

    # 2. the ribs. mount() only -- publish() folds a knot and is forbidden.
    raw = _run("mag.rib_bus", "mount", "--domain", a.domain)
    ribs = []
    try:
        j = json.loads(raw)
        ribs = j if isinstance(j, list) else j.get("ribs", j.get("items", []))
    except Exception:
        ribs = [{"note": "rib mount returned non-JSON; raw head follows", "raw_head": raw[:400]}]

    # 2b. the VAULT -- the mount that was missing. Bus invariants in, vault law in.
    vault = mount_vault()

    # 3. the live brief -- FROZEN. Read, never written. The tooling refuses to overwrite it and
    #    this module does not try. R4-L2 (2026-10-05): this block served the 2026-09-26 fossil
    #    head verbatim while every pack renderer already diverted it (mag/lanes.py:227-235, the
    #    Q1 poison fix); the same divert rides here so the boot artifact stops injecting the
    #    fossil. state/CURRENT.md is the live truth the freeze banner itself names.
    brief = {}
    if BRIEF.is_file():
        t = BRIEF.read_text(encoding="utf-8", errors="replace")
        if t.lstrip().startswith("# FROZEN"):
            current = ROOT / "state" / "CURRENT.md"
            if current.is_file():
                brief["diverted_from_frozen"] = True
                t = current.read_text(encoding="utf-8", errors="replace")
        brief = {**brief, "chars": len(t), "head": " ".join(t.split())[:600]}

    # 4. the demotion register -- pointed at, never mutated here (R4-L2: the estate's
    #    first demotion instrument; the boot that mounts law must also point at law
    #    the estate retired, or promotion stays one-way).
    superseded = {"path": SUPERSEDED.relative_to(ROOT).as_posix(),
                  "exists": SUPERSEDED.is_file()}

    out = {
        "schema": "rib_boot.v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "publish_called": False,
        "domain": a.domain,
        "chain": chain,
        "rib_count": len(ribs),
        "vault_md_count": vault["md_count"],
        "vault_census_moment": vault["census_moment"],
        "vault_law_ribs_mounted": vault["mounted_count"],
        "vault_amendments_mounted": vault["amendments_mounted"],
        "superseded_register": superseded,
        "vault": vault,
        "core_laws": [{"id": i, "law": l} for i, l in CORE_LAWS],
        "brief": brief,
        "ribs": ribs,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    if a.json:
        print(json.dumps({k: v for k, v in out.items() if k != "ribs"}, indent=2,
                         ensure_ascii=False))
    else:
        print(f"  RIB BOOT -- domain={a.domain}  ribs={len(ribs)}  "
              f"chain_index={chain.get('index')}  root={str(chain.get('verkle_root'))[:16]}  "
              f"brief={brief.get('chars')}B"
              + ("  [DIVERTED from FROZEN brief to state/CURRENT.md]"
                 if brief.get("diverted_from_frozen") else ""))
        print(f"  CHAIN ANCHOR: {chain.get('anchor', 'memory/biography/verkle_tip.json')}"
              f"  {chain.get('age_debt', chain.get('error', ''))}")
        print(f"  VAULT: {vault['md_count']} .md ribs censused {vault['census_moment']}; "
              f"{vault['mounted_count']}/{len(VAULT_RIBS)} law ribs mounted; "
              f"{vault['amendments_mounted']} amendments riding after the heads")
        sup_note = ("present" if superseded["exists"]
                    else "MISSING -- mint it (row 1: the 1693dd2ad convergence retraction)")
        print(f"  SUPERSEDED register: {superseded['path']} ({sup_note})")
        print("  READ-ONLY: no knot folded, publish() not called.\n")
        print("  LAWS MOUNTED")
        for i, l in CORE_LAWS:
            print(f"    {i:22s} {l}")
        print(f"\n  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())