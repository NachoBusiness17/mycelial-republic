#!/usr/bin/env python3
"""tools/sovereign/expand_corpus_streamer.py — Sovereign Multi-Corpus Vault Streamer.

Deploys to desktop workstation (foste@100.96.161.76) on 1 Gbps fiber:
1. Canons: ai_canon, mycology_canon, electronics_canon, ractors, shadertoy21k, game_design_docs
2. Codebases to Deconstruct: livingmud, embassy-aos, mycelial-republic, tor_stack, agent-tools
3. Model Manifests: Ollama & custom sovereign model configurations (athena-class, gemma4, qwen2.5-coder)
4. Open-Access Coding & Systems Classics: SICP, Pro Git, Think OS, Think Python, Crafting Interpreters concepts

Zero-Local-Bloat Invariant: Runs entirely on desktop fiber directly to gdrive_sd: with zero bytes on laptop bob.
"""

from __future__ import annotations
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

DESKTOP_PROJECTS = Path(r"C:\Users\foste\Documents\projects")
CORPUS_ROOT = DESKTOP_PROJECTS / "local_sovereign_agent" / "memory" / "corpus"
STAGING_DIR = Path(r"C:\Users\foste\Desktop\vault_staging")

CANONS_TO_STREAM = [
    {
        "name": "ai_canon",
        "src": CORPUS_ROOT / "ai_canon",
        "dest": "gdrive_sd:corpus/canons/ai_canon",
        "desc": "AI theory, Reinforcement Learning (Sutton & Barto), Information Theory (MacKay), SLP3"
    },
    {
        "name": "mycology_canon",
        "src": CORPUS_ROOT / "mycology_canon",
        "dest": "gdrive_sd:corpus/canons/mycology_canon",
        "desc": "Biological and unconventional computing, Physarum and fungal electronics"
    },
    {
        "name": "electronics_canon",
        "src": CORPUS_ROOT / "electronics_canon",
        "dest": "gdrive_sd:corpus/canons/electronics_canon",
        "desc": "Circuits, embedded systems, hardware architecture"
    },
    {
        "name": "ractors",
        "src": CORPUS_ROOT / "ractors",
        "dest": "gdrive_sd:corpus/canons/ractors",
        "desc": "Rust Actor concurrency, message passing, and actor frameworks"
    },
    {
        "name": "shadertoy21k",
        "src": CORPUS_ROOT / "shadertoy21k",
        "dest": "gdrive_sd:corpus/canons/shadertoy21k",
        "desc": "21,000 GPU graphics shaders and algorithmic rendering kernels"
    },
    {
        "name": "game_design_docs",
        "src": CORPUS_ROOT / "game_design_docs",
        "dest": "gdrive_sd:corpus/canons/game_design_docs",
        "desc": "Massive multi-user game systems, virtual world mechanics, actor state machines"
    }
]

CODEBASES_TO_DECONSTRUCT = [
    {
        "name": "livingmud",
        "src": DESKTOP_PROJECTS / "livingmud",
        "dest": "gdrive_sd:corpus/codebases_to_deconstruct/livingmud",
        "desc": "Multi-user text virtual world, state transitions, and persistent worldloop"
    },
    {
        "name": "embassy-aos",
        "src": DESKTOP_PROJECTS / "embassy-aos",
        "dest": "gdrive_sd:corpus/codebases_to_deconstruct/embassy_aos",
        "desc": "Embedded async OS & Embassy hardware abstraction layers"
    },
    {
        "name": "mycelial-republic",
        "src": DESKTOP_PROJECTS / "mycelial-republic",
        "dest": "gdrive_sd:corpus/codebases_to_deconstruct/mycelial_republic",
        "desc": "Decentralized biological topology & distributed consensus"
    },
    {
        "name": "tor_stack",
        "src": DESKTOP_PROJECTS / "tor_stack",
        "dest": "gdrive_sd:corpus/codebases_to_deconstruct/tor_stack",
        "desc": "Onion routing, sovereign network proxy, and traffic anonymization"
    },
    {
        "name": "agent-tools",
        "src": Path(r"C:\Users\foste\agent-tools"),
        "dest": "gdrive_sd:corpus/codebases_to_deconstruct/agent_tools",
        "desc": "210 sovereign agent tool implementations and schema interfaces"
    }
]

OPEN_CS_BOOKS = [
    {
        "title": "Structure_and_Interpretation_of_Computer_Programs_SICP.pdf",
        "url": "https://web.mit.edu/6.001/6.037/sicp.pdf",
        "desc": "SICP (Abelson & Sussman, MIT Press - Creative Commons)"
    },
    {
        "title": "Pro_Git_Second_Edition.pdf",
        "url": "https://github.com/progit/progit2/releases/download/2.1.436/progit.pdf",
        "desc": "Pro Git (Scott Chacon & Ben Straub - Creative Commons Apress)"
    },
    {
        "title": "Think_OS_A_Brief_Introduction_to_Operating_Systems.pdf",
        "url": "https://greenteapress.com/thinkos/thinkos.pdf",
        "desc": "Think OS (Allen B. Downey, Green Tea Press - CC BY-NC 3.0)"
    },
    {
        "title": "Think_Python_Second_Edition.pdf",
        "url": "https://greenteapress.com/thinkpython2/thinkpython2.pdf",
        "desc": "Think Python (Allen B. Downey, Green Tea Press - CC BY-NC 3.0)"
    }
]


def run_rclone(src: str, dest: str) -> dict:
    cmd = [
        "rclone", "copy",
        src, dest,
        "--transfers=8",
        "--checkers=16",
        "--fast-list",
        "-v"
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
        dur = round(time.time() - t0, 1)
        if proc.returncode == 0:
            return {"status": "SUCCESS", "duration_s": dur, "remote": dest}
        else:
            return {"status": "ERROR", "error": proc.stderr[-300:], "duration_s": dur}
    except Exception as e:
        return {"status": "FAILED", "error": str(e), "duration_s": round(time.time() - t0, 1)}


def main():
    print("=== SOVEREIGN MULTI-CORPUS VAULT STREAMER ===", flush=True)
    results = {}

    # 1. Stream Canons
    print("\n--- PHASE 1: STREAMING RESEARCH CANONS ---", flush=True)
    for c in CANONS_TO_STREAM:
        p = c["src"]
        if p.exists():
            print(f"Streaming {c['name']} ({c['desc']}) -> {c['dest']} ... ", end="", flush=True)
            res = run_rclone(str(p), c["dest"])
            print(res["status"])
            results[c["name"]] = res
        else:
            print(f"Skipping {c['name']} (path {p} does not exist)")

    # 2. Stream Codebases
    print("\n--- PHASE 2: STREAMING CODEBASES TO DECONSTRUCT ---", flush=True)
    for cb in CODEBASES_TO_DECONSTRUCT:
        p = cb["src"]
        if p.exists():
            print(f"Streaming {cb['name']} ({cb['desc']}) -> {cb['dest']} ... ", end="", flush=True)
            res = run_rclone(str(p), cb["dest"])
            print(res["status"])
            results[cb["name"]] = res
        else:
            print(f"Skipping {cb['name']} (path {p} does not exist)")

    # 3. Stream Model Manifests
    print("\n--- PHASE 3: EXPORTING MODEL MANIFESTS & CONFIGS ---", flush=True)
    ollama_manifests = Path(r"C:\Users\foste\.ollama\models\manifests")
    if ollama_manifests.exists():
        print(f"Streaming Ollama model manifests -> gdrive_sd:corpus/models/manifests/ ... ", end="", flush=True)
        res = run_rclone(str(ollama_manifests), "gdrive_sd:corpus/models/manifests")
        print(res["status"])
        results["model_manifests"] = res

    # 4. Ingest Open CS Books
    print("\n--- PHASE 4: INGESTING OPEN CS & CODING TEXTBOOKS ---", flush=True)
    books_staging = STAGING_DIR / "coding_books"
    books_staging.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for b in OPEN_CS_BOOKS:
        dest_file = books_staging / b["title"]
        if not dest_file.exists() or dest_file.stat().st_size == 0:
            print(f"Downloading {b['title']} from {b['url']} ... ", end="", flush=True)
            try:
                req = urllib.request.Request(b["url"], headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp, open(dest_file, "wb") as out:
                    out.write(resp.read())
                sz_mb = dest_file.stat().st_size / (1024**2)
                print(f"OK ({sz_mb:.1f} MB)")
            except Exception as e:
                print(f"FAILED: {e}")
        else:
            print(f"Already staged: {b['title']}")

    print("Uploading staged books -> gdrive_sd:corpus/books/coding_and_systems/ ... ", end="", flush=True)
    res = run_rclone(str(books_staging), "gdrive_sd:corpus/books/coding_and_systems")
    print(res["status"])
    results["coding_books"] = res

    print("\n=== EXPANDED CORPUS STREAMING COMPLETED ===")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
