// frontend/services/api/apiClient.ts
import { authService } from './authService';

// Base URL with the /api suffix since all routes now have the /api prefix
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || (typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8000/api'
  : 'https://aaneeq-todo.hf.space/api');

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    console.log('ApiClient: request called with URL:', url);

    // Check if body is FormData to avoid setting Content-Type header
    const isFormData = options.body instanceof FormData;
    console.log('ApiClient: isFormData:', isFormData);

    let headers: Record<string, string> = {};

    // Only set Content-Type to application/json if not sending FormData
    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }

    // Add any additional headers from options
    if (options.headers) {
      if (options.headers instanceof Headers) {
        // Convert Headers object to plain object
        options.headers.forEach((value, key) => {
          headers[key] = value;
        });
      } else if (typeof options.headers === 'object') {
        // Spread the headers if it's already a plain object
        for (const [key, value] of Object.entries(options.headers)) {
          if (typeof key === 'string' && typeof value === 'string') {
            headers[key] = value;
          }
        }
      }
    }

    // Add authorization header if user is authenticated
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    console.log('ApiClient: final headers:', headers);

    const config: RequestInit = {
      headers,
      ...options,
    };
    console.log('ApiClient: fetch config prepared');

    try {
      console.log('ApiClient: calling fetch with URL:', url);
      const response = await fetch(url, config);
      console.log('ApiClient: fetch response received:', response.status);

      // If response is 401, user might need to log in again
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized. Please log in again.');
      }

      if (!response.ok) {
        console.log('ApiClient: response not ok, status:', response.status);
        // Check if response is JSON before parsing
        const contentType = response.headers.get('content-type');
        let errorData: any = {};
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json().catch(() => ({}));
        } else {
          // If not JSON, try to get text and create an error object
          const errorText = await response.text().catch(() => '');
          errorData = { detail: errorText || `HTTP error! status: ${response.status}` };
        }
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      // Handle empty response
      if (response.status === 204) {
        return null;
      }

      // Check if response is JSON by looking at Content-Type header
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const jsonData = await response.json();
        console.log('ApiClient: parsed JSON response:', jsonData);
        return jsonData;
      } else {
        // For non-JSON responses, return as text or handle as needed
        const jsonData = await response.json(); // Still try to parse as JSON since auth endpoints return JSON
        console.log('ApiClient: parsed JSON response:', jsonData);
        return jsonData;
      }
    } catch (error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();