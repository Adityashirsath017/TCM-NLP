from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from ..database.models import PredictRequest, PredictResponse
from ..predictor import predict_comment
from ..security import sanitize_comment

router = APIRouter(tags=["Predict"])


def _handle_prediction(req: PredictRequest):
    # Extract text from either 'text' or 'comment'
    raw_text = req.text if req.text is not None else req.comment

    if raw_text is None or not str(raw_text).strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Comment text cannot be empty."}
        )

    # Sanitize input against malicious scripts and control characters
    try:
        clean_text = sanitize_comment(raw_text)
    except Exception as e:
        detail = getattr(e, "detail", "Invalid comment format.")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": detail}
        )

    try:
        result = predict_comment(clean_text)
        return PredictResponse(
            success=True,
            text=result["text"],
            prediction=result["prediction"],
            label=result["label"],
            toxic_probability=result["toxic_probability"],
            non_toxic_probability=result["non_toxic_probability"],
            threshold=result["threshold"],
            model=result["model"],
            toxic=result["toxic"],
            probability=result["probability"],
            status=result["status"],
            message=result["message"]
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Prediction failed: {str(e)}"}
        )


@router.post("/predict", response_model=PredictResponse)
def predict_endpoint(req: PredictRequest):
    """
    Primary real-time toxic comment detection endpoint using ToxicGuard MuRIL.
    Accepts {"text": "..."} or {"comment": "..."}.
    """
    return _handle_prediction(req)


@router.post("/api/predict", response_model=PredictResponse)
def api_predict_endpoint(req: PredictRequest):
    """
    API route for frontend and backward-compatible integration.
    """
    return _handle_prediction(req)
