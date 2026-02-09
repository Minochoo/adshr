import requests
import csv
import time
import random

# ==============================
# CONFIG
# ==============================
TLD = ".com"
BATCH_SIZE = 40
SLEEP_BETWEEN_BATCHES = 0.5
OUTPUT_CSV = "available_brandable_domains.csv"
TOTAL_DOMAINS = 3000

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Accept": "application/json"
}

BASE_URL = "https://domains.revved.com/v1/domainStatus"
RCS_PARAM = "Mms%2FKCVrc3hxcHl5ent%2FcH5laydrc2t%2BeSx7LS9%2BcXF%2BfXhxfHt4LX8qLS15f3BxenlxKn1%2Ff2s0"

# ==============================
# PHONETIC LETTER SETS (CLEAN)
# ==============================
VOWELS = "aeio"
CONSONANTS = "blmnrsdtvpf"  # ناعمة فقط – تشبه أسماء شركات

# ==============================
# BRANDABLE PATTERNS
# ==============================
PATTERNS = [
    "CVCVC",
    "CVCCV"
]

# ==============================
# PHONETIC RULES
# ==============================
def is_pronounceable(name: str) -> bool:
    bad_pairs = ["aa", "ee", "ii", "oo", "rr", "ll"]
    bad_clusters = ["dt", "pf", "sr"]

    for bp in bad_pairs:
        if bp in name:
            return False

    for bc in bad_clusters:
        if bc in name:
            return False

    return True

# ==============================
# DOMAIN GENERATOR (BRANDABLE)
# ==============================
def generate_domains():
    generated = set()

    while len(generated) < TOTAL_DOMAINS:
        pattern = random.choice(PATTERNS)
        name = ""

        for ch in pattern:
            if ch == "C":
                name += random.choice(CONSONANTS)
            else:
                name += random.choice(VOWELS)

        if not is_pronounceable(name):
            continue

        domain = name + TLD

        if domain not in generated:
            generated.add(domain)
            yield domain

# ==============================
# CHECK BATCH
# ==============================
def check_batch(domains):
    url = f"{BASE_URL}?domains={','.join(domains)}&rcs={RCS_PARAM}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        return r.json().get("status", [])
    except:
        return []

# ==============================
# MAIN
# ==============================
def run():
    domains = list(generate_domains())
    print(f"[+] Generated {len(domains)} brandable domains")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "premium", "price"])

        for i in range(0, len(domains), BATCH_SIZE):
            batch = domains[i:i+BATCH_SIZE]
            results = check_batch(batch)

            for entry in results:
                if entry.get("available") is True:
                    domain = entry.get("name")
                    premium = entry.get("premium")
                    price = entry.get("fee", {}).get("retailAmount")

                    writer.writerow([domain, premium, price])
                    print(f"[AVAILABLE] {domain}")

            time.sleep(SLEEP_BETWEEN_BATCHES)

    print(f"\n✅ Finished. Only BRANDABLE available domains saved.")

if __name__ == "__main__":
    run()
