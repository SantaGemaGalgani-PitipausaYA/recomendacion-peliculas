from PyQt5.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QPixmap

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        layout= QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self)
        try:
            pixmap = QPixmap("assets/splashscreen.png").scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)
        except:
            self.label.setText("PITIPAUSA YA!")
            self.label.setFont(QFont("Arial", 28))

        self.text = QLabel("Cargando aplicación...")
        self.text.setFont(QFont("Arial", 14))

        self.progress = QProgressBar()
        self.progress.setFixedWidth(300)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid white;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(self.progress)

        self.setLayout(layout)

        # Animación de fade-in
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(1500)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.opacity_anim.start()

        # Iniciar carga de barra
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)

        self.counter = 0

    def update_progress(self):
        self.counter += 1
        self.progress.setValue(self.counter)

        if self.counter >= 100:
            self.timer.stop()
            self.close()
            self.on_finish()  # Señal manual al main

    def on_finish(self):
        # Esta función será sobreescrita desde main.py
        pass