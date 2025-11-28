# ------------------------------------------------------------
# ver_despues_window.py
# Ventana que muestra las películas guardadas por el usuario para ver después.
# ------------------------------------------------------------

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QHeaderView
)

class VerDespuesWindow(QWidget):
    def __init__(self, main_window=None, user_id=None, db=None):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.db = db
        self.setWindowTitle("Ver más tarde")

        layout = QVBoxLayout()
        title_label = QLabel("Películas guardadas para ver después")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # Tabla: una columna (título). Si deseas más columnas (p.ej. fecha),
        # incrementa setColumnCount y cabeceras.
        self.table = QTableWidget()
        self.table.setObjectName("verDespuesTable")
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Título"])

        # 🔑 Ajuste clave: que la columna se estire al máximo
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Botón volver: siempre conectado a una función robusta
        back_btn = QPushButton("Volver")
        back_btn.setProperty("class", "app_boton")
        back_btn.clicked.connect(self.volver)
        layout.addWidget(back_btn)

        self.setLayout(layout)
        self.load_films()

    def load_films(self):
        """
        Carga desde la base de datos las películas en 'ver después' del usuario.
        Si la BD no implementa el método, se usan ejemplos.
        """
        try:
            items = self.db.get_ver_despues_usuario(self.user_id) or []
        except Exception as e:
            print(f"Error al cargar ver después: {e}")
            items = []

        self.table.clearContents()
        self.table.setRowCount(len(items))
        for i, film in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(str(film)))

    def volver(self):
        """
        Cierra esta ventana y muestra la ventana principal (si existe).
        Si main_window es None, simplemente se cierra.
        """
        self.close()
        if self.main_window:
            try:
                self.main_window.show()
            except Exception:
                pass
