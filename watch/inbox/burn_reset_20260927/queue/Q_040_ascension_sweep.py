#!/usr/bin/env python3
'''Q_040_ascension_sweep.py — FW-40 receipt probe: the MUD ascension ladder balance sweep.

Reads the exact scaling curve from dashboard/static/games/mud.html spawnEnemy/spawnBoss:

    a       = min(G.ng, 20)                      (mud.html:776)
    hpMult  = 1 + a*0.15 + G.ng*0.05            (:777)
    dmgMult = 1 + a*0.22 + G.ng*0.08            (:778)
    speed   = min(base.speed * hpMult, 220)     (:794)   <-- rides the HEALTH multiplier
    boss    = 500*hpMult, 32*dmgMult, 90*min(hpMult,1.8)   (:812-819)
    champion (on top): hp*2.6, dmg*1.4, speed*1.15 cap 200  (:850-852)

Player side (startGame reset, :2507-2518): every run restarts at 100 maxHp, 200 speed,
rusted sword 12 dmg; the only cross-run power is the horde-lore unlocks (none add hp).
In-run counter-scaling: +1 stat point/level, +15 maxHp per Vigor point (:1841).

Run: ./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/queue/Q_040_ascension_sweep.py
'''
import math

PLAYER_HP = 100
PLAYER_SPEED = 200
VIGOR_HP = 15

def mults(ng):
    a = min(ng, 20)
    return a, 1 + a * 0.15 + ng * 0.05, 1 + a * 0.22 + ng * 0.08

def enemy_speed(base, hp_mult):
    return min(base * hp_mult, 220.0)

BASE = {          # mud.html:780-789
    'walker':  dict(hp=40, speed=70,  dmg=14),
    'spitter': dict(hp=30, speed=50,  dmg=11),
    'dodger':  dict(hp=25, speed=130, dmg=16),
    'k8':      dict(hp=90, speed=95,  dmg=18),
    'rogue':   dict(hp=35, speed=125, dmg=26),
    'cleric':  dict(hp=60, speed=80,  dmg=8),
    'bmage':   dict(hp=55, speed=60,  dmg=14),
    'ranger':  dict(hp=45, speed=100, dmg=10),
}

print('=== FW-40 ascension sweep (curve verbatim from mud.html:776-794) ===')
print(f"{'A':>3} {'hpMult':>7} {'dmgMult':>8} | {'walker dmg':>10} {'hits->kill 100hp':>16} | {'walker spd':>10} {'k8 spd':>7} | {'champ hp':>9} {'champ dmg':>9}")
for ng in [0, 1, 2, 3, 5, 8, 10, 12, 15, 18, 20, 25, 30, 40, 60, 100]:
    a, hm, dm = mults(ng)
    wdmg = BASE['walker']['dmg'] * dm
    hits = math.ceil(PLAYER_HP / wdmg)
    wspd = enemy_speed(BASE['walker']['speed'], hm)
    k8spd = enemy_speed(BASE['k8']['speed'], hm)
    champ_hp = BASE['k8']['hp'] * hm * 2.6      # champion-grade escort (Verak is a rogue; k8 used as the tanky chassis)
    champ_dmg = BASE['k8']['dmg'] * dm * 1.4
    print(f"{ng:>3} {hm:>7.2f} {dm:>8.2f} | {wdmg:>10.1f} {hits:>16} | {wspd:>10.1f} {k8spd:>7.1f} | {champ_hp:>9.0f} {champ_dmg:>9.0f}")

print()
print('=== finding 1: the speed term double-dips on the HEALTH multiplier (mud.html:794) ===')
for t, row in BASE.items():
    for ng in range(0, 41):
        _, hm, _ = mults(ng)
        if enemy_speed(row['speed'], hm) >= 219.5:
            print(f'  {t:>8}: reaches the 220 cap (player runs 200) at A{ng}')
            break
    else:
        print(f'  {t:>8}: never caps (max {enemy_speed(row["speed"], mults(40)[1]):.0f} at A40)')

print()
print('=== finding 2: the "20 levels" ladder never tops (a-cap only caps term 1) ===')
for ng in [20, 40, 60, 100]:
    _, hm, dm = mults(ng)
    print(f'  A{ng:>3}: hp x{hm:.2f}  dmg x{dm:.2f}  (walker one-shots a 100hp player: {BASE["walker"]["dmg"]*dm >= PLAYER_HP})')
print('  display caps at 20 while the curve keeps climbing: addMsg uses min(G.ng,20) (:2537,:2561)')

print()
print('=== finding 3: boss at the cap (mud.html:812-819) ===')
_, hm, dm = mults(20)
print(f'  A20 boss: hp {500*hm:.0f}, dmg {32*dm:.1f} (one-shots 100hp), speed {90*min(hm,1.8):.0f}')

print()
print('=== finding 4: what the player can answer with (in-run only) ===')
# levels: xpNext = 20 * 1.5^k; walker pays 8 xp, room clear pays 60 souls (no xp)
total, lvl, xp_next = 0.0, 1, 20
marks = {}
for lvl_ups in range(1, 13):
    total += xp_next
    marks[lvl_ups + 1] = total
    xp_next = math.floor(xp_next * 1.5)
walker_xp = 8
for lv, need in sorted(marks.items()):
    print(f'  level {lv:>2}: {need:>7.0f} xp total = {need/walker_xp:>5.0f} walker kills; all-in Vigor -> maxHp {PLAYER_HP + VIGOR_HP*(lv-1)}')
print(f'  full clear (courtyard..forge) queue xp: refectory 2w+1s, infirmary 1c+1w, scriptorium 2r, crypt 2w+d+w, forge b+s+r, ossuary r+d+w+s')
queue_xp = (2*8+10) + (22+8) + (2*18) + (2*8+12+8) + (20+10+16) + (18+12+8+10)
print(f'  = {queue_xp} xp from queues alone -> level {max(lv for lv, need in marks.items() if need <= queue_xp)} before champions; +vigor HP ceiling ~{PLAYER_HP + VIGOR_HP*7}')
