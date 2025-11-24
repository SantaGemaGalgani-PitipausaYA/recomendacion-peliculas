from PyQt5.QtWidgets import  QLabel, QPushButton, QVBoxLayout, QWidget

class HistorialWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Historial de recomendaciones - Pitipausa YA!")

        layout= QVBoxLayout()
        layout.addWidget(QLabel("Historial de recomendaciones"))
        layout.addWidget(QLabel("Aqui iria el historial de recomendaciones"))

        back_btn = QPushButton("Volver")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def volver(self):
        self.close()
        self.main_window.show()