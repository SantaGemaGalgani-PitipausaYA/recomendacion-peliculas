# ------------------------------------------------------------
# viewed_films_window.py
# Ventana que muestra las películas que el usuario ya ha visto.
# ------------------------------------------------------------

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem
)
from bbdd.bbdd import BaseDeDatos

class ViewedFilmsWindow(QWidget):
    def __init__(self, main_window=None, user_id=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.db: BaseDeDatos = db
        self.setWindowTitle("Películas Vistas")
        self.setGeometry(100, 100, 640, 360)

        layout = QVBoxLayout()
        page_title = QLabel("Listado de Películas Vistas")
        page_title.setObjectName("titleLabel")
        layout.addWidget(page_title)

        # Tabla con dos columnas: título y fecha
        self.table = QTableWidget()
        self.table.setObjectName("filmsTable")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Título", "Fecha"])
        layout.addWidget(self.table)

        button_volver = QPushButton("Volver")
        button_volver.setProperty("class", "app_boton")
        button_volver.clicked.connect(self.go_back)
        layout.addWidget(button_volver)

        self.setLayout(layout)

        # Cargar contenido al inicializar la ventana
        self.load_viewed_films()

    def load_viewed_films(self):
        """
        Recupera el historial de películas vistas del usuario desde la BD.
        Se espera que self.db.get_historial_usuario(user_id) devuelva
        una lista de tuplas (title, fecha) o similar.
        """
        try:
            pelis = self.db.get_historial_usuario(self.user_id) or []
        except Exception:
            # Si falla la consulta, mostramos vacío en vez de romper
            pelis = []

        self.table.setRowCount(len(pelis))
        for i, item in enumerate(pelis):
            # Item puede ser (title, fecha) o sólo title; manejamos ambos casos.
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                title, fecha = item[0], item[1]
            else:
                title, fecha = (str(item), "")
            self.table.setItem(i, 0, QTableWidgetItem(str(title)))
            self.table.setItem(i, 1, QTableWidgetItem(str(fecha)))

    def go_back(self):
        """
        Cierra esta ventana y vuelve a la ventana principal si está presente.
        """
        self.close()
        if self.main_window:
            try:
                self.main_window.show()
            except Exception:
                pass
