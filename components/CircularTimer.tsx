"use client";

import { motion } from "framer-motion";

interface CircularTimerProps {
  remaining: number;
  total: number;
  label: string;
  color?: "gold" | "red";
}

export function CircularTimer({
  remaining,
  total,
  label,
  color = "gold",
}: CircularTimerProps) {
  const percentage = (remaining / total) * 100;
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const borderColor = color === "gold" ? "#f0a500" : "#ef4444";

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative w-32 h-32">
        {/* Background Circle */}
        <svg
          className="absolute inset-0 w-full h-full transform -rotate-90"
          viewBox="0 0 100 100"
        >
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="2"
          />
        </svg>

        {/* Progress Circle */}
        <svg
          className="absolute inset-0 w-full h-full transform -rotate-90"
          viewBox="0 0 100 100"
        >
          <motion.circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke={borderColor}
            strokeWidth="3"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            animate={{
              strokeDashoffset: strokeDashoffset,
            }}
            transition={{ duration: 0.5 }}
            strokeLinecap="round"
          />
        </svg>

        {/* Time Text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-4xl font-bold text-primary">
              {remaining}
            </div>
            <div className="text-xs text-muted-foreground mt-1">sec</div>
          </div>
        </div>
      </div>

      <p className="text-lg font-semibold text-primary">{label}</p>
    </div>
  );
}
