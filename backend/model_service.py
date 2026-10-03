import os
import warnings
from .model_loader import load_muril_assets, get_threshold, get_model, is_model_loaded
from .predictor import predict_comment

# Suppress unpickle / version warnings
warnings.filterwarnings("ignore")

# Primary model identifier
MODEL_NAME = "ToxicGuard MuRIL Context-Aware Toxicity Classifier"
threshold = 0.20


def load_ml_assets():
    """
    Load the newly trained ToxicGuard MuRIL Transformer model once on startup.
    Keeps model in memory for real-time contextual toxicity detection.
    """
    global threshold
    load_muril_assets()
    threshold = get_threshold()


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
