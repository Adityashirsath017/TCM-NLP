from fastapi import APIRouter
from ..database.models import PredictRequest, PredictResponse
from ..model_service import predict_toxicity
from ..security import sanitize_comment

router = APIRouter(prefix="/api", tags=["Predict"])

@router.post("/predict", response_model=PredictResponse)
def predict_comment_toxicity(req: PredictRequest):
    # Sanitize input against malicious scripts and control characters
    clean_text = sanitize_comment(req.comment)

    result = predict_toxicity(clean_text)
    return PredictResponse(
        toxic=result["toxic"],
        probability=result["probability"],
        status=result["status"],
        message=result["message"]
    )
