"use client";

import { useState } from "react";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);

  const askQuestion = async () => {
    if (!question) return;
    const userMessage = { role: "user", content: question };
    setMessages([...messages, userMessage]);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      console.log(data);

      const botMessage = { 
        role: "bot", 
        content: `${data.answer?.answer || "Erreur"}` 
      };

      setMessages([...messages, userMessage, botMessage]);
      setQuestion("");
    } catch (error) {
      console.error(error);
      const errorMessage = { role: "bot", content: "Erreur de connexion au backend" };
      setMessages([...messages, userMessage, errorMessage]);
      setQuestion("");
    }
  };

  return (
<div className="chat-container">
  <img src="/logo.jpg" alt="Logo Entreprise" className="logo" />
  <h1>RAG Chatbot</h1>
  <div className="chat-box">
    {messages.map((msg, i) => (
      <div key={i} className={`message ${msg.role}`}>
        {msg.content}
      </div>
    ))}
  </div>
  <div className="chat-input">
    <input
      type="text"
      value={question}
      onChange={(e) => setQuestion(e.target.value)}
      placeholder="Pose ta question..."
    />
    <button onClick={askQuestion}>Envoyer</button>
  </div>
</div>

  );
}
