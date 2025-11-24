import os
from PyQt5.QtWidgets import  QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from windows.profile_pic_window import ProfilePicWindow

class PerfilWindow(QWidget):
    def __init__(self, main_window, logged_user, db):
        super().__init__()
        self.main_window = main_window
        self.logged_user = logged_user
        self.db = db
        self.setWindowTitle("Perfil - Pitipausa YA!")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.profile_dir = os.path.join(self.base_dir, "..", "assets", "profile")

        layout = QVBoxLayout()

        # Foto de perfil
        layout.addWidget(QLabel("Foto de perfil:"))
        self.profile_label = QLabel()
        self.profile_label.setFixedSize(100, 100)
        self.profile_label.setScaledContents(True)
        profile_pic = self.db.get_user_profile_pic(self.logged_user['id'])
        if not profile_pic:
            profile_pic = "default.png"
        self.current_profile_path = os.path.join(self.profile_dir, profile_pic)
        self.profile_label.setPixmap(QPixmap(self.current_profile_path))
        layout.addWidget(self.profile_label)

        # Botón para cambiar foto de perfil
        change_pic_btn = QPushButton("Cambiar foto de perfil")
        change_pic_btn.clicked.connect(self.open_profile_pic_window)
        layout.addWidget(change_pic_btn)

        # Username editable
        layout.addWidget(QLabel("Usuario:"))
        self.username_input = QLineEdit(self.logged_user['username'])
        layout.addWidget(self.username_input)

        # Email editable
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit(self.logged_user['email'])
        layout.addWidget(self.email_input)

        # Biografía editable
        layout.addWidget(QLabel("Biografía:"))
        self.bio_input = QTextEdit()
        # Traer bio desde la BBDD
        bio = self.db.get_user_bio(self.logged_user['id'])
        self.bio_input.setText(bio if bio else "")
        layout.addWidget(self.bio_input)

        # Botón para guardar cambios
        save_btn = QPushButton("Guardar cambios")
        save_btn.clicked.connect(self.guardar_cambios)
        layout.addWidget(save_btn)

        # Botón volver
        back_btn = QPushButton("Volver")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def open_profile_pic_window(self):
        self.pic_window = ProfilePicWindow(self, self.profile_dir, self.cambiar_foto)
        self.pic_window.show()

    def cambiar_foto(self, pic_file):
        self.current_profile_path = os.path.join(self.profile_dir, pic_file)
        self.profile_label.setPixmap(QPixmap(self.current_profile_path))
    def guardar_cambios(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        bio = self.bio_input.toPlainText().strip()
        profile_pic = os.path.basename(self.current_profile_path)

        if not username or not email:
            QMessageBox.warning(self, "Error", "Usuario y email no pueden estar vacíos")
            return

        if "@" not in email or (not email.endswith(".com") and not email.endswith(".es")):
            QMessageBox.warning(self, "Error", "El email no es válido")
            return

        # Actualizar BBDD
        self.db.update_user(self.logged_user['id'], username=username, email=email, bio=bio, profile_pic=profile_pic)
        QMessageBox.information(self, "Perfil actualizado", "Tus cambios se han guardado correctamente")

        # Actualizar diccionario logged_user
        self.logged_user['username'] = username
        self.logged_user['email'] = email
        self.logged_user['profile_picture'] = profile_pic

    def volver(self):
        self.main_window.show()
        self.close()

    