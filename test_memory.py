# test_memory.py
import requests

API_URL = "http://localhost:3001/api/chat"

def chat_with_memory():
    conversation = []
    
    print("🤖 Chatbot avec mémoire (tape 'quit' pour sortir)\n")
    
    while True:
        user_input = input("💬 Toi: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("👋 Au revoir !")
            break
        
        # Ajoute le message de l'utilisateur à l'historique
        conversation.append({
            "role": "user",
            "content": user_input
        })
        
        # Envoie l'historique complet au serveur
        response = requests.post(API_URL, json={
            "messages": conversation
        })
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data['response']
            tokens = data['tokens']
            
            print(f"🤖 IA: {ai_response}")
            print(f"💰 Tokens: {tokens}\n")
            
            # Ajoute la réponse de l'IA à l'historique
            conversation.append({
                "role": "assistant",
                "content": ai_response
            })
        else:
            print(f"❌ Erreur: {response.json()}")

if __name__ == "__main__":
    # Vérifie que le serveur tourne
    try:
        requests.get("http://localhost:3001/")
        chat_with_memory()
    except:
        print("❌ Le serveur n'est pas lancé !")
        print("Lance d'abord: python server.py")