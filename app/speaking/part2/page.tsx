"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { useTest } from "@/context/TestContext";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { MicButton } from "@/components/MicButton";
import { AnswerInput } from "@/components/AnswerInput";
import { CircularTimer } from "@/components/CircularTimer";
import { LoadingOverlay } from "@/components/LoadingOverlay";
import { AudioRecorder } from "@/lib/audio";
import { getAPI, postAPI } from "@/lib/api";

interface CueCard {
  topic: string;
  hints: string[];
  follow_up?: string;
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

enum Phase {
  PREP = "prep",
  SPEAKING = "speaking",
  DONE = "done",
}

export default function Part2() {
  const { token } = useAuth();
  const { setPart2Result } = useTest();
  const router = useRouter();

  const [cueCard, setCueCard] = useState<CueCard | null>(null);
  const [phase, setPhase] = useState<Phase>(Phase.PREP);
  const [prepTime, setPrepTime] = useState(60);
  const [speakingTime, setSpeakingTime] = useState(120);
  const [answer, setAnswer] = useState("");
  const [recording, setRecording] = useState<Blob | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState("");

  const recorder = new AudioRecorder();

  // Load cue card
  useEffect(() => {
    const loadCueCard = async () => {
      try {
        const data = await getAPI<CueCard>("/generate-part2", token);
        setCueCard(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load cue card"
        );
      } finally {
        setIsLoading(false);
      }
    };

    if (token) {
      loadCueCard();
    }
  }, [token]);

  // Prep timer effect
  useEffect(() => {
    if (phase !== Phase.PREP || isLoading) return;

    const interval = setInterval(() => {
      setPrepTime((t) => {
        if (t <= 1) {
          setPhase(Phase.SPEAKING);
          return t;
        }
        return t - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [phase, isLoading]);

  // Speaking timer effect
  useEffect(() => {
    if (phase !== Phase.SPEAKING) return;

    const interval = setInterval(() => {
      setSpeakingTime((t) => {
        if (t <= 1) {
          setPhase(Phase.DONE);
          return t;
        }
        return t - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [phase]);

  // Auto-start recording when speaking phase starts
  useEffect(() => {
    if (phase === Phase.SPEAKING && !isRecording) {
      startRecording();
    }
  }, [phase]);

  // Auto-stop recording when done
  useEffect(() => {
    if (phase === Phase.DONE && isRecording) {
      stopRecording();
    }
  }, [phase]);

  const startRecording = async () => {
    try {
      await recorder.start();
      setIsRecording(true);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to start recording"
      );
    }
  };

  const stopRecording = async () => {
    try {
      const audioBlob = await recorder.stop();
      setRecording(audioBlob);
      setIsRecording(false);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to stop recording"
      );
    }
  };

  const toggleRecording = async () => {
    if (isRecording) {
      await stopRecording();
    } else {
      await startRecording();
    }
  };

  const handleSubmit = async () => {
    setIsEvaluating(true);
    try {
      const evaluationData = {
        questions: [
          {
            question: cueCard?.topic || "Long Turn Question",
            answer: answer,
          },
        ],
      };

      const result = await postAPI<PartResult>(
        "/evaluate",
        evaluationData,
        token
      );
      setPart2Result(result);
      router.push("/speaking/part3");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to evaluate answer"
      );
    } finally {
      setIsEvaluating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <div className="space-y-4 text-center">
          <div className="flex justify-center gap-2">
            <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
            <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
            <div className="h-3 w-3 rounded-full bg-accent animate-pulse"></div>
          </div>
          <p className="text-muted-foreground">Loading cue card...</p>
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
          Part 2: Long Turn
        </h1>
        <p className="text-muted-foreground">
          You will have 60 seconds to prepare and 2 minutes to speak
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

      <div className="grid md:grid-cols-2 gap-12 items-start">
        {/* Left: Cue Card & Timer */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-8"
        >
          {/* Cue Card */}
          {cueCard && (
            <div className="card-base p-8 space-y-6">
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground font-semibold uppercase">
                  Describe:
                </p>
                <h2 className="text-3xl font-bold text-primary">
                  {cueCard.topic}
                </h2>
              </div>

              <div className="space-y-3">
                <p className="text-sm text-muted-foreground font-semibold">
                  You should say:
                </p>
                <ul className="space-y-2">
                  {cueCard.hints.map((hint, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <span className="text-accent mt-1">•</span>
                      <span className="text-foreground">{hint}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {cueCard.follow_up && (
                <div className="pt-4 border-t border-border">
                  <p className="text-sm text-muted-foreground">
                    And if possible, explain {cueCard.follow_up}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Timer */}
          <div className="flex justify-center">
            {phase === Phase.PREP && (
              <CircularTimer
                remaining={prepTime}
                total={60}
                label="Prepare your answer"
                color="gold"
              />
            )}
            {phase === Phase.SPEAKING && (
              <CircularTimer
                remaining={speakingTime}
                total={120}
                label="Speak now!"
                color="red"
              />
            )}
            {phase === Phase.DONE && (
              <div className="text-center">
                <div className="text-5xl mb-4">✓</div>
                <p className="text-xl font-semibold text-success">
                  Time's up!
                </p>
              </div>
            )}
          </div>
        </motion.div>

        {/* Right: Recording & Answer */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-8"
        >
          {/* Recording Status */}
          <div className="card-base p-6 text-center space-y-4">
            <p className="text-sm font-semibold text-muted-foreground uppercase">
              {phase === Phase.PREP && "Preparing..."}
              {phase === Phase.SPEAKING && "Recording..."}
              {phase === Phase.DONE && "Recording Complete"}
            </p>

            {/* Mic Button */}
            {phase !== Phase.PREP && (
              <div className="flex justify-center">
                <MicButton
                  isRecording={isRecording}
                  onClick={toggleRecording}
                  disabled={phase === Phase.DONE}
                />
              </div>
            )}

            {recording && (
              <p className="text-sm text-success font-semibold">
                ✓ Answer recorded
              </p>
            )}
          </div>

          {/* Answer Notes */}
          <AnswerInput
            value={answer}
            onChange={setAnswer}
            placeholder="Write notes about your answer (optional)"
            disabled={phase === Phase.PREP}
          />

          {/* Submit Button */}
          {phase === Phase.DONE && (
            <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              onClick={handleSubmit}
              disabled={isEvaluating}
              className="btn-primary w-full disabled:opacity-50"
            >
              {isEvaluating ? "Evaluating..." : "Submit Part 2"}
            </motion.button>
          )}
        </motion.div>
      </div>
    </main>
  );
}
