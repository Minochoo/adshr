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
    "apple", "table", "chair", "house", "water", "light", "night", "black", "white", "green",
    "blue", "heart", "world", "earth", "peace", "grace", "place", "space", "trace", "brave",
    "flame", "frame", "shame", "blame", "claim", "train", "brain", "chain", "plain", "grain",
    "paint", "saint", "faint", "giant", "plant", "grant", "slant", "chant", "front", "blunt",
    "stunt", "grunt", "count", "mount", "shout", "scout", "trout", "snout", "cloud", "proud",
    "crowd", "blood", "flood", "floor", "store", "score", "shore", "swore", "spoke", "smoke",
    "broke", "choke", "cloak", "croak", "steak", "speak", "freak", "sneak", "creek", "cheek",
    "sleek", "steel", "wheel", "kneel", "feels", "heels", "peels", "deals", "seals", "meals",
    "reals", "zeal", "realm", "dream", "cream", "steam", "gleam", "seam", "beam", "team",
    "clean", "ocean", "queen", "scene", "green", "preen", "sheen", "teens", "jeans", "beans",
    "means", "leans", "glean", "fiend", "blend", "spend", "trend", "blend", "mend", "fend",
    "lend", "rend", "wend", "bend", "sends", "tends", "fends", "lends", "bonds", "ponds",
    "wands", "hands", "bands", "lands", "sands", "grand", "brand", "bland", "stand", "gland",
    "clamp", "cramp", "stamp", "champ", "tramp", "swamp", "claps", "snaps", "traps", "wraps",
    "grabs", "crabs", "slabs", "stabs", "scabs", "jabs", "tabs", "cabs", "dabs", "labs",
    "fabs", "nabs", "blabs", "drabs", "shaft", "draft", "craft", "graft", "waft", "daft",
    "after", "asked", "awful", "basic", "basis", "beach", "begin", "being", "below", "birth",
    "board", "bonus", "boost", "booth", "bound", "boxer", "break", "breed", "brick", "bride",
    "brief", "bring", "brisk", "broad", "broke", "brook", "broom", "broth", "brown", "brush",
    "build", "built", "bunch", "burst", "buyer", "cabin", "cable", "candy", "carry", "catch",
    "cause", "cease", "cells", "cents", "chaos", "charm", "chase", "cheap", "check", "chest",
    "chief", "child", "chips", "civic", "civil", "class", "clean", "clear", "clerk", "click",
    "cliff", "climb", "clock", "clone", "close", "cloth", "coach", "coast", "color", "comes",
    "coral", "cover", "craft", "crash", "crazy", "cream", "crime", "crisp", "cross", "cruel",
    "crush", "curve", "cycle", "daily", "dance", "death", "debut", "delay", "dense", "depot",
    "depth", "derby", "devil", "digit", "dirty", "disco", "dodge", "doors", "doubt", "dough",
    "draft", "drain", "drama", "drank", "drawn", "dress", "dried", "drift", "drink", "drive",
    "drone", "drove", "dryer", "dunes", "dying", "eager", "early", "eight", "elite", "empty",
    "enemy", "enjoy", "enter", "entry", "equal", "error", "essay", "event", "every", "exact",
    "exist", "extra", "fable", "faced", "faith", "falls", "false", "fancy", "fatal", "fault",
    "feast", "fence", "fever", "fewer", "fiber", "field", "fifth", "fifty", "fight", "final",
    "first", "fixed", "flare", "flash", "fleet", "flesh", "flies", "float", "flock", "flood",
    "flora", "floss", "flour", "fluid", "flush", "focus", "force", "forge", "forth", "forum",
    "found", "frank", "fraud", "fresh", "frost", "froze", "fully", "funds", "fungi", "funny",
    "gauge", "ghost", "given", "gland", "glare", "glass", "glide", "gloss", "glove", "going",
    "grace", "grade", "graph", "grasp", "grass", "grave", "graze", "greet", "grief", "grind",
    "groan", "gross", "group", "grove", "growl", "grown", "guard", "guide", "guile", "guise",
    "gusto", "habit", "happy", "harsh", "haven", "hawks", "heads", "heard", "heavy", "hence",
    "herbs", "hinge", "hippo", "holds", "holly", "homer", "honey", "honor", "hooks", "horse",
    "hotel", "hours", "human", "humor", "hurry", "hyena", "ideal", "image", "imply", "index",
    "indie", "infer", "inner", "input", "inter", "intro", "irony", "issue", "ivory", "jazzy",
    "jewel", "joint", "joker", "joust", "judge", "juice", "juicy", "jumbo", "karma", "kayak",
    "keeps", "knack", "knife", "knock", "known", "label", "large", "laser", "later", "laugh",
    "layer", "leads", "learn", "lease", "least", "leave", "legal", "level", "limit", "lined",
    "links", "liver", "logic", "loose", "lover", "lower", "lucky", "lunar", "lunch", "lyric",
    "magic", "major", "maker", "manor", "maple", "march", "match", "mayor", "media", "mercy",
    "merit", "metal", "micro", "might", "minor", "minus", "mixed", "model", "money", "monks",
    "month", "moral", "motor", "mouse", "mouth", "moved", "movie", "multi", "music", "nasal",
    "nerve", "never", "noble", "noise", "north", "noted", "novel", "nurse", "nymph", "occur",
    "offer", "often", "olive", "onset", "opera", "order", "other", "outer", "oxide", "ozone",
    "paced", "panel", "panic", "paper", "party", "pasta", "patch", "pause", "pearl", "penny",
    "phase", "phone", "photo", "piano", "pilot", "pitch", "pixel", "pizza", "plain", "plane",
    "plate", "plaza", "plumb", "plume", "plunge","poetic","point", "polar", "polis", "poppy",
    "porch", "posed", "power", "press", "price", "pride", "prime", "print", "prior", "prize",
    "probe", "prone", "proof", "prose", "proud", "prove", "proxy", "pulse", "pupil", "purse",
    "queen", "quest", "queue", "quick", "quiet", "quota", "quote", "rabbi", "radar", "radio",
    "rainy", "rally", "ranch", "range", "rapid", "ratio", "reach", "react", "ready", "refer",
    "reign", "relax", "reply", "rider", "ridge", "right", "rigid", "risky", "rival", "river",
    "robot", "rocky", "rodeo", "roman", "rouge", "rough", "round", "route", "royal", "rugby",
    "ruler", "rural", "sadly", "saint", "salad", "sauce", "scale", "scary", "sedan", "sense",
    "serve", "setup", "seven", "shade", "shake", "shall", "share", "shark", "sharp", "sheep",
    "shelf", "shell", "shift", "shine", "shirt", "shoes", "shoot", "short", "shrug", "siege",
    "sight", "sigma", "silly", "since", "sixth", "skill", "skull", "slang", "slash", "slate",
    "slave", "sleep", "slice", "slide", "slime", "slope", "smart", "smell", "smile", "smith",
    "solid", "solve", "sound", "south", "spark", "spawn", "speak", "spear", "speed", "spell",
    "spend", "spine", "spite", "split", "spoke", "spore", "sport", "spray", "squad", "stack",
    "staff", "stage", "stain", "stair", "stale", "stall", "start", "state", "stays", "steam",
    "steep", "steer", "stern", "stick", "stiff", "still", "stock", "stone", "stood", "storm",
    "story", "stove", "strap", "straw", "stray", "strip", "stuck", "study", "stuff", "style",
    "sugar", "suite", "sunny", "super", "surge", "swift", "sword", "swore", "swung", "taxes",
    "tense", "tenth", "terms", "theft", "theme", "there", "thick", "thing", "think", "third",
    "thorn", "those", "three", "threw", "throw", "tiger", "tight", "timer", "tired", "title",
    "today", "token", "tombs", "tools", "topic", "total", "touch", "tough", "towel", "tower",
    "toxic", "track", "trade", "trail", "trait", "trans", "trash", "treat", "trial", "tribe",
    "trick", "tried", "troop", "truck", "truly", "trust", "truth", "tumor", "tuner", "tunes",
    "tutor", "twice", "twist", "typed", "ultra", "under", "unify", "union", "unity", "until",
    "upper", "urban", "usage", "usual", "utter", "valid", "value", "valve", "vapor", "vault",
    "video", "vigor", "viral", "virus", "visit", "visor", "vital", "vivid", "vocal", "voice",
    "voter", "vowed", "wager", "waste", "watch", "weary", "wedge", "weird", "whale", "wheat",
    "where", "which", "while", "whole", "whose", "wider", "witch", "woman", "women", "worry",
    "worse", "worst", "worth", "would", "wound", "wrath", "wrist", "yacht", "yield", "young",
    "youth", "zebra", "zones", "zooms", "abbey", "acorn", "adorn", "agile", "aisle", "algae",
    "alien", "align", "alley", "allot", "altar", "amber", "amend", "amiss", "angel", "anger",
    "angle", "annex", "antic", "anvil", "apart", "apron", "aptly", "arbor", "arena", "argon",
    "armed", "aroma", "arose", "array", "arson", "aside", "atlas", "attic", "audit", "avail",
    "avant", "avian", "oasis", "blend", "bliss", "bloke", "bloat", "bleat", "bless", "blown",
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
