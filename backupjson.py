import json

# อ่านไฟล์ต้นฉบับ
with open("prices_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

result = {}

for group, cards in data.items():
    result[group] = {}
    for card_id, card in cards.items():
        result[group][card_id] = {
            "name": card.get("name"),
            "image_url": card.get("image_url")
        }

# เขียนไฟล์ใหม่
with open("mapping_img.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("Done: mapping_img.json created")