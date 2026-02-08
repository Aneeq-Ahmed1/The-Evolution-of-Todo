'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Check localStorage for saved theme
    const savedTheme = localStorage.getItem('theme') as Theme | null;
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    let initialTheme: Theme = 'light';
    if (savedTheme) {
      initialTheme = savedTheme;
    } else if (typeof window !== 'undefined' && systemPrefersDark) {
      initialTheme = 'dark';
    }

    setTheme(initialTheme);
    if (typeof document !== 'undefined') {
      document.documentElement.classList.toggle('dark', initialTheme === 'dark');
    }
    setMounted(true);
  }, []);

  useEffect(() => {
    // Apply theme to document element when theme changes
    if (typeof document !== 'undefined') {
      document.documentElement.classList.toggle('dark', theme === 'dark');
    }
    // Save theme to localStorage
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  // Don't render children until theme is set to prevent flash of unstyled content
  if (!mounted) {
    return <div className="min-h-screen bg-white dark:bg-gray-900" />;
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
