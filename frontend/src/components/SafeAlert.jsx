import React from 'react';
import { CheckCircle2 } from 'lucide-react';

export default function SafeAlert({ safeCount = 1, lastPrediction = null }) {
  // Logic:
  // 1st non-toxic comment -> Daya Bhabhi
  // 2nd non-toxic comment -> Hathi Bhai
  const isHathiBhai = safeCount % 2 === 0;

  const toxicProb = lastPrediction?.toxic_probability ?? 0.01;
  const toxicPercent = Math.round(toxicProb * 100);

  const meme = isHathiBhai
    ? {
        src: '/images/safe_meme_1.png',
        alt: 'Dr. Hathi: Wonderful comment',
        caption: 'Dr. Hathi: "That\'s right! Wonderful and respectful comment!" 💉😄'
      }
    : {
        src: '/images/safe_daya.png',
        alt: 'Daya Bhabhi: Great comment',
        caption: 'Daya Bhabhi: "Oh wonderful! What a great comment!" 🙏💃'
      };

  return (
    <div className="safe-alert-card" role="status">
      <div className="safe-alert-header">
        <CheckCircle2 size={18} />
        <span>✅ Comment Approved &amp; Posted!</span>
      </div>

      <div style={{
        margin: '10px 0',
        padding: '10px 14px',
        background: '#ECFDF5',
        border: '1px solid #A7F3D0',
        borderRadius: '8px',
        textAlign: 'left'
      }}>
        <div style={{ fontWeight: 700, color: '#047857', fontSize: '0.95rem' }}>
          Result: ✓ Non-Toxic
        </div>
        <div style={{ color: '#374151', fontSize: '0.875rem', marginTop: '4px' }}>
          Toxic Probability: <strong style={{ color: '#047857' }}>{toxicPercent}%</strong>
          <span style={{ fontSize: '0.75rem', color: '#6B7280', marginLeft: '6px' }}>(Threshold: {lastPrediction?.threshold ?? 0.20})</span>
        </div>
      </div>

      <p className="safe-alert-message">
        Your comment is safe and has been published to the feed.
      </p>

      {/* Exactly 1 meme image displayed according to condition */}
      <div className="safe-meme-container">
        <img
          src={meme.src}
          alt={meme.alt}
          className="safe-meme-image"
          loading="eager"
        />
        <div className="safe-meme-punchline">{meme.caption}</div>
      </div>
    </div>
  );
}
