from rag import retrieve

QUESTIONS = [
    "Quels documents faut-il fournir pour renouveler un passeport marocain au Maroc ?",
    "Quels documents faut-il fournir pour une première demande de passeport pour un enfant de moins de 12 ans ?",
    "Comment renouveler un passeport marocain depuis l'étranger ?"
]

for i, question in enumerate(QUESTIONS, 1):

    print("\n" + "=" * 65)
    print(f"QUESTION {i}")
    print("=" * 65)

    print(question)

    passages = retrieve(question)

    print(f"\nNombre de passages récupérés : {len(passages)}")

    for j, passage in enumerate(passages, 1):
        print(f"\nPassage {j}")
        print("Score :", round(passage["score"], 3))
        print("Source :", passage["source"])
