# SurakshaScan

AI-powered scam/fraud message detector for English, Hindi, and Telugu —
built for HackNowa Global Hackathon 2026 (Digital Safety & Cybersecurity).

Paste a suspicious SMS, WhatsApp message, or email and get an instant risk
score, the scam category it matches, a plain-language explanation, and a
concrete next step — grounded in real Indian fraud patterns (UPI collect
fraud, fake KYC messages, courier/customs scams, lottery scams, job scams,
"digital arrest" scams).

Full PRD, architecture, and the 13-day build plan: see the project blueprint
(shared separately) or `/docs` once you copy it in.

## Project structure
```
surakshascan/
├── backend/          FastAPI app (layered: routes -> services -> providers)
│   ├── app/
│   │   ├── routes/          API endpoints
│   │   ├── services/        detection pipeline + language detection
│   │   │   └── heuristics/  per-language Strategy pattern (en/hi/te)
│   │   ├── providers/       LLM provider (Factory pattern, Groq by default)
│   │   └── models/          Pydantic request/response schemas
│   ├── requirements.txt
│   └── .env.example
└── frontend/         React (Vite) + Tailwind CSS v4
    └── src/
        ├── App.jsx               container component (state + API call)
        └── components/           presentational components
```

## Backend setup
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and paste your free Groq API key (https://console.groq.com)
uvicorn app.main:app --reload
```
Runs at `http://localhost:8000`. Check `http://localhost:8000/health`.

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:5173` and proxies `/api/*` to the backend
(see `vite.config.js`) — no CORS setup needed in local dev.

## Getting a free Groq API key
1. Sign up at https://console.groq.com (free, no credit card)
2. Create an API key
3. Paste it into `backend/.env` as `GROQ_API_KEY`

Groq hosts open-source models (Llama 3.3 etc.) and has a generous free tier
with very fast inference — good for the "under 5 seconds per analysis"
requirement.

## Current status (Phase 0-2 of the build plan)
- [x] Backend skeleton: FastAPI app, layered architecture, CORS configured
- [x] Language detection (English/Hindi/Telugu, with script-range fallback
      for short/code-mixed text)
- [x] Heuristic engine: Strategy pattern per language, starter keyword banks
      for 6 scam categories (UPI fraud, fake KYC, courier scam, lottery
      scam, job scam, digital arrest scam)
- [x] LLM provider: Factory pattern, Groq implementation wired up (needs a
      real API key to actually call it — not tested live in this
      environment since it has no network access to groq.com)
- [x] Detection pipeline wiring all of the above together
- [x] Frontend: input box, result card with risk score bar, copy-report
      button, mobile-responsive layout, Tailwind styling
- [ ] Phase 1: expand the starter keyword banks with real scraped examples
      from cybercrime.gov.in / RBI advisories / news coverage — the current
      banks are a reasonable starting point, not the final data set
- [ ] Phase 5: end-to-end testing against a real sample set once you have a
      live Groq key
- [ ] Phase 6: deployment (Render for backend, Vercel for frontend)
- [ ] Phase 7: demo video + submission materials

## Notes / things to verify once you have your Groq key
- Confirm the model name in `.env` (`GROQ_MODEL`) is still current — Groq
  occasionally renames/deprecates free-tier models, worth checking
  https://console.groq.com/docs/models before Phase 5 testing.
- The LLM is asked to reply in the same language as the input message —
  test this with real Hindi/Telugu samples and adjust the prompt in
  `app/providers/llm_provider.py` if it doesn't hold consistently.
