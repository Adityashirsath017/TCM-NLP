import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ToxicAlert({ onTryAgain, toxicCount = 1, lastPrediction = null }) {
  // Logic:
  // 1st Toxic comment -> Jethalal
  // 2nd or repeated toxic comment -> Bapuji
  const isBapuji = toxicCount >= 2;

  const toxicProb = lastPrediction?.toxic_probability ?? 0.95;
  const toxicPercent = Math.round(toxicProb * 100);

  const meme = isBapuji
    ? {
        src: '/images/toxic_meme_1.png',
        alt: 'Bapuji: Keep calm and speak peacefully',
        caption: 'Bapuji: "Keep calm and speak peacefully!" 👴👓',
        warningTag: 'Warning 2: Repeat Toxic Violation'
      }
    : {
        src: '/images/toxic_meme_2.png',
        alt: 'Jethalal: Stop right there',
        caption: 'Jethalal: "Inappropriate language is not permitted here!" 🛑✋',
        warningTag: 'Warning 1: Toxic Comment Blocked'
      };

  return (
    <div className="toxic-alert-card" role="alert">
      <div className="toxic-alert-header">
        <AlertTriangle size={18} />
        <span>⚠️ {meme.warningTag}</span>
      </div>

      <div style={{
        margin: '10px 0',
        padding: '10px 14px',
        background: '#FEF2F2',
        border: '1px solid #FCA5A5',
        borderRadius: '8px',
        textAlign: 'left'
      }}>
        <div style={{ fontWeight: 700, color: '#B91C1C', fontSize: '0.95rem' }}>
          Result: ⚠️ Toxic
        </div>
        <div style={{ color: '#374151', fontSize: '0.875rem', marginTop: '4px' }}>
          Toxic Probability: <strong style={{ color: '#B91C1C' }}>{toxicPercent}%</strong>
          <span style={{ fontSize: '0.75rem', color: '#6B7280', marginLeft: '6px' }}>(Threshold: {lastPrediction?.threshold ?? 0.20})</span>
        </div>
      </div>

      <p className="toxic-alert-message">
        Your comment was detected as toxic and has been blocked.
        <br />
        Please keep the conversation respectful and constructive.
      </p>

      {/* Exactly 1 meme image displayed according to condition */}
      <div className="toxic-meme-container">
        <img
          src={meme.src}
          alt={meme.alt}
          className="toxic-meme-image"
          loading="eager"
        />
        <div className="toxic-meme-punchline">{meme.caption}</div>
      </div>

      <button
        type="button"
        className="toxic-alert-btn"
        id="try-again-btn"
        onClick={onTryAgain}
        aria-label="Try again with a respectful comment"
      >
        <RefreshCw size={14} />
        <span>Try Again</span>
      </button>
    </div>
  );
}
