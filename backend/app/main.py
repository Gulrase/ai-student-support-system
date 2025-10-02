from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.chat import router as chat_router
from app.api.risk import router as risk_router


app = FastAPI(title="AI Student Support System", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(risk_router, prefix="/api/risk", tags=["risk"])

# Serve minimal UI from frontend directory at ' / ' without intercepting API paths
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.exists():
    # Mount static assets under /ui (if any), and handle root explicitly
    app.mount("/ui", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

    @app.get("/")
    def root() -> FileResponse:  # type: ignore[override]
        index_path = FRONTEND_DIR / "index.html"
        return FileResponse(str(index_path))


