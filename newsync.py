import requests
from bs4 import BeautifulSoup
import json
import time

# =========================================================
# ⚙️ ตั้งค่าระบบ
# =========================================================
SETS = [f"op{str(i).zfill(2)}" for i in range(1, 16)]
RATE = 0.2011
OUTPUT_FILE = "prices_full.json"

# 🟢 แมปปิ้งรหัสกล่องจาก Yuyu-tei เข้ากับรหัส Series ของ Official เว็บ
OFFICIAL_URL_MAP = {
    "op15": "563115",
    "op14": "563114",
    "op13": "563113",
    "op12": "563112",
    "op11": "563111",
    "op10": "563110",
    "op09": "563109",
    "op08": "563108",
    "op07": "563107",
    "op06": "563106",
    "op05": "563105",
    "op04": "563104",
    "op03": "563103",
    "op02": "563102",
    "op01": "563101",
}

all_prices = {}
variant_counts = {}

# =========================================================
# 1. ฟังก์ชันดึงข้อมูลราคาจาก Yuyu-tei
# =========================================================
def scrape_yuyutei(set_id):
    url = f"https://yuyu-tei.jp/sell/opc/s/{set_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    print(f"\n📦 กำลังประมวลผลกล่อง: {set_id.upper()}")
    print(f"  > ดึงข้อมูลจาก Yuyu-tei...", end=" ")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200: return {}
    except: return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    set_data = {}
    rarity_sections = soup.select('.cards-list')
    
    for section in rarity_sections:
        rarity_badge = section.select_one('h3 span')
        if not rarity_badge: continue
        rarity = rarity_badge.text.strip()
        
        cards = section.select('.card-product')
        for card in cards:
            try:
                id_elem = card.select_one('span.border-dark')
                card_id = id_elem.text.strip() if id_elem else "UNKNOWN"
                if card_id in ["UNKNOWN", "-"]: continue
                    
                name_elem = card.select_one('h4')
                name = name_elem.text.strip() if name_elem else "Unknown"
                
                price_elem = card.select_one('strong')
                if price_elem:
                    price_str = price_elem.text.replace('円', '').replace(',', '').strip()
                    jpy_price = int(price_str) if price_str.isdigit() else 0
                else: jpy_price = 0
                    
                is_sold_out = 'sold-out' in card.get('class', [])
                img_elem = card.select_one('.product-img img')
                img_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                
                key = card_id
                is_variant = "パラレル" in name or "コミック" in name or rarity.startswith("P-") or rarity == "SP"
                
                if is_variant:
                    if card_id not in variant_counts:
                        variant_counts[card_id] = 1
                    else:
                        variant_counts[card_id] += 1
                    key = f"{card_id}_p{variant_counts[card_id]}"
                    
                set_data[key] = {
                    "name": name,
                    "rarity": rarity,
                    "jpy": jpy_price,
                    "thb": round(jpy_price * RATE),
                    "stock": not is_sold_out,
                    "image_url": img_url
                }
            except: continue
            
    print(f"สำเร็จ ({len(set_data)} ใบ)")
    return set_data

# =========================================================
# 2. ฟังก์ชันดึงข้อมูลชื่อ ENG และรูปภาพจาก Official (POST Method) 🟢
# =========================================================
def scrape_official(series_id):
    url = "https://asia-th.onepiece-cardgame.com/cardlist/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # 🟢 ส่งข้อมูลเป็น formdata เข้าไปแบบ POST
    payload = {
        "freewords": "",
        "series": series_id
    }
    
    try:
        # เปลี่ยนจากการใช้ get() มาเป็น post() แล้วแนบตัวแปร payload ผ่านคำสั่ง data=
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200: return {}
    except: return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    official_data = {}
    
    card_modals = soup.find_all('dl', class_='modalCol')
    
    for modal in card_modals:
        try:
            # ดึง ID มาเป็น Key เช่น OP15-086_p1
            card_key = modal.get('id') 
            if not card_key: continue
            
            # ดึงชื่อภาษาอังกฤษ
            name_elem = modal.find('div', class_='cardName')
            card_name = name_elem.text.strip() if name_elem else "Unknown"
            
            # ดึง URL รูปภาพ
            img_elem = modal.find('img', class_='lazy')
            img_url = ""
            if img_elem and img_elem.has_attr('data-src'):
                raw_src = img_elem['data-src']
                # แปลง URL ให้เป็นลิงก์เต็ม
                img_url = raw_src.replace("../", "https://asia-th.onepiece-cardgame.com/")
                
            official_data[card_key] = {
                "name": card_name,
                "image_url": img_url
            }
        except: continue
        
    return official_data

# =========================================================
# 3. เริ่มกระบวนการดึงข้อมูลและ Merge ข้อมูล
# =========================================================
print("--- เริ่มกระบวนการ ---")
for set_id in SETS:
    
    # 1. ดึงข้อมูลจาก Yuyu
    yuyu_data = scrape_yuyutei(set_id)
    
    # 2. ถ้ามีการ Map รหัส Series ของเว็บ Official ไว้ ให้ดึงมาทับ
    if set_id in OFFICIAL_URL_MAP:
        series_id = OFFICIAL_URL_MAP[set_id]
        print(f"  > ดึงข้อมูลภาพ/ชื่อจาก Official (Series: {series_id})...", end=" ")
        
        official_data = scrape_official(series_id)
        print(f"สำเร็จ ({len(official_data)} ใบ)")
        
        # 3. นำข้อมูล Official มาจับคู่ (เฉพาะการ์ดที่รหัสตรงกันในกล่องนั้นๆ)
        matched_count = 0
        for key in yuyu_data.keys():
            if key in official_data:
                # ทับชื่อญี่ปุ่นเป็นอังกฤษ
                yuyu_data[key]['name'] = official_data[key]['name']
                # ทับรูปจาก Yuyu เป็นรูปจากเซิร์ฟ Official (ถ้า Official มีรูปให้)
                if official_data[key]['image_url']:
                    yuyu_data[key]['image_url'] = official_data[key]['image_url']
                matched_count += 1
                
        print(f"  ✨ ทับชื่อและรูปภาพได้ทั้งหมด {matched_count} ใบ")

    # บันทึกลงตัวแปรหลักเพื่อเตรียมเซฟ JSON
    all_prices[set_id] = yuyu_data
    time.sleep(1) # พักหน่วงเวลา 1 วินาทีเพื่อไม่ให้เป็นภาระเซิร์ฟเวอร์

# บันทึกเป็นไฟล์ JSON รวม
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_prices, f, ensure_ascii=False, indent=2)

print(f"\n🎉 สำเร็จ! ดึงข้อมูลและประกอบร่างบันทึกเป็น '{OUTPUT_FILE}' เรียบร้อยแล้วครับ")