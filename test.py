from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def test_api():
    print("🤖 Appel à l'API OpenAI...\n")
    
    completion = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant qui explique l'IA de façon simple."
            },
            {
                "role": "user",
                "content": "Explique-moi en 3 phrases ce qu'est un LLM."
            }
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    print("✅ Réponse de l'IA :\n")
    print(completion.choices[0].message.content)
    print(f"\n💰 Tokens utilisés : {completion.usage.total_tokens}")


if __name__ == "__main__":
    test_api()