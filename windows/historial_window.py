# historial_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class HistorialWindow(QWidget):
    def __init__(self, main_window, logged_user=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.logged_user = logged_user
        self.db = db
        self.setWindowTitle("Historial de recomendaciones - Pitipausa YA!")

        layout = QVBoxLayout()
        title = QLabel("Historial de recomendaciones")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setObjectName("historialTable")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Película", "Fecha"])
        layout.addWidget(self.table)

        buttons_layout = QVBoxLayout()
        btn_ver_despues = QPushButton("Ver después")
        btn_ver_despues.setProperty("class", "app_boton")
        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_marcar_vista = QPushButton("Marcar como vista")
        btn_marcar_vista.setProperty("class", "app_boton")
        buttons_layout.addWidget(btn_ver_despues)
        buttons_layout.addWidget(btn_calificar)
        buttons_layout.addWidget(btn_marcar_vista)
        layout.addLayout(buttons_layout)

        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

        # Ejemplo de selección que llevaría a la ficha
        # self.table.itemDoubleClicked.connect(self.open_ficha)

    def load_historial(self):
        items = [("Interstellar", "2025-11-01"), ("Arrival", "2025-11-15")]
        self.table.setRowCount(len(items))
        for i, (film, date) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(film))
            self.table.setItem(i, 1, QTableWidgetItem(date))

    def open_ficha(self, item):
        # obtener pelicula_id desde BBDD y abrir ficha
        pass

    def volver(self):
        self.close()
        self.main_window.show()
