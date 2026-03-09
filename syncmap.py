import requests
from bs4 import BeautifulSoup
import json
import time
import os # นำเข้า module os เพื่อเช็คว่ามีไฟล์อยู่จริงไหม

# =========================================================
# ⚙️ ตั้งค่าระบบ
# =========================================================
SETS = [f"op{str(i).zfill(2)}" for i in range(1, 16)]
RATE = 0.2011
OUTPUT_FILE = "prices_full.json"
MAPPING_FILE = "mapping_img.json" # 🟢 ชื่อไฟล์ Mapping ที่คุณเตรียมไว้

all_prices = {}
variant_counts = {}

# 🟢 1. โหลดข้อมูลจาก mapping_img.json ไว้ใน Memory ก่อนเริ่มทำงาน
local_mapping_data = {}
if os.path.exists(MAPPING_FILE):
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        local_mapping_data = json.load(f)
    print(f"📁 โหลดไฟล์ {MAPPING_FILE} สำเร็จ เตรียมพร้อมสำหรับ Mapping!")
else:
    print(f"⚠️ ไม่พบไฟล์ {MAPPING_FILE} ระบบจะใช้ชื่อและรูปจาก Yuyu-tei เป็นค่าเริ่มต้น")


# =========================================================
# 2. ฟังก์ชันดึงข้อมูลราคาจาก Yuyu-tei
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
                    "name": name,          # ค่าตั้งต้นจาก Yuyu
                    "rarity": rarity,
                    "jpy": jpy_price,
                    "thb": round(jpy_price * RATE),
                    "stock": not is_sold_out,
                    "image_url": img_url   # ค่าตั้งต้นจาก Yuyu
                }
            except: continue
            
    print(f"สำเร็จ ({len(set_data)} ใบ)")
    return set_data


# =========================================================
# 3. เริ่มกระบวนการดึงข้อมูลและ Merge ข้อมูล
# =========================================================
print("--- เริ่มกระบวนการ ---")
for set_id in SETS:
    
    # ดึงข้อมูลจาก Yuyu
    yuyu_data = scrape_yuyutei(set_id)
    
    # 🟢 นำข้อมูลจาก local_mapping_data มาจับคู่ (เฉพาะภายในกล่องนั้นๆ)
    if set_id in local_mapping_data:
        matched_count = 0
        for key in yuyu_data.keys():
            if key in local_mapping_data[set_id]:
                map_info = local_mapping_data[set_id][key]
                
                # ทับชื่อเป็นภาษาอังกฤษ (ถ้าใน JSON มีระบุไว้)
                if "name" in map_info and map_info["name"]:
                    yuyu_data[key]['name'] = map_info["name"]
                    
                # ทับรูปภาพเป็นของเว็บ Official (ถ้าใน JSON มีระบุไว้)
                if "image_url" in map_info and map_info["image_url"]:
                    yuyu_data[key]['image_url'] = map_info["image_url"]
                    
                matched_count += 1
                
        print(f"  ✨ ทับชื่อและรูปภาพจาก mapping_img.json ได้ทั้งหมด {matched_count} ใบ")

    # บันทึกลงตัวแปรหลักเพื่อเตรียมเซฟ JSON
    all_prices[set_id] = yuyu_data
    time.sleep(1) # พักหน่วงเวลา 1 วินาทีเพื่อไม่ให้เป็นภาระเซิร์ฟเวอร์ Yuyu

# บันทึกเป็นไฟล์ JSON รวม
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_prices, f, ensure_ascii=False, indent=2)

print(f"\n🎉 สำเร็จ! ดึงข้อมูลและประกอบร่างบันทึกเป็น '{OUTPUT_FILE}' เรียบร้อยแล้วครับ")