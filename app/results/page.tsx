"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { useTest } from "@/context/TestContext";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { postAPI } from "@/lib/api";
import { SpeakingNavbar } from "@/components/SpeakingNavbar";

interface AggregatedResult {
  overall_band_score: number;
  band_level: string;
  fluency_coherence: number;
  lexical_resource: number;
  grammatical_range: number;
  pronunciation: number;
  strengths: string[];
  areas_to_improve: string[];
  improved_answers?: Record<string, string>;
  mock_test_audio_url?: string;
}

export default function Results() {
  const { token } = useAuth();
  const { part1Result, part2Result, part3Result, clearResults } = useTest();
  const router = useRouter();

  const [result, setResult] = useState<AggregatedResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  useEffect(() => {
    if (!part1Result || !part2Result || !part3Result) {
      router.push("/speaking/part1");
      return;
    }

    const fetchResults = async () => {
      try {
        const aggregatedData = {
          part1: part1Result,
          part2: part2Result,
          part3: part3Result,
        };

        const aggregatedResult = await postAPI<AggregatedResult>(
          "/aggregate-results",
          aggregatedData,
          token || undefined
        );
        setResult(aggregatedResult);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load results"
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [part1Result, part2Result, part3Result, token, router]);

  const handleRetake = () => {
    clearResults();
    router.push("/speaking/part1");
  };

  if (isLoading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-background">
          <SpeakingNavbar />
          <div className="flex h-[60vh] items-center justify-center">
            <div className="space-y-4 text-center">
              <div className="flex justify-center gap-2">
                <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
                <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
                <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
              </div>
              <p className="text-muted-foreground">Processing your results...</p>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  if (!result) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-background">
          <SpeakingNavbar />
          <main className="max-w-4xl mx-auto px-6 py-12">
            <div className="text-center text-error">
              {error || "Failed to load results"}
            </div>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  const criteria = [
    {
      label: "Fluency & Coherence",
      score: result.fluency_coherence,
    },
    {
      label: "Lexical Resource",
      score: result.lexical_resource,
    },
    {
      label: "Grammatical Range & Accuracy",
      score: result.grammatical_range,
    },
    {
      label: "Pronunciation",
      score: result.pronunciation,
    },
  ];

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        <SpeakingNavbar />
        <main className="max-w-6xl mx-auto px-6 py-12">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl lg:text-5xl font-bold text-primary mb-2">
              Your Results
            </h1>
            <p className="text-muted-foreground">
              Here's your detailed evaluation
            </p>
          </motion.div>

          {/* Section 1: Overall Score */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="card-base p-8 mb-12 text-center"
          >
            <p className="text-muted-foreground mb-4 uppercase text-sm font-semibold">
              Overall Band Score
            </p>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="mb-6"
            >
              <div className="text-7xl font-bold text-accent mb-2">
                {result.overall_band_score.toFixed(1)}
              </div>
              <p className="text-lg text-foreground font-semibold">
                {result.band_level}
              </p>
            </motion.div>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Your IELTS speaking proficiency level based on comprehensive
              evaluation across all three parts
            </p>
          </motion.div>

          {/* Section 2: Criteria Breakdown */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-12"
          >
            <h2 className="text-2xl font-bold text-primary mb-6">
              Assessment Criteria
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              {criteria.map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  className="card-base p-6"
                >
                  <div className="flex items-start justify-between mb-4">
                    <p className="font-semibold text-foreground">
                      {item.label}
                    </p>
                    <span className="text-2xl font-bold text-accent">
                      {item.score.toFixed(1)}
                    </span>
                  </div>
                  <div className="w-full bg-border rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${(item.score / 9) * 100}%` }}
                      transition={{ delay: 0.3 + i * 0.1, duration: 0.8 }}
                      className="bg-accent h-full rounded-full"
                    />
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Section 3: Strengths & Areas to Improve */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-12"
          >
            <h2 className="text-2xl font-bold text-primary mb-6">
              Feedback
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              {/* Strengths */}
              <div className="card-base p-6 bg-success/5">
                <h3 className="font-bold text-success mb-4">Strengths</h3>
                <ul className="space-y-2">
                  {result.strengths.map((strength, i) => (
                    <motion.li
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.3 + i * 0.05 }}
                      className="flex items-start gap-2 text-foreground"
                    >
                      <span className="text-success mt-1">✓</span>
                      <span>{strength}</span>
                    </motion.li>
                  ))}
                </ul>
              </div>

              {/* Areas to Improve */}
              <div className="card-base p-6 bg-warning/5">
                <h3 className="font-bold text-warning mb-4">
                  Areas to Improve
                </h3>
                <ul className="space-y-2">
                  {result.areas_to_improve.map((area, i) => (
                    <motion.li
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.3 + i * 0.05 }}
                      className="flex items-start gap-2 text-foreground"
                    >
                      <span className="text-warning mt-1">⚠</span>
                      <span>{area}</span>
                    </motion.li>
                  ))}
                </ul>
              </div>
            </div>
          </motion.div>

          {/* Section 4: Improved Answers */}
          {result.improved_answers && Object.keys(result.improved_answers).length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="mb-12"
            >
              <h2 className="text-2xl font-bold text-primary mb-6">
                Improved Answers
              </h2>
              <div className="space-y-4">
                {Object.entries(result.improved_answers).map(([key, value], i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 + i * 0.05 }}
                    className="card-base p-6"
                  >
                    <button
                      onClick={() =>
                        setExpandedSection(
                          expandedSection === key ? null : key
                        )
                      }
                      className="w-full text-left flex items-center justify-between font-semibold text-foreground hover:text-accent transition"
                    >
                      <span>{key}</span>
                      <span className="text-xl">
                        {expandedSection === key ? "−" : "+"}
                      </span>
                    </button>

                    {expandedSection === key && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4 space-y-3 pt-4 border-t border-border"
                      >
                        <div className="p-4 bg-success/5 rounded-lg">
                          <p className="text-xs font-semibold text-muted-foreground mb-2">
                            Improved Version
                          </p>
                          <p className="text-foreground leading-relaxed">
                            {value}
                          </p>
                        </div>
                      </motion.div>
                    )}
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Section 5: CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <button
              onClick={handleRetake}
              className="btn-primary"
            >
              Retake Test
            </button>
            <button className="btn-secondary">
              Download Results
            </button>
          </motion.div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
