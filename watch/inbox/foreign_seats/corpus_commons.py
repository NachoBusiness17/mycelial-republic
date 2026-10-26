#!/usr/bin/env python3
"""tools/sovereign/corpus_commons.py - Estate Invariant Training Commons & Wishlist Manager.

Zero-dependency sovereign tool to:
1. Inspect the 10TB cloud vault training corpus (gdrive_sd / gdrive_nacho).
2. Manage the estate's 'Nice-to-Have' Wishlist with content-addressed pointers (Magnets, ArXiv IDs, Gutenberg IDs, Infohashes).
3. Stream newly requested open-access texts/papers directly into the cloud tiers (zero local NVMe bloat).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE = Path(r"C:\Users\etfag\.zcode\workspace\default")
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))
RCLONE = WORKSPACE / "tools" / "rclone.exe"
SSL_CTX = ssl._create_unverified_context()
COMMONS_DIR = WORKSPACE / "watch" / "inbox" / "foreign_seats"
WISHLIST_FILE = COMMONS_DIR / "ESTATE_WISHLIST_CATALOG.json"


def load_catalog() -> Dict[str, Any]:
    if WISHLIST_FILE.exists():
        with open(WISHLIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"shelves": {}, "updated_at": datetime.now(timezone.utc).isoformat()}


def save_catalog(cat: Dict[str, Any]) -> None:
    WISHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    cat["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2)


def add_item(
    shelf: str,
    title: str,
    author: str,
    handle_type: str,
    handle: str,
    why: str,
    tier: str = "PD",
) -> None:
    cat = load_catalog()
    if shelf not in cat["shelves"]:
        cat["shelves"][shelf] = []

    # Deduplicate
    for item in cat["shelves"][shelf]:
        if item.get("handle") == handle or item.get("title").lower() == title.lower():
            print(f"Item '{title}' already exists on shelf '{shelf}'.")
            return

    new_entry = {
        "title": title,
        "author": author,
        "handle_type": handle_type,  # gutenberg, arxiv, magnet, infohash, url
        "handle": handle,
        "why": why,
        "tier": tier,
        "status": "WISHLIST",  # WISHLIST | FULFILLED
        "added_at": datetime.now(timezone.utc).isoformat(),
        "landed_path": None,
    }
    cat["shelves"][shelf].append(new_entry)
    save_catalog(cat)
    print(f"Added '{title}' by {author} to shelf '{shelf}' [{handle_type}: {handle}].")


def fulfill_stream(shelf: str, handle: str) -> bool:
    """Streams a public-domain Gutenberg book or ArXiv paper directly to cloud vault."""
    cat = load_catalog()
    target_item = None
    for item in cat["shelves"].get(shelf, []):
        if item.get("handle") == handle:
            target_item = item
            break

    if not target_item:
        print(f"Error: item {handle} not found on shelf {shelf}.")
        return False

    url = None
    fname = None
    htype = target_item.get("handle_type")

    if htype == "gutenberg":
        gid = target_item["handle"]
        url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
        slug = "".join(c if c.isalnum() else "_" for c in target_item["title"].lower())[:32]
        fname = f"pg{gid}_{slug}.txt"
    elif htype == "arxiv":
        aid = target_item["handle"]
        url = f"https://arxiv.org/pdf/{aid}.pdf"
        slug = "".join(c if c.isalnum() else "_" for c in target_item["title"].lower())[:32]
        fname = f"arxiv_{aid.replace('.', '_')}_{slug}.pdf"
    elif htype == "url":
        url = target_item["handle"]
        fname = url.split("/")[-1]

    if not url:
        print(f"Streaming not implemented for handle type '{htype}' (requires peer torrent client).")
        return False

    print(f"Streaming '{target_item['title']}' from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 EstateCorpusCommons/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=35.0, context=SSL_CTX) as resp:
            data = resp.read()
    except Exception as e:
        print(f"Fetch failed: {e}")
        return False

    size = len(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"Fetched {size:,} bytes | SHA-256: {digest[:16]}...")

    remote_sd = f"gdrive_sd:corpus/library/{shelf}/{fname}"
    remote_nacho = f"gdrive_nacho:corpus/library/{shelf}/{fname}"

    for rem in [remote_sd, remote_nacho]:
        cmd = [str(RCLONE), "rcat", rem]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate(input=data)
        if p.returncode != 0:
            print(f"Rclone failed to {rem}")
            return False

    print(f"Landed successfully in both 10TB cloud vaults: {fname}")
    target_item["status"] = "FULFILLED"
    target_item["landed_path"] = f"corpus/library/{shelf}/{fname}"
    target_item["bytes"] = size
    target_item["sha256"] = digest
    target_item["fulfilled_at"] = datetime.now(timezone.utc).isoformat()
    save_catalog(cat)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estate Invariant Training Commons Manager")
    parser.add_argument("--list", action="store_true", help="List all shelves and items")
    parser.add_argument("--list-lenses", action="store_true", help="List all secondhand invariant lenses")
    parser.add_argument("--search-magnets", type=str, help="Search Pirate Face P2P network for model/dataset magnets")
    parser.add_argument("--add", action="store_true", help="Add an item to wishlist")
    parser.add_argument("--shelf", type=str, help="Shelf name")
    parser.add_argument("--title", type=str, help="Title of work")
    parser.add_argument("--author", type=str, help="Author name")
    parser.add_argument("--type", type=str, choices=["gutenberg", "arxiv", "magnet", "infohash", "url"], help="Handle type")
    parser.add_argument("--handle", type=str, help="Pointer value (ID, magnet, URL, hash)")
    parser.add_argument("--why", type=str, default="", help="Load-bearing rationale")
    parser.add_argument("--fulfill", action="store_true", help="Stream an item from wishlist to cloud vault")

    args = parser.parse_args()

    if args.list_lenses:
        lens_dir = COMMONS_DIR / "lenses"
        print(f"=== Estate Secondhand Invariant Lenses ({lens_dir}) ===")
        if lens_dir.exists():
            for f in sorted(lens_dir.glob("ESTATE_LENS_*.md")):
                print(f"  * {f.name}")
        else:
            print("  (No lenses directory found)")
        sys.exit(0)

    if args.search_magnets:
        try:
            from tools.sovereign.standin_scrubber import PirateFaceMagnetBridge
            print(f"=== Searching Pirate Face P2P Magnet Index for: '{args.search_magnets}' ===")
            results = PirateFaceMagnetBridge.search_magnets(args.search_magnets)
            for i, r in enumerate(results, 1):
                print(f"\n[{i}] {r.get('name', args.search_magnets)}")
                print(f"    Magnet : {r.get('magnet')}")
                print(f"    Seeders: {r.get('seeders', 'N/A')} | Note: {r.get('note', '')}")
        except Exception as e:
            print(f"Magnet search error: {e}")
        sys.exit(0)

    if args.add:
        if not (args.shelf and args.title and args.author and args.type and args.handle):
            print("Missing required fields for --add.")
            sys.exit(1)
        add_item(args.shelf, args.title, args.author, args.type, args.handle, args.why)
    elif args.fulfill:
        if not (args.shelf and args.handle):
            print("Must specify --shelf and --handle to fulfill.")
            sys.exit(1)
        fulfill_stream(args.shelf, args.handle)
    elif args.list or len(sys.argv) == 1:
        cat = load_catalog()
        print(f"=== Estate Invariant Training Commons & Wishlist (Updated: {cat.get('updated_at')}) ===")
        for shelf, items in cat.get("shelves", {}).items():
            print(f"\n[Shelf: {shelf}] ({len(items)} items)")
            for it in items:
                status_box = "[x]" if it["status"] == "FULFILLED" else "[ ]"
                print(f"  {status_box} {it['title']} by {it['author']} ({it['handle_type']}: {it['handle']})")
                if it.get("why"):
                    print(f"      Why: {it['why']}")
