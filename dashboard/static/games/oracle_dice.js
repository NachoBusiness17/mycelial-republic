"use strict";
// oracle_dice.js — the fleet's shared RPG dice module (deterministic, seeded).
// Used by: mud.html, ruins_go.html, frontier_souls.html, any game that needs rolls.
// Same mulberry32 PRNG as the engine; seed per session, rolls recorded.

function mulberry32Shared(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

const OracleDice = {
  _rng: null,
  _seed: 0,
  _log: [],

  init(seed) {
    this._seed = seed || Date.now();
    this._rng = mulberry32Shared(this._seed);
    this._log = [];
  },

  // dN: roll one N-sided die
  dN(n) {
    if (!this._rng) this.init();
    const v = Math.floor(this._rng() * n) + 1;
    this._log.push({ die: `d${n}`, result: v });
    return v;
  },

  d4() { return this.dN(4); },
  d6() { return this.dN(6); },
  d8() { return this.dN(8); },
  d10() { return this.dN(10); },
  d12() { return this.dN(12); },
  d20() { return this.dN(20); },
  d100() { return this.dN(100); },

  // Roll with modifier: d20 + mod, returns {roll, mod, total, crit}
  check(mod) {
    const roll = this.d20();
    const total = roll + (mod || 0);
    return { roll, mod: mod || 0, total, crit: roll === 20, fail: roll === 1 };
  },

  // Advantage/disadvantage: roll 2d20, take higher/lower
  advantage(mod) {
    const a = this.d20(), b = this.d20();
    const roll = Math.max(a, b);
    return { roll, mod: mod || 0, total: roll + (mod || 0), crit: roll === 20, fail: roll === 1 };
  },
  disadvantage(mod) {
    const a = this.d20(), b = this.d20();
    const roll = Math.min(a, b);
    return { roll, mod: mod || 0, total: roll + (mod || 0), crit: roll === 20, fail: roll === 1 };
  },

  // Oracle: yes/no question with a modifier
  // +2 likely, 0 even, -2 unlikely. 11+ = yes, 16+ = yes and, 6- = no, 2- = no and.
  yesNo(mod) {
    const r = this.d20() + (mod || 0);
    if (r >= 16) return "yes_and";
    if (r >= 11) return "yes";
    if (r >= 6) return "no";
    return "no_and";
  },

  // Oracle: pick from a table
  pick(table) {
    if (!Array.isArray(table) || !table.length) return null;
    return table[Math.floor(this._rng() * table.length)];
  },

  // Get the roll log (for receipts / debugging)
  log() { return this._log.slice(); },

  // Reset with a new seed (deterministic replay)
  reseed(seed) { this.init(seed); },

  get seed() { return this._seed; },
};

if (typeof window !== "undefined") window.OracleDice = OracleDice;
if (typeof module !== "undefined" && module.exports) module.exports = OracleDice;
