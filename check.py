import requests
import itertools
import csv
import time
import random

# ==============================
# CONFIG
# ==============================
TLD = ".com"
BATCH_SIZE = 40
SLEEP_BETWEEN_BATCHES = 0.50
OUTPUT_CSV = "generated_domains_results.csv"

HEADERS = { 
    'User-Agent': "Mozilla/5.0 (Linux; Android 10)",
    'Accept': "application/json"
}

BASE_URL = "https://domains.revved.com/v1/domainStatus"
RCS_PARAM = "Mms%2FKCVrc3hxcHl5ent%2FcH5laydrc2t%2BeSx7LS9%2BcXF%2BfXhxfHt4LX8qLS15f3BxenlxKn1%2Ff2s0"

# ==============================
# LETTER POOLS FOR 5-CHAR BRANDABLE DOMAINS
# ==============================
CONSONANTS = "bcdfglmnprstv"
VOWELS = "aeio"

# ==============================
# GENERATE DOMAINS AUTOMATICALLY
# ==============================
def generate_domains(n_domains=1000):
    generated = set()
    while len(generated) < n_domains:
        # اختيار نمط CVCVC
        c1 = random.choice(CONSONANTS)
        v1 = random.choice(VOWELS)
        c2 = random.choice(CONSONANTS)
        v2 = random.choice(VOWELS)
        c3 = random.choice(CONSONANTS)

        domain = f"{c1}{v1}{c2}{v2}{c3}{TLD}"

        # التأكد من عدم التكرار
        if domain not in generated:
            generated.add(domain)
            yield domain

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
    all_domains = list(generate_domains(n_domains=1000))
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
