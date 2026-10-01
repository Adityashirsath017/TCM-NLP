import React from 'react';

export default function Header() {
  return (
    <header className="header-container" role="banner">
      <div className="header-brand">
        <div className="header-title-row">
          <span className="header-icon" aria-hidden="true">🛡️</span>
          <h1 className="header-title">ToxicGuard</h1>
        </div>
        <p className="header-subtitle">Safe &amp; Respectful Comments</p>
      </div>
      <div className="header-badge" title="AI Toxicity Protection Active">
        <span className="header-badge-dot" aria-hidden="true"></span>
        <span>AI Protected</span>
      </div>
    </header>
  );
}
