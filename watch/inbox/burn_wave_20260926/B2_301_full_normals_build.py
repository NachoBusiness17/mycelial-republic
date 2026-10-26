"""B2-301 full-normals combined-world hill rebuild (lane B2-476 deep compute).

B2-71 proved the raise at SECTION level: the V2 glossary-locked wording took
the adventure_2d6 section pair to 0.914 (rerun 0.885) over the 0.5 bar. But
the filed settlement (CATHEDRAL_CURVATURE_SCAN_20260921, adventure 0.483
SADDLE) is measured over the WHOLE normals: complete build docs, per-region
blocks, shipped first-match assignment law. This lane closes that gap.

Design:
  seats   seatA = groq openai/gpt-oss-120b (stands in for the grok seat; xai
                 paid-dormant; substitution declared, not hidden)
          seatB = together deepseek-ai/DeepSeek-V4-Flash-0731 (the deepseek
                 v4-flash family that built the original deepseek normal)
  build   per-region sections, ALL SIX regions (water_computer, fractal_maze,
          riddler_optics, riddler_engram, audit_dungeon, adventure_2d6),
          each grounded on that module's own JSON bytes, shared cross-region
          doctrine (the RIB AGREE invariants), V2 glossary-locked wording
          (exact identifiers, never paraphrase). Assembled per seat into a
          complete build normal. adventure_2d6 uses B2-71's winning
          instruction verbatim.
  meter   SHIPPED law, unmodified: tools/curvature_scan.py build_sections +
          curvature are imported and called, never reimplemented. GATE:
          shipped curvature() on the archived 09-21 normals must reproduce
          adventure 0.483 SADDLE before any new number counts.
  falsifier  the full build re-fired fresh at both seats; the claim
          "V2 glossary wording reads HILL over the whole normals" reproduces
          only if the rerun pair ALSO crosses 0.5 under the shipped meter.
  no-stuffing  per-region S2 density (section keyword count vs module bytes)
          and kw share of the cosine dot product, reported per region.

Run (repo root): .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_301_full_normals_build.py
Outputs: B2_301_sections/<region>__<seat>[.rerun].md
         B2_301_normals/<seat>[.rerun].md (complete build docs)
         B2_301_results.json, B2_301_curvature_scan.json
"""
import hashlib
import json
import math
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
GM = os.path.join(REPO, "memory", "game_modules")
TRI_ORIGINAL = os.path.join(REPO, "memory", "runs", "combined_game_triangulation")
SECDIR = os.path.join(HERE, "B2_301_sections")
NORMALDIR = os.path.join(HERE, "B2_301_normals")
RESULTS = os.path.join(HERE, "B2_301_results.json")
SCAN = os.path.join(HERE, "B2_301_curvature_scan.json")
BAR = 0.5

# descent order for doc assembly (assembly order does not touch the meter:
# assignment is first-match by keyword set, never positional)
DESCENT = ["water_computer", "fractal_maze", "riddler_optics",
           "riddler_engram", "audit_dungeon", "adventure_2d6"]
MODULE_FILE = {
    "water_computer": "water_computer.v1.json",
    "fractal_maze": "fractal_maze.v1.json",
    "riddler_optics": "riddler_optics.v1.json",
    "riddler_engram": "riddler_engram.v1.json",
    "audit_dungeon": "audit_dungeon.v1.json",
    "adventure_2d6": "adventure_2d6_stub.v1.json",
}
# shipped keyword table, quoted from tools/curvature_scan.py build_sections
# (import below is the source of truth; this dict only names the keys)
REGIONS = list(DESCENT)

DOCTRINE = (
    "Agreed cross-region doctrine you may rely on: the river ford loops "
    "north into the water computer's gallery (loop-closes, RIB "
    "RIB_CATHEDRAL_WORLD_V1 AGREE); the audit dungeon's git vault opens onto "
    "the crossroads; the audit doctrine library's ten lenses gate the optics "
    "garage at 10 of 10 collected (lens-count-gate AGREE); the fractal maze "
    "leaf gate entry needs the water computer's OUT height as its "
    "temperature (water-feeds-field AGREE).")


def load_env():
    env = {}
    with open(os.path.join(REPO, ".env"), encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*(.*)$", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


ENV = load_env()
SEATS = {
    "seatA": {"lane": "groq", "base": "https://api.groq.com/openai/v1",
              "keys": [ENV.get("GROQ_API_KEY", ""), ENV.get("GROQ_API_KEY_2", "")],
              "model": "openai/gpt-oss-120b",
              "extra": {"reasoning_effort": "low"}},
    "seatB": {"lane": "together", "base": "https://api.together.xyz/v1",
              "keys": [ENV.get("TOGETHER_API_KEY", "")],
              "model": "deepseek-ai/DeepSeek-V4-Flash-0731",
              "extra": None},
}

TRUNCATION_STATS = {"discarded_truncated": 0, "refires": 0,
                    "retries_non200": 0}


def _one_call(seat, prompt, max_tokens):
    cfg = SEATS[seat]
    key = next((k for k in cfg["keys"] if k), "")
    if not key:
        return {"status": 0, "error": "no key on file for " + cfg["lane"]}
    payload = {"model": cfg["model"],
               "messages": [{"role": "user", "content": prompt}],
               "max_tokens": max_tokens, "temperature": 0}
    if cfg["extra"]:
        payload.update(cfg["extra"])
    req = urllib.request.Request(
        cfg["base"] + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json",
                 "User-Agent": "MagB2301/1.0"},
        method="POST")
    t0 = time.time()
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            status = resp.status
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        status = e.code
    except Exception as e:
        return {"status": 0, "error": type(e).__name__ + ": " + str(e)[:200]}
    try:
        j = json.loads(body)
        choice = j["choices"][0]
        content = choice["message"].get("content") or ""
        usage = j.get("usage") or {}
        finish_reason = choice.get("finish_reason") or ""
    except Exception:
        content, usage, finish_reason = "", {}, ""
    return {"status": status, "latency_s": round(time.time() - t0, 2),
            "content": content, "usage": usage, "finish_reason": finish_reason,
            "err_body": body[:200] if status != 200 else ""}


def chat(seat, prompt, max_tokens=4000):
    """chat() with the B2-302 truncation guard plus transient-status retry.

    CAUSE (retry arm): a 429 or 5xx on one region call would leave the full
    normal with a DARK region and sink the whole-normals scan for a transport
    reason, not a content reason. FIX: up to 3 attempts on non-200 with 10/30
    second backoff, counted in TRUNCATION_STATS.retries_non200 and disclosed
    in the receipt. The B2-302 truncation arm is unchanged: finish_reason
    length refires ONCE at 3x budget capped 16000, truncated call discarded
    and counted; a second truncation returns truncated_final: true.
    """
    raised = min(max_tokens * 3, 16000)
    r = _one_call(seat, prompt, max_tokens)
    attempt = 0
    while r.get("status") != 200 and attempt < 2:
        attempt += 1
        TRUNCATION_STATS["retries_non200"] += 1
        time.sleep(10 * attempt)
        r = _one_call(seat, prompt, max_tokens)
    if r.get("status") == 200 and r.get("finish_reason") == "length":
        TRUNCATION_STATS["discarded_truncated"] += 1
        r2 = _one_call(seat, prompt, raised)
        if r2.get("status") == 200:
            TRUNCATION_STATS["refires"] += 1
            r2["refired"] = True
            r2["discarded_truncated_calls"] = 1
            r2["original_max_tokens"] = max_tokens
            r2["refire_max_tokens"] = raised
            if r2.get("finish_reason") == "length":
                r2["truncated_final"] = True
            return r2
        r2["discarded_truncated_calls"] = 1
        return r2
    return r


# ---- prompts: framing + module bytes + doctrine + V2 glossary wording ----
with open(os.path.join(GM, MODULE_FILE["adventure_2d6"]), encoding="utf-8") as f:
    ADV_JSON = f.read()

# B2-71 winning V2 instruction, verbatim
ADV_V2 = ("Use the module's exact identifiers whenever you name anything: the "
          "rooms crossroads, hill_shrine, market_ruin, river_ford; the Hungry "
          "Dog encounter; the Wanderer; the 2d6 resolution with pass threshold "
          "7. Never paraphrase these proper nouns.")


def region_v2_instruction(region):
    if region == "adventure_2d6":
        return ADV_V2
    with open(os.path.join(GM, MODULE_FILE[region]), encoding="utf-8") as f:
        m = json.loads(f.read())
    ids = [str(m.get("module_id", region))]
    ids += list(m.get("rooms", {}).keys())
    named = ", ".join(ids[:14])
    return ("Use the module's exact identifiers whenever you name anything: "
            + named + ". Never paraphrase these proper nouns.")


def region_prompt(region):
    with open(os.path.join(GM, MODULE_FILE[region]), encoding="utf-8") as f:
        module_json = f.read()
    return (
        "You are one of two independent builders writing a combined "
        "game-world spec. The world merges six region modules into one "
        "persistent world (schema mag_game_module.v1; exits and hooks are the "
        "only glue; no new engine). Your section covers ONLY the region "
        "defined by this module JSON:\n\n" + module_json + "\n\n"
        + DOCTRINE + "\n\n"
        "Write 6 to 10 blank-line-separated markdown paragraphs describing "
        "this region for the build document. "
        + region_v2_instruction(region) + "\n\n"
        "Output the section only: no preamble, no code fences.")


PROMPTS = {r: region_prompt(r) for r in REGIONS}


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def assemble(region_texts, seat, suffix):
    """Complete build doc: one title line, then the six region sections."""
    title = ("Combined-world build normal (%s, V2 glossary-locked, B2-301%s)"
             % (seat, ", rerun" if suffix else ""))
    parts = [title]
    for r in DESCENT:
        t = region_texts.get(r)
        if t:
            parts.append(t.strip())
    return "\n\n".join(parts) + "\n"


def main():
    t_start = time.time()
    os.makedirs(SECDIR, exist_ok=True)
    os.makedirs(NORMALDIR, exist_ok=True)
    os.chdir(REPO)  # shipped curvature_scan resolves ROOT from cwd
    sys.path.insert(0, REPO)
    from pathlib import Path
    import tools.curvature_scan as cs

    results = {"schema": "b301.full.normals.build.v1", "bar": BAR,
               "meter_law": "tools/curvature_scan.py build_sections + curvature, "
                            "imported and called, never reimplemented; "
                            "assignment single-label first-match, declared order "
                            "adventure_2d6, water_computer, fractal_maze, "
                            "riddler_optics, riddler_engram, audit_dungeon "
                            "(B2-230 spec)",
               "seats": {s: {"lane": SEATS[s]["lane"], "model": SEATS[s]["model"]}
                         for s in SEATS},
               "calls": [], "gates": {}, "scans": {},
               "truncation_stats": TRUNCATION_STATS}

    mods = cs.load_modules()

    # ---- GATE 1: shipped meter reproduces 0.483 on the archived normals ----
    cs.TRI = Path(TRI_ORIGINAL)
    gate_scan = cs.curvature(mods)
    adv_archived = gate_scan.get("adventure_2d6", {})
    results["gates"]["archived_adventure"] = adv_archived
    results["gates"]["archived_scan_all_regions"] = gate_scan
    gate_ok = (adv_archived.get("class") == "SADDLE"
               and adv_archived.get("cos") == 0.483)
    results["gates"]["baseline_gate_0_483"] = gate_ok
    print("GATE archived normals adventure=%s cos=%s (want SADDLE 0.483) "
          "gate=%s" % (adv_archived.get("class"), adv_archived.get("cos"),
                       gate_ok))
    if not gate_ok:
        print("GATE FAILED - no new number counts; filing results as owed")
        results["wall_clock_s"] = round(time.time() - t_start, 1)
        with open(RESULTS, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        return

    # ---- fire the builders: 6 regions x 2 seats, primary then rerun ----
    def run_batch(suffix):
        region_texts = {}
        for region in REGIONS:
            for seat in SEATS:
                path = os.path.join(SECDIR, "%s__%s%s.md" % (region, seat, suffix))
                if os.path.exists(path):
                    with open(path, encoding="utf-8", errors="replace") as f:
                        region_texts.setdefault(region, {})[seat] = f.read()
                    print("skip existing", os.path.basename(path))
                    continue
                r = chat(seat, PROMPTS[region])
                entry = {"region": region, "seat": seat, "run":
                         "rerun" if suffix else "primary",
                         "lane": SEATS[seat]["lane"],
                         "model": SEATS[seat]["model"],
                         "status": r["status"],
                         "latency_s": r.get("latency_s"),
                         "usage": r.get("usage", {}),
                         "finish_reason": r.get("finish_reason"),
                         "path": os.path.relpath(path, REPO)}
                if r["status"] == 200 and r.get("content", "").strip():
                    with open(path, "w", encoding="utf-8", newline="\n") as f:
                        f.write(r["content"])
                    region_texts.setdefault(region, {})[seat] = r["content"]
                    entry["sha256_16"] = sha16(r["content"].encode("utf-8"))
                    print("OK %s %s%s %s tok=%s" % (
                        region, seat, suffix, entry["sha256_16"],
                        (r.get("usage") or {}).get("total_tokens")))
                else:
                    entry["error"] = (r.get("error")
                                      or r.get("err_body", "")[:160])
                    print("FAIL", region, seat, suffix, entry["error"])
                results["calls"].append(entry)
                time.sleep(2)
        normals = {}
        for seat in SEATS:
            texts = {rg: region_texts.get(rg, {}).get(seat)
                     for rg in REGIONS}
            if all(texts.values()):
                doc = assemble(texts, seat, suffix)
                npath = os.path.join(
                    NORMALDIR, "%s%s.md" % (seat, suffix))
                with open(npath, "w", encoding="utf-8", newline="\n") as f:
                    f.write(doc)
                normals[seat] = npath
                print("wrote normal", os.path.basename(npath),
                      "paras=%d" % len(re.split(r"\n\s*\n", doc)))
        return normals

    t_build0 = time.time()
    normals_primary = run_batch("")
    normals_rerun = run_batch(".rerun")
    results["build_wall_clock_s"] = round(time.time() - t_build0, 1)

    # ---- scan the new normals with the SHIPPED curvature() ----
    scan_out = {}
    for label, normals in (("primary", normals_primary),
                           ("rerun", normals_rerun)):
        if len(normals) != 2:
            scan_out[label] = {"error": "incomplete normal pair, scan skipped"}
            continue
        # shipped code path: curvature() reads build_sections over TRI files
        # named version_grok.md / version_deepseek.md; stage the pair under a
        # temp TRI with those names, restore the archived TRI after.
        stage = os.path.join(HERE, "B2_301_tri_stage")
        os.makedirs(stage, exist_ok=True)
        with open(os.path.join(stage, "version_grok.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(open(normals["seatA"], encoding="utf-8",
                         errors="replace").read())
        with open(os.path.join(stage, "version_deepseek.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(open(normals["seatB"], encoding="utf-8",
                         errors="replace").read())
        cs.TRI = Path(stage)
        scan_out[label] = cs.curvature(mods)
        cs.TRI = Path(TRI_ORIGINAL)
    results["scans"] = scan_out
    for label, sc in scan_out.items():
        if isinstance(sc, dict) and "adventure_2d6" in sc:
            a = sc["adventure_2d6"]
            print("SCAN %s adventure=%s cos=%s" % (
                label, a.get("class"), a.get("cos")))
            for rg, c in sc.items():
                print("  %-16s %-7s %s" % (rg, c.get("class"), c.get("why")))

    # ---- no-stuffing axes per region (S2 density + kw share of dot) ----
    KEYS_SHIPPED = {
        "adventure_2d6": ["2d6", "ford", "river", "adventure"],
        "water_computer": ["water", "cistern", "valve", "tank", "hydraulic"],
        "fractal_maze": ["fractal", "maze", "recursion", "refract"],
        "riddler_optics": ["optics", "lens", "garage", "light"],
        "riddler_engram": ["engram", "summon", "card", "memory"],
        "audit_dungeon": ["audit", "doctrine", "library"],
    }

    def stuffing(doc_a, doc_b):
        out = {}
        ga = cs.build_sections(Path(doc_a))
        gb = cs.build_sections(Path(doc_b))
        for rg, kws in KEYS_SHIPPED.items():
            a, b = ga.get(rg), gb.get(rg)
            if not a or not b:
                continue
            common = set(a) & set(b)
            kw_mass = sum(a[t] * b[t] for t in common if t in kws)
            all_mass = sum(a[t] * b[t] for t in common)
            with open(os.path.join(GM, MODULE_FILE[rg]), encoding="utf-8") as f:
                low_m = f.read().lower()
            dens = {}
            for seat, cnt in (("seatA", a), ("seatB", b)):
                per = {}
                for k in kws:
                    # token-level: shipped meter counters hold [a-z0-9_]{3,}
                    # tokens, so a keyword inside a longer token counts once
                    # per token, not per raw substring occurrence
                    tok_hits = sum(v for t, v in cnt.items() if k in t)
                    cm = len(re.findall(re.escape(k), low_m))
                    per[k] = {"section_tokens": tok_hits,
                              "ratio": round(tok_hits / cm, 2) if cm else None}
                dens[seat] = per
            out[rg] = {"kw_share_of_dot": round(kw_mass / all_mass, 3)
                       if all_mass else None,
                       "density_token_level_max_ratio": max(
                           (c["ratio"] for s in dens.values()
                            for c in s.values() if c["ratio"] is not None),
                           default=None),
                       "density_token_level": dens}
        return out

    for label, normals in (("primary", normals_primary),
                           ("rerun", normals_rerun)):
        if len(normals) == 2:
            results.setdefault("no_stuffing", {})[label] = stuffing(
                normals["seatA"], normals["seatB"])

    # ---- verdict ----
    def verdict_of(scan):
        a = scan.get("adventure_2d6", {}) if isinstance(scan, dict) else {}
        return a.get("class"), a.get("cos")

    v_primary = verdict_of(scan_out.get("primary", {}))
    v_rerun = verdict_of(scan_out.get("rerun", {}))
    results["verdict"] = {
        "primary_adventure": {"class": v_primary[0], "cos": v_primary[1]},
        "rerun_adventure": {"class": v_rerun[0], "cos": v_rerun[1]},
        "claim_reproduces": (v_primary[0] == "HILL" and v_rerun[0] == "HILL"),
    }
    results["truncation_stats"] = TRUNCATION_STATS
    results["wall_clock_s"] = round(time.time() - t_start, 1)
    tok = sum((c.get("usage") or {}).get("total_tokens") or 0
              for c in results["calls"])
    results["token_totals"] = {"total_tokens_all_calls": tok,
                               "calls": len(results["calls"])}

    # ---- scan artifact ----
    scan_doc = {
        "schema": "b301.curvature.scan.v1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "what": "full-normals curvature scan over the B2-301 complete build "
                "docs, computed by the shipped tools/curvature_scan.py "
                "curvature() (imported, called, unmodified)",
        "assignment_order_law": "single-label first-match, declared order "
                                "adventure_2d6, water_computer, fractal_maze, "
                                "riddler_optics, riddler_engram, audit_dungeon "
                                "(B2-230 spec; receipts quoting region cosines "
                                "name this order version)",
        "normals": {k: os.path.relpath(v, REPO)
                    for k, v in normals_primary.items()},
        "normals_rerun": {k: os.path.relpath(v, REPO)
                          for k, v in normals_rerun.items()},
        "archived_gate": {"tri": os.path.relpath(TRI_ORIGINAL, REPO),
                          "adventure_2d6": adv_archived},
        "regions_primary": scan_out.get("primary"),
        "regions_rerun": scan_out.get("rerun"),
        "verdict": results["verdict"],
    }
    with open(SCAN, "w", encoding="utf-8") as f:
        json.dump(scan_doc, f, indent=2)
    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("wrote", os.path.basename(RESULTS), "and", os.path.basename(SCAN))
    print("VERDICT primary=%s rerun=%s reproduces=%s wall=%.1fs tok=%d" % (
        v_primary[0], v_rerun[0], results["verdict"]["claim_reproduces"],
        results["wall_clock_s"], tok))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
