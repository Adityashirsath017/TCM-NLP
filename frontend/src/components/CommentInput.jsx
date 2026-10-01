import React from 'react';
import { Send } from 'lucide-react';

export default function CommentInput({
  commentText,
  onChange,
  onSubmit,
  isSubmitting,
  inputRef
}) {
  const trimmed = commentText.trim();
  const isEmpty = trimmed.length === 0;
  const isTooLong = commentText.length > 500;
  const charsRemaining = 500 - commentText.length;

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isEmpty && !isTooLong && !isSubmitting) {
        onSubmit(e);
      }
    }
  };

  return (
    <div className="comment-input-area">
      <div className="input-character-hint">
        <span>Respectful comments only</span>
        <span style={{ color: charsRemaining < 30 ? '#EF4444' : 'inherit' }}>
          {commentText.length}/500
        </span>
      </div>

      <form className="input-form" onSubmit={onSubmit}>
        <input
          ref={inputRef}
          type="text"
          id="comment-input-field"
          value={commentText}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Write a comment..."
          maxLength={500}
          disabled={isSubmitting}
          className="comment-text-input"
          aria-label="Write a comment"
          autoComplete="off"
        />

        <button
          type="submit"
          id="send-comment-btn"
          disabled={isEmpty || isTooLong || isSubmitting}
          className="send-comment-btn"
          aria-label="Send comment"
          title={isEmpty ? "Enter a comment" : "Post comment"}
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
