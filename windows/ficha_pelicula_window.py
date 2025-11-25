from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

class FichaPeliculaWindow(QWidget):
    def __init__(self, pelicula_id=None):
        super().__init__()
        self.setWindowTitle("Ficha de Película : " + str(pelicula_id)) #Hay que cambiarlo por el título real
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        header = QHBoxLayout()
        header_text = QVBoxLayout()
        film_image = QLabel("Imagen de la Película")
        pixmap_film = QPixmap("path/to/film_image.jpg").scaled(100, 150)
        title_label = QLabel(str(pelicula_id))  # Cambiar por el título real
        synopsis_label = QLabel("Sinopsis de la Película")
        synopsis_text = QLabel("Aquí va la sinopsis detallada de la película. Esta sección contendrá una descripción completa de la trama, los personajes principales, y otros detalles relevantes que ayuden al usuario a entender de qué trata la película.")
        synopsis_text.setWordWrap(True)

        header_text.addWidget(title_label)
        header_text.addWidget(synopsis_label)
        header.addWidget(film_image)
        header.addLayout(header_text)

        layout.addLayout(header)

        button_layout = QHBoxLayout()

        # Aquí se pueden añadir botones como "Ver Trailer", "Agregar a Favoritos", etc.

        self.button_ver_despues = QPushButton("Ver Después")
        button_layout.addWidget(self.button_ver_despues)
        self.button_calificar = QPushButton("Calificar")
        button_layout.addWidget(self.button_calificar)
        self.button_marcar_vista = QPushButton("Marcar como Vista")
        button_layout.addWidget(self.button_marcar_vista)

        layout.addLayout(button_layout)

        self.setLayout(layout)





        