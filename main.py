from fastapi import FastAPI
from api import routes_auth, routes_eval, routes_questions, routes_voice, routes_results

app = FastAPI(
    title="IELTS Speaking AI",
    description="AI-powered IELTS Speaking test simulator and evaluator.",
    version="1.0.0",
)

# Auth (public — no token required)
app.include_router(routes_auth.router)

# Protected endpoints (JWT + rate-limited)
app.include_router(routes_eval.router)
app.include_router(routes_questions.router)
app.include_router(routes_voice.router)
app.include_router(routes_results.router)