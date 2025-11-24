from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout
from windows.perfil_window import PerfilWindow
from windows.historial_window import HistorialWindow
from windows.calificar_window import CalificarWindow

class MainWindow(QWidget):
    def __init__(self, logged_user= None, db = None):
        super().__init__()
        self.logged_user = logged_user
        self.db = db
        self.setWindowTitle("Pitipausa YA! - Recomendador 3M,5")
        
        layout = QVBoxLayout()

        see_label = QLabel("¿Que quieres ver hoy?")
        layout.addWidget(see_label)

        txt_recommend = QLineEdit()
        txt_recommend.setPlaceholderText("Escribe un prompt aquí sobra la peli que quieras ver")
        layout.addWidget(txt_recommend)

        recomendation_layout = QHBoxLayout()
        btn_perfil = QPushButton("Perfil")
        btn_historial = QPushButton("Historial")
        btn_calificar = QPushButton("Calificar")
        recomendation_layout.addWidget(btn_perfil)
        recomendation_layout.addWidget(btn_historial)
        recomendation_layout.addWidget(btn_calificar)

        layout.addLayout(recomendation_layout)

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
        self.historial_window = HistorialWindow(self)
        self.historial_window.show()

    def go_to_calificar(self):
        self.hide()
        self.calificar_window = CalificarWindow(self)
        self.calificar_window.show()

# quitar comillas para ejecutar

'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

'''