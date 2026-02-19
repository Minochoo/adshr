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
WORDS =
    # جذر الفهم والعلم
    "fahim",
    "aleem",
    "arift",
    "ilmak",
    "ilmai",
    "fikra",
    "fahma",
    "zakat",
    "zakii",
    "aqlai",
    "aqlan",
    "aqlly",
    "fahmy",
    "ulmak",
    "elmak",

    # جذر النور والإضاءة
    "siraj",
    "noura",
    "nouri",
    "nawir",
    "diyaa",
    "diyal",
    "nurly",
    "anwar",
    "fajri",
    "fajra",
    "ishrq",
    "ishri",
    "basar",
    "basra",
    "dayai",

    # جذر الإجابة والتوضيح
    "moujb",
    "mujib",
    "mubyn",
    "mubin",
    "bayni",
    "wuduh",
    "jalaa",
    "tabyn",
    "tabin",
    "bayan",
    "wakif",
    "waqif",
    "sarih",
    "fasih",
    "wasih",

    # جذر الكشف والاستيعاب
    "kashf",
    "kasif",
    "jaliy",
    "jalia",
    "hatif",
    "rawad",
    "kashy",
    "faraj",
    "farij",
    "munir",
    "munaj",
    "tabsr",
    "tabir",
    "wajid",
    "wajad",

    # جذر الهداية والتوجيه
    "hadii",
    "hadia",
    "rushd",
    "mursd",
    "dalil",
    "dalal",
    "minhj",
    "minha",
    "qayym",
    "sirty",
    "sirat",
    "hudaa",
    "hudan",
    "irsad",
    "irshd",

    # جذر النجاح والتفوق
    "najib",
    "nujba",
    "rafii",
    "rafea",
    "faaiq",
    "fayek",
    "mumtz",
    "tamyz",
    "tamiz",
    "muwfq",
    "tofiq",
    "tawfq",
    "nabil",
    "nabih",
    "zafir",

    # جذر المساعدة والمرافقة
    "muawn",
    "muayn",
    "rafiq",
    "saand",
    "nafia",
    "naafi",
    "wakyl",
    "wakil",
    "sadiq",
    "ameen",
    "amina",
    "waafi",
    "wafai",
    "mueen",
    "muyin",

    # جذر التعليم والتدريس
    "talim",
    "talem",
    "tadrs",
    "tadry",
    "tarby",
    "talqn",
    "tabid",
    "tadib",
    "daris",
    "darsa",
    "sabak",
    "sabqa",
    "durus",
    "sabaq",
    "darss",

    # جذر الحكمة والتفكير
    "hakym",
    "hakim",
    "hikma",
    "fikri",
    "raaid",
    "raady",
    "tafkr",
    "mantq",
    "maniq",
    "dhaka",
    "dhaky",
    "rawiy",
    "rawia",
    "lubbk",
    "lubab",

    # جذر القلم والكتابة والمعرفة
    "qalam",
    "qalem",
    "kitab",
    "kutub",
    "warqa",
    "lawha",
    "rakam",
    "naqsh",
    "kalam",
    "balag",
    "khatt",
    "raqam",
    "satar",
    "lawha",
    "safha",

    # أسماء قصيرة وعصرية بإيقاع جيد
    "zekra",
    "zikra",
    "nafis",
    "wajiz",
    "laziz",
    "latif",
    "wasim",
    "nazif",
    "basit",
    "fasil",
    "naqiy",
    "rakiz",
    "razin",
    "rasim",
    "shaff",

    # مزيج إبداعي
    "taalm",
    "taaly",
    "nurly",
    "fahml",
    "ilmly",
    "zekly",
    "nurif",
    "guidl",
    "tutor",
    "mentr",
    "brainy",
    "solvr",
    "learnr",
    "studai",
    "aqlai",

    # إضافات بجذور أصيلة
    "wadih",
    "sabyl",
    "tariq",
    "masra",
    "nafiz",
    "bashir",
    "bishry",
    "amali",
    "hayya",
    "nahjy",
    "nahja",
    "tajly",
    "wafid",
    "mazid",
    "taqwa",
    "wafed",
    "tajal",
    "nafidh",
    "maseer",
    "sabeel",
    "wadhih",
    "amalak",
    "mazyd",
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
