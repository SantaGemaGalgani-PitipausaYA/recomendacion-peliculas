# ------------------------------------------------------------
# ranking_window.py
# Muestra el ranking de las calificaciones del usuario.
# Mejoras aplicadas:
#   ✓ Botón "Volver" funcional en cualquier contexto.
#   ✓ Comentarios extensos y claros.
#   ✓ Preparado para cargar datos reales desde la BD.
# ------------------------------------------------------------

from bbdd.bbdd import BaseDeDatos

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget,
    QPushButton, QTableWidgetItem
)

class RankingWindow(QWidget):
    def __init__(self, main_window=None, user_id=None, db=None):
        super().__init__()

        self.main_window = main_window  # Puede ser la ventana principal o la ficha de película
        self.user_id = user_id
        self.db:BaseDeDatos = db

        self.setWindowTitle("Ranking de tus calificaciones")

        # ------------------------------------------------------------
        # LAYOUT PRINCIPAL
        # ------------------------------------------------------------
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ------------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------------
        title_label = QLabel("Ranking de tus calificaciones")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # ------------------------------------------------------------
        # TABLA DE RANKING
        # ------------------------------------------------------------
        self.table = QTableWidget()
        self.table.setObjectName("rankingTable")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Película", "Puntuación"])
        layout.addWidget(self.table)

        # ------------------------------------------------------------
        # BOTÓN VOLVER
        # Comportamiento mejorado:
        #   - Si viene de la ventana principal → vuelve a ella
        #   - Si viene de ficha de película → vuelve a ella
        #   - Si no hay ventana previa → solo cierra
        # ------------------------------------------------------------
        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)
        self.load_ranking()

    # ------------------------------------------------------------
    # FUNCIÓN: Cargar datos del ranking
    # ------------------------------------------------------------
    def load_ranking(self):
        """
        Carga las calificaciones del usuario.
        Si la base de datos tiene un método para obtenerlas,
        se usa; de lo contrario, se muestran unas de ejemplo.
        """

        films = self.db.get_user_ranking(self.user_id)

        self.table.setRowCount(len(films))

        # Rellenar la tabla
        for row, (film, score) in enumerate(films):
            self.table.setItem(row, 0, QTableWidgetItem(film))
            self.table.setItem(row, 1, QTableWidgetItem(str(score)))

    # ------------------------------------------------------------
    # FUNCIÓN: Volver a la ventana anterior
    # ------------------------------------------------------------
    def volver(self):
        """
        Lógica inteligente para volver:
        - Si main_window es una ventana válida → mostrarla
        - Si no hay ventana previa → solo cerrarse
        """

        self.close()

        if self.main_window:
            try:
                self.main_window.show()
            except:
                # Si ocurre algún error, no hacemos nada más.
                pass
