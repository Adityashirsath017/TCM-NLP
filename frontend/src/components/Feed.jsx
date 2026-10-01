import React from 'react';
import PostCard from './PostCard';

export default function Feed({ posts, loading, error, onOpenComments, onRetry }) {
  if (loading && (!posts || posts.length === 0)) {
    return (
      <main className="feed-container">
        <div style={{ textAlign: 'center', padding: '40px 10px', color: 'var(--text-secondary)' }}>
          <div className="spinner" style={{ margin: '0 auto 12px' }} />
          <p>Loading posts...</p>
        </div>
      </main>
    );
  }

  if (error && (!posts || posts.length === 0)) {
    return (
      <main className="feed-container">
        <div style={{ textAlign: 'center', padding: '40px 10px', color: '#EF4444' }}>
          <p style={{ marginBottom: '12px' }}>⚠️ Unable to load posts.</p>
          <button
            type="button"
            className="view-comments-btn"
            style={{ maxWidth: '200px', margin: '0 auto' }}
            onClick={onRetry}
          >
            Try Again
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="feed-container" role="feed" aria-label="Photo posts feed">
      {posts.map((post) => (
        <PostCard
          key={post.id}
          post={post}
          onOpenComments={onOpenComments}
        />
      ))}
    </main>
  );
}
