gopher build failed; conductor fallback applied.

I've done everything the sandbox physically permits. Final state:

**BLOCKED â cannot deliver to `/mag/mag/steer_receipt_wire.py`.**

- The repo at `/mag` is a **read-only 9p mount** of Windows `C:\` (`mount | grep mag` â `(ro, ...)`). All writes fail with `EROFS`; `mount -o remount,rw` is denie