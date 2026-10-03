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
    prediction: Optional[str] = None
    toxic_probability: Optional[float] = None
    threshold: Optional[float] = None
    model: Optional[str] = None

class PredictRequest(BaseModel):
    text: Optional[str] = Field(None, description="Comment text to analyze")
    comment: Optional[str] = Field(None, description="Alternative field for comment text")

class PredictResponse(BaseModel):
    success: bool = True
    text: str
    prediction: str
    label: int
    toxic_probability: float
    non_toxic_probability: float
    threshold: float = 0.20
    model: str = "ToxicGuard-MuRIL"
    toxic: bool
    probability: float
    status: str
    message: str
