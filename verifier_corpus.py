
from pathlib import Path
from collections import Counter
import re

fichiers = sorted(Path("corpus").glob("page_*.txt"))

total_mots = 0
lignes_globales = Counter()

for fichier in fichiers:
    lignes = fichier.read_text(encoding="utf-8").splitlines()

    url = lignes[0]
    texte = "\n".join(lignes[1:])

    mots = re.findall(r"\b[\wÀ-ÿ'-]+\b", texte)
    total_mots += len(mots)

    print("\n" + "=" * 55)
    print(fichier.name)
    print("URL :", url)
    print("Nombre de mots :", len(mots))
    print("Début du contenu :")

    for ligne in lignes[1:5]:
        print("-", ligne[:150])

    for ligne in lignes[1:]:
        propre = " ".join(ligne.split()).casefold()
        if propre:
            lignes_globales[propre] += 1

doublons = {
    ligne: n for ligne, n in lignes_globales.items()
    if n > 1
}

print("\n" + "=" * 55)
print("BILAN DU CORPUS")
print("Nombre de fichiers :", len(fichiers))
print("Nombre total de mots :", total_mots)
print("Lignes répétées :", len(doublons))

for ligne, n in list(doublons.items())[:10]:
    print(f"[{n} fois] {ligne[:150]}")
