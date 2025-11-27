from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

class FichaPeliculaWindow(QWidget):
    def __init__(self, pelicula_id=None):
        super().__init__()
        self.setWindowTitle("Ficha de Película : " + str(pelicula_id))  # Cambiar por el título real
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        header = QHBoxLayout()
        header_text = QVBoxLayout()

        # Imagen de la película
        film_image = QLabel("Imagen de la Película")
        pixmap_film = QPixmap("path/to/film_image.jpg").scaled(100, 150)
        film_image.setPixmap(pixmap_film)

        # Título con estilo
        title_label = QLabel(str(pelicula_id))  # Cambiar por el título real
        title_label.setObjectName("titleLabel")

        # Sinopsis
        synopsis_label = QLabel("Sinopsis de la Película")
        synopsis_label.setObjectName("titleLabel")
        synopsis_text = QLabel(
            "Aquí va la sinopsis detallada de la película. Esta sección contendrá una descripción completa "
            "de la trama, los personajes principales, y otros detalles relevantes que ayuden al usuario a "
            "entender de qué trata la película."
        )
        synopsis_text.setWordWrap(True)

        header_text.addWidget(title_label)
        header_text.addWidget(synopsis_label)
        header.addWidget(film_image)
        header.addLayout(header_text)

        layout.addLayout(header)
        layout.addWidget(synopsis_text)

        # Botones con estilo
        button_layout = QHBoxLayout()

        self.button_ver_despues = QPushButton("Ver Después")
        self.button_ver_despues.setProperty("class", "app_boton")
        button_layout.addWidget(self.button_ver_despues)

        self.button_calificar = QPushButton("Calificar")
        self.button_calificar.setProperty("class", "app_boton")
        button_layout.addWidget(self.button_calificar)

        self.button_marcar_vista = QPushButton("Marcar como Vista")
        self.button_marcar_vista.setProperty("class", "app_boton")
        button_layout.addWidget(self.button_marcar_vista)

        layout.addLayout(button_layout)

        self.setLayout(layout)
