from ai_dataset.ai_module import Recommender

# Crear recomendador
recommender = Recommender()

# Pedir recomendaciones
titulo = "Inception"  # Puedes poner cualquier título que exista en el dataset
recomendadas = recommender.recomendar(titulo, top_n=5)
print("Películas recomendadas para", titulo, ":")
for peli in recomendadas:
    print("-", peli)
