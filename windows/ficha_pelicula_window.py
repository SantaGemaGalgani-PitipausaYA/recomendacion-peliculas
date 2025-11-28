# ------------------------------------------------------------
# ficha_pelicula_window.py
# Ventana que muestra la información detallada de una película.
# Permite marcar para ver después, marcar como vista y calificar.
# ------------------------------------------------------------

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QMessageBox, QDialog, QComboBox
)
from bbdd.bbdd import BaseDeDatos
from windows.ranking_window import RankingWindow

class FichaPeliculaWindow(QWidget):
    """
    Ventana con la ficha de una película.
    Muestra el título, la sinopsis y varios botones de acción.
    """

    def __init__(self, pelicula_id=None, db=None, user_id=None):
        super().__init__()

        self.db = db
        self.user_id = user_id
        self.pelicula_id = pelicula_id

        # ------------------------------
        # Datos de la película
        # ------------------------------
        self.title = self.db.get_movie_title(pelicula_id)
        self.overview = self.db.get_movie_overview(pelicula_id)

        self.setWindowTitle(f"Ficha de Película: {self.title}")
        layout = QVBoxLayout()

        # ------------------------------
        # TÍTULO
        # ------------------------------
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("titleLabel")
        layout.addWidget(self.title_label)

        # ------------------------------
        # SINOPSIS
        # ------------------------------
        self.synopsis_text = QLabel(self.overview)
        self.synopsis_text.setWordWrap(True)
        layout.addWidget(self.synopsis_text)

        # ------------------------------
        # BOTONES DE ACCIÓN
        # ------------------------------
        btn_ver_despues = QPushButton("Ver después")
        btn_ver_despues.setProperty("class", "app_boton")
        btn_ver_despues.clicked.connect(self.marcar_ver_despues)

        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_calificar.clicked.connect(self.calificar)

        btn_marcar_vista = QPushButton("Marcar como vista")
        btn_marcar_vista.setProperty("class", "app_boton")
        btn_marcar_vista.clicked.connect(self.marcar_vista)

        # Layout para los botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(btn_ver_despues)
        buttons_layout.addWidget(btn_calificar)
        buttons_layout.addWidget(btn_marcar_vista)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    # ------------------------------------------------------------
    # FUNCIÓN: Marcar película para ver después
    # ------------------------------------------------------------
    def marcar_ver_despues(self):
        """
        Añade la película a la lista 'ver después' en la base de datos
        y muestra una confirmación al usuario.
        """
        self.db.add_ver_despues(self.user_id, self.pelicula_id)

        QMessageBox.information(
            self,
            "Añadido",
            "La película se ha añadido a tu lista de 'Ver después'."
        )

    # ------------------------------------------------------------
    # FUNCIÓN: Abrir ventana para votar 1-5
    # ------------------------------------------------------------
    def calificar(self):
        """
        Muestra un diálogo modal donde el usuario elige la puntuación (1-5).
        Tras confirmar se guarda la votación y se abre la ventana de ranking.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Calificar película")
        layout = QVBoxLayout(dialog)

        label = QLabel("Selecciona una puntuación (1-5):")
        layout.addWidget(label)

        # Selector de puntuación
        combo = QComboBox()
        combo.addItems(["1", "2", "3", "4", "5"])
        layout.addWidget(combo)

        # Botón confirmar
        btn_confirmar = QPushButton("Confirmar")
        layout.addWidget(btn_confirmar)

        # Al confirmar, guardamos la calificación
        def confirmar():
            puntuacion = int(combo.currentText())
            self.db.add_rating(
                rating=puntuacion,
                id_user=self.user_id,
                id_movie=self.pelicula_id
            )
            dialog.accept()

            # Abrimos ranking pasando main_window=self para que el botón
            # 'Volver' en RankingWindow regrese a esta ficha.
            self.ranking_window = RankingWindow(
                main_window=self,
                user_id=self.user_id,
                db=self.db
            )
            self.ranking_window.show()

        btn_confirmar.clicked.connect(confirmar)
        dialog.exec_()

    # ------------------------------------------------------------
    # FUNCIÓN: Marcar película como vista
    # ------------------------------------------------------------
    def marcar_vista(self):
        """
        Marca la película como vista. En la BD se registra como rating=0.
        Muestra confirmación al usuario.
        """
        self.db.add_rating(
            rating=0,
            id_user=self.user_id,
            id_movie=self.pelicula_id
        )

        QMessageBox.information(
            self,
            "Película marcada",
            "La película se ha marcado como vista."
        )
