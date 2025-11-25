from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QPushButton

class ViewedFilmsWindow(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.setWindowTitle("Películas Vistas")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        page_title = QLabel("Listado de Películas Vistas")
        layout.addWidget(page_title)

        # Aquí se añadiría la lógica para mostrar las películas vistas por el usuario

        table = QTableWidget()
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Título de la Película"])
        layout.addWidget(table)

        button_volver = QPushButton("Volver")
        button_volver.clicked.connect(self.go_back)
        layout.addWidget(button_volver)

        self.setLayout(layout)

    def load_viewed_films(self, user_id):
        # Aquí se implementaría la lógica para cargar las películas vistas desde la base de datos
        pass

    def go_back(self):
        self.close()