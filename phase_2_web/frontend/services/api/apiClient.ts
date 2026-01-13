// frontend/services/api/apiClient.ts
import { authService } from './authService';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    // Check if body is FormData to avoid setting Content-Type header
    const isFormData = options.body instanceof FormData;

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

    const config: RequestInit = {
      headers,
      ...options,
    };

    try {
      const response = await fetch(url, config);

      // If response is 401, user might need to log in again
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        throw new Error('Unauthorized. Please log in again.');
      }

      if (!response.ok) {
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
        return await response.json();
      } else {
        // For non-JSON responses, return as text or handle as needed
        return await response.json(); // Still try to parse as JSON since auth endpoints return JSON
      }
    } catch (error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();