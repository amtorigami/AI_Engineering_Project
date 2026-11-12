import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():

    server = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("serveur_mcp.py"))]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            outils = await session.list_tools()

            print("OUTILS DISPONIBLES :")
            for outil in outils.tools:
                print("-", outil.name, ":", outil.description)

            print("\nTEST DE RECHERCHE :")

            resultat = await session.call_tool(
                "rechercher_passeport",
                {
                    "query": "Documents nécessaires pour renouveler un passeport marocain",
                    "top_k": 5
                }
            )

            for contenu in resultat.content:
                if hasattr(contenu, "text"):
                    print(contenu.text)

asyncio.run(main())
