from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QHBoxLayout, QWidget

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        
        layout = QHBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (solo para registro)")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login_user)

        self.register_button = QPushButton("Registrar nuevo usuario")
        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(QLabel("Inicia sesión o regístrate"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        # Aquí iría la lógica para iniciar sesión del usuario
        print(f"Intentando iniciar sesión con usuario: {username}")
        # Lógica de autenticación aquí
        pass
    def register_user(self):
        username = self.user_input.text()
        email = self.email_input.text()
        password = self.pass_input.text()
        # Aquí iría la lógica para registrar un nuevo usuario
        print(f"Intentando registrar usuario: {username} con email: {email}")
        # Lógica de registro aquí
        pass
