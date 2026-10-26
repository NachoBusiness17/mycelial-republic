"""B2-71 hill build: builder-prompt experiments to raise adventure_2d6
builder agreement across the 0.5 HILL bar, honestly.

Baseline (settled by B2-17): cos(grok_normal, deepseek_normal) = 0.483 on the
adventure_2d6 section, bar 0.5, gap +0.017 (CATHEDRAL_CURVATURE_SCAN_20260921).
B2-72 proved measurement-side keyword/order variants cannot produce the raise.
So the raise must come from BUILD CONTENT: fresh sections written by two live
builder seats under varied prompt wording, measured by the shipped meter law.

Design:
  seats   seatA = groq openai/gpt-oss-120b (stands in for the grok seat; xai
                 is paid-dormant; substitution is declared, not hidden)
          seatB = together deepseek-ai/DeepSeek-V4-Flash-0731 (the same
                 deepseek-v4-flash family that built the original deepseek
                 normal)
  prompt  same prompt to both seats per variant; variants differ ONLY in
          section-wording instructions (V0 control / V1 facts-first /
          V2 glossary-locked). Grounding = adventure_2d6_stub.v1.json bytes
          (fictional game module only; no keys, no PII, no private diaries).
  meter   shipped law, unchanged: blank-line paragraphs, first-match keyword
          assignment (adventure_2d6 first), [a-z0-9_]{3,} counters, cosine =
          common-dot / full-norms, round 3. GATE: recomputing the ORIGINAL
          normals must reproduce 0.483 bit-for-bit before any v2 number counts.
  no-stuffing gates
          S2 density: per adventure keyword, section count vs module count.
          S3 decomposition: share of the cosine dot product carried by the
          four adventure keywords vs all other shared content tokens. A rise
          carried by keywords is stuffing-shaped and does not count as the
          honest raise; a rise carried by room nouns / invariant terms is
          content-shaped.
  falsifier  the winning variant is re-fired fresh at both seats; the claim
          "this prompt wording raises agreement above the bar" reproduces only
          if the rerun pair also crosses 0.5 under the same meter.

Run: .venv/Scripts/python.exe B2_71_hill_build.py [--rerun-only]
Outputs: B2_71_results.json, B2_71_sections/<variant>__<seat>[.rerun].md
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
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TRI = os.path.join(REPO, "memory", "runs", "combined_game_triangulation")
MODULE = os.path.join(REPO, "memory", "game_modules", "adventure_2d6_stub.v1.json")
SECDIR = os.path.join(HERE, "B2_71_sections")
RESULTS = os.path.join(HERE, "B2_71_results.json")
BAR = 0.5

# ---- shipped meter law (tools/curvature_scan.py build_sections), verbatim ----
KEYS = {
    "adventure_2d6": ["2d6", "ford", "river", "adventure"],
    "water_computer": ["water", "cistern", "valve", "tank", "hydraulic"],
    "fractal_maze": ["fractal", "maze", "recursion", "refract"],
    "riddler_optics": ["optics", "lens", "garage", "light"],
    "riddler_engram": ["engram", "summon", "card", "memory"],
    "audit_dungeon": ["audit", "doctrine", "library"],
}
ADV_KWS = KEYS["adventure_2d6"]
# keyword-coverage axis: module-grounded room ids (from the module's own
# rooms block) added to the adventure key set; reported separately, never
# silently substituted for the shipped meter.
COVERAGE_EXTRA = ["crossroads", "hill_shrine", "market_ruin", "wanderer"]


def build_sections(txt, keys=None):
    keys = keys or KEYS
    blocks = {r: [] for r in keys}
    total_paras = 0
    for para in re.split(r"\n\s*\n", txt):
        if not para.strip():
            continue
        total_paras += 1
        low = para.lower()
        for r, kws in keys.items():
            if any(k in low for k in kws):
                blocks[r].append(low)
                break
    counters = {r: Counter(re.findall(r"[a-z0-9_]{3,}", " ".join(v)))
                for r, v in blocks.items() if v}
    return counters, total_paras


def cosine(g, d):
    common = set(g) & set(d)
    num = sum(g[t] * d[t] for t in common)
    den = math.sqrt(sum(v * v for v in g.values())) * \
        math.sqrt(sum(v * v for v in d.values()))
    return (num / den) if den else 0.0


def adv_cos(gtxt, dtxt, keys=None, detail=False):
    gc, _ = build_sections(gtxt, keys)
    dc, _ = build_sections(dtxt, keys)
    g, d = gc.get("adventure_2d6"), dc.get("adventure_2d6")
    if not g or not d:
        return (None, {}) if detail else None
    common = set(g) & set(d)
    kw_mass = sum(g[t] * d[t] for t in common if t in ADV_KWS)
    all_mass = sum(g[t] * d[t] for t in common)
    info = {"grok_terms": len(g), "deep_terms": len(d),
            "common": len(common)}
    info["kw_share_of_dot"] = round(kw_mass / all_mass, 3) if all_mass else None
    info["kw_dot"] = kw_mass
    info["all_dot"] = all_mass
    info["top_shared"] = [(t, g[t], d[t]) for t in
                          sorted(common, key=lambda t: -(g[t] * d[t]))[:12]]
    c = cosine(g, d)
    return (c, info) if detail else c


# ---- builder lanes (both verified ALIVE 2026-09-26 by B2-04) ----
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


# B2-302 truncation-guard counter (2026-09-26): every discarded truncated call
# lands here so a build receipt can dump TRUNCATION_STATS and total honestly.
TRUNCATION_STATS = {"discarded_truncated": 0, "refires": 0}


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
                 "User-Agent": "MagB271/1.0"},
        method="POST")
    t0 = time.time()
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
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
    """chat() with the B2-302 truncation guard (2026-09-26).

    CAUSE: together DeepSeek-V4-Flash reasoning burned a 2500 max_tokens budget
    into a 91-byte mid-sentence section (B2-71 first V0 pair, discarded and
    disclosed in B2_71_hill_build_20260926.md Falsifier; sibling evidence
    B2-231 version_deepseek.md erratum) -- the old helper dropped
    finish_reason, so a length-truncated call looked like a normal answer.
    FIX: detect finish_reason == "length" and refire ONCE at a raised budget
    (x3, capped at 16000); the truncated call is discarded and counted in
    TRUNCATION_STATS (discarded_truncated / refires) for the receipt totals.
    A second truncation is returned as-is with truncated_final: true -- the
    caller sees the honesty flag instead of a silent short section.
    """
    raised = min(max_tokens * 3, 16000)
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


# ---- prompts: shared framing, variants differ only in wording instructions ----
with open(MODULE, encoding="utf-8") as f:
    MODULE_JSON = f.read()

SHARED = (
    "You are one of two independent builders writing a combined game-world "
    "spec. The world merges seven existing module files into one persistent "
    "world (schema mag_game_module.v1; exits and hooks are the only glue; no "
    "new engine). Your section covers ONLY the region defined by this module "
    "JSON:\n\n" + MODULE_JSON + "\n\n"
    "Agreed cross-region doctrine you may rely on: the river ford loops north "
    "into the water computer's gallery (loop-closes); the audit dungeon's "
    "git vault opens onto the crossroads. Write 6 to 10 blank-line-separated "
    "markdown paragraphs describing this region for the build document. "
    "Output the section only: no preamble, no code fences.\n\n")
VARIANTS = {
    "V0_control": SHARED,
    "V1_facts_first": SHARED +
        "Structure the section in exactly this order: first the resolution "
        "rules (which dice, what counts as a pass); then a room-by-room walk "
        "naming each room and the exits from it; then the cross-region loop "
        "invariant; then at most one line of flavor.\n\n",
    "V2_glossary": SHARED +
        "Use the module's exact identifiers whenever you name anything: the "
        "rooms crossroads, hill_shrine, market_ruin, river_ford; the Hungry "
        "Dog encounter; the Wanderer; the 2d6 resolution with pass threshold "
        "7. Never paraphrase these proper nouns.\n\n",
}


def density(txt):
    """S2: keyword counts in section vs in the module bytes."""
    low_m = MODULE_JSON.lower()
    out = {}
    for k in ADV_KWS:
        cm = len(re.findall(re.escape(k), low_m))
        cs = len(re.findall(re.escape(k), txt.lower()))
        out[k] = {"section": cs, "module": cm,
                  "ratio": round(cs / cm, 2) if cm else None}
    return out


def grounding(txt):
    """S1 (reported, not gated): pct of len>=3 tokens found in module bytes."""
    toks = re.findall(r"[a-z0-9_]{3,}", txt.lower())
    mod = set(re.findall(r"[a-z0-9_]{3,}", MODULE_JSON.lower()))
    hit = sum(1 for t in toks if t in mod)
    return round(hit / len(toks), 3) if toks else 0.0


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def main():
    rerun_only = "--rerun-only" in sys.argv
    os.makedirs(SECDIR, exist_ok=True)
    results = {"schema": "b271.hill.build.v1", "bar": BAR, "runs": [],
               "reruns": [], "gates": {}}

    # ---- GATE: shipped meter reproduces the filed 0.483 on the originals ----
    with open(os.path.join(TRI, "version_grok.md"), encoding="utf-8",
              errors="replace") as f:
        grok_orig = f.read()
    with open(os.path.join(TRI, "version_deepseek.md"), encoding="utf-8",
              errors="replace") as f:
        deep_orig = f.read()
    base = adv_cos(grok_orig, deep_orig)
    results["gates"]["baseline_originals_cos"] = round(base, 6) if base else None
    results["gates"]["baseline_gate"] = (base is not None
                                         and round(base, 3) == 0.483)
    coverage_on_originals = adv_cos(
        grok_orig, deep_orig,
        {**KEYS, "adventure_2d6": ADV_KWS + COVERAGE_EXTRA})
    results["gates"]["coverage_variant_on_originals"] = round(
        coverage_on_originals, 3)
    print("GATE originals adventure cos=%.6f (want 0.483) gate=%s | "
          "coverage-variant on originals=%.3f"
          % (base, results["gates"]["baseline_gate"],
             coverage_on_originals))
    if not results["gates"]["baseline_gate"]:
        print("GATE FAILED - no v2 number counts; file as owed")
        with open(RESULTS, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        return

    jobs = [(v, s) for v in VARIANTS for s in SEATS]
    if rerun_only:
        jobs = [(v, s) for v in sys.argv[2].split(",") for s in SEATS]

    # ---- fire the builders (sequential; width law) ----
    for variant, seat in jobs:
        suffix = ".rerun" if rerun_only else ""
        path = os.path.join(SECDIR, "%s__%s%s.md" % (variant, seat, suffix))
        if os.path.exists(path):
            print("skip existing", os.path.basename(path))
            continue
        r = chat(seat, VARIANTS[variant])
        entry = {"variant": variant, "seat": seat, "lane": SEATS[seat]["lane"],
                 "model": SEATS[seat]["model"], "status": r["status"],
                 "latency_s": r.get("latency_s"), "usage": r.get("usage", {}),
                 "path": os.path.relpath(path, REPO)}
        if r["status"] == 200 and r.get("content", "").strip():
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(r["content"])
            entry["sha256_16"] = sha16(r["content"].encode("utf-8"))
            print("OK %s %s %s tok=%s" % (
                variant, seat, entry["sha256_16"],
                (r.get("usage") or {}).get("total_tokens")))
        else:
            entry["error"] = r.get("error") or r.get("err_body", "")[:160]
            print("FAIL", variant, seat, entry["error"])
        results.setdefault("calls", []).append(entry)
        time.sleep(2)

    # ---- meter over whatever sections exist ----
    def pair_for(variant, suffix):
        out = {}
        for seat in SEATS:
            p = os.path.join(SECDIR, "%s__%s%s.md" % (variant, seat, suffix))
            out[seat] = open(p, encoding="utf-8", errors="replace").read() \
                if os.path.exists(p) else None
        return out

    def bucket_key(suffix):
        return "reruns" if suffix else "runs"

    def measure(variant, suffix, bucket):
        txts = pair_for(variant, suffix)
        a, b = txts.get("seatA"), txts.get("seatB")
        if not a or not b:
            return
        cos, info = adv_cos(a, b, detail=True)
        cos_cov = adv_cos(a, b, {**KEYS, "adventure_2d6": ADV_KWS + COVERAGE_EXTRA})
        if not info:
            print("%-14s %s DARK: a seat's adventure section is empty under "
                  "the shipped meter" % (variant, "rerun" if suffix else "primary"))
            results[bucket_key(suffix)].append({
                "variant": variant, "run": "rerun" if suffix else "primary",
                "cos": None, "class": None, "cos_coverage_variant": None,
                "sha_seatA": sha16(a.encode("utf-8")),
                "sha_seatB": sha16(b.encode("utf-8"))})
            return
        row = {
            "variant": variant, "run": "rerun" if suffix else "primary",
            "cos": round(cos, 3) if cos is not None else None,
            "class": ("HILL" if cos >= BAR else "SADDLE") if cos is not None else None,
            "cos_coverage_variant": round(cos_cov, 3) if cos_cov is not None else None,
            "kw_share_of_dot": info["kw_share_of_dot"],
            "kw_dot": info["kw_dot"], "all_dot": info["all_dot"],
            "terms_grok": info["grok_terms"], "terms_deep": info["deep_terms"],
            "common_terms": info["common"],
            "top_shared_terms": info["top_shared"][:8],
            "density_seatA": density(a), "density_seatB": density(b),
            "grounding_seatA": grounding(a), "grounding_seatB": grounding(b),
            "paras_seatA": len(re.split(r"\n\s*\n", a)),
            "paras_seatB": len(re.split(r"\n\s*\n", b)),
            "sha_seatA": sha16(a.encode("utf-8")), "sha_seatB": sha16(b.encode("utf-8")),
        }
        bucket.append(row)
        print("%-14s %s cos=%s class=%s cov=%s kw_share=%s" % (
            variant, row["run"], row["cos"], row["class"],
            row["cos_coverage_variant"], row["kw_share_of_dot"]))

    for v in VARIANTS:
        measure(v, "", results["runs"])
    for v in VARIANTS:
        measure(v, ".rerun", results["reruns"])

    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("wrote", os.path.basename(RESULTS))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
