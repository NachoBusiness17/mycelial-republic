# ESTATE INVARIANT TRAINING COMMONS & WISHLIST

**Date:** 2026-10-22  
**Vault Endpoints:** `gdrive_sd:corpus/` & `gdrive_nacho:corpus/` (Combined 10.002 TiB total | 9.907 TiB free capacity)  
**Catalog Format:** [`ESTATE_WISHLIST_CATALOG.json`](./ESTATE_WISHLIST_CATALOG.json)  
**Sovereign Manager CLI:** [`tools/sovereign/corpus_commons.py`](../../tools/sovereign/corpus_commons.py)  

---

## 1. The Architectural Thesis: Source Materials as Invariant Anchors

> *"What better invariants than the source materials that are open source, and pointers to the ones that we need?"*

Model weights degrade across training epochs, frameworks deprecate across minor versions, and cloud APIs revoke access. The only true ground-truth invariants of an intelligent system are:
1. **The Primary Source Texts:** The foundational writings of human thought—philosophy, mathematics, military statecraft, cybernetics, and speculative fiction.
2. **Content-Addressed References:** Cryptographic hashes (SHA-256, BitTorrent infohashes, Magnet URIs, Gutenberg IDs, ArXiv IDs) that identify data by *what it is*, not *where it lives*.

The estate’s 10TB dual Google Drive cloud tiers (`gdrive_sd:` and `gdrive_nacho:`) serve as the **Sovereign Training Commons**. By using zero-disk streaming (`rclone rcat`), edge nodes like `bob` (with 17GB local NVMe headroom) can stream gigabytes of training corpora directly into the cloud without touching local disk.

---

## 2. Live Landed Holdings (Verified in 10TB Dual Cloud Vaults)

These items are fully landed, SHA-256 verified, and stored across both `gdrive_sd:` and `gdrive_nacho:`:

### Shelf: `corpus/papers/deltanet/` (Recurrent & Linear Attention Foundations)
- `arxiv_2102_11174_linear_transformers_delta_rule.pdf` (Schlag et al.) — Original associative delta-rule linear recurrence.
- `arxiv_2307_08621_retnet_retentive_network.pdf` (Sun et al.) — RetNet: Recurrent retention mechanism with explicit decay.
- `arxiv_2404_05892_rwkv7_eagle_and_finch.pdf` (Peng et al.) — RWKV-7 Goose architecture with matrix-valued state.
- `arxiv_2405_21060_state_space_duality_mamba2.pdf` (Dao & Gu) — State Space Duality unifying linear attention and continuous SSMs.

### Shelf: `corpus/library/military_concentric_statecraft/`
- `pg132_the_art_of_war.txt` (Sun Tzu, trans. Lionel Giles; 342 KB, SHA-256: `2301ae1ce2087538...`).
- Historical Siege & Fortification Tranche:
  - PG #41168: *The Siege of Norwich Castle* (M. M. Blake; 786 KB)
  - PG #47197: *Sevastopol* (Leo Tolstoy; 340 KB)
  - PG #60518: *The Defense of Plevna 1877* (William V. Herbert; 1.2 MB)
  - PG #59253: *The Siege of Derry* (John Graham; 824 KB)

### Shelf: `corpus/library/scifi_cybernetics_speculative/`
- `pg19208_star_maker.txt` (Olaf Stapledon; 315 KB, SHA-256: `607d52250b9da7ea...`).

---

## 3. The "Nice-to-Have" & Wishlist Catalog

This catalog is designed for all seats (`foste`, `bob`, `pixel`, `t90`) and peer collaborators to inspect, extend, and fulfill:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ESTATE WISHLIST & POINTER REGISTRY                               │
├───────────────────────────────┬──────────────────────┬─────────────┬─────────────┬───────────────┤
│ Title                         │ Author / Source      │ Handle Type │ Identifier  │ Status        │
├───────────────────────────────┼──────────────────────┼─────────────┼─────────────┼───────────────┤
│ [x] Linear Transformers Delta │ Schlag et al.        │ arxiv       │ 2102.11174  │ FULFILLED     │
│ [x] Retentive Network (RetNet)│ Sun et al.           │ arxiv       │ 2307.08621  │ FULFILLED     │
│ [x] RWKV-7 (Eagle & Finch)    │ Peng et al.          │ arxiv       │ 2404.05892  │ FULFILLED     │
│ [x] Mamba-2 (State Space Dual)│ Dao & Gu             │ arxiv       │ 2405.21060  │ FULFILLED     │
│ [x] The Art of War            │ Sun Tzu              │ gutenberg   │ 132         │ FULFILLED     │
│ [x] Star Maker                │ Olaf Stapledon       │ gutenberg   │ 19208       │ FULFILLED     │
├───────────────────────────────┼──────────────────────┼─────────────┼─────────────┼───────────────┤
│ [ ] On War                    │ Carl von Clausewitz  │ gutenberg   │ 1946        │ WISHLIST      │
│ [ ] Annals of a Fortress      │ Viollet-le-Duc       │ gutenberg   │ 48473       │ WISHLIST      │
│ [ ] The Muqaddimah            │ Ibn Khaldun          │ url         │ archive.org │ POINTER       │
│ [ ] R.U.R. (Universal Robots) │ Karel Capek          │ gutenberg   │ 59112       │ WISHLIST      │
│ [ ] The Time Machine          │ H.G. Wells           │ gutenberg   │ 35          │ WISHLIST      │
│ [ ] The Diamond Age           │ Neal Stephenson      │ isbn        │ 0553380965  │ DEBT-POINTER  │
│ [ ] Cybernetics               │ Norbert Wiener       │ url         │ archive.org │ POINTER       │
│ [ ] Experimental Researches   │ Michael Faraday      │ gutenberg   │ 14986       │ WISHLIST      │
│ [ ] Origin of Species         │ Charles Darwin       │ gutenberg   │ 1228        │ WISHLIST      │
│ [ ] Homo Ludens               │ Johan Huizinga       │ url         │ archive.org │ POINTER       │
│ [ ] The Grasshopper           │ Bernard Suits        │ url         │ archive.org │ POINTER       │
├───────────────────────────────┼──────────────────────┼─────────────┼─────────────┼───────────────┤
│ [ ] Gutenberg Complete Bulk   │ Gutenberg Consortium │ magnet      │ urn:btih:...│ TORRENT       │
│ [ ] Standard Ebooks EPUB Bulk │ Standard Ebooks Team │ url         │ github/se   │ POINTER       │
│ [ ] Qwen3.8-Flash-Next Weights│ Alibaba / Qwen       │ url/hf      │ Qwen/Flash  │ WEIGHTS       │
└───────────────────────────────┴──────────────────────┴─────────────┴─────────────┴───────────────┘
```

---

## 4. Peer Contribution Protocol: How to Add & Fulfill

Any seat or human operator can interact with the commons using [`tools/sovereign/corpus_commons.py`](../../tools/sovereign/corpus_commons.py):

### 1. View the Registry
```bash
python tools/sovereign/corpus_commons.py --list
```

### 2. Add an Item or Pointer
```bash
python tools/sovereign/corpus_commons.py --add \
    --shelf scifi_cybernetics_speculative \
    --title "Last and First Men" \
    --author "Olaf Stapledon" \
    --type gutenberg \
    --handle "gutenberg_aus_0601101" \
    --why "History of future humanity over two billion years."
```

### 3. Fulfill and Stream Directly into the 10TB Cloud Vault
```bash
python tools/sovereign/corpus_commons.py --fulfill \
    --shelf military_concentric_statecraft \
    --handle 1946
```
*(Fetches in-memory, verifies SHA-256, and pipes directly into `gdrive_sd:` and `gdrive_nacho:` with zero local NVMe disk bloat.)*

---

## 5. Torrent & Distributed P2P Federation

For datasets too large for standard HTTP fetching (e.g. the 70,000-book Project Gutenberg dump or model weights), the catalog preserves **Magnet URIs and Torrent infohashes**. 

Any node with available external storage or seeding capability can claim the torrent pointer, pull the tranche, verify the SHA-256 root manifest, and push it into the estate's cloud tiers. The catalog remains the single source of truth across all worldlines.
