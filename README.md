# OfferCopilot

A research-first copilot for job seekers. Uses DuckDuckGo HTML search, Playwright page fetching, and structured analysis to help evaluate company/role fit.

## Structure

- `frontend/` — Next.js app
- `backend/` — FastAPI app
- `OfferCopilotDocs/` — project docs (separate repo)

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on http://localhost:3000

## Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload
```

Runs on http://localhost:8000

## Demo Flow

1. Enter job intent → get company recommendations → select company → add JD → run analysis
2. Or enter company + JD + links + resume directly → run analysis
3. Review structured report with sources
4. Ask follow-up questions
5. If search is weak, use the refine page to add links/JD text
