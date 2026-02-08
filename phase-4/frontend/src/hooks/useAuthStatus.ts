import { useState, useEffect } from 'react';
import { useSession } from '../lib/auth';

export const useAuthStatus = () => {
  const [authStatus, setAuthStatus] = useState<'checking' | 'authenticated' | 'unauthenticated'>('checking');
  const { data: session } = useSession();

  useEffect(() => {
    // Since our useSession doesn't have loading state, we just check immediately
    setAuthStatus(session?.session?.user ? 'authenticated' : 'unauthenticated');
  }, [session]);

  return { authStatus, session };
};