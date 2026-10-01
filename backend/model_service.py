import os
import re
import json
import warnings
import joblib
import numpy as np
from scipy.sparse import hstack

# Suppress scikit-learn unpickle version notice for clean terminal logs
warnings.filterwarnings("ignore", category=UserWarning)

# Global singleton references loaded ONCE on FastAPI startup
model = None
word_vectorizer = None
char_vectorizer = None
model_config = {}
threshold = 0.63
class_1_idx = 1

def clean_text(text: str) -> str:
    """Clean and normalize comment text conservatively as in V3 training."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_ml_assets():
    """Load the trained V3 model, dual TF-IDF vectorizers, and configuration once at startup."""
    global model, word_vectorizer, char_vectorizer, model_config, threshold, class_1_idx

    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")

    model_path = os.path.join(models_dir, "toxic_comment_model_v3.pkl")
    word_vec_path = os.path.join(models_dir, "toxic_comment_word_vectorizer_v3.pkl")
    char_vec_path = os.path.join(models_dir, "toxic_comment_char_vectorizer_v3.pkl")
    config_path = os.path.join(models_dir, "toxic_comment_config_v3.json")

    # Validate file presence
    for path, name in [
        (model_path, "Model V3"),
        (word_vec_path, "Word Vectorizer V3"),
        (char_vec_path, "Char Vectorizer V3"),
        (config_path, "Config V3")
    ]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {name} file at: {path}")

    # Load configuration
    with open(config_path, "r", encoding="utf-8") as f:
        model_config = json.load(f)

    threshold = float(model_config.get("threshold", 0.63))
    print(f"[V3 Model] Loaded config: threshold = {threshold}, version = {model_config.get('model_version', 'V3')}")

    print("[V3 Model] Loading Model V3 and dual TF-IDF vectorizers into memory...")
    model = joblib.load(model_path)
    word_vectorizer = joblib.load(word_vec_path)
    char_vectorizer = joblib.load(char_vec_path)

    # Confirm index of class 1 (Toxic)
    if 1 in model.classes_:
        class_1_idx = int(np.where(model.classes_ == 1)[0][0])
    else:
        class_1_idx = 1

    print(f"[V3 Model] Loaded successfully. Classes: {model.classes_}, Toxic Class Index: {class_1_idx}")

def predict_toxicity(text: str) -> dict:
    """
    Run V3 ML prediction on input comment.
    Pipeline:
    clean text -> word vectorizer + char vectorizer -> hstack -> model.predict_proba() -> threshold (0.63)
    """
    global model, word_vectorizer, char_vectorizer, threshold, class_1_idx

    if model is None or word_vectorizer is None or char_vectorizer is None:
        raise RuntimeError("V3 ML model assets have not been initialized.")

    cleaned = clean_text(text)
    if not cleaned:
        return {
            "toxic": False,
            "probability": 0.0,
            "status": "approved",
            "message": "Empty or whitespace comment"
        }

    # Transform using dual word + char TF-IDF vectorizers
    X_word = word_vectorizer.transform([cleaned])
    X_char = char_vectorizer.transform([cleaned])
    X = hstack([X_word, X_char])

    # Probability of class 1 (toxic)
    probabilities = model.predict_proba(X)[0]
    prob_toxic = float(probabilities[class_1_idx])

    # Decision logic based on V3 threshold = 0.63
    is_toxic = bool(prob_toxic >= threshold)

    if is_toxic:
        return {
            "toxic": True,
            "probability": round(prob_toxic, 4),
            "status": "blocked",
            "message": "Comment contains toxic or offensive language"
        }
    else:
        return {
            "toxic": False,
            "probability": round(prob_toxic, 4),
            "status": "approved",
            "message": "Comment is non-toxic"
        }
