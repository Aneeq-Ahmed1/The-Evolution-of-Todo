import { useState, useEffect } from 'react';
import { isAuthenticated } from '../lib/auth';

type AuthStatus = 'checking' | 'authenticated' | 'unauthenticated';

export const useAuthState = () => {
  const [authStatus, setAuthStatus] = useState<AuthStatus>('checking');

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authenticated = await isAuthenticated();
        setAuthStatus(authenticated ? 'authenticated' : 'unauthenticated');
      } catch (error) {
        setAuthStatus('unauthenticated');
      }
    };

    checkAuthStatus();

    // Set up a periodic check to update auth status if needed
    const interval = setInterval(checkAuthStatus, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const checkCurrentStatus = async (): Promise<AuthStatus> => {
    try {
      const authenticated = await isAuthenticated();
      const newStatus: AuthStatus = authenticated ? 'authenticated' : 'unauthenticated';
      setAuthStatus(newStatus);
      return newStatus;
    } catch (error) {
      setAuthStatus('unauthenticated');
      return 'unauthenticated';
    }
  };

  return { authStatus, checkCurrentStatus };
};