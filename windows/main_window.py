# main_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from windows.perfil_window import PerfilWindow
from windows.historial_window import HistorialWindow
from windows.calificar_window import CalificarWindow

class MainWindow(QWidget):
    def __init__(self, logged_user=None, db=None):
        super().__init__()
        self.setWindowTitle("Pitipausa YA! - Inicio")
        self.resize(600, 400)
        self.logged_user = logged_user
        self.db = db

        layout = QVBoxLayout()

        title = QLabel("¿Qué quieres ver hoy?")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.txt_recommend = QLineEdit()
        self.txt_recommend.setProperty("class", "bigInputText")
        self.txt_recommend.setPlaceholderText("Escribe un prompt aquí sobre la peli que quieras ver")
        layout.addWidget(self.txt_recommend)

        btn_layout = QHBoxLayout()
        btn_perfil = QPushButton("Perfil")
        btn_perfil.setProperty("class", "app_boton")
        btn_historial = QPushButton("Historial")
        btn_historial.setProperty("class", "app_boton")
        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_layout.addWidget(btn_perfil)
        btn_layout.addWidget(btn_historial)
        btn_layout.addWidget(btn_calificar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        btn_perfil.clicked.connect(self.go_to_perfil)
        btn_historial.clicked.connect(self.go_to_historial)
        btn_calificar.clicked.connect(self.go_to_calificar)

    def go_to_perfil(self):
        self.hide()
        self.perfil_window = PerfilWindow(self, self.logged_user, self.db)
        self.perfil_window.show()

    def go_to_historial(self):
        self.hide()
        self.historial_window = HistorialWindow(self, self.logged_user, self.db)
        self.historial_window.show()

    def go_to_calificar(self):
        self.hide()
        self.calificar_window = CalificarWindow(self, self.logged_user, self.db)
        self.calificar_window.show()
