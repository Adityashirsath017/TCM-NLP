from typing import List
from fastapi import APIRouter, HTTPException, status
from ..database.models import PostModel, CommentModel
from ..posts_data import (
    get_code_posts,
    get_code_post_by_id,
    get_default_comments_for_post
)
from ..database.firebase import (
    get_user_comments_for_post,
    count_user_comments_for_post
)
from ..security import sanitize_id

router = APIRouter(prefix="/api", tags=["Posts"])

@router.get("/posts", response_model=List[PostModel])
def get_posts():
    """
    Retrieve default photo posts directly from code,
    with dynamic comment counts reflecting comments stored in Firebase Realtime Database.
    """
    code_posts = get_code_posts()
    results = []
    for p in code_posts:
        default_count = len(get_default_comments_for_post(p["id"]))
        user_count = count_user_comments_for_post(p["id"])
        results.append(
            PostModel(
                id=p["id"],
                image_url=p["image_url"],
                caption=p["caption"],
                like_count=p["like_count"],
                comment_count=default_count + user_count,
                created_at=p["created_at"]
            )
        )
    return results

@router.get("/posts/{post_id}/comments", response_model=List[CommentModel])
def get_post_comments(post_id: int):
    """
    Retrieve approved comments for a specific post.
    Combines default code comments with approved comments from Firebase Realtime Database.
    """
    valid_id = sanitize_id(post_id)
    post = get_code_post_by_id(valid_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    # 1. Default initial comments directly from code
    default_comments = get_default_comments_for_post(valid_id)

    # 2. Approved user comments stored in Firebase Realtime Database
    user_comments = get_user_comments_for_post(valid_id)

    combined = list(default_comments) + list(user_comments)

    return [
        CommentModel(
            id=c["id"],
            post_id=c["post_id"],
            username=c["username"],
            comment_text=c["comment_text"],
            toxicity_probability=c["toxicity_probability"],
            status=c["status"],
            created_at=c["created_at"]
        )
        for c in combined
    ]
