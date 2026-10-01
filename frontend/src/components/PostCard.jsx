import React from 'react';
import { Heart, MessageCircle } from 'lucide-react';

export default function PostCard({ post, onOpenComments }) {
  return (
    <article className="post-card" id={`post-${post.id}`}>
      <div className="post-image-wrapper">
        <img
          src={post.image_url}
          alt={post.caption}
          className="post-image"
          loading="lazy"
        />
      </div>

      <div className="post-content">
        <p className="post-caption">{post.caption}</p>

        <div className="post-metrics-row">
          <div className="post-metric-item" aria-label={`${post.like_count} likes`}>
            <Heart className="post-metric-icon heart" fill="#F43F5E" />
            <span>{post.like_count}</span>
          </div>

          <div className="post-metric-item" aria-label={`${post.comment_count} comments`}>
            <MessageCircle className="post-metric-icon" />
            <span>{post.comment_count}</span>
          </div>
        </div>

        <button
          type="button"
          className="view-comments-btn"
          id={`view-comments-btn-${post.id}`}
          onClick={() => onOpenComments(post)}
          aria-label={`View comments for ${post.caption}`}
        >
          <MessageCircle size={16} />
          <span>View Comments</span>
        </button>
      </div>
    </article>
  );
}
