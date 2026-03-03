from fastapi import FastAPI
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