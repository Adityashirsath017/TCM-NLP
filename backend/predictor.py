import re
import torch
from .model_loader import get_model, get_tokenizer, get_threshold, get_device

MAX_LENGTH = 192


def clean_text(text: str) -> str:
    """Conservative text normalization preserving script and contextual tokens."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@torch.no_grad()
def predict_comment(text: str) -> dict:
    """
    Run real-time toxicity inference using the ToxicGuard MuRIL model.

    Args:
        text (str): Comment text (Hindi, English, Hinglish, code-mixed, etc.)

    Returns:
        dict: Complete prediction dictionary with probabilities, threshold decision, and UI fields.
    """
    cleaned = clean_text(text)
    if not cleaned:
        raise ValueError("Comment text cannot be empty.")

    model = get_model()
    tokenizer = get_tokenizer()
    threshold = get_threshold()
    device = get_device()

    model.eval()

    encoded = tokenizer(
        cleaned,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )

    encoded = {
        key: value.to(device)
        for key, value in encoded.items()
    }

    outputs = model(**encoded)

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )[0]

    non_toxic_probability = float(probabilities[0].item())
    toxic_probability = float(probabilities[1].item())

    # Production decision threshold: 0.20
    predicted_label = int(toxic_probability >= threshold)
    predicted_class = "Toxic" if predicted_label == 1 else "Non-Toxic"

    return {
        "success": True,
        "text": text,
        "prediction": predicted_class,
        "label": predicted_label,
        "toxic_probability": round(toxic_probability, 4),
        "non_toxic_probability": round(non_toxic_probability, 4),
        "threshold": threshold,
        "model": "ToxicGuard-MuRIL",
        # Backwards-compatibility fields for UI / Comment flow
        "toxic": bool(predicted_label == 1),
        "probability": round(toxic_probability, 4),
        "status": "blocked" if predicted_label == 1 else "approved",
        "message": (
            "Comment contains toxic or offensive language"
            if predicted_label == 1
            else "Comment is non-toxic"
        )
    }
