from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import router

BACKEND_DIR = Path(__file__).resolve().parents[1]
WEBAPP_DIR = BACKEND_DIR.parent
FRONTEND_DIR = WEBAPP_DIR / "frontend"

app = FastAPI(
    title="ReproPilot API",
    version="0.2.0",
    description="Grounded reproducibility assessment for public scientific software repositories.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def homepage():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}
