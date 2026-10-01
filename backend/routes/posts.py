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
    get_all_approved_comments
)
from ..security import sanitize_id

router = APIRouter(prefix="/api", tags=["Posts"])

@router.get("/posts", response_model=List[PostModel])
def get_posts():
    """
    Retrieve photo posts directly from code,
    with dynamic comment counts reflecting ONLY live comments in Firebase Realtime Database.
    """
    code_posts = get_code_posts()
    comments_by_post = get_all_approved_comments()
    results = []
    for p in code_posts:
        count = len(comments_by_post.get(p["id"], []))
        results.append(
            PostModel(
                id=p["id"],
                image_url=p["image_url"],
                caption=p["caption"],
                like_count=p["like_count"],
                comment_count=count,
                created_at=p["created_at"]
            )
        )
    return results

@router.get("/posts/{post_id}/comments", response_model=List[CommentModel])
def get_post_comments(post_id: int):
    """
    Retrieve approved comments for a specific post directly from Firebase Realtime Database.
    If comments are deleted from the database, they will NOT appear here.
    """
    valid_id = sanitize_id(post_id)
    post = get_code_post_by_id(valid_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    # Fetch approved user comments stored in Firebase Realtime Database ONLY
    user_comments = get_user_comments_for_post(valid_id)

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
        for c in user_comments
    ]
