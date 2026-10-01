import React from 'react';
import CommentItem from './CommentItem';

export default function CommentList({ comments, loading }) {
  if (loading && (!comments || comments.length === 0)) {
    return (
      <div className="comments-list-area">
        <div style={{ textAlign: 'center', padding: '30px 10px', color: 'var(--text-secondary)' }}>
          <div className="spinner" style={{ margin: '0 auto 10px' }} />
          <p style={{ fontSize: '0.85rem' }}>Loading comments...</p>
        </div>
      </div>
    );
  }

  if (!comments || comments.length === 0) {
    return (
      <div className="comments-list-area">
        <p className="empty-comments-state">No comments yet. Be the first to comment!</p>
      </div>
    );
  }

  return (
    <div className="comments-list-area" role="region" aria-label="Comments list">
      {comments.map((comment) => (
        <CommentItem key={comment.id} comment={comment} />
      ))}
    </div>
  );
}
