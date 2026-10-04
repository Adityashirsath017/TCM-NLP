import os
import warnings
from .model_loader import load_muril_assets, get_threshold, get_model, is_model_loaded
from .predictor import predict_comment

# Suppress unpickle / version warnings
warnings.filterwarnings("ignore")

# Primary model identifier
MODEL_NAME = "ToxicGuard MuRIL Context-Aware Toxicity Classifier"
threshold = 0.20


HUGGINGFACE_SPACE_URL = os.environ.get(
    "HUGGINGFACE_SPACE_URL",
    "https://riocoder-toxicguard-muril-api.hf.space"
)


def load_ml_assets():
    """
    Initialize ML assets.
    If HUGGINGFACE_SPACE_URL is configured, inference is delegated to Hugging Face ZeroGPU.
    This saves ~1GB RAM on Render, preventing 512MB RAM Out-Of-Memory crashes.
    """
    global threshold
    if HUGGINGFACE_SPACE_URL:
        print(f"[ML] ToxicGuard is connected to Hugging Face ZeroGPU Space: {HUGGINGFACE_SPACE_URL}", flush=True)
        threshold = 0.20
        return

    try:
        from .model_loader import load_muril_assets, get_threshold
        load_muril_assets()
        threshold = get_threshold()
    except Exception as e:
        print(f"[Warning] Local model assets not loaded ({e}). Remote HF Space fallback will be used if set.")


def predict_toxicity(text: str) -> dict:
    """
    Delegate toxicity inference to the ToxicGuard MuRIL predictor.
    Maintains compatibility with existing routes and components.
    """
    try:
        return predict_comment(text)
    except ValueError:
        return {
            "success": False,
            "toxic": False,
            "probability": 0.0,
            "toxic_probability": 0.0,
            "non_toxic_probability": 1.0,
            "status": "approved",
            "prediction": "Non-Toxic",
            "label": 0,
            "threshold": threshold,
            "message": "Empty or whitespace comment"
        }
