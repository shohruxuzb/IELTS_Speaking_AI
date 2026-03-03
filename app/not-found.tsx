"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary to-primary/80 text-white flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center space-y-6"
      >
        <div className="text-7xl font-bold text-accent mb-4">404</div>
        <h1 className="text-3xl lg:text-4xl font-bold">Page Not Found</h1>
        <p className="text-lg text-gray-200 max-w-md">
          Looks like you took a wrong turn. Let's get you back on track.
        </p>
        <Link
          href="/"
          className="inline-block rounded-full px-8 py-3 bg-accent text-primary font-semibold hover:opacity-90 transition"
        >
          Return Home
        </Link>
      </motion.div>
    </div>
  );
}
