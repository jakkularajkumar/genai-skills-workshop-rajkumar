import React, { useState } from "react";

const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://testing-485101432623.europe-west1.run.app", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: input }),
      });
      console.log("gere");
      
      const data = await res.json();
      console.log(data,"data");
      
      const botReply = { role: "bot", text: data.data || "No response." };
      setMessages((prev) => [...prev, botReply]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error sending message." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h2 style={{ textAlign: "center" }}>ADS Chatbot </h2>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          padding: 10,
          height: '80vh',
          overflowY: "auto",
          background: "#f5f5f5",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
              marginBottom: 8,
            }}
          >
            <div
              style={{
                padding: "1px 14px",
                borderRadius: 16,
                justifyContent: 'flex-start',
                background: msg.role === "user" ? "#d1e7dd" : "#fff",
                maxWidth: "70%",
                boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              }}
            >
              <p style={{textAlign: 'left'}}>{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ fontStyle: "italic", color: "#666" }}>Bot is gathering info...</div>
        )}
      </div>

      <div style={{ marginTop: 10, display: "flex" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={{
            flexGrow: 1,
            padding: 10,
            borderRadius: 8,
            border: "1px solid #ccc",
            fontSize: 14,
          }}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          style={{
            marginLeft: 10,
            padding: "10px 16px",
            borderRadius: 8,
            background: "#007bff",
            color: "#fff",
            border: "none",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatApp;
