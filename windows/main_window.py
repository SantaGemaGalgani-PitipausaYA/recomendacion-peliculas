# main_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from windows.perfil_window import PerfilWindow
from windows.historial_window import HistorialWindow
from windows.calificar_window import CalificarWindow
from ai_dataset.ai_module import Recommender
from windows.ficha_pelicula_window import FichaPeliculaWindow

class MainWindow(QWidget):
    def __init__(self, logged_user=None, db=None):
        super().__init__()
        self.setWindowTitle("Pitipausa YA! - Inicio")
        self.resize(600, 400)
        self.logged_user = logged_user
        self.db = db
        self.recommender = Recommender()
        

        layout = QVBoxLayout()

        self.recommend_layout = QVBoxLayout()
        layout.addLayout(self.recommend_layout)

        title = QLabel("¿Qué quieres ver hoy?")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.txt_recommend = QLineEdit()
        self.txt_recommend.setProperty("class", "bigInputText")
        self.txt_recommend.setPlaceholderText("Escribe un prompt aquí sobre la peli que quieras ver")
        self.txt_recommend.returnPressed.connect(self.buscar_por_prompt)
        layout.addWidget(self.txt_recommend)

        btn_layout = QHBoxLayout()
        btn_perfil = QPushButton("Perfil")
        btn_perfil.setProperty("class", "app_boton")
        btn_historial = QPushButton("Historial")
        btn_historial.setProperty("class", "app_boton")
        btn_calificar = QPushButton("Calificar")
        btn_calificar.setProperty("class", "app_boton")
        btn_layout.addWidget(btn_perfil)
        btn_layout.addWidget(btn_historial)
        btn_layout.addWidget(btn_calificar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        btn_perfil.clicked.connect(self.go_to_perfil)
        btn_historial.clicked.connect(self.go_to_historial)
        btn_calificar.clicked.connect(self.go_to_calificar)

    def go_to_perfil(self):
        self.hide()
        self.perfil_window = PerfilWindow(self, self.logged_user, self.db)
        self.perfil_window.show()

    def go_to_historial(self):
        self.hide()
        self.historial_window = HistorialWindow(self, self.logged_user, self.db)
        self.historial_window.show()

    def go_to_calificar(self):
        self.hide()
        self.calificar_window = CalificarWindow(self, self.logged_user, self.db)
        self.calificar_window.show()

    def buscar_por_prompt(self):
        prompt = self.txt_recommend.text().strip()
        if not prompt:
            return

        # Obtener recomendaciones
        recomendaciones = self.recommender.recomendar_por_prompt(prompt, top_n=5)

        # Limpiar layout anterior
        while self.recommend_layout.count():
            child = self.recommend_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Añadir botón por cada recomendación
        for titulo in recomendaciones:
            btn = QPushButton(titulo)
            btn.setProperty("class", "app_boton")
            btn.clicked.connect(lambda checked, t=titulo: self.abrir_ficha(t))
            self.recommend_layout.addWidget(btn)

    def abrir_ficha(self, titulo):
        # Buscar id de la película en la BBDD
        conn = self.db.conn if hasattr(self.db, 'conn') else None
        pelicula_id = None
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Movies WHERE title=?", (titulo,))
            row = cursor.fetchone()
            if row:
                pelicula_id = row[0]
            else:
                # Si no existe, la agregamos
                self.db.add_movie(titulo)
                cursor.execute("SELECT id FROM Movies WHERE title=?", (titulo,))
                row = cursor.fetchone()
                if row:
                    pelicula_id = row[0]
            conn.commit()
            cursor.close()

        # Abrir ventana ficha
        self.ficha_window = FichaPeliculaWindow(pelicula_id=pelicula_id, db=self.db, user_id=self.logged_user['id'])
        self.ficha_window.show()
