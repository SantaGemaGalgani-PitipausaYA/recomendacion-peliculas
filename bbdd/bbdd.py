import sqlite3
from datetime import datetime

class BaseDeDatos():
    def __init__(self):
        self.crear_bbdd()
        pass

    def crear_bbdd(self):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Genres
        (
        	label TEXT PRIMARY KEY,
        	description TEXT NOT NULL
        );""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies
        (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	title TEXT NOT NULL,
        	overview TEXT NOT NULL
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_genre
        (
        	id_movie INTEGER,
        	label_genre TEXT,
        	PRIMARY KEY (id_movie, label_genre)
        	FOREIGN KEY (id_movie) REFERENCES Movies(id),
        	FOREIGN KEY (label_genre) REFERENCES Genres(label)
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users
        (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	username TEXT NOT NULL,
        	password TEXT NOT NULL,
        	email TEXT NOT NULL,
        	bio TEXT,
            profile_pic TEXT DEFAULT 'default.svg'
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ratings
        (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	rating REAL NOT NULL,
        	id_user INTEGER NOT NULL,
        	id_movie INTEGER NOT NULL,
        	FOREIGN KEY (id_user) REFERENCES Users(id),
        	FOREIGN KEY (id_movie) REFERENCES Movies(id)
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tags
        (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	tags TEXT NOT NULL,
        	id_movie INTEGER NOT NULL,
        	id_user INTEGER NOT NULL,
        	FOREIGN KEY (id_movie) REFERENCES Movies(id),
        	FOREIGN KEY (id_user) REFERENCES User(id)
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Historial
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            id_movie INTEGER,
            fecha TEXT,
            FOREIGN KEY (id_user) REFERENCES Users(id),
            FOREIGN KEY (id_movie) REFERENCES Movies(id)
        );""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS VerDespues
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            id_movie INTEGER,
            FOREIGN KEY (id_user) REFERENCES Users(id),
            FOREIGN KEY (id_movie) REFERENCES Movies(id)
        );""")

        conn.commit()
        print("Base de datos creada")
        conn.close()
        pass


    def add_rating(self, rating: float, id_user: int, id_movie: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ratings (rating, id_user, id_movie) VALUES (?, ?, ?)", (rating, id_user, id_movie))
        conn.commit()
        conn.close()
        pass

    def add_movie(self, title: str, overview: str = ""):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Movies (title, overview) VALUES (?, ?)", (title, overview))
        conn.commit()
        conn.close()
        pass

    def add_genre(self, label: str, description: str):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Genres VALUES (?, ?)", (label, description))
        conn.commit()
        conn.close()
        pass

    def add_genre_to_movie(self, id_movie: int, label: str):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movie_genre VALUES (?, ?)", (id_movie, label))
        conn.commit()
        conn.close()
        pass

    def add_user(self, username: str, password: str, email: str, bio: str, profile_pic: str = "default.svg"):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, password, email, bio, profile_pic) VALUES (?, ?, ?, ?, ?)", (username, password, email, bio, profile_pic))
        conn.commit()
        conn.close()
        pass

    def add_tag(self, tag: str, id_movie: int, id_user: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tags (tags, id_movie, id_user) VALUES (?, ?, ?)", (tag, id_movie, id_user))
        conn.commit()
        conn.close()
        pass

    def get_user_password(self, username: str):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def get_user_bio(self, id_user):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bio FROM Users WHERE id=?", (id_user,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else ""
    
    def get_user_profile_pic(self, user_id):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT profile_pic FROM Users WHERE id=?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def update_user(self, user_id, username=None, email=None, bio=None, profile_pic=None):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()

        fields = []
        values = []

        if username is not None:
            fields.append("username=?")
            values.append(username)
        if email is not None:
            fields.append("email=?")
            values.append(email)
        if bio is not None:
            fields.append("bio=?")
            values.append(bio)
        if profile_pic is not None:
            fields.append("profile_pic=?")
            values.append(profile_pic)

        values.append(user_id)
        sql = f"UPDATE Users SET {', '.join(fields)} WHERE id=?"
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    def get_user_by_username(self, username):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM Users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "username": row[1], "email": row[2]}
        return None
    
    def get_movie_id(self, title: str):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Movies WHERE title=?", (title,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def add_historial(self, id_user: int, id_movie: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Historial (id_user, id_movie, fecha) VALUES (?, ?, ?)", (id_user, id_movie, fecha))
        conn.commit()
        conn.close()
        
    def get_historial_usuario(self, user_id):
        """
        Devuelve una lista de tuplas (titulo_pelicula, fecha) del historial de un usuario.
        """
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.title, h.fecha
            FROM Historial h
            JOIN Movies m ON m.id = h.id_movie
            WHERE h.id_user=?
            ORDER BY h.fecha DESC
        """, (user_id,))
        items = cursor.fetchall()
        conn.close()
        return items
        

    def add_ver_despues(self, id_user: int, id_movie: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO VerDespues (id_user, id_movie) VALUES (?, ?)", (id_user, id_movie))
        conn.commit()
        conn.close()

    def get_movie_overview(self, id_movie: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT overview FROM Movies WHERE id=?", (id_movie,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "Sinopsis no disponible"
    
    def get_movie_title(self, id_movie: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM Movies WHERE id=?", (id_movie,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "Título desconocido"
    
# Devuelve una lista de tuplas (titulo_pelicula, rating) de un usuario
    def get_user_ranking(self, id_user):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.title, r.rating
            FROM Ratings r
            JOIN Movies m ON r.id_movie = m.id
            WHERE r.id_user=?
            ORDER BY r.rating DESC
        """, (id_user,))
        items = cursor.fetchall()
        conn.close()
        return items
   
    def load_ranking(self):
        """
        Carga las calificaciones del usuario en la tabla.
        Usa directamente el método get_user_ranking de la BD.
        """

        films = []
        if self.db and self.user_id:
            try:
                films = self.db.get_user_ranking(self.user_id)
            except Exception as e:
                # Si hay error en la consulta, usamos datos de ejemplo
                print(f"Error al cargar ranking: {e}")
                films = [
                    ("Matrix", 5),
                    ("Inception", 4),
                    ("Interstellar", 3)
                ]
        else:
            # Si no hay BD o user_id, mostramos datos de ejemplo
            films = [
                ("Matrix", 5),
                ("Inception", 4),
                ("Interstellar", 3)
            ]

        # Poblar la tabla
        self.table.clearContents()
        self.table.setRowCount(len(films))

        for row, (film, score) in enumerate(films):
            self.table.setItem(row, 0, QTableWidgetItem(str(film)))
            self.table.setItem(row, 1, QTableWidgetItem(str(score)))

        # Opcional: ajustar cabecera
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)

    # Devuelve la lista de títulos que el usuario ha marcado como "Ver después"
    def get_ver_despues_usuario(self, id_user):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.title
            FROM VerDespues v
            JOIN Movies m ON v.id_movie = m.id
            WHERE v.id_user=?
        """, (id_user,))
        items = [row[0] for row in cursor.fetchall()]
        conn.close()
        return items

    def SHOW_ALL_DEBUG(self):
        """
        DEBUG: Shows all the data in the database, for debug purposes only. Made by GPT.
        """
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        print("\n==================== DEBUG: DATABASE CONTENTS ====================\n")

        tables = [
            "Genres",
            "Movies",
            "movie_genre",
            "Users",
            "Ratings",
            "Tags",
            "Historial",
            "VerDespues"
        ]

        for table in tables:
            print(f"-------------------- TABLE: {table} --------------------")

            try:
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()

                if not rows:
                    print("(empty)\n")
                    continue

                # Print column names
                col_names = [description[0] for description in cursor.description]
                print(col_names)

                # Print rows
                for row in rows:
                    print(row)

                print()  # spacing

            except Exception as e:
                print(f"Error reading table {table}: {e}\n")

        print("================== END OF DATABASE DUMP ==================\n")
        conn.close()