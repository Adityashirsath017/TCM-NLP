import React from 'react';
import { User, CheckCircle2 } from 'lucide-react';

export default function CommentItem({ comment }) {
  const isYou = comment.username === 'You';

  return (
    <div className="comment-item" id={`comment-${comment.id}`}>
      <div className={`comment-avatar ${isYou ? 'user-avatar' : ''}`} aria-hidden="true">
        {isYou ? 'You' : <User size={18} />}
      </div>

      <div className={`comment-bubble ${isYou ? 'user-bubble' : ''}`}>
        <div className="comment-header-row">
          <span className={`comment-username ${isYou ? 'you-badge' : ''}`}>
            {comment.username}
          </span>
          <span className="comment-badge-safe" title="Verified Safe by ML Model">
            <CheckCircle2 size={11} /> Safe
          </span>
        </div>
        <p className="comment-text">{comment.comment_text}</p>
      </div>
    </div>
  );
}
