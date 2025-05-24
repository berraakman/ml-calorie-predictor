import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Veriyi yükle
veri = pd.read_csv("birlesik_kalori_encoded.csv")

# Korelasyon Matrisi (Heatmap)
plt.figure(figsize=(10, 6))
sns.heatmap(veri.corr(), annot=True, cmap="coolwarm")
plt.title("Korelasyon Matrisi: Calories ile en ilişkili değişkenler")
plt.tight_layout()
plt.show()

# Weight vs Calories
plt.figure()
sns.scatterplot(data=veri, x="Weight", y="Calories", hue="Gender")
plt.title("Kilo - Kalori İlişkisi")
plt.tight_layout()
plt.show()

# Duration vs Calories
plt.figure()
sns.scatterplot(data=veri, x="Duration", y="Calories", hue="Gender")
plt.title("Süre - Kalori İlişkisi")
plt.tight_layout()
plt.show()

# Heart_Rate vs Calories
plt.figure()
sns.scatterplot(data=veri, x="Heart_Rate", y="Calories", hue="Gender")
plt.title("Kalp Atış Hızı - Kalori İlişkisi")
plt.tight_layout()
plt.show()
