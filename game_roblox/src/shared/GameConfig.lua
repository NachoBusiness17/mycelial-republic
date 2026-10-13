--[[
    THE LEDGER OF EMPTY CHAIRS
    GameConfig — shared constants and world state

    Standing law: Never state the truth. Hint. Let the player connect it themselves.
    The game is a tool for the vigilant, not a substitute sovereign.
    The system does not require belief in the lie — only that you become too tired
    to keep pointing at the empty chairs.
]]

local GameConfig = {}

-- ── World constants ──────────────────────────────────────────────────
GameConfig.WORLD_NAME = "The Ledger of Empty Chairs"
GameConfig.VERSION = "0.1.0"
GameConfig.CHAIR_COUNT = 6

-- ── Boss: The Answer (5 phases) ──────────────────────────────────────
GameConfig.BOSS = {
    NAME = "The Answer",
    TOTAL_PHASES = 5,
    WING_CHUN_STEP_DEGREES = 15.0,   -- the corpus's angle, the tell
    PHASES = {
        [1] = { name = "The Fall",    hint = "Winning was the mistake." },
        [2] = { name = "The Suit",    hint = "Accumulation was always the leash." },
        [3] = { name = "Wing Chun",   hint = "Blocking feeds it. Count the steps." },
        [4] = { name = "The Fold",    hint = "Aim at the empty point." },
        [5] = { name = "Blue Light",  hint = "Stand it under the light." },
    },
}

-- ── Virtue Marks (the cage) ─────────────────────────────────────────
GameConfig.VIRTUE_MARKS = {
    COUNTER_INTERVAL = 10,          -- seconds between passive counts
    COUNT_REWARD = 1,               -- marks earned per chair counted
    MURAL_WEEP_THRESHOLD = 3,       -- ignore chairs this many cycles → mural weeps
}

-- ── Shadow Ledger (what the hall records) ────────────────────────────
GameConfig.SHADOW_LEDGER = {
    ENTRY_TYPES = {
        COUNTED = "counted",         -- player pointed at the empty chairs
        IGNORED = "ignored",         -- player walked past
        SAT_DOWN = "sat_down",       -- player took a chair
        SPOKE = "spoke",             -- player said the count aloud
    },
}

-- ── Rashomon Filter (the five tells) ─────────────────────────────────
GameConfig.RASHOMON_TELLS = {
    TEARS = "tears",                 -- instant emotional regression
    ARCHETYPE = "archetype",         -- clean hero / clean monster
    PHRASE_CLONE = "phrase_clone",   -- identical slogans from unrelated mouths
    SPEED = "speed",                 -- saturation in hours, not days
    PUNISHMENT = "punishment",       -- doubt feels like hurting the victim
}

-- ── Narrative fragments (hinted, never stated) ───────────────────────
GameConfig.NARRATIVE = {
    BROTHER_VELLUM = "Brother Vellum, of the Open Hand, smiles a Grant of Belonging.",
    GRANT_TEXT = "The Open Hand sees you. Your seat is ready. Simply sign.",
    LEDGER_SCRAP = "A salt-cellar scrap, three names, same hand as the roll.",
    MURAL_WEEPS = "The mural weeps cloned tears.",
    HALL_FILES = "The hall files which you chose.",
    CANDLE_LIT = "A candle lights itself beside the empty chair.",
    CANDLE_UNLIT = "One chair remains dark.",
}

-- ── Realm structure (unlock as players progress) ─────────────────────
GameConfig.REALMS = {
    { name = "Hall of Shared Supper",  unlockLevel = 0,  chairs = 6 },
    { name = "The Long Corridor",      unlockLevel = 1,  chairs = 12 },
    { name = "The Counting House",     unlockLevel = 3,  chairs = 20 },
    { name = "The Garden of Grades",   unlockLevel = 5,  chairs = 30 },
    { name = "The Cellar",             unlockLevel = 8,  chairs = 1  },
}

return GameConfig
