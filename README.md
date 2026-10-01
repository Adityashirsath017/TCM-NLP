# ToxicGuard: Toxic Comment Detection (NLP / ML Project)

A real-time Machine Learning and Natural Language Processing web application that automatically detects toxic or offensive comments on social-style photo posts, approving and publishing safe comments while instantly blocking harmful content.

Designed with a **mobile-first** responsive UI (optimized for 360px, 375px, 390px, 414px mobile devices, tablets, and desktop), backed by **FastAPI** and **Firebase Realtime Database**.

---

## 📌 Architecture & System Flow

```
User View Post ➔ Open Comments (Bottom Sheet)
        ↓
User Writes Comment ("You")
        ↓
Submit Comment ➔ "🔄 Analyzing comment... Checking for toxic content"
        ↓
FastAPI Backend (/api/comments)
        ↓
Text Preprocessing
        ↓
TF-IDF Vectorizer (Word + Character n-grams)
        ↓
Trained Logistic Regression Model (Loaded via joblib at startup)
        ↓
Toxicity Probability Calculation (Threshold: 0.50)
        ↓
   ┌──────────────────────────────────────────────┐
   │                                              │
   ▼                                              ▼
NON-TOXIC (toxic = false)                TOXIC (toxic = true)
   │                                              │
   ▼                                              ▼
Status: Approved                          Status: Blocked
Saved to Firebase Realtime Database       Blocked from Public Feed
Live Comment Displayed in UI              ⚠️ Warning Card Shown
"✅ Comment posted"                       "Please try a respectful comment."
Post Comment Count Incremented            [ Try Again ] Button
```

---

## 🛠️ Technology Stack

- **Frontend:**
  - React 19 + Vite
  - Axios
  - Lucide React Icons
  - Mobile-First Custom Design System (CSS)
- **Backend:**
  - Python
  - FastAPI
  - Uvicorn
  - Scikit-learn
  - Joblib
- **Database:**
  - **Firebase Realtime Database** (with synchronized dual-mode for direct cloud sync via `serviceAccountKey.json` or `FIREBASE_DATABASE_URL`)
- **Machine Learning Pipeline:**
  - Text Normalization & Cleaning
  - TF-IDF Feature Extraction (Word n-grams `(1, 2)` + Character n-grams `(2, 5)`)
  - Logistic Regression Classifier

---

## 📂 Project Structure

```
NLP Project/
├── backend/
│   ├── main.py                     # FastAPI entrypoint & startup lifespan
│   ├── model/
│   │   ├── toxic_comment_model.pkl       # Trained ML classification model
│   │   └── toxic_comment_vectorizer.pkl  # Trained TF-IDF vectorizer
│   ├── model_service.py            # Singleton model loader and predictor
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── posts.py                # GET /api/posts and GET /api/posts/{id}/comments
│   │   ├── comments.py             # POST /api/comments (moderation & posting)
│   │   └── predict.py              # POST /api/predict (raw toxicity check)
│   ├── database/
│   │   ├── __init__.py
│   │   ├── firebase.py             # Firebase Realtime Database client & seeding
│   │   └── models.py               # Pydantic data schemas
│   ├── requirements.txt            # Python dependencies
│   └── serviceAccountKey.json      # (Optional) Firebase service account credentials
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # Sticky header with ToxicGuard branding & AI status
│   │   │   ├── Feed.jsx            # Single-column photo feed
│   │   │   ├── PostCard.jsx        # Post card with image, caption, counts & button
│   │   │   ├── CommentModal.jsx    # Mobile bottom sheet & desktop modal
│   │   │   ├── CommentList.jsx     # Scrollable comments list
│   │   │   ├── CommentItem.jsx     # Individual comment item ("You" / other users)
│   │   │   ├── CommentInput.jsx    # Mobile-friendly input with counter and send button
│   │   │   ├── ToxicAlert.jsx      # Blocked warning card with Try Again button
│   │   │   └── LoadingState.jsx    # "Analyzing comment..." animated spinner
│   │   ├── services/
│   │   │   └── api.js              # Centralized Axios API client
│   │   ├── App.jsx                 # Main state management
│   │   ├── main.jsx
│   │   └── index.css               # Mobile-first design system styles
│   ├── .env                        # VITE_API_URL=http://localhost:8000
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

## 🤖 Pre-Trained Model Files

The pre-trained model files are located inside:
```
backend/model/
    ├── toxic_comment_model.pkl
    └── toxic_comment_vectorizer.pkl
```

These files are loaded **once** when the FastAPI server boots up via `lifespan`, ensuring fast inference times (sub-10ms per comment) without reloading per request.

---

## ☁️ Firebase Realtime Database Configuration

The application uses **Firebase Realtime Database** for storing posts and comments:

1. **Option A (With Service Account Key):**
   - Place your `serviceAccountKey.json` inside `backend/`.
   - Set the environment variable:
     ```bash
     set FIREBASE_DATABASE_URL=https://<your-project>-default-rtdb.firebaseio.com/
     ```

2. **Option B (Direct REST URL):**
   - In your Firebase Console, enable Realtime Database and set rules to read/write.
   - Set:
     ```bash
     set FIREBASE_DATABASE_URL=https://<your-project>-default-rtdb.firebaseio.com/
     ```

3. **Option C (Default Instant Mode):**
   - If no Firebase credentials are provided yet, the backend automatically initializes with a synchronized local store pre-populated with the 5 predefined posts and safe comments, ready to sync whenever Firebase credentials are added.

---

## 🚀 Running the Project

### 1. Start Backend

```bash
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run FastAPI server
uvicorn backend.main:app --reload --port 8000
```
Backend will be available at: `http://localhost:8000`  
Interactive Swagger API docs: `http://localhost:8000/docs`

### 2. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend will be available at: `http://localhost:5173`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Backend and ML model health check |
| `GET` | `/api/posts` | Returns all predefined posts with real-time comment counts |
| `GET` | `/api/posts/{post_id}/comments` | Returns approved comments for a specific post |
| `POST` | `/api/predict` | Runs toxicity prediction on arbitrary comment text |
| `POST` | `/api/comments` | Moderates comment via ML model: approves/stores or blocks |

### Example Request (`POST /api/comments`)

```json
{
  "post_id": 1,
  "comment": "This is a beautiful photo."
}
```

### Approved Response (Safe Comment)

```json
{
  "toxic": false,
  "probability": 0.0847,
  "status": "approved",
  "message": "Comment is non-toxic",
  "comment": {
    "id": 32,
    "post_id": 1,
    "username": "You",
    "comment_text": "This is a beautiful photo.",
    "toxicity_probability": 0.0847,
    "status": "approved",
    "created_at": "2026-10-01T15:02:46Z"
  }
}
```

### Blocked Response (Toxic Comment)

```json
{
  "toxic": true,
  "probability": 0.9371,
  "status": "blocked",
  "message": "Comment contains toxic or offensive language",
  "comment": null
}
```

---

## 📱 Mobile-First Features

- Single-column social feed layout centered on desktop viewports.
- Bottom sheet comments drawer on mobile devices with drag handle.
- Large touch-friendly tap targets (minimum 44px).
- Safe comment publishing under the identity **"You"**.
- Real-time feedback with loading spinner (`Analyzing comment... Checking for toxic content`).
- Non-toxic comments display a green **Safe** badge.
- Toxic comments display an inline alert card with **[ Try Again ]** button without polluting the comments list.
- Empty comments and comments over 500 characters are validated both client-side and server-side.
