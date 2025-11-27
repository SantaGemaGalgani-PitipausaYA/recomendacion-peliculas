# ficha_pelicula_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from bbdd.bbdd import BaseDeDatos
from windows.ranking_window import RankingWindow

class FichaPeliculaWindow(QWidget):
    """
    Ventana de ficha de película.
    Permite ver información, calificar, marcar como vista o agregar a ver después.
    """
    def __init__(self, pelicula_id=None, db=None, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.pelicula_id = pelicula_id

        # Datos de película
        self.title = self.db.get_movie_title(pelicula_id)
        self.overview = self.db.get_movie_overview(pelicula_id)

        self.setWindowTitle(f"Ficha de Película: {self.title}")
        layout = QVBoxLayout()

        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("titleLabel")
        layout.addWidget(self.title_label)

        self.synopsis_text = QLabel(self.overview)
        self.synopsis_text.setWordWrap(True)
        layout.addWidget(self.synopsis_text)

        # Botones de acción
        btn_ver_despues = QPushButton("Ver después")
        btn_ver_despues.setProperty("class", "app_boton")
        btn_ver_despues.clicked.connect(self.marcar_ver_despues)

        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_calificar.clicked.connect(self.calificar)

        btn_marcar_vista = QPushButton("Marcar como vista")
        btn_marcar_vista.setProperty("class", "app_boton")
        btn_marcar_vista.clicked.connect(self.marcar_vista)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(btn_ver_despues)
        buttons_layout.addWidget(btn_calificar)
        buttons_layout.addWidget(btn_marcar_vista)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def marcar_ver_despues(self):
        self.db.add_ver_despues(self.user_id, self.pelicula_id)

    def calificar(self):
        self.ranking_window = RankingWindow(main_window=None, user_id=self.user_id, db=self.db)
        self.ranking_window.load_ranking()  # Cargar datos reales
        self.ranking_window.show()

    def marcar_vista(self):
        # Guardar rating como vista
        self.db.add_rating(rating=0, id_user=self.user_id, id_movie=self.pelicula_id)
