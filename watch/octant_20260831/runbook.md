# Operator runbook — reconcile and apply (2026-08-31)

This runbook is for the Windows host checkout. It is intentionally explicit:
the patch queue is applied one file at a time, not as a transaction. A preflight
must pass before any write. Historical files in `PATCHES\applied` do not count
as evidence that the current queue is applied.

## 0. Establish the host root and make a recoverable backup

Run in PowerShell:

```powershell
$MagRoot = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
Set-Location -LiteralPath $MagRoot
$Py = Join-Path $MagRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $Py)) { throw "Missing host venv: $Py" }
$Backup = "C:\backups\mag_$(Get-Date -Format yyyyMMdd-HHmmss)"
robocopy $MagRoot $Backup /E /COPY:DAT /R:2 /W:5 /XD .venv __pycache__ .git
if ($LASTEXITCODE -ge 8) { throw "Backup failed with robocopy exit code $LASTEXITCODE" }
```

The backup is a recovery copy, not proof of a successful deployment.

## 1. Reconcile before writing

```powershell
& $Py -m mag.openclaw_patches preflight
if ($LASTEXITCODE -ne 0) { throw 'Patch preflight failed; no patches were applied.' }
```

Preflight reports the exact current queue, target collisions, missing target
files, invalid payloads, and whether each search string is present. Do not
manually edit `sancho_lattice_row.json`: the lattice row is already part of the
current queue and must be handled by the same preflight/apply path.

## 2. Apply the verified queue

```powershell
& $Py -m mag.openclaw_patches apply
if ($LASTEXITCODE -ne 0) { throw 'Patch application reported a failure; inspect its per-file rows.' }
& $Py -m mag.openclaw_patches status
```

At the time this runbook was written, the queue contained 11 JSON patch files.
Use preflight for the live count. Those were 11 operations, including the
lattice-row operation; it was not “11 patches plus a lattice row.” Two files
target `mag/api_gateway.py` and two target `mag/swarm_tools.py`, so order is
significant and the applicator must report each operation separately.

## 3. Record row zero from the shared host surface

```powershell
$RowZero = Join-Path $MagRoot 'watch\ask_router_row0.json'
if (-not (Test-Path -LiteralPath $RowZero)) { throw "Missing row zero: $RowZero" }
Get-Content -LiteralPath $RowZero -Raw | & $Py -m mag.ask_router --record
```

The container-visible equivalent is `/board/ask_router_row0.json`; the durable
host source is `watch\ask_router_row0.json`.

## 4. Run acceptance checks that do not spend

```powershell
& $Py -m pytest (Join-Path $MagRoot 'tests\test_blade_templates.py') -v
& $Py -c "from mag import harness; print(harness.run_once(dry=True))"
& $Py -m mag.atlas build
```

These checks do not prove a live Vast instance or live model call. They prove
that the local code path and receipt path execute. Live work remains explicitly
operator-gated.

## 5. Inspect service health

```powershell
docker ps
docker logs --tail 50 mag-worker
```

Do not treat an unhealthy container flag as a seat instruction. It requires an
operator decision and a receipt.

## Failure rule

If any patch fails its search match, stop. Keep the per-file result, reconcile
that target against the current source, and only then retry. Never infer “done”
from a moved file in `applied`; require the target change plus a validation
receipt. The runbook does not delete historical records or claim atomic rollback.

Sources: the current queue under `queue\handoff\openclaw\PATCHES`, the shared
host surface under `watch\inbox`, and the local applicator
`mag\openclaw_patches.py`.
