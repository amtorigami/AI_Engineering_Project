import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-embedding-001"
DIMENSION = 768

# Connexion à Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Chargement des chunks
with open("chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

print("Nombre de chunks :", len(chunks))

# Récupérer uniquement les textes
textes = [chunk["text"] for chunk in chunks]

# Générer les embeddings
response = client.models.embed_content(
    model=MODEL,
    contents=textes,
    config={
        "output_dimensionality": DIMENSION
    }
)

# Associer chaque vecteur à son chunk
resultats = []

for chunk, embedding in zip(chunks, response.embeddings):

    resultats.append({
        "id": chunk["id"],
        "values": embedding.values,
        "text": chunk["text"],
        "source_url": chunk["source_url"],
        "source_file": chunk["source_file"]
    })

# Sauvegarder les résultats
with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(
        resultats,
        f,
        ensure_ascii=False,
        indent=2
    )

print("\nEmbeddings générés avec succès !")
print("Nombre de vecteurs :", len(resultats))
print("Dimension :", len(resultats[0]["values"]))
print("Fichier créé : embeddings.json")