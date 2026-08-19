import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, AuthResponse } from '../types';
import { authApi } from '../api/client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, pass: string) => Promise<void>;
  register: (name: string, email: string, pass: string, role?: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  switchDemoRole: (role: 'ADMIN' | 'ANALYST' | 'CUSTOMER') => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('nexus_token'));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initUser = async () => {
      const savedToken = localStorage.getItem('nexus_token');
      if (savedToken) {
        try {
          const userData = await authApi.getMe();
          setUser(userData);
        } catch {
          localStorage.removeItem('nexus_token');
          setToken(null);
          setUser(null);
        }
      } else {
        // Auto-login default customer user for immediate demo access
        await switchDemoRole('CUSTOMER');
      }
      setIsLoading(false);
    };
    initUser();
  }, []);

  const login = async (email: string, pass: string) => {
    setIsLoading(true);
    try {
      const authRes: AuthResponse = await authApi.login(email, pass);
      localStorage.setItem('nexus_token', authRes.access_token);
      setToken(authRes.access_token);
      setUser({
        id: authRes.user_id,
        email: authRes.email,
        full_name: authRes.name,
        role: authRes.role as any,
        customer_id: authRes.customer_id
      });
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (name: string, email: string, pass: string, role = 'CUSTOMER') => {
    setIsLoading(true);
    try {
      const authRes: AuthResponse = await authApi.register({ full_name: name, email, password: pass, role });
      localStorage.setItem('nexus_token', authRes.access_token);
      setToken(authRes.access_token);
      setUser({
        id: authRes.user_id,
        email: authRes.email,
        full_name: authRes.name,
        role: authRes.role as any,
        customer_id: authRes.customer_id
      });
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('nexus_token');
    setToken(null);
    setUser(null);
  };

  const switchDemoRole = async (role: 'ADMIN' | 'ANALYST' | 'CUSTOMER') => {
    setIsLoading(true);
    try {
      const creds = {
        ADMIN: { email: 'admin@platform.ai', pass: 'Admin@123456' },
        ANALYST: { email: 'analyst@platform.ai', pass: 'Analyst@123456' },
        CUSTOMER: { email: 'customer@platform.ai', pass: 'Customer@123456' },
      }[role];
      const authRes = await authApi.login(creds.email, creds.pass);
      localStorage.setItem('nexus_token', authRes.access_token);
      setToken(authRes.access_token);
      setUser({
        id: authRes.user_id,
        email: authRes.email,
        full_name: authRes.name,
        role: authRes.role as any,
        customer_id: authRes.customer_id
      });
    } catch (e) {
      console.warn('Demo switch note:', e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isLoading, switchDemoRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
