"""Provider registry: detection, API capability, adapters, manual runbooks.

API capability research (2026-10-25):
  openrouter  API: provisioning key -> POST /api/v1/keys (create), DELETE /api/v1/keys/{hash}.
  xai         API: management key -> POST management-api.x.ai/auth/api-keys/{id}/rotate
              (old secret valid ~24h grace, max 7d); key id via GET api.x.ai/v1/api-key.
  cloudflare  API: PUT /client/v4/user/tokens/{id}/value rolls a token (caller needs
              API Tokens Write); id via GET /user/tokens/verify.
  github      no API to create a PAT (classic or fine-grained); manual. (Revoke of leaked
              tokens via POST /credentials/revoke exists, creation does not.)
  notion, deepseek, nous, huggingface, google AI Studio, groq, zai, x, openai project keys,
  anthropic (admin API can list/disable, not create): manual dashboard rotation.
Adapters run ONLY with --apply plus --confirm <key_id> for that key, at an interactive TTY
(configs/secrets_policy.yaml: non_interactive_always_deny). New values go straight from
the HTTP response into the owner-only store; they are never printed or logged.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Provider:
    name: str
    env_re: str
    value_re: str | None
    dashboard: str
    steps: list[str]
    api: bool = False
    mgmt_env: list[str] = field(default_factory=list)  # env names the adapter needs (names only)


P = [
    Provider("openrouter", r"OPENROUTER|^OR_API", r"^sk-or-", "https://openrouter.ai/settings/keys",
             ["Create key with same label + '-r<date>'", "Paste into store", "Delete old key"],
             api=True, mgmt_env=["OPENROUTER_PROVISIONING_KEY"]),
    Provider("xai", r"^XAI|GROK", r"^xai-", "https://console.x.ai/team/default/api-keys",
             ["API Keys > key > Rotate (or create new)", "Paste into store", "Disable old after grace"],
             api=True, mgmt_env=["XAI_MANAGEMENT_KEY"]),
    Provider("cloudflare", r"CLOUDFLARE|^CF_", None, "https://dash.cloudflare.com/profile/api-tokens",
             ["Token > Roll", "Paste into store"], api=True, mgmt_env=["CLOUDFLARE_TOKENS_ADMIN"]),
    Provider("github", r"GITHUB|^GH_", r"^(ghp_|github_pat_|gho_|ghs_)", "https://github.com/settings/tokens",
             ["Generate new fine-grained token with same scopes/repos", "Paste into store",
              "Delete old token on the same page"]),
    Provider("notion", r"NOTION", r"^(ntn_|secret_)", "https://www.notion.so/profile/integrations",
             ["Open integration > Configuration > Refresh internal integration secret", "Paste into store"]),
    Provider("deepseek", r"DEEPSEEK", None, "https://platform.deepseek.com/api_keys",
             ["Create new API key", "Paste into store", "Delete old key"]),
    Provider("nous", r"NOUS", None, "https://portal.nousresearch.com/api-keys",
             ["Create new API key", "Paste into store", "Delete old key"]),
    Provider("anthropic", r"ANTHROPIC|CLAUDE", r"^sk-ant-", "https://console.anthropic.com/settings/keys",
             ["Create key", "Paste into store", "Disable then delete old key"]),
    Provider("openai", r"OPENAI", r"^sk-(proj-)?[A-Za-z0-9]", "https://platform.openai.com/api-keys",
             ["Create new secret key in same project", "Paste into store", "Revoke old key"]),
    Provider("huggingface", r"^HF_|HUGGING", r"^hf_", "https://huggingface.co/settings/tokens",
             ["Token > Invalidate and refresh", "Paste into store"]),
    Provider("google", r"GEMINI|GOOGLE", r"^AIza", "https://aistudio.google.com/apikey",
             ["Create API key", "Paste into store", "Delete old key"]),
    Provider("groq", r"GROQ", r"^gsk_", "https://console.groq.com/keys",
             ["Create API key", "Paste into store", "Delete old key"]),
    Provider("zai", r"^ZAI|ZHIPU|GLM", None, "https://z.ai/manage-apikey/apikey-list",
             ["Add new API key", "Paste into store", "Delete old key"]),
    Provider("x", r"^X_|TWITTER", None, "https://developer.x.com/en/portal/projects-and-apps",
             ["App > Keys and tokens > Regenerate", "Paste into store", "Re-run OAuth if user tokens"]),
    Provider("telegram", r"TELEGRAM", None, "https://t.me/BotFather",
             ["/revoke in BotFather, pick bot", "Paste new token into store"]),
]
UNKNOWN = Provider("unknown", r"$^", None, "(identify issuing service first)",
                   ["Identify the issuing service from the env name", "Rotate in its dashboard", "Paste into store"])


def classify(name: str, value: str) -> Provider:
    for p in P:
        if p.value_re and re.match(p.value_re, value):
            return p
    for p in P:
        if re.search(p.env_re, name, re.I):
            return p
    return UNKNOWN


def by_name(n: str) -> Provider:
    return next((p for p in P if p.name == n), UNKNOWN)


def mgmt_ready(p: Provider) -> list[str]:
    """Names of missing management credentials (env presence only, no values read)."""
    return [e for e in p.mgmt_env if not os.environ.get(e)]


# ---------------- adapters (only reached from cli --apply path) ----------------

def _http(method: str, url: str, token: str, body: dict | None = None, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read() or b"{}")


def rotate_openrouter(old_value: str, label: str) -> tuple[str, dict]:
    mk = os.environ["OPENROUTER_PROVISIONING_KEY"]
    info = _http("GET", "https://openrouter.ai/api/v1/key", old_value).get("data", {})
    new = _http("POST", "https://openrouter.ai/api/v1/keys", mk, {"name": f"{label}-rot"})
    meta = {"new_hash": new.get("data", {}).get("hash"), "old_label": info.get("label")}
    return new["key"], meta


def revoke_openrouter(key_hash: str) -> None:
    _http("DELETE", f"https://openrouter.ai/api/v1/keys/{key_hash}", os.environ["OPENROUTER_PROVISIONING_KEY"])


def rotate_xai(old_value: str, label: str) -> tuple[str, dict]:
    mk = os.environ["XAI_MANAGEMENT_KEY"]
    kid = _http("GET", "https://api.x.ai/v1/api-key", old_value).get("api_key_id")
    out = _http("POST", f"https://management-api.x.ai/auth/api-keys/{kid}/rotate", mk, {})
    return out["apiKey"], {"api_key_id": kid, "grace": "old secret valid about 24h"}


def rotate_cloudflare(old_value: str, label: str) -> tuple[str, dict]:
    mk = os.environ["CLOUDFLARE_TOKENS_ADMIN"]
    tid = _http("GET", "https://api.cloudflare.com/client/v4/user/tokens/verify", old_value)["result"]["id"]
    out = _http("PUT", f"https://api.cloudflare.com/client/v4/user/tokens/{tid}/value", mk, {})
    return out["result"], {"token_id": tid, "note": "roll invalidates old value immediately"}


ADAPTERS: dict[str, Callable[[str, str], tuple[str, dict]]] = {
    "openrouter": rotate_openrouter, "xai": rotate_xai, "cloudflare": rotate_cloudflare,
}
