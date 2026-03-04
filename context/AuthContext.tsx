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

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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
      console.log("[v0] Register attempt:", { email, apiUrl: API_URL });

      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, full_name: fullName }),
      });

      if (!response.ok) {
        const error = await response.json();
        console.error("[v0] Registration failed:", error);
        throw new Error(error.detail || "Registration failed");
      }

      console.log("[v0] Registration successful");
      // Registration successful, user can now login
    } catch (error) {
      console.error("[v0] Register error:", error instanceof Error ? error.message : String(error));
      throw error;
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      console.log("[v0] Login attempt:", { email, apiUrl: API_URL });

      const response = await fetch(`${API_URL}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        console.error("[v0] Login failed:", error);
        throw new Error(error.detail || "Login failed");
      }

      const data = await response.json();
      const accessToken = data.access_token;

      setToken(accessToken);
      setEmail(email);

      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("user_email", email);
      console.log("[v0] Login successful");
    } catch (error) {
      console.error("[v0] Login error:", error instanceof Error ? error.message : String(error));
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
