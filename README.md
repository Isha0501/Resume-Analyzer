# Resume AI | Semantic Matcher

A premium, AI-powered resume analyzer that uses semantic similarity to compare resumes against job descriptions. It provides a match score, identifies missing technical keywords, and offers actionable improvement tips.

## 🚀 Features
- **PDF Upload Support**: Directly upload your PDF resume for analysis.
- **Semantic Matching**: Uses `SentenceTransformers` (all-MiniLM-L6-v2) for context-aware alignment.
- **Balanced Scoring**: A weighted algorithm (70% semantic, 30% keyword) for realistic results.
- **Premium UI**: Modern dark-mode interface with glassmorphism and smooth animations.

## 🛠️ Tech Stack
- **Frontend**: Vanilla HTML5, CSS3, JavaScript.
- **Backend**: FastAPI (Python), PyMuPDF (PDF Parser), SentenceTransformers (NLP).

## 📦 Setup & Installation

### Backend
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the server:
   ```bash
   python3 backend/main.py
   ```

### Frontend
Since the frontend is static, you can serve it with any simple HTTP server:
```bash
python3 -m http.server 3000
```
Then open `http://localhost:3000` in your browser.

## 🌐 Deployment to GitHub Pages
1. Push this repository to GitHub.
2. Go to **Settings > Pages**.
3. Set the source to **Deploy from a branch**.
4. Select the `main` branch and the `/ (root)` folder (or `/frontend` if you kept them separated).

> [!NOTE]
> Ensure the `API_URL` in `frontend/script.js` is updated to point to your live backend server once deployed.
