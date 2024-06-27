import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Conversation.css";

const Conversation = () => {
  const [senderId, setSenderId] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // Ensure this hook is used within the functional component

  const handleChange = (event) => {
    setSenderId(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/messaging/conversation_users_history/${senderId}/`
      ); // Changed receiverId to senderId
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error("Error fetching conversation:", error);
    }
    setLoading(false);
  };

  const handleUsernameClick = (userId) => {
    console.log("Navigating to App");
    navigate("/chat", { state: { senderId: senderId, id: userId } });
  };

  return (
    <div className="conversation-container">
      <form onSubmit={handleSubmit}>
        <label htmlFor="sender-id">Enter sender ID:</label>
        <input
          id="sender-id"
          type="text"
          value={senderId}
          onChange={handleChange}
        />
        <button type="submit">Fetch Conversation</button>
      </form>
      {loading && <p>Loading...</p>}
      <ul className="message-list">
        {messages.map((message, index) => (
          <li
            key={index}
            className={
              message.sender === senderId ? "received-message" : "sent-message"
            }
          >
            <button
              className="username-button"
              onClick={() => handleUsernameClick(message.id)}
            >
              {message.username}
            </button>
            <span>{message.last_login}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Conversation;
