import json, os

TMP = os.path.join(os.path.dirname(__file__), "_rcp_profiles_tmp.json")
profiles = json.load(open(TMP, encoding="utf-8"))

doc = {
  "meta": {
    "source": "Dwarf Fortress (Steam) install, READ ONLY mine",
    "roots": {
      "procedural_lua": "data/vanilla/vanilla_procedural/scripts/generators/ (creatures.lua, creatures/rcp.lua, creatures/shared_info.lua, interactions*.lua, evil.lua, materials.lua, divine.lua, entities.lua)",
      "static_interactions": "data/vanilla/vanilla_interactions/objects/interaction_standard.txt",
      "materials": "data/vanilla/vanilla_materials/objects/material_template_default.txt",
      "creature_variations": "data/vanilla/vanilla_creatures/objects/c_variation_default.txt"
    },
    "note": "Modern DF (Steam/v50+) generates forgotten beasts, titans, demons, night creatures, curses and secrets at WORLD GEN time via Lua that EMITS raw token text. vanilla_procedural has no .txt objects; the txt vocabulary is emitted by Lua.",
    "mined": "2026-09-25"
  },

  "assembly_chain_forgotten_beast": {
    "entry": "creatures.fb.default(layer_type, tok)  [creatures.lua:154]",
    "steps": [
      "1. STATIC SEED: [FEATURE_BEAST] [ATTACK_TRIGGER:0:0:2] (2 created wealth) NAME/CASTE_NAME 'forgotten beast' NO_GENDER CARNIVORE DIFFICULTY:10 NATURAL_SKILL melee set 6 LARGE_PREDATOR",
      "2. add_regular_tokens + BIOME:SUBTERRANEAN_WATER (layer_type 0) or SUBTERRANEAN_CHASM; options.spheres = {CAVERNS} + {WATER if water layer} + one random evil sphere; is_evil=true; sickness 'beast sickness'; strong_attack_tweak=true",
      "3. populate_sphere_info -> emits [SPHERE:X] per sphere",
      "4. get_random_creature_profile(options) -> weighted pick from random_creature_types (235 profiles; base table pushed by C++, Lua-extendable); is_valid_random_creature gates water/humanoidable/good/beast lists",
      "5. add_body_size(max(10000000 cm3, rcp.min_size)) + [CREATURE_TILE:<rcp.tile>]",
      "6. build_procgen_creature(rcp, tbl, options) = build_body_from_rcp + build_description + build_pcg_graphics"
    ],
    "build_body_from_rcp": [
      "a. body_base_fun[rcp.body_base] -> RCP_* body part list + sets pcg_layering_base (BEAST_INSECT/SPIDER/SCORPION/SNAKE/WORM_LONG/WORM_SHORT/AMORPHOUS/HUMANOID/BIPEDAL_DINOSAUR/QUADRUPED_BULKY/QUADRUPED_SLINKY/FRONT_GRASP/WALRUS) + walk gait variant + base walk speed; QUADRUPED has 1-in-20 to grow SIX_LEGGED or EIGHT_LEGGED",
      "b. rcp.must_have_* parts added unconditionally (wings/tail/shell/trunk/antennae/horns/mandibles/pincers/claw_arms/mantis_arms/stingers/proboscis); otherwise pushed as tweak candidates",
      "c. btc1_tweaks loop; then ONE primary tweak (options.btc) picked from candidates -> tweaks[btc].body() mutates the part list (WINGS, WINGS_FLIGHTLESS, TAIL, SHELL, TRUNK, ANTENNAE, HEAD_HORNS, LARGE_MANDIBLES, SIX_LEGGED, EIGHT_LEGGED, MAKE_HUMANOID, ...)",
      "d. digits: rcp.front_digits/rear_digits (2-5) -> RCP_n_FINGERS/FRONT_TOES/REAR_TOES; hoof/paw BODYGLOSS",
      "e. MATERIAL CLASS: options.r_class = rcp.c_class; 1-in-20 flip to UNIFORM for any non-uniform class (or forced by sphere_rcm for titans/demons/angels, blocked by never_uniform for bogeymen/nightmares); r_class_table = random_creature_class[r_class] merges features (eyes/heart/guts/blood...) into options",
      "f. secondary tweak btc2 from r_class tweaks + evil_tweaks (SKINLESS, BEAK_MISSING, NOSE_MISSING, RIBS_EXTERNAL, LIDLESS_EYES) + good_tweaks + eye variants (NO_EYES/ONE_EYE/THREE_EYES); default TWO_EYES otherwise",
      "g. glowing eyes 1-in-10 (werebeasts always): [GLOWTILE][GLOWCOLOR] + bright eye color",
      "h. forced stingers/proboscis at 1-in-20 each -> attack_tweak = TAIL_STINGER / INSECT_STINGER / PROBOSCIS_BLOOD",
      "i. emit [BODY:RCP_UPPER_BODY:...:RCP_HEAD:...] + [BODYGLOSS:...] + [CANOPENDOORS][EQUIPS] if RCP_TWO_PART_ARMS",
      "j. surface tweak (HAIR/FEATHERS/SCALES/SKIN/SKIN_BONES/EXOSKELETON/SKINLESS) emits USE_MATERIAL_TEMPLATE/USE_TISSUE_TEMPLATE + STATE_COLOR; horn/shell templates if present",
      "k. r_class body_plan: [BODY_DETAIL_PLAN:VERTEBRATE_TISSUE_LAYERS:SKIN|SCALE|NONE:FAT:MUSCLE:BONE:CARTILAGE] or [EXOSKELETON_TISSUE_LAYERS:CHITIN|SKIN:FAT:MUSCLE] + SINEW tendons/ligaments + HAS_NERVES; UNIFORM instead emits one TISSUE:UNIFORM_TIS over the WHOLE body from the picked material",
      "l. UNIFORM material pick: random_creature_material table (18 families) alignment-gated; sphere-linked via sphere_random_creature_materials (DEATH->ASH, FIRE->ASH|FLAME, CAVERNS->ANY_MINERAL...) or ANY_MINERAL = random SPECIAL-flagged inorganic from the world's stone/gem/metal list",
      "m. [NOBREATHE] + [EXTRAVISION] if UNIFORM; HOMEOTHERM:10040 unless fixed_temp (snow/ice 9990, steam 10200, flame 25000); blood = BLOOD/ICHOR/GOO template via heart artery layer",
      "n. color pick from monotone color patterns, sphere-aware (DEATH/MISERY->grays/blacks, DARKNESS/NIGHT->dark blues); [STATE_COLOR:ALL_SOLID:<color>] on surface material; [COLOR:f:b:br]",
      "o. ATTACK TWEAK: strong_attack_tweak (FB/titan/demon) forces pick_random_conditional_pairs(attack_tweaks); apply() emits poison material + syndrome + CDI interaction tokens",
      "p. post_attack_tweaks: melee ATTACK tokens by body part (PUNCH on RCP_TWO_PART_ARMS, SNATCH on pincers/claw arms, bites, tail attacks)",
      "q. gaits: [APPLY_CREATURE_VARIATION:STANDARD_SWIMMING_GAITS:...] unless cannot_swim; STANDARD_FLYING_GAITS + [FLIER] if wings; walk variant by body base; STANDARD_CRAWLING_GAITS always; STANDARD_CLIMBING_GAITS if any climbing part",
      "r. pcg_layering extras: QUILLS/PLATES 1-in-5 (or forced by profile), EXTERNAL_RIBS, BEAK layer for snake/dino/humanoid bases, MANDIBLES layers; 5 decoration slots coin-flipped"
    ],
    "build_description": "[DESCRIPTION: size adjective + btc/btc2 adjectives + rcp.name_string + form_desc (twisted_desc if evil) + post_mat_adj 'composed of X' + flavor line (default/good/evil pools, sphere-gated) + 'Its eyes glow <color>' + attack tweak warning 'Beware its webs/fire/deadly dust!'] + [PREFSTRING:...] + optional [ODOR_STRING]/[ODOR_LEVEL:90]",
    "build_pcg_graphics": "[PROCEDURAL_CREATURE_GRAPHICS:DEFAULT] + ordered [PCG_LAYERING:BEAST_*] (base, decorations, wings lacy/feathered/bat BACK|FRONT, shell BACK|FRONT, tail ONE|TWO|THREE, trunk, antennae, horns1/2, quills, plates, external ribs, eyes ONE|TWO|THREE) + [USE_COLOR_PALETTE:<color>] per layer; body_size<=500000 swaps BEAST_* to BEAST_SMALL_*; organic surfaces add BEAST_ORGANIC_* layers; separate portrait pass for experiments"
  },

  "never_repeating_combinatorics": {
    "creature_profiles": "235 weighted profiles: insects 44 (w22 each), arachnids 5 (w200-250), crustaceans 3, worms/molluscs 8, amphibians 4, reptiles 25, birds 73, mammals 69, plus GENERAL_BLOB/QUADRUPED/HUMANOID (w1000 each)",
    "body_bases": 17,
    "leg_variants": "quadruped -> 4/6/8 legs (1-in-20)",
    "primary_tweaks": "ONE of ~26 btc tweaks",
    "secondary_tweaks": "ONE of ~10 per r_class (+evil/good/eye extras)",
    "material_flip": "1-in-20 any creature becomes UNIFORM (single-material body, 18 material families incl. ANY_MINERAL/GEM/METAL/SOIL drawn from the world's own inorganics)",
    "attack_tweaks": "10 classes x poison state (LIQUID/GAS/SOLID_POWDER) x randomized syndrome (up to 5 of 17 CE_ effects, random severity/timing/organ targeting)",
    "spheres": "CAVERNS + WATER + 1 evil sphere per FB; spheres drive color pools, material pools, description flavor",
    "colors": "sphere-filtered monotone color patterns for surface + glowing eye color",
    "graphics": "layered PCG sprite composition (5 decoration slots, wing type, shell side, tail count, horn count)"
  },

  "creature_profile_flags_vocabulary": {
    "must_have": ["insect_wings","antennae","insect_stinger","poison_bite","webs","pincers","scorpion_tail","grabbing_claws","crustacean_tail","giant_mandibles","one_head_horn","shell","mantis_arms","suck_blood_through_proboscis","suck_blood_through_mouth","walrus_flippers","tail","feather_tail","skin_wings","feather_wings","quills","plates","elephant_trunk"],
    "cannot_have": ["tail","shell","get_more_legs","antennae","mandibles"],
    "other": ["always_flightless","requires_flexible_material (blob: forces UNIFORM non-solid)","front_digits/rear_digits 2-5","default_hoof_gloss/paw_gloss/claws/talons/nails","min_size (cm^3; FB floor 10,000,000)"]
  },

  "random_creature_class_material_classes": {
    "MAMMAL": {"surface":"HAIR","count":69,"features":"eyes nose cheeks lungs heart guts throat spine neck brain skull mouth teeth ribs eyelids tongue blood","tissue_plan":"VERTEBRATE_TISSUE_LAYERS:SKIN:FAT:MUSCLE:BONE:CARTILAGE","tweaks":["FEATHERS","SCALES"],"evil_tweaks":["SKINLESS"]},
    "CHITIN_EXO": {"surface":"EXOSKELETON","count":52,"features":"eyes heart guts brain mouth ichor","tissue_plan":"EXOSKELETON_TISSUE_LAYERS:CHITIN:FAT:MUSCLE","tweaks":["HAIR","FEATHERS","SCALES"]},
    "FLESHY": {"surface":"SKIN","count":8,"features":"heart guts brain mouth ichor","tissue_plan":"EXOSKELETON_TISSUE_LAYERS:SKIN:FAT:MUSCLE (no bones)","tweaks":["HAIR","FEATHERS","SCALES"]},
    "AMPHIBIAN": {"surface":"SKIN_BONES","count":4,"features":"full vertebrate set, blood","tissue_plan":"VERTEBRATE_TISSUE_LAYERS","tweaks":["HAIR","FEATHERS","SCALES"],"evil_tweaks":["SKINLESS"]},
    "REPTILE": {"surface":"SCALES","count":25,"features":"full vertebrate set, teeth","tissue_plan":"VERTEBRATE_TISSUE_LAYERS:SCALE:...","material_template":"SCALE:SCALE_TEMPLATE"},
    "REPTILE_FEATHERED": {"surface":"FEATHERS","count":1},
    "AVIAN": {"surface":"FEATHERS","count":73,"features":"beak instead of mouth, no teeth","tweaks":"none (flight/species recognition)"},
    "UNIFORM": {"surface":None,"count":3,"body_plan":"single TISSUE:UNIFORM_TIS from picked material over ALL body parts, NOT_LIVING NOT_BUTCHERABLE NOBREATHE EXTRAVISION; flame material grants built-in fireball+firejet+FIREEIMMUNE_SUPER"}
  },

  "uniform_body_materials": {
    "_note": "random_creature_material table; UNIFORM creatures are 'composed of X'; evil-gated entries only roll for evil creatures",
    "inorganic_pick": ["ANY_MINERAL","ANY_SOIL","ANY_GEM","ANY_METAL (random SPECIAL-flagged inorganic from world gen list)"],
    "matter": {
      "ASH": "ash/shadow/soot/embers/cinders; smoke_mat, INTANGIBLE, odor soot",
      "MUD": "mud/sludge/muck; dust_mat",
      "VOMIT": "evil only; prefstring 'disgusting appearance'",
      "SALT_POWDER": "salt/brine; INTANGIBLE powder",
      "GRIME": "filth/grime; miasma_mat, odor filth",
      "SNOW": "fixed_temp 9990, INTANGIBLE, possible name suffix ' of tears'",
      "WATER": "water/rain; mist_mat",
      "STEAM": "fixed_temp 10200, INTANGIBLE, fog_mat",
      "FLAME": "fixed_temp 25000, INTANGIBLE, fire_mat -> built-in FIREBALL + FIREJET interactions",
      "AMBER": "solid",
      "CORAL": "solid",
      "GLASS_GREEN|GLASS_CLEAR|GLASS_CRYSTAL": "solid glass bodies",
      "CHARCOAL|COKE": "evil only; odor soot",
      "SALT_SOLID": "solid salt",
      "ICE": "fixed_temp 9990"
    },
    "insubstantial_set": ["ASH","SALT_POWDER","SNOW","STEAM","FLAME"],
    "sphere_material_map": {
      "MUCK": ["MUD"], "FIRE": ["ASH","FLAME"], "DEPRAVITY": ["VOMIT"],
      "DISEASE": ["VOMIT","GRIME"], "BLIGHT": ["VOMIT","GRIME"],
      "SALT": ["SALT_POWDER","SALT_SOLID"], "ART|BEAUTY|RAINBOWS": ["GLASS_*"],
      "EARTH": ["ANY_SOIL"], "CAVERNS|MINERALS": ["ANY_MINERAL"], "CHAOS": ["FLAME","STEAM"],
      "DARKNESS|DEATH": ["ASH"], "COASTS": ["CORAL"], "PLANTS|TREES|NATURE": ["AMBER"],
      "JEWELS": ["ANY_GEM"], "METALS": ["ANY_METAL"], "MIST": ["STEAM"],
      "MOUNTAINS": ["SNOW","ICE","ANY_MINERAL"], "OCEANS": ["WATER","SALT_*"],
      "LAKES|RAIN|RIVERS|STORMS": ["WATER"], "VOLCANOS": ["FLAME","ANY_MINERAL"],
      "WATER|WEATHER": ["SNOW","ICE","WATER","STEAM"]
    }
  },

  "attack_tweaks": {
    "_note": "attack_tweaks table shared_info.lua:5092; FB/titan/demon set strong_attack_tweak=true so one is ALWAYS applied (unless good/intangible); spiders force WEBS via must_have_webs",
    "TAIL_STINGER": {"trigger":"tail + 1-in-20, or scorpion profile (forced)","grants":"CREATURE_EXTRACT_TEMPLATE POISON (LIQUID) + syndrome + tail sting attack","warning":"Beware its poisonous sting!"},
    "INSECT_STINGER": {"trigger":"lower body stinger (wasp/bee profiles forced, or 1-in-20)","grants":"extract poison syndrome","warning":"Beware its poisonous sting!"},
    "FIRE": {"trigger":"has mouth/beak; roll: fireball only, firejet only, or both","grants":"[CDI:FLOW:FIREBALL] range 15 / [CDI:FLOW:FIREJET] range 5 + FIREIMMUNE","warning":"Beware its fire!"},
    "WEBS": {"grants":"[THICKWEB][WEBIMMUNE] SILK_TEMPLATE + [WEBBER:LOCAL_CREATURE_MAT:SILK] + CDI Spray web (WEB_SPRAY, range 5)","warning":"Beware its webs!"},
    "BREATHE_TRAILING_FLOW": {"trigger":"evil only","grants":"extract POISON as LIQUID(vapor)/GAS(gas)/SOLID_POWDER(dust) TRAILING_*_FLOW CDI","warning":"Beware its poisonous vapors/gas/deadly dust!"},
    "BREATHE_GLOB": {"grants":"POISON LIQUID/SOLID_POWDER *_GLOB spit CDI","warning":"Beware its deadly spittle!"},
    "BREATHE_UNDIRECTED": {"trigger":"evil only","grants":"POISON UNDIRECTED_VAPOR/GAS/DUST cloud around self","warning":"Beware its poisonous vapors/gas/deadly dust!"},
    "SECRETION": {"trigger":"evil/experiment + solid surface body","grants":"[SECRETION:LOCAL_CREATURE_MAT:POISON:<state>:BY_CATEGORY:ALL:<surface>]","warning":"Beware its noxious secretions!"},
    "POISON_BLOOD": {"trigger":"evil/experiment + blood/ichor/goo","grants":"poison syndrome on own BLOOD/ICHOR/GOO material","warning":"Beware its deadly blood!"},
    "POISON_BITE": {"grants":"extract POISON LIQUID + bite injection","warning":"Beware its poisonous bite!"},
    "PROBOSCIS_BLOOD": {"grants":"blood-sucking proboscis attack","warning":"Beware its hunger for warm blood!"}
  },

  "poison_system": {
    "material_template": "CREATURE_EXTRACT_TEMPLATE (material_template_default.txt:2589): white extract; states liquid 'extract', solid 'frozen extract', gas 'boiling extract'; ENTERS_BLOOD; value 1",
    "states": {"LIQUID":"default extract","GAS":"MELTING_POINT:9800 BOILING_POINT:9900","SOLID_POWDER":"MELTING_POINT:10200 BOILING_POINT:10400"},
    "syndrome_scaffold": "[SYNDROME] SYN_AFFECTED_CLASS:GENERAL_POISON + SYN_IMMUNE_CREATURE:<self> + SYN_INJECTED/SYN_CONTACT/SYN_INHALED/SYN_INGESTED",
    "effect_pool": ["CE_PAIN","CE_SWELLING","CE_OOZING","CE_BRUISING","CE_BLISTERS","CE_NUMBNESS","CE_PARALYSIS","CE_FEVER","CE_BLEEDING","CE_COUGH_BLOOD","CE_VOMIT_BLOOD","CE_NAUSEA","CE_UNCONSCIOUSNESS","CE_NECROSIS","CE_IMPAIR_FUNCTION","CE_DROWSINESS","CE_DIZZINESS"],
    "randomization": "add_base_poison_effects: 1-5 distinct effects, random start/peak/end windows, 1-in-30 permanent (no END), RESISTABLE 1-in-30, SIZE_DELAYS/SIZE_DILUTES rolls; NECROSIS/IMPAIR_FUNCTION randomly LOCALIZED or organ-targeted (15 organ categories incl. BRAIN, HEART)"
  },

  "interactions": {
    "static_raws": {
      "file": "vanilla_interactions/objects/interaction_standard.txt",
      "count": 5,
      "list": ["CLEANING (I_EFFECT:CLEAN)","BP_BUMP (CONTACT)","PET_ANIMAL (CONTACT, forbidden CAN_LEARN)","MATERIAL_EMISSION (creature_action emission; template all generated sprays ride on)","MATERIAL_EMISSION_WITH_HIDE_EFFECT (emission + HIDE, IE_LOCATION:IN_WATER)"]
    },
    "generator_count": 30,
    "table": [
      {"family":"curse (deity)","count":3,"generators":["minor.bad_luck","medium.become_beast","major.vampire"]},
      {"family":"blessing (deity)","count":5,"generators":["minor.luck","medium.holy_item","medium.improve_equipment","medium.pet","medium.healing"]},
      {"family":"disturbance (mummy tomb)","count":1,"generators":["default: resurrect-as-mummy with Curse + Animate corpse + Raise lieutenant sub-interactions"]},
      {"family":"secret (necromancy)","count":1,"generators":["necromancer"]},
      {"family":"were-curse (deity)","count":1,"generators":["werebeast_origin_interactions.default + _BITE variant"]},
      {"family":"mythical (dread path)","count":14,"generators":["mythical.default (dread lord branding syndrome)","13 mythical_item_powers"]},
      {"family":"powers (lieutenant powers)","count":4,"generators":["ice bolt","vanish","propel away","raise fog"]},
      {"family":"regional (evil biome)","count":1,"generators":["regional.animate (weekly corpse reanimation in evil regions)"]}
    ],
    "grants_detail": {
      "vampire_curse": {
        "source":"I_SOURCE:INGESTION (tainted blood); targets CAN_LEARN+HAS_BLOOD; forbidden NOT_LIVING/SUPERNATURAL; mutually exclusive vs WERECURSE/VAMPCURSE/DISTURBANCE_CURSE/RAISED_UNDEAD/RAISED_GHOST/GHOUL syndrome classes",
        "grants":"SYN_CLASS:VAMPCURSE; BLOODSUCKER NO_AGING STERILE NOT_LIVING NOEXERT NOPAIN NOBREATHE NOSTUN NONAUSEA NO_DIZZINESS NO_FEVERS PARALYZEIMMUNE NO_EAT NO_DRINK NO_SLEEP NO_PHYS_ATT_GAIN/RUST; STR/AGI/TOU doubled (200); CE_MATERIAL_FORCE_MULTIPLIER 1:2 (takes half damage); own blood becomes infectious vector (CE_BODY_MAT_INTERACTION RESERVED_BLOOD, spread via ingested/injected); tooth length +150% (fangs, gated on COUNTER_TRIGGER:DRINKING_BLOOD); display name 'vampire'; senses GENERAL_POISON class"
      },
      "necromancy_secret": {
        "source":"IS_SECRET:SUPERNATURAL_LEARNING_POSSIBLE + mundane research/teaching/recording (BOOK_INSTRUCTION:SECRET_DEATH); goal IMMORTALITY; sphere DEATH (+NIGHTMARES if summoner)",
        "grants":"SYN_CLASS:NECROMANCER; NO_AGING NO_EAT NO_DRINK NO_SLEEP NOEXERT NO_PHYS_ATT_GAIN/RUST (+NIGHT_CREATURE_EXPERIMENTER 1-in-3); personality flip (anxiety +50, trust -50); CDI Animate corpse; THEN at least one of: Raise lieutenant (resurrects corpses as RAISED_UNDEAD servants with lieutenant powers; named from 33 adjectives x 8 nouns, e.g. 'fell ghoul'), Summon bogeymen/nightmare (SUMMON_UNIT by caste flag, cooldown 200-300 / 12000), Create ghoul (EXPERIMENT_ONLY contagious bite, OPPOSED_TO_LIFE, random speed debuff); ghost-raising code present but disabled (if false)"
      },
      "were_curse": {
        "source":"I_SOURCE:DEITY (major curse hint) + I_SOURCE:ATTACK (bite variant)",
        "grants":"SYN_CLASS:WERECURSE; CE_BODY_TRANSFORMATION to the generated werebeast creature token; CE:PERIODIC:MOON_PHASE:27:0 (full moon); NO_AGING; deity-source immediate, bite-source delayed START:16800 (~16 days); same mutual-exclusion block; the werebeast ITSELF is an RCP creature (beast_only, humanoidable_only, prioritize_bite, CRAZED, NO_GENDER, BONECARN, combat skills 6, SNEAK 20, DIFFICULTY 3, LAIR SIMPLE_BURROW) with a per-world profile blacklist so were-forms never repeat"
      },
      "mummy_disturbance": {
        "source":"I_SOURCE:DISTURBANCE on corpse (FIT_FOR_RESURRECTION CAN_LEARN CAN_SPEAK)",
        "grants":"resurrect as mummy (STR/TOU 300, NOT_LIVING full undead tag set, vengeful +100 personality); carries 3 CDIs: Curse (week-long CE_SKILL_ROLL_ADJUST PERC:0 PERC_ON:20), Animate corpse, Raise <adjective noun> lieutenant; names from 13 tomb adjectives x 8 nouns"
      },
      "deity_minor_medium": {
        "bad_luck":"CE_SKILL_ROLL_ADJUST PERC:0 PERC_ON:20, one week (8400 ticks)",
        "become_beast":"CE_BODY_TRANSFORMATION into random NATURAL_ANIMAL (megabeast/demon/etc forbidden) one week + NO_AGING/NO_EAT/NO_DRINK + fast effortless gait",
        "luck":"CE_SKILL_ROLL_ADJUST PERC:150 PERC_ON:50 one week",
        "holy_item":"CREATE_ITEM artifact-quality weapon (1/3) / shield (1/3) / armor piece",
        "improve_equipment":"IE_CHANGE_QUALITY:+2 on carried gear",
        "pet":"SUMMON_UNIT random LARGE_PREDATOR natural animal, IE_MAKE_PET_IF_POSSIBLE",
        "healing":"full CE heal bundle (STOP_BLEEDING, CLOSE_OPEN_WOUNDS, HEAL_TISSUES, HEAL_NERVES, REGROW_PARTS, CURE_INFECTION, reduce pain/swelling/paralysis...) 12-tick burst"
      },
      "mythical_item_powers": ["ice_bolt","propel","pain","blisters","paralysis","bleeding","cough_blood","vomit_blood","nausea","necrosis","blind","suffocate","dizziness"],
      "lieutenant_powers": ["launch ice bolt (WATER:SHARP_ROCK material emission)","vanish (HIDE)","propel away (PROPEL_UNIT force 100000)","raise fog (CHANGE_WEATHER FOG_THICK) + randomized curse touches (PAIN/BLISTERS/PARALYSIS/BLEEDING/SICKEN/NECROSIS/IMPAIR/DIZZY)"],
      "evil_region_weather": "evil.lua: clouds named '<adj> mist/dust/ash/soot/fog/gloom/murk/smoke/vapor' (19 adjectives); 50% living-death (husk/zombie/thrall renaming + full undead tag set) else poison burst; evil rain '<adj> slime/goo/mucus/ooze/sludge/filth/muck/slush' (18 adjectives) mild poison"
    }
  },

  "creature_variation_static_weaving": {
    "_note": "the ANIMAL_PERSON / GIANT side: static CV templates in vanilla_creatures/objects/c_variation_default.txt applied to real animals (the procedural Lua path handles megabeasts; CV handles animal people)",
    "pattern": "[CREATURE:TOAD_MAN] [COPY_TAGS_FROM:TOAD] [APPLY_CREATURE_VARIATION:ANIMAL_PERSON] [GO_TO_END] castes rename",
    "ANIMAL_PERSON_chain": "CV_REMOVE_TAG x49 (NAME/PET/ATTACK*/GAIT/VERMIN_*/MAXAGE/SPEED...) + CV_CONVERT_TAG body swaps (QUADRUPED->HUMANOID, QUADRUPED_NECK->HUMANOID_NECK:3FINGERS, ...) + civ-level additions (CAN_LEARN CAN_SPEAK)",
    "GIANT_variation": "same strip + size multiplier, keeps animal body",
    "attack_variations": ["MOUTH_BITE_ATTACK","MOUTH_BITE_EDGE_ATTACK","MOUTH_BITE_VENOM_ATTACK","TOOTH_BITE_ATTACK","TOOTH_BITE_VENOM_ATTACK","TOOTH_WHORL_BITE_ATTACK","BEAK_BITE_ATTACK","PROBOSCIS_BITE_ATTACK","PROBOSCIS_SUCK_ATTACK","MOUTH_SUCK_ATTACK","CLAW_SCRATCH_ATTACK","NAIL_SCRATCH_ATTACK","TALON_SCRATCH_ATTACK","PUNCH_ATTACK","KICK_ATTACK","KICK_HIGHVEL_ATTACK","HOOF_ATTACK","HORN_ATTACK","TUSK_STAB_ATTACK","TAIL_ATTACK","TAIL_STING_VENOM_ATTACK","PINCER_ATTACK","ARM_LOWER_SNATCH_ATTACK"],
    "gait_variations": ["STANDARD_WALKING_GAITS","STANDARD_QUADRUPED_GAITS","STANDARD_BIPED_GAITS","STANDARD_FLYING_GAITS","STANDARD_SWIMMING_GAITS","STANDARD_CRAWLING_GAITS","STANDARD_CLIMBING_GAITS","STANDARD_WALK_CRAWL_GAITS"]
  },

  "creature_profiles": profiles,

  "key_files": {
    "rcp_lua": "C:/Program Files (x86)/Steam/steamapps/common/Dwarf Fortress/data/vanilla/vanilla_procedural/scripts/generators/creatures/rcp.lua (235-profile table + body_base_fun + get_random_creature_profile)",
    "shared_info_lua": "C:/Program Files (x86)/Steam/steamapps/common/Dwarf Fortress/data/vanilla/vanilla_procedural/scripts/generators/creatures/shared_info.lua (tweaks:3841, sphere mats:3694, random_creature_material:4284, random_creature_class:4630, add_poison_bits:5052, attack_tweaks:5092, build_body_from_rcp:5698, build_description:6438, build_pcg_graphics:6567, build_procgen_creature:6994)",
    "creatures_lua": "C:/Program Files (x86)/Steam/steamapps/common/Dwarf Fortress/data/vanilla/vanilla_procedural/scripts/generators/creatures.lua (creatures.fb.default:154, titan:194, demon:270, werebeast:1126, experiments:1254)"
  }
}

out = os.path.join(os.path.dirname(__file__), "df_procedural.json")
json.dump(doc, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
os.remove(TMP)
print("wrote", out, os.path.getsize(out), "bytes,", len(profiles), "profiles")
