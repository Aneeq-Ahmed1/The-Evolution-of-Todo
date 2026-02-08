'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Array<{id: string, role: string, content: string, timestamp: Date}>>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Get user token from localStorage or other auth mechanism
      const token = localStorage.getItem('access_token');

      // For demo purposes, use a consistent user ID
      // In a real implementation, this would come from authentication
      const userId = 'demo_user';

      // Debug logging to see the actual URL being called
      const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/${userId}/chat`;
      console.log('Calling API:', apiUrl);
      console.log('Environment variable NEXT_PUBLIC_API_BASE_URL:', process.env.NEXT_PUBLIC_API_BASE_URL);
      console.log('User ID:', userId);
      console.log('Request body:', {
        conversation_id: conversationId || undefined,
        message: input
      });

      // Call the chat API endpoint with user identification
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '', // Include token if available
        },
        body: JSON.stringify({
          conversation_id: conversationId || undefined,
          message: input
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if new conversation was created
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add AI response to chat
      const aiMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Additional debugging for 404 errors
      if (error instanceof Error && error.message.includes('404')) {
        console.error('404 Error details: The API endpoint may not exist or the server may not be running');
        console.error('Please check:');
        console.error('1. Is the backend server running on port 8000?');
        console.error('2. Is the NEXT_PUBLIC_API_BASE_URL set correctly?');
        console.error('3. Is the endpoint /api/demo_user/chat accessible?');
      }
      const errorMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: 'var(--background)' }}>
      {/* Yahoo-style Navigation */}
      <nav className="bg-white border-b" style={{ borderColor: 'var(--border)', height: '57px' }}>
        <div className="max-w-7xl mx-auto px-4 h-full flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-2xl font-semibold" style={{ color: 'var(--primary)' }}>AI Task Assistant</h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => router.push('/')}
              className="text-sm px-4 py-2 rounded font-medium"
              style={{ backgroundColor: 'var(--secondary)', color: 'var(--text-primary)' }}
            >
              Home
            </button>
          </div>
        </div>
      </nav>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-4">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4" style={{ maxHeight: 'calc(100vh - 200px)', backgroundColor: 'var(--surface)', borderRadius: '8px', padding: '16px' }}>
          {messages.length === 0 ? (
            <div className="text-center py-10">
              <h2 className="text-xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
                Welcome to AI Task Assistant!
              </h2>
              <p className="text-base mb-6" style={{ color: 'var(--text-secondary)' }}>
                I can help you manage your tasks through natural language. Try saying things like:
              </p>
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-2">
                {[
                  "Add a task to buy groceries",
                  "Show me my pending tasks",
                  "Mark the report task as complete",
                  "Delete my meeting task"
                ].map((suggestion, index) => (
                  <div
                    key={index}
                    className="p-3 rounded text-sm cursor-pointer hover:opacity-90 transition-opacity"
                    style={{
                      backgroundColor: 'var(--surface)',
                      border: '1px solid var(--border)',
                      color: 'var(--text-primary)'
                    }}
                    onClick={() => setInput(suggestion)}
                  >
                    "{suggestion}"
                  </div>
                ))}
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
              >
                <div className={`flex max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  {/* Avatar */}
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold ${
                    message.role === 'user'
                      ? 'bg-purple-500 text-white ml-2'
                      : 'bg-gray-200 text-gray-700 mr-2'
                  }`}>
                    {message.role === 'user' ? 'U' : 'AI'}
                  </div>

                  {/* Message bubble */}
                  <div className={`rounded-xl p-4 ${
                    message.role === 'user'
                      ? 'bg-purple-500 text-white rounded-tr-none'
                      : 'bg-white text-gray-800 border border-gray-200 rounded-tl-none'
                  }`}>
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-purple-200' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="flex max-w-[80%] flex-row">
                {/* AI Avatar */}
                <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold bg-gray-200 text-gray-700 mr-2">
                  AI
                </div>

                {/* Loading indicator */}
                <div className="bg-white text-gray-800 border border-gray-200 rounded-xl p-4 rounded-tl-none">
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-gray-400 mr-1 animate-bounce"></div>
                    <div className="w-2 h-2 rounded-full bg-gray-400 mr-1 animate-bounce delay-100"></div>
                    <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <form onSubmit={handleSubmit} className="mt-auto">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me to manage your tasks..."
              className="flex-1 px-4 py-3 rounded-lg border text-sm"
              style={{
                border: '1px solid var(--border)',
                backgroundColor: 'var(--surface)',
                color: 'var(--text-primary)'
              }}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="px-6 py-3 rounded-lg font-medium text-sm"
              style={{
                backgroundColor: 'var(--primary)',
                color: 'white',
                minHeight: '44px'
              }}
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </div>
          <p className="text-xs mt-2 text-center" style={{ color: 'var(--text-tertiary)' }}>
            Ask me to add, list, complete, update, or delete tasks using natural language
          </p>
        </form>
      </div>
    </div>
  );
}