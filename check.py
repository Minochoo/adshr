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
OUTPUT_CSV = "available_only_unique_domains.csv"
TOTAL_DOMAINS_TO_GENERATE = 3000

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Accept": "application/json"
}

BASE_URL = "https://domains.revved.com/v1/domainStatus"
RCS_PARAM = "Mms%2FKCVrc3hxcHl5ent%2FcH5laydrc2t%2BeSx7LS9%2BcXF%2BfXhxfHt4LX8qLS15f3BxenlxKn1%2Ff2s0"

# ==============================
# SMART LETTER POOLS
# ==============================
VOWELS = "aeio"
SOFT_CONSONANTS = "blmnrsdtv"
TECH_CONSONANTS = "xzk"
ALL_CONSONANTS = SOFT_CONSONANTS + TECH_CONSONANTS

# ==============================
# BRANDABLE PATTERNS
# ==============================
PATTERNS = [
    "CVCVC",
    "CVCCV",
    "CVCVX",
    "CVVCV"
]

# ==============================
# DOMAIN GENERATOR (UNIQUE)
# ==============================
def generate_domains():
    generated = set()

    while len(generated) < TOTAL_DOMAINS_TO_GENERATE:
        pattern = random.choice(PATTERNS)
        name = ""

        for char in pattern:
            if char == "C":
                name += random.choice(ALL_CONSONANTS)
            elif char == "V":
                name += random.choice(VOWELS)
            elif char == "X":
                name += random.choice("xz")

        # فلترة إضافية (جمالية)
        if any(bad in name for bad in ["zx", "q", "aa", "ii"]):
            continue

        full_domain = name + TLD

        if full_domain not in generated:
            generated.add(full_domain)
            yield full_domain

# ==============================
# CHECK BATCH
# ==============================
def check_batch(domains):
    domains_param = ",".join(domains)
    url = f"{BASE_URL}?domains={domains_param}&rcs={RCS_PARAM}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        return data.get("status", [])
    except:
        return []

# ==============================
# MAIN
# ==============================
def run():
    domains = list(generate_domains())
    print(f"[+] Generated {len(domains)} unique domains")

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
                    print(f"[AVAILABLE] {domain} | Premium={premium} | Price={price}")

            time.sleep(SLEEP_BETWEEN_BATCHES)

    print(f"\n✅ Done. Saved only AVAILABLE domains to {OUTPUT_CSV}")

if __name__ == "__main__":
    run()
