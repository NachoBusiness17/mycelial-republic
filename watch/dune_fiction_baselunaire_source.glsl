// DUNE FICTION — baselunaire (Shadertoy, CC BY-NC-SA default)
// Source hand-carried by the operator 2026-09-04 (paste verbatim; walls blocked
// all fetch routes). Techniques stolen for the B1 v1 skin catalog; our own GLSL
// is written fresh — this file is the REFERENCE RECEIPT, never shipped.
// Author: baselunaire — https://baselunaire.fr/?page_id=6327 (ENG) music: Skaven
// Steal inventory: ornithopter scale-phase ensemble loop, ring-distance worm with
// angular wobble in rotating frame, SDF character (Emperor/stillsuit), radial
// chromatic aberration, scanline-tied heat shimmer, parallax cloud stacks.

// Beware. Because Paul is coming for ALL OF US ! Yes. YES ! Even for you, Ix !
// Why ?! Did you think you'd get a special treatment ?!

// Another scene taken from my fanart-in-a-shader" : DUNE FICTION
// which you can watch for free on my blog in English OR French.
// ENG : https://baselunaire.fr/?page_id=6327
// VF  : https://baselunaire.fr/?page_id=6325

// I'm trying to bring back some life into scifi by making it fly with the help
// of motorized algebra (i.e. "shaders"). =D

// Again thanks to Skaven for the music :
// https://soundcloud.com/skaven252/exhumed-glory

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
     vec2 p = fragCoord.xy/iResolution.xy;
     vec4 col = vec4(0.0,0.0,0.0,1.0);

     if(abs(p.y-0.5)<0.4)
     {
        if(f(vec2(iTime)+357.321)>0.8)
        {
           p.x+=0.04*f(vec2(iTime,0.0)+654.987)*noise(vec2(floor(150.0*p.y)+1.05*iTime,0.0)+654.987);
           p.y+=0.04*f(vec2(iTime,0.0)+123.456)*noise(vec2(floor(150.0*p.x)+1.05*iTime,0.0)+123.456);
        };
        
        float chromab = length(p-vec2(0.5,0.5));
        col.r = texture(iChannel0,p + vec2( 0.007*chromab)).x;
        col.g = texture(iChannel0,p + vec2( 0.000*chromab)).y;
        col.b = texture(iChannel0,p + vec2(-0.007*chromab)).z;

        if(f(vec2(iTime)+357.321)>0.8)col += 0.300*f(vec2(iTime,0.0)        )*noise(vec2(floor( 20.0*p.y)+1.05*iTime,0.0))
                                            +0.300*f(vec2(iTime,0.0)+123.654)*noise(vec2(floor(150.0*p.y)+1.05*iTime,0.0)+654.589);
     };

     fragColor = col+0.125*f(vec2(iTime,0.0))*noise(vec2(p.y+1.05*iTime,0.0));
}

// NOTE (steal shelf): the Scene1 body (starfield, Eagle clouds, Muad'dib
// constellation, DCA turrets, jihad ships, mesas, horizon dunes, salt lake,
// ornithopter scale-phase ensemble loop, sand clouds, leaping worm, Emperor SDF)
// is preserved verbatim in the operator's 09-04 paste logged in session chat and
// inventoried in watch/INTAKE_DUNE_FICTION_SOURCE_20260904.md. The ornithopter
// loop and worm algebra are inventoried there with line-level descriptions.
