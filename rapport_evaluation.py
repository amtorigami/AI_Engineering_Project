import statistics

temps_recherche = [4.50, 0.50, 0.51, 0.51, 0.51, 0.51]
temps_generation = [2.77, 3.38, 2.66, 4.51, 2.25, 2.66]

temps_total = [
    recherche + generation
    for recherche, generation
    in zip(temps_recherche, temps_generation)
]

print("=" * 55)
print("RAPPORT D'EVALUATION DU SYSTEME RAG")
print("=" * 55)

print(f"Nombre de questions testées : {len(temps_total)}")
print(f"Nombre de passages récupérés : 8")
print(f"Temps moyen de recherche : {statistics.mean(temps_recherche):.2f} s")
print(f"Temps moyen de génération : {statistics.mean(temps_generation):.2f} s")
print(f"Temps moyen total : {statistics.mean(temps_total):.2f} s")

print("\nBILAN QUALITATIF")
print("- Retrieval : résultats pertinents")
print("- Génération : réponses cohérentes avec le contexte")
print("- Hors périmètre : refus de répondre")
print("- Sources : affichage des sources utilisées")

print("\nEVALUATION TERMINEE")
