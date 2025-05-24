import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Veriyi yükle
veri = pd.read_csv("birlesik_kalori.csv")


# Gender sütunu var mı?

if "Gender" in veri.columns:
    le = LabelEncoder()
    veri["Gender"] = le.fit_transform(veri["Gender"])  # male→1, female→0 gibi
    print("✅ Gender sütunu encode edildi:")
    print(veri["Gender"].head())
else:
    print("❌ Gender sütunu bulunamadı!")


# Encode edilmiş veriyi kaydet

veri.to_csv("birlesik_kalori_encoded.csv", index=False)
print("💾 Encode edilmiş veri kaydedildi: birlesik_kalori_encoded.csv")
