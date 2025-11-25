from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import bbdd.bbdd as bbdd

class LoginWindow(QWidget):
    def __init__(self, db=None, on_login_success=None):
        super().__init__()
        self.setWindowTitle("Login - Pitipausa YA!")
        self.resize(800, 400)

        self.db = db
        self.on_login_success = on_login_success

        # Layout principal dividido en dos mitades
        main_layout = QHBoxLayout(self)

        # --- Mitad izquierda: Imagen cuadrada ---
        image_label = QLabel()
        pixmap = QPixmap("logo.png")  # pon tu imagen aquí
        pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setObjectName("posterImage")

        # --- Mitad derecha: Formulario vertical ---
        form_layout = QVBoxLayout()

        self.info_label = QLabel("Inicia sesión o regístrate")
        self.info_label.setObjectName("titleLabel")
        form_layout.addWidget(self.info_label)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setObjectName("inputField")
        form_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setObjectName("inputField")
        form_layout.addWidget(self.pass_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (solo para registro)")
        self.email_input.setObjectName("inputField")
        self.email_input.hide()
        form_layout.addWidget(self.email_input)

        # Botones en horizontal abajo
        btn_layout = QHBoxLayout()
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setProperty("class", "app_boton")

        self.register_button = QPushButton("Registrar nuevo usuario")
        self.register_button.setProperty("class", "app_boton")

        btn_layout.addWidget(self.login_button)
        btn_layout.addWidget(self.register_button)

        form_layout.addStretch()
        form_layout.addLayout(btn_layout)

        # Añadir las dos mitades al layout principal
        main_layout.addWidget(image_label, 1)
        main_layout.addLayout(form_layout, 1)

        # Conexiones
        self.login_button.clicked.connect(self.login_user)
        self.register_button.clicked.connect(self.show_register)

    def login_user(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Debes introducir usuario y contraseña")
            return

        stored_password = self.db.get_user_password(username)
        if stored_password is None:
            QMessageBox.warning(self, "Error", "Usuario no registrado")
        elif stored_password != password:
            QMessageBox.warning(self, "Error", "Contraseña incorrecta")
        else:
            conn = bbdd.sqlite3.connect("peliculas.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, email FROM Users WHERE username=?", (username,))
            row = cursor.fetchone()
            conn.close()
            id_user = row[0]
            email = row[1]

            user_info = self.db.get_user_by_username(username)
            if self.on_login_success:
                self.on_login_success(user_info)
            self.close()

    def show_register(self):
        self.email_input.show()
        self.login_button.setText("Registrar y entrar")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.register_user)
        self.register_button.setDisabled(True)

    def register_user(self):
        username = self.user_input.text().strip()
        email = self.email_input.text().strip()
        password = self.pass_input.text().strip()

        if not username or not password or not email:
            QMessageBox.warning(self, "Error", "Debes completar todos los campos")
            return

        if "@" not in email or (not email.endswith(".com") and not email.endswith(".es")):
            QMessageBox.warning(self, "Error", "El email no es válido")
            return

        if self.db.get_user_password(username) is not None:
            QMessageBox.warning(self, "Error", "El usuario ya existe")
            return

        self.db.add_user(username=username, password=password, email=email, bio="", profile_pic="default.svg")
        QMessageBox.information(self, "Registro exitoso", "Usuario registrado correctamente")

        conn = bbdd.sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM Users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        id_user = row[0]
        email = row[1]

        user_info = self.db.get_user_by_username(username)
        if self.on_login_success:
            self.on_login_success(user_info)
        self.close()

        self.email_input.hide()
        self.login_button.setText("Iniciar sesión")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.login_user)
        self.register_button.setDisabled(False)

'''if __name__ == "__main__":
    app = QApplication(sys.argv)


    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())'''
