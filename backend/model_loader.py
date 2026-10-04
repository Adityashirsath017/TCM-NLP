from pathlib import Path
import os
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None
    AutoTokenizer = None
    AutoModelForSequenceClassification = None

# Base directory for backend
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models" / "ToxicGuard_MuRIL_Final"

# Global singletons to ensure model is loaded ONCE on backend startup
_tokenizer = None
_model = None
_threshold = 0.20
_device = None
_is_loaded = False


def get_device():
    """Return the active compute device (cuda if available, else cpu)."""
    global _device
    if not HAS_TORCH:
        return "cpu"
    if _device is None:
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return _device


def load_muril_assets():
    """
    Load the ToxicGuard MuRIL model, tokenizer, and threshold once during server startup.
    Validates file presence and keeps the model in memory for real-time inference.
    """
    global _tokenizer, _model, _threshold, _device, _is_loaded

    if _is_loaded and _model is not None and _tokenizer is not None:
        return _model, _tokenizer, _threshold

    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"ToxicGuard MuRIL model files not found. Expected directory: {MODEL_DIR}")

    # Verify critical model files
    required_files = ["config.json", "model.safetensors", "tokenizer.json", "threshold.txt"]
    missing_files = [f for f in required_files if not (MODEL_DIR / f).exists()]
    if missing_files:
        raise FileNotFoundError(
            f"ToxicGuard MuRIL model files not found. Missing: {missing_files} in {MODEL_DIR}"
        )

    # Load threshold from threshold.txt (selected via validation threshold optimization: 0.20)
    threshold_file = MODEL_DIR / "threshold.txt"
    try:
        with open(threshold_file, "r", encoding="utf-8") as f:
            _threshold = float(f.read().strip())
    except Exception as e:
        print(f"[Warning] Could not read threshold.txt ({e}), falling back to 0.20")
        _threshold = 0.20

    _device = get_device()

    print(f"[Model Loader] Loading ToxicGuard MuRIL tokenizer from {MODEL_DIR}...")
    _tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))

    print(f"[Model Loader] Loading ToxicGuard MuRIL sequence classification model from {MODEL_DIR}...")
    _model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
    _model.to(_device)
    _model.eval()

    _is_loaded = True

    device_str = "GPU (CUDA)" if _device.type == "cuda" else "CPU"
    banner = f"""
==================================================
TOXICGUARD MODEL
==================================================
Model: google/muril-base-cased
Task: Toxic Comment Classification
Threshold: {_threshold:.2f}
Device: {device_str}
Model path: {MODEL_DIR}
Status: Loaded
==================================================
ToxicGuard MuRIL model loaded successfully
"""
    print(banner, flush=True)

    return _model, _tokenizer, _threshold


def get_model():
    """Retrieve loaded model instance or load it if not initialized."""
    global _model
    if _model is None:
        load_muril_assets()
    return _model


def get_tokenizer():
    """Retrieve loaded tokenizer instance or load it if not initialized."""
    global _tokenizer
    if _tokenizer is None:
        load_muril_assets()
    return _tokenizer


def get_threshold() -> float:
    """Retrieve the production decision threshold (0.20)."""
    global _threshold
    return _threshold


def is_model_loaded() -> bool:
    """Check if model is currently loaded in memory."""
    return _is_loaded
