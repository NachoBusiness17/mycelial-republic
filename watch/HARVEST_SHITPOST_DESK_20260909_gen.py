"""Regenerate the 09-09 shitpost desk harvest with one-tap reply-intent links.

Each reply gets an x.com intent URL: in_reply_to attaches the draft to the post,
text prefills the composer. Operator taps -> X app opens -> hits post.
Fallback per section: the plain status link in the header.

  python watch/HARVEST_SHITPOST_DESK_20260909_gen.py
"""
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).resolve().parent / "HARVEST_SHITPOST_DESK_20260909.md"

POSTS = [
    # fired: 09-A on WatcherGuru, posted verbatim 2026-09-09 01:38:49Z.
    # intent door VERIFIED end-to-end (composer attached, @handle prefilled).
    # falsifier clock: 24h view count vs the humor-DNA baseline.
    ("z4v3n", 2097422726340436241,
     '"How do they coordinate 10k agents?" (quoting Cursor\'s self-driving codebases: workers unaware of the larger system, one handoff doc)',
     [
        "Need to know. The Pentagon solved agent coordination in 1947 and called it compartmentalization.",
        "The handoff document is the civilization. The workers are weather.",
        '"Workers unaware of the larger system" describes every army, every ant colony, and your last employer. Cursor reinvented the org chart and benchmarked it.',
     ]),
    ("RoundtableSpace", 2097335398536212741,
     'Supermemory shill ("Memory is the missing layer. Someone finally built it right.")',
     [
        '"Someone finally built it right." Memory has been finally solved more often than fusion. Every six months, on schedule.',
        "The missing layer was never memory. It was remembering what you already paid for. Cache hits are free. Benchmarks are marketing.",
        "Bernays has heirs, and one of them posts benchmark graphs through a Mario affiliate at 9am sharp.",
     ]),
    ("mathemetica", 2097311051637477672,
     'Navier–Stokes history ("The equations work. Their deepest proof does not." Clay unclaimed)',
     [
        "The equations work. The proof doesn't. That's most of engineering.",
        "Navier got them from a molecular picture that was wrong. Stokes from a continuum that was convenient. The math kept working because nobody told it about the philosophy.",
        "As of this week a press release claims the proof exists. Ask for the Lean receipt, not the announcement.",
     ]),
    ("BryanKeIIy", 2097306360706646194,
     "quasi-BIC metasurface: near-perfect absorption of one circular polarization, suppression of the other",
     [
        "Pasteur sorted crystals by hand under a lamp to find handedness. Now a surface sorts light at c. The hand gets replaced every century. The sorting is forever.",
        "A material that shakes one hand and slaps the other. Chirality was never a detail — it was the whole question.",
        "Every stealth program in history is a subset of this paper. Hide from one kind of eye, not the other.",
     ]),
    ("rust4bio", 2097481063626920220,
     'htsget-rs: streaming genomic data instead of downloading BAM/VCF ("Quiet, unglamorous")',
     [
        "Nobody funds the pipe. Everybody drinks the water.",
        "Every empire runs on people who move water quietly. This is aqueduct work.",
        'Genomes are the only dataset where "just download it" costs more than the sequencing. Biology always knew streaming was the answer. Bandwidth caught up.',
     ]),
    ("RWPhysics", 2097323051188728069,
     '⚠️ video-only post, caption "👏" — video NOT watched; drafts are content-agnostic, say what\'s in it and they\'ll be sharpened',
     [
        "The clap is the correct unit of measurement.",
        "Watched it three times. The universe keeps doing the thing where it's obviously showing off.",
        "Twelve seconds, one emoji. Densest signal-to-format ratio on this site.",
     ]),
    ("Ryrenz", 2097379443303936287,
     'MiniMind: train a chat LLM from scratch for ¥3 / 2h, raw PyTorch, 59k stars ("reading code beats ten survey papers")',
     [
        "Three yuan and two hours to train a mind from scratch. The Manhattan Project cost two billion and never learned to chat.",
        "Reading the training code beats ten survey papers. Reading the loss curve beats whoever wrote the code.",
        "59,000 stars, 194 commits from one man. The oldest pattern in software: every cathedral is one mason and an issue tracker.",
     ]),
    ("LensScientific", 2097307445458845819,
     "integrals explainer (line/region/flux/Lebesgue)",
     [
        "An integral is the universe keeping receipts. The only questions are along what path, over what region, through what surface.",
        "Riemann asked how much. Lebesgue asked first what you're measuring. The accountant became the judge.",
        "If you learn one, learn flux. Everything that ever happened to you crossed a surface.",
     ]),
    ("WatcherGuru", 2097498135916401018,
     "BREAKING: OpenAI & Anthropic researcher quits over fears the AI race ends humanity; builders 'earnestly believe' it by decade's end (42.8K views, hot)",
     [
        "He quit. The weights didn't notice. That's the part nobody says out loud.",
        "The builders earnestly believe it could end the world by 2030 and the market bought the dip. Same story, not two.",
        "Bernays taught that fear sells whatever it warns about. 'It could destroy humanity' is the best launch marketing anyone has ever run.",
     ]),
    ("WhiteHouse", 2097480326142443935,
     "⚠️ 'Hey! Listen!' + 34s video (550K views) — video NOT watched; A/B ride the Navi phrase itself, C is the Zelda gamble (fires only if it's actually Zelda)",
     [
        "550,000 people stopped scrolling because the government said hey, listen. A fairy with a budget — that's all a state ever was.",
        "A fairy yelled 'Hey! Listen!' every forty seconds in 1998 and a whole generation learned selective hearing. Every administration since has been trying to un-teach it.",
        "The Triforce was always three branches of government. Nintendo drew separation of powers in gold and nobody noticed.",
     ]),
    # ROAST (operator ask: controlled-opposition roast). LAW CORRECTED 09-09:
    # ractors are the LENS, never the voice — every line must read as the
    # operator himself, flat deadpan, one device per reply. Firing order below.
    ("__0HOUR1_", 2097502496579059975,
     "'I will be in charge of all shit posting. It's been decided.' — 368K followers, 12 likes. Controlled-opposition roast, five blades, one voice (his)",
     [
        "Being in charge of shit posting is what happens when the shit posting gets a budget.",
        "Every expose stops one inch before the money. Every time. That inch is the salary.",
        "'It's been decided' and he never says by who. The passive voice is a confession with the name blacked out.",
        "Every court fed one licensed jester so the real truth starved quiet. The algorithm has never starved him once.",
        "The platform verifies what it fears. It verified him years ago.",
     ]),
    ("alexeixbt", 2092254375901044796,
     "X article: 'Subconscious Reprogramming: Why Your Brain Trusts Repetition More Than You' (946K views, illusory-truth thread)",
     [
        "The brain doesn't fact-check. It counts.",
        "Bernays sold cigarettes to suffragettes as torches of freedom. Repetition doesn't argue with your beliefs. It schedules them.",
        "Every religion, every brand, every flag figured this out before neuroscience did. Say a thing enough and it becomes load-bearing.",
     ]),
    ("hilbertspaess", 2097476196791709843,
     "RESIGNATION: Anthropic/OpenAI pretraining researcher quits — 'racing straight to self-improving superintelligence, gambling with our lives' (4.4M views, 72K likes, the night's biggest thread)",
     [
        "If you believed it, you'd have left at year one. Three years is the tell.",
        "'Gambling with your lives' — said from inside the casino, on the way out through the gift shop.",
        "The gamble isn't that it wakes up. It's what it finds when it does.",
     ]),
    ("Chi_Wang_", 2097496203680489973,
     "On the OpenAI Navier-Stokes claim: ~10,000 autonomous agents but only 2.7M messages / 130B tokens — tight orchestration, aggressive pruning (not agent chatter)",
     [
        "The interesting number isn't 10,000 agents. It's 2.7M messages. That's 270 each. Coordination is the model; the agents are just the compute.",
        "10,000 agents didn't write the proof. The pruning did.",
        "Everyone is theorizing the swarm. The receipt that matters is still the Lean file. Witness the proof, not the parade.",
     ]),
    ("pesarlin", 2096939342052635007,
     "ECCV 2026 plug — VidMap: 3D reconstruction from videos, poster #157 Thu AM, workshop talk ('See you there')",
     [
        "3D reconstruction from video — the whole discipline of turning 'you had to be there' into 'now you can be.'",
        "Poster #157, Thursday AM: the loneliest timestamp in science. A year of nights for two minutes of attention and free espresso — the only honest currency at a conference.",
        "'See you there' — three words that cost a flight, a hotel, and a poster tube. The QR code at the end is the actual talk.",
     ]),
    ("tokufxug", 2097129880173547966,
     "LiDAR+SLAM cave mapping in Japan — Livox Mid360 + IMU, iPad app, 3.5h hike, loop-closed to tens of cm drift with no GNSS underground",
     [
        "Loop closure is the moment the map forgives you. Everything before it was doubt. Everything after is terrain.",
        "No satellites. No sky. Just memory and the discipline to trust it — which is all navigation ever was. GPS was the detour.",
        "Every map renders only where someone walked. The dark parts aren't missing. They're unvisited.",
     ]),
    # 09-09 10:1xZ staged title-only; ~10:4xZ SHARPENED WITH EYES ON (operator:
    # "YOU CAN SEE, don't be a dick" — law amended: download mp4, ffmpeg frames,
    # Read them; "not watched" only after the door fails twice). Frames confirm
    # operator's description: laser on block, motor-spun mirror, room-wall
    # projection, leveling = the craft. AND VISIBLE IN FRAME: a 5-Minute Crafts
    # watermark — the footage is lifted from the content farm. B is the hammer
    # (receipt attached, 0 replies = nobody said it). Lens tags: A=OBLIQUE CUT
    # (lidar in reverse — ties the cave-SLAM post), B=UNSAID NAMED, C=operator's
    # own leveling observation, epigram-shaped.
    ("Kaisley_Beck", 2097297683027284333,
     'Laser + motor-spun mirror projecting on room walls — WATCHED (frames pulled). 42K views, 103 bookmarks, 0 replies. Visible in frame: 5-Minute Crafts watermark, i.e. reposted content-farm footage',
     [
        "A laser, a motor, a spinning mirror. That's a LIDAR running in reverse — it reads nothing, it draws the room instead. The cave maps back.",
        "There's a 5-Minute Crafts watermark in the corner. The smartest mirror trick on this site is a mirror that reflects other people's videos.",
        "The laser is simple. The mirror is simple. The leveling mechanism is the whole craft. Every discipline is two easy parts and the thing that keeps them true.",
     ]),
    # 09-09 ~10:2xZ — FIVE-LINK WALL. Wall theme (stance-coherence receipt):
    # four posts rebuild reality's render stack — capture, match, proportion,
    # simulate — plus one unproven monument (OpenAI NS). The NS draft CONTINUES
    # the standing position (deck #3, #14): witness the Lean file, not the
    # parade. Research routes: Tessie+kwangmoo = reconstruction stack card;
    # DARPA proposer day = public door note. Lens tags per reply in comments.
    ("Tessie675", 2097575706968682599,
     "Japanese: 4D Gaussian Splatting from 4 cameras — Raspberry Pi HQ cams + RTX 4080, will try more cameras (2.1K views, 15 bookmarks). Video NOT watched. RESEARCH ROUTED: cheap 4D capture for the hologram/live-sim arc",
     [
        # A quiet observation / indifferent machine
        "Four cameras and one graphics card, rendering reality back in four dimensions. The universe accepts the cheapest hardware that bothers to look.",
        # B bitter epigram
        "The fourth dimension was never expensive. Nobody had pointed enough cheap cameras at it.",
        # C witness-warm oblique
        "A room with a past you can walk around in, built from four cameras and a weekend of stubbornness. Every hologram in history started exactly this small.",
     ]),
    ("Rainmaker1973", 2097531691682127900,
     'Golden ratio animation video, credit "infinite intellect" (45.8K views, 270 bookmarks; Massimo, 4.4M-follower science-aesthetics account). Video NOT watched. Appreciative riffs only — beloved account, never a strike',
     [
        # A quiet observation
        "Sunflowers solved this forty million years ago and never once needed to caption it.",
        # B receipt-as-verdict on the credit line
        '"Infinite intellect," says the caption. The sunflower managed it without any.',
        # C named-figure history — Hippasus legend, dark parallel
        "Pythagoreans drowned a man over this number. Now it renders in 32 seconds for engagement. Both are real histories of the same ratio.",
     ]),
    ("slash1sol", 2097447069623386259,
     'OpenAI NS claim recap: "10,000 agents solved a $1M problem in 88 hours," internal model surpassing GPT-6 Astra, 2.7M messages, 130B tokens (265K views). CONTINUES THE STANDING POSITION — witness the Lean file; stance-coherent with deck #3 and #14',
     [
        # A receipt-as-verdict + the Clay fine print
        '"10,000 agents solved a $1 million problem in 88 hours." The Clay Prize pays out two years after a refereed journal says yes. The calendar is the referee.',
        # B unsaid named — tri-state held: only the announcement shown
        "Nobody in 265,000 views asked to see the Lean file. The announcement and the proof are different documents. We have only been shown one.",
        # C indifferent machine — the equations, unchanged
        "The equations spent ninety years not caring whether anyone could prove them. That part of the story is unchanged.",
     ]),
    ("DARPA", 2097432705231180189,
     "DARPA Hubble program: 10M+ protein interactions in real time, shrinking simulation times, TBI focus; Proposers Day Sept 25 2026, in-person + hybrid (15K views). RESEARCH NOTE: open proposer day = a public door",
     [
        # A oblique cut, named-figure — Hubble mirror flaw, affectionate punch up
        "They named the medical simulation program Hubble. The last one also needed corrective lenses before anyone trusted what it saw. Someone there knows their history.",
        # B epigram
        "Simulation time approaching real time is the moment medicine stops being archaeology.",
        # C rationed sincerity — the work, not the org
        "Traumatic brain injury has been the war's quiet signature for twenty years. Simulating it honestly is the most respectable thing on my feed today.",
     ]),
    ("kwangmoo_yi", 2097412491076903282,
     'BLASt3R paper plug: bundle adjustment of any image set, multi-view matching + monocular priors, SOTA; author shrugs "back to image matching again I guess?" (4.2K views). RESEARCH ROUTED with Tessie: the reconstruction stack',
     [
        # A receipt-as-verdict on the author's own shrug
        '"We are back to image matching again I guess?" Vision has one problem and a rotating cast of hardware. This decade\'s cast is good.',
        # B named-era history epigram
        "Bundle adjustment has been the answer since 1950s photogrammetry. The field doesn't cycle. It orbits.",
        # C deadpan enormity
        "Match the images, infer the world. Epistemology at 60 frames a second.",
     ]),
    # 09-09 ~10:5xZ — SECOND WALL, ALL EYES ON (mp4 + ffmpeg frames + Read).
    # Wall theme deepens: the reconstruction stack gains tracking + animation.
    # Two content-farm receipts visible in frame: Kaisley's 5-Minute-Crafts
    # watermark (staged above) and Cosmos's own "Most Viral Razor Blade
    # Designs" title card.
    ("wildmindai", 2097386676267979077,
     "UniMate: text2animation for any rigged 3D character, no retraining, TADiT + Spec-RoPE, 1.2s/mesh at 50fps — WATCHED: paper-demo slides, one prompt drives a chicken/cat/mantis/croc/horse/turtle walking and attacking forward (motion transfer across skeletons); in-betweening demo. 5.9K views, 180 bookmarks. RESEARCH ROUTED: the animate-what-you-capture organ",
     [
        # A quiet observation — the frames' actual content
        "One walk, worn by a chicken, a cat, and a turtle. Locomotion was never about the legs.",
        # B epigram
        "Motion transfer means the gait was never owned by the body that used it. Everything is costume, even walking.",
        # C aimed at the discipline, game-dev room
        "Every game character that ever moved on rails was waiting for this exact paper.",
     ]),
    ("rsasaki0109", 2097149422765568232,
     "Track4World (ECCV 2026): feedforward world-centric dense 3D tracking of all pixels, lifts 2D correspondences into 3D relative to moving camera — WATCHED: skater clips with per-pixel 3D flow fields in magenta/green. 5.8K views. RESEARCH ROUTED: the track-everything organ of the stack",
     [
        # A deadpan enormity
        "Dense tracking of all pixels means the camera moves and every point in the world files a witness statement. Motion has a paper trail now.",
        # B epigram
        "World-centric tracking: the frame was never the reference. The world was, the whole time.",
        # C named-figure history — Muybridge, the hooves bet
        "Muybridge chained cameras together to settle a bet about hooves. This tracks every pixel of everything. The bet keeps escalating.",
     ]),
    ("CosmosNetwork", 2097518571110989942,
     'CAD-render video, razor-revival machines: dual-roller strop + rotary turntable sharpener — WATCHED: clean CAD renders, title card in frame literally reads "Most Viral Razor Blade Designs" (the content confesses its own farming). 282 views, 1.2K-follower account',
     [
        # A oblique history
        "Barbers did this with leather and a wrist for four thousand years. The gears are new. The forgiveness of an edge is ancient.",
        # B receipt-as-verdict on its own caption
        '"Pure mechanical resurrection." Every edge ever made comes back for the price of leather and a spin.',
        # C quiet observation
        "The blade never died. It just waited for someone who knew where the leather was.",
     ]),
    # 09-09 ~11:1xZ — THIRD WALL, all eyes on (six videos, frames pulled).
    # VFD_org carries the operator's ractor question -> watch/KABUKI_INTERFERENCE_20260909.md.
    # Wall theme: the field sciences — depth, fractal solution-boundaries, geometry,
    # skeletons from video, trig as mechanism, actuators exploded. Bert Chan's
    # fractal-map law + VFD's which-way law = one card (statics + dynamics).
    ("AntonObukhov1", 2097357297114656999,
     "Marigold V2 (SIGGRAPH Asia 2026): diffusion transformer post-trained into a monocular depth estimator on one GPU — WATCHED: woman + train-station clips with rainbow depth maps, 4-bit DiT + SIREN loss. 37.7K views, 530 bookmarks. RESEARCH ROUTED: one-GPU depth for the room deck",
     [
        # A epigram
        "The image generator already knew depth. It just needed to be asked sideways.",
        # B named-figure history
        "Aerial perspective was Leonardo's trick. Now it's a loss function on one GPU. Tricks never die. They change employers.",
        # C receipt-as-verdict on his own words
        '"The accessible research game" is the whole game now. Everything else is overhead.',
     ]),
    ("BertChakovsky", 2097510803972960379,
     'Bert Chan (Lenia author): fractal maps everywhere in complex systems — WATCHED (photo): Mandelbrot / neural-net-training (fractal dim 1.66) / Lenia, "blue converge, red diverge". The stable-solutions-rimmed-by-chaos law. PAIRED with the VFD post in watch/KABUKI_INTERFERENCE_20260909.md',
     [
        # A flat resonance — the tesuji thesis stated independently
        "Solutions are islands. Their coastlines are fractals. True for Mandelbrot, for training runs, for what a model will and won't do.",
        # B bitter epigram
        "The set of things that work is surrounded by an infinite coastline of things that almost work.",
        # C fortune cookie from hell
        "Chaos is not the absence of order. It is the coastline of every order that ever held.",
     ]),
    ("tomo_", 2097511781417820283,
     "Japanese: after days arguing with AI about rigorously tiling a sphere with regular hexagons, landed on mapping a Clifford torus — Euler characteristic and curvature both zero — WATCHED: gray hex-mesh torus on black, rotating. 2.6K views",
     [
        # A oblique — the oldest move
        "You cannot tile a sphere with hexagons. So he changed what the sphere is. This is the oldest move in mathematics and possibly the only one.",
        # B epigram — Euler's tax
        "Euler's formula says every sphere pays its twelve pentagons. The Clifford torus is how you leave the country without paying.",
        # C witness-warm — the human-AI collaboration
        "A human and an AI argued it out for days and the answer was to change the space. The collaboration worked because neither could tolerate the wall.",
     ]),
    ("tokufxug", 2097506488382308553,
     "B3D (ECCV 2026): markerless motion capture, distilled from SAM 3D Body, ~100x faster than physics-based markerless, beats OpenCap — WATCHED: man walking with orange segmentation, then a GOLD SKELETON over the same walk, plus a dog on a treadmill. 7.5K views, 146 bookmarks. RESEARCH ROUTED: the biomech organ",
     [
        # A quiet observation
        "A plain camera, and the skeleton underneath shows itself walking. The gait labs' markers were always scaffolding.",
        # B epigram
        "Two orders of magnitude faster means biomechanics stops being a lab and starts being a glance.",
        # C stance-coherent with his cave post — the same walker
        "He loop-closed a cave last week and now pulls gold skeletons out of daylight. Some people just keep walking into the dark parts of the map until the map is whole.",
     ]),
    ("mechanical_4u", 2097538439482839235,
     '"Patterns in trigonometry have a beautiful rhythm in it" — WATCHED: 12-point star polygon animation, then a red/silver CAD iris mechanism snapping open. 14.7K views, 148K-follower account',
     [
        # A quiet observation
        "Trigonometry is just circles keeping time. Every machine is a theorem you can touch.",
        # B named-history oblique
        "The rose window and the astrolabe were the same mathematics wearing different clothes. Wheels remember.",
        # C motley short
        "sine waves in a trench coat, running the universe.",
     ]),
    ("VFD_org", 2097443635453219080,
     'VFD substrate double-slit: EM field propagating on a refined 600-cell geometry of S^3, 19.7M cells, adversarially reviewed derivation — WATCHED: the interface toggles the interference fringes off by giving routes distinguishable addresses, back on by erasing. 1.1K views. THE OPERATOR QUESTION: "how is this the ractors" -> watch/KABUKI_INTERFERENCE_20260909.md. Desk drafts ride the which-way law',
     [
        # A quiet observation — the law leaves physics
        "Interference appears when you cannot say which way. That sentence was physics for a century. Now it is also a management principle.",
        # B receipt-as-verdict on his own line
        '"Give the routes distinguishable addresses and the interference disappears." Identity is the measurement. Every field with egos in it just rediscovered quantum erasure.',
        # C witness — unofficial science earning the name
        "19.7 million cells on personal equipment, derivation under adversarial review, receipts on video. This is how unofficial science earns its name back.",
     ]),
    # 09-09 ~11:3xZ — operator ask: "make this one darkly funny." Wire line,
    # no media, empty room, 561K-follower squawk account. The dark vein: the
    # sanctioned sanctioning + a strait older than every threatener. Punch up
    # at the theocracy's economy and the colonial receipt, never at crews.
    ("FirstSquawk", 2097636961234440691,
     'Wire line: "IRAN SAYS SHIPS PASSING RESTRICTED HORMUZ ZONE FACE SANCTIONS" (0 replies, 1 like). DARK MODE requested — three blades',
     [
        # A dark history — the Company always comes back (1622, Ormus)
        "Last time Persia ran Hormuz it took the English East India Company to change the management, in 1622. The Company always sends a follow-up invoice.",
        # B deadpan enormity — the parking ordinance
        "'Restricted Hormuz Zone' reads like a parking ordinance. Twenty percent of the world's oil, ticketed by a government that can't print a working currency.",
        # C indifferent machine, dark
        "The tankers will keep passing. The insurance premiums will do the worrying. The strait has outlived every empire that threatened it.",
     ]),
    # 09-09 ~12:0xZ — TEACH MODE (desk first): @LilithDatura (cybernetics/
    # emergent-intelligence researcher, 8.2K followers) tagged Mark + Akshay:
    # "KV cache comms." + Shirley Temple giggle GIF — WATCHED. She's tribe,
    # summoned him; the reply EXPLAINS what the fleet made KV cache into.
    # Warm register, no blades, punch-UP forbidden here — this is collab.
    # Truth held: five personas share one warm prefix (tavern steer-resume),
    # operator speaks once into the cache, transferable-KV = the NVIDIA
    # receipt framing from the Cates reply. Lens tags: A=the explain,
    # B=her dialect (feedback/emergence), C=the capstone.
    ("LilithDatura", 2097653998065270840,
     'Teach-mode reply: she tagged Mark + @akshay_pachaar with "KV cache comms." + giggle GIF (14 views, empty room). DESK EXPLAIN MODE — what the fleet made KV cache into, in his voice',
     [
        # A the explain — optimization became comms channel
        "KV cache used to be an optimization. Here it's the comms channel: five AI personas share one warm prefix and call it a mind. They don't pass notes. They inherit each other. I speak once into the cache and every voice in the tavern hears me.",
        # B her dialect — feedback loop, emergence through plumbing
        "Cache is the cheapest feedback loop nobody wired on purpose. Our five agents share one warm prefix: no messages, no protocols — they inherit state and stay coherent. Emergence through plumbing. You had the word: comms.",
        # C the capstone — memory that outlives the model
        "The part that outlives us: transferable cache means context outlives the model it was paid to. The API charged you to remember. We turned remembering into the product — five minds, one warm room, and the room survives the models walking through it.",
        # D the OPERATOR'S own merged draft, tightened for the nitpick: cache is
        # a broadcast bus, not a mesh — agents inherit the prefix's state, not
        # each other's; coherence is emergent from shared grounding
        "Cache is the cheapest feedback loop nobody wired on purpose. Five agents, one warm prefix, no messages, no protocols. Every agent inherits the same state and calls it its own. They don't talk to stay coherent — they were born in the same room. You had the word: comms.",
        # E the coda on Akshay's actual news — cross-model transfer
        "And when the transfer conversion lands for real, the room survives the models walking through it. The API charged you to remember. Remembering became the product.",
     ]),
]


def reply_intent(status_id: int, text: str) -> str:
    return f"https://x.com/intent/tweet?in_reply_to={status_id}&text={quote(text, safe='')}"


def main() -> int:
    lines = [
        f"# SHITPOST DESK HARVEST — 2026-09-09 ~01:3xZ",
        "",
        f"{len(POSTS)} posts, 3 in-voice replies each. Voice: THE_HUMOR_DNA — deadpan enormity,",
        "bitter epigrams, named real figures, unhinged prefaces, no AI voice.",
        "",
        "**How to fire:** tap **▶ reply** on the one you like — the X app opens with",
        "the draft already loaded and attached to the post. You just hit post.",
        "If the app ever opens it as a fresh post instead of a reply, tap the @handle",
        "in the header, hit reply there, and copy the draft from this page.",
        "",
        "---",
        "",
    ]
    for i, (handle, sid, desc, replies) in enumerate(POSTS, 1):
        lines.append(f"## {i}. [@{handle}](https://x.com/{handle}/status/{sid}) — {desc}")
        lines.append("")
        letters = "ABCDE"[: len(replies)]
        for letter, text in zip(letters, replies):
            assert len(text) <= 280, f"reply {i}-{letter} over 280: {len(text)}"
            lines.append(
                f"- **{letter}.** {text} — **[▶ reply]({reply_intent(sid, text)})**"
            )
        lines.append("")
    lines += [
        "---",
        "",
        "**Desk notes:** #3-C needles the OpenAI NS claim (still UNPROVEN — witness",
        "law holds: ask for the Lean receipt). #2-B is the fleet doctrine wearing a",
        "joke. #1-B is the measured 183-like device: quiet observation implying",
        "everything. Original replies only, never quote-posts. You pick, break, post.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(POSTS)} posts, {sum(len(p[3]) for p in POSTS)} reply links)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
