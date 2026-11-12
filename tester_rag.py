
from rag import retrieve, generate_answer



QUESTIONS = [

    "Quels documents faut-il fournir pour renouveler un passeport marocain au Maroc ?",

    "Quels documents faut-il fournir pour une première demande de passeport pour un enfant de moins de 12 ans ?",

    "Comment renouveler un passeport marocain depuis l'étranger ?",

    "Que faire en cas de perte ou de vol de son passeport marocain ?",

    "Est-ce qu'un enfant de moins de 12 ans doit présenter une CNIE pour obtenir un passeport marocain ?",

    "Quels documents faut-il fournir pour obtenir un visa Schengen ?",

    "Est-ce que je peux renouveler mon passeport entièrement en ligne ?",

    "Combien de temps est valable le passeport marocain pour un enfant de moins de 3 ans ?",

    "Un mineur âgé de 12 à 18 ans doit-il obligatoirement fournir une CNIE ?",

    "Quel est le prix d'un passeport marocain ?",

    "Comment renouveler un passeport marocain depuis la France sans CNIE valide ?"

]

for i, question in enumerate(QUESTIONS, start=1):

    print("\n" + "=" * 75)
    print(f"TEST {i}/{len(QUESTIONS)}")
    print("=" * 75)

    print("\nQUESTION :", question)

    try:

        passages = retrieve(question)

        print("\nPASSAGES RETROUVÉS :", len(passages))

        for j, passage in enumerate(passages, start=1):

            print(
                f"\nPassage {j} | "
                f"Score : {passage['score']:.3f}"
            )

            print("Source :", passage["source"])

        print("\nRÉPONSE DU RAG :\n")

        reponse = generate_answer(question, passages)

        print(reponse)

    except Exception as e:

        print("\nERREUR PENDANT CE TEST :")
        print(e)

        print("\nPassage au test suivant...")


print("\n" + "=" * 75)
print("TOUS LES TESTS SONT TERMINÉS.")
print("=" * 75)
