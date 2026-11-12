import time
from config import get_client, generer
from prompt import SYSTEM_PROMPT

client = get_client()

questions = [
    "Quels documents faut-il pour renouveler mon passeport ?",
    "Que faire si j'ai perdu mon passeport ?",
    "Quel est le tarif du passeport biométrique ?",
    "Comment obtenir une carte grise ?",
]

for q in questions:
    print("Q :", q)
    print("R :", generer(client, q, SYSTEM_PROMPT))
    print("-" * 40)
    time.sleep(13)