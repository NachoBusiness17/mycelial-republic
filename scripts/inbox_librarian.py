"""inbox_librarian -- the 'magic librarians' catalog for watch/inbox (non-destructive).

Pattern: JevAgentHarness-style cheap decider (tier 1 = path/prefix rules) that escalates
to a small LOCAL model (tier 2 = Ollama, no paid calls) only when the rules cannot place a
file; Terminal-RSI-style "keep only verified work" via the verified field on cards.

Writes ONLY under watch/LIBRARY/. Never moves, renames or deletes inbox files. Never reads
contents of sensitive files (.env, steps.jsonl, key/secret/token-named files, anything under
secret_gate_results/ or free_keys*/) -- those are classified by path only.

RUN (incremental / resume, default):  python scripts\\inbox_librarian.py --model-budget-min 30
     Resume is automatic: model answers are cached in watch/LIBRARY/model_cache.jsonl (per file
     path|size|mtime and per folder), cards are re-used from catalog.jsonl, so a run that was cut off or
     ran out of budget simply continues with the files still marked tier "pending".
     full rebuild:            python scripts\\inbox_librarian.py --full --model-budget-min 110
     rules only (no model):   python scripts\\inbox_librarian.py --no-model
     options: --model qwen2.5:7b  --ollama http://localhost:11434  --model-budget-min 20
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, sys, time, urllib.request
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "watch" / "inbox"
LIB = ROOT / "watch" / "LIBRARY"
CATALOG = LIB / "catalog.jsonl"
STATE = LIB / ".librarian_state.json"
MCACHE = LIB / "model_cache.jsonl"
RUNLOG = LIB / "librarian_run.log"

SHELVES = {  # letter: (NAME, ascii, description)
    "α": ("CHAIN", "alpha", "memory chain: chain restore, v2 bintree, verkle/merkle knots, biography, seals, rib vaults"),
    "β": ("GSTD", "beta", "GSTD/TON settlement: contracts, bridge, soak, A2A, gstdcoin mapping, money/revenue pages"),
    "γ": ("LANES", "gamma", "model/provider lanes: free tiers, Hermes burn, burn waves, OpenRouter/DeepSeek/GLM/Gemini/Grok, quotas, width, gopher"),
    "δ": ("BOB", "delta", "bob + Antigravity primary-seat handoff and the work it spawned (asks, task bank, oracle hunt, ractor resolutions)"),
    "ε": ("DOCTRINE", "epsilon", "doctrine, laws, canon, constitution, Lilith, X intel/link drops, parables, essays, posts, research reading"),
    "ζ": ("OPS", "zeta", "operations: patrols, receipts, triage, audits, census, backups, secret gate, mates protocol, tool state (.mimosa), logs"),
    "ω": ("ARCHIVE", "omega", "cold: effective date >30 days, media exports, dormant campaign folders (nothing in 14 days), frontier_olm day folders"),
    "χ": ("UNSORTED", "chi", "rules and model could not place it confidently (needs_review)"),
}
ASCII2G = {v[1]: k for k, v in SHELVES.items()}

# ---------------- tier 1 rules (derived from the 2026-10-17 inventory CSV) ----------------
PREFIX_RULES = [  # (shelf, regex on UPPERCASE filename)
    ("α", r"^(CHAIN|V2|VERKLE|MERKLE|KNOT|ZKNOT|BIOGRAPHY|BINTREE|SEAL|ALPHA)[_\-.]|CHAIN_RESTORE|BINTREE|VERKLE"),
    ("β", r"GSTD|^(TON|A2A|SETTLEMENT|BRIDGE|WORMHOLE|MONEY|BETA)[_\-.]|(^|_)TON[_\-.]"),
    ("γ", r"GOPHER|FREE_TIER|^(BURN|HERMES|H247|FREE|FREELANE|LANE\d*|AGY|GEMINI|PROVIDER|QUOTA|DEEPSEEK|GLM|OPENROUTER|WIDTH|TWO_K|SCRUM|STEALTH|LITE|ZCODE|GROK\d*|KV50|FLASHX|THE50|GAMMA|LANES)[_\-.]"),
    ("δ", r"^(BOB|ANTIGRAVITY|RIB_BOB|SUCCESSION|ORACLE|TASKBANK|DELTA)[_\-.]|ORACLE_HUNT|ANTIGRAVITY_ASKS"),
    ("ε", r"LILITH|CONSTITUTION|DOCTRINE|CANON|^(LINK|LINKS|LINK_DROPS|PREDATOR|PARABLE|RIDDLE|RIDDLER|QUEEN|X|TWEET|SHITPOST|LAW\d*|EPSILON)[_\-.]"),
    ("ζ", r"^(DRIFT_PATROL|MORNING_TRIAGE|RECEIPT|AUDIT|SECRET|CENSUS|FOSSIL|JANITOR|HYGIENE|VENV|BACKUP|OFFSITE|DISK|BOOT|INDEX|LAWPACK|DATED_METERS|ORPHAN|PROMISE|WEEKLY_DIGEST|SPOTCHECK|PURGE|MIGRATION|SECURITY|ROOM_STATE|SEAT_DECAY|R2_VENV|QCAPTION|TASK_WALL|FORGOTTEN|SELF_ARCHAEOLOGY|MEM_ECHO|PACK_OFFLOAD|ESSENTIALS|ZETA|OPS)[_\-.]|_(ARCHAEOLOGIST|CARTOGRAPHER|GAMBITER|INNKEEPER|JESTER|LAMPLIGHTER|LOCKSMITH|MARINER)\."),
]
FOLDER_RULES = [  # (shelf, regex on top-level folder name)
    ("ω", r"^(mrpool_export|qdrop_export|bearableguy_export|frontier_olm_\d{4}-?\d{2}-?\d{2}|music|media)$"),
    ("ζ", r"^(secret_gate_results|mates_leave_protocol|disk_audit_\d+|audit_\d+|\.mimosa|endpoint_news|probes|spore_audit_\d+|reboot_patches_\d+|night_cools?_\d+|night_shift_\d+)$"),
    ("α", r"^(ribvault_\d+|seed_rib_\d+|biography_\d+|verkle.*)$"),
    ("β", r"^(gstd.*|GSTD.*|money_rev.*|money_revolution.*)$"),
    ("γ", r"^(hermes_burn|hermes_daily|glm_burn|deepseek_research|replay_.*|free_keys.*|frontier_asks|frontier_olm_adhoc|model_garden|local_fanout|spiking_wide|fifty_wide_\d+|union_fullsend_\d+|fullsend_s2|ds_batches|xai_grok47|burn_wave_\d+|burn_reset_\d+|full_blast_\d+)$"),
    ("δ", r"^(bob_handoff|handoff|task_bank|ractor|harness_intel_\d+)$"),
    ("ε", r"^(link_drops_\d+|canon_drops_\d+|parables|babelfish.*|vaultmother_babelfish_\d+|esoteric_mine_\d+|luther_moment_\d+|falsifier_index_\d+|riddler_.*|retrocausal_riddler_\d+|trickster_protocol_\d+|circle_of_command_\d+|person_mine|ractor_spore_posts_\d+|spore_posts_\d+|.*_drop_\d{8}|nacho_.*|outerweb_.*|standing_channel_theory_\d+|hut_bible_.*|sensory_inputs_\d+|cammarata_thread_\d+)$"),
]
PATH_ONLY_DIRS = re.compile(r"^(secret_gate_results|free_keys[^\\/]*)$", re.I)
SENSITIVE_NAME = re.compile(r"(^\.env|\.env$|\.env\.|^steps\.jsonl$|secret|credential|passw|token|api_?key|(^|[_\-.])keys?([_\-.]|$)|\.pem$|\.key$|\.p12$|\.pfx$|wallet|mnemonic|seed_?phrase|\.enc$|id_rsa|id_ed25519|\.kdbx$)", re.I)
TEXT_EXT = {".md", ".txt", ".json", ".jsonl", ".py", ".html", ".htm", ".csv", ".yaml", ".yml", ".xml", ".ps1", ".sh", ".log", ".toml", ".rss", ".ts", ".js", ".source"}
MODEL_EXT = {".md", ".txt", ".json", ".jsonl", ".py", ".html", ".csv", ".yaml", ".yml", ".ps1", ".sh", ".log", ".toml"}
MASK = [re.compile(p) for p in [
    r"(sk-|sk_|ghp_|gho_|github_pat_|xox[abposr]-|AKIA|ASIA|AIza|eyJ|hf_|gsk_|xai-|glpat-)[A-Za-z0-9_\-\.=]{6,}",
    r"(?i)(api[_-]?key|secret|token|password|passwd|bearer|authorization|private[_-]?key|seed|mnemonic)(\s*[:=]\s*|\s+)\S+",
    r"[A-Za-z0-9+/_\-]{32,}={0,2}",
    r"-----BEGIN [A-Z ]+-----[\s\S]*?(-----END [A-Z ]+-----|$)",
]]
NOW = dt.datetime.now()
DATE_RX = re.compile(r"(?<![0-9A-Fa-f])(20[12]\d)-?(0[1-9]|1[0-2])-?(0[1-9]|[12]\d|3[01])(?:[T_-]?([01]\d|2[0-3])-?([0-5]\d)-?([0-5]\d)?)?Z?(?!\d)")


def mask(s: str) -> str:
    for rx in MASK:
        s = rx.sub("[MASKED]", s)
    return s


def fn_date(name: str):
    best = None
    for m in DATE_RX.finditer(name):
        try:
            t = dt.datetime(int(m[1]), int(m[2]), int(m[3]), int(m[4] or 0), int(m[5] or 0), int(m[6] or 0))
        except ValueError:
            continue
        if t > NOW + dt.timedelta(days=1) or t.year < 2020:
            continue
        best = t if best is None or t > best else best
    return best


def family(n: str) -> str:
    s = re.sub(r"\.[A-Za-z0-9]{1,6}$", "", n)
    s = re.sub(r"\.[A-Za-z0-9]{1,6}$", "", s)
    if re.fullmatch(r"[0-9a-fA-F]{24,}.*", s):
        return "<hash>"
    s = re.sub(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "UUID", s)
    s = re.sub(r"(?<![A-Za-z])[0-9a-f]{6,}(?![A-Za-z])", "", s)
    s = DATE_RX.sub("", s)
    s = re.sub(r"[0-9a-fA-F]{8,}", "", s)
    s = re.sub(r"\d+", "#", s)
    s = re.sub(r"[#_\-.\s]+$", "", s)
    s = re.sub(r"^[#_\-.\s]+", "", s)
    s = re.sub(r"[_\-]{2,}", "_", s)
    return s.upper() if s else "<numeric>"


def is_sensitive(rel: str, name: str) -> bool:
    parts = re.split(r"[\\/]", rel)
    return bool(SENSITIVE_NAME.search(name)) or any(PATH_ONLY_DIRS.match(p) for p in parts[:-1])


def head(p: Path, n: int, maxch: int = 4000) -> str:
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            out = []
            for i, ln in enumerate(f):
                if i >= n:
                    break
                out.append(ln.rstrip("\n")[:300])
        return mask("\n".join(out))[:maxch]
    except OSError:
        return ""


def first_heading(p: Path, ext: str) -> str:
    if ext not in TEXT_EXT:
        return ""
    txt = head(p, 25, 3000)
    for ln in txt.splitlines():
        if ln.startswith("#"):
            return ln.lstrip("# ").strip()[:160]
    for ln in txt.splitlines():
        s = ln.strip()
        if len(s) > 3 and not s.startswith(("{", "[", "<", "---")):
            return s[:160]
    return ""


def log(msg: str):
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with open(RUNLOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------- scan ----------------
def scan():
    files = []
    for dp, dns, fns in os.walk(INBOX):
        for fn in fns:
            p = Path(dp) / fn
            try:
                st = p.stat()
            except OSError:
                continue
            rel = str(p.relative_to(INBOX))
            parts = re.split(r"[\\/]", rel)
            lw = dt.datetime.fromtimestamp(st.st_mtime)
            fd = fn_date(fn)
            eff = max(lw, fd) if fd else lw
            files.append(dict(path=rel, top=parts[0] if len(parts) > 1 else "(root)", name=fn,
                              ext=os.path.splitext(fn)[1].lower(), size=st.st_size, mtime=int(st.st_mtime),
                              fdate=fd, eff=eff, sensitive=is_sensitive(rel, fn), mimosa=".mimosa" in parts[:-1]))
    return files + scan_library_docs()


GENERATED = {"catalog.jsonl", "catalog.jsonl.tmp", "catalog.tmp", ".librarian_state.json", "model_cache.jsonl", "librarian_run.log",
             "run_stdout.txt", "run_stderr.txt", "INDEX.md", "ARCHIVE_PROPOSAL.md", "_verify_sample.py", "verify_sample.json",
             "verify_verdicts.json", "VERIFICATION.md", "verify_evidence.txt"}


def scan_library_docs():
    out = []
    if not LIB.exists():
        return out
    for p in LIB.iterdir():
        if not p.is_file() or p.name in GENERATED:
            continue
        st = p.stat()
        lw = dt.datetime.fromtimestamp(st.st_mtime); fd = fn_date(p.name)
        out.append(dict(path="..\\LIBRARY\\" + p.name, top="(root)", name=p.name, ext=p.suffix.lower(), size=st.st_size,
                        mtime=int(st.st_mtime), fdate=fd, eff=max(lw, fd) if fd else lw,
                        sensitive=is_sensitive(p.name, p.name), mimosa=False))
    return out


def tier1(f, folder_newest):
    age = (NOW - f["eff"]).total_seconds() / 86400
    top, up = f["top"], f["name"].upper()
    if f["top"] != "(root)" and PATH_ONLY_DIRS.match(top):
        return ("ζ" if top.lower().startswith("secret") else "γ"), f"path-only:{top}"
    if age > 30:
        return "ω", "age>30d"
    for g, rx in FOLDER_RULES[:1]:
        if re.match(rx, top):
            return g, f"folder:{top}~archive"
    if f["mimosa"]:
        return "ζ", "path:.mimosa tool state"
    for g, rx in PREFIX_RULES:
        m = re.search(rx, up)
        if m:
            return g, f"name:{m.group(0).strip('_-.')}"
    if top != "(root)":
        for g, rx in FOLDER_RULES[1:]:
            if re.match(rx, top):
                return g, f"folder:{top}"
        if (NOW - folder_newest[top]).days > 14:
            return "ω", "folder-dormant>14d"
        return None, "folder-unmapped"
    if f["ext"] == ".jsonl":
        return "ζ", "root-log:.jsonl"
    return None, "root-unmapped"


# ---------------- tier 2: local model ----------------
PROMPT = """You are a librarian sorting files of an AI-agent research estate onto shelves.
Shelves:
alpha = CHAIN: the memory chain: verkle/merkle/bintree chain, chain restore, v2 chain, knots, biography, seals, rib memory vault.
beta = GSTD: GSTD token and TON blockchain settlement, smart contracts, bridge, A2A protocol, gstdcoin, money/revenue, wallets.
gamma = LANES: AI model/provider lanes: free tiers, OpenRouter, Hermes burn, burn waves, DeepSeek/GLM/Gemini/Grok/Qwen usage, quotas, rate limits, width, model gardens, model benchmarks, fine-tuning.
delta = BOB: handoff to the bob machine and the Antigravity seat, standing wave, handoff ribs, Antigravity asks, task bank.
epsilon = DOCTRINE: ideas and doctrine, laws, canon, constitution, Lilith, X/Twitter intel and link drops, parables, essays, public posts, philosophy, research paper reading notes.
zeta = OPS: operations and maintenance: patrols, receipts, audits, triage, census, backups, disks, venv, secret scans, healthchecks, indexes, logs, fleet status.
chi = UNSORTED: none of the above (games, media, misc) or you cannot tell.
Answer ONLY with JSON: {"shelf": "alpha|beta|gamma|delta|epsilon|zeta|chi", "summary": "<one line, max 20 words>", "confidence": <number 0.0-1.0>}
"""


def ask_model(args, label: str, text: str):
    body = json.dumps({"model": args.model, "stream": False, "format": "json",
                       "options": {"temperature": 0, "num_predict": 90, "num_ctx": 2048},
                       "prompt": PROMPT + "\n" + label + "\n----\n" + text + "\n----\nJSON:"}).encode()
    req = urllib.request.Request(args.ollama.rstrip("/") + "/api/generate", data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.loads(r.read())
    secs = time.time() - t0
    try:
        j = json.loads(out.get("response", "{}"))
    except json.JSONDecodeError:
        j = {}
    sh = str(j.get("shelf", "chi")).lower().strip()
    g = next((ASCII2G[k] for k in ASCII2G if sh.startswith(k)), None)
    if g is None:
        g = next((k for k, v in SHELVES.items() if v[0].lower() in sh), "χ")
    try:
        c = float(j.get("confidence", 0))
    except (TypeError, ValueError):
        c = 0.0
    if c > 1:
        c = c / 100.0
    return g, max(0.0, min(1.0, c)), str(j.get("summary", ""))[:200], secs


# ---------------- outputs ----------------
def rel_link(path: str) -> str:
    p = path.replace("\\", "/").replace(" ", "%20")
    return "../" + p[len("../LIBRARY/"):] if p.startswith("../LIBRARY/") else "../../inbox/" + p


def human(n: int) -> str:
    return f"{n/1e9:.2f} GB" if n >= 1e9 else f"{n/1e6:.1f} MB"


def write_outputs(cards):
    by = defaultdict(list)
    for c in cards:
        by[c["shelf"]].append(c)
    hot = [c for c in cards if c["age_days"] <= 7]
    cold = [c for c in cards if c["age_days"] > 30]
    rows = []
    for g, (name, _, desc) in SHELVES.items():
        cs = by.get(g, [])
        d = LIB / f"{g}_{name}"
        d.mkdir(parents=True, exist_ok=True)
        tot = sum(c["size"] for c in cs)
        h = [c for c in cs if c["age_days"] <= 7]
        subst = [c for c in cs if c["path"].lower().endswith((".md", ".txt")) and c["size"] >= 800 and c["latest"]
                 and ".mimosa" not in c["path"]]
        subst.sort(key=lambda c: c["effective_date"], reverse=True)
        series = defaultdict(list)
        for c in cs:
            if c.get("series_key"):
                series[c["series_key"]].append(c)
        ser = [(k, v) for k, v in series.items() if len(v) >= 3]
        ser.sort(key=lambda kv: max(c["effective_date"] for c in kv[1]), reverse=True)
        L = [f"# {g} {name}: LATEST", "", f"_{desc}_", "",
             f"Generated {NOW:%Y-%m-%d %H:%M} ET by scripts/inbox_librarian.py. Read-only view; files stay where they are in watch/inbox.", "",
             f"**{len(cs):,} files, {human(tot)}**; last 7 days: {len(h):,} files, {human(sum(c['size'] for c in h))}; "
             f"tiers: {sum(1 for c in cs if c['tier']=='rule'):,} rule / {sum(1 for c in cs if c['tier'].startswith('model')):,} model; "
             f"needs_review: {sum(1 for c in cs if c.get('needs_review')):,}; verified false: {sum(1 for c in cs if c.get('verified') is False):,}.", "",
             "## Newest 15 substantive docs", "", "| effective (ET) | doc | summary |", "|---|---|---|"]
        for c in subst[:15]:
            L.append(f"| {c['effective_date'][:16].replace('T',' ')} | [{c['path']}]({rel_link(c['path'])}) | {(c.get('summary') or '').replace('|','/')[:140]} |")
        L += ["", "## Repeating series (latest copy only)", "", "| series | copies | span | latest |", "|---|---|---|---|"]
        for k, v in ser[:40]:
            v.sort(key=lambda c: c["effective_date"])
            L.append(f"| {k} | {len(v)} | {v[0]['effective_date'][:10]} .. {v[-1]['effective_date'][:10]} | [{v[-1]['path']}]({rel_link(v[-1]['path'])}) |")
        if not ser:
            L.append("| (none) | | | |")
        tops = Counter(c["path"].split("\\")[0] if "\\" in c["path"] else "(root)" for c in cs)
        L += ["", "## Where its files live (top folders)", ""] + [f"- `{t}`: {n:,}" for t, n in tops.most_common(15)]
        (d / "LATEST.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        rows.append((g, name, desc, len(cs), tot, len(h), sum(c["size"] for c in h)))
    nr = sum(1 for c in cards if c.get("needs_review"))
    vt = sum(1 for c in cards if c.get("verified") is True)
    vf = sum(1 for c in cards if c.get("verified") is False)
    I = ["# WATCH LIBRARY: INDEX (read this first)", "",
         f"Generated {NOW:%Y-%m-%d %H:%M} ET by `scripts/inbox_librarian.py`. The library is a **catalog**, not a move: every file stays at its path in `watch/inbox/`.",
         "Cards live in [`catalog.jsonl`](catalog.jsonl) (one JSON card per file: path, size, effective_date, shelf, tier, rule or confidence, summary, family, supersedes, latest, needs_review, verified).", "",
         "## Shelves", "", "| shelf | what goes here | files | size | last 7 days | LATEST |", "|---|---|---|---|---|---|"]
    for g, name, desc, n, tot, hn, hb in rows:
        I.append(f"| **{g} {name}** | {desc} | {n:,} | {human(tot)} | {hn:,} ({human(hb)}) | [{g}_{name}/LATEST.md]({g}_{name}/LATEST.md) |")
    I += ["", "## Hot and cold", "",
          f"- Total: {len(cards):,} files, {human(sum(c['size'] for c in cards))}.",
          f"- Hot (effective date within 7 days): {len(hot):,} files, {human(sum(c['size'] for c in hot))}.",
          f"- Cold (older than 30 days): {len(cold):,} files, {human(sum(c['size'] for c in cold))}.",
          f"- Archive shelf ω (cold + media exports + dormant folders): {len(by.get('ω', [])):,} files, {human(sum(c['size'] for c in by.get('ω', [])))}. See [ARCHIVE_PROPOSAL.md](ARCHIVE_PROPOSAL.md).",
          f"- Tiers: {sum(1 for c in cards if c['tier']=='rule'):,} rule cards, {sum(1 for c in cards if c['tier']=='model'):,} per-file model cards, {sum(1 for c in cards if c['tier']=='model-folder'):,} folder-model cards, {sum(1 for c in cards if c['tier']=='pending'):,} pending (model budget ran out).",
          f"- needs_review: {nr:,}. Verified sample: {vt} true / {vf} false (method and accuracy: [VERIFICATION.md](VERIFICATION.md)).", "",
          "## Resume / refresh", "",
          "`python scripts\\inbox_librarian.py --model-budget-min 30` continues where the last run stopped. It re-uses model_cache.jsonl, and it only sends files still marked tier `pending` plus new or changed files to the local model. Use `--no-model` for a rules-only refresh. Never schedule it while another seat is using Ollama heavily.", "",
          "## Rule for new files (every seat)", "",
          "1. **Name it with a shelf prefix**: `ALPHA_`/`CHAIN_`, `BETA_`/`GSTD_`, `GAMMA_`/`LANES_`, `DELTA_`/`BOB_`, `EPSILON_`/`DOCTRINE_`, `ZETA_`/`OPS_` (for example `CHAIN_V2_CATCHUP_20261018.md`). Keep the `YYYYMMDD` date in the name.",
          "2. **Append one card** to `watch/LIBRARY/catalog.jsonl`, or just run `python scripts\\inbox_librarian.py` (incremental: catalogs new or changed files, then refreshes every LATEST.md and this INDEX).",
          "3. A repeating series (patrols, receipts, digests) keeps the same family name and a new date. The newest copy is marked `latest`, and older copies are reachable through `supersedes`.",
          "4. Trust only cards with `verified: true` or tier `rule` for decisions. `needs_review` cards sit on χ until a human or seat re-shelves them.", "",
          "## How tiers work", "",
          "- **Tier 1 (rule, cheap decider):** a path-only rule for secret_gate_results/free_keys, then age >30d → ω, media/day-folder exports → ω, `.mimosa` tool state → ζ, filename-prefix rules, folder rules, dormant folder (nothing in 14d) → ω. The rule that fired is stored on the card.",
          "- **Tier 2 (escalation, local Ollama only):** unplaced root files get path + first ~30 lines (key-like strings masked) → {shelf, summary, confidence}. Unmapped active folders are classified once per folder. Confidence < 0.6 → χ with needs_review.",
          "- Sensitive files (.env, steps.jsonl, key/secret/token names, secret_gate_results/, free_keys*/) are classified by path only and never read."]
    (LIB / "INDEX.md").write_text("\n".join(I) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--no-model", action="store_true")
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--ollama", default="http://localhost:11434")
    ap.add_argument("--model-budget-min", type=float, default=20.0)
    ap.add_argument("--threshold", type=float, default=0.6)
    args = ap.parse_args()
    LIB.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    old = {}
    if CATALOG.exists() and not args.full:
        for ln in CATALOG.read_text(encoding="utf-8").splitlines():
            try:
                c = json.loads(ln); old[c["path"]] = c
            except (json.JSONDecodeError, KeyError):
                pass
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    prev_sig = {} if args.full else state.get("sig", {})
    folder_cache = {} if args.full else state.get("folder_shelves", {})
    mcache = {}
    if MCACHE.exists():
        for ln in MCACHE.read_text(encoding="utf-8").splitlines():
            try:
                j = json.loads(ln); mcache[j["key"]] = j
            except (json.JSONDecodeError, KeyError):
                pass
    for k, j in mcache.items():
        if k.startswith("folder:") and k[7:] not in folder_cache:
            folder_cache[k[7:]] = [j["shelf"], j["confidence"], j["summary"]]
    if RUNLOG.exists():  # recover folder decisions of an interrupted run from its log
        for ln in RUNLOG.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.search(r" folder (\S+): (\S) conf=([\d.]+) \([\d.]+s\) ?(.*)$", ln)
            if m and m[2] in SHELVES and m[1] not in folder_cache:
                folder_cache[m[1]] = [m[2], float(m[3]), m[4]]
    files = scan()
    log(f"scan: {len(files)} files in {INBOX} (+ {sum(1 for f in files if f['path'].startswith('..'))} seat docs in LIBRARY); cached folder decisions {len(folder_cache)}, cached file decisions {sum(1 for k in mcache if not k.startswith('folder:'))}")
    folder_newest = defaultdict(lambda: dt.datetime(1970, 1, 1))
    for f in files:
        folder_newest[f["top"]] = max(folder_newest[f["top"]], f["eff"])
    changed = 0
    cards, need_file, need_folder = [], [], defaultdict(list)
    for f in files:
        sig = [f["size"], f["mtime"]]
        unchanged = prev_sig.get(f["path"]) == sig
        changed += not unchanged
        g, rule = tier1(f, folder_newest)
        oc = old.get(f["path"]) if unchanged else None
        card = dict(path=f["path"], size=f["size"], effective_date=f["eff"].isoformat(timespec="seconds"),
                    age_days=round((NOW - f["eff"]).total_seconds() / 86400, 2), shelf=g, tier="rule", rule=rule,
                    confidence=None, summary=None, family=family(f["name"]), supersedes=None, latest=True,
                    needs_review=False, verified=(oc or {}).get("verified"),
                    series_key=None)
        if f["sensitive"]:
            card["summary"] = "(contents not read: sensitive name or path)"
        elif oc and oc.get("summary") and oc.get("tier") == "rule":
            card["summary"] = oc["summary"]
        else:
            card["summary"] = first_heading(INBOX / f["path"], f["ext"])
        if g is None:
            key = f"{f['path']}|{f['size']}|{f['mtime']}"
            if f["top"] != "(root)":
                need_folder[f["top"]].append(card)
            elif f["sensitive"] or f["ext"] not in MODEL_EXT or f["size"] == 0:
                card.update(shelf="χ", rule="root-unmapped:not-model-readable", needs_review=True)
            elif key in mcache:
                j = mcache[key]
                card.update(tier="model", rule=None, confidence=j["confidence"], shelf=j["shelf"], summary=j["summary"] or card["summary"])
            else:
                card["_key"] = key; card["_eff"] = f["eff"]
                need_file.append(card)
        cards.append(card)
    log(f"tier1 placed {sum(1 for c in cards if c['shelf'])} of {len(cards)}; changed/new {changed}; root files for model {len(need_file)}; unmapped active folders {len(need_folder)}")
    budget = 0 if args.no_model else args.model_budget_min * 60
    t_model = time.time(); n_calls = 0; secs_total = 0.0
    # folder-level escalation first (cheap: one call per folder)
    for top, cs in sorted(need_folder.items(), key=lambda kv: -len(kv[1])):
        if top in folder_cache:
            g, conf, summ = folder_cache[top]
        elif time.time() - t_model < budget:
            names = "\n".join(sorted({c["path"] for c in cs})[:25])
            sample = next((c for c in sorted(cs, key=lambda c: c["size"], reverse=True)
                           if c["path"].lower().endswith((".md", ".txt")) and not is_sensitive(c["path"], Path(c["path"]).name)), None)
            txt = f"FILE LIST:\n{mask(names)}\n" + (f"\nSAMPLE {sample['path']}:\n{head(INBOX / sample['path'], 30)}" if sample else "")
            try:
                g, conf, summ, s = ask_model(args, f"FOLDER: watch/inbox/{top} ({len(cs)} files)", txt[:5000])
            except Exception as e:  # noqa: BLE001
                log(f"model error folder {top}: {e}"); g, conf, summ, s = "χ", 0.0, "", 0
            n_calls += 1; secs_total += s
            folder_cache[top] = [g, conf, summ]
            with open(MCACHE, "a", encoding="utf-8") as mcf:
                mcf.write(json.dumps({"key": f"folder:{top}", "shelf": g, "confidence": conf, "summary": summ, "secs": round(s, 2), "model": args.model}, ensure_ascii=False) + "\n")
            log(f"folder {top}: {g} conf={conf:.2f} ({s:.1f}s) {summ[:80]}")
        else:
            g, conf, summ = None, None, None
        for c in cs:
            if g is None:
                c.update(shelf="χ", tier="pending", rule="model budget exhausted", needs_review=True)
            else:
                c.update(tier="model-folder", rule=None, confidence=conf,
                         shelf=g if conf >= args.threshold else "χ", needs_review=conf < args.threshold)
                if not c["summary"]:
                    c["summary"] = summ
    need_file.sort(key=lambda c: c["_eff"], reverse=True)
    with open(MCACHE, "a", encoding="utf-8") as mc:
        for i, c in enumerate(need_file):
            if time.time() - t_model >= budget:
                c.update(shelf="χ", tier="pending", rule="model budget exhausted", needs_review=True)
                continue
            try:
                g, conf, summ, s = ask_model(args, f"PATH: watch/inbox/{c['path']} ({c['size']} bytes)", head(INBOX / c["path"], 30))
            except Exception as e:  # noqa: BLE001
                log(f"model error {c['path']}: {e}"); c.update(shelf="χ", tier="pending", rule=f"model error", needs_review=True); continue
            n_calls += 1; secs_total += s
            mc.write(json.dumps({"key": c["_key"], "shelf": g, "confidence": conf, "summary": summ, "secs": round(s, 2), "model": args.model}, ensure_ascii=False) + "\n"); mc.flush()
            c.update(tier="model", rule=None, confidence=conf, summary=summ or c["summary"])
            c["shelf"] = g if conf >= args.threshold else "χ"
            c["needs_review"] = conf < args.threshold
            if n_calls % 25 == 0:
                log(f"model progress: {i+1}/{len(need_file)} root files, {n_calls} calls, avg {secs_total/max(n_calls,1):.1f}s/call")
    for c in cards:
        if c.get("tier") == "model" and c.get("confidence") is not None and c["confidence"] < args.threshold:
            c["shelf"] = "χ"; c["needs_review"] = True
        c.pop("_key", None); c.pop("_eff", None)
    # supersedes chains: dated copies of the same family in the same folder
    groups = defaultdict(list)
    for c, f in zip(cards, files):
        if f["fdate"]:
            d = os.path.dirname(c["path"])
            groups[(d, c["family"])].append(c)
    for (d, fam), cs in groups.items():
        if len(cs) < 2:
            continue
        cs.sort(key=lambda c: (c["effective_date"], c["path"]))
        for i, c in enumerate(cs):
            c["series_key"] = (d + "\\" if d else "") + fam
            c["supersedes"] = cs[i - 1]["path"] if i else None
            c["latest"] = i == len(cs) - 1
    tmp = CATALOG.with_suffix(".jsonl.tmp")
    with open(tmp, "w", encoding="utf-8") as fo:
        for c in cards:
            fo.write(json.dumps(c, ensure_ascii=False) + "\n")
    os.replace(tmp, CATALOG)
    state = {"last_run": NOW.isoformat(timespec="seconds"), "model": args.model,
             "sig": {f["path"]: [f["size"], f["mtime"]] for f in files}, "folder_shelves": folder_cache,
             "last_model_calls": n_calls, "last_model_secs": round(secs_total, 1)}
    STATE.write_text(json.dumps(state), encoding="utf-8")
    write_outputs(cards)
    cnt = Counter(c["shelf"] for c in cards)
    log("shelves: " + ", ".join(f"{g}:{cnt.get(g,0)}" for g in SHELVES))
    log(f"tiers: " + ", ".join(f"{k}:{v}" for k, v in Counter(c['tier'] for c in cards).items()) +
        f"; needs_review {sum(1 for c in cards if c['needs_review'])}; model calls {n_calls}, {secs_total:.0f}s"
        f" ({(secs_total/n_calls if n_calls else 0):.1f}s/call, {(3600*n_calls/secs_total if secs_total else 0):.0f}/h); run {time.time()-t_start:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
