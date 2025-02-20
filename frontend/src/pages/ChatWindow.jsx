import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "../styles/ChatWindow.css";

const MAX_MESSAGES = 50; // Store as many messages as possible

const ChatWindow = () => {
  const [question, setQuestion] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const chatLogRef = useRef(null); // Reference to chat log container

  // Ensure the scrollbar is always at the bottom
  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [chatLog]);

  const handleInputChange = (e) => {
    setQuestion(e.target.value);
  };

  // Handles sending the message
  const handleSend = async () => {
    if (question.trim() === "") return;

    let updatedChatLog = [...chatLog, { type: "user", text: `<strong>User:</strong> ${question}` }];
    
    if (updatedChatLog.length > MAX_MESSAGES) {
      updatedChatLog = updatedChatLog.slice(-MAX_MESSAGES); // Keep only the most recent messages
    }

    setChatLog(updatedChatLog);
    setQuestion("");

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/chat`, { question, conversation_history: updatedChatLog });
      const aiResponse = response.data.response;

      // Ensure escape characters are preserved in the AI response
      updatedChatLog = [...updatedChatLog, { type: "ai", text: `<strong>AI:</strong> ${aiResponse.replace(/\n/g, "<br>").replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;")}` }];

      if (updatedChatLog.length > MAX_MESSAGES) {
        updatedChatLog = updatedChatLog.slice(-MAX_MESSAGES);
      }

      setChatLog(updatedChatLog);
    } catch (error) {
      console.error("Error fetching AI response:", error.response ? error.response.data : error.message);
      setChatLog([...updatedChatLog, { type: "ai", text: "<strong>AI:</strong> An error occurred while generating content." }]);
    }
  };

  // Handle Enter key press
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  };

  // Clear chat log
  const handleClear = () => {
    setChatLog([]);
  };

  return (
    <div className="chat-background">
      <div className="chat-window">
        <h1 className="chat-title">Chat With The AI</h1>
        <div className="chat-log" ref={chatLogRef}>
          {chatLog.map((entry, index) => (
            <div
              key={index}
              className={`chat-entry ${entry.type}`}
              dangerouslySetInnerHTML={{ __html: entry.text }}
            />
          ))}
        </div>
        <div className="chat-input">
          <textarea
            value={question}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your question here..."
            rows="5" // Adjust the number of rows for height
            style={{ wordWrap: "break-word" }} // Ensure word wrap
          />
          <button onClick={handleSend}>Send</button>
          <button onClick={handleClear} className="clear-btn">Clear</button>
        </div>
        <p className="disclaimer">The AI does not remember previous conversations. <br></br>Powered by Google Gemini 2.0</p>
      </div>
    </div>
  );
};

export default ChatWindow;
