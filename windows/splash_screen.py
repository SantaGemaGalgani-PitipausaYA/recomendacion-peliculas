# splash_screen.py
from PyQt5.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QPixmap

class SplashScreen(QWidget):
    def __init__(self, on_finish=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(500, 300)
        self.on_finish = on_finish

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.label = QLabel(self)
        pixmap = QPixmap("assets/splashscreen.png")
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.text = QLabel("Cargando aplicación...")
        self.text.setFont(QFont("Arial", 14))
        self.text.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setObjectName("splashProgress")
        self.progress.setFixedWidth(300)
        self.progress.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.text, alignment=Qt.AlignCenter)
        layout.addWidget(self.progress, alignment=Qt.AlignCenter)

        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(1500)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.opacity_anim.start()

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
            if self.on_finish:
                self.on_finish()
