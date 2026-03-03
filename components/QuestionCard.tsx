"use client";

import { motion } from "framer-motion";

interface QuestionCardProps {
  number: number;
  question: string;
  onClick?: () => void;
}

export function QuestionCard({
  number,
  question,
  onClick,
}: QuestionCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: number * 0.1 }}
      onClick={onClick}
      className="card-base p-6 cursor-pointer hover:shadow-xl hover:border-accent/50 transition"
    >
      <div className="flex gap-4 items-start">
        <div className="w-10 h-10 rounded-full bg-accent text-primary flex items-center justify-center font-bold flex-shrink-0">
          {number}
        </div>
        <div className="flex-1">
          <p className="text-foreground leading-relaxed">{question}</p>
        </div>
      </div>
    </motion.div>
  );
}
