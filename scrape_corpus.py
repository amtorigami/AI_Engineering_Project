
import os
import time
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URLS = [
    "https://www.demarchesmaroc.com/renouvellement-passeport-marocain/",
    "https://www.demarchesmaroc.com/passeport-biometrique/",
    "https://www.demarchesmaroc.com/obtenir-carte-identite-et-passeport-depuis-etranger/",
    "https://www.demarchesmaroc.com/?p=724",
    "https://www.demarchesmaroc.com/creer-compte-prendre-rendez-vous-rdv-consulat-maroc/",
]

FIN = [
    "ceci peut aussi vous intéresser",
    "articles similaires",
    "articles recommandés",
]

BALISES_INUTILES = [
    "script", "style", "nav", "header",
    "footer", "aside", "form", "iframe"
]

PUBLICITES = [
    "nos conseillers vous répondent",
    "nos conseillers sont là pour vous aider",
    "gagnez du temps et de la sérénité",
    "contactez-nous dès maintenant",
    "cet article vous a-t-il été utile",
    "2€/min",
]

os.makedirs("corpus", exist_ok=True)


def nettoyer_texte(texte):
    """Nettoie les espaces inutiles dans un texte."""
    return " ".join(texte.split())


def extraire_section(soup, titre_section):
    """Extrait une section et ses sous-sections."""

    titre = None

    for h in soup.find_all(["h2", "h3"]):
        texte = nettoyer_texte(h.get_text(" ", strip=True))

        if titre_section.casefold() in texte.casefold():
            titre = h
            break

    if titre is None:
        print(f"Section introuvable : {titre_section}")
        return []

    niveau = int(titre.name[1])

    lignes = [nettoyer_texte(titre.get_text(" ", strip=True))]

    for element in titre.find_all_next(["h2", "h3", "p", "li"]):

        if element.name in ["h2", "h3"]:
            niveau_suivant = int(element.name[1])

            if niveau_suivant <= niveau:
                break

        texte = nettoyer_texte(element.get_text(" ", strip=True))

        texte = re.sub(r"https?://\S+", " ", texte).strip()
        texte = nettoyer_texte(texte)

        if texte and texte.casefold() != lignes[-1].casefold():
            lignes.append(texte)

    return lignes


def extraire_contenu(soup):
    """Extrait les titres, paragraphes et listes de la page."""

    titre = soup.find("h1")

    if titre is None:
        return None

    lignes = []
    lignes.append(nettoyer_texte(titre.get_text(" ", strip=True)))

    for element in titre.find_all_next(["h2", "h3", "p", "li"]):

        texte = nettoyer_texte(element.get_text(" ", strip=True))

        if not texte:
            continue

        texte_minuscule = texte.casefold()

        if any(fin in texte_minuscule for fin in FIN):
            break

        if any(pub in texte_minuscule for pub in PUBLICITES):
            continue

        if texte.casefold() != lignes[-1].casefold():
            lignes.append(texte)

    return lignes


def scraper_page(url, numero):

    print(f"\nRécupération de la page {numero}...")

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for balise in soup(BALISES_INUTILES):
            balise.decompose()

        if numero == 3:
            lignes = extraire_section(soup, "Le passeport biométrique")

        elif numero == 4:
            lignes = extraire_section(soup, "Attestation de déclaration de perte / de vol")

        else:
            lignes = extraire_contenu(soup)

        if not lignes or len(lignes) < 2:
            print("Contenu insuffisant :", url)
            return

        texte_complet = "\n".join(lignes)

        if len(texte_complet.split()) < 50:
            print("Attention : contenu très court :", url)
            return

        nom = f"corpus/page_{numero}.txt"

        with open(nom, "w", encoding="utf-8") as fichier:
            fichier.write(url + "\n")
            fichier.write(texte_complet)

        nombre_mots = len(texte_complet.split())

        print(f"OK : {nom}")
        print(f"Titre : {lignes[0]}")
        print(f"Lignes : {len(lignes)}")
        print(f"Mots : {nombre_mots}")

    except requests.RequestException as erreur:
        print("Erreur de téléchargement :", url)
        print(erreur)


for numero, url in enumerate(URLS, start=1):

    scraper_page(url, numero)

    if numero < len(URLS):
        time.sleep(2)

print("\nScraping terminé.")
