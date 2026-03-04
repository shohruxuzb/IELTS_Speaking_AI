"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export function APIErrorBoundary({ children }: { children: React.ReactNode }) {
  const [apiStatus, setApiStatus] = useState<"checking" | "ok" | "error">(
    "checking"
  );
  const [error, setError] = useState<string>("");

  useEffect(() => {
    // Check if API is accessible
    const checkAPI = async () => {
      const apiUrl =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

      try {
        const response = await fetch(`${apiUrl}/docs`, {
          method: "HEAD",
        });

        if (response.ok || response.status === 405) {
          // 405 is expected for HEAD request on /docs
          setApiStatus("ok");
        } else {
          setApiStatus("error");
          setError(
            `API returned status ${response.status}. Ensure backend is running.`
          );
        }
      } catch (err) {
        setApiStatus("error");
        setError(
          `Cannot connect to API at ${apiUrl}. Make sure the backend is running.`
        );
        console.error("[v0] API health check failed:", err);
      }
    };

    checkAPI();
  }, []);

  if (apiStatus === "error") {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center px-4">
        <div className="max-w-md w-full card-base p-8">
          <div className="text-center">
            <div className="mb-4 text-4xl">⚠️</div>
            <h1 className="text-2xl font-bold text-foreground mb-2">
              Connection Error
            </h1>
            <p className="text-muted-foreground mb-6">{error}</p>

            <div className="bg-secondary/10 border border-secondary rounded-lg p-4 mb-6 text-left text-sm">
              <p className="font-semibold text-foreground mb-2">
                Setup Instructions:
              </p>
              <ol className="list-decimal list-inside space-y-1 text-muted-foreground">
                <li>
                  Ensure FastAPI backend is running on port 8000:
                  <code className="bg-background px-2 py-1 rounded text-xs block mt-1">
                    python main.py
                  </code>
                </li>
                <li>
                  Create .env.local with:
                  <code className="bg-background px-2 py-1 rounded text-xs block mt-1">
                    NEXT_PUBLIC_API_URL=http://localhost:8000
                  </code>
                </li>
                <li>
                  Restart the Next.js dev server:
                  <code className="bg-background px-2 py-1 rounded text-xs block mt-1">
                    npm run dev
                  </code>
                </li>
              </ol>
            </div>

            <div className="space-y-2">
              <button
                onClick={() => window.location.reload()}
                className="w-full btn-primary"
              >
                Retry Connection
              </button>
              <Link href="/" className="w-full btn-secondary block text-center">
                Go to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
