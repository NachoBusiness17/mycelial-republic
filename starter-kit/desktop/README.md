# starter kit desk (Electron v0 scaffold)

A three-pane desktop shell for the starter kit. Scaffold and docs only:
the Electron binary itself is a heavy, operator-gated download and is NOT
bundled here.

## What is in the box

| File | Role |
|---|---|
| `package.json` | npm manifest; pins `electron` 41.10.7 exact; `npm start` runs it |
| `main.js` | main process: one window, installer stream, allowlisted surface reads, offline chat stub |
| `preload.js` | the only renderer bridge: four functions on `window.kit` |
| `renderer/index.html` | the three panes (INSTALL, SURFACES, HERMES) |
| `renderer/styles.css` | local stylesheet |
| `renderer/app.js` | pane logic; talks only to `window.kit` |
| `renderer/surfaces/smith_chart.html` | byte-exact copy of the smith chart exhibit (fold law), single file, canvas + inline JS |
| `renderer/surfaces/BOOT.md` | byte-exact copy of the kit clean-boot loop |

## The three panes

1. **INSTALL** - one button runs the kit's own installer script
   (`../setup/install.ps1` on Windows via powershell, `../setup/install.sh`
   elsewhere via bash), cwd pinned to the kit root, and streams every
   stdout/stderr line into the pane as it arrives. The script itself is the
   kit's; this scaffold adds no second installer and changes no step.
2. **SURFACES** - the smith chart iframed from its local file, and BOOT.md
   text loaded through an allowlisted IPC read (`surfaces:read`), because
   Chromium blocks `fetch()` on `file://` pages. The allowlist in `main.js`
   is the whole surface of that read; no arbitrary file access exists.
3. **HERMES** - a chat pane stubbed to the plug. Messages ride IPC to a
   handler that answers with a fixed offline note and opens no socket. The
   live fire leg stays in `integrations/hermes/hermes_client.py`, which by
   kit law refuses to fire without an operator key and banks every burn.
   Wiring the live leg is an operator-keyed change, not a scaffold change.

## Zero fetch law

No network calls, no external fonts, no CDNs, no images, no remote
navigation. Enforced in four places:

- renderer CSP: `default-src 'none'; script-src 'self'; style-src 'self'; frame-src 'self'`
- `main.js`: `loadFile` on one local file, `setWindowOpenHandler` deny,
  `will-navigate` preventDefault
- every asset is a local file; the only non-local bytes in the tree would be
  `node_modules` after install
- the chat stub is offline by construction (no net module touched)

## Run it (operator-gated)

```
cd starter-kit/desktop
npm install        # downloads the Electron binary, operator-gated heavy
npm start
```

`npm install --package-lock-only --ignore-scripts` is the light check: it
resolves the manifest and writes the lockfile without downloading the
Electron binary or running its postinstall.

## Version pin

`electron` is pinned exact at 41.10.7 (the 41-x-y tip on the npm registry,
2026-10-07 probe). Rationale: the estate's own desktop build rides Electron
41 (corpus/steal/ZCODE_REPO_STEAL_MAP_20260924.md, desktop-shell lane), so
41.x is the proven major; `latest` was 44.6.0 at the same probe and a v0
scaffold does not ride the newest line. Bump only with a receipt.

## Security shape

Per the Electron 41 security checklist (docs/tutorial/security.md at tag
v41.10.7): `contextIsolation: true`, `sandbox: true`,
`nodeIntegration: false`, restrictive CSP, no popups, no navigation. The
installer spawn takes no renderer input beyond a single button press; the
script path is fixed in `main.js`.

## No business data inside

The scaffold carries no keys, no operator info, no estate receipts. The two
surfaces are the kit's own public clean-boot text and the smith chart
exhibit. If you fork this desk for estate work, keep it that way or the
zero-fetch audit fails on contents, not just transport.

## Falsifier (how to know it works)

- with the network unplugged, `npm start` still opens all three panes, the
  smith chart draws, BOOT.md loads, and the installer streams
- the HERMES pane answers with the stub note and zero packets leave the
  machine (any packet capture shows none from this process)
- `grep -rE "https?://" starter-kit/desktop` over the scaffold sources
  returns nothing (surfaces copy included)
