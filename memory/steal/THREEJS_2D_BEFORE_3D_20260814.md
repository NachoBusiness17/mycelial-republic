# THREE.JS STEAL — 2D BEFORE 3D (2026-08-14)

We used their model. Then we designed ours. Not a Three.js throne.

## Fetched (not guessed)
- three.js r185 SVGRenderer.js (github mrdoob/three.js examples/jsm/renderers/SVGRenderer.js)
  Use cases they name: interactive maps, complex/animated UIs, diagrams.
  Crystal-clear, CSS-styleable, accessible metadata. No shading, no textures, no shadows.
  Internals stolen: scene graph, renderOrder, painter z-sort, path pooling, viewBox as camera,
  SVGObject wrapping DOM nodes, path batching by style.
- three.js discourse: SVGRenderer is NOT a WebGL fallback for 3D. Orthographic HUD is a second
  scene. CSS2DRenderer is HTML labels. Canvas overlay is cheap.
- Raph Levien "2D Graphics on Modern GPU": retained scene graph, swap backends later.
- AntV G / Scenery: one graph, SVG now, WebGL later, DOM labels mixed in.
- DEV: SVG = retained scene graph for free (hit-test, labels). WebGL when the graph is huge.

## Mag already
- /wave room_svg + clickable data-exit (DOM picking = Raycaster for free)
- surface_render viewBox + hairline SVG
- flock_shader (agent=pixel) — GPU contract, not a 3D engine
- Swiss HUD frames = CSS2D labels
- chasm/table bytes = the scene. Renderer is interchangeable.

## Mapping (learn, then own)
| Three | Mag 2D now |
| Object3D graph | svg g data-layer=world|exits|labels data-order |
| Camera / viewBox | svg viewBox data-camera=ortho |
| renderOrder / painter | layer order in the SVG |
| SVGObject | HTML compass + passage (CSS2D) |
| Raycaster | data-exit click on SVG |
| WebGLRenderer | later, same bytes, different backend |
| Unity/Unreal | never. Assemble Mag parts. |

## Law
2D SVG is the interface. 3D is a later backend on the same graph.
Never store the scene as truth. Campaign/chasm is the nucleus.
Grok writes. Swarm ollama does not shade the HUD.
