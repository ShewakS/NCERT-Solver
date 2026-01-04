from fastapi import FastAPI
from backend.api import chat, feedback
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import FileResponse

app = FastAPI(title="NCERT Multilingual Doubt Solver")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

app.include_router(chat.router, prefix="/api/chat")
app.include_router(feedback.router, prefix="/api/feedback")

@app.get("/")
def root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"status": "ok", "service": "NCERT Doubt Solver"}
