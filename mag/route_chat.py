"""route_chat - the ONE front door for model calls from estate tools.

Standing correction (2026-10-03, operator: "you have a pet model harness and
never use it by default"): every tool this day hand-rolled its own urllib
path - hermes_burn fence, ds_workhorse lane, grok_burn xAI client, tavern and
dungeon carriers - while the house routing brain (configs/providers.yaml
lanes, mag.model_pick, mag.cost_truth dormant gate) sat unused as policy
without a call path. This module IS the call path. New tools call THIS; a
bespoke carrier needs a written reason.

What it does per call:
1. resolve lane + model: explicit lane/model wins; else mag.model_pick
   recommends by goal; else the lane's default_model
2. dormant gate: mag.cost_truth's B2-133 rule - a dormant lane refuses
   without an operator GO flag
3. endpoint fence (the Mimosa rulings): https + allowlisted host from the
   lane config, resolved IPs refused private/loopback/link-local/reserved/
   multicast; the connection is then pinned to the fence-validated IPs
   (a08-rails-laws r7: urlopen re-resolves DNS, and check-vs-connect
   disagreement was a TOCTOU window)
4. call openai_compat chat/completions with fail-loud errors
5. bank usage to memory/runs/route_chat/usage.jsonl (driving-ladder law);
   exceptions bank an ok:false error row too (a08-rails-laws r10:
   everything-banks held only for parsed responses)

Usage:
    from mag.route_chat import route_chat
    text = route_chat("summarize this receipt", goal="mechanical fold")
    text = route_chat(msgs, lane="xai", model="grok-4.7")
"""
from __future__ import annotations

import ipaddress
import json
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
USAGE = ROOT / "memory" / "runs" / "route_chat" / "usage.jsonl"


def _load_lanes() -> dict:
    import yaml  # noqa: PLC0415 - lazy: only imported on calls
    cfg = (ROOT / "configs" / "providers.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(cfg) or {}
    return data.get("providers") or {}


def _keys_for(lane: dict) -> list[tuple[str, str]]:
    """The lane's key chain, in order (the nous lane law: both keys as one
    failover chain - key 1 can 402 while key 2 carries the credits)."""
    import os  # noqa: PLC0415
    out = []
    for env in lane.get("api_key_envs") or [lane.get("api_key_env")]:
        if not env:
            continue
        if os.environ.get(env):
            out.append((env, os.environ[env]))
            continue
        for line in (ROOT / ".env").read_text(encoding="utf-8",
                                              errors="replace").splitlines():
            if line.strip().startswith(env + "="):
                out.append((env, line.split("=", 1)[1].strip().strip('"').strip("'")))
                break
    return out


def _fence(base_url: str, host: str) -> set[str]:
    """Refuse non-allowlisted URLs and non-public resolutions; return the
    set of validated public IPs so the connect can be pinned to them."""
    parsed = urllib.parse.urlsplit(base_url)
    if parsed.scheme != "https" or parsed.hostname != host:
        raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
    safe: set[str] = set()
    for info in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(f"endpoint fence: {host} resolves to non-public {ip}")
        safe.add(info[4][0])
    return safe


def _pin_dns(host: str, safe: set[str]):
    """Close the fence TOCTOU (a08-rails-laws r7): _fence validates the IPs
    the lane host resolves to, but urlopen re-resolves the same host at
    connect time, so a DNS rebinding in that window passes the fence and
    connects elsewhere. While pinned, getaddrinfo answers this host ONLY
    with the fence-validated addresses; a re-resolution that disagrees is
    refused. Evidence: the fence resolved at route_chat.py:75 while urlopen
    re-resolved at :145 (185-line tree). Fix, not a guard branch: the check
    and the connect now consume the same address set."""
    real_getaddrinfo = socket.getaddrinfo

    def pinned(hostname, port, *args, **kwargs):
        infos = real_getaddrinfo(hostname, port, *args, **kwargs)
        if hostname == host:
            infos = [i for i in infos if i[4][0] in safe]
            if not infos:
                raise RuntimeError(
                    f"endpoint fence: {host} re-resolved outside the "
                    "fence-validated address set (TOCTOU pin)")
        return infos

    return pinned


def _thinking_forbidden(model: str) -> bool:
    """True when the model's inference_budget recipe carries a MEASURED
    rejection of the thinking key (e.g. qwen3.7-flash 400s on any reasoning
    param). This is D3 falsifier (1) in code: capability-scoped off only
    where a 400 was measured; every other lane gets the explicit key."""
    try:
        from mag.inference_budget import recipe_for  # noqa: PLC0415
    except ImportError:
        return False
    return "thinking" in recipe_for(model=model or "").forbidden_keys


# D3 2026-10-04: thinking rides only design asks with real headroom; the
# founding failure spent 15998 of a 16000 completion cap on reasoning
# (memory/runs/hermes_burn/usage.jsonl line 1151), so anything smaller is
# a hollow-judgment burn in the making.
DESIGN_MIN_TOKENS = 32_000


def wire_thinking(body_obj: dict, depth: str, model: str, *,
                  attested: bool = False, max_tokens: int = 0) -> dict:
    """D3 ruling 2026-10-04 (watch/inbox/ractor_engine/
    2026-10-04-parked-decisions/SYNTHESIS.md:11-17): depth=mechanical sends
    thinking:{type:disabled} UNCONDITIONALLY, regardless of the lane's
    disable_thinking flag - omission is a MEASURED ON state (d4 probe,
    watch/inbox/go_wave_20261004/d4_thinking_probe.md:53-62: omitted key =
    18 reasoning tokens on a one-word ask, disabled = 0), and the founding
    $0.464 burn rode a lane with no flag at all (usage.jsonl:1151-1152).
    depth=design is the ONLY ON path and raises unless the lane attests
    thinking-key capability (providers.yaml disable_thinking, demoted from
    enforcement to attestation by the same ruling) AND max_tokens >=
    DESIGN_MIN_TOKENS. Pure function so the payload and the refusal can be
    inspected offline; a refusal raises before any network byte and banks
    an error row through route_chat's exception path."""
    if depth == "mechanical":
        if not _thinking_forbidden(model):
            body_obj["thinking"] = {"type": "disabled"}
    elif depth == "design":
        if not attested:
            raise RuntimeError(
                "route_chat: depth=design refused - lane carries no "
                "thinking capability attestation (providers.yaml "
                "disable_thinking); D3 2026-10-04, SYNTHESIS.md:11-17")
        if max_tokens < DESIGN_MIN_TOKENS:
            raise RuntimeError(
                f"route_chat: depth=design refused at max_tokens={max_tokens}"
                f" - thinking needs >= {DESIGN_MIN_TOKENS} headroom (the"
                " founding burn spent 15998 of 16000 on reasoning,"
                " usage.jsonl:1151)")
        body_obj["thinking"] = {"type": "enabled"}
    return body_obj


def _bank(row: dict) -> None:
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def route_chat(prompt, *, goal: str = "", lane: str | None = None,
               model: str | None = None, max_tokens: int = 4000,
               retries: int = 1, operator_go: bool = False,
               depth: str = "mechanical", body_extra: dict | None = None) -> str:
    """One front door. prompt = str or openai messages list.

    depth: 'mechanical' (default) sends thinking:{type:disabled} on the
    wire for EVERY lane - omission is a measured ON state (d4 probe
    2026-10-04), so the carrier never relies on it; 'design' is the only
    thinking-ON path and refuses without lane capability attestation
    (providers.yaml disable_thinking) or below 32000 max_tokens of
    headroom. Sacred-cow probe 2026-10-03, claim SCOPED
    (a06-sacred-cow#0/#3): arm 1 (cow- ids, 4 asks) 4/4 complete with zero
    AH10 failure modes, but arm 2 (cow2- ids, 10 asks) banked 2/10
    ZERO-CONTENT rows at exactly the 16000-token cap, so the earlier
    "zero AH10 failure modes" headline was arm-1-only and "16K+" is not a
    safe design budget (7/14 probe rows pinned at or over the 16K cap).
    Budget accordingly: reasoning burns max_tokens; design asks need 32K+
    or a smaller ask. Any other depth string raises ValueError."""
    if depth not in ("mechanical", "design"):
        # a06-sacred-cow#3: depth had no enum validation - anything but
        # "design" silently rode mechanical, so a typo'd depth read as law.
        raise ValueError(
            f"route_chat: depth must be 'mechanical' or 'design', got {depth!r}")
    try:
        return _route(prompt, goal=goal, lane=lane, model=model,
                      max_tokens=max_tokens, retries=retries,
                      operator_go=operator_go, depth=depth,
                      body_extra=body_extra)
    except Exception as exc:  # noqa: BLE001 - re-raised below; the row is the point
        # Exception-path ledger row (a08-rails-laws r10, the everything-banks
        # law): calls dying on the fence, dormant gate, missing keys,
        # timeouts or all-keys-failed used to land NO row - inspect.getsource
        # over the 185-line tree showed _bank absent from every except path,
        # thinning everything-banks at the front door (contrast:
        # tools/ds_workhorse.py banks __ERROR__ rows). The raise re-fires
        # after the row lands; failures are visible, not swallowed.
        _bank({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "lane": lane, "model": model, "goal": goal[:80],
               "prompt_tokens": 0, "completion_tokens": 0,
               "ok": False, "error": type(exc).__name__,
               "detail": str(exc)[:200]})
        raise


def _route(prompt, *, goal: str, lane: str | None, model: str | None,
           max_tokens: int, retries: int, operator_go: bool,
           depth: str, body_extra: dict | None) -> str:
    """The unwrapped call path; route_chat wraps this with the enum check
    and the exception-path ledger row."""
    lanes = _load_lanes()
    if lane is None:
        try:
            from mag.model_pick import recommend_model  # noqa: PLC0415
            rec = recommend_model(goal or "general")
            model = rec.get("model") or model
        except Exception as exc:  # routing brain unavailable: caller must name lane+model
            # 2026-10-04 ratchet: silent except-pass flagged; the fallback's
            # contract is the RuntimeError below, but the reason it fired
            # belongs in the ledger row the caller banks.
            sys.stderr.write(f"route_chat: model_pick unavailable: {exc}\n")
        if lane is None or model is None:
            raise RuntimeError("route_chat: no lane given and model_pick "
                               "could not resolve one; pass lane=/model=")
    lane_cfg = lanes.get(lane)
    if lane_cfg is None:
        raise RuntimeError(f"route_chat: unknown lane {lane}")
    if lane_cfg.get("dormant") and not operator_go:
        raise RuntimeError(f"lane {lane} is DORMANT (B2-133 gate); "
                           "operator GO required")
    model = model or lane_cfg.get("default_model")
    if not model:
        raise RuntimeError(f"route_chat: no model for lane {lane}")
    base = lane_cfg["base_url"].rstrip("/")
    host = urllib.parse.urlsplit(base).hostname
    safe = _fence(base, host)
    keys = _keys_for(lane_cfg)
    if not keys:
        raise RuntimeError(f"route_chat: no keys for lane {lane}")
    messages = (prompt if isinstance(prompt, list)
                else [{"role": "user", "content": prompt}])
    body_obj: dict = {"model": model, "messages": messages,
                      "max_tokens": max_tokens, "temperature": 0.3,
                      "stream": False}
    if lane_cfg.get("use_max_completion_tokens"):
        body_obj["max_completion_tokens"] = body_obj.pop("max_tokens")
    # a06-sacred-cow#3 + a08-rails-laws r5 wired the lane flag; D3 (10-04)
    # removed the lane-config condition: the founding $0.464 burn rode a
    # lane with no flag. providers.yaml disable_thinking is demoted to
    # design-depth capability attestation (passed below) and is never read
    # on mechanical. A lane that rejects the key 400s loudly and banks an
    # error row.
    wire_thinking(body_obj, depth, model,
                  attested=bool(lane_cfg.get("disable_thinking")),
                  max_tokens=max_tokens)
    if body_extra:
        body_obj.update(body_extra)
    body = json.dumps(body_obj).encode()
    url = f"{base}/chat/completions"
    real_getaddrinfo = socket.getaddrinfo
    socket.getaddrinfo = _pin_dns(host, safe)
    try:
        last = None
        for env, key in keys:  # the lane's failover chain, in order
            for attempt in range(retries + 1):
                req = urllib.request.Request(url, data=body, method="POST",
                                             headers={"Authorization": "Bearer " + key,
                                                      "Content-Type": "application/json"})
                try:
                    with urllib.request.urlopen(req, timeout=900) as r:
                        resp = json.loads(r.read())
                    msg = resp["choices"][0]["message"]
                    # a06-sacred-cow#3: the fallback key was "reasoning", a
                    # dead name - the openai_compat vendor field is
                    # "reasoning_content", so the fallback could never fire.
                    content = (msg.get("content")
                               or msg.get("reasoning_content") or "")
                    usage = resp.get("usage", {}) or {}
                    finish = resp["choices"][0].get("finish_reason") or ""
                    # D3 closed loop: the off state is verified from the
                    # response (reasoning_tokens), not assumed from the request
                    rt = ((usage.get("completion_tokens_details") or {})
                          .get("reasoning_tokens"))
                    # RACTOR MOVE 1 (2026-10-03): the substance gate. A row whose
                    # content is hollow (<=1 char) banks ok=false with its finish
                    # reason - silent-green rows made every downstream meter lie.
                    ok = len(content.strip()) > 1
                    _bank({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "lane": lane, "model": model, "goal": goal[:80],
                           "key_env": env,
                           "prompt_tokens": usage.get("prompt_tokens", 0),
                           "completion_tokens": usage.get("completion_tokens", 0),
                           "content_chars": len(content.strip()),
                           "finish_reason": finish,
                           "depth": depth,
                           "thinking_sent": (body_obj.get("thinking") or {}).get("type"),
                           "reasoning_tokens": rt,
                           "ok": ok})
                    if not content:
                        raise RuntimeError("empty content and reasoning channels "
                                           f"(finish={finish})")
                    return content
                except urllib.error.HTTPError as exc:
                    last = exc
                    if exc.code in (401, 402, 403):
                        break  # this key is dead on this lane: fail over to the next
                    if attempt < retries:
                        time.sleep(15)
                except (urllib.error.URLError, TimeoutError,
                        json.JSONDecodeError, KeyError, RuntimeError) as exc:
                    last = exc
                    if attempt < retries:
                        time.sleep(15)
        raise RuntimeError(f"route_chat {lane}/{model} failed on all "
                           f"{len(keys)} key(s): {last!r}")
    finally:
        socket.getaddrinfo = real_getaddrinfo


if __name__ == "__main__":
    print(route_chat(sys.argv[1] if len(sys.argv) > 1 else "reply with the word ack",
                     lane="xai", model="grok-3-mini", max_tokens=16))
