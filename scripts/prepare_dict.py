import pandas as pd
from pathlib import Path
import re
import json

# Dosya Yolları
input_path = Path("data/processed/esco_skills_selected.csv")
output_path = Path("data/processed/esco_skill_dictionary.json")

# Veriyi oku
df = pd.read_csv(input_path)

skill_dict = {}

for _, row in df.iterrows():
    # Temizleme: Preferred Label
    preferred = str(row["preferredLabel"]).strip()
    if not preferred or preferred.lower() == "nan":
        continue
        
    # Temizleme: Alt Labels (Regex ile parçala ve boşlukları at)
    alt_raw = str(row["altLabels"])
    if alt_raw.lower() == "nan" or alt_raw.strip() == "":
        alts = []
    else:
        # Hem ; hem \n karakterlerine göre böl, temizle ve boş olanları filtrele
        alts = [x.strip() for x in re.split(r"[;\n]+", alt_raw) if x.strip()]
    
    # Temizleme: Description
    description = str(row["description"]).strip()
    if description.lower() == "nan":
        description = ""

    # Sözlüğe ekle (Eğer aynı preferredLabel varsa üzerine yazar/günceller)
    skill_dict[preferred] = {
        "alternative_names": alts,
        "description": description
    }

# JSON olarak kaydet
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(skill_dict, f, ensure_ascii=False, indent=2)

print(f"Sözlük başarıyla oluşturuldu: {len(skill_dict)} ana yetenek.")