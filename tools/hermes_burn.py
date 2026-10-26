"""hermes_burn — spend the Nous credits USEFULLY: Claude into the squeaky joints.

Vehicle for the 2026-10-01 operator order ("spend 70+$ hermes credits, use
claude to inject logic into our squeakiest joints"). The Nous inference API
serves the anthropic/* family (probed live 2026-10-01: 423 models incl.
opus-5.5/sonnet-5.5/fable-5.1); pricing table below captured from that probe.

Contract per ask (the frontier-ask production-line laws):
- every ask is a DIRECTORY under the queue root: ask.json {id, model, system,
  evidence: [repo-relative paths], contract, max_tokens, revision: bool}
  plus optional revision.md (steering text for round 2 on the same context)
- outputs land at watch/inbox/hermes_burn/<id>.md (out-prefix law: one file
  per ask, never a shared slot)
- usage rows append to memory/runs/hermes_burn/usage.jsonl:
  {ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok}
  (the driving-ladder law: every paid dispatch banks its burn)
- fail-loud per ask, batch continues; retry-once per turn on transport errors
- finish=stop: no runaway loops, one retry then the ask is marked failed

CARRIER-PATCH laws (2026-10-01, receipts watch/inbox/hermes_burn/
DAY1_CROSS_RACTOR.md E1/E3/N3 + DAY1_RIB_WARMTH.md X1/X2; the day bled
$18.89 of $29.91 as pure re-fire theater):
- LANDED BEATS FORCE: a fire is refused when the output file exists unless a
  revision rides turn2_only; the force flag can no longer re-burn a landed
  deliverable (a stale force ask burned A1 45x at $20.53 after landing)
- REFUSED IS TERMINAL: after 2 provider refusals for one ask id the carrier
  mints <ask_dir>/REFUSED (refusal snippet) and skips on sight forever;
  re-arming requires an operator edit of the ask bytes plus marker removal
  (N1 x42 and DUEL1_hidden_5 x46 refusal-retry loops are the disease)
- EVIDENCE PREFLIGHT: before ANY API call, every evidence[] path must exist
  on disk and its rendered bytes must be present in the message body being
  sent, and an ask with no evidence at all fails closed (DUEL2 fired 14 paid
  calls whose material never reached the model; T1W2 went out evidence: [])
- TERMINAL IS TERMINAL (ops-triage move 2, 2026-10-07, receipt
  watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md): an ask that fails
  EVIDENCE-PREFLIGHT once, or whose TRAILING ledger run of transport
  failures reaches 2, mints <ask_dir>/TERMINAL and skips on sight forever;
  re-arm requires an operator edit of the ask bytes plus marker removal.
  Transport failures bank as data rows (turn: None, ok: false) so the wall
  is visible in the ledger. The 10-06 23:54Z .. 10-07 08:00Z provider 402
  wall fired MagHermesBurn247 hourly ~8 times, 402ing A1 twice per fire
  with nothing banked and no terminal state - the loop could not self-stop
  and every fire exited 1.

Endpoint fence (the Mimosa SSRF rulings, same shape as tools/binary_attest.py):
fixed https URL on exactly one host, asserted per call, AND the host resolved
with private/loopback/link-local/reserved/multicast IPs refused (DNS or
hosts-file re-pointing cannot aim this tool at internal surfaces).

REPOINT 2026-10-16 (operator: "i dont have any more money in hermes but you
cna drive the free lanes and stealth models through it" - the Nous credits
died on the 10-06/07 402 wall, ledger cold since 10-07): the carrier is now
endpoint-portable by env. HERMES_BURN_API_BASE is the FULL https chat URL
(default unchanged: the Nous endpoint); the fence still asserts exactly that
URL's one host, public-only, per call. Key names extended
(HERMES_BURN_API_KEY, then OPENROUTER_API_KEY / OPENROUTER_KEY_1, then the
legacy HERMES pair). HERMES_BURN_UNPRICED_OK=1 prices unknown models at
(0.0, 0.0) so free-lane :free SKUs fire and bank zero-cost rows; without the
flag the fail-closed pricing law stands. First free-lane endpoint:
https://openrouter.ai/api/v1/chat/completions (live 2026-10-14/16). Path
lesson receipted: a host-only override sent OpenRouter-shape asks to
openrouter.ai/v1/... and Cloudflare answered 1010 - the base is the full URL.

Exit: 0 all asks ok / 1 any failed / 2 usage.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mag.inference_budget import guard_terminal, plan_call, skip_terminal  # noqa: E402
from tools.instance_guard import (  # noqa: E402
    claim_ask,
    doubled_key_check,
    release_ask,
)
OUT_DIR = ROOT / "watch" / "inbox" / "hermes_burn"
USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
# 2026-10-16 repoint, corrected: the override is the FULL URL, not a host.
# Host-only was wrong for OpenRouter (/api/v1/... vs the Nous /v1/... path)
# and its unknown-path hits came back Cloudflare 1010 (signature/403), which
# cost the first test ask its 2-strike transport trail. The fence still
# asserts the one host of this one fixed URL, public-only, per call.
_DEFAULT_API = "https://inference-api.nousresearch.com/v1/chat/completions"
API = os.environ.get("HERMES_BURN_API_BASE", _DEFAULT_API)

# tor circuit wire-in (2026-10-21, tor_circuits organ): HERMES_BURN_PROXY=
# socks5://127.0.0.1:9050 routes ALL of this carrier's transport through the
# local Tor SOCKS port; HERMES_BURN_PROXY_USER gives a per-conversation
# circuit (Tor isolates by SOCKS credential - tools/tor_circuits.py socks_for).
# Default OFF: the wire is direct until the isolation is wanted. PySocks is
# already in the venv; the global in-process monkeypatch is safe because this
# module is the transport owner and mostly runs as its own CLI process.
if os.environ.get("HERMES_BURN_PROXY", "").startswith("socks5"):
    import socks as _pysocks
    import socket as _socket
    _proxy_parts = os.environ["HERMES_BURN_PROXY"].split("//", 1)[-1]
    _proxy_host, _, _proxy_port = _proxy_parts.partition(":")
    _proxy_user = os.environ.get("HERMES_BURN_PROXY_USER", "")
    _pysocks.set_default_proxy(_pysocks.SOCKS5, _proxy_host or "127.0.0.1",
                               int(_proxy_port or "9050"), rdns=True,
                               username=_proxy_user or None, password="x")
    _socket.socket = _pysocks.socksocket

_parsed_api = urllib.parse.urlsplit(API)
if _parsed_api.scheme != "https" or not _parsed_api.hostname:
    raise SystemExit("HERMES_BURN_API_BASE must be a full https URL")
API_HOST = _parsed_api.hostname

# Captured from the live /v1/models pricing fields, 2026-10-01 probe.
PRICING = {  # usd per token: (input, output)
    "anthropic/claude-opus-5.5": (0.000004, 0.00002),
    "anthropic/claude-sonnet-5.5": (0.000002, 0.00001),
    "anthropic/claude-fable-5.1": (0.00001, 0.00005),
    "anthropic/claude-haiku-4.5": (0.000001, 0.000005),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _hermes_key() -> str:
    # 2026-10-16 repoint: generic then OpenRouter names first (the free-lane
    # hosts), legacy KEY_2-first Nous order kept as fallback for the default
    # host (2026-10-01 live probe - key 1 402s on premium anthropic SKUs,
    # key 2 carried the credits while credits existed).
    for name in ("HERMES_BURN_API_KEY", "OPENROUTER_API_KEY",
                 "OPENROUTER_KEY_1", "HERMES_API_KEY_2", "HERMES_API_KEY_1"):
        for line in open(ROOT / ".env", encoding="utf-8", errors="replace"):
            line = line.strip()
            if line.startswith(name + "="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    raise SystemExit("no HERMES_API_KEY in .env")


def _assert_public_endpoint() -> None:
    infos = socket.getaddrinfo(API_HOST, 443, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(
                f"endpoint fence: {API_HOST} resolves to non-public {ip}")


def _build_body(model: str, messages: list[dict], max_tokens: int,
                extra_body: dict | None = None) -> dict:
    """The request body, pure (offline-inspectable). extra_body is the
    inference_budget plan (thinking control merged, forbidden keys already
    stripped). Fix 2026-10-04 (parked-decisions SYNTHESIS.md:243-250): the
    plan was computed at the call site and dropped one hop before the wire,
    so the nous-primes reasoning {max_tokens: 6000} rail never reached the
    request that burned 15998 reasoning tokens (usage.jsonl:1151). The core
    keys win over the plan; the plan cannot rewrite model/messages."""
    body = dict(extra_body or {})
    body.update({"model": model, "messages": messages,
                 "max_tokens": max_tokens})
    return body


def _call(model: str, messages: list[dict], max_tokens: int, key: str,
          retries: int = 1, extra_body: dict | None = None) -> dict:
    parsed = urllib.parse.urlsplit(API)
    if parsed.scheme != "https" or parsed.hostname != API_HOST:
        raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
    _assert_public_endpoint()
    body = json.dumps(_build_body(model, messages, max_tokens,
                                  extra_body)).encode("utf-8")
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            API, data=body, method="POST",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError) as exc:
            last = exc
            if attempt < retries:
                # 2026-10-16 free-lane lesson: a 429 on a free SKU is a
                # rolling-window rate limit - the OC width law says HOLD, not
                # retreat; back off minutes-scale, not 20 seconds.
                time.sleep(120 if isinstance(exc, urllib.error.HTTPError)
                           and getattr(exc, "code", 0) == 429 else 20)
    raise RuntimeError(f"transport failed after {retries + 1} tries: {last!r}")


def _read_evidence(paths: list[str]) -> str:
    parts = []
    for rel in paths:
        p = ROOT / rel
        if not p.is_file():
            parts.append(f"\n\n=== EVIDENCE {rel} (MISSING) ===\n")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        cap = 400_000
        if len(text) > cap:
            text = text[:cap] + f"\n... [truncated at {cap} chars]"
        parts.append(f"\n\n=== EVIDENCE {rel} ===\n{text}")
    return "".join(parts)


PROVIDER_USAGE = ROOT / "logs" / "provider_usage.jsonl"


def _bank(row: dict) -> None:
    # Dogfood-48h move 1 ingest tripwire: a banked (id, turn) that already
    # rows the ledger is the re-fire signature (13 doubled keys, $2.25 twin
    # window; A1 x49 for $21.09). Flag + alarm, never silently absorb.
    row = doubled_key_check(USAGE, row)
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    # Ghost 3 cure (2026-10-17): mirror hermes_burn rows into logs/provider_usage.jsonl
    # so estate meters (usage_monitor, cost_ledger, smith_chart) see openrouter/nous burns.
    try:
        PROVIDER_USAGE.parent.mkdir(parents=True, exist_ok=True)
        prov = "openrouter" if "openrouter" in API_HOST else ("nous" if "nous" in API_HOST else API_HOST)
        pin = int(row.get("prompt_tokens") or 0)
        pout = int(row.get("completion_tokens") or 0)
        prow = {
            "ts": row.get("ts") or _now(),
            "provider": prov,
            "model": row.get("model", ""),
            "calls": 1,
            "prompt_tokens": pin,
            "completion_tokens": pout,
            "cache_hit_tokens": 0,
            "cache_miss_tokens": pin,
            "session_id": f"hermes_burn:{row.get('id', '')}",
            "latency_ms": 0,
            "tokens": pin + pout,
            "cost_usd": float(row.get("cost_usd") or 0.0),
            "ok": bool(row.get("ok", False)),
            "meta": {"source": "hermes_burn", "turn": row.get("turn"), "channel": row.get("channel")},
        }
        with open(PROVIDER_USAGE, "a", encoding="utf-8") as pfh:
            pfh.write(json.dumps(prow, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _system_for(model: str) -> str:
    """Dogfood: the claritas canon face for the animal + the deterministic
    estate-law block every ask rides (the pre-warmed rib laws, fixed text)."""
    from mag.claritas import face_for
    laws = (
        "\n\nESTATE LAWS (deterministic block, applies to every answer):\n"
        "- Trust bytes, not reports: cite file:line for every claim about the code.\n"
        "- A verdict without its conditions is not a verdict: name instrument,\n"
        "  moment, and context assumptions for any measurement you rely on.\n"
        "- Citations resolve to quoted bytes or are marked UNVERIFIED.\n"
        "- No em-dashes anywhere. Plain hyphens only.\n"
        "- Prefer ONE landable deliverable (a spec or patch a seat can apply\n"
        "  as-is) over a survey. Name your own deliverable's falsifier."
    )
    return face_for(model) + laws


def _refusal_state(ask_id: str) -> tuple[int, str]:
    """(count, last snippet) of provider-refusal ledger rows for one ask id.

    CARRIER-PATCH 2 read side: refusals are data, not failures to retry
    (DAY1_RIB_WARMTH X2: the carrier banked the refused field all day while
    the driver retried DUEL1_hidden_5 46x and N1 42x for over two hours)."""
    count, snippet = 0, ""
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("id") == ask_id and row.get("refused"):
                count += 1
                snippet = str(row["refused"])
    return count, snippet


def _mint_refused_marker(ask_dir: Path, ask_id: str, snippet: str) -> Path:
    marker = ask_dir / "REFUSED"
    marker.write_text(
        f"{snippet[:500]}\n\n[REFUSED terminal marker, minted {_now()} for ask id "
        f"{ask_id} after >= 2 provider refusals (DAY1_RIB_WARMTH X2). The carrier "
        "skips this ask on sight. Re-arm only by editing the ask bytes AND "
        "deleting this marker.]\n",
        encoding="utf-8")
    return marker


def _terminal_state(ask_id: str) -> tuple[int, str]:
    """(consecutive transport-failure count, last error) for one ask id.

    Ops-triage move 2 (morning-block-20261007): the 10-06 23:54Z .. 10-07
    08:00Z wall fired MagHermesBurn247 hourly for ~8h and every fire 402'd
    A1 twice (transport failed after 2 tries) with NOTHING banked and no
    terminal state, so the loop could never self-stop (logs/
    hermes_burn_247.log; memory/attention.md:699-729, one exit-1 row per
    hour). Transport failures are banked as data (turn: None, the
    guard_terminal empty_reasoning precedent) and read back here as the
    ask's TRAILING RUN of transport_error rows: any banked outcome for the
    ask that is not a transport failure resets the run to zero."""
    count, last_err = 0, ""
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("id") != ask_id:
                continue
            if row.get("transport_error"):
                count += 1
                last_err = str(row["transport_error"])
            else:
                count, last_err = 0, ""
    return count, last_err


def _mint_terminal_marker(ask_dir: Path, ask_id: str, snippet: str,
                          cause: str) -> Path:
    marker = ask_dir / "TERMINAL"
    marker.write_text(
        f"{snippet[:500]}\n\n[TERMINAL terminal marker ({cause}), minted "
        f"{_now()} for ask id {ask_id}. The carrier skips this ask on sight. "
        "Re-arm only by editing the ask bytes AND deleting this marker.]\n",
        encoding="utf-8")
    return marker


def _landed_skip(meta: dict, ask_dir: Path, out_path: Path) -> dict | None:
    """CARRIER-PATCH 1: the deliverable-exists truth beats the force flag.

    DAY1_RIB_WARMTH X1 + LADDER-TRUTH 2: A1_steer_antiforgery re-burned 45x
    ($20.53) after its deliverable landed at 16:10Z because a stale force
    flag in memory/plans/hermes_burn_batch1/A1_steer_antiforgery/ask.json
    (mtime 09:18, never cleaned) bypassed the old skip on every 45s driver
    cycle; the flag-hygiene fix only cured NEW staging. Every (re)fire enters
    through run_ask, so this entry check is the single choke point for both
    cycle-boundary retry triggers (empty content channel, provider refusal).
    Only a pending revision riding turn2_only re-opens a landed ask (the
    standing revision shape; a revision flag without turn2_only skipped at
    entry under the old gate too)."""
    if not out_path.exists():
        return None
    revision_pending = (bool(meta.get("revision"))
                        and (ask_dir / "revision.md").is_file())
    if revision_pending and meta.get("turn2_only"):
        return None
    return {"id": meta["id"], "ok": True,
            "skipped": ("output exists (no revision pending; force cannot "
                        "re-burn a landed deliverable)")}


def _assert_evidence_in_body(meta: dict, messages: list[dict]) -> None:
    """CARRIER-PATCH 3: fail closed BEFORE any API call on lost material.

    DAY1_CROSS_RACTOR E3/N3 + DAY1_RIB_WARMTH X5: DUEL2 fired 14 paid calls
    where the material bytes never reached the model (every output opens with
    'the EVIDENCE block is empty') and all four T1W2 asks went out with
    evidence: []; the duel stager pasted ask_bank's NON-reveal draw metadata
    (bank/draw_id/material_path/first_line JSON) into the contract instead of
    the rendered material (tools/ask_bank.py cmd_draw without --reveal).
    Every evidence path must exist on disk and its rendered head must appear
    in the message body actually being sent; an evidence-less ask fails
    closed the same way (E3 steal: exit on an evidence-less fire)."""
    evidence = meta.get("evidence") or []
    if not evidence:
        raise RuntimeError(
            "EVIDENCE-PREFLIGHT: ask carries no evidence paths (evidence: []); "
            "refusing an evidence-less fire per DAY1_CROSS_RACTOR E3 - stage "
            "the material into evidence[] or render it into the contract")
    body = "\n".join(str(m.get("content") or "") for m in messages)
    for rel in evidence:
        p = ROOT / rel
        if not p.is_file():
            raise RuntimeError(
                f"EVIDENCE-PREFLIGHT: evidence path missing on disk: {rel}")
        text = p.read_text(encoding="utf-8", errors="replace")
        # head probe: _read_evidence truncates at 400k chars, so the first
        # 400 always survive into the body verbatim when the render worked
        probe = text[:400].strip()
        if not probe:
            raise RuntimeError(
                f"EVIDENCE-PREFLIGHT: evidence file is empty: {rel}")
        if probe not in body:
            raise RuntimeError(
                f"EVIDENCE-PREFLIGHT: rendered bytes of {rel} absent from the "
                "message body (the render step dropped the material)")


def run_ask(ask_dir: Path, key: str, execute: bool = True) -> dict:
    """The public entry and the claim choke point. ATOMIC ASK CLAIM
    (dogfood-48h ractor move 1, 2026-10-02): _landed_skip only protects
    AFTER the deliverable lands - two racers (the 20:40:13Z twins, the
    19:17Z T1W2 pair) both passed it and both paid for the same ask. The
    O_EXCL CLAIM closes the money window; a dead holder's marker goes
    stale and is stolen by the next cycle (instance_guard.claim_ask)."""
    ask_id = json.loads(
        (ask_dir / "ask.json").read_text(encoding="utf-8")).get("id")
    claim = claim_ask(ask_dir, str(ask_id))
    if claim is None:
        return {"id": ask_id, "ok": True,
                "skipped": "CLAIM held by a live instance (atomic fire claim)"}
    try:
        return _fire_ask(ask_dir, key, execute)
    finally:
        release_ask(claim)


def _fire_ask(ask_dir: Path, key: str, execute: bool = True) -> dict:
    meta = json.loads((ask_dir / "ask.json").read_text(encoding="utf-8"))
    model = meta["model"]
    if model not in PRICING:
        # 2026-10-16: free-lane SKUs (OpenRouter :free tier) have no pricing
        # row and cost nothing; with the operator-set flag they bank zero-cost
        # rows. Without the flag the fail-closed pricing law stands.
        if os.environ.get("HERMES_BURN_UNPRICED_OK") != "1":
            raise ValueError(f"unknown model {model}; add pricing first")
        PRICING[model] = (0.0, 0.0)
    out_path = OUT_DIR / f"{meta['id']}.md"
    # CARRIER-PATCH 2, entry half: skip-on-sight for terminally refused asks,
    # with ledger backfill (the standing N1 x42 / DUEL1_hidden_5 x46 loops
    # predate this marker; the count heals them without one more fire).
    refused_marker = ask_dir / "REFUSED"
    if refused_marker.is_file():
        return {"id": meta["id"], "ok": True,
                "skipped": "REFUSED (terminal; operator edit + marker removal "
                           "required to re-arm)"}
    refusals, refusal_snippet = _refusal_state(meta["id"])
    if refusals >= 2:
        _mint_refused_marker(ask_dir, meta["id"], refusal_snippet)
        return {"id": meta["id"], "ok": True,
                "skipped": f"REFUSED (terminal; {refusals} ledger refusals, "
                           "marker minted)"}
    # TERMINAL entry half (ops-triage move 2, morning-block-20261007; the
    # refusal-law shape above): an ask whose last 2 ledger outcomes were
    # transport failures, or that ever failed EVIDENCE-PREFLIGHT, skips on
    # sight. The 10-06/07 402 wall looped A1 hourly for ~8h because
    # transport failures banked nothing and nothing went terminal.
    terminal_marker = ask_dir / "TERMINAL"
    if terminal_marker.is_file():
        return {"id": meta["id"], "ok": True,
                "skipped": "TERMINAL (transport/preflight wall; operator edit "
                           "+ marker removal required to re-arm)"}
    transports, transport_err = _terminal_state(meta["id"])
    if transports >= 2:
        _mint_terminal_marker(ask_dir, meta["id"], transport_err,
                              f"{transports} consecutive transport failures")
        return {"id": meta["id"], "ok": True,
                "skipped": f"TERMINAL (minted; {transports} consecutive "
                           "transport failures, marker minted)"}
    # INFERENCE-BUDGET entry: a terminally burned ask never refires same params.
    done = skip_terminal(ask_dir, meta["id"])
    if done is not None:
        return done
    # CARRIER-PATCH 1, entry half (see _landed_skip for the receipt).
    skip = _landed_skip(meta, ask_dir, out_path)
    if skip is not None:
        return skip
    prompt = (_system_for(model) + "\n\n=== CONTRACT ===\n" + meta["contract"]
              + "\n\n=== EVIDENCE ===" + _read_evidence(meta.get("evidence", []))
              + "\n\nProduce the deliverable the CONTRACT demands. Positive AND negative examples where they clarify. Match the requested shape exactly.")
    messages = [{"role": "user", "content": prompt}]
    original_user_msg = messages[0]
    turns = []
    result_row = {"id": meta["id"], "model": model, "ok": True}
    for turn_no in (1, 2):
        if turn_no == 2:
            rev = ask_dir / "revision.md"
            if not meta.get("revision") or not rev.is_file() or not execute:
                break
            # Window-1 defect fix: turn 2 sent the assistant echo and both
            # channels came back empty (usage={}); revision turns now carry
            # ONLY [original user prompt, revision user message] - the model
            # re-derives its own draft from context, no echo to choke on.
            messages = [original_user_msg,
                        {"role": "user", "content": rev.read_text(encoding="utf-8")}]
        if not execute:
            turns.append({"turn": turn_no, "dry": True})
            continue
        if turn_no == 1 and meta.get("turn2_only"):
            turns.append({"turn": 1, "skipped": "turn2_only"})
            continue
        # CARRIER-PATCH 3: the evidence preflight fails closed BEFORE any
        # API call, on every turn (turn 2 rebuilds messages; the material
        # must still be in the body actually being sent). TERMINAL mint
        # half (ops-triage move 2): a preflight failure is deterministic
        # (missing/empty evidence, dropped render) and never self-heals, so
        # the marker mints on FIRST occurrence; the raise still propagates
        # so this cycle reports the fail.
        try:
            _assert_evidence_in_body(meta, messages)
        except RuntimeError as exc:
            if "EVIDENCE-PREFLIGHT" in str(exc) and \
                    not (ask_dir / "TERMINAL").is_file():
                _mint_terminal_marker(ask_dir, meta["id"], str(exc),
                                      "EVIDENCE-PREFLIGHT")
            raise
        # INFERENCE-BUDGET: the RIB_MODEL_GATES recipe plans the fire (floor per
        # ask shape, thinking control) and guards the response (fable B1/B5 shape).
        plan = plan_call(model=model, prompt_chars=len(prompt), requested_max_tokens=meta.get("max_tokens"))
        try:
            resp = _call(model, messages, plan.max_tokens or meta.get("max_tokens", 24000), key,
                         extra_body=plan.extra_body)
        except RuntimeError as exc:
            # TERMINAL mint half, transport leg (ops-triage move 2): bank the
            # failure as data (turn: None, the guard_terminal precedent, so
            # doubled_key_check stays silent) and go terminal when the ask's
            # TRAILING ledger run of transport failures reaches 2. The 10-06
            # 402 wall burned 8 hourly fires on A1 before this state existed.
            if "transport failed" in str(exc):
                _bank({"ts": _now(), "id": meta["id"], "model": model,
                       "turn": None, "transport_error": str(exc)[:200],
                       "cost_usd": 0.0, "ok": False})
                n_transport, last_err = _terminal_state(meta["id"])
                if n_transport >= 2 and not (ask_dir / "TERMINAL").is_file():
                    _mint_terminal_marker(ask_dir, meta["id"], last_err,
                                          f"{n_transport} consecutive transport failures")
            raise
        usage = resp.get("usage", {})
        pin, pout = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        cin, cout = PRICING[model]
        cost = pin * cin + pout * cout
        msg = resp["choices"][0]["message"]
        raw_content, finish_reason = msg.get("content"), resp["choices"][0].get("finish_reason")
        if cause := guard_terminal(ask_dir, meta["id"], plan.recipe_key, finish_reason, usage, raw_content, _bank, model=model, pin=pin, pout=pout, cost=cost):
            raise RuntimeError("EMPTY_REASONING (terminal): " + cause + ". Re-stage with the FAMILY_TABLE recipe or switch family")
        content, chan = raw_content, "content"
        if not content:
            content = msg.get("reasoning") or ""
            chan = "reasoning (content channel empty)"
        if not content:
            refusal = msg.get("refusal")
            if refusal:
                _bank({"ts": _now(), "id": meta["id"], "model": model,
                       "turn": turn_no, "refused": refusal[:200],
                       "prompt_tokens": pin, "completion_tokens": pout,
                       "cost_usd": round(cost, 4), "ok": False})
                # CARRIER-PATCH 2, mint half: the SECOND banked refusal for
                # this ask id makes the state terminal (DAY1_RIB_WARMTH X2;
                # the raise still propagates so this cycle reports the fail).
                n_refused, last_snippet = _refusal_state(meta["id"])
                if n_refused >= 2 and not refused_marker.is_file():
                    _mint_refused_marker(ask_dir, meta["id"], last_snippet)
                raise RuntimeError(f"REFUSED by provider: {refusal[:120]}")
            raise RuntimeError("empty response: both content and reasoning "
                               f"channels empty; usage={usage}")
        messages.append({"role": "assistant", "content": content})
        # RACTOR MOVE 1 (2026-10-03): the substance gate. A 1-char content
        # row banked ok:true tonight (19:25:23Z prime-judgment); hollow rows
        # now bank ok=false with their finish reason, and every downstream
        # meter divides by honest rows.
        row = {"ts": _now(), "id": meta["id"], "model": model, "turn": turn_no,
               "prompt_tokens": pin, "completion_tokens": pout,
               "reasoning_tokens": usage.get("completion_tokens_details", {}).get("reasoning_tokens"),
               "channel": chan, "content_chars": len(content.strip()),
               "finish_reason": finish_reason,
               "cost_usd": round(cost, 4),
               "ok": len(content.strip()) > 1}
        _bank(row)
        turns.append(row)
        if turn_no == 1:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                f"# {meta['id']} ({model}, turn 1, channel: {chan})\n\n{content}\n",
                encoding="utf-8")
        else:
            with open(out_path, "a", encoding="utf-8") as fh:
                fh.write(f"\n\n---\n\n# REVISION (turn 2)\n\n{content}\n")
    result_row["turns"] = turns
    result_row["cost_usd"] = round(sum(t.get("cost_usd", 0) for t in turns), 4)
    return result_row


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="hermes_burn")
    ap.add_argument("queue", help="dir of ask dirs (each holding ask.json)")
    ap.add_argument("--dry", action="store_true", help="validate asks, no calls")
    args = ap.parse_args(argv)
    qroot = Path(args.queue)
    ask_dirs = sorted(p for p in qroot.iterdir() if (p / "ask.json").is_file())
    if not ask_dirs:
        print(f"USAGE-ERROR: no ask dirs under {qroot}")
        return 2
    key = _hermes_key() if not args.dry else ""
    failed = 0
    results = []
    for d in ask_dirs:
        try:
            row = run_ask(d, key, execute=not args.dry)
            results.append(row)
            cost = row.get("cost_usd", 0)
            print(f"{'OK ' if row.get('ok') else 'FAIL'} {row['id']} "
                  f"cost=${cost:.2f}" + (" (skipped)" if row.get("skipped") else ""))
        except Exception as exc:  # noqa: BLE001 - fail-loud per ask, continue
            failed += 1
            results.append({"id": d.name, "ok": False})
            print(f"FAIL {d.name}: {exc!r}")
    total = 0.0
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                total += json.loads(line).get("cost_usd", 0)
            except json.JSONDecodeError:
                pass
    # Ops-triage move 2 (morning-block-20261007): the flat "2/3 asks" shape
    # read the 10-07 08:00Z fire as "2 OK asks" when those 2 were SKIPS
    # ($0.00, landed-output skips) and the 1 real ask was the failure -
    # paid/skipped/failed are different states and the summary now says so.
    paid = sum(1 for r in results if r.get("ok") and not r.get("skipped"))
    skipped = sum(1 for r in results if r.get("skipped"))
    print(f"HERMES-BURN: {'FAIL' if failed else 'PASS'} - paid {paid} "
          f"skipped {skipped} failed {failed} of {len(ask_dirs)} asks; "
          f"ledger total ${total:.2f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
