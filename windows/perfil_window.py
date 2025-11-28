# perfil_window.py
import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from windows.profile_pic_window import ProfilePicWindow
from windows.viewed_films_window import ViewedFilmsWindow
from windows.ranking_window import RankingWindow
from windows.ver_despues_window import VerDespuesWindow
from bbdd.bbdd import BaseDeDatos

class PerfilWindow(QWidget):
    def __init__(self, main_window, logged_user, db: None):
        super().__init__()
        self.setWindowTitle("Perfil - Pitipausa YA!")
        self.main_window = main_window
        self.logged_user = logged_user
        self.db = db

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.profile_dir = os.path.join(self.base_dir, "..", "assets", "profile")

        layout = QVBoxLayout()

        foto_label = QLabel("Foto de perfil")
        foto_label.setObjectName("titleLabel")
        layout.addWidget(foto_label)

        self.profile_label = QLabel()
        self.profile_label.setFixedSize(100, 100)
        self.profile_label.setScaledContents(True)
        profile_pic = self.db.get_user_profile_pic(self.logged_user['id']) or "default.png"
        self.current_profile_path = os.path.join(self.profile_dir, profile_pic)
        self.profile_label.setPixmap(QPixmap(self.current_profile_path))
        layout.addWidget(self.profile_label)

        change_pic_btn = QPushButton("Cambiar foto de perfil")
        change_pic_btn.setProperty("class", "app_boton")
        change_pic_btn.clicked.connect(self.open_profile_pic_window)
        layout.addWidget(change_pic_btn)

        layout.addWidget(QLabel("Usuario:"))
        self.username_input = QLineEdit(self.logged_user['username'])
        self.username_input.setObjectName("inputField")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit(self.logged_user['email'])
        self.email_input.setObjectName("inputField")
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Biografía:"))
        self.bio_input = QTextEdit()
        self.bio_input.setObjectName("inputField")
        bio = self.db.get_user_bio(self.logged_user['id']) or ""
        self.bio_input.setText(bio)
        layout.addWidget(self.bio_input)

        save_btn = QPushButton("Guardar cambios")
        save_btn.setProperty("class", "app_boton")
        save_btn.clicked.connect(self.guardar_cambios)
        layout.addWidget(save_btn)

        # Accesos: Vistas, Ranking, Ver después
        links_layout = QHBoxLayout()
        btn_vistas = QPushButton("Tus pelis vistas")
        btn_vistas.setProperty("class", "app_boton")
        btn_ranking = QPushButton("Ranking de tus calificaciones")
        btn_ranking.setProperty("class", "app_boton")
        btn_ver_despues = QPushButton("Ver más tarde")
        btn_ver_despues.setProperty("class", "app_boton")
        links_layout.addWidget(btn_vistas)
        links_layout.addWidget(btn_ranking)
        links_layout.addWidget(btn_ver_despues)
        layout.addLayout(links_layout)

        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

        btn_vistas.clicked.connect(self.open_viewed)
        btn_ranking.clicked.connect(self.open_ranking)
        btn_ver_despues.clicked.connect(self.open_ver_despues)

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
        self.db.update_user(self.logged_user['id'], username=username, email=email, bio=bio, profile_pic=profile_pic)
        QMessageBox.information(self, "Perfil actualizado", "Tus cambios se han guardado correctamente")
        self.logged_user['username'] = username
        self.logged_user['email'] = email
        self.logged_user['profile_picture'] = profile_pic

    def open_viewed(self):
        self.viewed_window = ViewedFilmsWindow(self, user_id=self.logged_user['id'], db=self.db)
        self.viewed_window.show()

    def open_ranking(self):
        self.ranking_window = RankingWindow(self, user_id=self.logged_user['id'], db=self.db)
        self.ranking_window.show()

    def open_ver_despues(self):
        self.ver_despues_window = VerDespuesWindow(self, user_id=self.logged_user['id'], db=self.db)
        self.ver_despues_window.show()

    def volver(self):
        self.main_window.show()
        self.close()
