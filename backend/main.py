import os
import sys
from contextlib import asynccontextmanager

# Configure Windows console encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load environment variables securely from .env
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(root_env):
            load_dotenv(root_env)
except ImportError:
    pass

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .database.firebase import init_firebase
from .model_service import load_ml_assets, threshold
from .routes import posts, comments, predict

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Firebase] Initializing Firebase Realtime Database (credentials from .env)...", flush=True)
    init_firebase()
    print("[ML] Initializing ToxicGuard MuRIL Context-Aware Toxicity Classifier...", flush=True)
    load_ml_assets()
    print("[Ready] ToxicGuard Backend is Ready & Secured with MuRIL Model!", flush=True)
    yield
    print("[Shutdown] Shutting down Toxic Comment Detection Backend...", flush=True)

app = FastAPI(
    title="ToxicGuard API (MuRIL)",
    description="Real-time ML-powered Toxic Comment Detection System with ToxicGuard MuRIL Context-Aware Toxicity Classifier (Threshold: 0.20)",
    version="4.0.0",
    lifespan=lifespan
)

# Attach Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register routes
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(predict.router)

# Mount static images directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")
if os.path.exists(static_dir):
    from fastapi.staticfiles import StaticFiles
    app.mount("/images", StaticFiles(directory=static_dir), name="images")

@app.get("/api/health", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    from .model_loader import get_threshold, is_model_loaded, get_device
    return {
        "status": "healthy",
        "model_name": "ToxicGuard MuRIL Context-Aware Toxicity Classifier",
        "base_model": "google/muril-base-cased",
        "model_version": "MuRIL-Final",
        "threshold": get_threshold(),
        "database": "firebase_realtime_database",
        "security": "enabled",
        "app": "Toxic Comment Detection",
        "model_loaded": is_model_loaded(),
        "device": str(get_device()),
        "version": "4.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
