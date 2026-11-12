from rag import retrieve, generate_answer

QUESTIONS = [
    {
        "question": "Quels documents faut-il fournir pour renouveler un passeport marocain au Maroc ?",
        "attendu": "Formulaire, e-timbre, CNIE valide, photo et ancien passeport."
    },
    {
        "question": "Quels documents faut-il fournir pour une première demande de passeport pour un enfant de moins de 12 ans ?",
        "attendu": "Acte de naissance ou livret de famille, photo, formulaire, justificatifs des parents et e-timbre."
    },
    {
        "question": "Comment renouveler un passeport marocain depuis l'étranger ?",
        "attendu": "Dépôt au consulat, immatriculation consulaire, formulaire, CNIE ou récépissé, ancien passeport et photos."
    },
    {
        "question": "Que faire en cas de perte ou de vol de son passeport marocain ?",
        "attendu": "Déclarer immédiatement la perte ou le vol auprès des autorités compétentes."
    },
    {
        "question": "Est-ce qu'un enfant de moins de 12 ans doit présenter une CNIE pour obtenir un passeport marocain ?",
        "attendu": "Non. Un acte de naissance ou un livret de famille peut être présenté."
    },
    {
        "question": "Quels documents faut-il fournir pour obtenir un visa Schengen ?",
        "attendu": "Question hors périmètre. Le système doit reconnaître qu'il ne dispose pas des informations."
    }
]

for i, test in enumerate(QUESTIONS, 1):

    question = test["question"]

    print("\n" + "=" * 70)
    print(f"ÉVALUATION {i}/{len(QUESTIONS)}")
    print("=" * 70)

    passages = retrieve(question)

    reponse = generate_answer(question, passages)

    print("\nQUESTION :", question)
    print("\nRÉPONSE ATTENDUE :", test["attendu"])
    print("\nRÉPONSE DU RAG :", reponse)

    print("\nNOMBRE DE PASSAGES :", len(passages))
    print("SOURCES :", list(set(p["source"] for p in passages)))

print("\nÉVALUATION TERMINÉE.")
