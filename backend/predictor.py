import os
import re
import json
import requests

HUGGINGFACE_SPACE_URL = os.environ.get(
    "HUGGINGFACE_SPACE_URL",
    "https://riocoder-toxicguard-muril-api.hf.space"
)

MAX_LENGTH = 192


def clean_text(text: str) -> str:
    """Conservative text normalization preserving script and contextual tokens."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


HF_TOKEN = (
    os.environ.get("HF_TOKEN") or
    os.environ.get("HUGGINGFACE_TOKEN") or
    os.environ.get("HUGGINGFACE_API_TOKEN") or
    ""
)


def predict_via_hf_space(cleaned_text: str, space_url: str = HUGGINGFACE_SPACE_URL) -> dict:
    """
    Execute high-speed inference on Hugging Face ZeroGPU Space.
    Includes Hugging Face authentication token when available to access user quota.
    """
    headers = {"Content-Type": "application/json"}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    call_url = f"{space_url.rstrip('/')}/gradio_api/call/predict"
    resp = requests.post(call_url, json={"data": [cleaned_text]}, headers=headers, timeout=25)
    resp.raise_for_status()
    event_id = resp.json().get("event_id")
    if not event_id:
        raise ValueError("No event_id returned from Hugging Face Space")

    result_url = f"{space_url.rstrip('/')}/gradio_api/call/predict/{event_id}"
    req_headers = {}
    if HF_TOKEN:
        req_headers["Authorization"] = f"Bearer {HF_TOKEN}"

    res = requests.get(result_url, headers=req_headers, timeout=30)
    res.raise_for_status()
    for line in res.iter_lines():
        line_str = line.decode("utf-8") if isinstance(line, bytes) else str(line)
        if line_str.startswith("data:"):
            payload = json.loads(line_str[5:].strip())
            data_item = payload[0] if isinstance(payload, list) else payload
            if isinstance(data_item, dict) and "error" in data_item:
                raise RuntimeError(f"Hugging Face ZeroGPU error: {data_item.get('error')}")
            return data_item
    raise ValueError("No prediction data received from Hugging Face Space")


def predict_comment(text: str) -> dict:
    """
    Run real-time toxicity inference using the ToxicGuard MuRIL model.
    Prioritizes Hugging Face ZeroGPU Space for fast, low-memory inference on Render.
    Falls back to local PyTorch model if available.

    Args:
        text (str): Comment text (Hindi, English, Hinglish, code-mixed, etc.)

    Returns:
        dict: Complete prediction dictionary with probabilities, threshold decision, and UI fields.
    """
    cleaned = clean_text(text)
    if not cleaned:
        raise ValueError("Comment text cannot be empty.")

    # 1. Primary: Remote inference via Hugging Face Space (ideal for Render 512MB RAM)
    if HUGGINGFACE_SPACE_URL:
        try:
            return predict_via_hf_space(cleaned, HUGGINGFACE_SPACE_URL)
        except Exception as e:
            print(f"[Warning] Hugging Face Space inference failed ({e}), checking local model fallback...")

    # 2. Local PyTorch inference fallback
    try:
        import torch
        from .model_loader import get_model, get_tokenizer, get_threshold, get_device

        model = get_model()
        tokenizer = get_tokenizer()
        threshold = get_threshold()
        device = get_device()

        model.eval()
        with torch.no_grad():
            encoded = tokenizer(
                cleaned,
                truncation=True,
                padding="max_length",
                max_length=MAX_LENGTH,
                return_tensors="pt"
            )
            encoded = {key: value.to(device) for key, value in encoded.items()}
            outputs = model(**encoded)
            probabilities = torch.softmax(outputs.logits, dim=1)[0]

        non_toxic_probability = float(probabilities[0].item())
        toxic_probability = float(probabilities[1].item())

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
            "toxic": bool(predicted_label == 1),
            "probability": round(toxic_probability, 4),
            "status": "blocked" if predicted_label == 1 else "approved",
            "message": (
                "Comment contains toxic or offensive language"
                if predicted_label == 1
                else "Comment is non-toxic"
            )
        }
    except Exception as e:
        raise RuntimeError(f"Prediction failed on both Hugging Face Space and local model: {e}")

