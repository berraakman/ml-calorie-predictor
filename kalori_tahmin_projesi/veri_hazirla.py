import pandas as pd
from sklearn.preprocessing import StandardScaler

# Encode edilmiş veriyi yükle
veri = pd.read_csv("birlesik_kalori_encoded.csv")

#  Hedef sütun: Calories

y = veri["Calories"]  # Tahmin etmek istediğimiz değer
X = veri.drop("Calories", axis=1)  # Geri kalan tüm sütunlar: özellikler


#  Scaling (Normalizasyon)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# X ve y'yi ayrı ayrı kaydet (isteğe bağlı)

X_df = pd.DataFrame(X_scaled, columns=X.columns)
X_df["Calories"] = y.values

X_df.to_csv("veri_model_icin_hazir.csv", index=False)
print("✅ X ve y ayrıldı, veriler ölçeklendi ve kaydedildi.")
