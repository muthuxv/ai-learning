# chat_simple.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def chat(user_message):
    """Envoie un message à l'IA et retourne la réponse"""
    completion = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": "Tu es un assistant utile et amical."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    return completion.choices[0].message.content

def main():
    print("🤖 Chatbot démarré ! (tape 'quit' pour sortir)\n")
    
    while True:
        # Demande à l'utilisateur
        user_input = input("💬 Toi: ")
        
        # Si l'utilisateur veut quitter
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Au revoir !")
            break
        
        # Si l'input est vide
        if not user_input.strip():
            print("⚠️  Tu n'as rien écrit ! Essaye encore.\n")
            continue
        
        # Appel à l'IA
        print("\n🤖 IA: [réfléchit...]")
        response = chat(user_input)
        print(f"🤖 IA: {response}\n")

if __name__ == "__main__":
    main()