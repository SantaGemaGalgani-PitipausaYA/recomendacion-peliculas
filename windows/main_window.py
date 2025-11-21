from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout
import sys
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pitipausa YA! - Recomendador 3M,5")
        
        layout = QVBoxLayout()

        see_label = QLabel("¿Que quieres ver hoy?")
        layout.addWidget(see_label)
        txt_recommend = QLineEdit()
        txt_recommend.setPlaceholderText("Escribe un prompt aquí sobra la peli que quieras ver")
        layout.addWidget(txt_recommend)
        recomendation_layout = QHBoxLayout()
        btn_1 = QPushButton("Placeholder 1")
        btn_2 = QPushButton("Placeholder 2")
        btn_3 = QPushButton("Placeholder 3")
        self.setLayout(layout)
        recomendation_layout.addWidget(btn_1)
        recomendation_layout.addWidget(btn_2)
        recomendation_layout.addWidget(btn_3)
        layout.addLayout(recomendation_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())