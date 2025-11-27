import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import re

class Recommender:
    """
    Clase encargada de recomendar películas.
    Combina:
    - TF-IDF de la sinopsis (overview)
    - One-hot encoding de géneros
    - Normalización de duración
    Soporta recomendaciones por título exacto y por prompt libre.
    """

    def __init__(self, dataset_path="ai_dataset/tmdb_5000_movies.csv"):
        self.df = pd.read_csv(dataset_path)
        # Selección de columnas relevantes
        self.df = self.df[['title', 'genres', 'release_date', 'overview', 'runtime', 'vote_average', 'original_language', 'production_countries']].dropna()
        # Procesar géneros
        self.df['genres'] = self.df['genres'].apply(self.parse_genres)
        # Procesar países
        self.df['countries'] = self.df['production_countries'].apply(self.parse_countries)
        # Preparar features
        self.mlb = MultiLabelBinarizer()
        genres_encoded = self.mlb.fit_transform(self.df['genres'])
        self.tfidf = TfidfVectorizer(stop_words='english')
        overview_tfidf = self.tfidf.fit_transform(self.df['overview'])
        self.scaler = StandardScaler()
        runtime_scaled = self.scaler.fit_transform(self.df[['runtime']])
        self.X = hstack([overview_tfidf, genres_encoded, runtime_scaled])
        self.cosine_sim = cosine_similarity(self.X, self.X)
        # Diccionario de aprendizaje (prompt -> peliculas seleccionadas)
        self.learned_preferences = {}

    def parse_genres(self, genres_str):
        try:
            genres_list = ast.literal_eval(genres_str)
            return [g['name'] for g in genres_list]
        except:
            return []

    def parse_countries(self, countries_str):
        try:
            countries_list = ast.literal_eval(countries_str)
            return [c.get('name', '') for c in countries_list]
        except:
            return []

    def recomendar(self, titulo, top_n=5):
        """Recomendación basada en título exacto"""
        if titulo not in self.df['title'].values:
            return []
        idx = self.df[self.df['title'] == titulo].index[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # Excluir la misma película
        return [self.df.iloc[i[0]]['title'] for i in sim_scores]

    def recomendar_por_prompt(self, prompt, top_n=5):
        """
        Recomendación por descripción libre.
        Filtra por palabras clave, géneros o país si se mencionan explícitamente.
        Guarda preferencias para aprendizaje futuro.
        """
        # Detectar país o idioma en prompt
        prompt_lower = prompt.lower()
        country_filter = None
        if "español" in prompt_lower or "españa" in prompt_lower:
            country_filter = "Spain"
        if "francia" in prompt_lower:
            country_filter = "France"

        # Transformar prompt a vector TF-IDF
        prompt_vec = self.tfidf.transform([prompt])
        overview_tfidf = self.tfidf.transform(self.df['overview'])
        sim_scores = cosine_similarity(prompt_vec, overview_tfidf)[0]

        # Aplicar filtro de país si hay
        if country_filter:
            indices = self.df[self.df['countries'].apply(lambda x: country_filter in x)].index
            filtered_scores = [(i, sim_scores[i]) for i in indices]
            filtered_scores.sort(key=lambda x: x[1], reverse=True)
            top_indices = [i[0] for i in filtered_scores[:top_n]]
        else:
            top_indices = sim_scores.argsort()[::-1][:top_n]

        # Aprendizaje simple: guardar prompt y resultados
        self.learned_preferences[prompt] = [self.df.iloc[i]['title'] for i in top_indices]

        return [self.df.iloc[i]['title'] for i in top_indices]
