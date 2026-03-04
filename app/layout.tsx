import type { Metadata } from "next";
import { Inter, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import { TestProvider } from "@/context/TestContext";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  weight: "400",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "IELTS Speaking AI",
  description: "Practice IELTS Speaking with AI-powered evaluation",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${ibmPlexMono.variable} font-sans antialiased`}
      >
        <AuthProvider>
          <TestProvider>
            {children}
          </TestProvider>
        </AuthProvider>
      </body>
    </html>
  );
}