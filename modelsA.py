import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import joblib

# 📌 Veriyi yükle
df = pd.read_csv("kalori_tahmin_projesi/veri_model_icin_hazir.csv")


# 📌 Kullanılacak 7 özellik (User_ID yok!)
ozellikler = ["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]
X = df[ozellikler]
y = df["Calories"]

# 📌 Eğitim/test ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔸 Linear Regression modeli
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
joblib.dump(lr_model, "linear_model.pkl")

# 🔸 Random Forest modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
joblib.dump(rf_model, "random_forest_model.pkl")

print("✅ Linear ve Random Forest modelleri başarıyla eğitildi ve kaydedildi.")
