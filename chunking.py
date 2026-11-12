import json
from pathlib import Path

TAILLE_CHUNK = 500
OVERLAP = 80

DOSSIER_CORPUS = Path("corpus")
FICHIER_SORTIE = Path("chunks.json")


def decouper_texte(texte):
    """Découpe le texte en chunks en respectant les paragraphes."""

    paragraphes = [
        p.strip()
        for p in texte.splitlines()
        if p.strip()
    ]

    chunks = []
    chunk_actuel = []
    nombre_mots = 0

    for paragraphe in paragraphes:

        mots = paragraphe.split()
        taille = len(mots)

        if taille > TAILLE_CHUNK:
            if chunk_actuel:
                chunks.append(" ".join(chunk_actuel))
                chunk_actuel = []
                nombre_mots = 0

            for debut in range(0, taille, TAILLE_CHUNK - OVERLAP):
                morceau = " ".join(
                    mots[debut:debut + TAILLE_CHUNK]
                )
                if morceau:
                    chunks.append(morceau)

            continue

        if nombre_mots + taille > TAILLE_CHUNK:

            chunks.append(" ".join(chunk_actuel))

            # On conserve les derniers mots pour l'overlap.
            anciens_mots = " ".join(chunk_actuel).split()
            chunk_actuel = anciens_mots[-OVERLAP:]
            nombre_mots = len(chunk_actuel)

        chunk_actuel.extend(mots)
        nombre_mots += taille

    if chunk_actuel:
        chunks.append(" ".join(chunk_actuel))

    return chunks


def creer_chunks():

    tous_les_chunks = []

    fichiers = sorted(DOSSIER_CORPUS.glob("page_*.txt"))

    for fichier in fichiers:

        lignes = fichier.read_text(
            encoding="utf-8"
        ).splitlines()

        if not lignes:
            continue

        url = lignes[0].strip()
        texte = "\n".join(lignes[1:])

        morceaux = decouper_texte(texte)

        for numero, morceau in enumerate(morceaux, start=1):

            tous_les_chunks.append({
                "id": f"{fichier.name}_chunk_{numero:03d}",
                "text": morceau,
                "source_url": url,
                "source_file": fichier.name
            })

        print(f"{fichier.name} : {len(morceaux)} chunks")

    FICHIER_SORTIE.write_text(
        json.dumps(
            tous_les_chunks,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("\nDécoupage terminé.")
    print("Nombre total de chunks :", len(tous_les_chunks))
    print("Fichier créé :", FICHIER_SORTIE)


if __name__ == "__main__":
    creer_chunks()
