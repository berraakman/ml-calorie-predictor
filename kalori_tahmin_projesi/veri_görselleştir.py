import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Encode edilmiş veriyi yükle
veri = pd.read_csv("birlesik_kalori_encoded.csv")


#  Korelasyon Isı Haritası (Heatmap)

plt.figure(figsize=(10,6))
sns.heatmap(veri.corr(), annot=True, cmap='coolwarm')
plt.title("🔍 Korelasyon Matrisi")
plt.tight_layout()
plt.show()

# Kilo - Kalori İlişkisi

sns.scatterplot(data=veri, x="Weight", y="Calories", hue="Gender")
plt.title("⚖️ Kilo - Kalori Yakımı")
plt.show()

# Süre - Kalori İlişkisi

sns.scatterplot(data=veri, x="Duration", y="Calories", hue="Gender")
plt.title("🕒 Süre - Kalori Yakımı")
plt.show()
