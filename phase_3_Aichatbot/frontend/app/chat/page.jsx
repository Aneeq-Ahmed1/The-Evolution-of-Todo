"use client";

import ChatInterface from './ChatInterface';

/**
 * Chat Page Component
 * Entry point for the chat interface
 */
export default function ChatPage() {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">AI Assistant Chat</h1>
                <div className="h-[600px]">
                    <ChatInterface />
                </div>
            </div>
        </div>
    );
}