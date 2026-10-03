import React, { useEffect, useRef } from 'react';
import { X, CheckCircle2, AlertCircle } from 'lucide-react';
import CommentList from './CommentList';
import CommentInput from './CommentInput';
import ToxicAlert from './ToxicAlert';
import SafeAlert from './SafeAlert';
import LoadingState from './LoadingState';

export default function CommentModal({
  isOpen,
  onClose,
  post,
  comments,
  loadingComments,
  commentText,
  setCommentText,
  onSubmitComment,
  isAnalyzing,
  toxicAlert,
  setToxicAlert,
  toxicCount = 1,
  safeCount = 1,
  lastPrediction = null,
  successMessage,
  errorMessage,
  setErrorMessage
}) {
  const inputRef = useRef(null);

  // Close on Escape key & manage body scroll
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    // Prevent background scrolling
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    // Focus input after opening
    setTimeout(() => {
      inputRef.current?.focus();
    }, 150);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = originalOverflow;
    };
  }, [isOpen, onClose]);

  if (!isOpen || !post) return null;

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleTryAgain = () => {
    setToxicAlert(false);
    setTimeout(() => {
      inputRef.current?.focus();
    }, 50);
  };

  return (
    <div
      className="sheet-overlay"
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="comments-sheet-title"
    >
      <div className="sheet-container">
        {/* Mobile drag handle */}
        <div className="sheet-drag-handle-wrapper" aria-hidden="true">
          <div className="sheet-drag-handle" />
        </div>

        {/* Sheet Header */}
        <div className="sheet-header">
          <div className="sheet-header-left">
            <h2 id="comments-sheet-title" className="sheet-title">Comments</h2>
            <span className="sheet-count">({comments.length})</span>
          </div>

          <button
            type="button"
            className="sheet-close-btn"
            id="close-comments-btn"
            onClick={onClose}
            aria-label="Close comments"
          >
            <X size={20} />
          </button>
        </div>

        {/* Scrollable Comments List */}
        <CommentList
          comments={comments}
          loading={loadingComments}
        />

        {/* Status / Alert Area */}
        <div style={{ padding: '0 16px' }}>
          {isAnalyzing && <LoadingState />}

          {toxicAlert && (
            <ToxicAlert onTryAgain={handleTryAgain} toxicCount={toxicCount} lastPrediction={lastPrediction} />
          )}

          {successMessage && (
            <SafeAlert safeCount={safeCount} lastPrediction={lastPrediction} />
          )}

          {errorMessage && (
            <div className="error-banner" role="alert">
              <AlertCircle size={16} />
              <span>{errorMessage}</span>
            </div>
          )}
        </div>

        {/* Bottom Input Area */}
        <CommentInput
          commentText={commentText}
          onChange={(val) => {
            setCommentText(val);
            if (errorMessage) setErrorMessage('');
          }}
          onSubmit={onSubmitComment}
          isSubmitting={isAnalyzing}
          inputRef={inputRef}
        />
      </div>
    </div>
  );
}
