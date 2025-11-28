# ------------------------------------------------------------
# splash_screen.py
# Pantalla inicial de carga de la aplicación.
# Incluye una animación de desvanecimiento (fade-in), una imagen,
# un mensaje informativo y una barra de progreso.
# ------------------------------------------------------------

from PyQt5.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QPixmap

class SplashScreen(QWidget):
    def __init__(self, on_finish=None):
        super().__init__()

        # ---------------------------------------------------
        # CONFIGURACIÓN DE LA VENTANA
        # ---------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint)  # Quita los bordes
        self.setFixedSize(500, 300)                  # Tamaño del splash
        self.on_finish = on_finish                  # Función que se ejecutará al terminar

        # ---------------------------------------------------
        # LAYOUT PRINCIPAL
        # ---------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # ---------------------------------------------------
        # IMAGEN DEL SPLASH (LOGO O ILUSTRACIÓN)
        # ---------------------------------------------------
        self.label = QLabel(self)
        pixmap = QPixmap("assets/splashscreen.png")  # Imagen del splash
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        # ---------------------------------------------------
        # TEXTO INFORMATIVO
        # ---------------------------------------------------
        self.text = QLabel("Cargando aplicación...")
        self.text.setFont(QFont("Arial", 14))
        self.text.setAlignment(Qt.AlignCenter)

        # ---------------------------------------------------
        # BARRA DE PROGRESO
        # *Modificación solicitada*: la subimos poniendo
        # un stretch antes de añadirla al layout.
        # ---------------------------------------------------
        self.progress = QProgressBar()
        self.progress.setObjectName("splashProgress")
        self.progress.setFixedWidth(300)
        self.progress.setAlignment(Qt.AlignCenter)

        # Añadimos los elementos al layout
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.text, alignment=Qt.AlignCenter)

        # ---------------------------------------------------
        # Stretch para subir la barra de progreso
        # Esto empuja la barra hacia arriba y evita que
        # quede pegada al borde inferior de la ventana.
        # ---------------------------------------------------
        layout.addStretch(1)

        layout.addWidget(self.progress, alignment=Qt.AlignCenter)

        # ---------------------------------------------------
        # ANIMACIÓN DE FADE-IN
        # ---------------------------------------------------
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(1500)           # Duración de la animación
        self.opacity_anim.setStartValue(0)            # Comienza transparente
        self.opacity_anim.setEndValue(1)              # Termina visible
        self.opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.opacity_anim.start()

        # ---------------------------------------------------
        # TIMER PARA SIMULAR EL PROGRESO DE CARGA
        # ---------------------------------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)  # Velocidad del llenado (ms entre pasos)
        self.counter = 0

    # ------------------------------------------------------------
    # FUNCIÓN QUE ACTUALIZA LA BARRA DE PROGRESO
    # ------------------------------------------------------------
    def update_progress(self):
        self.counter += 1
        self.progress.setValue(self.counter)

        # Cuando llega al 100%, terminamos el splash
        if self.counter >= 100:
            self.timer.stop()
            self.close()

            # Si se definió una función para continuar, la ejecutamos
            if self.on_finish:
                self.on_finish()
