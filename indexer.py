import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")

if not API_KEY:
    raise ValueError("Clé API Pinecone manquante dans .env")

INDEX_NAME = "passeport-marocain"
DIMENSION = 768

pc = Pinecone(api_key=API_KEY)

noms_indexes = pc.list_indexes().names()

if INDEX_NAME not in noms_indexes:
    print("Création de l'index Pinecone...")

    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    print("Index créé !")
else:
    print("L'index existe déjà.")

index = pc.Index(INDEX_NAME)

with open("embeddings.json", encoding="utf-8") as f:
    embeddings = json.load(f)

print("Nombre de vecteurs à insérer :", len(embeddings))

vecteurs = []

for element in embeddings:
    vecteurs.append({
        "id": element["id"],
        "values": element["values"],
        "metadata": {
            "text": element["text"],
            "source_url": element["source_url"],
            "source_file": element["source_file"]
        }
    })

index.upsert(vectors=vecteurs)

print("Insertion terminée !")

stats = index.describe_index_stats()

print("\nVérification de l'index :")
print("Nombre de vecteurs :", stats.total_vector_count)
print("Dimension :", DIMENSION)
