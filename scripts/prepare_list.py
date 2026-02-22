import pandas as pd
from pathlib import Path
import re

# Dosya Yolları
input_path = Path("data/processed/esco_skills_selected.csv")
output_path = Path("data/processed/esco_all_skill_names_including_alts.csv")

# Veriyi oku
df = pd.read_csv(input_path)

# 1. Preferred Labels listesi
preferred_series = df["preferredLabel"].astype(str).str.strip()

# 2. Alt Labels listesi (Hata veren kısım burasıydı)
alt_series = (
    df["altLabels"]
    .apply(lambda x: [i.strip() for i in re.split(r"[;\n]+", str(x)) if i.strip() and str(i).lower() != "nan"])
)

# Listeyi satırlara yayıyoruz
alt_expanded = alt_series.explode()

# 3. Birleştirme
all_names = pd.concat([preferred_series, alt_expanded], ignore_index=True)

# 4. Final Temizlik
all_names = (
    all_names
    .astype(str)  # Her şeyi stringe zorla
    .str.strip()
    .replace(["nan", "None", ""], pd.NA)
    .dropna()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

# Kaydet
all_names.to_frame("skill_name").to_csv(output_path, index=False)

print(f"Toplam benzersiz yetenek ismi listelendi: {len(all_names)}")