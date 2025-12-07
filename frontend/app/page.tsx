"use client"; // ← Ajoute cette ligne en tout début du fichier

import { useState } from 'react';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);

  const askQuestion = async () => {
    if (!question) return;
    const userMessage = { role: 'user', content: question };
    setMessages([...messages, userMessage]);

    const res = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    const botMessage = { role: 'bot', content: data.answer || 'Erreur' };
    setMessages([...messages, userMessage, botMessage]);
    setQuestion('');
  };

  return (
    <div className="chat-container">
      <h1>RAG Chatbot</h1>
      <div>
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Pose ta question..."
      />
      <button onClick={askQuestion}>Envoyer</button>
    </div>
  );
}
