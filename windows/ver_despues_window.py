# ver_despues_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem

class VerDespuesWindow(QWidget):
    def __init__(self, main_window=None, user_id=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.db = db
        self.setWindowTitle("Ver más tarde")

        layout = QVBoxLayout()
        title_label = QLabel("Películas guardadas para ver después")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        self.table = QTableWidget()
        self.table.setObjectName("verDespuesTable")
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Título"])
        layout.addWidget(self.table)

        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        if self.main_window:
            back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_films(self):
        films = ["Avatar", "Tenet", "The Batman"]
        self.table.setRowCount(len(films))
        for i, film in enumerate(films):
            self.table.setItem(i, 0, QTableWidgetItem(film))

    def volver(self):
        self.close()
        self.main_window.show()
