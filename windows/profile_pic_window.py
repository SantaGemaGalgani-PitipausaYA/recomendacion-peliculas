# profile_pic_window.py
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class ProfilePicWindow(QWidget):
    def __init__(self, parent, profile_dir, callback):
        super().__init__()
        self.setWindowTitle("Seleccionar foto de perfil")
        self.callback = callback
        self.profile_dir = profile_dir
        self.parent = parent

        grid = QGridLayout()
        row, col = 0, 0

        for pic_file in os.listdir(self.profile_dir):
            if not pic_file.lower().endswith((".png", ".jpg", ".jpeg", ".svg")):
                continue
            btn = QPushButton()
            btn.setProperty("class", "profile_pic_button")
            icon = QIcon(os.path.join(self.profile_dir, pic_file))
            btn.setIcon(icon)
            btn.setIconSize(QSize(80, 80))
            btn.setFixedSize(100, 100)
            btn.clicked.connect(lambda checked, p=pic_file: self.select_pic(p))
            grid.addWidget(btn, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

        self.setLayout(grid)

    def select_pic(self, pic_file):
        self.callback(pic_file)
        self.close()
