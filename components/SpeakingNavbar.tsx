"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useRouter, usePathname } from "next/navigation";
import { motion } from "framer-motion";

export function SpeakingNavbar() {
  const { logout, email } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  const getPart = () => {
    if (pathname.includes("part1")) return 1;
    if (pathname.includes("part2")) return 2;
    if (pathname.includes("part3")) return 3;
    if (pathname.includes("results")) return 4;
    return 0;
  };

  const currentPart = getPart();
  const parts = [1, 2, 3, 4];

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="text-xl font-bold text-accent">
          IELTS AI
        </Link>

        {/* Progress Indicator */}
        <div className="hidden md:flex items-center gap-2">
          {parts.map((part, i) => (
            <div key={part} className="flex items-center">
              <motion.div
                initial={{ scale: 1 }}
                animate={{
                  scale: currentPart === part ? 1.2 : 1,
                  backgroundColor:
                    currentPart >= part ? "#1e3a5f" : "#e5e7eb",
                }}
                className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold"
                style={{
                  color: currentPart >= part ? "#ffffff" : "#6b7280",
                }}
              >
                {part === 4 ? "R" : `P${part}`}
              </motion.div>
              {i < parts.length - 1 && (
                <div
                  className="w-8 h-0.5 mx-2"
                  style={{
                    backgroundColor:
                      currentPart > part ? "#1e3a5f" : "#e5e7eb",
                  }}
                />
              )}
            </div>
          ))}
        </div>

        {/* User Info & Logout */}
        <div className="flex items-center gap-4">
          <span className="text-sm text-muted-foreground hidden sm:inline">
            {email}
          </span>
          <button
            onClick={handleLogout}
            className="text-sm font-semibold text-primary hover:text-accent transition"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
