#!/usr/bin/env python3
"""public_lattice_manifest: the PUBLIC tier, a strict one-way mirror (2026-10-17).

Two Drives, two roles. The PRIVATE vault (local vault -> magbrain: crypt) holds
the whole brain. The PUBLIC drive (`magpublic:`, separate account, not crypt)
serves only the cleaned INVARIANT LATTICE, built from a STRICT ALLOWLIST:

  law_cards.json            core_laws + law-rib heads/amendments derived from
                            memory/rib_boot.json (same fields as the warm
                            mag://warm/laws card)
  chain_v2/tip_v2.json      the v2 chain root (n, root, chain_id, state_hash)
  chain_v2/checkpoints_v2.jsonl   v2 checkpoints (currently unsigned; status
                            field says so)
  verify/verify_knot_v2.py  the stdlib verifier, so anyone can check the root
  modules/<card>            librarian module cards, WHEN they exist
                            (watch/LIBRARY/modules/*.card.json|*.card.md)

Nothing from watch/inbox, memory bodies, knots, chains rows, or anything secret
is eligible: anything not named above is simply never considered.

ONE-WAY LAW
  - SOURCE is the private vault: the newest <vault>/manifests/brain_manifest_*
    and its content-addressed objects, each re-hashed on read (mesh_delta's
    verify-then-serve). The live repo is not read.
  - Every published byte is masked (mag/warm_surface.redact_text: secrets,
    repo path -> <repo>, home paths -> <home>, tailnet IPs) plus any other
    IPv4 / e-mail, then re-scanned with deepseek_direct_runner.redact_lines;
    a file that still trips is excluded (path only).
  - The public drive is WRITE-ONLY from our side. The only rclone verbs this
    module can emit are `copy <local staging> <public remote> --ignore-existing`
    and `check <local staging> <public remote> --one-way` (hash/size compare;
    its output is discarded, only the exit code is kept). Nothing is ever read
    back from public into the brain, and no public content is trusted.
  - NEVER automatic: `build` stages + writes PUBLIC_RELEASE_REVIEW.md; `push`
    requires --approve <public manifest sha> equal to the staged manifest's
    sha, re-hashes every staged file at push time (publish-time re-check) and
    refuses any extra file in the payload.

Reused: bintree_v2.publish_checkpoint's posture (default-off, explicit gate,
never overwrite, atomic write, never runs git), warm_surface.redact_text and
laws() field set, deepseek_direct_runner.redact_lines, mesh_delta's
re-hash-before-serve, brain_replicate.guard()/rclone_bin()/rclone_remotes().

CLI:
  python scripts/public_lattice_manifest.py build
  python scripts/public_lattice_manifest.py push --approve <sha>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import brain_replicate as br  # noqa: E402

SCHEMA = "public_lattice_manifest.v1"
MANIFEST_NAME = "PUBLIC_MANIFEST.json"
REVIEW_NAME = "PUBLIC_RELEASE_REVIEW.md"

_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def mask(text: str) -> str:
    from mag.warm_surface import redact_text

    out = redact_text(text)
    out = _IPV4.sub("<ip>", out)
    return _EMAIL.sub("<email>", out)


def _law_cards(data: bytes) -> bytes:
    rb = json.loads(data.decode("utf-8"))
    ribs = []
    for rib in (rb.get("vault") or {}).get("law_ribs") or []:
        if isinstance(rib, dict):
            ribs.append({"file": rib.get("file"), "law_head": rib.get("law_head"),
                         "law_amendments": rib.get("law_amendments") or [],
                         "amendment_count": rib.get("amendment_count")})
    cards = {"schema": "public_law_cards.v1", "rib_boot_ts": rb.get("ts"),
             "core_laws": rb.get("core_laws") or [], "law_ribs": ribs,
             "note": "amend-never-rewrite: amendments ride after the head"}
    return (json.dumps(cards, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")


def _identity(data: bytes) -> bytes:
    return data


# Code is published VERBATIM or not at all: masking would corrupt it (the warm
# KEY=value mask turns `secret: bytes` into `secret: <redacted>`). A verbatim
# file must already be clean: redaction scan, home/repo path, IPv4, e-mail.
VERBATIM = {"verify/verify_knot_v2.py"}

# Lines worth a human look in the review (not secrets by rule, but identity /
# account / ops detail on a PUBLIC drive). Flag only; the review decides.
_ATTENTION = re.compile(r"(?i)\b(?:accounts?|logged in|login|credential\w*|passw\w*|tokens?|"
                        r"wallet|seed phrase|portproxy|elevat\w+)\b")


def attention_lines(text: str, limit: int = 40) -> list[str]:
    out = []
    for ln in text.splitlines():
        for m in _ATTENTION.finditer(ln):
            a, b = max(0, m.start() - 60), min(len(ln), m.end() + 60)
            out.append(ln[a:b].strip())
            if len(out) >= limit:
                return out
    return out


# brain path -> (public path, transform). STRICT: nothing else is ever eligible.
ALLOW: dict[str, tuple[str, Callable[[bytes], bytes]]] = {
    "memory/rib_boot.json": ("law_cards.json", _law_cards),
    "memory/biography_v2/tip_v2.json": ("chain_v2/tip_v2.json", _identity),
    "memory/biography_v2/checkpoints_v2.jsonl": ("chain_v2/checkpoints_v2.jsonl", _identity),
    "scripts/verify_knot_v2.py": ("verify/verify_knot_v2.py", _identity),
}
MODULE_CARD = re.compile(r"^watch/LIBRARY/modules/([A-Za-z0-9_.-]+\.card\.(?:json|md))$")


def eligible(brain_path: str) -> tuple[str, Callable[[bytes], bytes]] | None:
    if brain_path in ALLOW:
        return ALLOW[brain_path]
    m = MODULE_CARD.fullmatch(brain_path)
    return ("modules/" + m.group(1), _identity) if m else None


def latest_brain_manifest(vault: Path) -> tuple[Path, dict, str]:
    ms = sorted((vault / "manifests").glob("brain_manifest_*.json"))
    if not ms:
        raise SystemExit(f"no brain manifest in {vault}/manifests (run brain_replicate first)")
    raw = ms[-1].read_bytes()
    return ms[-1], json.loads(raw), hashlib.sha256(raw).hexdigest()


def _vault_bytes(vault: Path, sha: str) -> bytes:
    data = br.object_path(vault, sha).read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit(f"vault object {sha[:12]} is corrupt; refusing to publish")
    return data


def canonical(obj: dict) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")


def build(vault: Path, staging_root: Path, *, review_copy: Path | None = None) -> dict[str, Any]:
    from mag.deepseek_direct_runner import redact_lines

    mpath, bman, bsha = latest_brain_manifest(vault)
    files, excluded, staged, flags = [], [], {}, {}
    for f in bman["files"]:
        rule = eligible(f["path"])
        if rule is None:
            continue
        pub_path, transform = rule
        src = _vault_bytes(vault, f["sha256"])
        text = transform(src).decode("utf-8", errors="replace")
        masked = mask(text)
        if pub_path in VERBATIM:
            # code: publish unchanged only if masking finds nothing but known
            # code false positives (the KEY=value pattern); any path / IP /
            # e-mail / scanner hit excludes it
            from mag.warm_surface import _HOME_RE, _root_variants
            dirty = (_HOME_RE.search(text) or _IPV4.search(text) or _EMAIL.search(text)
                     or any(v in text for v in _root_variants()))
            _, hits = redact_lines(text.splitlines())
            if dirty or hits:
                excluded.append(pub_path)
                continue
            masked = text
        _, hits = redact_lines(masked.splitlines())
        if hits:
            excluded.append(pub_path)
            continue
        data = masked.encode("utf-8")
        staged[pub_path] = data
        flags[pub_path] = attention_lines(masked)
        files.append({"path": pub_path, "sha256": hashlib.sha256(data).hexdigest(),
                      "size": len(data), "source_path": f["path"],
                      "source_sha256": f["sha256"],
                      "masked": masked != text, "derived": transform is not _identity,
                      "verbatim": pub_path in VERBATIM})
    manifest = {"schema": SCHEMA, "source_brain_manifest_sha256": bsha,
                "source_brain_manifest": mpath.name, "v2": bman.get("v2"),
                "files": sorted(files, key=lambda x: x["path"]), "excluded": sorted(excluded),
                "law": "one-way mirror: private vault -> public drive; never read back"}
    raw = canonical(manifest)
    sha = hashlib.sha256(raw).hexdigest()
    stage = staging_root / sha
    payload = stage / "payload"
    if not (payload / MANIFEST_NAME).exists():  # same content -> same sha -> already staged
        tmp = staging_root / f".{sha}.building"
        if tmp.exists():
            shutil.rmtree(tmp)  # our own half-built staging only
        for rel, data in staged.items():
            p = tmp / "payload" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        (tmp / "payload" / MANIFEST_NAME).write_bytes(raw)
        tmp.rename(stage)
    review = render_review(manifest, sha, flags)
    rp = stage / REVIEW_NAME
    if not rp.exists():
        rp.write_text(review, encoding="utf-8", newline="\n")
    if review_copy is not None:
        review_copy.write_text(review, encoding="utf-8", newline="\n")
    return {"manifest_sha256": sha, "staging": str(stage), "files": len(files),
            "excluded": manifest["excluded"], "review": str(review_copy or rp)}


def render_review(manifest: dict, sha: str, flags: dict | None = None) -> str:
    rows = "\n".join(
        f"| `{f['path']}` | {f['size']} | `{f['sha256'][:16]}` | `{f['source_path']}` | "
        f"{'yes' if f['masked'] else 'no'} | {'yes' if f['derived'] else 'no'} |"
        for f in manifest["files"])
    exc = "\n".join(f"- `{p}`" for p in manifest["excluded"]) or "- (none)"
    att = []
    for path, lines in sorted((flags or {}).items()):
        att.extend(f"- `{path}`: {ln.replace('|', '/')}" for ln in lines)
    attention = "\n".join(att) or "- (none)"
    v2 = manifest.get("v2") or {}
    return f"""# PUBLIC RELEASE REVIEW

Public manifest sha256: `{sha}`

Built {datetime.now(timezone.utc).isoformat(timespec='seconds')} from private vault manifest
`{manifest['source_brain_manifest']}` (sha256 `{manifest['source_brain_manifest_sha256']}`).
v2 chain root `{v2.get('root')}` at n={v2.get('n')}.

Every file below would be published, and nothing else, to `magpublic:lattice/{sha}/`.
Read them in the staging payload folder next to this file. Nothing is published until
you run:

    python scripts/public_lattice_manifest.py push --approve {sha}

If any byte changes, the sha changes and the old approval stops matching.

| public path | bytes | sha256 (16) | source in brain | masked | derived |
|---|---|---|---|---|---|
{rows}
| `{MANIFEST_NAME}` | (this manifest) | `{sha[:16]}` | n/a | no | yes |

Excluded after masking (redaction scan still tripped; path only):
{exc}

Attention lines (NOT blocked by rule; identity / account / ops detail you may not
want on a public drive; if any should go, say so and the allowlist/transform is
tightened, which changes the sha):
{attention}

One-way law: the public drive is write-only from our side. Push = `rclone copy
--ignore-existing`; check = `rclone check --one-way` (hash compare, output discarded).
Nothing is ever read back from public into the brain.
"""


def push_cmds(rclone: str, payload: Path, remote_dir: str) -> list[list[str]]:
    """The ONLY two commands that ever touch the public remote."""
    return [br.guard([rclone, "copy", str(payload), remote_dir, "--ignore-existing",
                      "--ask-password=false"]),
            br.guard([rclone, "check", str(payload), remote_dir, "--one-way",
                      "--ask-password=false"])]


def recheck(stage: Path, approve: str) -> dict:
    """Publish-time re-check: manifest sha == approve, every file re-hashed, no extras."""
    payload = stage / "payload"
    raw = (payload / MANIFEST_NAME).read_bytes()
    if hashlib.sha256(raw).hexdigest() != approve:
        raise SystemExit("refused: staged manifest sha != --approve")
    m = json.loads(raw)
    want = {f["path"]: f["sha256"] for f in m["files"]}
    have = {p.relative_to(payload).as_posix() for p in payload.rglob("*") if p.is_file()}
    extra = have - set(want) - {MANIFEST_NAME}
    if extra:
        raise SystemExit(f"refused: unlisted files in payload: {sorted(extra)}")
    for rel, sha in want.items():
        if hashlib.sha256((payload / rel).read_bytes()).hexdigest() != sha:
            raise SystemExit(f"refused: {rel} changed since review")
    return m


def push(cfg: dict, approve: str | None, *, staging_root: Path,
         receipts: Path | None = None, runner=None) -> dict[str, Any]:
    if not approve or not re.fullmatch(r"[0-9a-f]{64}", approve):
        raise SystemExit("refused: push needs --approve <64-hex public manifest sha> "
                         "from PUBLIC_RELEASE_REVIEW.md")
    stage = staging_root / approve
    if not (stage / "payload" / MANIFEST_NAME).is_file():
        raise SystemExit("refused: no staged release with that sha (run build first)")
    recheck(stage, approve)
    pub = cfg.get("public") or {}
    remote = str(pub.get("remote") or "")
    result: dict[str, Any] = {"manifest_sha256": approve, "remote": remote}
    rclone = br.rclone_bin()
    if rclone is None:
        result.update(status="skipped", reason="rclone not installed")
    elif remote.split(":", 1)[0] + ":" not in br.rclone_remotes(rclone):
        result.update(status="skipped",
                      reason=f"rclone remote {remote} not configured (docs/BRAIN_HOSTING.md)")
    else:
        dest = f"{remote.rstrip('/')}{pub.get('dest', 'lattice')}/{approve}"
        run = runner or br._run
        copy_cmd, check_cmd = push_cmds(rclone, stage / "payload", dest)
        c = run(copy_cmd, 7200)
        k = run(check_cmd, 7200) if c.returncode == 0 else None
        result.update(status="ok" if c.returncode == 0 else "failed", dest=dest,
                      copy_exit=c.returncode,
                      verify={"pass": bool(k is not None and k.returncode == 0),
                              "method": "rclone check --one-way (hash only, output discarded)"})
    rdir = receipts or br.RECEIPTS
    rdir.mkdir(parents=True, exist_ok=True)
    rp = rdir / f"public_{br._utc()}.json"
    with open(rp, "x", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"schema": "public_push_receipt.v1", **result}, indent=1) + "\n")
    result["receipt_path"] = str(rp)
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="public_lattice_manifest", description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["build", "push"])
    ap.add_argument("--approve", help="public manifest sha Nacho reviewed (push only)")
    ap.add_argument("--config", type=Path)
    a = ap.parse_args(argv)
    cfg = br.load_config(a.config)
    vault = Path(next(t for t in cfg["targets"] if t.get("kind") == "vault")["path"])
    staging = Path((cfg.get("public") or {}).get("staging") or (vault.parent / "public_staging"))
    staging.mkdir(parents=True, exist_ok=True)
    if a.cmd == "build":
        out = build(vault, staging, review_copy=ROOT / REVIEW_NAME)
    else:
        out = push(cfg, a.approve, staging_root=staging)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
