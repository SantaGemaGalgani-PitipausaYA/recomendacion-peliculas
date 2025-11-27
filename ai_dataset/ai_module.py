import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack

class Recommender:
    def __init__(self, dataset_path="ai_dataset/tmdb_5000_movies.csv"):
        """
        Inicializa el recomendador:
        - Carga el dataset TMDB 5000
        - Selecciona solo columnas necesarias
        - Procesa géneros, sinopsis y duración
        - Calcula similitud de coseno para recomendaciones
        """
        # 1️⃣ Cargar dataset
        self.df = pd.read_csv(dataset_path)

        # 2️⃣ Seleccionar solo columnas que necesitamos
        self.df = self.df[['title', 'genres', 'release_date', 'overview', 'runtime', 'vote_average']].dropna()

        # 3️⃣ Convertir géneros de string JSON a lista
        self.df['genres'] = self.df['genres'].apply(self.parse_genres)

        # 4️⃣ Preparar features
        # Géneros → One-hot encoding
        self.mlb = MultiLabelBinarizer()
        genres_encoded = self.mlb.fit_transform(self.df['genres'])

        # Sinopsis → TF-IDF
        self.tfidf = TfidfVectorizer(stop_words='english')
        overview_tfidf = self.tfidf.fit_transform(self.df['overview'])

        # Duración → Normalización
        self.scaler = StandardScaler()
        runtime_scaled = self.scaler.fit_transform(self.df[['runtime']])

        # 5️⃣ Combinar todas las features en una matriz
        self.X = hstack([overview_tfidf, genres_encoded, runtime_scaled])

        # 6️⃣ Calcular similitud de coseno
        self.cosine_sim = cosine_similarity(self.X, self.X)

    def parse_genres(self, genres_str):
        """
        Convierte la columna 'genres' de string JSON a lista de nombres
        Ejemplo: '[{"id": 28, "name": "Action"}]' → ['Action']
        """
        try:
            genres_list = ast.literal_eval(genres_str)
            return [g['name'] for g in genres_list]
        except:
            return []

    def recomendar(self, titulo, top_n=5):
        """
        Devuelve películas similares a un título exacto
        """
        if titulo not in self.df['title'].values:
            return []
        idx = self.df[self.df['title'] == titulo].index[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # Excluir la misma película
        return [self.df.iloc[i[0]]['title'] for i in sim_scores]

    def recomendar_por_prompt(self, prompt, top_n=5):
        """
        Devuelve películas recomendadas a partir de un prompt libre
        Ejemplo de prompt: "Quiero ver una película de ciencia ficción con robots y viajes en el tiempo"
        """
        # Transformar prompt a vector TF-IDF
        prompt_vec = self.tfidf.transform([prompt])

        # Solo usamos TF-IDF de overview para medir similitud con el prompt
        overview_tfidf = self.tfidf.transform(self.df['overview'])
        sim_scores = cosine_similarity(prompt_vec, overview_tfidf)[0]

        # Ordenar y coger top_n
        top_indices = sim_scores.argsort()[::-1][:top_n]
        return [self.df.iloc[i]['title'] for i in top_indices]
