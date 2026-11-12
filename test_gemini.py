from config import get_client

client = get_client()

candidats = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-latest",
]

for nom in candidats:
    try:
        r = client.models.generate_content(
            model=nom,
            contents="Dis bonjour en une phrase.",
        )
        print("OK  ", nom, "->", r.text.strip())
    except Exception as e:
        print("ECHEC", nom, "->", type(e).__name__)