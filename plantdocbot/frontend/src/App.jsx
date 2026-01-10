import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ChatMessage from './components/ChatMessage';

const API_BASE_URL = 'http://localhost:8001';

function App() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Hello! I am PlantDocBot. 🌱\nUpload a photo of a plant leaf or describe symptoms, and I will help diagnose the disease.',
      image: null,
      treatment: null
    }
  ]);
  const [input, setInput] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      // Focus back to input
    }
  };

  const [lastDiagnosis, setLastDiagnosis] = useState(null); // Context for follow-up questions

  const handleSubmit = async () => {
    if (!input.trim() && !selectedImage) return;

    const userMessage = {
      sender: 'user',
      text: input,
      image: previewUrl,
      treatment: null
    };

    setMessages(prev => [...prev, userMessage]);

    // Clear input state immediately
    const currentInput = input;
    const currentImage = selectedImage;
    setInput('');
    setSelectedImage(null);
    setPreviewUrl(null);
    setIsLoading(true);

    try {
      let response;
      const formData = new FormData();

      if (currentImage && currentInput) {
        // Combined mode
        formData.append('file', currentImage);
        formData.append('text', currentInput);
        response = await axios.post(`${API_BASE_URL}/predict-combined`, formData);
      } else if (currentImage) {
        // Image only
        formData.append('file', currentImage);
        response = await axios.post(`${API_BASE_URL}/predict-image`, formData);
      } else {
        // Text only - Include context if available
        const formDataText = new FormData();
        formDataText.append('text', currentInput);
        if (lastDiagnosis) {
          formDataText.append('context_disease', lastDiagnosis);
        }
        response = await axios.post(`${API_BASE_URL}/predict-text`, formDataText);
      }

      const data = response.data;

      let botResponse;

      if (data.type === 'chat') {
        botResponse = {
          sender: 'bot',
          text: data.message,
          treatment: null,
          image: null
        };
      } else {
        // Handle Diagnosis (Card View)
        botResponse = {
          sender: 'bot',
          text: `**Diagnosis:** ${data.disease}\n**Confidence:** ${data.confidence}`,
          treatment: data.treatment,
          image: null
        };
        // Save this diagnosis as context for future questions
        if (data.disease_code) {
          setLastDiagnosis(data.disease_code);
        }
      }

      setMessages(prev => [...prev, botResponse]);

      // If there's an additional chat response (from Combined Q&A), add it as a separate message
      if (data.chat_response) {
        const extraMessage = {
          sender: 'bot',
          text: data.chat_response,
          treatment: null,
          image: null
        };
        // Small delay to make it feel natural
        setTimeout(() => {
          setMessages(prev => [...prev, extraMessage]);
        }, 500);
      }

    } catch (error) {
      console.error("Error calling API:", error);
      const errorMsg = {
        sender: 'bot',
        text: "Sorry, I encountered an error processing your request. Please ensure the backend is running.",
        image: null,
        treatment: null
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="brand">
          <span className="brand-icon">🌿</span> PlantDocBot
        </div>
        <button className="new-chat-btn" onClick={() => window.location.reload()}>
          <span>+</span> New Diagnosis
        </button>
      </div>

      {/* Main Chat Area */}
      <div className="main-chat-area">
        <div className="chat-container">
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg} />
          ))}
          {isLoading && (
            <div className="message-row bot">
              <div className="message-content">
                <div className="avatar bot-avatar">🤖</div>
                <div className="message-bubble typing-dots">Thinking...</div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="input-container">
          <div className="input-box">
            {previewUrl && (
              <div className="preview-area">
                <img src={previewUrl} alt="Preview" className="preview-thumb" />
                <button
                  className="remove-img-btn"
                  onClick={() => { setSelectedImage(null); setPreviewUrl(null); }}
                >
                  ✕
                </button>
              </div>
            )}

            <div className="textarea-wrapper">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleImageSelect}
                accept="image/*"
                style={{ display: 'none' }}
              />

              <div className="tools">
                <button
                  className="tool-btn"
                  onClick={() => fileInputRef.current.click()}
                  title="Upload Image"
                >
                  📷
                </button>
              </div>

              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Describe symptoms or upload a leaf photo..."
                rows={1}
              />

              <button
                className="send-btn"
                onClick={handleSubmit}
                disabled={!input && !selectedImage && !isLoading}
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
