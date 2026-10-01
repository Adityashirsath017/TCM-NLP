from typing import Optional
from pydantic import BaseModel, Field

class PostModel(BaseModel):
    id: int
    image_url: str
    caption: str
    like_count: int
    comment_count: int
    created_at: str

class CommentModel(BaseModel):
    id: int
    post_id: int
    username: str
    comment_text: str
    toxicity_probability: float
    status: str
    created_at: str

class CommentCreateRequest(BaseModel):
    post_id: int = Field(..., description="Post ID for the comment")
    comment: str = Field(..., description="Comment text to analyze and post")

class CommentCreateResponse(BaseModel):
    toxic: bool
    probability: float
    status: str
    message: str
    comment: Optional[CommentModel] = None

class PredictRequest(BaseModel):
    comment: str = Field(..., description="Comment to analyze for toxicity")

class PredictResponse(BaseModel):
    toxic: bool
    probability: float
    status: str
    message: str
