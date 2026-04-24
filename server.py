# server_with_memory.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

request_count = 0

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🤖 API Chatbot avec MÉMOIRE !",
        "status": "running",
        "version": "2.0 - With Memory",
        "requests_served": request_count
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    global request_count
    request_count += 1
    
    try:
        data = request.json
        print(f"\n📨 Requête #{request_count} reçue: {data}")
        # Récupère l'historique complet de la conversation
        messages = data.get('messages', [])
        temperature = data.get('temperature', 0.7)

        if not messages or len(messages) == 0:
            return jsonify({"error": "Messages manquants"}), 400
        

        print(f"📊 Historique de la conversation ({len(messages)} messages):")
        
        # Ajoute le system prompt au début si pas présent
        if messages[0].get('role') != 'system':
            messages.insert(0, {
                "role": "system",
                "content": "Tu es un assistant utile et amical. Tu te souviens de toute la conversation."
            })
        
        print(f"📨 Requête #{request_count} avec {len(messages)} messages dans l'historique")
        
        # Envoie TOUT l'historique à l'API
        completion = client.chat.completions.create(
            model="gemini-3-flash-preview",
            messages=messages,
            temperature=temperature
        )
        
        response_text = completion.choices[0].message.content
        
        print(f"✅ Réponse envoyée ({completion.usage.total_tokens} tokens)")
        
        return jsonify({
            "response": response_text,
            "tokens": completion.usage.total_tokens,
            "temperature": temperature,
            "request_id": request_count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🧠 SERVEUR API CHATBOT AVEC MÉMOIRE")
    print("=" * 60)
    print("📍 URL: http://localhost:3001")
    print("💬 Chat endpoint: POST http://localhost:3001/api/chat")
    print("📝 Format: {\"messages\": [{\"role\": \"user\", \"content\": \"...\"}, ...]}")
    print("=" * 60)
    app.run(debug=True, port=3001)