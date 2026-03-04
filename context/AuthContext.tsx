"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface AuthContextType {
  token: string | null;
  email: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  // Load token from localStorage on mount
  useEffect(() => {
    try {
      const savedToken = localStorage.getItem("access_token");
      const savedEmail = localStorage.getItem("user_email");
      if (savedToken) {
        setToken(savedToken);
        setEmail(savedEmail);
      }
    } catch (error) {
      console.error("Failed to load token from localStorage:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = async (
    email: string,
    password: string,
    fullName: string
  ) => {
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password: password }),
      });

      if (!response.ok) {
        const error = await response.json();
        const errorMessage = typeof error.detail === "string"
          ? error.detail
          : (Array.isArray(error.detail) ? error.detail[0].msg : "Registration failed");
        throw new Error(errorMessage);
      }

      // Registration successful, user can now login
    } catch (error) {
      throw error;
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch(`${API_URL}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }

      const data = await response.json();
      const accessToken = data.access_token;

      setToken(accessToken);
      setEmail(email);

      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("user_email", email);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    setToken(null);
    setEmail(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
  };

  const value = {
    token,
    email,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated: !!token,
  };

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
