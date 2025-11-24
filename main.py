import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from windows.splash_screen import SplashScreen
from windows.login_window import LoginWindow
from windows.main_window import MainWindow
import bbdd.bbdd as bbdd

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.logged_user= None

        # Inicializar base de datos ANTES de abrir ventanas
        self.bd = bbdd.BaseDeDatos()
        self.bd.SHOW_ALL_DEBUG()

        # Iniciar splash
        self.splash_screen = SplashScreen()
        self.splash_screen.on_finish= self.open_login
        self.splash_screen.show()
    
    def open_login(self):
        self.login_window = LoginWindow(self.bd, on_login_success=self.open_mainwindow)
        self.login_window.show()

    def open_mainwindow(self, user_info):
        self.logged_user = user_info
        self.main_window = MainWindow(logged_user=self.logged_user, db=self.bd)
        self.main_window.show()

        # Cerrar ventana de login si aún esta abierta
        if hasattr(self, "login_window"):
            self.login_window.close()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":

    controller= AppController()
    controller.run()
