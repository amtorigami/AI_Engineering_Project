import os
from dotenv import load_dotenv

from pinecone import Pinecone
from google.genai import types

from config import generer, get_client, EMBED_MODEL
from prompt import SYSTEM_PROMPT

load_dotenv()

INDEX_NAME = "passeport-marocain"
DIMENSION = 768

TOP_K = 8
SEUIL_SIMILARITE = 0.70

API_KEY = os.getenv("PINECONE_API_KEY")

if not API_KEY:
    raise ValueError("PINECONE_API_KEY manquante dans .env")

client = get_client()

pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)


def embed_query(query):
    """Transforme une question en vecteur."""

    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=DIMENSION
        )
    )

    return result.embeddings[0].values


def retrieve(query, top_k=TOP_K):
    """Recherche les passages pertinents dans Pinecone."""

    query_vector = embed_query(query)

    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    passages = []

    for match in results.matches:

        score = match.score
        metadata = match.metadata or {}

        if score < SEUIL_SIMILARITE:
            continue

        texte = metadata.get("text")
        source = metadata.get("source_url", "Source inconnue")

        if texte:
            passages.append({
                "text": texte,
                "source": source,
                "score": score
            })

    return passages


def generate_answer(question, passages):
    """Génère une réponse à partir des passages récupérés."""

    if not passages:
        return "Je ne trouve pas d'informations pertinentes dans ma base documentaire."

    contexte = "\n\n".join(
        f"PASSAGE {i}\n{p['text']}"
        for i, p in enumerate(passages, start=1)
    )

    prompt_final = f"""
CONTEXTE DOCUMENTAIRE :
{contexte}

QUESTION :
{question}

CONSIGNES :
- Réponds uniquement à partir du contexte.
- N'invente aucune information.
- Si une information manque, indique-le clairement.
- Distingue les démarches au Maroc et à l'étranger.
- Distingue la première demande du renouvellement.
- Si la localisation n'est pas précisée et change les documents requis,
  présente les deux situations ou demande une précision.
- Ne présente pas une information incertaine comme une obligation.
- Réponds de manière claire et structurée.
- Ne génère pas de section Sources.
"""

    reponse = generer(
        client,
        prompt_final,
        system=SYSTEM_PROMPT
    )

    sources = list(dict.fromkeys(
        p["source"] for p in passages
    ))

    resultat = reponse + "\n\nSources utilisées :\n"

    for source in sources:
        resultat += f"- {source}\n"

    return resultat

def question_hors_sujet(question):
    mots_passeport = [
        "passeport", "biométrique", "biometrique",
        "renouvellement", "renouveler",
        "perte", "vol", "mineur", "consulat",
        "e-timbre", "timbre"
    ]

    question = question.lower()

    return not any(mot in question for mot in mots_passeport)

def ask_rag(question):

    if question_hors_sujet(question):
        return (
            "Je ne sais pas, je suis spécialisé "
            "uniquement dans le passeport marocain."
        )

    passages = retrieve(question)
    return generate_answer(question, passages)


if __name__ == "__main__":

    question = "Quels documents faut-il fournir pour renouveler un passeport marocain au Maroc ?"

    passages = retrieve(question)

    print("\nQuestion :", question)
    print("\nNombre de passages pertinents :", len(passages))

    print("\nRéponse de l'agent RAG :")
    print(generate_answer(question, passages))
