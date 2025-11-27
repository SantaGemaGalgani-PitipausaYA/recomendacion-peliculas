# historial_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from windows.ficha_pelicula_window import FichaPeliculaWindow

class HistorialWindow(QWidget):
    def __init__(self, main_window, logged_user=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.logged_user = logged_user
        self.db = db
        self.setWindowTitle("Historial de recomendaciones - Pitipausa YA!")

        layout = QVBoxLayout()
        title = QLabel("Historial de recomendaciones")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.load_historial()

        self.table = QTableWidget()
        self.table.setObjectName("historialTable")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Película", "Fecha"])
        layout.addWidget(self.table)

        buttons_layout = QVBoxLayout()
        btn_ver_despues = QPushButton("Ver después")
        btn_ver_despues.setProperty("class", "app_boton")
        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_marcar_vista = QPushButton("Marcar como vista")
        btn_marcar_vista.setProperty("class", "app_boton")
        buttons_layout.addWidget(btn_ver_despues)
        buttons_layout.addWidget(btn_calificar)
        buttons_layout.addWidget(btn_marcar_vista)
        layout.addLayout(buttons_layout)

        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)

        #HACER DOBLECLICK SOBRE FILA PARA ABRIR LA FICHA
        self.table.itemDoubleClicked.connect(self.open_ficha)

    def load_historial(self):
        """
        Carga el historial del usuario desde la base de datos y lo muestra en la tabla.
        """
        items = self.db.get_historial_usuario(self.logged_user['id'])
        self.table.setRowCount(len(items))
        for i, (film, date) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(film))
            self.table.setItem(i, 1, QTableWidgetItem(date))

    def open_ficha(self, item):
        """
        Abre la ficha de la película seleccionada.
        Detecta la fila seleccionada, obtiene el título y llama a la ventana FichaPeliculaWindow.
        """
        row = item.row()
        titulo = self.table.item(row, 0).text()
        pelicula_id = self.db.get_movie_id(titulo)

        # Abrir ficha de película
        self.ficha_window = FichaPeliculaWindow(pelicula_id=pelicula_id, db=self.db, user_id=self.logged_user['id'])
        self.ficha_window.show()

    def volver(self):
        self.close()
        self.main_window.show()
