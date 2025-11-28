# ------------------------------------------------------------
# historial_window.py
# Ventana que muestra el historial de recomendaciones del usuario.
# Permite abrir la ficha de una película con doble clic.
# ------------------------------------------------------------

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from windows.ficha_pelicula_window import FichaPeliculaWindow

class HistorialWindow(QWidget):
    def __init__(self, main_window, logged_user=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.logged_user = logged_user
        self.db = db
        self.setWindowTitle("Historial de recomendaciones")
        self.setBaseSize(600, 400)

        layout = QVBoxLayout()
        title = QLabel("Historial de recomendaciones")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Creamos la tabla antes de cargar datos (evita errores)
        self.table = QTableWidget()
        self.table.setObjectName("historialTable")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Película", "Fecha"])

        # 🔑 Ajuste clave: columnas ocupan todo el ancho
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

        # Conectar doble clic en la tabla para abrir ficha
        self.table.itemDoubleClicked.connect(self.open_ficha)

        # Cargar historial tras crear la tabla
        self.load_historial()

    def load_historial(self):
        """
        Carga el historial del usuario desde la base de datos y lo muestra en la tabla.
        Se espera que self.db.get_historial_usuario(user_id) devuelva lista de (titulo, fecha).
        """
        try:
            items = self.db.get_historial_usuario(self.logged_user['id']) or []
        except Exception as e:
            print(f"Error al cargar historial: {e}")
            items = []

        self.table.clearContents()
        self.table.setRowCount(len(items))
        for i, (film, date) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(str(film)))
            self.table.setItem(i, 1, QTableWidgetItem(str(date)))

    def open_ficha(self, item):
        """
        Abre la ficha de la película seleccionada (fila del item).
        """
        row = item.row()
        titulo_item = self.table.item(row, 0)
        if not titulo_item:
            return
        titulo = titulo_item.text()
        pelicula_id = None
        try:
            pelicula_id = self.db.get_movie_id(titulo)
        except Exception:
            pelicula_id = None

        if not pelicula_id:
            overview = ""
            try:
                self.db.add_movie(titulo, overview)
                pelicula_id = self.db.get_movie_id(titulo)
            except Exception:
                pelicula_id = None

        if pelicula_id:
            self.ficha_window = FichaPeliculaWindow(
                pelicula_id=pelicula_id,
                db=self.db,
                user_id=self.logged_user['id']
            )
            self.ficha_window.show()

    def volver(self):
        """
        Vuelve a la ventana principal.
        """
        self.close()
        if self.main_window:
            try:
                self.main_window.show()
            except Exception:
                pass
