import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ToxicAlert({ onTryAgain, toxicCount = 1 }) {
  // Logic as requested:
  // 1st Toxic comment -> Jethalal ("Chal chal aave!")
  // Next time agar phir se toxic comment kiya (2nd or repeated) -> Bapuji ("Gandhi Ji Ban Gandhi Ji!")
  const isBapuji = toxicCount >= 2;

  const meme = isBapuji
    ? {
        src: '/images/toxic_meme_1.png',
        alt: 'Bapuji: Gandhi Ji Ban Gandhi Ji',
        caption: 'Bapuji: "Gandhi Ji Ban Gandhi Ji! Shanti se baat karo!" 👴👓',
        warningTag: 'Warning 2: Repeat Toxic Violation'
      }
    : {
        src: '/images/toxic_meme_2.png',
        alt: 'Jethalal: Chal chal aave',
        caption: 'Jethalal: "Chal chal aave! Yahan aisi bhasha nahi chalegi!" 🛑✋',
        warningTag: 'Warning 1: Toxic Comment Blocked'
      };

  return (
    <div className="toxic-alert-card" role="alert">
      <div className="toxic-alert-header">
        <AlertTriangle size={18} />
        <span>⚠️ {meme.warningTag}</span>
      </div>

      <p className="toxic-alert-message">
        Aapka comment toxic paya gaya hai aur block kar diya gaya hai.
        <br />
        Kripya respectful comment likhein.
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
