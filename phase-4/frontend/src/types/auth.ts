export type AuthStatus = 'checking' | 'authenticated' | 'unauthenticated';

export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  expires_in?: number;
}

export interface AuthState {
  status: AuthStatus;
  user?: User;
  token?: string;
}

export interface AuthContextType {
  authState: AuthState;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  checkAuthStatus: () => Promise<AuthStatus>;
}