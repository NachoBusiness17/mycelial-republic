# STEAL — r/MUD web clients (ex7qjj) + 2026 equivalents onto /wave

Date: 2026-08-14
OP (Wayback): maps you can point/click; menus for tasks; keep the text.

Comments 403. Named soil from the thread's living descendants, not invented quotes:

- Iron Realms Nexus: separate windows (output, inventory, comms, map); compass tap; GMCP. https://www.ironrealms.com/the-nexus-client/
- Icesus browser 2026: GMCP is the HUD (vitals, exits, party, map). Do not scrape the text stream. https://icesus.org/guides/clients/
- Mudlet / mudix: mapper + gauges; browser now runs the same idea.
- maldorne mud-web-client: command history, scrollback, GMCP. https://github.com/maldorne/mud-web-client

Mag mapping (compose, do not throne):
- GMCP = GET /api/v1/wave (already).
- Map click = room_svg data-exit + compass from narrative.exits.
- Menus = legal-move action bar, not a dropdown chrome.
- Output reads down (append). History = up/down. n/s/e/w when the line is empty.
- Bags look on click. Unseated is empty, not 0 HP.
- Swiss: Helvetica, hairlines, one red for down seats. Gold/green chrome out of the SVG.

Scripts stay Mag verbs. No Lua throne.
