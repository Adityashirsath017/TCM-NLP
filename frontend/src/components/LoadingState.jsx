import React from 'react';

export default function LoadingState() {
  return (
    <div className="analyzing-box" role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <div>
        <div className="analyzing-title">Analyzing comment...</div>
        <div className="analyzing-subtitle">Checking for toxic content</div>
      </div>
    </div>
  );
}
