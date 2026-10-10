# SurakshaScan 🛡️

AI-powered scam/fraud message detector for English, Hindi, and Telugu —
built for HackNowa Global Hackathon 2026 (Digital Safety & Cybersecurity).

**Live demo:** https://surakshascan-umber.vercel.app
**Backend API:** https://surakshascan.onrender.com

Paste a suspicious SMS, WhatsApp message, or email and get an instant risk
score, the scam category it matches, a plain-language explanation, and a
concrete next step — grounded in real Indian fraud patterns (UPI collect
fraud, fake KYC messages, courier/customs scams, lottery scams, job scams,
"digital arrest" scams, fake account-suspension phishing).

## Why this matters
Digital fraud costs Indians thousands of crores every year, and most
victims — especially less tech-literate users — have no fast way to check
whether a message is real. Existing spam filters don't explain *why*
something is dangerous or *what to do next*, and almost none of them work
in Hindi or Telugu, despite a huge share of scam SMS traffic in India not
being in English at all.

## Features
- **Trilingual detection** — English, Hindi, and Telugu, with automatic
  language detection (script-range + fallback) on the input message
- **Hybrid detection pipeline** — fast rule-based heuristics (regex/keyword
  pattern banks per language) combined with an LLM reasoning layer for
  context the heuristics alone would miss
- **7 real scam categories** — UPI fraud, fake KYC/bank update, courier/
  customs scam, lottery/prize scam, job scam, digital arrest scam, and
  fake account-suspension phishing
- **Trilingual UI** — the interface itself (not just detection) toggles
  between EN / हिं / తె
- **Plain-language results** — risk score, category, a 2-3 sentence
  explanation, and one concrete recommended action, in the same language
  as the message being checked
- **Share / copy report** — formatted for WhatsApp/Telegram, with native
  share-sheet support on mobile
- **Rate limiting** — per-IP throttling on the API to protect the shared
  free-tier LLM quota from being exhausted by any single burst of traffic
- **Privacy-first** — messages are analyzed instantly and never stored

## Accuracy
Evaluated against 380 real labeled messages pulled from public datasets
(not synthetic/invented examples) covering English, Hindi, and Hinglish
scam/spam/legitimate messages:
- **91.3% overall accuracy** (347/380)
- Most remaining "misses" are legitimate promotional marketing (e.g. real
  telecom/e-commerce sale SMS) that some source datasets label as "scam"
  under a broader spam definition — SurakshaScan is scoped to actual
  fraud/safety risk, not general spam filtering, so correctly not-flagging
  those is intentional, not an error
- False positives on routine bank transaction alerts (a very common,
  high-stakes message type in India) were specifically tuned down, since
  false alarms on everyday bank SMS would undermine user trust fastest

## Project structure
```
surakshascan/
├── backend/          FastAPI app (layered: routes -> services -> providers)
│   ├── app/
│   │   ├── routes/          API endpoints (rate-limited)
│   │   ├── services/        detection pipeline, language detection, rate limiter
│   │   │   └── heuristics/  per-language Strategy pattern (en/hi/te)
│   │   ├── providers/       LLM provider (Factory pattern, Groq by default)
│   │   └── models/          Pydantic request/response schemas
│   ├── data/                 dataset inspection, test-set builder, eval scripts
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env.example
└── frontend/         React (Vite) + Tailwind CSS v4
    ├── src/
    │   ├── App.jsx               container component (state + API call)
    │   ├── i18n.js                EN/HI/TE UI translations
    │   └── components/           presentational components
    └── vercel.json
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

Groq hosts open-source models (currently `openai/gpt-oss-120b`) and has a
generous free tier with very fast inference.

## Deployment
- **Backend:** Render (see `backend/render.yaml`) — free tier spins down
  after ~15 min idle; first request after that can take 30-50s to wake up
- **Frontend:** Vercel, auto-deploys on push
- Both auto-deploy from the connected GitHub repo — no manual deploy step
  needed after the initial setup : https://github.com/Eshwarprasad-code/surakshascan

## Status: feature-complete, in final submission prep
- [x] Backend: FastAPI, layered architecture, CORS, rate limiting
- [x] Language detection (English/Hindi/Telugu)
- [x] Heuristic engine: 7 categories × 3 languages
- [x] LLM provider (Groq), with retry/backoff on rate limits
- [x] Detection pipeline, tuned against 380 real labeled messages (91.3%
      accuracy)
- [x] Frontend: input, results, example chips, loading/error states,
      trilingual UI toggle, share/copy
- [x] Live deployment (Render + Vercel)
- [x] Rate limiting to protect the shared LLM quota
- [x] Demo video
- [x] Final submission writeup

## Known limitations / honest caveats
- The heuristic keyword banks are a solid starting point, not an
  exhaustive list — built from a mix of hand-curated patterns and public
  dataset analysis, not a fully comprehensive scam-phrase database
- Telugu coverage in the underlying training/test data is thinner than
  English or Hindi, reflecting the general scarcity of public Telugu scam
  datasets — detection still works via the LLM's own language capability,
  but has had less real-world-example tuning than English/Hindi
- Free-tier hosting means a cold-start delay after idle periods (see
  Deployment above) — the UI shows a "waking up" message after ~8 seconds
  to set expectations rather than looking frozen