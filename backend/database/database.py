# Re-export Firebase Realtime Database methods
from .firebase import (
    init_firebase,
    get_posts_list,
    get_post_by_id,
    get_comments_for_post,
    add_comment,
    SEED_POSTS
)
