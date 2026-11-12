import time
from rag import retrieve, generate_answer

QUESTIONS = [
    "Quels documents faut-il fournir pour renouveler un passeport marocain au Maroc ?",
    "Quels documents faut-il fournir pour une première demande de passeport pour un enfant de moins de 12 ans ?",
    "Comment renouveler un passeport marocain depuis l'étranger ?",
    "Que faire en cas de perte ou de vol de son passeport marocain ?",
    "Est-ce qu'un enfant de moins de 12 ans doit présenter une CNIE pour obtenir un passeport marocain ?",
    "Quels documents faut-il fournir pour obtenir un visa Schengen ?"
]

temps_recherche = []
temps_generation = []

print("\nÉVALUATION DES PERFORMANCES DU RAG\n")

for i, question in enumerate(QUESTIONS, start=1):

    print("=" * 65)
    print(f"TEST {i}/{len(QUESTIONS)}")
    print("QUESTION :", question)

    debut = time.time()
    passages = retrieve(question)
    fin = time.time()

    duree_recherche = fin - debut

    debut = time.time()
    reponse = generate_answer(question, passages)
    fin = time.time()

    duree_generation = fin - debut

    temps_recherche.append(duree_recherche)
    temps_generation.append(duree_generation)

    print("\nPassages récupérés :", len(passages))
    print(f"Temps de recherche : {duree_recherche:.2f} secondes")
    print(f"Temps de génération : {duree_generation:.2f} secondes")
    print(f"Temps total : {duree_recherche + duree_generation:.2f} secondes")


print("\n" + "=" * 65)
print("RÉSULTATS GLOBAUX")
print("=" * 65)

print(f"Temps moyen de recherche : {sum(temps_recherche)/len(temps_recherche):.2f} s")
print(f"Temps moyen de génération : {sum(temps_generation)/len(temps_generation):.2f} s")
print(f"Temps moyen total : {(sum(temps_recherche)+sum(temps_generation))/len(QUESTIONS):.2f} s")

print("\nÉVALUATION TERMINÉE.")
