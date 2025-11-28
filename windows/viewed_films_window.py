# viewed_films_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem
from bbdd.bbdd import BaseDeDatos;

class ViewedFilmsWindow(QWidget):
    def __init__(self, main_window=None, user_id=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.db: BaseDeDatos = db
        self.setWindowTitle("Películas Vistas")
        self.setGeometry(100, 100, 480, 320)

        layout = QVBoxLayout()
        page_title = QLabel("Listado de Películas Vistas")
        page_title.setObjectName("titleLabel")
        layout.addWidget(page_title)

        self.table = QTableWidget()
        self.table.setObjectName("filmsTable")
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Título"])
        layout.addWidget(self.table)

        button_volver = QPushButton("Volver")
        button_volver.setProperty("class", "app_boton")
        if self.main_window:
            button_volver.clicked.connect(self.go_back)
        layout.addWidget(button_volver)

        self.setLayout(layout)

        self.load_viewed_films()

    def load_viewed_films(self):
        pelis = self.db.get_historial_usuario(self.user_id)
        self.table.setRowCount(len(pelis))
        for i, (title, fecha) in enumerate(pelis):
            self.table.setItem(i, 0, QTableWidgetItem(str(title)))
            self.table.setItem(i, 1, QTableWidgetItem(str(fecha)))

    def go_back(self):
        self.close()
        self.main_window.show()
