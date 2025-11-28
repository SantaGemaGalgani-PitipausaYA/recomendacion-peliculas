# ------------------------------------------------------------
# main_window.py
# Ventana principal de la aplicación: prompt de recomendación,
# botones de navegación (Perfil, Historial) y lista de recomendaciones.
# ------------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from windows.perfil_window import PerfilWindow
from windows.historial_window import HistorialWindow
# from windows.calificar_window import CalificarWindow  # Eliminado: botón 'Calificar' quitado
from ai_dataset.ai_module import Recommender
from windows.ficha_pelicula_window import FichaPeliculaWindow
from bbdd.bbdd import BaseDeDatos

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
        # Eliminado btn_calificar: ya no existe en la UI principal
        btn_layout.addWidget(btn_perfil)
        btn_layout.addWidget(btn_historial)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        btn_perfil.clicked.connect(self.go_to_perfil)
        btn_historial.clicked.connect(self.go_to_historial)
        # btn_calificar removed

    def go_to_perfil(self):
        """
        Navegar a la ventana Perfil. Ocultamos la principal mientras el usuario
        esté en la ventana de perfil para no duplicar pantallas.
        """
        self.hide()
        self.perfil_window = PerfilWindow(self, self.logged_user, self.db)
        self.perfil_window.show()

    def go_to_historial(self):
        """
        Navegar a la ventana Historial. La ventana principal se oculta y
        la ventana historial recibe una referencia a la ventana principal
        para poder volver.
        """
        self.hide()
        self.historial_window = HistorialWindow(self, self.logged_user, self.db)
        self.historial_window.show()

    def buscar_por_prompt(self):
        """
        Llama al recomendador con el prompt del usuario y muestra botones
        con los títulos recomendados. Al pulsar un título se abre su ficha.
        """
        prompt = self.txt_recommend.text().strip()
        if not prompt:
            return

        recomendaciones = self.recommender.recomendar_por_prompt(prompt, top_n=5)

        # Limpiar layout anterior
        while self.recommend_layout.count():
            child = self.recommend_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Crear botones por cada recomendación
        for titulo in recomendaciones:
            pelicula_id = self.db.get_movie_id(titulo)
            if not pelicula_id:
                row = self.recommender.df[self.recommender.df['title'] == titulo]
                overview = row.iloc[0]['overview'] if not row.empty else ""
                self.db.add_movie(titulo, overview)
                pelicula_id = self.db.get_movie_id(titulo)

            # Guardar en historial del usuario (si procede)
            try:
                self.db.add_historial(self.logged_user['id'], pelicula_id)
            except Exception:
                pass

            btn = QPushButton(titulo)
            btn.setProperty("class", "app_boton")
            # Uso de lambda con default arg para evitar cierre sobre la variable
            btn.clicked.connect(lambda checked, t=titulo: self.abrir_ficha(t))
            self.recommend_layout.addWidget(btn)

    def abrir_ficha(self, titulo):
        """
        Abre la ventana ficha para el título seleccionado.
        La ficha recibirá db y user_id para poder realizar acciones.
        """
        pelicula_id = self.db.get_movie_id(titulo)
        if not pelicula_id:
            row = self.recommender.df[self.recommender.df['title'] == titulo]
            overview = row.iloc[0]['overview'] if not row.empty else ""
            self.db.add_movie(titulo, overview)
            pelicula_id = self.db.get_movie_id(titulo)

        # Abrir ventana ficha
        self.ficha_window = FichaPeliculaWindow(
            pelicula_id=pelicula_id,
            db=self.db,
            user_id=self.logged_user['id']
        )
        self.ficha_window.show()
