"use client";

import React, { createContext, useContext, useState } from "react";

export interface TestResult {
  band_score: number;
  fluency_coherence: number;
  lexical_resource: number;
  grammatical_range: number;
  pronunciation: number;
  strengths: string[];
  areas_to_improve: string[];
  improved_answers?: string[];
}

interface TestContextType {
  part1Result: TestResult | null;
  part2Result: TestResult | null;
  part3Result: TestResult | null;
  setPart1Result: (result: TestResult) => void;
  setPart2Result: (result: TestResult) => void;
  setPart3Result: (result: TestResult) => void;
  clearResults: () => void;
}

const TestContext = createContext<TestContextType | undefined>(undefined);

export function TestProvider({ children }: { children: React.ReactNode }) {
  const [part1Result, setPart1Result] = useState<TestResult | null>(null);
  const [part2Result, setPart2Result] = useState<TestResult | null>(null);
  const [part3Result, setPart3Result] = useState<TestResult | null>(null);

  const clearResults = () => {
    setPart1Result(null);
    setPart2Result(null);
    setPart3Result(null);
  };

  const value = {
    part1Result,
    part2Result,
    part3Result,
    setPart1Result,
    setPart2Result,
    setPart3Result,
    clearResults,
  };

  return (
    <TestContext.Provider value={value}>{children}</TestContext.Provider>
  );
}

export function useTest() {
  const context = useContext(TestContext);
  if (context === undefined) {
    throw new Error("useTest must be used within TestProvider");
  }
  return context;
}
