import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 🔹 Veriyi oku
df = pd.read_csv("kalori_tahmin_projesi/veri_model_icin_hazir.csv")

# 🔹 Sadece bu 7 özelliği kullan (tüm modellerle tutarlı!)
ozellikler = ["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]
X = df[ozellikler]
y = df["Calories"]

# 🔹 Eğitim/test ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔸 Modelleri yükle
lr_model = joblib.load("linear_model.pkl")
rf_model = joblib.load("random_forest_model.pkl")
xgb_model = joblib.load("xgb_model_final.pkl")

# 🔍 Tahminler
y_pred_lr = lr_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)
y_pred_xgb = xgb_model.predict(X_test)

# 📊 Metrikler (RMSE, MAE, R²)
def evaluate(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return rmse, mae, r2

rmse_lr, mae_lr, r2_lr = evaluate(y_test, y_pred_lr)
rmse_rf, mae_rf, r2_rf = evaluate(y_test, y_pred_rf)
rmse_xgb, mae_xgb, r2_xgb = evaluate(y_test, y_pred_xgb)

# 📋 Sonuçları yazdır
print("📊 Model Karşılaştırma:")
print(f"🔸 Linear Regression - RMSE: {rmse_lr:.2f} | MAE: {mae_lr:.2f} | R²: {r2_lr:.4f}")
print(f"🔸 Random Forest      - RMSE: {rmse_rf:.2f} | MAE: {mae_rf:.2f} | R²: {r2_rf:.4f}")
print(f"🔸 XGBoost            - RMSE: {rmse_xgb:.2f} | MAE: {mae_xgb:.2f} | R²: {r2_xgb:.4f}")

# 📈 Grafik
model_adlari = ["Linear", "RandomForest", "XGBoost"]
rmse_skorlari = [rmse_lr, rmse_rf, rmse_xgb]
mae_skorlari = [mae_lr, mae_rf, mae_xgb]
r2_skorlari = [r2_lr, r2_rf, r2_xgb]

plt.figure(figsize=(10, 6))

# RMSE
plt.subplot(1, 3, 1)
plt.bar(model_adlari, rmse_skorlari)
plt.title("RMSE (Düşük daha iyi)")
plt.ylabel("RMSE")

# MAE
plt.subplot(1, 3, 2)
plt.bar(model_adlari, mae_skorlari)
plt.title("MAE (Düşük daha iyi)")

# R²
plt.subplot(1, 3, 3)
plt.bar(model_adlari, r2_skorlari)
plt.title("R² Score (Yüksek daha iyi)")

plt.tight_layout()
plt.show()
