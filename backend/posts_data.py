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
        "default_comments": [
            {"id": 1, "post_id": 1, "username": "Jethalal", "comment_text": "Bhide master, subah subah gyan mat baanto!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T07:05:00Z"},
            {"id": 2, "post_id": 1, "username": "Popatlal", "comment_text": "Duniya hila dunga main Bhide ji!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T07:10:00Z"},
            {"id": 3, "post_id": 1, "username": "Madhavi", "comment_text": "Aaho, achhar papad ka hisab bhi likh lo zara.", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T07:15:00Z"},
            {"id": 4, "post_id": 1, "username": "Taarak", "comment_text": "Gokuldham ke ekmev secretary ka swag hi alag hai.", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T07:20:00Z"}
        ]
    },
    {
        "id": 2,
        "caption": "Jab koi be-tukka gana chalaye: ARREY BAND KARR!! 🛑🙉",
        "image_url": "/images/tmkoc2_bandkar.png",
        "like_count": 389,
        "created_at": "2026-10-01T08:00:00Z",
        "default_comments": [
            {"id": 5, "post_id": 2, "username": "Jethalal", "comment_text": "Bapuji ke samne tezz aawaz karne ka nateeja! 😂", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T08:05:00Z"},
            {"id": 6, "post_id": 2, "username": "Tapu", "comment_text": "Sorry Dadaji, bas gaana enjoy kar rahe the 😅", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T08:10:00Z"},
            {"id": 7, "post_id": 2, "username": "Sodhi", "comment_text": "Oye party sharty band ho gayi balle balle!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T08:15:00Z"}
        ]
    },
    {
        "id": 3,
        "caption": "Jethalal: स्वर्ग से उतरी हुई कोकिल-कंठी अप्सरा लग रही हो ✨😍",
        "image_url": "/images/tmkoc3_apsara.png",
        "like_count": 512,
        "created_at": "2026-10-01T09:00:00Z",
        "default_comments": [
            {"id": 8, "post_id": 3, "username": "BabitaJi", "comment_text": "Thank you Jetha ji, aap hamesha itni tareef karte hain 😊", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T09:05:00Z"},
            {"id": 9, "post_id": 3, "username": "Iyer", "comment_text": "Excuse me Mr. Jethalal, main yahan khada hoon!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T09:10:00Z"},
            {"id": 10, "post_id": 3, "username": "Taarak", "comment_text": "Jetha, thoda control kar bhai! 😂", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T09:15:00Z"}
        ]
    },
    {
        "id": 4,
        "caption": "Daya Ben: Hey Maa Mataji!! Tapu ke papa! 🙏💃",
        "image_url": "/images/tmkoc4_daya.png",
        "like_count": 420,
        "created_at": "2026-10-01T10:00:00Z",
        "default_comments": [
            {"id": 11, "post_id": 4, "username": "Jethalal", "comment_text": "Daya, subah subah non-stop garba shuru mat karo!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T10:05:00Z"},
            {"id": 12, "post_id": 4, "username": "Sundar", "comment_text": "Behna! Ahmedabad se gathiya leke aa raha hoon!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T10:10:00Z"},
            {"id": 13, "post_id": 4, "username": "Komal", "comment_text": "Oh come on, Daya ka garba to hamesha energetic hota hai!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T10:15:00Z"}
        ]
    },
    {
        "id": 5,
        "caption": "Champaklal (Bapuji): Jethiyaaa! Nahane jaa nahane jaa! 👴👓",
        "image_url": "/images/tmkoc5_bapuji.png",
        "like_count": 340,
        "created_at": "2026-10-01T11:00:00Z",
        "default_comments": [
            {"id": 14, "post_id": 5, "username": "Jethalal", "comment_text": "Bapuji bas do minute, abhi gaya nahane!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T11:05:00Z"},
            {"id": 15, "post_id": 5, "username": "Bagha", "comment_text": "Jaisi jiski soch Seth ji!", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T11:10:00Z"},
            {"id": 16, "post_id": 5, "username": "NattuKaka", "comment_text": "Seth ji, humari pagar badhane ki baat chal rahi thi?", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T11:15:00Z"}
        ]
    },
    {
        "id": 6,
        "caption": "Ricky Gervais: This is the photo I want the news channels to use when I die 📸😂",
        "image_url": "/images/post1.png",
        "like_count": 182,
        "created_at": "2026-10-01T12:00:00Z",
        "default_comments": [
            {"id": 17, "post_id": 6, "username": "Alex", "comment_text": "Absolute legend haha! 😂", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T12:05:00Z"},
            {"id": 18, "post_id": 6, "username": "Sam", "comment_text": "News channels: Challenge accepted.", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T12:10:00Z"}
        ]
    },
    {
        "id": 7,
        "caption": "'Did you mean to post that?' Social Media Manager 💀⚰️",
        "image_url": "/images/post2.png",
        "like_count": 145,
        "created_at": "2026-10-01T13:00:00Z",
        "default_comments": [
            {"id": 19, "post_id": 7, "username": "Kabir", "comment_text": "Literally every social media manager's worst nightmare! 😭", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T13:05:00Z"},
            {"id": 20, "post_id": 7, "username": "Liam", "comment_text": "Heart rate went from 0 to 200 bpm.", "toxicity_probability": 0.05, "status": "approved", "created_at": "2026-10-01T13:10:00Z"}
        ]
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
