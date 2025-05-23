import sys
import numpy as np
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QFormLayout, QStackedWidget, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QPixmap
from PyQt6.QtCore import Qt

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

class KaloriTahminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalori Tahmin Sistemi")
        self.setGeometry(100, 100, 600, 800)
        self.setFixedSize(800,600 )
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e0e0e0;
            }
            QWidget {
                background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #1a5e6a;  /* teal */
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #17a2b8;  /* cyan hover */
            }
            QLabel {
                font-size: 20px;
                border-radius: 10px;
                padding: 6px;
                color: #0d47a1;
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

    def init_giris_ekrani(self):
        self.giris_ekrani = QWidget()
        layout = QVBoxLayout()

        baslik = QLabel("Kalori Tahmin Giriş Ekranı")
        baslik.setFont(QFont("Arial", 100, QFont.Weight.Bold))
        baslik.setStyleSheet("color: #001f3f; margin-bottom: 10px;")
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baslik.setFixedHeight(90)
        baslik.setWordWrap(True)
        baslik.setMaximumWidth(1000)
        layout.addWidget(baslik, alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.gender = QComboBox()
        self.gender.addItems(["Kadın", "Erkek"])
        form_container_layout.addRow("🚻 Cinsiyet:", self.gender)

        emoji_labels = {
            "Yaş": "🧓 Yaş",
            "Boy (cm)": "🧍‍♂️ Boy (cm)",
            "Kilo (kg)": "🏋️‍♂️ Kilo (kg)",
            "Süre (dk)": "⏱️ Egzersiz Süresi",
            "Nabız": "🫀 Kalp Atışı",
            "Sıcaklık (°C)": "🌡️ Termometre"
        }

        self.inputs = {}
        for label in ["Yaş", "Boy (cm)", "Kilo (kg)", "Süre (dk)", "Nabız", "Sıcaklık (°C)"]:
            line = QLineEdit()
            self.inputs[label] = line
            form_container_layout.addRow(f"{emoji_labels[label]}:", line)

        layout.addWidget(form_widget)

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

        alt_baslik = QLabel("📊 Değerlendirme")
        alt_baslik.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        alt_baslik.setStyleSheet("color: #001f3f; margin-top: 20px;")
        alt_baslik.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.sonuc_layout.addWidget(alt_baslik)

        yorum_label = QLabel("...")
        yorum_label.setFont(QFont("Arial", 18))
        yorum_label.setStyleSheet("color: #444; margin-left: 20px;")
        yorum_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.sonuc_layout.addWidget(yorum_label)

        self.geri_don_button = QPushButton("Geri Dön")
        self.geri_don_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.geri_don_button.clicked.connect(self.geriDon)

        self.sonuc_layout.addWidget(self.geri_don_button)
        self.sonuc_ekrani.setLayout(self.sonuc_layout)
        self.stacked.addWidget(self.sonuc_ekrani)

    def init_analiz_ekrani(self):
        self.analiz_ekrani = QWidget()
        layout = QVBoxLayout()

        baslik = QLabel("📈 Veri Analizi")
        baslik.setFont(QFont("Arial", 80, QFont.Weight.Bold))
        baslik.setStyleSheet("color: #001f3f; margin-bottom: 10px; text-align: center;")
        baslik.setFixedHeight(100)
        baslik.setWordWrap(True)
        baslik.setMaximumWidth(1000)
        layout.addWidget(baslik)

        grafik = QLabel()
        grafik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists("correlation.png"):
            grafik.setPixmap(QPixmap("correlation.png").scaledToWidth(500))
        else:
            grafik.setText("correlation.png bulunamadı.")

        geri_btn = QPushButton("Geri Dön")
        geri_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        geri_btn.clicked.connect(self.geriDon)

        layout.addWidget(grafik)
        layout.addWidget(geri_btn)
        self.analiz_ekrani.setLayout(layout)
        self.stacked.addWidget(self.analiz_ekrani)

    def tahminEt(self):
        dummy_kalori = np.random.uniform(180, 400)

        if self.daire_placeholder is not None:
            self.sonuc_layout.removeWidget(self.daire_placeholder)
            self.daire_placeholder.deleteLater()

        self.daire_placeholder = DaireWidget(dummy_kalori)
        self.sonuc_layout.insertWidget(1, self.daire_placeholder)

        self.stacked.setCurrentWidget(self.sonuc_ekrani)

    def veriAnalizineGit(self):
        self.stacked.setCurrentWidget(self.analiz_ekrani)

    def geriDon(self):
        self.stacked.setCurrentWidget(self.giris_ekrani)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KaloriTahminApp()
    pencere.show()
    sys.exit(app.exec())