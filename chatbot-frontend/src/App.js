// src/App.js
import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [totalTokens, setTotalTokens] = useState(0);
  const messagesEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Ajoute le message de l'utilisateur
    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      // Appelle ton API Flask
      const response = await axios.post('http://localhost:3001/api/chat', {
        messages: newMessages
      });

      setTotalTokens(totalTokens + response.data.tokens);

      // Ajoute la réponse de l'IA
      setMessages([...newMessages, {
        role: 'assistant',
        content: response.data.response
      }]);
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const clearConversation = () => {
    if (window.confirm('Effacer toute la conversation ?')) {
      setMessages([]);
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
      <div className="chat-header">
        <h1>🤖 Mon Chatbot IA</h1>
        <p>Propulsé par Gemini • 💰 {totalTokens} tokens utilisés</p>
        <button className="clear-btn" onClick={clearConversation}>
          🗑️ Nouvelle conversation
        </button>
      </div>

        <div className="messages-container">
          {messages.length === 0 && (
            <div className="empty-state">
              <p>👋 Salut ! Pose-moi une question pour commencer.</p>
            </div>
          )}

          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-avatar">
                {msg.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <div className="message-text">{msg.content}</div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Écris ton message ici..."
            rows="3"
            disabled={loading}
          />
          <button 
            onClick={sendMessage} 
            disabled={loading || !input.trim()}
          >
            {loading ? '⏳' : '🚀'} Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;