import requests
from bs4 import BeautifulSoup
import json
import time

# รายชื่อชุด OP-01 ถึง OP-15
SETS = [f"op{str(i).zfill(2)}" for i in range(1, 16)]
RATE = 0.2011
OUTPUT_FILE = "prices_full.json"

all_prices = {}

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
    # เพราะเว็บนี้จัดกลุ่มการ์ดตามความหายากไว้ในหัวข้อ
    rarity_sections = soup.select('.cards-list')
    
    for section in rarity_sections:
        # ดึงความหายากจากหัวข้อ (เช่น P-SEC, SR, R)
        rarity_badge = section.select_one('h3 span')
        if not rarity_badge:
            continue
            
        rarity = rarity_badge.text.strip()
        
        # ค้นหาการ์ดทุกใบที่อยู่ในโซนความหายากนี้ (Class: .card-product)
        cards = section.select('.card-product')
        
        for card in cards:
            try:
                # 1. รหัสการ์ด (อยู่ใน <span> ที่มีขอบสีดำ)
                id_elem = card.select_one('span.border-dark')
                card_id = id_elem.text.strip() if id_elem else "UNKNOWN"
                if card_id == "UNKNOWN" or card_id == "-":
                    continue
                    
                # 2. ชื่อการ์ด (อยู่ในแท็ก <h4>)
                name_elem = card.select_one('h4')
                name = name_elem.text.strip() if name_elem else "Unknown"
                
                # 3. ราคา (อยู่ในแท็ก <strong>)
                price_elem = card.select_one('strong')
                if price_elem:
                    # ตัดคำว่า " 円" และเครื่องหมายลูกน้ำออก
                    price_str = price_elem.text.replace('円', '').replace(',', '').strip()
                    jpy_price = int(price_str) if price_str.isdigit() else 0
                else:
                    jpy_price = 0
                    
                # 4. สต็อก (ถ้ากล่องการ์ดมีคลาส sold-out แปลว่าของหมด)
                is_sold_out = 'sold-out' in card.get('class', [])
                
                # 5. สร้าง Key แยกการ์ด Parallel และ Super Parallel
                key = card_id
                
                # ถ้ามีคำว่า スーパーパラレル (Super Parallel) หรือ コミック (Comic)
                if "スーパーパラレル" in name or "コミック" in name or rarity == "SP":
                    key = f"{card_id}_p2"
                # ถ้ามีแค่คำว่า パラレル (Parallel) หรือความหายากขึ้นต้นด้วย P- (เช่น P-SR)
                elif "パラレル" in name or rarity.startswith("P-"):
                    key = f"{card_id}_p1"
                    
                # บันทึกข้อมูลลง Dictionary
                set_data[key] = {
                    "name": name,
                    "rarity": rarity,
                    "jpy": jpy_price,
                    "thb": round(jpy_price * RATE),
                    "stock": not is_sold_out
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
    time.sleep(2) # หน่วงเวลา 2 วินาทีระหว่างเปลี่ยนหน้า เพื่อไม่ให้รบกวนเซิร์ฟเวอร์เขาหนักเกินไป

# บันทึกเป็นไฟล์ JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_prices, f, ensure_ascii=False, indent=2)

print(f"\n🎉 สำเร็จ! ดึงข้อมูลครบทุกกล่อง และบันทึกไฟล์เป็น '{OUTPUT_FILE}' เรียบร้อยครับ")