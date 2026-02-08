// frontend/services/api/authService.ts
import { AuthCredentials } from '../types';
import { apiClient } from './apiClient';

export const authService = {
  async login(credentials: AuthCredentials): Promise<{ user: any; token: string }> {
    console.log('AuthService: login called with credentials:', credentials);
    // Create form data for login
    const formData = new FormData();
    formData.append('email', credentials.email);
    formData.append('password', credentials.password);

    console.log('AuthService: calling apiClient.request with /api/login');
    const data = await apiClient.request('/api/login', {
      method: 'POST',
      body: formData,
    });
    console.log('AuthService: apiClient.request succeeded, received data:', data);

    // Store the token and user data in localStorage
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    console.log('AuthService: returning user and token');
    return {
      user: data.user,
      token: data.access_token,
    };
  },

  async signup(credentials: AuthCredentials): Promise<{ user: any; token: string }> {
    // Create form data for registration
    const formData = new FormData();
    formData.append('email', credentials.email);
    formData.append('password', credentials.password);
    if (credentials.name) {
      formData.append('name', credentials.name);
    }

    const data = await apiClient.request('/api/register', {
      method: 'POST',
      body: formData,
    });

    // Store the token and user data in localStorage
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    return {
      user: data.user,
      token: data.access_token,
    };
  },

  async logout(): Promise<void> {
    // Clear localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser(): any | null {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        return JSON.parse(storedUser);
      } catch (e) {
        console.error('Error parsing user from localStorage', e);
        return null;
      }
    }
    return null;
  },

  isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    return token !== null && token !== undefined && token !== '';
  },
};