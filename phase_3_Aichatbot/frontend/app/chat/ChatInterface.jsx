"use client";

import { useState, useRef, useEffect } from 'react';
import { sendMessage } from '../../services/api';

/**
 * ChatInterface Component
 * Implements the chat UI for interacting with the AI agent
 * Implements FR-005: System MUST provide a web-based chatbot UI for user interaction
 * Implements FR-006: System MUST display agent identity and role clearly in the UI
 * Implements FR-009: System MUST render responses without duplication or confusion in the UI
 */
export default function ChatInterface() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState(null);
    const messagesEndRef = useRef(null);

    // Scroll to bottom of messages when they change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!inputValue.trim() || isLoading) return;

        // Add user message to the chat
        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: inputValue,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // Send message to backend
            const response = await sendMessage({
                message: inputValue,
                conversation_id: conversationId
            });

            // Update conversation ID if new conversation was created
            if (response.conversation_id && !conversationId) {
                setConversationId(response.conversation_id);
            }

            // Add assistant message to the chat
            const assistantMessage = {
                id: `assistant-${Date.now()}`,
                role: 'assistant',
                content: response.response,
                metadata: response.metadata,
                timestamp: new Date().toISOString()
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error sending message:', error);

            // Add error message to the chat
            const errorMessage = {
                id: `error-${Date.now()}`,
                role: 'system',
                content: 'Sorry, I encountered an error processing your request. Please try again.',
                timestamp: new Date().toISOString()
            };

            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const formatMessageContent = (content, metadata = {}) => {
        // Basic markdown-like formatting
        let formattedContent = content;

        // Convert **bold** to <strong>
        formattedContent = formattedContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Convert *italic* to <em>
        formattedContent = formattedContent.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // Convert line breaks
        formattedContent = formattedContent.replace(/\n/g, '<br />');

        return <span dangerouslySetInnerHTML={{ __html: formattedContent }} />;
    };

    const getMessageLabel = (role) => {
        switch (role) {
            case 'user':
                return 'You';
            case 'assistant':
                return 'AI Assistant';
            case 'system':
                return 'System';
            default:
                return role;
        }
    };

    const getMessageClass = (role) => {
        switch (role) {
            case 'user':
                return 'bg-blue-500 text-white ml-auto';
            case 'assistant':
                return 'bg-gray-200 text-gray-800 mr-auto';
            case 'system':
                return 'bg-yellow-100 text-yellow-800 mx-auto';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="flex flex-col h-full max-w-4xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
            {/* Chat header */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4">
                <h1 className="text-xl font-bold">AI Assistant Chat</h1>
                <p className="text-sm opacity-80">Ask me anything and I'll help you out!</p>
            </div>

            {/* Messages container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50" style={{ maxHeight: 'calc(100vh - 250px)' }}>
                {messages.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                        <p>Start a conversation by sending a message below.</p>
                        <p className="mt-2 text-sm">Try asking: "What can you help me with?"</p>
                    </div>
                ) : (
                    messages.map((message) => (
                        <div
                            key={message.id}
                            className={`max-w-[80%] p-3 rounded-lg ${getMessageClass(message.role)}`}
                        >
                            <div className="font-semibold text-xs mb-1">
                                {getMessageLabel(message.role)}
                            </div>
                            <div className="text-sm">
                                {formatMessageContent(message.content, message.metadata)}
                            </div>
                            {message.metadata && Object.keys(message.metadata).length > 0 && (
                                <div className="text-xs opacity-70 mt-1">
                                    {message.metadata.source_agent && `Agent: ${message.metadata.source_agent}`}
                                    {message.metadata.detected_intent && ` | Intent: ${message.metadata.detected_intent}`}
                                </div>
                            )}
                        </div>
                    ))
                )}
                {isLoading && (
                    <div className="bg-gray-200 text-gray-800 mr-auto max-w-[80%] p-3 rounded-lg">
                        <div className="font-semibold text-xs mb-1">AI Assistant</div>
                        <div className="flex space-x-2">
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div className="border-t p-4 bg-white">
                <form onSubmit={handleSubmit} className="flex space-x-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Type your message here..."
                        className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!inputValue.trim() || isLoading}
                        className={`bg-blue-600 text-white px-4 py-2 rounded-r-lg font-medium ${
                            (!inputValue.trim() || isLoading) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
                        }`}
                    >
                        Send
                    </button>
                </form>
                <p className="text-xs text-gray-500 mt-2">
                    Press Enter to send • Your conversation {conversationId ? `ID: ${conversationId}` : 'will be saved'}
                </p>
            </div>
        </div>
    );
}