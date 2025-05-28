import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib
import numpy as np

# 🔹 Veriyi oku
df = pd.read_csv("kalori_tahmin_projesi/veri_model_icin_hazir.csv")


# 🔹 Kullanılacak 7 özellik
ozellikler = ["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]
X = df[ozellikler]
y = df["Calories"]

# 🔹 Eğitim/test ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔸 XGBoost modelini eğit
xgb_model = XGBRegressor()
xgb_model.fit(X_train, y_train)

# 🔸 Modeli kaydet
joblib.dump(xgb_model, "xgb_model_final.pkl")
print("✅ XGBoost modeli başarıyla kaydedildi.\n")

# 🔍 Test verisi ile tahmin yap
y_pred = xgb_model.predict(X_test)

# 📊 Değerlendirme metrikleri
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 📋 Sonuçları yazdır
print("📊 Model Performansı (Test Verisi):")
print(f"🔹 RMSE (Root Mean Squared Error): {rmse:.2f}")
print(f"🔹 MAE  (Mean Absolute Error)     : {mae:.2f}")
print(f"🔹 R²   (R2 Score)                 : {r2:.4f}")


# Test örnekleri
X1 = pd.DataFrame([[1.0, 1.0, 1.5, 1.1, 1.6, 0.99, 0.99]], columns=ozellikler)
X2 = pd.DataFrame([[-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]], columns=ozellikler)

# Tahmin
model = joblib.load("xgb_model_final.pkl")
print("🔎 Tahmin 1:", model.predict(X1)[0])
print("🔎 Tahmin 2:", model.predict(X2)[0])
