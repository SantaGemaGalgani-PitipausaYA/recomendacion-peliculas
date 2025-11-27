# calificar_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
class CalificarWindow(QWidget):
    def __init__(self, main_window, logged_user=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.logged_user = logged_user
        self.db = db
        self.setWindowTitle("Calificar película")

        layout = QVBoxLayout()
        title = QLabel("Busca y califica una película")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.search_input = QLineEdit()
        self.search_input.setProperty("class", "bigInputText")
        self.search_input.setPlaceholderText("Escribe el título o usa un prompt como en recomendaciones")
        layout.addWidget(self.search_input)

        self.btn_search = QPushButton("Buscar")
        self.btn_search.setProperty("class", "app_boton")
        layout.addWidget(self.btn_search)

        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def volver(self):
        self.close()
        self.main_window.show()
