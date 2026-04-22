from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def experiment(systemPrompt, userPrompt, temperature=0.7):
    print("🤖 Appel à l'API Gemini...\n")
    print('\n' + '=' * 60)
    print('🧪 EXPÉRIENCE')
    print('System:', systemPrompt)
    print('User:', userPrompt)
    print('Temperature:', temperature)
    print('\n' + '=' * 60)
    
    completion = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": systemPrompt
            },
            {
                "role": "user",
                "content": userPrompt
            }
        ],
        temperature=temperature
    )
    
    print('✅ Réponse :\n')
    print(completion.choices[0].message.content)
    print(f'\n💰 Tokens: {completion.usage.total_tokens}')

async def test_experiment():
    await experiment(
        "Tu es un professeur strict et précis.",
        "Qu'est-ce que React ? Explique en détail.",
        0.1 
    )

    await experiment(
        "Tu es un poète qui explique la tech avec des métaphores.",
        "Qu'est-ce que React ? Développe ta réponse.",
        1.0
    )

    await experiment(
        "Tu es un expert Python. Réponds uniquement avec du code, sans explication.",
        "Écris une fonction qui inverse une string.",
        0.3
    )

    await experiment(
        "Tu es un traducteur professionnel.",
        "Traduis en anglais : 'Je cherche un emploi en tant que développeur IA.' Propose plusieurs variantes.",
        0.2
    )

if __name__ == "__main__":
    asyncio.run(test_experiment())