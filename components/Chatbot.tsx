import React, { useEffect, useRef, useState } from 'react';
import { getChatbotResponse } from '../services/geminiService';
import type { ChatMessage } from '../types';
import Button from './common/Button';
import LoadingSpinner from './common/LoadingSpinner';

const Chatbot: React.FC = (): React.ReactElement => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: 'bot',
      text: "Hello! I'm FitAI, your personal fitness coach. How can I help you today?",
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
    scrollToBottom();
  }, [messages]);

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

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-4">AI Coach Chat</h1>
      <div className="flex-1 bg-gray-800 rounded-lg shadow-lg overflow-y-auto p-4 mb-4">
        {messages.map((msg) => (
          <div
            key={
              msg.id ?? `${msg.sender}-${Math.random().toString(36).slice(2)}`
            }
            className={`flex items-start my-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs md:max-w-md lg:max-w-lg px-4 py-2 rounded-lg ${msg.sender === 'user' ? 'bg-teal-600 text-white rounded-br-none' : 'bg-gray-700 text-gray-200 rounded-bl-none'}`}
            >
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start my-3">
            <div className="bg-gray-700 text-gray-200 px-4 py-2 rounded-lg rounded-bl-none">
              <LoadingSpinner />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex items-center bg-gray-800 p-2 rounded-lg shadow-lg">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about fitness..."
          className="flex-1 bg-gray-700 text-white p-3 rounded-l-md focus:outline-none focus:ring-2 focus:ring-teal-500"
          disabled={isLoading}
        />
        <Button
          onClick={handleSend}
          disabled={isLoading || input.trim() === ''}
          className="rounded-l-none"
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default Chatbot;
