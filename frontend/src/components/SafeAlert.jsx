import React from 'react';
import { CheckCircle2 } from 'lucide-react';

export default function SafeAlert({ safeCount = 1 }) {
  // Logic as requested:
  // 1st non-toxic comment -> Daya Bhabhi ("Hey Maa Mataji!")
  // 2nd non-toxic comment -> Hathi Bhai ("Sahi baat hai!")
  // Subsequent comments cycle: Daya Bhabhi -> Hathi Bhai -> Daya Bhabhi...
  const isHathiBhai = safeCount % 2 === 0;

  const meme = isHathiBhai
    ? {
        src: '/images/safe_meme_1.png',
        alt: 'Dr. Hathi: Sahi baat hai',
        caption: 'Dr. Hathi: "Sahi baat hai! Ekdum badhiya comment!" 💉😄'
      }
    : {
        src: '/images/safe_daya.png',
        alt: 'Daya Bhabhi: Hey Maa Mataji',
        caption: 'Daya Bhabhi: "Hey Maa Mataji! Tapu ke papa dekho kitna sundar comment kiya hai!" 🙏💃'
      };

  return (
    <div className="safe-alert-card" role="status">
      <div className="safe-alert-header">
        <CheckCircle2 size={18} />
        <span>✅ Comment Approved & Posted!</span>
      </div>

      <p className="safe-alert-message">
        Aapka comment safe paya gaya aur feed mein publish ho chuka hai.
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
