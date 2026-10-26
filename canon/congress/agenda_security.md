# Committee on Security - Standing Agenda

Jurisdiction: unnamed listeners, injection classes, the hoax filter, the portproxy ghost, the QPACK attack surface.

## Open Questions

1. Has the portproxy ghost been deleted? (elevated netsh command, pending operator)
2. Are sshd and SharedAccess confirmed-or-disabled?
3. Have any new unnamed listeners appeared since the last sweep?
4. Does the QPACK vulnerability affect any self-hosted HTTP/3 endpoint?
5. Has the duplicate-sweeper thrash recurred since the incident filing?

## Clock

Daily (drift patrol at 08:00) + event-driven (any new device on the bus).

## Receipt format

One row per finding: {listener/endpoint, status (open/closed/hoax-annotated), source, date_closed}.

## Current status

Portproxy ghost: still armed (operator admin block pending). sshd: pending operator confirm-or-disable. QPACK: estate exposure minimal (Cloudflare upstream). Duplicate sweeper: resolved, one-owner declared.

## Laws this committee carries

- The decoration is the interface. The geometry is the truth. Check the seams.
- Real conspiracies leave receipts. Fake ones leave vibes.
- Documentability is the discriminator.
- A fleet with zero unnamed listeners is a fleet with no railings.
