"use client";

import { motion } from "framer-motion";

interface MicButtonProps {
  isRecording: boolean;
  onClick: () => void;
  disabled?: boolean;
}

export function MicButton({
  isRecording,
  onClick,
  disabled = false,
}: MicButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: disabled ? 1 : 1.05 }}
      whileTap={{ scale: disabled ? 1 : 0.95 }}
      onClick={onClick}
      disabled={disabled}
      className={`relative w-16 h-16 rounded-full font-semibold transition-colors flex items-center justify-center ${
        isRecording
          ? "bg-error text-white"
          : "bg-accent text-primary hover:opacity-90"
      } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      {isRecording ? (
        <motion.div
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="absolute inset-0 rounded-full border-2 border-error"
        />
      ) : null}
      <span className="text-2xl">{isRecording ? "⏹" : "🎤"}</span>
    </motion.button>
  );
}
