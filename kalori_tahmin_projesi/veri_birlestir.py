import pandas as pd

# 1. CSV dosyalarını oku
calories = pd.read_csv("calories.csv")
exercise = pd.read_csv("exercise.csv")

# 2. Ortak sütun "User_ID" üzerinden birleştir
veri = pd.merge(exercise, calories, on="User_ID")

# 3. Kontrol için ilk 5 satırı yazdır
print("Birleşmiş Veri:")
print(veri.head())

# 4. Dilersen kaydet (isteğe bağlı)
veri.to_csv("birlesik_kalori.csv", index=False)
