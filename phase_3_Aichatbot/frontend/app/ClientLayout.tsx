'use client';

import { AuthProvider } from '../components/Auth/AuthProvider';
import { ReactNode } from 'react';

export default function ClientLayout({ children }: { children: ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}