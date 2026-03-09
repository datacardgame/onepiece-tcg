import requests
from bs4 import BeautifulSoup
import json
import time

# รายชื่อชุด OP-01 ถึง OP-15
SETS = [f"op{str(i).zfill(2)}" for i in range(1, 16)]
RATE = 0.2011
OUTPUT_FILE = "prices_full.json"

all_prices = {}

# 🟢 สร้าง Dictionary ส่วนกลางเพื่อจำว่า การ์ดแต่ละรหัสเจอภาพพิเศษไปกี่ใบแล้ว
variant_counts = {}

def scrape_yuyutei(set_id):
    url = f"https://yuyu-tei.jp/sell/opc/s/{set_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"กำลังดึงข้อมูล: {set_id.upper()} ...", end=" ")
    
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}
        
    if response.status_code != 200:
        print(f"❌ Status Code: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    
    set_data = {}
    card_count = 0
    
    # วนลูปหา "โซนความหายาก" (Class: .cards-list)
    rarity_sections = soup.select('.cards-list')
    
    for section in rarity_sections:
        # ดึงความหายากจากหัวข้อ
        rarity_badge = section.select_one('h3 span')
        if not rarity_badge:
            continue
            
        rarity = rarity_badge.text.strip()
        
        # ค้นหาการ์ดทุกใบที่อยู่ในโซนความหายากนี้
        cards = section.select('.card-product')
        
        for card in cards:
            try:
                # 1. รหัสการ์ด
                id_elem = card.select_one('span.border-dark')
                card_id = id_elem.text.strip() if id_elem else "UNKNOWN"
                if card_id == "UNKNOWN" or card_id == "-":
                    continue
                    
                # 2. ชื่อการ์ด
                name_elem = card.select_one('h4')
                name = name_elem.text.strip() if name_elem else "Unknown"
                
                # 3. ราคา
                price_elem = card.select_one('strong')
                if price_elem:
                    price_str = price_elem.text.replace('円', '').replace(',', '').strip()
                    jpy_price = int(price_str) if price_str.isdigit() else 0
                else:
                    jpy_price = 0
                    
                # 4. สต็อก
                is_sold_out = 'sold-out' in card.get('class', [])
                
                # =======================================================
                # 5. 🟢 เปลี่ยนมาใช้ระบบบวกเลข Suffix อัตโนมัติ (_p1, _p2, _p3...)
                # =======================================================
                key = card_id
                
                # ตรวจสอบว่าเป็นการ์ดลายพิเศษไหม (มีคำว่า Parallel, Comic หรือเป็นระดับ SP, ขึ้นต้นด้วย P-)
                is_variant = "パラレル" in name or "コミック" in name or rarity.startswith("P-") or rarity == "SP"
                
                if is_variant:
                    # ถ้าเพิ่งเคยเจอการ์ดรหัสนี้ที่เป็นภาพพิเศษครั้งแรก ให้นับเป็น 1
                    if card_id not in variant_counts:
                        variant_counts[card_id] = 1
                    # ถ้าเคยเจอมาแล้วจากกล่องก่อนหน้า ให้บวกเพิ่มอีก 1
                    else:
                        variant_counts[card_id] += 1
                        
                    # ประกอบร่าง Key ใหม่ (เช่น OP01-120_p2, OP01-120_p3)
                    key = f"{card_id}_p{variant_counts[card_id]}"

                # 6. ดึง URL รูปภาพจาก Yuyu-tei 🟢
                img_elem = card.select_one('.product-img img')
                img_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                    
                # บันทึกข้อมูลลง Dictionary
                set_data[key] = {
                    "name": name,
                    "rarity": rarity,
                    "jpy": jpy_price,
                    "thb": round(jpy_price * RATE),
                    "stock": not is_sold_out,
                    "image_url": img_url
                }
                card_count += 1
                
            except Exception as e:
                continue
                
    print(f"✅ ได้มา {card_count} ใบ")
    return set_data

# เริ่มกระบวนการดูดข้อมูล (Scraping)
print("--- เริ่มดึงข้อมูลจาก Yuyu-tei ---")
for s in SETS:
    all_prices[s] = scrape_yuyutei(s)
    time.sleep(2) # หน่วงเวลา 2 วินาทีระหว่างเปลี่ยนหน้า

# บันทึกเป็นไฟล์ JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_prices, f, ensure_ascii=False, indent=2)

print(f"\n🎉 สำเร็จ! ดึงข้อมูลครบทุกกล่อง (รองรับการรันเลข _p2, _p3 อัตโนมัติ) และบันทึกเป็น '{OUTPUT_FILE}' เรียบร้อยครับ")