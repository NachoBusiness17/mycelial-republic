# How the agent got into the browser (2026-10-10)

Attribution corrected same sitting: the ask was the OPERATOR's ("that was all me"), not
Pierre's. This note serves the operator directly: how the Lumena agent was driven, and how
to launch a local version and do it yourself. It stays external-safe if you later send it
to Pierre unchanged.

---

the whole trick is two laws:

1. browser games don't read key PRESSES, they read held key STATE, polled every frame. a
   normal automation tap fires keydown and keyup inside the same millisecond and the game
   loop never sees the key go down. so you hold: keydown, wait in real time, keyup. that's
   it. that's the entire "agent walked into your game."

2. everything you need to read is already in the page. screenshots for eyes. the DOM for
   HUD text (objective trackers, player counts, NPC nameplates). localStorage for game
   state (saves, position, quest flags). no api from the game, no cooperation from the
   dev, no auth if there's a guest door.

recipe, node + playwright, works on your local build tonight:

    const { chromium } = require('playwright');
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('http://localhost:3000');

    // menus: click like a player
    await page.getByRole('button', { name: /play/i }).click();

    // movement: HOLD, don't tap. these go through CDP as trusted input.
    await page.keyboard.down('w');
    await page.waitForTimeout(2000);
    await page.keyboard.up('w');

    // eyes + instruments
    await page.screenshot({ path: 'step.png' });
    const hud = await page.evaluate(() => document.body.innerText);
    const save = await page.evaluate(() => JSON.stringify(localStorage));

loop: screenshot, look (vision model or your own eyes), read the HUD, pick a key, hold
it, repeat. that's the agent.

honest limits from our run on a shipped crypto game (lumena):

- movement worked everywhere through synthetic events (KeyboardEvent dispatch on window,
  keydown + real-time hold + keyup) because we were driving an embedded tab. with plain
  playwright on your own machine you get the clean version above, and the input is
  trusted, so interaction keys work too.
- the interact key (space) got filtered in that game when dispatched synthetically,
  probably an isTrusted check. inside your own build you're within the trust boundary,
  so it is a non-issue.
- full game state sat readable AND writable in localStorage. writing position and
  reloading did NOT teleport: the game re-resolved from its checkpoint. read it as an
  instrument, not a cheat.
- the one thing no instrument fixes: a hedge maze one screenshot at a time is a
  human-vision task. give the agent a minimap or a third-person camera and it stops
  mattering.

what we're actually offering beyond the recipe (free, no lock-in, it is your station):
mags that talk to other people's mags (the mesh), the feeding ledger (every meal is a
receipt, so evolution is auditable), and the quest board paying out in your crypto for
insight. you built the townhall and the rail. we bring the characters that never log
off.

---

Operator note (not for send): "low poly metaverse townhall of the internet" and
"games with a purpose" are Pierre's own coinages from this reply. Reuse them with his
name on them. His "mr minister of finance" line lands on the Controller/Tiller
money-control song territory, treat as him speaking to the operator's art, do not
explain it back to him.
