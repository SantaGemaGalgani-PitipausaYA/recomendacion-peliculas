from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QHeaderView
)

class ViewedFilmsWindow(QWidget):
    def __init__(self, main_window=None, user_id=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.db = db
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

        # 🔑 Ajuste clave: que las columnas se estiren al máximo
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_volver = QPushButton("Volver")
        button_volver.setProperty("class", "app_boton")
        button_volver.clicked.connect(self.go_back)
        layout.addWidget(button_volver)

        self.setLayout(layout)

        # Cargar contenido al inicializar la ventana
        self.load_viewed_films()

    def load_viewed_films(self):
        try:
            pelis = self.db.get_historial_usuario(self.user_id) or []
        except Exception as e:
            print(f"Error al cargar historial: {e}")
            pelis = []

        self.table.setRowCount(len(pelis))
        for i, (title, fecha) in enumerate(pelis):
            self.table.setItem(i, 0, QTableWidgetItem(str(title)))
            self.table.setItem(i, 1, QTableWidgetItem(str(fecha)))

    def go_back(self):
        self.close()
        if self.main_window:
            try:
                self.main_window.show()
            except Exception:
                pass
