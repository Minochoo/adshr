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
    # النور والإضاءة
    "Siraj",   # السراج - المصباح المنير
    "Anwar",   # أنور - أشد نوراً
    "Nawir",   # نوّر - منير ومضيء
    "Diyaa",   # ضياء - النور والإشراق
    "Zahir",   # زاهر - المتألق والمشرق
    "Lamih",   # لامح - اللمعة والبريق
    "Munir",   # منير - المنير والمضيء
    "Nurus",   # نور - النور الخالص
    "Zuhur",   # ظهور - الظهور والتجلي
    "Raaiq",   # رائق - الصافي النقي

    # الهداية والتوجيه
    "Rushd",   # رشد - النضج والهداية
    "Hadii",   # هادي - الموجه والمرشد
    "Dalil",   # دليل - يدلك على الطريق
    "Irsad",   # إرشاد - التوجيه السليم
    "Tariq",   # طارق - الطريق
    "Sabyl",   # سبيل - الطريق الواضح
    "Minhj",   # منهج - طريق التعلم
    "Nujum",   # نجوم - النجوم التي تهدي
    "Qiyas",   # قياس - المعيار والميزان
    "Raaed",   # رائد - الرائد والمكتشف

    # الفهم والعلم
    "Fahim",   # فاهم - المدرك والمتعلم
    "Aleem",   # عليم - صاحب العلم
    "Fikra",   # فكرة - الفكر والإبداع
    "Ilham",   # إلهام - وحي الأفكار
    "Idrak",   # إدراك - الفهم العميق
    "Zikra",   # ذكرى - الحفظ والتذكر
    "Rasid",   # راصد - المراقب الفاهم
    "Nafis",   # نفيس - الثمين والقيّم
    "Dhihn",   # ذهن - الذهن والعقل
    "Yaqin",   # يقين - اليقين والثقة

    # الحكمة والتفكير
    "Hakim",   # حكيم - صاحب الحكمة
    "Hikma",   # حكمة - الحكمة والفطنة
    "Lubab",   # لباب - خلاصة الحكمة
    "Rawiy",   # راوي - الحافظ والناقل
    "Dhaka",   # ذكاء - الذكاء والفطنة
    "Latif",   # لطيف - الدقيق اللطيف
    "Basir",   # بصير - صاحب البصيرة
    "Razin",   # رزين - الرزين والحكيم
    "Matin",   # متين - القوي الراسخ
    "Wazin",   # وازن - المتوازن والمعتدل

    # الإجابة والتوضيح
    "Mujib",   # مجيب - من يجيب ويرد
    "Mubin",   # مبين - الواضح والصريح
    "Bayan",   # بيان - الوضوح والفصاحة
    "Fasih",   # فصيح - البليغ الواضح
    "Sarih",   # صريح - الصادق الواضح
    "Wuduh",   # وضوح - الوضوح التام
    "Jaliy",   # جلي - الظاهر الواضح
    "Nafid",   # نافذ - النافذ المؤثر
    "Balag",   # بلاغ - إيصال المعلومة
    "Wasit",   # وسيط - الجسر بين الغامض والواضح

    # النجاح والتفوق
    "Najib",   # نجيب - النجيب المتفوق
    "Nabil",   # نبيل - النبيل الكريم
    "Rafii",   # رفيع - رفيع المستوى
    "Faaiq",   # فائق - المتفوق والمتميز
    "Tamiz",   # تميز - التميز والتفرد
    "Zafir",   # ظافر - المنتصر الناجح
    "Sabiq",   # سابق - المتقدم والمتفوق
    "Tofiq",   # توفيق - التوفيق والنجاح
    "Nabih",   # نبيه - الذكي المنبّه
    "Akram",   # أكرم - الأكرم والأفضل

    # المساعدة والقرب
    "Rafiq",   # رفيق - الصديق والمساعد
    "Sadiq",   # صادق - الصادق الأمين
    "Naafi",   # نافع - المفيد للجميع
    "Wakil",   # وكيل - الممثل والمعتمد
    "Ameen",   # أمين - الأمين الموثوق
    "Mueen",   # معين - المساعد والناصر
    "Waafi",   # وافي - الوافي بالوعد
    "Karim",   # كريم - الكريم العطاء
    "Anees",   # أنيس - الأنيس المقرب
    "Mufid",   # مفيد - المفيد للجميع

    # التعليم والتدريس
    "Talim",   # تعليم - العلم والتعليم
    "Daris",   # دارس - طالب العلم
    "Sabaq",   # سبق - التقدم في التعلم
    "Durus",   # دروس - دروس العلم
    "Tadib",   # تأديب - التأديب والتهذيب
    "Sahwi",   # صحوة - اليقظة والانتباه
    "Talib",   # طالب - طالب العلم
    "Tarby",   # تربية - التربية والتنشئة
    "Marji",   # مرجع - المرجع الموثوق
    "Masdr",   # مصدر - مصدر المعرفة

    # القلم والكتابة
    "Qalam",   # قلم - رمز العلم والكتابة
    "Kitab",   # كتاب - وعاء المعرفة
    "Waraq",   # ورق - الصفحة البيضاء
    "Kalam",   # كلام - البيان والتعبير
    "Naqsh",   # نقش - الأثر الباقي
    "Khatt",   # خط - خط العلم والكتابة
    "Raqam",   # رقم - الرياضيات والحساب
    "Safha",   # صفحة - صفحة المعرفة
    "Satar",   # سطر - سطور العلم
    "Rasim",   # رسّام - الرسم والتصوير

    # الكشف والاستيعاب
    "Kashf",   # كشف - اكتشاف الحقيقة
    "Kasif",   # كاشف - من يكشف الغموض
    "Faraj",   # فرج - الفرج بعد الصعوبة
    "Wajid",   # واجد - من وجد الحل
    "Faris",   # فارس - الفارس في العلم
    "Mahir",   # ماهر - الكفء والمتقن
    "Hatif",   # هاتف - الصوت الموجّه
    "Rakiz",   # ركيز - الراسخ والثابت
    "Naqib",   # نقيب - الممثل والرئيس
    "Rabit",   # رابط - الرابط بين الأفكار

    # الإبداع والتميز
    "Badii",   # بديع - البديع والجميل
    "Ibdaa",   # إبداع - الإبداع والابتكار
    "Zahiy",   # زاهي - المتألق والمزدهر
    "Samiy",   # سامي - السامي الرفيع
    "Majid",   # ماجد - الماجد الكريم
    "Nadir",   # نادر - النادر والمتميز
    "Nadiy",   # ندي - الندي الكريم
    "Wafir",   # وافر - الوافر الكثير
    "Shaml",   # شامل - الشامل والمتكامل
    "Aamil",   # عامل - العامل الفاعل

    # الصفات الإيجابية
    "Basit",   # بسيط - السهل الميسور
    "Nazif",   # نظيف - النقي الصافي
    "Wajiz",   # وجيز - الموجز والمختصر
    "Naqiy",   # نقي - النقي الصافي
    "Sadid",   # سديد - السديد والصحيح
    "Qawim",   # قويم - المستقيم والصحيح
    "Sahih",   # صحيح - الصحيح والسليم
    "Qadir",   # قادر - القادر والمتمكن
    "Salim",   # سليم - السليم والصحيح
    "Tayyb",   # طيب - الطيب النقي

    # إلهام من علماء العرب
    "Jabir",   # جابر - جابر بن حيان
    "Rusyd",   # رشد - فيلسوف الأندلس
    "Sinaa",   # سينا - الشيخ الرئيس
    "Hayth",   # هيثم - أبو البصريات
    "Farbi",   # فارابي - المعلم الثاني
    "Birni",   # بيروني - العالم الموسوعي

    # أسماء بطاقة إيجابية
    "Nasir",   # ناصر - الناصر والمساعد
    "Safir",   # سفير - سفير المعرفة
    "Raafd",   # رافد - الرافد والمُغذّي
    "Majdy",   # مجدي - المجدي والنافع
    "Nazim",   # ناظم - المنظّم والمرتّب
    "Hamid",   # حامد - الحامد الشاكر
    "Warid",   # وارد - الوارد والجديد
    "Zaaid",   # زائد - الزائد والمتقدم
    "Raqib",   # رقيب - المراقب والمتابع
    "Qaaim",   # قائم - القائم والمستمر

    # إضافات جميلة
    "Wabil",   # وابل - المطر الغزير كالعلم
    "Thaqb",   # ثاقب - الثاقب النافذ
    "Wasim",   # وسيم - الجميل الحسن
    "Yusur",   # يسر - السهولة والتيسير
    "Zamil",   # زميل - الزميل والرفيق
    "Ziyad",   # زياد - الزيادة والنمو
    "Basim",   # باسم - المبتسم المتفائل
    "Fatin",   # فاتن - الجذاب والمؤثر
    "Sahil",   # ساحل - المنطلق للآفاق
    "Shafi",   # شافي - الشافي للجهل

    # المزيد
    "Qudwa",   # قدوة - القدوة الحسنة
    "Murad",   # مراد - الهدف المنشود
    "Umran",   # عمران - العمارة والبناء
    "Hayba",   # هيبة - الوقار والاحترام
    "Ikhls",   # إخلاص - الإخلاص في التعلم
    "Iltqy",   # ملتقى - ملتقى المعرفة
    "Namus",   # ناموس - القانون والنظام
    "Zakat",   # زكاة - النقاء والطهارة
    "Zahwa",   # زهوة - الفخر والاعتزاز
    "Zuhar",   # زهر - الازدهار والتفتح

    # ختام
    "Wijdan",  # وجدان - الوجدان والضمير
    "Yaqaz",   # يقظة - اليقظة والانتباه
    "Taalq",   # تألق - التألق والنجاح
    "Sabur",   # صبور - الصبر على التعلم
    "Samah",   # سماح - التسامح والانفتاح
    "Dawiy",   # داوي - المعالج والمصلح
    "Ghawi",   # غاوي - المولع بالتعلم
    "Taqym",   # تقييم - التقييم والتصحيح
    "Tarqy",   # ترقي - الترقي والصعود
    "Wahid",   # واحد - المتفرد بالعلم

    # مزيد من الأسماء
    "Aflah",   # أفلح - الفائز والمفلح
    "Ajwad",   # أجود - الأجود والأكمل
    "Hafiz",   # حافظ - الحافظ للعلم
    "Kamil",   # كامل - الكامل المتكامل
    "Labib",   # لبيب - اللبيب العاقل
    "Nabig",   # نابغ - النابغة المتميز
    "Qabis",   # قابس - شعلة النور
    "Qaher",   # قاهر - المتغلب على الصعاب
    "Raghb",   # راغب - الراغب في التعلم
    "Sabih",   # صبيح - الجميل المشرق
    "Saigh",   # صائغ - صائغ الأفكار
    "Salik",   # سالك - سالك طريق العلم
    "Samin",   # ثمين - الثمين والقيّم
    "Kabir",   # كبير - الكبير في العلم
    "Hasib",   # حسيب - الحسيب المحاسب
    "Habir",   # حبير - الخبير العالم
    "Jawid",   # جويد - الجيد الرفيع
    "Farih",   # فارح - المبتهج بالتعلم
    "Rawin",   # راوٍ - الراوي للعلم
    "Manah",   # مناح - الهبة والعطاء
    "Namiq",   # نامق - الكاتب البارع
    "Nagem",   # ناجم - الناجم والبارز
    "Muzid",   # مزيد - المزيد من العلم
    "Nafiz",   # نافذ - النافذ المؤثر
    "Raziq",   # رازق - المُعطي والمُغني
    "Ramin",   # رامن - الهادئ المتأمل
    "Lamis",   # لامس - من يلمس الفهم
    "Qarib",   # قريب - القريب والميسور
    "Anzar",   # أنظر - الناظر المتأمل
    "Asdaq",   # أصدق - الأصدق والأمين
    "Arshd",   # أرشد - الأكثر رشداً
    "Awfaq",   # أوفق - الأكثر توفيقاً
    "Naabt",   # نابت - النابت والمتنامي
    "Qassm",   # قاسم - الموزع للعلم
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
