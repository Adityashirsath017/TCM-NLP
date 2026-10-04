import React, { useRef, useState, useEffect, useCallback } from 'react';
import { ChevronLeft, ChevronRight, ChevronUp, Sparkles } from 'lucide-react';
import PostCard from './PostCard';

export default function Feed({
  posts = [],
  loading,
  error,
  onOpenComments,
  onRetry,
  isModalOpen = false,
  currentIndex = 0,
  setCurrentIndex
}) {
  const containerRef = useRef(null);
  const touchStart = useRef({ x: 0, y: 0, time: 0 });
  const touchEnd = useRef({ x: 0, y: 0 });
  const isPointerDown = useRef(false);
  const pointerStart = useRef({ x: 0, y: 0 });
  const lastWheelTrigger = useRef(0);

  const safeIndex = Math.min(Math.max(0, currentIndex), Math.max(0, posts.length - 1));

  const goToNext = useCallback(() => {
    if (safeIndex < posts.length - 1 && setCurrentIndex) {
      setCurrentIndex((prev) => Math.min(prev + 1, posts.length - 1));
    }
  }, [safeIndex, posts.length, setCurrentIndex]);

  const goToPrev = useCallback(() => {
    if (safeIndex > 0 && setCurrentIndex) {
      setCurrentIndex((prev) => Math.max(prev - 1, 0));
    }
  }, [safeIndex, setCurrentIndex]);

  // Keyboard navigation: Left/Right arrows change posts, Up arrow opens comments
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (isModalOpen || !posts.length) return;
      if (e.key === 'ArrowRight') {
        goToNext();
      } else if (e.key === 'ArrowLeft') {
        goToPrev();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        onOpenComments(posts[safeIndex]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isModalOpen, safeIndex, posts, goToNext, goToPrev, onOpenComments]);

  // Touch handlers for mobile swipe
  const handleTouchStart = (e) => {
    if (isModalOpen) return;
    touchStart.current = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY,
      time: Date.now()
    };
    touchEnd.current = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY
    };
  };

  const handleTouchMove = (e) => {
    if (isModalOpen) return;
    touchEnd.current = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY
    };
  };

  const handleTouchEnd = () => {
    if (isModalOpen || !posts.length) return;
    const deltaX = touchEnd.current.x - touchStart.current.x;
    const deltaY = touchEnd.current.y - touchStart.current.y;
    const absX = Math.abs(deltaX);
    const absY = Math.abs(deltaY);

    // 1. Vertical swipe up gesture (deltaY < -45) -> open comment box!
    if (deltaY < -45 && absY > absX * 0.7) {
      onOpenComments(posts[safeIndex]);
      return;
    }

    // 2. Horizontal swipe gesture
    if (absX > 40 && absX > absY) {
      if (deltaX < 0) {
        // Swiped Right-to-Left -> NEXT post
        goToNext();
      } else {
        // Swiped Left-to-Right -> PREVIOUS post
        goToPrev();
      }
    }
  };

  // Mouse drag handlers for desktop users
  const handleMouseDown = (e) => {
    if (isModalOpen) return;
    // Don't drag if clicking buttons or links
    if (e.target.closest('button')) return;
    isPointerDown.current = true;
    pointerStart.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseUp = (e) => {
    if (!isPointerDown.current || isModalOpen || !posts.length) return;
    isPointerDown.current = false;
    const deltaX = e.clientX - pointerStart.current.x;
    const deltaY = e.clientY - pointerStart.current.y;
    const absX = Math.abs(deltaX);
    const absY = Math.abs(deltaY);

    // Upward drag -> open comments
    if (deltaY < -40 && absY > absX * 0.7) {
      onOpenComments(posts[safeIndex]);
      return;
    }

    // Horizontal drag -> change post
    if (absX > 45 && absX > absY) {
      if (deltaX < 0) {
        goToNext();
      } else {
        goToPrev();
      }
    }
  };

  // Mouse wheel handler: scroll up or down
  const handleWheel = (e) => {
    if (isModalOpen || !posts.length) return;
    const now = Date.now();
    if (now - lastWheelTrigger.current < 450) return; // Debounce

    // Vertical wheel: scrolling down/upwards triggers comment box
    if (Math.abs(e.deltaY) > 30 && Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      if (e.deltaY > 0) {
        // Scrolled down (finger moving up) -> open comment drawer!
        lastWheelTrigger.current = now;
        onOpenComments(posts[safeIndex]);
      }
    } else if (Math.abs(e.deltaX) > 30) {
      // Horizontal trackpad wheel
      lastWheelTrigger.current = now;
      if (e.deltaX > 0) {
        goToNext();
      } else {
        goToPrev();
      }
    }
  };

  if (loading && (!posts || posts.length === 0)) {
    return (
      <main className="feed-container">
        <div style={{ textAlign: 'center', padding: '60px 10px', color: 'var(--text-secondary)' }}>
          <div className="spinner" style={{ margin: '0 auto 12px' }} />
          <p>Loading posts...</p>
        </div>
      </main>
    );
  }

  if (error && (!posts || posts.length === 0)) {
    return (
      <main className="feed-container">
        <div style={{ textAlign: 'center', padding: '60px 10px', color: '#EF4444' }}>
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
    <main
      className="feed-container"
      ref={containerRef}
      role="feed"
      aria-label="Swipeable photo posts feed"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onWheel={handleWheel}
    >
      {/* Top Story-style Indicator Bar */}
      <div className="feed-story-indicators" aria-label="Post navigation indicators">
        {posts.map((p, idx) => (
          <div
            key={p.id}
            className={`feed-story-dot ${idx === safeIndex ? 'active' : ''}`}
            onClick={() => setCurrentIndex && setCurrentIndex(idx)}
            title={`Go to post ${idx + 1}`}
          />
        ))}
      </div>

      <div className="feed-top-status">
        <span className="feed-post-counter">
          Post {safeIndex + 1} of {posts.length}
        </span>
        <span className="feed-swipe-badge">
          Swipe ◀ ▶ for posts
        </span>
      </div>

      {/* Horizontal Carousel Viewport */}
      <div className="carousel-viewport">
        <div
          className="carousel-track"
          style={{
            transform: `translateX(-${safeIndex * 100}%)`,
            transition: 'transform 0.38s cubic-bezier(0.2, 0.9, 0.3, 1)'
          }}
        >
          {posts.map((post, idx) => (
            <div key={post.id} className="carousel-slide" aria-hidden={idx !== safeIndex}>
              <PostCard
                post={post}
                isActive={idx === safeIndex}
                onOpenComments={onOpenComments}
              />
            </div>
          ))}
        </div>

        {/* Desktop Left / Right Navigation Chevrons */}
        {safeIndex > 0 && (
          <button
            type="button"
            className="carousel-nav-btn prev-btn"
            onClick={goToPrev}
            aria-label="Previous post (Swipe Right)"
          >
            <ChevronLeft size={24} />
          </button>
        )}

        {safeIndex < posts.length - 1 && (
          <button
            type="button"
            className="carousel-nav-btn next-btn"
            onClick={goToNext}
            aria-label="Next post (Swipe Left)"
          >
            <ChevronRight size={24} />
          </button>
        )}
      </div>

      {/* Bottom Swipe-Up Prompt Banner */}
      <div className="feed-bottom-hint">
        <button
          type="button"
          className="swipe-up-trigger-pill"
          onClick={() => onOpenComments(posts[safeIndex])}
          aria-label="Swipe up or click to open comments"
        >
          <ChevronUp size={16} className="bounce-chevron" />
          <span>Swipe up or click for comments</span>
          <span className="hint-comment-bubble">
            💬 {posts[safeIndex]?.comment_count ?? 0}
          </span>
        </button>
      </div>
    </main>
  );
}
