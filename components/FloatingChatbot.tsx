import React, { useEffect, useRef, useState } from 'react';
import { getChatbotResponse } from '../services/geminiService';
import type { ChatMessage } from '../types';
import Button from './common/Button';
import { ChatIcon } from './common/Icons';
import LoadingSpinner from './common/LoadingSpinner';

interface FloatingChatbotProps {
  isOpen: boolean;
  onClose: () => void;
}

const CloseIcon = (): React.ReactElement => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-6 w-6"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M6 18L18 6M6 6l12 12"
    />
  </svg>
);

const FloatingChatbot: React.FC<FloatingChatbotProps> = ({
  isOpen,
  onClose,
}): React.ReactElement | null => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: 'bot',
      text: "Hello! I'm your Genius Concierge. Whether you need a new workout plan, want to analyze a meal, or have a fitness question, I'm here to help. What's on your mind?",
      id: `bot-${Date.now()}`,
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect((): void => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (): Promise<void> => {
    if (input.trim() === '' || isLoading) return;

    const userMessage: ChatMessage = {
      sender: 'user',
      text: input,
      id: `user-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const botResponse = await getChatbotResponse(input);
    const botMessage: ChatMessage = {
      sender: 'bot',
      text: botResponse,
      id: `bot-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    };
    setMessages((prev) => [...prev, botMessage]);
    setIsLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-4 right-4 w-96 h-[600px] max-h-[80vh] bg-gray-800/80 backdrop-blur-md rounded-lg shadow-2xl flex flex-col z-50 text-white transition-all duration-300 ease-in-out transform animate-fadeInUp">
      <header className="flex items-center justify-between p-4 bg-gray-900/50 rounded-t-lg border-b border-gray-700">
        <div className="flex items-center">
          <ChatIcon className="w-6 h-6 text-teal-400 mr-2" />
          <h2 className="text-lg font-bold">AI Coach</h2>
        </div>
        <button
          onClick={onClose}
          aria-label="Close chat"
          className="text-gray-400 hover:text-white transition-colors"
        >
          <CloseIcon />
        </button>
      </header>

      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg) => (
          <div
            key={
              msg.id ?? `${msg.sender}-${Math.random().toString(36).slice(2)}`
            }
            className={`flex items-start my-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-4 py-2 rounded-lg shadow ${msg.sender === 'user' ? 'bg-teal-600 text-white rounded-br-none' : 'bg-gray-700 text-gray-200 rounded-bl-none'}`}
            >
              <p className="whitespace-pre-wrap text-sm">{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start my-3">
            <div className="bg-gray-700 text-gray-200 px-4 py-2 rounded-lg rounded-bl-none shadow">
              <LoadingSpinner />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-gray-900/50 rounded-b-lg border-t border-gray-700">
        <div className="flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything..."
            className="flex-1 bg-gray-700 text-white p-3 rounded-l-md focus:outline-none focus:ring-2 focus:ring-teal-500 text-sm"
            disabled={isLoading}
          />
          <Button
            onClick={handleSend}
            disabled={isLoading || input.trim() === ''}
            className="rounded-l-none text-sm"
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};

export default FloatingChatbot;
