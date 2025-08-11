import React, { createContext, useState, ReactNode, useEffect } from 'react';
import jwtDecode from 'jwt-decode';

interface User {
  username: string;
  role: 'parent' | 'child';
}

interface AuthContextType {
  user: User | null;
  login: (access: string, refresh: string) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const access = localStorage.getItem('access_token');
    if (access) {
      const decoded: any = jwtDecode(access);
      setUser({ username: decoded.username, role: decoded.role });
    }
  }, []);

  const login = (access: string, refresh: string) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    const decoded: any = jwtDecode(access);
    setUser({ username: decoded.username, role: decoded.role });
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
