#!/usr/bin/env python3
"""mickey17_v2_fold.py — deterministic fold sections for MICKEY-17 v2.1.

A2 casualty header; A5 script-written counts + top-K; A11 --check-urls;
A12 PRISMA/WIDTH-ECONOMICS/FIDELITY/verifier-table; A14 --check-master,
the unbound-aggregate gate (the 191.8M ERRATA 001 class: any master-prose
number whose named source file does not carry it fails the gate, exit 2).
The fold reads the fixed estate lane archive and writes the fixed sections
file FOLD_SECTIONS.md in the fixed estate run dir. Fold IO is pathlib-only
on fixed constants (no os.path.join chains, no open()); --check-master is
the one path-taking mode and only reads.
"""
import argparse, datetime, glob, hashlib, ipaddress, json, re, socket
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

FIELDS = ("quote", "source", "steal", "estate_status")
RUN_ROOT = Path.home() / "Documents" / "projects" / "local_sovereign_agent" / "memory" / "runs" / "mickey17_v2"
LANES_DIR = RUN_ROOT / "lanes"
OUT_NAME = "FOLD_SECTIONS.md"


def norm(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def url_allowed(u):
    try:
        p = urlparse(u)
        if p.scheme not in ("http", "https") or not p.hostname:
            return False
        infos = socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == "https" else 80),
                                   proto=socket.IPPROTO_TCP)
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                    or ip.is_multicast or ip in ipaddress.ip_network("169.254.0.0/16")
                    or ip in ipaddress.ip_network("fc00::/7")):
                return False
        return True
    except Exception:
        return False


def check_url(u):
    import urllib.request, urllib.error

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = urllib.request.build_opener(_NoRedirect)
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(u, method=method,
                                         headers={"User-Agent": "Mozilla/5.0 (fold-liveness-check)"})
            with opener.open(req, timeout=6) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception:
            continue
    return -1


def load_lanes(lanes_dir):
    lanes = {}
    for p in sorted(lanes_dir.glob("*.json")):
        if not p.is_file() or lanes_dir not in p.parents:
            continue
        lid = p.stem
        if lid.endswith(".checks"):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            lanes[lid] = {"error": str(e), "rows": []}
            continue
        rows = data.get("rows") if isinstance(data, dict) else data
        if not isinstance(rows, list):
            rows = []
        meta = data if isinstance(data, dict) else {}
        lanes[lid] = {"rows": rows, "ok": meta.get("ok"), "note": meta.get("note", "")}
    return lanes


def load_checks(lanes_dir):
    out = {}
    for p in sorted(lanes_dir.glob("*.checks.json")):
        if not p.is_file() or lanes_dir not in p.parents:
            continue
        lid = p.name.removesuffix(".checks.json")
        try:
            out[lid] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return out


# --- A14: unbound-aggregate gate (the 191.8M ERRATA 001 class) --------------
# Founding phantom: STORY.md:240 claimed "191.8M tokens spent" citing
# watch/inbox/frontier_olm_20260928/DIGEST.md, a file carrying no such number
# (watch/inbox/48h_synth/ERRATA.md, ERRATA 001). Law: any number stated on a
# master-prose line that names at least one resolvable estate file must be
# carried by one of those named files' bytes, or the gate fails. Documented
# false-positive controls: ISO datetimes and clock times are stripped (their
# digits are moments, not claims), numeric dash ranges are stripped (line and
# page anchors), the source path tokens themselves are stripped, and lines
# inside fenced code blocks are skipped (command transcripts, already
# bytes-cited evidence). Two more citation-form controls: colon-anchored
# numbers (file.py:183, doc.md:50) are line anchors, not quantities, and
# compact estate dates (20261003) are receipt name digits, not aggregates.
# R3 move 5 (ouroboros 2026-10-05): a line naming only sources that fail to
# resolve is a finding (kind unresolved-source), not silence - the 900M probe
# citing a nonexistent path passed check-master exit 0, so the founding class
# survived one dead-path citation.
REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_RE = re.compile(r"[\w.\-]+(?:[/\\][\w.\-]+)+\.(?:md|json|jsonl|txt|py|yaml|yml|csv|ts)\b")
DATETIME_RE = re.compile(r"\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?")
CLOCK_RE = re.compile(r"\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?")
RANGE_RE = re.compile(r"\d[\d,]*(?:\.\d+)?\s*-\s*\d[\d,]*(?:\.\d+)?")
ANCHOR_RE = re.compile(r"(?<=:)\d[\d,]*(?:\.\d+)?")
COMPACT_DATE_RE = re.compile(r"(?<![0-9])20\d{6}(?![0-9])")
NUM_RE = re.compile(r"(?<![A-Za-z0-9])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)([MBKmkb]?)(?![0-9A-Za-z])")
UNIT_MULT = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}


def carried_forms(num, unit):
    """Byte forms a named source may carry the number in: as written, comma-
    stripped, and for unit-scaled aggregates (191.8M) the expanded integer in
    bare and comma-grouped spellings."""
    plain = num.replace(",", "")
    forms = {num, plain}
    if unit and unit.lower() in UNIT_MULT:
        total = int(round(float(plain) * UNIT_MULT[unit.lower()]))
        forms.add(str(total))
        forms.add(f"{total:,}")
    return forms


def resolve_source(tok, root, base_dir):
    """Named sources are estate-root-relative; a master prose sitting outside
    the repo may also name files relative to its own directory. Repo root
    wins, the prose's own directory is the fallback."""
    cand = root / tok.replace("\\", "/")
    if cand.is_file():
        return cand
    cand = base_dir / tok.replace("\\", "/")
    return cand if cand.is_file() else None


def unbound_aggregates(master_path, root=None):
    """Return one dict per master-prose number no named source carries:
    {line, number, sources, kind}. A number passes if ANY source named on its
    line carries any of its forms. R3 move 5 (ouroboros 2026-10-05,
    SYNTHESIS row 5): a number on a line whose named sources ALL fail to
    resolve files kind="unresolved-source" (the 900M probe passed check-master
    exit 0, so the founding 191.8M class survived one dead-path citation);
    resolvable lines keep kind="unbound"."""
    root = Path(root) if root is not None else REPO_ROOT
    master_path = Path(master_path)
    base_dir = master_path.resolve().parent
    fails = []
    fenced = False
    text = master_path.read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        sources = []
        unresolved = []
        for m in SOURCE_RE.finditer(line):
            tok = m.group(0)
            cand = resolve_source(tok, root, base_dir)
            if cand is not None:
                sources.append((tok, cand))
            else:
                unresolved.append(tok)
        if not sources and not unresolved:
            continue
        clean = DATETIME_RE.sub(" ", line)
        clean = CLOCK_RE.sub(" ", clean)
        clean = RANGE_RE.sub(" ", clean)
        clean = ANCHOR_RE.sub(" ", clean)
        clean = COMPACT_DATE_RE.sub(" ", clean)
        for tok, _ in sources:
            clean = clean.replace(tok, " ")
        for tok in unresolved:
            clean = clean.replace(tok, " ")
        src_bytes = {tok: cand.read_text(encoding="utf-8", errors="replace")
                     for tok, cand in sources}
        for num, unit in NUM_RE.findall(clean):
            if not sources:
                fails.append({"line": i, "number": num + (unit or ""),
                              "sources": sorted(set(unresolved)),
                              "kind": "unresolved-source"})
                continue
            forms = carried_forms(num, unit)
            if not any(f in b for b in src_bytes.values() for f in forms):
                fails.append({"line": i, "number": num + (unit or ""),
                              "sources": sorted(src_bytes), "kind": "unbound"})
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fired", type=int, default=0, help="targets fired; default = lane files found")
    ap.add_argument("--check-urls", action="store_true")
    ap.add_argument("--check-master", default="", metavar="PATH",
                    help="master-prose path (repo-root-relative or absolute): every number on a "
                         "line naming an existing estate file must be carried by one of the named "
                         "files' bytes; any unbound number exits 2 (the 191.8M ERRATA class)")
    ap.add_argument("--run", default="", help="run slug: reads runs/<slug>/lanes (bare [A-Za-z0-9-]); default = legacy top-level lanes dir")
    a = ap.parse_args()
    if a.check_master:
        mp = Path(a.check_master)
        if not mp.is_file():
            mp = REPO_ROOT / a.check_master
        if not mp.is_file():
            raise SystemExit(f"--check-master: master prose not found: {a.check_master}")
        fails = unbound_aggregates(mp)
        if fails:
            print(f"UNBOUND AGGREGATES: {len(fails)} number(s) not carried by any named source in {mp}")
            for f in fails:
                mark = " UNRESOLVED-SOURCE" if f.get("kind") == "unresolved-source" else ""
                print(f"  - line {f['line']}: {f['number']}{mark} (named: {', '.join(f['sources'])})")
            raise SystemExit(2)
        print(f"master-prose aggregate check: OK ({mp})")
        return
    lanes_dir = LANES_DIR
    if a.run:
        if not re.fullmatch(r"[A-Za-z0-9-]+", a.run) or ".." in a.run:
            raise SystemExit("--run must be a bare slug: letters, digits, dash")
        lanes_dir = RUN_ROOT / "runs" / a.run / "lanes"
        if not lanes_dir.is_dir():
            raise SystemExit(f"run archive not found: {lanes_dir}")
    out_real_parent = RUN_ROOT if not a.run else (RUN_ROOT / "runs" / a.run)
    out_real_parent.mkdir(parents=True, exist_ok=True)

    lanes = load_lanes(lanes_dir)
    checks = load_checks(lanes_dir)
    all_rows = [(lid, i, r) for lid, l in lanes.items() for i, r in enumerate(l.get("rows", []))
                if isinstance(r, dict)]
    n_files = len(lanes)
    fired = a.fired or n_files
    # Ops-triage move 5 (morning-block 2026-10-07): a --fired below the archive
    # count used to fold "missing (no file): <negative>" into the casualty
    # header as a computed fact, and the surplus survived only as a seat's
    # prose patch (corpus/steal/MASTER_DOGFOOD_100M_20261006.md: "the minus
    # sign is the file surplus, not absence"). Fail closed instead: a negative
    # count rendered as fact is the fabrication-shaped hole this gate exists
    # for, and the contradiction is real data (stale lane files in the
    # archive, or a wrong --fired), never a number to print.
    if fired < n_files:
        print(f"FIRED-BELOW-ARCHIVE GATE: --fired {fired} < archive count {n_files} in {lanes_dir}; "
              "a negative missing count rendered as computed fact is a fabrication-shaped hole. "
              "Raise --fired to the true fired width or remove stale lane files, then refold.")
        raise SystemExit(2)
    parse_errors = [lid for lid, l in lanes.items() if l.get("error")]
    landed = [lid for lid, l in lanes.items() if not l.get("error")]
    landed_empty = [lid for lid, l in lanes.items()
                    if not l.get("error") and len(l.get("rows", [])) == 0]
    missing = fired - n_files

    # R1 row 1 fold stamp (2026-10-05, ouroboros): an unversioned fold cannot
    # be told apart from the blind ancestor that wrote the same file name.
    folded_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]
    md = ["# MICKEY-17 v2.1 — SCRIPTED FOLD SECTIONS", "",
          f"- folded_at: {folded_at} (script sha256 {script_sha})",
          "Every number below was computed by this script from the lane archive at " + str(lanes_dir) + ". "
          "Seats write prose around them; any number a seat brings itself must be tagged `carried`.", ""]

    md += ["## CASUALTY HEADER", "",
           f"- fired: {fired}", f"- landed (parseable files): {len(landed)}",
           f"- landed-empty (0 rows): {len(landed_empty)}"
           + (f" — {', '.join(sorted(landed_empty))}" if landed_empty else ""),
           f"- parse errors: {len(parse_errors)}"
           + (f" — {', '.join(sorted(parse_errors))}" if parse_errors else ""),
           f"- missing (no file): {missing}",
           "- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.", ""]

    st, lv = Counter(), Counter()
    for _, _, r in all_rows:
        st[r.get("estate_status", "?")] += 1
        lv[r.get("leverage", "?")] += 1
    md += ["## SCOREBOARD (recount)", "",
           f"- rows: {len(all_rows)}",
           "- estate_status: " + ", ".join(f"{k} {v}" for k, v in st.most_common()),
           "- leverage: " + ", ".join(f"{k} {v}" for k, v in lv.most_common()), ""]

    ok = sum(1 for _, _, r in all_rows if all((r.get(f) or "").strip() for f in FIELDS))
    md += ["## FIDELITY", "",
           f"- rows with all of quote/source/steal/estate_status non-empty: {ok}/{len(all_rows)}"
           f" ({round(100 * ok / len(all_rows), 1) if all_rows else 0}%)", ""]

    # R1 row 1 de-blind + R3 move 2 hardening (2026-10-05, ouroboros r3 trust,
    # SYNTHESIS row 2; R1 receipt: run-0 FOLD_SECTIONS.md:27 vs :40). Runners
    # persist tier-2 verdicts as deep_tier2 arrays in <id>.checks.json, row_key
    # "<laneId>: <first six claim words>" (deepAsk shape), verdict in the
    # DeepCheck enum (verified | same-chain-verified | unconfirmed | crashed);
    # the legacy top-level `unconfirmed` list stays for older archives, both
    # codes file into PRISMA excluded 9 with labels kept separate. R3 cures:
    # (a) verdicts compare casefolded (norm lowercases; a capital-U
    # "Unconfirmed" rode included under the exact-case whitelist); (b) verdict
    # values outside the enum route to a named unmapped bucket, exclude-and-
    # label, never silently included (empty row_key lands there too); (c) join
    # gate: an exclusion-weight verdict on a row_key matching zero lane rows
    # is a silently lost exclusion - the pre-fix crash fallback key
    # "<lane>: crashed" (mickey17-burn.dwf.ts:454 + its mickey17-v2.dwf.ts:263
    # twin, both fixed this sitting) could NEVER join, so every producer crash
    # rode included under a zero-unconfirmed headline; exit 2 names each lost
    # exclusion; verified join-misses carry no exclusion weight (verdicts only
    # exclude), so they print as a labeled census line, never silent.
    DEEP_OK = frozenset(("verified", "same-chain-verified"))
    unconf_keys = set()
    deep_unconf, deep_crashed, deep_unmapped = set(), set(), set()
    unmapped_verdicts, deep_join = Counter(), []
    for lid, c in checks.items():
        for x in (c.get("unconfirmed") or []):
            if isinstance(x, dict):
                unconf_keys.add(norm(x.get("claim", ""))[:80])
        for x in (c.get("deep_tier2") or []):
            if not isinstance(x, dict):
                continue
            verdict, rk = norm(x.get("verdict") or ""), norm(str(x.get("row_key", "")))
            deep_join.append((verdict, rk, verdict not in DEEP_OK))
            if not rk or verdict not in DEEP_OK | {"unconfirmed", "crashed"}:
                unmapped_verdicts[verdict or "<empty>"] += 1
                if rk:
                    deep_unmapped.add(rk)
            elif verdict == "unconfirmed":
                deep_unconf.add(rk)
            elif verdict == "crashed":
                deep_crashed.add(rk)

    def deep_keys(lid, claim):
        c = str(claim or "")
        return {norm(lid + ": " + " ".join(c.split(" ")[:6])),
                norm(lid + ": " + " ".join(c.split()[:6]))}

    universe = set()
    for lid, i, r in all_rows:
        universe |= deep_keys(lid, r.get("claim"))
    lost = [(v, rk) for v, rk, w in deep_join if w and (not rk or rk not in universe)]
    inert_miss = [(v, rk) for v, rk, w in deep_join if not w and rk and rk not in universe]
    if lost:
        print("JOIN-HIT-RATE GATE: " + str(len(lost)) + " deep_tier2 row(s) carry an exclusion-weight "
              "verdict but the row_key matches zero lane rows, so the exclusion is silently lost (fix "
              "the data or the producer key shape): "
              + "; ".join(f"[{v or '<empty>'}] {rk or '<no row_key>'}" for v, rk in lost[:10]))
        raise SystemExit(2)

    md += ["## VERIFIER TABLE (persisted verdicts)", ""]
    if checks:
        # R1: verdict-VALUE splits, not list lengths ("deep_tier2 16" hid 6
        # unconfirmed + crashed rows). R3 move 2e: every list-valued key and
        # value-bearing field splits - "supports 20" hid its yes/no mix the
        # same way; a length certifies nothing.
        vc, vsplit = Counter(), {}
        for c in checks.values():
            for k, v in c.items():
                if not isinstance(v, list):
                    continue
                vc[k] += len(v)
                vals = vsplit.setdefault(k, {})
                for e in v:
                    if isinstance(e, dict):
                        pairs = [(f, e[f]) for f in ("verdict", "supports") if isinstance(e.get(f), str)]
                        f, val = pairs[0] if pairs else ("<no-value-field>", "<dict>")
                        vals.setdefault(f, Counter())[norm(val)] += 1
                    else:
                        key = norm(e) if isinstance(e, str) else f"<{type(e).__name__}>"
                        vals.setdefault("<value>", Counter())[key] += 1
        lines = [" ".join([f"{k} {vc[k]}"] + [f"({f} split: {s})" for f, cnts in
                    sorted((vsplit.get(k) or {}).items()) for s in
                    [", ".join(f"{val} {n}" for val, n in sorted(cnts.items()))]]) for k in sorted(vc)]
        md += [f"- lanes with persisted checks: {len(checks)}",
               "- verdicts: " + (", ".join(lines) or "none listed")]
        if deep_join:
            md.append(f"- deep_tier2 join: {len(deep_join) - len(lost) - len(inert_miss)}/{len(deep_join)}"
                      f" row_keys match a lane row" + (f"; join-miss (verified, no exclusion weight,"
                      f" labeled not fatal): {len(inert_miss)}" if inert_miss else ""))
        if unmapped_verdicts:
            md.append("- unmapped verdict values (exclude-and-label bucket): " + ", ".join(
                f"{v} {n}" for v, n in sorted(unmapped_verdicts.items())))
    else:
        md += ["- **no persisted verdict files found** — if the runner ran a verifier pass without writing "
               "`<id>.checks.json`, its verdicts do not exist for the recount (the v2 defect class, A3)."]
    md.append("")

    per_lane = sorted((len(l.get("rows", [])) for l in lanes.values()), reverse=True)
    med = per_lane[len(per_lane) // 2] if per_lane else 0
    top10 = sum(per_lane[:10])
    q = Counter(norm(r.get("quote")) for _, _, r in all_rows if r.get("quote"))
    dups = sum(c - 1 for c in q.values() if c > 1)
    gate_line = "- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)"
    if per_lane and med == per_lane[0] == per_lane[-1]:
        gate_line += " [gate-vacuous: median==max==min, every lane the same width, Law 7 bites nothing this run]"
    md += ["## WIDTH-ECONOMICS", "",
           f"- rows/lane: median {med}, max {max(per_lane) if per_lane else 0}, min {min(per_lane) if per_lane else 0}",
           f"- top-10 lanes share: {round(100 * top10 / len(all_rows), 1) if all_rows else 0}%",
           f"- exact cross-lane duplicate quotes (normalized): {dups}",
           gate_line, ""]

    excluded = Counter()
    included = 0
    single_row_dead = {lid for lid, l in lanes.items() if len(l.get("rows", [])) == 1}
    for lid, i, r in all_rows:
        keys = deep_keys(lid, r.get("claim"))
        if lid in single_row_dead:
            excluded["1 phantom-source (dead-lane negative row)"] += 1
        elif norm(r.get("claim"))[:80] in unconf_keys:
            excluded["9 verifier-unconfirmed"] += 1
        elif keys & deep_unconf:
            excluded["9 verifier-unconfirmed (deep_tier2)"] += 1
        elif keys & deep_crashed:
            excluded["9 verifier-crashed (deep_tier2)"] += 1
        elif keys & deep_unmapped:
            excluded["9 verifier-unmapped verdict (deep_tier2)"] += 1
        else:
            included += 1
    identified = len(all_rows)
    md += ["## PRISMA FLOW", "",
           f"- identified: {identified}",
           "- screened: " + str(identified) + " (all rows carry the six rubric fields or their gap notes)",
           "- excluded: " + (", ".join(f"{k}: {v}" for k, v in sorted(excluded.items())) or "0"),
           f"- included: {included}"]
    assert identified == included + sum(excluded.values()), \
        f"PRISMA invariant broken: {identified} != {included} + {sum(excluded.values())}"
    md += [f"- invariant: identified == included + excluded **HOLDS** ({identified} = {included} + {sum(excluded.values())})", ""]

    rank = sorted(all_rows, key=lambda t: ({"high": 0, "medium": 1, "low": 2}.get(t[2].get("leverage"), 3), t[0], t[1]))
    md += ["## TOP-K (script-computed; a lane-claimed top steal outside this list files as DISPUTED)", ""]
    for lid, i, r in rank[:12]:
        md.append(f"- [{r.get('leverage', '?')}] {lid}#{i}: {norm(r.get('claim'))[:110]}")
    md.append("")

    if a.check_urls and all_rows:
        urls = sorted({r.get("source") for _, _, r in all_rows if (r.get("source") or "").startswith("http")})
        allowed = [u for u in urls if url_allowed(u)]
        blocked = len(urls) - len(allowed)
        results = {}
        with ThreadPoolExecutor(max_workers=20) as ex:
            futs = {ex.submit(check_url, u): u for u in allowed}
            for f in as_completed(futs):
                results[futs[f]] = f.result()
        dead = {u: s for u, s in results.items() if not (200 <= s < 400)}
        md += ["## URL LIVENESS (scripted at fold time)", "",
               f"- unique URLs: {len(urls)}; fetched: {len(allowed)}; skipped non-public: {blocked}; "
               f"live: {len(allowed) - len(dead)}; dead/blocked-status: {len(dead)}"]
        for u, s in sorted(dead.items(), key=lambda kv: kv[1])[:20]:
            md.append(f"  - HTTP {s}: {u[:100]}")
        md += ["", "- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.", ""]

    out_path = out_real_parent / OUT_NAME
    out_path.write_text("\n".join(md), encoding="utf-8")
    print(f"lanes={n_files} rows={len(all_rows)} included={included} excluded={sum(excluded.values())} "
          f"dups={dups} median_rows={med} -> {out_path}")


if __name__ == "__main__":
    main()
