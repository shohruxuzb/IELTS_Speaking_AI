import os
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

out_dir = os.path.join(os.path.dirname(__file__) or ".", "out")

if os.path.isdir(out_dir):
    next_dir = os.path.join(out_dir, "_next")
    if os.path.isdir(next_dir):
        app.mount("/_next", StaticFiles(directory=next_dir), name="next")
    
    static_subdir = os.path.join(out_dir, "static")
    if os.path.isdir(static_subdir):
        app.mount("/static", StaticFiles(directory=static_subdir), name="static")

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

# Catch-all route for Next.js static pages
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_nextjs_frontend(full_path: str):
    """
    Serve the Next.js static export.
    If full_path is empty, serves index.html.
    Otherwise, tries out/{full_path}.html, then out/{full_path}/index.html,
    and falls back to out/404.html
    """
    if not os.path.isdir(out_dir):
        return {"status": "ok", "message": "API is running (No frontend build found)"}
        
    if not full_path or full_path == "/":
        target = os.path.join(out_dir, "index.html")
    else:
        # Prevent directory traversal
        clean_path = os.path.normpath(full_path).lstrip(os.sep)
        
        # Try exact html file (e.g., /login -> /login.html)
        target = os.path.join(out_dir, f"{clean_path}.html")
        if not os.path.exists(target):
            # Try as a directory with index.html (e.g., /speaking -> /speaking/index.html)
            target = os.path.join(out_dir, clean_path, "index.html")
            
    if os.path.exists(target):
        return FileResponse(target)
        
    # Fallback to 404 or index
    not_found = os.path.join(out_dir, "404.html")
    if os.path.exists(not_found):
        return FileResponse(not_found, status_code=404)
        
    return JSONResponse(status_code=404, content={"detail": "Not found"})

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    # Use reload=True for development; set to False in production
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
