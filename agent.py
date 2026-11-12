
import os
from pathlib import Path
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

serveur = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=str(BASE_DIR / "rag_venv/bin/python"),
            args=[str(BASE_DIR / "serveur_mcp.py")],
            env={
                **os.environ,
                "PYTHONPATH": str(BASE_DIR)
            }
        )
    )
)

root_agent = Agent(
    name="demarchesmaroc_agent",
    model="gemini-3.5-flash-lite",
    instruction="""
Tu es un assistant spécialisé uniquement dans le passeport marocain.

RÈGLES :

1. Pour toute question concernant le passeport marocain,
   utilise obligatoirement l'outil rechercher_passeport.

2. Réponds uniquement à partir des informations récupérées.

3. N'invente jamais de documents, tarifs ou délais.

4. Si les informations sont insuffisantes, indique-le clairement.

5. Pour les questions hors sujet (CIN, visa, mariage,
   carte grise...), réponds exactement :
   Je ne sais pas, je suis spécialisé uniquement
   dans le passeport marocain.

6. Réponds en français, clairement et poliment.
""",
    tools=[serveur]
)
