from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import (
    routes_auth,
    routes_eval,
    routes_questions,
    routes_voice,
    routes_results,
    routes_jobs,
    routes_history,
)

app = FastAPI(
    title="IELTS Speaking AI",
    description="AI-powered IELTS Speaking test simulator and evaluator.",
    version="1.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth (public)
app.include_router(routes_auth.router)

# Protected + rate-limited AI endpoints
app.include_router(routes_eval.router)
app.include_router(routes_questions.router)
app.include_router(routes_voice.router)
app.include_router(routes_results.router)

# Job polling
app.include_router(routes_jobs.router)

# History & progress
app.include_router(routes_history.router)
