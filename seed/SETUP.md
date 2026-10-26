# SETUP — what you need before FIRST_BOOT

- **Python 3.9+** (`python --version`). Everything runs on the standard library.
- **Optional:** `pip install matplotlib` — only for the smith chart's PNG plot.
  Without it, the chart prints its console meter and skips the plot. Nothing needs the network to boot.
- **A `.env` file (optional):** put provider keys here as `NAME=value` lines; the engines
  also read real environment variables. Declare every key you use in `configs/keys.json`
  (a template entry is there; copy its shape). The audit (`python engines/key_law.py --audit`)
  fails loud on any key that is live but undeclared — that is the design.
- **Verify the package first:** `python verify_seal.py` (step 0 of FIRST_BOOT) — and on
  Linux/macOS `sha256sum -c MANIFEST.sha256` works too.

Windows: all commands are the same; use `py` or `python` as you have it.
