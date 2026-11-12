
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.5-flash-lite"
MODELES_SECOURS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]

EMBED_MODEL = "gemini-embedding-001"


def get_client():
    return genai.Client(
        http_options=types.HttpOptions(
            timeout=60000
        )
    )


def generer(client, contents, system=None):

    config = types.GenerateContentConfig(
        system_instruction=system
    )

    for tour in range(2):

        for nom in MODELES_SECOURS:

            try:
                print(f"Génération avec {nom}...")

                r = client.models.generate_content(
                    model=nom,
                    contents=contents,
                    config=config
                )

                return r.text

            except Exception as e:

                msg = str(e).upper()

                if any(x in msg for x in [
                    "429", "500", "503", "504",
                    "UNAVAILABLE", "DEADLINE",
                    "TIMEOUT"
                ]):
                    print(f"Erreur temporaire avec {nom}")
                    time.sleep(5)

                else:
                    raise

    return "Je ne peux pas générer une réponse pour le moment. Réessayez plus tard."
