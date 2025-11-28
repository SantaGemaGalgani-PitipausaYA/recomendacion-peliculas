import pandas as pd
import ast
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack, csr_matrix
from deep_translator import GoogleTranslator   # pip install deep-translator
from langdetect import detect, LangDetectException  # pip install langdetect

NUMBER_WORDS_ES = {
    "cero":0,"uno":1,"una":1,"dos":2,"tres":3,"cuatro":4,"cinco":5,
    "seis":6,"siete":7,"ocho":8,"nueve":9,"diez":10
}

class Recommender:
    def __init__(self, dataset_path="ai_dataset/tmdb_5000_movies.csv"):
        # --------------------------
        # Cargar dataset
        # --------------------------
        self.df = pd.read_csv(dataset_path)
        cols = ['title','genres','release_date','overview','runtime',
                'vote_average','original_language','production_countries']
        missing = [c for c in cols if c not in self.df.columns]
        if missing:
            raise ValueError(f"Faltan columnas en el CSV: {missing}")
        self.df = self.df[cols].copy()
        # Rellenar NaN en text cols
        self.df[['genres','release_date','overview','original_language','production_countries']] = \
            self.df[['genres','release_date','overview','original_language','production_countries']].fillna("")

        # --------------------------
        # LIMPIAR y convertir runtime
        # --------------------------
        self.df['runtime'] = pd.to_numeric(self.df['runtime'], errors='coerce')
        valid_runtimes = self.df.loc[self.df['runtime'] > 0, 'runtime']
        median_runtime = valid_runtimes.median() if len(valid_runtimes) > 0 else 90.0
        self.df['runtime'] = self.df['runtime'].fillna(median_runtime)
        self.df.loc[self.df['runtime'] <= 0, 'runtime'] = median_runtime
        self.df['runtime'] = self.df['runtime'].astype(float)

        # --------------------------
        # Procesar genres / countries
        # --------------------------
        self.df['genres'] = self.df['genres'].apply(self.parse_json_list)
        self.df['countries'] = self.df['production_countries'].apply(self.parse_json_list)

        # --------------------------
        # Año como entero
        # --------------------------
        def parse_year(d):
            try:
                if isinstance(d, str) and len(d) >= 4 and d[:4].isdigit():
                    return int(d[:4])
            except:
                pass
            return 0
        self.df['year'] = self.df['release_date'].apply(parse_year)

        # --------------------------
        # Codificar géneros
        # --------------------------
        self.mlb = MultiLabelBinarizer()
        genres_array = self.mlb.fit_transform(self.df['genres'])
        genres_sparse = csr_matrix(genres_array)

        # --------------------------
        # TF-IDF de overview (usar bigramas mejora coincidencias)
        # --------------------------
        self.tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=50000)
        overview_tfidf = self.tfidf.fit_transform(self.df['overview'].astype(str))

        # --------------------------
        # Normalizar runtime
        # --------------------------
        self.scaler = StandardScaler()
        runtime_scaled = self.scaler.fit_transform(self.df[['runtime']].values)
        runtime_sparse = csr_matrix(runtime_scaled)

        # --------------------------
        # Matriz final
        # --------------------------
        self.X = hstack([overview_tfidf, genres_sparse, runtime_sparse], format='csr')
        self.cosine_matrix = cosine_similarity(self.X, self.X)  # precalculo (si dataset grande, cambiar estrategia)

        # PREPARAR textos lower para checks rápidos
        self._overview_lower = self.df['overview'].astype(str).str.lower()
        self._titles_lower = self.df['title'].astype(str).str.lower()

        # Palabras clave temáticas (inglés y español) para boost
        self.topic_keywords = {
            "space": ["space","outer space","spacecraft","spaceship","astronaut","astronauts","interstellar","cosmos","extraterrestrial","alien","martian","mars","moon","lunar","orbital","space travel","space opera"],
            "horror": ["horror","terror","scary","ghost","ghoul","monster"],
            "romance": ["romance","love","lover","relationship","couple","romantic"],
            "family": ["brother","sister","siblings","family","familia","hermano","hermana","hermanos"],
            # añade más temas si quieres
        }
        # traducir al español algunas keywords para detección en prompt en ES
        self.topic_keywords_es = {
            "space": ["espacio","espacio exterior","astronauta","nave espacial","marte","lunar","extraterrestre"],
            "romance": ["románt","amor","pareja"],
            "family": ["hermano","hermana","hermanos","familia"]
        }

    # --------------------------
    # Helpers
    # --------------------------
    def parse_json_list(self, s):
        try:
            data = ast.literal_eval(s)
            return [item.get('name', '') for item in data]
        except Exception:
            if isinstance(s, str) and "," in s:
                return [x.strip() for x in s.split(",") if x.strip()]
            return []

    def detect_prompt_language(self, text):
        try:
            return detect(text)
        except Exception:
            return "en"

    def translate_to_english(self, text):
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except Exception:
            return text

    # --------------------------
    # Parsear requerimiento de duración desde prompt
    # devuelve (min_minutes, max_minutes) donde cualquiera puede ser None
    # --------------------------
    def parse_duration_constraint(self, prompt):
        p = prompt.lower()
        # buscar "mas de X horas" (horas en número o palabra)
        m = re.search(r"más\s+de\s+(\d+)\s*horas?", p) or re.search(r"mas\s+de\s+(\d+)\s*horas?", p)
        if not m:
            # buscar "más de dos horas" con palabras
            for word, num in NUMBER_WORDS_ES.items():
                if f"más de {word} horas" in p or f"mas de {word} horas" in p:
                    m_val = num
                    break
            else:
                m_val = None
        else:
            m_val = int(m.group(1)) if m else None

        if m_val is not None:
            return (m_val * 60 + 1, None)  # más de N horas => min = N*60 +1

        # buscar "menos de X horas"
        m2 = re.search(r"menos\s+de\s+(\d+)\s*horas?", p)
        if m2:
            return (None, int(m2.group(1)) * 60 - 1)

        # buscar minutos explícitos "más de 90 minutos"
        mm = re.search(r"más\s+de\s+(\d+)\s*min", p) or re.search(r"mas\s+de\s+(\d+)\s*min", p)
        if mm:
            return (int(mm.group(1)) + 1, None)

        # buscar "dur(e)? más de X horas" con palabras inglesas "more than 2 hours"
        mm_en = re.search(r"more\s+than\s+(\d+)\s*hours?", p)
        if mm_en:
            return (int(mm_en.group(1)) * 60 + 1, None)

        return (None, None)

    # --------------------------
    # Recomendación por título (mejorada)
    # --------------------------
    def recomendar_por_titulo(self, titulo, top_n=5):
        titulo_en = self.translate_to_english(titulo).lower()
        titulo_lower = titulo.lower()

        # búsqueda exacta candidata
        exact_idx = self._titles_lower[self._titles_lower == titulo_en].index
        if len(exact_idx) == 0:
            exact_idx = self._titles_lower[self._titles_lower == titulo_lower].index

        if len(exact_idx) == 0:
            # contains fallback
            contains = self._titles_lower[self._titles_lower.str.contains(titulo_lower, na=False)].index
            if len(contains) == 0:
                return []
            idx = contains[0]
        else:
            idx = exact_idx[0]

        sim = list(enumerate(self.cosine_matrix[idx]))
        sim = sorted(sim, key=lambda x: x[1], reverse=True)[1:top_n+1]
        return [self.df.iloc[i]['title'] for i,_ in sim]

    # --------------------------
    # Recomendación por prompt libre (mejorada)
    # --------------------------
    def recomendar_por_prompt(self, prompt, top_n=5):
        # Detectar y traducir prompt
        lang = self.detect_prompt_language(prompt)
        prompt_en = self.translate_to_english(prompt)
        prompt_en_lower = prompt_en.lower()
        prompt_lower = prompt.lower()

        # Vector TF-IDF del prompt
        prompt_vec = self.tfidf.transform([prompt_en_lower])
        empty_genres = csr_matrix((1, len(self.mlb.classes_)))
        empty_runtime = csr_matrix((1,1))
        prompt_full_vec = hstack([prompt_vec, empty_genres, empty_runtime], format='csr')

        # Similitud inicial
        sim_scores = cosine_similarity(prompt_full_vec, self.X)[0]

        # Boost por idioma original
        sim_scores += (self.df['original_language'] == lang) * 0.20

        # Detectar géneros mencionados
        found_genres = [g for g in self.mlb.classes_ if g.lower() in prompt_en_lower or g.lower() in prompt_lower]
        if found_genres:
            genre_mask = self.df['genres'].apply(lambda gl: len(set(gl) & set(found_genres)) > 0)
            sim_scores += genre_mask * 0.30

        # Boost por keywords temáticas
        topics_found = set()
        for t, keys in self.topic_keywords.items():
            if any(k in prompt_en_lower for k in keys):
                topics_found.add(t)
        for t, keys in self.topic_keywords_es.items():
            if any(k in prompt_lower for k in keys):
                topics_found.add(t)
        if topics_found:
            for t in topics_found:
                keys_en = self.topic_keywords.get(t, [])
                keys_es = self.topic_keywords_es.get(t, [])
                mask = self._overview_lower.apply(lambda s: any(k in s for k in keys_en) or any(k in s for k in keys_es))
                sim_scores += mask * 0.40

        # --------------------------
        # Detectar país y año
        # --------------------------
        country = None
        for c in ["spain","france","italy","germany","usa","united kingdom","uk","japan","china","mexico","argentina"]:
            if c in prompt_lower:
                country = c
                break

        year_match = re.findall(r"(19\d{2}|20\d{2})", prompt)
        year = int(year_match[0]) if year_match else None

        # --------------------------
        # Parsear duración
        # --------------------------
        min_minutes, max_minutes = self.parse_duration_constraint(prompt_lower)

        # --------------------------
        # Filtrar dataset estrictamente antes del ranking
        # --------------------------
        filtered_idx = self.df.index.tolist()
        if country:
            filtered_idx = [i for i in filtered_idx if any(country.lower() in (c.lower() or "") for c in self.df.loc[i,'countries'])]
        if year:
            filtered_idx = [i for i in filtered_idx if self.df.loc[i,'year'] == year]

        # Fallback seguro si no hay coincidencias exactas
        if len(filtered_idx) == 0:
            if country:
                filtered_idx = [i for i in self.df.index if any(country.lower() in (c.lower() or "") for c in self.df.loc[i,'countries'])]
            if len(filtered_idx) == 0:
                filtered_idx = self.df.index.tolist()

        # --------------------------
        # Ranking según similitud
        # --------------------------
        sim_scores_filtered = [(i, sim_scores[i]) for i in filtered_idx]
        sim_scores_filtered.sort(key=lambda x: x[1], reverse=True)

        # Filtrar por duración
        def duration_ok(i):
            r = self.df.loc[i,'runtime']
            if min_minutes is not None and r < min_minutes:
                return False
            if max_minutes is not None and r > max_minutes:
                return False
            return True

        final_idx = [i for i,_ in sim_scores_filtered if duration_ok(i)]

        # Completar hasta top_n si hay pocos resultados
        if len(final_idx) < top_n:
            needed = top_n - len(final_idx)
            final_idx += [i for i,_ in sim_scores_filtered if i not in final_idx][:needed]

        return self.df.loc[final_idx[:top_n], 'title'].tolist()