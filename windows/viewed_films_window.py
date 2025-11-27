from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QPushButton

class ViewedFilmsWindow(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.setWindowTitle("Películas Vistas")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Título con estilo
        page_title = QLabel("Listado de Películas Vistas")
        page_title.setObjectName("titleLabel")
        layout.addWidget(page_title)

        # Tabla de películas vistas
        table = QTableWidget()
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Título de la Película"])
        layout.addWidget(table)

        # Botón volver con estilo
        button_volver = QPushButton("Volver")
        button_volver.setProperty("class", "app_boton")
        button_volver.clicked.connect(self.go_back)
        layout.addWidget(button_volver)

        self.setLayout(layout)

    def load_viewed_films(self, user_id):
        # Aquí se implementaría la lógica para cargar las películas vistas desde la base de datos
        pass

    def go_back(self):
        self.close()
