import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("kalori_tahmin_projesi/veri_model_icin_hazir.csv")

#Özellikler (X), hedef (y) 
X = df.drop(["Calories"], axis=1)
y = df["Calories"]

# Eğitim ve test seti olarak ayırıldı
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression modeli 
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
joblib.dump(lr_model, "linear_model.pkl")

# Random Forest Regressor modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
joblib.dump(rf_model, "random_forest_model.pkl")

print("Modeller başarıyla eğitildi ve kaydedildi.")