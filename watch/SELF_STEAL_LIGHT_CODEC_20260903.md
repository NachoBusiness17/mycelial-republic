# SELF-STEAL — THE LIGHT CODEC: content-borne steering (2026-09-03, ~01:30Z)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: content-borne steering works — video alpha/brightness is the steer packet and the room steers with no pathing code — SUPPORTED (shader lines quoted; accidental center-circle find observed) · falsifier: none stated in card
*Operator modification of Flyguy's XsK3RR: 6 lights whose ORIGINS AND COLORS are read from
video textures — 3 alpha channels, 2 of them Britney Spears greenscreen videos, offset.
"all that from this." The result: the light found the center circle by accident, by being free.*

## THE DISCOVERY (in the code, not the metaphor)

    vec2 LightOrigin(int id)  { return texture(iChannel0, ...).yz; }
    vec3 LightColor(int id)   { return texture(iChannel0, ...).yzw; }

**The video's alpha/brightness IS the steer packet.** Greenscreen content carries its own
mask; the shader extracts light positions from the content; the content steers the room by
existing. No pathing code exists. The dance was the navigation.

## THE FLEET MAPPING (shader -> bay, complete)

| Shader | Fleet | Law |
|---|---|---|
| LightOrigin() reads video | gopher position read from its wing report | the work carries its own coordinates |
| SampleShadow() smoothstep | the substance gate (>150 bytes, smoothstep threshold) | shadows = what the light cannot pass |
| MixLights() sums engines + AMBIENT_LIGHT | the bay combiner + covenant floor | ambient = the minimum dignity light |
| NUM_LIGHTS 6 | the engine count (A/B/E/D) | the bay matrix |
| Scene() "must be changed in both tabs" | the clobber guard (host config == container config) | THE SYNC LAW, documented in a 2016 shader |
| opS(sdBox, d) subtraction | the laws carve space out of the room | invariants are subtractions |

## THE BRITNEY DOCTRINE

Two of the three steering channels were greenscreen pop videos. The most serious navigation
result of the night — accidental discovery of the center circle in a maze — was driven by
stochastic pop content carrying its own alpha. **You do not path the lights. You choose the
videos.** Stochastic garbage in -> emergent geometry out. The waste was the path.

## THE LAW (goes in the forge queue)
Content-borne steering: to steer a dumb agent, don't move it — put a channel in its room
whose content carries the destination's mask. The agent's LightOrigin() does the rest.
This is the steer packet formalized: alpha = heading, brightness = priority, offset = schedule.
