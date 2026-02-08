/**
 * API Client for the AI Agent Platform
 * Implements communication with the backend API
 */

// Base URL for the API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Send a message to the AI agent
 * @param {Object} data - Message data
 * @param {string} data.message - The user's message
 * @param {string} [data.conversation_id] - Optional conversation ID
 * @returns {Promise<Object>} Response from the API
 */
export async function sendMessage(data) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add authorization header if available
                ...getAuthHeaders()
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail?.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
}

/**
 * Get all conversations for the current user
 * @returns {Promise<Array>} List of conversations
 */
export async function getConversations() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/conversations`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail?.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error getting conversations:', error);
        throw error;
    }
}

/**
 * Create a new conversation
 * @param {Object} data - Conversation data
 * @param {string} [data.initial_message] - Optional initial message
 * @param {string} [data.title] - Optional title for the conversation
 * @returns {Promise<Object>} Created conversation
 */
export async function createConversation(data = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/conversations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail?.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating conversation:', error);
        throw error;
    }
}

/**
 * Get a specific conversation
 * @param {string} conversationId - ID of the conversation
 * @returns {Promise<Object>} Conversation data
 */
export async function getConversation(conversationId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/conversations/${conversationId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail?.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error getting conversation:', error);
        throw error;
    }
}

/**
 * Get health status of the API
 * @returns {Promise<Object>} Health status
 */
export async function getHealthStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error getting health status:', error);
        throw error;
    }
}

/**
 * Get rate limit status for the current user
 * @returns {Promise<Object>} Rate limit status
 */
export async function getRateLimitStatus() {
    try {
        // Using a mock user ID since we don't have auth implemented yet
        const userId = localStorage.getItem('user_id') || 'anonymous';

        const response = await fetch(`${API_BASE_URL}/api/rate_limit_status`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            }
        });

        // Note: The backend doesn't currently have a rate_limit_status endpoint
        // This is a placeholder for future implementation

        // For now, return a mock response
        return {
            limit: 100,
            remaining: 99,
            reset_time: Date.now() + 3600000, // 1 hour from now
            window_size: 3600 // 1 hour
        };
    } catch (error) {
        console.error('Error getting rate limit status:', error);
        // Return a default response on error
        return {
            limit: 100,
            remaining: 100,
            reset_time: Date.now(),
            window_size: 3600
        };
    }
}

/**
 * Get authentication headers
 * @returns {Object} Headers object with authorization if available
 */
function getAuthHeaders() {
    // Get the JWT token from storage (localStorage or sessionStorage)
    // The AuthProvider stores the token as 'token', not 'access_token'
    let token = localStorage.getItem('token');

    // Try sessionStorage as fallback
    if (!token) {
        token = sessionStorage.getItem('token');
    }

    if (token) {
        return {
            'Authorization': `Bearer ${token}`
        };
    }

    return {};
}

/**
 * Helper function to handle API errors consistently
 * @param {Response} response - Fetch response object
 * @returns {Promise<Object>} Processed response data or error
 */
export async function handleApiResponse(response) {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;

        // Handle specific status codes
        if (response.status === 429) {
            // Rate limit exceeded
            throw new Error(`Rate limit exceeded. Try again later.`);
        } else if (response.status === 401) {
            // Unauthorized - possibly redirect to login
            throw new Error(`Unauthorized. Please log in.`);
        } else if (response.status === 403) {
            // Forbidden
            throw new Error(`Access forbidden.`);
        } else if (response.status >= 500) {
            // Server error
            throw new Error(`Server error. Please try again later.`);
        } else {
            // Other errors
            throw new Error(errorMessage);
        }
    }

    return await response.json();
}