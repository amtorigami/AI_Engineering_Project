from mcp.server.fastmcp import FastMCP
from rag import retrieve

mcp = FastMCP("passeport-marocain")

@mcp.tool()
def rechercher_passeport(query: str, top_k: int = 5) -> str:
    """
    Recherche les informations pertinentes dans les pages
    demarchesmaroc.com indexées sur le passeport marocain.
    Utiliser cet outil pour les documents, procédures,
    renouvellements, mineurs, pertes et vols.
    """
    passages = retrieve(query, top_k)

    if not passages:
        return "Aucune information pertinente trouvée."

    resultat = []

    for p in passages:
        resultat.append(
            f"Source : {p['source']}\n"
            f"Score : {p['score']}\n"
            f"Contenu : {p['text']}"
        )

    return "\n\n".join(resultat)


if __name__ == "__main__":
    mcp.run()
