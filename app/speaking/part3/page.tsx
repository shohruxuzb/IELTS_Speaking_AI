"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { useTest } from "@/context/TestContext";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { QuestionCard } from "@/components/QuestionCard";
import { MicButton } from "@/components/MicButton";
import { AnswerInput } from "@/components/AnswerInput";
import { LoadingOverlay } from "@/components/LoadingOverlay";
import { AudioRecorder } from "@/lib/audio";
import { getAPI, postAPI } from "@/lib/api";

interface Question {
  id: string;
  question: string;
}

interface PartResult {
  band_score: number;
  fluency_coherence: number;
  lexical_resource: number;
  grammatical_range: number;
  pronunciation: number;
  strengths: string[];
  areas_to_improve: string[];
  improved_answers?: string[];
}

export default function Part3() {
  const { token } = useAuth();
  const { setPart3Result } = useTest();
  const router = useRouter();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<string[]>(["", "", ""]);
  const [recordings, setRecordings] = useState<(Blob | null)[]>([null, null, null]);
  const [recordingIndex, setRecordingIndex] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState("");

  const recorder = new AudioRecorder();

  // Load questions on mount
  useEffect(() => {
    const loadQuestions = async () => {
      try {
        const data = await getAPI<{ questions: Question[] }>(
          "/generate-part3",
          token
        );
        setQuestions(data.questions || []);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load questions"
        );
      } finally {
        setIsLoading(false);
      }
    };

    if (token) {
      loadQuestions();
    }
  }, [token]);

  const toggleRecording = async (index: number) => {
    try {
      if (recordingIndex === index) {
        // Stop recording
        const audioBlob = await recorder.stop();
        const newRecordings = [...recordings];
        newRecordings[index] = audioBlob;
        setRecordings(newRecordings);
        setRecordingIndex(null);
      } else {
        // Stop previous recording if any
        if (recordingIndex !== null) {
          recorder.abort();
        }
        // Start new recording
        await recorder.start();
        setRecordingIndex(index);
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to manage recording"
      );
    }
  };

  const handleSubmit = async () => {
    if (!answers.every((a) => a.trim())) {
      setError("Please answer all questions");
      return;
    }

    setIsEvaluating(true);
    try {
      const evaluationData = {
        questions: questions.map((q, i) => ({
          question: q.question,
          answer: answers[i],
        })),
      };

      const result = await postAPI<PartResult>(
        "/evaluate",
        evaluationData,
        token
      );
      setPart3Result(result);
      router.push("/results");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to evaluate answers"
      );
    } finally {
      setIsEvaluating(false);
    }
  };

  const allAnswersFilled = answers.every((a) => a.trim().length > 0);

  if (isLoading) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <div className="space-y-4 text-center">
          <div className="flex justify-center gap-2">
            <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
            <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
            <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
          </div>
          <p className="text-muted-foreground">Loading questions...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="max-w-6xl mx-auto px-6 py-12">
      <LoadingOverlay isVisible={isEvaluating} />

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12"
      >
        <h1 className="text-3xl lg:text-4xl font-bold text-primary mb-2">
          Part 3: Discussion
        </h1>
        <p className="text-muted-foreground">
          Answer the following abstract questions
        </p>
      </motion.div>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-error/10 border border-error text-error p-4 rounded-lg mb-6"
        >
          {error}
        </motion.div>
      )}

      {/* Questions */}
      <div className="space-y-6 mb-12">
        {questions.map((q, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="space-y-4"
          >
            <QuestionCard number={i + 1} question={q.question} />

            {/* Recording & Answer */}
            <div className="grid md:grid-cols-2 gap-6 lg:ml-14">
              {/* Mic Button */}
              <div className="flex items-center justify-center">
                <MicButton
                  isRecording={recordingIndex === i}
                  onClick={() => toggleRecording(i)}
                />
              </div>

              {/* Answer Input */}
              <AnswerInput
                value={answers[i]}
                onChange={(val) => {
                  const newAnswers = [...answers];
                  newAnswers[i] = val;
                  setAnswers(newAnswers);
                }}
                placeholder="Type your answer here..."
              />
            </div>

            {recordings[i] && (
              <div className="lg:ml-14 text-sm text-success font-semibold">
                ✓ Answer recorded
              </div>
            )}
          </motion.div>
        ))}
      </div>

      {/* Submit Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="flex gap-4"
      >
        <button
          onClick={handleSubmit}
          disabled={!allAnswersFilled || isEvaluating}
          className={`flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed ${
            !allAnswersFilled ? "opacity-50" : ""
          }`}
        >
          {isEvaluating ? "Evaluating..." : "Submit Part 3"}
        </button>
      </motion.div>
    </main>
  );
}
