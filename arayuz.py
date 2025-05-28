import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QFormLayout, QStackedWidget, QHBoxLayout, QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QPixmap
from PyQt6.QtCore import Qt
import joblib 

# -------------------
# DaireWidget: Tahmin sonucunu gösterir
# -------------------
class DaireWidget(QWidget):
    def __init__(self, kalori):
        super().__init__()
        self.kalori = kalori
        self.setMinimumSize(300, 300)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setPen(QPen(Qt.GlobalColor.black, 4))
        qp.setBrush(QColor("#FFC0CB"))  # baby pink
        rect = self.rect().adjusted(50, 50, -50, -50)
        qp.drawEllipse(rect)

        font = QFont("Arial", 22, QFont.Weight.Bold)
        qp.setFont(font)
        qp.setPen(QColor(0, 0, 0))
        text = f"{self.kalori:.2f} kcal"
        qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

# -------------------
# Ana Arayüz Sınıfı
# -------------------
class KaloriTahminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalori Tahmin Sistemi")
        self.setGeometry(100, 100, 880, 690)
        self.setFixedSize(1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6E6FA;
            }
            QWidget {
                background-color: #E6E6FA;
            }
            QPushButton {
                background-color: #800080;
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #BA55D3;
            }
           QLabel {
                font-size: 26px;
                border-radius: 20px;
                padding: 6px;
                color: #0d47a1;
            }

            /* Sadece başlık için özel stil */
            QLabel#baslikLabel {
            color: #191970;
            font-size: 47px;
            border-radius: 0px;
            padding: 0px;
            }
            QLineEdit, QComboBox {
                font-size: 20px;
                padding: 9px;
                border-radius: 10px;
                border: 1px solid #6c757d;
                background-color: #ffffff;
                color: #343a40;
            }
        """)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self.init_giris_ekrani()
        self.init_sonuc_ekrani()
        self.init_analiz_ekrani()

    
    # Giriş Ekranı: Kullanıcı girişi, form ve butonlar
   
    def init_giris_ekrani(self):
        self.giris_ekrani = QWidget()
        layout = QVBoxLayout()

        # Logo ve başlık
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaledToHeight(260, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        baslik = QLabel("Kalori Tahmin Giriş Ekranı")
        baslik.setObjectName("baslikLabel")
        baslik.setFont(QFont("Times New Roman", 100, QFont.Weight.Bold))
        baslik.setStyleSheet("color: #191970; margin-left: 20px;")
        baslik.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        baslik.setWordWrap(False)

        baslik_layout = QHBoxLayout()
        baslik_layout.addWidget(logo_label)
        baslik_layout.addWidget(baslik)
        baslik_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(baslik_layout)
        layout.setSpacing(0)

        # Form alanı
        form_widget = QWidget()
        form_layout = QHBoxLayout()
        form_widget.setLayout(form_layout)
        form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addStretch()

        form_container = QWidget()
        form_container_layout = QFormLayout()
        form_container.setLayout(form_container_layout)
        form_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(form_container)
        form_layout.addStretch()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        form_widget.setMinimumWidth(500)
        layout.addWidget(form_widget)

        # Form girişleri
        self.gender = QComboBox()
        self.gender.addItems(["Kadın", "Erkek"])
        form_container_layout.addRow("🚻 Cinsiyet:", self.gender)

        emoji_labels = {
            "Yaş": "🧓 Yaş",
            "Boy (cm)": "🧍‍♂️ Boy (cm)",
            "Kilo (kg)": "🏋️‍♂️ Kilo (kg)",
            "Süre (dk)": "⏱️ Egzersiz Süresi",
            "Nabız": "🫀 Kalp Atışı",
            "Sıcaklık (°C)": "🌡️ Sıcaklık"
        }

        self.inputs = {}
        for label in ["Yaş", "Boy (cm)", "Kilo (kg)", "Süre (dk)", "Nabız", "Sıcaklık (°C)"]:
            line = QLineEdit()
            self.inputs[label] = line
            form_container_layout.addRow(f"{emoji_labels[label]}:", line)

        # Butonlar
        tahmin_button = QPushButton("Tahmin Et")
        tahmin_button.clicked.connect(self.tahminEt)
        analiz_button = QPushButton("Veri Analizine Git")
        analiz_button.clicked.connect(self.veriAnalizineGit)

        btn_container = QWidget()
        btn_container_layout = QHBoxLayout()
        btn_container.setLayout(btn_container_layout)
        btn_container_layout.addWidget(tahmin_button, 1)
        btn_container_layout.addWidget(analiz_button, 1)
        layout.addWidget(btn_container)

        self.giris_ekrani.setLayout(layout)
        self.stacked.addWidget(self.giris_ekrani)

    # -------------------
    # Sonuç Ekranı: Tahmin sonucu ve yorum
    # -------------------
    def init_sonuc_ekrani(self):
        self.sonuc_ekrani = QWidget()
        self.sonuc_layout = QVBoxLayout()

        baslik = QLabel("🔍 Kalori Tahmin Sonucu")
        baslik.setFont(QFont("Arial", 80, QFont.Weight.Bold))
        baslik.setStyleSheet("color: #001f3f; margin-bottom: 10px;")
        baslik.setFixedHeight(100)
        baslik.setWordWrap(True)
        baslik.setMaximumWidth(1000)
        self.sonuc_layout.addWidget(baslik)

        self.daire_placeholder = None

        # Yorum bölümü
        self.yorum_label = QLabel("...")
        self.yorum_label.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        self.yorum_label.setStyleSheet("color: #001f3f; margin-top: 20px;")
        self.yorum_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.sonuc_layout.addWidget(self.yorum_label)

        self.geri_don_button = QPushButton("Geri Dön")
        self.geri_don_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.geri_don_button.clicked.connect(self.geriDon)
        self.sonuc_layout.addWidget(self.geri_don_button)

        self.sonuc_ekrani.setLayout(self.sonuc_layout)
        self.stacked.addWidget(self.sonuc_ekrani)

    
    # Analiz Ekranı: Örnek grafik görüntüleme
 
    def init_analiz_ekrani(self):
        from PyQt6.QtWidgets import QGridLayout
        self.analiz_ekrani = QWidget()
        layout = QVBoxLayout()

        baslik = QLabel("📈 Veri Analizi")
        baslik.setFont(QFont("Arial", 80, QFont.Weight.Bold))
        baslik.setStyleSheet("color: #001f3f; margin-bottom: 10px; text-align: center;")
        baslik.setFixedHeight(100)
        baslik.setWordWrap(True)
        baslik.setMaximumWidth(1000)
        layout.addWidget(baslik)

        # 2x2 grid for analysis images
        grid_layout = QGridLayout()

        grafik2 = QLabel()
        grafik2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists("skor.png"):
            grafik2.setPixmap(QPixmap("skor.png").scaledToWidth(450))
        else:
            grafik2.setText("skor.png bulunamadı.")
        grid_layout.addWidget(grafik2, 0, 0)

        grafik3 = QLabel()
        grafik3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists("kalpatis_kalori.png"):
            grafik3.setPixmap(QPixmap("kalpatis_kalori.png").scaledToWidth(450))
        else:
            grafik3.setText("kalpatis_kalori.png bulunamadı.")
        grid_layout.addWidget(grafik3, 0, 1)

        grafik4 = QLabel()
        grafik4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists("süre_kalori.png"):
            grafik4.setPixmap(QPixmap("süre_kalori.png").scaledToWidth(450))
        else:
            grafik4.setText("süre_kalori.png bulunamadı.")
        grid_layout.addWidget(grafik4, 1, 0)

        grafik5 = QLabel()
        grafik5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists("korelasyon_matrisi.png"):
            grafik5.setPixmap(QPixmap("korelasyon_matrisi.png").scaledToWidth(450))
        else:
            grafik5.setText("korelasyon_matrisi.png bulunamadı.")
        grid_layout.addWidget(grafik5, 1, 1)

        layout.addLayout(grid_layout)

        geri_btn = QPushButton("Geri Dön")
        geri_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        geri_btn.clicked.connect(self.geriDon)
        layout.addWidget(geri_btn)

        self.analiz_ekrani.setLayout(layout)
        self.stacked.addWidget(self.analiz_ekrani)

  
    # Tahmin Et Butonunun Fonksiyonu (xgb_model_final.pkl kullanılarak)
  
    def tahminEt(self):
     try:
        # Girişleri al
        gender = 1 if self.gender.currentText() == "Erkek" else 0
        yas = float(self.inputs["Yaş"].text())
        boy = float(self.inputs["Boy (cm)"].text())
        kilo = float(self.inputs["Kilo (kg)"].text())
        sure = float(self.inputs["Süre (dk)"].text())
        kalp = float(self.inputs["Nabız"].text())
        sicaklik = float(self.inputs["Sıcaklık (°C)"].text())

        # Normalize işlemi için eğitim ortalama/std değerleri (örnek)
        means = {
            "Gender": 0.5,
            "Age": 30.0,
            "Height": 170.0,
            "Weight": 70.0,
            "Duration": 30.0,
            "Heart_Rate": 100.0,
            "Body_Temp": 36.5
        }

        stds = {
            "Gender": 0.5,
            "Age": 10.0,
            "Height": 10.0,
            "Weight": 15.0,
            "Duration": 10.0,
            "Heart_Rate": 15.0,
            "Body_Temp": 0.5
        }

        ozellikler = ["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]

        # Kullanıcı girişini normalize et
        X_raw = {
            "Gender": gender,
            "Age": yas,
            "Height": boy,
            "Weight": kilo,
            "Duration": sure,
            "Heart_Rate": kalp,
            "Body_Temp": sicaklik
        }

        X_normalized = [(X_raw[k] - means[k]) / stds[k] for k in ozellikler]
        X_df = pd.DataFrame([X_normalized], columns=ozellikler)

        # Modeli yükle ve tahmin yap
        model = joblib.load("xgb_model_final.pkl")
        sonuc = float(model.predict(X_df)[0])

        print("Model Tahmini:", sonuc)

        # Önceki daireyi kaldır
        if self.daire_placeholder:
            self.sonuc_layout.removeWidget(self.daire_placeholder)
            self.daire_placeholder.deleteLater()

        # Yeni sonucu göster
        self.daire_placeholder = DaireWidget(sonuc)
        self.sonuc_layout.insertWidget(1, self.daire_placeholder)

        # Yorumu üret
        if sonuc < 100:
            yorum = "🔵 <b><span style='color:#1E90FF'>Düşük Kalori</span></b> – Metabolizma yavaş olabilir."
        elif sonuc < 250:
            yorum = "🟡 <b><span style='color:#DAA520'>Orta Kalori</span></b> – Dengeli bir egzersiz."
        else:
            yorum = "🔴 <b><span style='color:#B22222'>Yüksek Kalori</span></b> – Yoğun bir antrenman!"

        self.yorum_label.setTextFormat(Qt.TextFormat.RichText)
        self.yorum_label.setText(yorum)

        # Sayfa geçişi
        self.stacked.setCurrentWidget(self.sonuc_ekrani)

     except Exception as e:
        QMessageBox.critical(self, "Hata", f"Tahmin yapılamadı:\n{e}")



    # Diğer Ekranlar Arası Geçiş
  
    def veriAnalizineGit(self):
        self.stacked.setCurrentWidget(self.analiz_ekrani)

    def geriDon(self):
        self.stacked.setCurrentWidget(self.giris_ekrani)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KaloriTahminApp()
    pencere.show()
    sys.exit(app.exec())
