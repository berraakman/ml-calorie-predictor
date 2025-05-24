import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veri setini yükle
veri = pd.read_csv("birlesik_kalori.csv")
# GENEL BİLGİ

print("✅ Veri Yapısı (info):")
print(veri.info())
print("\n✅ İlk 5 Satır:")
print(veri.head())
print("\n✅ Sayısal Özet:")
print(veri.describe())

# EKSİK VERİ KONTROLÜ


print("\n🔍 Eksik Veri Kontrolü:")
print(veri.isnull().sum())

#  AYKIRI DEĞER KONTROLÜ (Boxplot ile)


print("\n📊 Aykırı değer kontrolü başlatılıyor...")

plt.figure(figsize=(12,6))
sns.boxplot(data=veri.select_dtypes(include='number'))  # sadece sayısal sütunlar
plt.title("Aykırı Değer Kontrolü (Boxplot)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
