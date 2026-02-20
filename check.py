import requests
import itertools
import csv
import time

# ==============================
# CONFIG
# ==============================
TLD = ".com"
BATCH_SIZE = 40
SLEEP_BETWEEN_BATCHES = 0.50
OUTPUT_CSV = "combo500_results.csv"

HEADERS = { 
    'User-Agent': "Mozilla/5.0 (Linux; Android 10)",
    'Accept': "application/json"
}

BASE_URL = "https://domains.revved.com/v1/domainStatus"
RCS_PARAM = "Mms%2FKCVrc3hxcHl5ent%2FcH5laydrc2t%2BeSx7LS9%2BcXF%2BfXhxfHt4LX8qLS15f3BxenlxKn1%2Ff2s0"


# ==============================
# PREMIUM EXACT-MATCH WORD LIST (300 words)
# ==============================
WORDS = [
    "abbey", "abide", "abler", "abode", "abort", "about", "above", "abuse", "abyss", "acids",
    "acorn", "acres", "acted", "acute", "adage", "adapt", "added", "adept", "admit", "adobe",
    "adopt", "adorn", "adult", "aegis", "aeons", "after", "again", "agate", "agile", "aging",
    "aglow", "agony", "agree", "ahead", "aided", "aisle", "alarm", "album", "algae", "alien",
    "align", "alike", "allay", "alley", "allot", "allow", "aloft", "along", "aloof", "altar",
    "alter", "amber", "amble", "amend", "amiss", "ample", "angel", "anger", "angle", "angry",
    "angst", "annex", "antic", "anvil", "aorta", "apart", "aphid", "apple", "apply", "aptly",
    "arbor", "ardor", "arena", "argon", "arise", "armed", "aroma", "arose", "array", "arson",
    "aside", "asked", "atlas", "attic", "audit", "avail", "avian", "avoid", "awake", "award",
    "aware", "awful", "azure", "backs", "badge", "badly", "bagel", "balls", "banal", "basic",
    "basis", "batch", "beach", "beady", "begun", "being", "below", "bench", "bends", "berth",
    "birth", "bison", "black", "blade", "blame", "bland", "blank", "blare", "blast", "blaze",
    "bleak", "bleat", "blend", "bless", "blind", "bliss", "bloat", "block", "blood", "bloom",
    "blown", "blunt", "blurb", "blurt", "board", "bonus", "boost", "booth", "bound", "boxer",
    "brace", "brand", "brave", "break", "breed", "brick", "bride", "brief", "bring", "brisk",
    "broad", "brook", "broom", "broth", "brown", "brush", "build", "built", "bulky", "bunch",
    "burst", "buyer", "bylaw", "cabal", "cabin", "cable", "camel", "candy", "carry", "carve",
    "catch", "cause", "cease", "cedar", "cells", "cents", "chaos", "charm", "chase", "cheap",
    "check", "cheek", "chess", "chest", "chief", "child", "chips", "civic", "civil", "clamp",
    "clang", "clash", "class", "clean", "clear", "clerk", "click", "cliff", "climb", "cling",
    "clock", "clone", "close", "cloth", "cloud", "clout", "coach", "coast", "color", "comet",
    "coral", "cover", "covet", "craft", "crash", "creak", "cream", "creed", "crime", "crimp",
    "crisp", "croak", "cross", "cruel", "crush", "curve", "cycle", "cynic", "daily", "daisy",
    "dance", "datum", "death", "debut", "decoy", "delay", "delta", "dense", "depot", "depth",
    "derby", "devil", "digit", "diner", "dirty", "disco", "dodge", "doors", "doubt", "dough",
    "draft", "drain", "drama", "drank", "drape", "drawl", "drawn", "dread", "dress", "dried",
    "drift", "drink", "drive", "drone", "drove", "dryer", "dunes", "dying", "eagle", "eager",
    "early", "eight", "elite", "ember", "emcee", "empty", "enemy", "enjoy", "enter", "entry",
    "equal", "error", "essay", "event", "every", "exact", "exist", "extra", "fable", "faced",
    "faith", "falls", "false", "fancy", "fatal", "fault", "feast", "flair", "fence", "fever",
    "fewer", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed", "fjord",
    "flare", "flash", "fleet", "flesh", "flies", "float", "flock", "flood", "flora", "floss",
    "flour", "fluid", "flush", "focus", "force", "forge", "forth", "forum", "found", "frank",
    "fraud", "fresh", "frost", "froze", "fully", "funds", "fungi", "funny", "gauge", "ghost",
    "given", "gland", "glare", "glass", "glide", "gloss", "glove", "going", "grace", "grade",
    "graph", "grasp", "grass", "grave", "graze", "greet", "grief", "grind", "groan", "gross",
    "group", "grove", "growl", "grown", "guard", "guide", "guile", "guise", "gusto", "habit",
    "happy", "harsh", "haven", "hawks", "heads", "heard", "heart", "heavy", "hence", "herbs",
    "hinge", "hippo", "holds", "holly", "homer", "honey", "honor", "hooks", "horse", "hotel",
    "hours", "human", "humor", "hurry", "hyena", "ideal", "image", "imply", "index", "indie",
    "infer", "inner", "input", "inter", "intro", "irony", "issue", "ivory", "jazzy", "jewel",
    "joint", "joker", "joust", "judge", "juice", "juicy", "jumbo", "karma", "kayak", "keeps",
    "knack", "knife", "knock", "known", "label", "large", "laser", "later", "laugh", "layer",
    "leads", "learn", "lease", "least", "leave", "legal", "level", "limit", "lined", "links",
    "liver", "logic", "loose", "lover", "lower", "lucky", "lunar", "lunch", "lyric", "magic",
    "major", "maker", "manor", "maple", "march", "match", "mayor", "media", "mercy", "merit",
    "metal", "micro", "might", "minor", "minus", "mixed", "model", "money", "monks", "month",
    "moral", "motor", "mouse", "mouth", "moved", "movie", "music", "nasal", "nerve", "never",
    "night", "noble", "noise", "north", "noted", "novel", "nurse", "nymph", "occur", "offer",
    "often", "olive", "onset", "opera", "order", "other", "outer", "oxide", "ozone", "oasis",
    "paced", "panel", "panic", "paper", "party", "pasta", "patch", "pause", "pearl", "penny",
    "phase", "phone", "photo", "piano", "pilot", "pitch", "pixel", "pizza", "plain", "plane",
    "plant", "plate", "plaza", "plumb", "plume", "point", "polar", "poppy", "porch", "posed",
    "power", "press", "price", "pride", "prime", "print", "prior", "prize", "probe", "prone",
    "proof", "prose", "proud", "prove", "proxy", "pulse", "pupil", "purse", "queen", "quest",
    "queue", "quick", "quiet", "quota", "quote", "rabbi", "radar", "radio", "rainy", "rally",
    "ranch", "range", "rapid", "ratio", "reach", "react", "ready", "refer", "reign", "relax",
    "reply", "rider", "ridge", "right", "rigid", "risky", "rival", "river", "robot", "rocky",
    "rodeo", "rouge", "rough", "round", "route", "royal", "rugby", "ruler", "rural", "sadly",
    "saint", "salad", "sauce", "scale", "scary", "sedan", "sense", "serve", "setup", "seven",
    "shade", "shake", "shall", "shame", "share", "shark", "sharp", "sheep", "shelf", "shell",
    "shift", "shine", "shirt", "shoes", "shoot", "short", "shrug", "siege", "sight", "sigma",
    "silly", "since", "sixth", "skill", "skull", "slang", "slash", "slate", "slave", "sleep",
    "slice", "slide", "slime", "slope", "smart", "smell", "smile", "smith", "solid", "solve",
    "sound", "south", "spark", "spawn", "speak", "spear", "speed", "spell", "spend", "spine",
    "spite", "split", "spoke", "spore", "sport", "spray", "squad", "stack", "staff", "stage",
    "stain", "stair", "stale", "stall", "start", "state", "stays", "steam", "steep", "steer",
    "stern", "stick", "stiff", "still", "stock", "stone", "stood", "storm", "story", "stove",
    "strap", "straw", "stray", "strip", "stuck", "study", "stuff", "style", "sugar", "suite",
    "sunny", "super", "surge", "swift", "sword", "swore", "swung", "taxes", "tense", "tenth",
    "terms", "theft", "theme", "there", "thick", "thing", "think", "third", "thorn", "those",
    "three", "threw", "throw", "tiger", "tight", "timer", "tired", "title", "today", "token",
    "tools", "topic", "total", "touch", "tough", "towel", "tower", "toxic", "track", "trade",
    "trail", "trait", "trans", "trash", "treat", "trial", "tribe", "trick", "tried", "troop",
    "truck", "truly", "trust", "truth", "tumor", "tuner", "tunes", "tutor", "twice", "twist",
    "ultra", "under", "unify", "union", "unity", "until", "upper", "urban", "usage", "usual",
    "utter", "valid", "value", "valve", "vapor", "vault", "video", "vigor", "viral", "virus",
    "visit", "visor", "vital", "vivid", "vocal", "voice", "voter", "vowed", "wager", "waste",
    "watch", "weary", "wedge", "weird", "whale", "wheat", "where", "which", "while", "whole",
    "whose", "wider", "witch", "woman", "women", "worry", "worse", "worst", "worth", "would",
    "wound", "wrath", "wrist", "yacht", "yield", "young", "youth", "zebra", "zones", "zooms",
    "abaft", "aback", "abbey", "abbot", "abhor", "abide", "abler", "abode", "abort", "abuts",
    "abyss", "acorn", "acres", "acted", "acrid", "addax", "adder", "adieu", "adman", "admit",
    "adobe", "ailed", "aimed", "aired", "afoot", "afoul", "affix", "afar",  "agave", "agony",
    "agent", "agape", "aglow", "aghas", "agism", "algal", "allay", "alloy", "aloft", "aloof",
    "aloes", "alums", "amaze", "amber", "ambry", "amour", "ample", "amply", "amuck", "angel",
    "anise", "annoy", "antsy", "anvil", "aphid", "apnea", "apple", "apron", "ardor", "argot",
    "ashen", "aspen", "atone", "atilt", "atlas", "atoll", "atopy", "attic", "avow",  "awash",
    "awing", "awoke", "axial", "axion", "azote", "azure", "baggy", "bairn", "baize", "balmy",
    "banal", "bandy", "bangs", "baron", "basil", "basin", "baulk", "bayou", "beech", "begot",
    "belle", "bells", "belly", "beset", "bevel", "bezel", "bigot", "bilge", "blond", "bloke",
    "bogus", "bolar", "bolts", "bonus", "boney", "borax", "botch", "brash", "bravo", "brawl",
    "bream", "breve", "broil", "broke", "buxom", "byway", "cache", "cadet", "camel", "cameo",
    "canny", "cargo", "carob", "carol", "caste", "caulk", "cavil", "charm", "chasm", "chirp",
    "choir", "chore", "cinch", "cleft", "cling", "cloak", "clown", "cluck", "cobalt","codon",
    "coils", "combs", "cramp", "crank", "crass", "crimp", "crook", "crown", "crypt", "cubic",
    "curly", "cushy", "daffy", "dandy", "dapper","darts", "datum", "decal", "decoy", "decry",
    "delve", "depot", "derby", "deter", "diode", "dirge", "ditty", "divot", "dizzy", "dogma",
    "dolce", "dolls", "donor", "dorsal","dowdy", "dowel", "downy", "dowse", "drool", "droop",
    "drove", "drowse","duchy", "dusky", "dusty", "dwarf", "dwell", "dwelt", "eagle", "easel",
    "eaves", "ebony", "edict", "edify", "educe", "eerie", "egret", "elbow", "elder", "elect",
    "elegy", "elfin", "elide", "elope", "emote", "enact", "envoy", "epoch", "ergot", "evade",
    "evoke", "exile", "exude", "exult", "faded", "faint", "fatty", "favor", "feign", "felon",
    "femur", "ferny", "ferry", "fetch", "fetid", "feud",  "ficus", "fiery", "finch", "fishy",
    "fixer", "fizzy", "fjord", "flail", "flank", "flick", "flinch","flung", "flute", "foamy",
    "foggy", "folio", "folly", "foray", "forte", "forty", "foyer", "frail", "franc", "friar",
    "frond", "froze", "frugal","fugue", "furor", "fuzzy", "gaily", "gaudy", "gauze", "gavel",
    "gawky", "geeky", "genial","giddy", "gigas", "girth", "gloat", "gloom", "glory", "gloss",
    "glyph", "gnash", "gnome", "goofy", "goose", "gouge", "gourd", "graft", "grail", "gramp",
    "grant", "gravy", "greys", "grimy", "gripe", "gruff", "grump", "guava", "gummy", "gusto",
    "gypsy", "haiku", "handy", "hazel", "heist", "helix", "hippy", "hitch", "hoard", "hoary",
    "hobby", "holly", "homer", "horde", "horny", "hound", "howdy", "hulky", "husky", "hyena",
    "hyper", "idiom", "igloo", "irate", "inane", "inept", "ingot", "inked", "ionic", "irate",
    "irked", "itchy", "ivory", "jazzy", "jiffy", "jokey", "joust", "jumpy", "kaput", "kebab",
    "kinky", "kitty", "kneel", "knell", "knelt", "knobs", "knots", "kudos", "labor", "lance",
    "lanky", "lapel", "lapse", "larva", "latch", "lathe", "laxly", "leafy", "leaky", "leapt",
    "ledge", "leech", "lefty", "lemma", "lemon", "lemur", "libel", "liner", "lingo", "lipid",
    "lithe", "livid", "llama", "lodge", "lofty", "loner", "lorry", "lousy", "lusty", "lusty",
    "mange", "mania", "manly", "mangy", "manly", "manor", "mantra","marly", "mauve", "maxim",
    "melee", "melon", "mercy", "messy", "mimic", "minty", "mirky", "mirth", "miser", "mocha",
    "mogul", "moldy", "molten","moody", "moose", "moped", "moron", "mossy", "motif", "muddy",
    "muggy", "mulch", "mummy", "murky", "musty", "myrrh", "nadir", "naive", "nanny", "natty",
    "naval", "needy", "nifty", "ninja", "nippy", "nitro", "nonce", "nosey", "notch", "novice",
    "nifty", "nudge", "nutty", "nymph", "oddly", "offal", "optic", "orate", "orbit", "other",
    "otter", "outdo", "ovoid", "paddy", "pagan", "patio", "patsy", "patty", "pauze", "payee",
    "peach", "peaky", "peeve", "petal", "petty", "pewit", "picky", "piggy", "piney", "pixel",
    "plait", "pluck", "plunk", "plush", "poach", "poker", "polka", "polyp", "poppy", "porky",
    "posit", "potty", "pouch", "poult", "powny", "prank", "prawn", "prior", "privy", "privy",
    "prone", "prude", "prune", "psalm", "pubic", "pubis", "pudgy", "puffy", "pugil","pulpy",
    "putty", "pygmy", "quirk", "rabid", "raspy", "ratty", "raven", "rawer", "rayon", "rebus",
    "reedy", "refit", "regal", "relic", "renal", "repay", "repel", "rerun", "reuse", "revel",
    "rider", "ripen", "rivet", "robin", "roman", "roomy", "roost", "rowdy", "ruddy", "ruled",
    "rusty", "rutty", "sadly", "saggy", "sandy", "saner", "savvy", "scald", "scalp", "scant",
    "scare", "scorn", "scout", "scowl", "scram", "scrap", "scrub", "seedy", "seize", "sepoy",
    "serum", "shack", "shady", "shale", "shawl", "sheen", "shire", "shoat", "shoal", "shrub",
    "shuck", "shunt", "silky", "sissy", "sixty", "skimp", "skipy", "skirt", "sleet", "slick",
    "slimy", "slosh", "sloth", "slunk", "slurp", "slyly", "smear", "smite", "smock", "smolt",
    "snare", "sneak", "sneer", "snide", "snipy", "snore", "snort", "snowy", "soggy", "solar",
    "sooty", "sorry", "spasm", "speck", "spied", "spill", "spiny", "spook", "spoon", "spore",
    "spout", "spunk", "spurn", "spurt", "squat", "squid", "stark", "stash", "stead", "steed",
    "stoic", "stomp", "stoop", "storey","strap", "stray", "strut", "stubs", "stump", "stunk",
    "stunt", "suave", "sulky", "sumac", "surly", "swamp", "swath", "swear", "sweat", "sweep",
    "sweet", "swept", "swerve","swill", "swine", "swipe", "swirl", "swoop", "tabby", "taboo",
    "taffy", "tangy", "taunt", "tawny", "tepid", "terse", "thane", "thatch","thyme", "tiara",
    "tidbit","timid", "tipsy", "titan", "tizzy", "toast", "tonal", "topaz", "topsy", "torso",
    "totem", "touchy","tramp", "trash", "triad", "tripe", "tromp", "trope", "troth", "trout",
    "trove", "truly", "truss", "tuber", "tulip", "tulle", "turbo", "tusks", "twang", "tweek",
    "twill", "twine", "twirl", "udder", "ulcer", "umbra", "unfit", "ungly", "updraft","usurp",
    "vague", "vaunt", "venal", "viand", "vigil", "villa", "viper", "virgo", "vogue", "voila",
    "vouch", "vulva", "wacky", "warty", "waver", "weedy", "whelp", "whiff", "whimsy","whirl",
    "whoop", "wimpy", "windy", "witty", "woken", "wordy", "wormy", "wring", "wrong", "yucky",
    "yummy", "zappy", "zesty", "zingy", "zippy", "abate", "abbot", "abhor", "abide", "abode",
    "acing", "acmes", "acned", "acnes", "acred", "acres", "acrid", "acted", "actin", "acton",
    "adage", "added", "adder", "addle", "addly", "adman", "adopt", "adore", "adorn", "adorn",
    "aeons", "agape", "agate", "agave", "agaze", "agene", "agent", "agger", "aggie", "agile",
    "aging", "agism", "agist", "aglow", "agone", "agony", "agree", "ailed", "aimed", "aimer",
    "aired", "airer", "airth", "aisle", "aitch", "alarm", "album", "alder", "allay", "aloft",
    "aloin", "aloof", "aloud", "along", "altar", "alter", "amaze", "amate", "amber", "amble",
    "ament", "amide", "amiss", "amity", "amuse", "anger", "anise", "annoy", "antsy", "aphid",
    "apian", "apnea", "apron", "aptly", "argot", "argil", "argon", "arson", "artsy", "ashen",
    "aspen", "atoll", "atone", "atilt", "avast", "avow",  "awash", "awing", "bairn", "baize",
    "balmy", "bandy", "baron", "basil", "baste", "batty", "bogus", "bolar", "botch", "brash",
    "brawl", "bream", "breve", "broil", "buxom", "byway", "cadet", "cameo", "canny", "cargo",
    "caste", "caulk", "cavil", "cinch", "cleft", "cloak", "clown", "cluck", "codon", "coils",
    "cramp", "crank", "crass", "crook", "crown", "crypt", "cubic", "curly", "cushy", "daffy",
    "dandy", "decal", "decry", "delve", "depot", "deter", "diode", "dirge", "ditty", "divot",
    "dizzy", "dogma", "dowel", "downy", "drool", "droop", "duchy", "dusky", "dusty", "dwarf",
    "dwell", "easel", "eaves", "ebony", "edict", "edify", "eerie", "egret", "elder", "elect",
    "elegy", "elfin", "elide", "elope", "emote", "enact", "envoy", "epoch", "ergot", "evade",
    "evoke", "exile", "exude", "exult", "faint", "fatty", "favor", "feign", "felon", "femur",
    "ferny", "ferry", "fetch", "fetid", "ficus", "fiery", "finch", "fishy", "fixer", "fizzy",
    "flail", "flank", "flick", "flung", "flute", "foamy", "foggy", "folio", "folly", "foray",
    "forte", "forty", "foyer", "frail", "franc", "friar", "frond", "fugue", "furor", "fuzzy",
    "gaily", "gaudy", "gauze", "gavel", "gawky", "geeky", "giddy", "girth", "gloat", "gloom",
    "glory", "glyph", "gnash", "gnome", "goofy", "goose", "gouge", "gourd", "graft", "grail",
    "grant", "gravy", "grimy", "gripe", "gruff", "grump", "guava", "gummy", "haiku", "handy",
    "hazel", "heist", "helix", "hippy", "hitch", "hoard", "hoary", "hobby", "homer", "horde",
    "hound", "hulky", "husky", "hyena", "hyper", "idiom", "igloo", "inane", "inept", "ingot",
    "ionic", "irked", "itchy", "jiffy", "jokey", "jumpy", "kaput", "kebab", "kinky", "kitty",
    "kneel", "knelt", "knobs", "knots", "kudos", "lance", "lanky", "lapel", "lapse", "larva",
    "latch", "lathe", "leafy", "leaky", "leapt", "ledge", "leech", "lefty", "lemma", "lemon",
    "lemur", "libel", "liner", "lingo", "lipid", "lithe", "livid", "llama", "lodge", "lofty",
    "loner", "lorry", "lousy", "lusty", "mange", "mania", "manly", "mauve", "maxim", "melee",
    "melon", "messy", "mimic", "minty", "mirth", "miser", "mocha", "mogul", "moldy", "moody",
    "moose", "moped", "moron", "mossy", "motif", "muddy", "muggy", "mulch", "mummy", "murky",
    "musty", "myrrh", "nadir", "naive", "nanny", "natty", "naval", "needy", "ninja", "nippy",
    "nitro", "nonce", "nosey", "notch", "nudge", "nutty", "offal", "optic", "orate", "orbit",
    "otter", "outdo", "ovoid", "paddy", "pagan", "patio", "patsy", "patty", "payee", "peach",
    "peaky", "peeve", "petal", "petty", "picky", "piggy", "plait", "pluck", "plunk", "plush",
    "poach", "poker", "polka", "polyp", "porky", "posit", "potty", "pouch", "prank", "prawn",
    "privy", "prude", "prune", "psalm", "pubis", "pudgy", "puffy", "pulpy", "putty", "pygmy",
    "quirk", "rabid", "raspy", "ratty", "raven", "rayon", "rebus", "reedy", "refit", "regal",
    "relic", "renal", "repay", "repel", "rerun", "reuse", "revel", "ripen", "rivet", "robin",
    "roomy", "roost", "rowdy", "ruddy", "rusty", "saggy", "sandy", "savvy", "scald", "scalp",
    "scant", "scare", "scorn", "scout", "scowl", "scram", "scrap", "scrub", "seedy", "seize",
    "serum", "shack", "shady", "shale", "shawl", "sheen", "shoal", "shrub", "shuck", "shunt",
    "silky", "sissy", "sixty", "skimp", "skirt", "sleet", "slick", "slimy", "slosh", "sloth",
    "slunk", "slurp", "slyly", "smear", "smite", "smock", "snare", "sneak", "sneer", "snide",
    "snore", "snort", "snowy", "soggy", "solar", "sooty", "sorry", "spasm", "speck", "spied",
    "spill", "spiny", "spook", "spoon", "spout", "spunk", "spurn", "spurt", "squat", "squid",
    "stark", "stash", "stead", "steed", "stoic", "stomp", "stoop", "strut", "stubs", "stump",
    "stunk", "stunt", "suave", "sulky", "sumac", "surly", "swamp", "swath", "swear", "sweat",
    "sweep", "sweet", "swept", "swill", "swine", "swipe", "swirl", "swoop", "tabby", "taboo",
    "taffy", "tangy", "taunt", "tawny", "tepid", "terse", "thyme", "tiara", "timid", "tipsy",
    "titan", "tizzy", "toast", "tonal", "topaz", "torso", "totem", "tramp", "triad", "tripe",
    "tromp", "trope", "troth", "trout", "trove", "truss", "tuber", "tulip", "tulle", "turbo",
    "twang", "twill", "twine", "twirl", "ulcer", "umbra", "unfit", "usurp", "vague", "vaunt",
    "venal", "viand", "vigil", "villa", "viper", "vogue", "vouch", "wacky", "warty", "waver",
    "weedy", "whelp", "whiff", "whirl", "whoop", "wimpy", "windy", "witty", "wordy", "wormy",
    "wring", "wrong", "yucky", "yummy", "zappy", "zesty", "zingy", "zippy", "mafia", "natal",
    "oaken", "psalm", "quaff", "quash", "quell", "quill", "radon", "rajah", "ramen", "recap",
    "recon", "rector","redux", "reedy", "reeve", "refer", "repro", "rerun", "retro", "rhino",
    "rowel", "rowdy", "ruche", "rumen", "runic", "rupee", "sagas", "salve", "salvo", "sanky",
    "saute", "scree", "sedan", "senna", "siren", "skein", "skimp", "sloop", "slosh", "slump",
    "smelt", "smite", "snaky", "solde","sigma", "sinew", "siren", "skiff", "skimp", "slate",
    "smoky", "snaky", "spade", "spasm", "spate", "spawn", "specs", "speed", "spire", "spite",
    "splay", "sprig", "sprue", "squab", "staid", "stamp", "stark", "swath", "sweat", "tabor",
    "taper", "tapir", "tardy", "terse", "tilde", "timid", "tinge", "tonal", "tongs", "tonic",
    "topaz", "traps", "trays", "trice", "trims", "troth", "trout", "trove", "truss", "tuber",
    "tummy", "tuner", "turbo", "tweed", "umbra", "unfed", "valor", "varve", "venal", "verse",
    "vicar", "vison", "vogue", "voila", "vying", "waltz", "wizen", "wonky", "wormy", "wrung",
    "yakut", "yearn", "yodel", "yokel", "zippy", "zloty", "algae", "alpha", "amend", "amino",
    "angst", "annex", "aphid", "arbor", "ardor", "argon", "arose", "artsy", "ascot", "ashen",
    "atone", "balmy", "basal", "basil", "bayou", "beech", "belle", "berry", "bevel", "bigot",
    "bilge", "bland", "blend", "bliss", "bloke", "brash", "bravo", "brawl", "breve", "broil",
    "brood", "broom", "byway", "cache", "cameo", "canny", "carom", "caste", "cavil", "cedar",
    "chasm", "choir", "chore", "cinch", "cleft", "cloak", "cobalt","comet", "coupe", "cramp",
    "crimp", "crook", "crypt", "cubic", "curly", "cushy", "daffy", "dandy", "decry", "delve",
    "deter", "ditty", "divot", "dizzy", "dolce", "dowel", "duchy", "eagle", "eaves", "ebony",
    "eerie", "egret", "elfin", "elide", "elope", "emote", "enact", "envoy", "epoch", "evade",
    "evoke", "exude", "exult", "faint", "fauve", "felon", "femur", "ferny", "fetid", "ficus",
    "fiery", "finch", "fizzy", "fjord", "flail", "flute", "folio", "folly", "forte", "foyer",
    "frail", "franc", "friar", "frond", "fugue", "furor", "fuzzy", "gaudy", "gauze", "gavel",
    "gawky", "giddy", "girth", "glyph", "gnash", "gnome", "gouge", "gourd", "grail", "grimy",
    "gripe", "gruff", "grump", "guava", "gummy", "haiku", "hazel", "heist", "helix", "hippy",
    "hitch", "hoard", "hoary", "horde", "hulky", "idiom", "igloo", "inane", "inept", "ingot",
    "ionic", "irked", "itchy", "jiffy", "jokey", "jumpy", "kaput", "kebab", "kinky", "kitty",
    "lance", "lanky", "lapel", "lapse", "larva", "latch", "lathe", "leafy", "leaky", "leapt",
    "ledge", "leech", "lemma", "lemur", "libel", "lingo", "lipid", "lithe", "livid", "llama",
    "lodge", "loner", "lorry", "lousy", "mange", "mania", "mauve", "maxim", "melee", "messy",
    "mimic", "minty", "mirth", "miser", "mocha", "mogul", "moldy", "moody", "moped", "moron",
    "mossy", "motif", "muddy", "muggy", "mulch", "mummy", "murky", "musty", "nadir", "naive",
    "nanny", "natty", "naval", "needy", "ninja", "nippy", "nitro", "nonce", "nosey", "notch",
    "nudge", "nutty", "offal", "optic", "orate", "orbit", "otter", "ovoid", "paddy", "pagan",
    "patsy", "patty", "payee", "peaky", "peeve", "petal", "petty", "picky", "piggy", "plait",
    "pluck", "plush", "poker", "polka", "polyp", "posit", "potty", "prank", "privy", "prude",
    "prune", "pudgy", "puffy", "pulpy", "putty", "pygmy", "quirk", "rabid", "raspy", "ratty",
    "raven", "rayon", "rebus", "reedy", "refit", "regal", "relic", "renal", "repay", "repel",
    "revel", "ripen", "rivet", "roomy", "roost", "rowdy", "ruddy", "rusty", "saggy", "savvy",
    "scald", "scalp", "scant", "scare", "scorn", "scout", "scowl", "scram", "scrub", "seize",
    "serum", "shack", "shady", "shale", "shawl", "shoal", "shrub", "shuck", "shunt", "silky",
    "sissy", "skimp", "sleet", "slick", "slimy", "slosh", "sloth", "slunk", "slurp", "smear",
    "snare", "sneer", "snide", "snore", "snort", "soggy", "solar", "sooty", "spasm", "spiny",
    "spook", "squat", "squid", "stark", "stash", "stead", "steed", "stoic", "stomp", "stump",
    "stunk", "stunt", "suave", "sulky", "sumac", "surly", "swamp", "swath", "swear", "swill",
    "swine", "swipe", "swirl", "swoop", "tabby", "taffy", "tangy", "taunt", "tawny", "tepid",
    "thyme", "tiara", "timid", "tipsy", "tizzy", "tonal", "tramp", "tripe", "tromp", "troth",
    "truss", "tuber", "tulip", "turbo", "twang", "twill", "twirl", "ulcer", "umbra", "usurp",
    "vague", "vaunt", "viand", "vigil", "villa", "viper", "vouch", "wacky", "warty", "waver",
    "weedy", "whelp", "whoop", "wimpy", "windy", "wormy", "wring", "wrong", "yucky", "yummy",
]

# ==============================
# GENERATE DOMAINS
# ==============================
def generate_domains():
    for w1 in WORDS:
            yield f"{w1}{TLD}"


# ==============================
# CHECK BATCH
# ==============================
def check_batch(domains_batch):
    domains_param = ",".join(domains_batch)
    url = f"{BASE_URL}?domains={domains_param}&rcs={RCS_PARAM}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        data = resp.json()
        results = []

        for entry in data.get("status", []):
            name = entry.get("name")
            available = entry.get("available")
            premium = entry.get("premium")
            fee = entry.get("fee", {})

            price = fee.get("retailAmount")

            results.append((name, available, premium, price))

        return results

    except Exception:
        return [(d, "error", None, None) for d in domains_batch]


# ==============================
# MAIN EXECUTION
# ==============================
def run_check():
    all_domains = list(generate_domains())
    print(f"Total domains to check: {len(all_domains)}")

    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["domain", "status", "premium", "price"])

        for i in range(0, len(all_domains), BATCH_SIZE):
            batch = all_domains[i:i+BATCH_SIZE]
            results = check_batch(batch)

            for domain, status, premium, price in results:
                status_str = "Available" if status is True else "Taken" if status is False else status
                writer.writerow([domain, status_str, premium, price])

                if status_str == "Available":
                    print(f"Available: {domain} | Premium: {premium} | Price: {price}")

            time.sleep(SLEEP_BETWEEN_BATCHES)

    print(f"Finished. Results saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    run_check()
