"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { TestProvider } from "@/context/TestContext";
import { SpeakingNavbar } from "@/components/SpeakingNavbar";

export default function SpeakingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedRoute>
      <TestProvider>
        <div className="min-h-screen bg-background">
          <SpeakingNavbar />
          {children}
        </div>
      </TestProvider>
    </ProtectedRoute>
  );
}
