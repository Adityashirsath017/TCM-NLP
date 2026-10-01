"""
Default Predefined Photo Posts and Initial Comments.
These are defined directly in the code as requested, without requiring database storage for posts.
"""

DEFAULT_POSTS = [
    {
        "id": 1,
        "caption": "Aatmaram Tukaram Bhide: Kuch na kuch likhna to padega ✍️📋",
        "image_url": "/images/tmkoc1_bhide.png",
        "like_count": 254,
        "created_at": "2026-10-01T07:00:00Z",
        "default_comments": []
    },
    {
        "id": 2,
        "caption": "Jab koi be-tukka gana chalaye: ARREY BAND KARR!! 🛑🙉",
        "image_url": "/images/tmkoc2_bandkar.png",
        "like_count": 389,
        "created_at": "2026-10-01T08:00:00Z",
        "default_comments": []
    },
    {
        "id": 3,
        "caption": "Jethalal: स्वर्ग से उतरी हुई कोकिल-कंठी अप्सरा लग रही हो ✨😍",
        "image_url": "/images/tmkoc3_apsara.png",
        "like_count": 512,
        "created_at": "2026-10-01T09:00:00Z",
        "default_comments": []
    },
    {
        "id": 4,
        "caption": "Daya Ben: Hey Maa Mataji!! Tapu ke papa! 🙏💃",
        "image_url": "/images/tmkoc4_daya.png",
        "like_count": 420,
        "created_at": "2026-10-01T10:00:00Z",
        "default_comments": []
    },
    {
        "id": 5,
        "caption": "Champaklal (Bapuji): Jethiyaaa! Nahane jaa nahane jaa! 👴👓",
        "image_url": "/images/tmkoc5_bapuji.png",
        "like_count": 340,
        "created_at": "2026-10-01T11:00:00Z",
        "default_comments": []
    },
    {
        "id": 6,
        "caption": "Ricky Gervais: This is the photo I want the news channels to use when I die 📸😂",
        "image_url": "/images/post1.png",
        "like_count": 182,
        "created_at": "2026-10-01T12:00:00Z",
        "default_comments": []
    },
    {
        "id": 7,
        "caption": "'Did you mean to post that?' Social Media Manager 💀⚰️",
        "image_url": "/images/post2.png",
        "like_count": 145,
        "created_at": "2026-10-01T13:00:00Z",
        "default_comments": []
    }
]

def get_code_posts():
    """Return predefined posts without exposing internal comments field."""
    return [
        {
            "id": p["id"],
            "caption": p["caption"],
            "image_url": p["image_url"],
            "like_count": p["like_count"],
            "created_at": p["created_at"]
        }
        for p in DEFAULT_POSTS
    ]

def get_code_post_by_id(post_id: int):
    """Retrieve post metadata by ID directly from code."""
    for p in DEFAULT_POSTS:
        if p["id"] == post_id:
            return p
    return None

def get_default_comments_for_post(post_id: int):
    """Retrieve the code-defined initial safe comments for a post."""
    for p in DEFAULT_POSTS:
        if p["id"] == post_id:
            return list(p["default_comments"])
    return []
