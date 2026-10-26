"""model_garden: multi-family ask runner (generalizes tools/hermes_burn.py).

The carrier's ask production line run against every allowlisted family,
without forking the Nous-specific guts (key ladder, pricing table, fixed
endpoint). Guard-law receipts: the carrier docstring +
watch/inbox/hermes_burn/DAY1_CROSS_RACTOR.md + DAY1_RIB_WARMTH.md.

Ask = a DIRECTORY under the queue root: ask.json {id, model, base_env,
base_url, evidence: [repo-relative paths], contract, max_tokens,
revision: bool, turn2_only: bool} + optional revision.md (turn-2
steering). NEW vs the carrier: base_env (NAME of the env var holding the
api key: os.environ then ROOT/.env) and base_url (https://host[/prefix];
chat path appended: empty -> /v1/chat/completions, other prefix ->
<prefix>/chat/completions, or the full URL). model stays free-form;
pricing rides PRICING, unknown models bank tokens at cost 0.0. Outputs:
watch/inbox/model_garden/<id>.md; ledger rows append to
memory/runs/model_garden/usage.jsonl as {ts, id, model, model_family,
base_url, turn, prompt_tokens, completion_tokens, reasoning_tokens?,
channel, cost_usd, ok} (refusal rows carry "refused" instead of channel).

Guards (CARRIER-PATCH laws, verbatim): landed-skip unless a revision
rides turn2_only; REFUSED terminal after 2 refusals per (id,
model_family) with a skip-on-sight <ask_dir>/REFUSED marker
(family-scoped so one id on two families cannot cross-contaminate);
evidence preflight (paths exist AND rendered in the body sent;
evidence-less fails closed). Dry runs the preflight: it is offline. The
system prompt is single-sourced from the carrier's _system_for.

Endpoint fence (Mimosa SSRF rulings): FAMILY_TABLE at the top is the ONE
place to extend; base_url must be bare https on exactly one allowlisted
host (exact or subdomain), asserted at entry AND per call, and the
resolved host must be public. Exit: 0 all ok / 1 any failed / 2 usage.

X3-1 A/B knob (2026-10-01, spec BATTERY.md amendment X3-1): ask.json may
carry system "bare" to fire with NO system prefix (the claritas A/B arm);
absent or null keeps the single-sourced production _system_for bytes.
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
OUT_DIR = ROOT / "watch" / "inbox" / "model_garden"
USAGE = ROOT / "memory" / "runs" / "model_garden" / "usage.jsonl"

# THE one place to extend the garden: host suffix -> family name.
# api.z.ai added 2026-10-01 for the garden battery cheap grid: glm-5.3-flash
# on the coding endpoint per configs/providers.yaml z_ai2 (endpoint law
# receipt: coding keys fake-1113 on raw /paas/v4, real path
# /api/coding/paas/v4); census row watch/inbox/model_garden/CENSUS.md.
FAMILY_TABLE = {
    "nousresearch.com": "nous",
    "api.x.ai": "xai",
    "api.deepseek.com": "deepseek",
    "api.moonshot.ai": "moonshot",
    "generativelanguage.googleapis.com": "google",
    "api.groq.com": "groq",
    "openrouter.ai": "openrouter",
    "api.z.ai": "zai",
}
# usd per token (input, output) by exact model id, extend as probed per family.
PRICING: dict[str, tuple[float, float]] = {
    # implied exact from our metered ledger n=6 rows, fit err < $0.00005
    # (watch/inbox/model_garden/ECON.md): fable-5.1 in $10/M out $50/M.
    "anthropic/claude-fable-5.1": (0.00001, 0.00005),
    # configs/cost_rates.yaml (docs.z.ai): glm-5.3-flash banked at cache-miss
    # input = upper bound; z.ai reports cached_tokens so receipts true it
    # down, never up.
    "glm-5.3-flash": (0.075e-6, 0.25e-6),
    # configs/cost_rates.yaml deepseek-v4 flash PEAK rates (fires landed
    # 22:1x UTC, outside the 01-04/06-10 UTC offpeak windows). deepseek-chat
    # is the estate's v4.1-flash mapping (tools/ds_workhorse.py AH10 law;
    # direct API has no v4.1 id - 400 names deepseek-flash/deepseek-v4-pro,
    # and canonical deepseek-flash defaults thinking ON while deepseek-chat
    # defaults OFF: probe 2026-10-01T22:11Z).
    "deepseek-chat": (0.44e-6, 1.32e-6),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _family_of(host: str) -> str:
    for suffix, family in FAMILY_TABLE.items():
        if host == suffix or host.endswith("." + suffix):
            return family
    raise RuntimeError(f"endpoint fence: host {host!r} not in FAMILY_TABLE "
                       f"{sorted(FAMILY_TABLE)} (extend the table to add one)")


def _endpoint(base_url: str) -> tuple[str, str]:
    """(full chat-completions URL, host) with the allowlist fence applied."""
    p = urllib.parse.urlsplit(base_url)
    if p.scheme != "https":
        raise RuntimeError(f"endpoint fence: base_url must be https, got {base_url!r}")
    if p.query or p.fragment or p.username:
        raise RuntimeError("endpoint fence: base_url must be bare https host"
                           f"[/prefix] with no query/userinfo, got {base_url!r}")
    host = p.hostname or ""
    _family_of(host)
    path = p.path.rstrip("/")
    if not path:
        path = "/v1/chat/completions"
    elif not path.endswith("/chat/completions"):
        path += "/chat/completions"
    return urllib.parse.urlunsplit((p.scheme, p.netloc, path, "", "")), host


def _assert_public_host(host: str) -> None:
    for info in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(f"endpoint fence: {host} resolves to non-public {ip}")


def _api_key(base_env: str) -> str:
    """base_env names the env var: os.environ first, then ROOT/.env."""
    val = os.environ.get(base_env, "").strip()
    if val:
        return val
    env_file = ROOT / ".env"
    if env_file.is_file():
        for line in open(env_file, encoding="utf-8", errors="replace"):
            if line.strip().startswith(base_env + "="):
                val = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    raise RuntimeError(f"no {base_env} in os.environ or {env_file}")


def _call(model: str, messages: list[dict], max_tokens: int | None, key: str,
          base_url: str, retries: int = 1,
          extra_body: dict | None = None) -> dict:
    # fence asserted PER CALL: the URL is rebuilt from the ask bytes every
    # time, so a stale patched constant cannot bypass the table
    url, host = _endpoint(base_url)
    _assert_public_host(host)
    # max_tokens None = UNCAPPED fire; extra_body = per-animal sampling rails
    # merged into the request body (e.g. z.ai reasoning_effort). Both are
    # API params only: the MESSAGE bytes stay byte-identical across families
    # (BATTERY.md law 1). Receipts: max_tokens-null = glm-5.3-flash row 17
    # (memory/continuity/seat_memory_20260927/ox-alpha-was-glm53-flash.md);
    # extra_body = z.ai 5.3-flash thinking-always-on law (thinking cannot be
    # disabled, 1210; bounded via reasoning_effort low + max_tokens >= the
    # 1536 floor per docs/ref/ZAI_API_EXPERT_REFERENCE.md section 4 + 5.1,
    # applied in the cheapgrid1 run after uncapped fires hung past the 900s
    # whole-response fence at default effort max / default budget 65536).
    body: dict = {"model": model, "messages": messages}
    if max_tokens is not None:
        body["max_tokens"] = max_tokens
    if extra_body:
        body.update(extra_body)
    body = json.dumps(body).encode("utf-8")
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, method="POST",
                                     headers={"Authorization": "Bearer " + key,
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError) as exc:
            last = exc
            if attempt < retries:
                time.sleep(20)
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


def _bank(row: dict) -> None:
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _refusal_state(ask_id: str, family: str) -> tuple[int, str]:
    """(count, last snippet) of refusal ledger rows for one (id, family);
    refusals are data, not failures to retry."""
    count, snippet = 0, ""
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (row.get("id") == ask_id and row.get("model_family") == family
                    and row.get("refused")):
                count += 1
                snippet = str(row["refused"])
    return count, snippet


def _mint_refused_marker(ask_dir: Path, ask_id: str, snippet: str) -> Path:
    marker = ask_dir / "REFUSED"
    marker.write_text(f"{snippet[:500]}\n\n[REFUSED terminal marker, minted {_now()} "
                      f"for ask id {ask_id} after >= 2 provider refusals. The garden "
                      "skips this ask on sight. Re-arm only by editing the ask bytes "
                      "AND deleting this marker.]\n", encoding="utf-8")
    return marker


def _landed_skip(meta: dict, ask_dir: Path, out_path: Path) -> dict | None:
    """The deliverable-exists truth beats the force flag; only a pending
    revision riding turn2_only re-opens a landed ask."""
    if not out_path.exists():
        return None
    if (bool(meta.get("revision")) and (ask_dir / "revision.md").is_file()
            and meta.get("turn2_only")):
        return None
    return {"id": meta["id"], "ok": True,
            "skipped": ("output exists (no revision pending; force cannot "
                        "re-burn a landed deliverable)")}


def _assert_evidence_in_body(meta: dict, messages: list[dict]) -> None:
    """Fail closed BEFORE any API call on lost material."""
    evidence = meta.get("evidence") or []
    # self_contained is the guard's own "render it into the contract" path,
    # made explicit per ask (BATTERY.md amendment 2026-10-01): the garden-v1
    # battery stages B6/B8 evidence-less per its evidence table and the bare
    # fail-close rejected them; every ask without evidence[] AND without
    # self_contained still fails closed exactly as before (DUEL2 law).
    if not evidence and not meta.get("self_contained"):
        raise RuntimeError("EVIDENCE-PREFLIGHT: ask carries no evidence paths "
                           "(evidence: []) and no self_contained flag; refusing "
                           "an evidence-less fire. Stage the material into "
                           "evidence[] or render it into the contract and "
                           "declare self_contained: true")
    body = "\n".join(str(m.get("content") or "") for m in messages)
    for rel in evidence:
        p = ROOT / rel
        if not p.is_file():
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: evidence path missing on disk: {rel}")
        probe = p.read_text(encoding="utf-8", errors="replace")[:400].strip()
        if not probe:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: evidence file is empty: {rel}")
        if probe not in body:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: rendered bytes of {rel} absent "
                               "from the message body (the render step dropped "
                               "the material)")


def run_ask(ask_dir: Path, key: str | None = None, execute: bool = True) -> dict:
    meta = json.loads((ask_dir / "ask.json").read_text(encoding="utf-8"))
    for field in ("id", "model", "base_env", "base_url", "contract"):
        if not meta.get(field):
            raise ValueError(f"ask.json missing required field {field!r}")
    base_url, model = meta["base_url"], meta["model"]
    family = _family_of(_endpoint(base_url)[1])  # fence at entry
    if execute and key is None:
        # key resolved per ask: a missing base_env fails that ask loud
        key = _api_key(meta["base_env"])
    out_path = OUT_DIR / f"{meta['id']}.md"
    refused_marker = ask_dir / "REFUSED"
    if refused_marker.is_file():
        return {"id": meta["id"], "ok": True,
                "skipped": "REFUSED (terminal; operator edit + marker removal "
                           "required to re-arm)"}
    refusals, refusal_snippet = _refusal_state(meta["id"], family)
    if refusals >= 2:
        _mint_refused_marker(ask_dir, meta["id"], refusal_snippet)
        return {"id": meta["id"], "ok": True,
                "skipped": f"REFUSED (terminal; {refusals} ledger refusals, "
                           "marker minted)"}
    # INFERENCE-BUDGET entry: a terminally burned ask (EMPTY_REASONING
    # marker) never refires the same params (the one-bug law, 2026-10-01).
    done = skip_terminal(ask_dir, meta["id"])
    if done is not None:
        return done
    skip = _landed_skip(meta, ask_dir, out_path)
    if skip is not None:
        return skip
    # the carrier's _system_for is model-agnostic (claritas face + the fixed
    # estate-law block): single-sourced from hermes_burn, not forked.
    # X3-1 A/B knob (BATTERY.md amendment X3-1): system "bare" fires the ask
    # with NO system prefix so the face's per-family value is measurable;
    # any other value fails loud here (fail-closed: no silent arm drift).
    system_mode = meta.get("system")
    if system_mode not in (None, "", "bare"):
        raise ValueError('ask.json "system" must be "bare" or absent, got '
                         f"{system_mode!r}")
    from tools.hermes_burn import _system_for
    body = ("=== CONTRACT ===\n" + meta["contract"]
            + "\n\n=== EVIDENCE ===" + _read_evidence(meta.get("evidence", []))
            + "\n\nProduce the deliverable the CONTRACT demands. Positive AND "
            "negative examples where they clarify. Match the requested shape "
            "exactly.")
    if system_mode == "bare":
        prompt = body
    else:
        prompt = _system_for(model) + "\n\n" + body
    messages = [{"role": "user", "content": prompt}]
    original_user_msg = messages[0]
    turns = []
    result_row = {"id": meta["id"], "model": model, "model_family": family,
                  "ok": True}
    for turn_no in (1, 2):
        if turn_no == 2:
            rev = ask_dir / "revision.md"
            if not meta.get("revision") or not rev.is_file() or not execute:
                break
            # revision turns carry ONLY [original prompt, revision message]:
            # the model re-derives its own draft, no echo
            messages = [original_user_msg,
                        {"role": "user", "content": rev.read_text(encoding="utf-8")}]
        if turn_no == 1 and meta.get("turn2_only"):
            turns.append({"turn": 1, "skipped": "turn2_only"})
            continue
        # preflight runs in dry mode too: offline, and the point of --dry
        _assert_evidence_in_body(meta, messages)
        if not execute:
            turns.append({"turn": turn_no, "dry": True})
            continue
        # INFERENCE-BUDGET: the RIB_MODEL_GATES recipe plans the fire (floor
        # per ask shape, thinking control, forbiddens stripped from the ask's
        # body_extra) and guards the response (fable B1/B5 shape terminal).
        plan = plan_call(model=model, family=family, prompt_chars=len(prompt),
                         requested_max_tokens=meta.get("max_tokens"),
                         ask_extra=meta.get("body_extra"))
        if plan.extra_body:
            resp = _call(model, messages, plan.max_tokens, key, base_url,
                         extra_body=plan.extra_body)
        else:
            resp = _call(model, messages, plan.max_tokens, key, base_url)
        usage = resp.get("usage", {})
        pin, pout = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        cin, cout = PRICING.get(model, (0.0, 0.0))
        cost = pin * cin + pout * cout
        msg = resp["choices"][0]["message"]
        finish_reason = resp["choices"][0].get("finish_reason")
        raw_content = msg.get("content")
        if cause := guard_terminal(ask_dir, meta["id"], plan.recipe_key, finish_reason, usage, raw_content, _bank, model=model, family=family, base_url=base_url, pin=pin, pout=pout, cost=cost):
            raise RuntimeError("EMPTY_REASONING (terminal): " + cause
                               + ". Re-stage with the FAMILY_TABLE recipe or switch family")
        content, chan = raw_content, "content"
        if not content:
            # reasoning_content joins the fallback chain 2026-10-01: z.ai and
            # deepseek return the reasoning channel under reasoning_content
            # (probe receipts in the cheap-grid run), so reading only
            # "reasoning" dropped real provider bytes and raised empty-response
            # on fires the provider had actually answered.
            content, chan = msg.get("reasoning") or msg.get("reasoning_content") or "", "reasoning (content channel empty)"
        if not content:
            refusal = msg.get("refusal")
            if refusal:
                _bank({"ts": _now(), "id": meta["id"], "model": model,
                       "model_family": family, "base_url": base_url,
                       "turn": turn_no, "refused": refusal[:200],
                       "prompt_tokens": pin, "completion_tokens": pout,
                       "cost_usd": round(cost, 4), "ok": False})
                n_refused, last_snippet = _refusal_state(meta["id"], family)
                if n_refused >= 2 and not refused_marker.is_file():
                    _mint_refused_marker(ask_dir, meta["id"], last_snippet)
                raise RuntimeError(f"REFUSED by provider: {refusal[:120]}")
            raise RuntimeError("empty response: both content and reasoning "
                               f"channels empty; usage={usage}")
        messages.append({"role": "assistant", "content": content})
        row = {"ts": _now(), "id": meta["id"], "model": model,
               "model_family": family, "base_url": base_url, "turn": turn_no,
               "prompt_tokens": pin, "completion_tokens": pout,
               "reasoning_tokens": usage.get("completion_tokens_details", {}).get("reasoning_tokens"),
               "channel": chan, "cost_usd": round(cost, 4), "ok": True}
        _bank(row)
        turns.append(row)
        if turn_no == 1:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                f"# {meta['id']} ({model} @ {family}, turn 1, channel: {chan})\n\n{content}\n",
                encoding="utf-8")
        else:
            with open(out_path, "a", encoding="utf-8") as fh:
                fh.write(f"\n\n---\n\n# REVISION (turn 2)\n\n{content}\n")
    result_row["turns"] = turns
    result_row["cost_usd"] = round(sum(t.get("cost_usd", 0) for t in turns), 4)
    return result_row


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="model_garden")
    ap.add_argument("queue", help="dir of ask dirs (each holding ask.json)")
    ap.add_argument("--dry", action="store_true", help="validate asks offline, no calls")
    args = ap.parse_args(argv)
    qroot = Path(args.queue)
    if not qroot.is_dir():
        print(f"USAGE-ERROR: queue dir not found: {qroot}")
        return 2
    ask_dirs = sorted(p for p in qroot.iterdir() if (p / "ask.json").is_file())
    if not ask_dirs:
        print(f"USAGE-ERROR: no ask dirs under {qroot}")
        return 2
    failed = 0
    for d in ask_dirs:
        try:
            row = run_ask(d, execute=not args.dry)
            cost = row.get("cost_usd", 0)
            print(f"{'OK ' if row.get('ok') else 'FAIL'} {row['id']} "
                  f"[{row.get('model_family', '?')}] cost=${cost:.2f}"
                  + (" (skipped)" if row.get("skipped") else ""))
        except Exception as exc:  # noqa: BLE001 fail-loud per ask, continue
            failed += 1
            print(f"FAIL {d.name}: {exc!r}")
    total = 0.0
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                total += json.loads(line).get("cost_usd", 0)
            except json.JSONDecodeError:
                total += 0.0  # torn tail write: counted as zero, not silent
    print(f"MODEL-GARDEN: {'FAIL' if failed else 'PASS'} "
          f"{len(ask_dirs) - failed}/{len(ask_dirs)} asks; ledger total ${total:.2f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
