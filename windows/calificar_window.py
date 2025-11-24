from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class CalificarWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Calificar película")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí podrías buscar y calificar una película"))

        back_btn = QPushButton("Volver")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def volver(self):
        self.close()
        self.main_window.show()