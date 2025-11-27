# ficha_pelicula_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

class FichaPeliculaWindow(QWidget):
    def __init__(self, pelicula_id=None, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle(f"Ficha de Película: {pelicula_id}")
        self.setGeometry(100, 100, 500, 360)

        layout = QVBoxLayout()
        header = QHBoxLayout()
        header_text = QVBoxLayout()

        film_image = QLabel()
        pixmap_film = QPixmap("assets/film_placeholder.jpg").scaled(120, 180)
        film_image.setPixmap(pixmap_film)

        title_label = QLabel("Título de la película")
        title_label.setObjectName("titleLabel")

        synopsis_label = QLabel("Sinopsis")
        synopsis_label.setObjectName("titleLabel")
        synopsis_text = QLabel("Texto de sinopsis detallada...")
        synopsis_text.setWordWrap(True)
        synopsis_text.setObjectName("synopsisText")

        header_text.addWidget(title_label)
        header_text.addWidget(synopsis_label)
        header.addWidget(film_image)
        header.addLayout(header_text)

        layout.addLayout(header)
        layout.addWidget(synopsis_text)

        buttons = QHBoxLayout()
        btn_ver_despues = QPushButton("Ver después")
        btn_ver_despues.setProperty("class", "app_boton")
        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_marcar_vista = QPushButton("Marcar como vista")
        btn_marcar_vista.setProperty("class", "app_boton")
        buttons.addWidget(btn_ver_despues)
        buttons.addWidget(btn_calificar)
        buttons.addWidget(btn_marcar_vista)

        layout.addLayout(buttons)
        self.setLayout(layout)
