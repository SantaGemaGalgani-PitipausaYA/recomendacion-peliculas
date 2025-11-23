import sqlite3

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
        	title TEXT NOT NULL
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
        	bio TEXT
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
        conn.commit()
        print("Base de datos creada")
        conn.close()
        pass


    def add_rating(self, rating: str, id_user: int, id_movie: int):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ratings (rating, id_user, id_movie) VALUES (?, ?, ?)", (rating, id_user, id_movie))
        conn.commit()
        conn.close()
        pass

    def add_movie(self, title: str):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Movies (title) VALUES (?)", (title,))
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

    def add_user(self, username: str, password: str, email: str, bio: str):
        conn = sqlite3.connect("peliculas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, password, email, bio) VALUES (?, ?, ?, ?)", (username, password, email, bio))
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
            "Tags"
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