from fastapi import APIRouter, HTTPException, status
from ..database.models import (
    CommentModel,
    CommentCreateRequest,
    CommentCreateResponse
)
from ..posts_data import get_code_post_by_id
from ..database.firebase import save_comment_to_firebase
from ..model_service import predict_toxicity
from ..security import sanitize_comment, sanitize_id

router = APIRouter(prefix="/api", tags=["Comments"])

@router.post("/comments", response_model=CommentCreateResponse)
def create_comment(req: CommentCreateRequest):
    # 1. Sanitize and validate post ID
    valid_post_id = sanitize_id(req.post_id)

    # 2. Sanitize user comment text against XSS/scripts/injections
    clean_text = sanitize_comment(req.comment)

    # 3. Validate post exists in code definitions
    post = get_code_post_by_id(valid_post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    # 4. Predict toxicity using the new Final V3 model (threshold = 0.63)
    prediction = predict_toxicity(clean_text)

    if prediction["toxic"]:
        # Blocked: Toxic comment is NOT stored/published anywhere
        return CommentCreateResponse(
            toxic=True,
            probability=prediction["probability"],
            status="blocked",
            message=prediction["message"],
            comment=None
        )

    # Non-toxic: Save approved comment to database
    saved = save_comment_to_firebase(
        post_id=valid_post_id,
        username="You",
        comment_text=clean_text,
        toxicity_probability=prediction["probability"],
        status="approved"
    )

    new_comment = CommentModel(
        id=saved["id"],
        post_id=saved["post_id"],
        username=saved["username"],
        comment_text=saved["comment_text"],
        toxicity_probability=saved["toxicity_probability"],
        status=saved["status"],
        created_at=saved["created_at"]
    )

    return CommentCreateResponse(
        toxic=False,
        probability=prediction["probability"],
        status="approved",
        message="Comment is non-toxic",
        comment=new_comment
    )
