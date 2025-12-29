"use client";

import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Trash2 } from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';


const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';


interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleClearChat = () => {
    setMessages([]);
  };

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please log in to use the AI Assistant.');
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, // ✅ /api hata diya, 
        { message: input },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      const aiMessage: ChatMessage = { role: 'assistant', content: response.data };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
      window.dispatchEvent(new Event('taskUpdated'));
    } catch (error) {
      console.error('Error sending message to AI:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: 'Oops! Something went wrong. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSendMessage();
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Floating Button */}
      <button
        onClick={toggleChat}
        className={`
          relative p-4 rounded-full shadow-lg text-white
          bg-gradient-to-r from-purple-600 to-blue-600
          hover:from-purple-700 hover:to-blue-700
          transition-all duration-300 ease-in-out
          ${isOpen ? 'rotate-90' : 'animate-pulse'}
        `}
      >
        {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div
          className={`
            fixed bottom-20 right-4 w-80 h-[400px] bg-gray-900/80 backdrop-blur-md rounded-xl shadow-2xl border border-gray-700
            flex flex-col transform transition-all duration-300 ease-in-out
            ${isOpen ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}
            md:w-96
          `}
        >
          {/* Header */}
          <div className="p-3 bg-gradient-to-r from-purple-700 to-blue-700 text-white rounded-t-xl font-bold text-lg flex justify-between items-center shadow-md">
            <span>AI Assistant ✨</span>
            <button onClick={handleClearChat} className="p-1 hover:bg-white/20 rounded-full">
              <Trash2 size={18} />
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 p-4 overflow-y-auto bg-gray-800/50 custom-scrollbar">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex mb-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] p-3 rounded-2xl text-sm shadow-lg
                  ${msg.role === 'user' 
                    ? 'bg-gradient-to-br from-purple-600 to-indigo-700 text-white rounded-br-none' 
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
                  }
                `}>
                  {msg.role === 'assistant' ? (
                    <div className="prose prose-sm max-w-none text-gray-800">
                        <ReactMarkdown
                            components={{
                                strong: ({node, ...props}) => <span className="font-bold text-purple-600" {...props} />,
                                ul: ({node, ...props}) => <ul className="list-disc pl-4 space-y-1 my-2" {...props} />,
                                li: ({node, ...props}) => <li className="marker:text-purple-500" {...props} />,
                                p: ({node, ...props}) => <p className="leading-snug" {...props} />
                            }}
                        >
                            {msg.content}
                        </ReactMarkdown>
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex items-center space-x-1 mb-2">
                <span className="animate-bounce delay-0 w-2 h-2 bg-purple-400 rounded-full"></span>
                <span className="animate-bounce delay-75 w-2 h-2 bg-purple-400 rounded-full">.</span>
                <span className="animate-bounce delay-150 w-2 h-2 bg-purple-400 rounded-full"></span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-3 border-t border-gray-700 bg-gray-800 rounded-b-xl">
            <input
              type="text"
              className="w-full p-2 bg-gray-900 text-white border-none rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Type your message..."
              value={input || ""}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
            />
          </div>
        </div>
      )}
      {/* Custom Scrollbar Style */}
      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(40, 40, 40, 0.5); /* Darker track */
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: linear-gradient(to bottom, #8b5cf6, #6366f1); /* Purple to blue gradient */
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: linear-gradient(to bottom, #7c3aed, #4f46e5); /* Darker gradient on hover */
        }
        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }
        .animate-pulse {
          animation: pulse 1.5s infinite ease-in-out;
        }
      `}</style>
    </div>
  );
};

export default ChatWidget;
