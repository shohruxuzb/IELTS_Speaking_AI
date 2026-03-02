from fastapi import FastAPI
from app.api import routes_eval, routes_questions, routes_voice, routes_results

app = FastAPI()

app.include_router(routes_eval.router)
app.include_router(routes_questions.router)
app.include_router(routes_voice.router)
app.include_router(routes_results.router)