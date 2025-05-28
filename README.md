
# 🔥 ML Calorie Predictor

Bu proje, kullanıcıdan alınan fiziksel özellikler ve egzersiz bilgilerine göre yakılan kalori miktarını tahmin eden bir makine öğrenmesi modeline sahiptir. PyQt6 ile geliştirilen kullanıcı dostu bir arayüz sayesinde kullanıcılar kolayca verilerini girip anında tahmin sonucunu görebilir.

---

## 🎯 Proje Amacı

- Kullanıcının fiziksel ve egzersiz verilerine dayanarak yakılan kalori miktarını tahmin etmek
- Farklı regresyon modellerini eğitip karşılaştırarak en iyi performansı elde etmek
- En iyi modeli kullanıcı arayüzüne entegre etmek
- Kullanımı kolay ve görsel açıdan zengin bir uygulama geliştirmek

---

## 👩‍💻 Görev Dağılımı

| Ekip Üyesi              | Sorumluluklar                                                                 |
|-------------------------|-------------------------------------------------------------------------------|
| **Berra Akman**         | PyQt6 ile arayüz geliştirme, Linear ve Random Forest modellerinin eğitimi      |
| **Dilara Cömert**       | PyQt6 ile arayüz geliştirme, XGBoost modeli eğitimi, model karşılaştırma analizleri     |
| **Zeynep Zümral Kılıç** | Verilerin temizlenmesi, görselleştirme, veri setlerinin birleştirilmesi      |

---

## ⚙️ Kullanılan Teknolojiler

- Python 3.10+
- scikit-learn
- XGBoost
- pandas & numpy
- matplotlib
- joblib
- PyQt6
- VS Code / Jupyter Notebook
- Git & GitHub

---

## 🤖 Model Eğitimi & Karşılaştırma

| Model                 | RMSE (Hata) | R² Skoru | Açıklama                          |
|-----------------------|-------------|----------|-----------------------------------|
| Linear Regression     | 11.49        | 0.9673     | İyi Performans       |
| Random Forest         | 2.65       | 0.9983     | Daha iyi performans               |
| **XGBoost Regressor** | **1.54**    | **0.9988** | 🔥 **En iyi sonuç, seçilen model** |

📌 Seçilen model: XGBoost  
Model dosyası: `xgb_model.pkl`  
`arayuz.py` dosyasına entegre edilmiştir.

---

## 📁 Veri Seti Açıklamaları

### 🔹 Kullanılan Veri Dosyaları

| Dosya Adı                    | Açıklama                                                                  |
|------------------------------|---------------------------------------------------------------------------|
| veriler/dataset1.csv         | İlk ham veri seti, eksik ve gürültülü veriler içermekteydi                |
| veriler/dataset_birlesmis.csv| Temizlenmiş ve birleştirilmiş ana veri seti (model eğitimi için kullanıldı) |

➡️ Veri işleme ve görselleştirme işlemleri Zeynep Zümral Kılıç tarafından gerçekleştirilmiştir.

---

## 📥 Kullanıcıdan Alınan Girişler

PyQt6 arayüzü (`arayuz.py`) kullanıcılardan şu bilgileri alır:

- Cinsiyet (`gender`)
- Yaş (`yas`)
- Boy (`boy`)
- Kilo (`kilo`)
- Egzersiz Süresi (`sure`)
- Nabız (`kalp`)
- Sıcaklık (`sicaklik`)

X = [[gender, yas, boy, kilo, sure, kalp, sicaklik]]

---

## 🎯 Model Çıktısı

| Çıktı Değeri          | Açıklama                                            |
|-----------------------|-----------------------------------------------------|
| Calories (kcal)       | Modelin tahmin ettiği egzersizle yakılan kalori miktarı |

---

## 🖼️ Ekran Görüntüleri

- Giriş Ekranı: `screenshots/giris.png`
- Tahmin Ekranı: `screenshots/tahmin.png`
- Veri Analiz Ekranı: `screenshots/veri_analiz.png`

---

## 📂 Proje Yapısı

ml-calorie-predictor/
├── arayuz.py
├── modelsA.py
├── model_karsilastir.py
├── modelB.py
├── linear_model.pkl
├── random_forest_model.pkl
├── xgb_model_final.pkl
├── scaler_son.pkl
├── scaler.pkl
├── skor_tablosu.txt
├── skor_grafik.png
├── süre_kalori.png
├── kalpatis_kalori.png
├── kilo_kalori.png
├── korelasyon_matrisi.png
├── veri_analiz.png
├── screenshots/
│   ├── giris.png
│   ├── tahmin.png
│   ├── veri_analiz.png
├── kalori_tahmin_projesi/
│   ├── exercise.csv
│   ├── calories.csv
│   ├── birlesik_kalori.csv
│   ├── birlesik_kalori_encoded.csv
│   ├── veri_model_icin_hazir.csv
│   ├── veri_birlestir.py
│   ├── veri_encoding.py
│   ├── veri_analiz.py
│   ├── veri_görselleştir.py
│   └── veri_hazirla.py
├── README.md

---

## ⚙️ Kurulum Talimatları

1. Depoyu klonlayın:
git clone https://github.com/berraakman/ml-calorie-predictor.git  
cd ml-calorie-predictor

2. Sanal ortam oluşturun (isteğe bağlı ama önerilir):
python -m venv venv  
source venv/bin/activate  # macOS/Linux  
venv\Scripts\activate   # Windows

3. Kütüphaneleri yükleyin:
pip install -r requirements.txt

4. Uygulamayı çalıştırın:
python arayuz.py

---

## ✅ Tamamlananlar

- [x] Veri temizliği ve birleştirme
- [x] Farklı modellerin eğitilmesi
- [x] Model karşılaştırması yapılması
- [x] En iyi modelin (XGBoost) arayüze entegrasyonu
- [x] PyQt6 arayüz geliştirme
- [x] Grafik analizler ve ekran görüntüleri

---

## 📝 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
