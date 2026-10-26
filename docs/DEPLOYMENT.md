# Deployment & Operations Guide
## Dubai BusinessOne AI — Intelligent Digital Operations Agent

---

## 1. Prerequisites
- **Operating System**: Linux (Ubuntu 22.04+ recommended), macOS, or Windows 11.
- **Python**: Version 3.10+ (tested on Python 3.12).
- **Node.js**: Version 18.0+ (tested on Node.js v24).
- **Docker**: Version 24+ (optional for containerized deployment).

---

## 2. Local Development Quickstart

### 2.1 Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend test suite to verify 100% test pass
python -m pytest tests/ -v

# Start FastAPI development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

### 2.2 Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Next.js development server
npm run dev
```
Access the web application at `http://localhost:3000`.

---

## 3. Production Deployment with Docker Compose
```bash
# Start full stack (FastAPI Backend + Next.js Frontend)
docker compose up -d --build

# Verify container health
docker compose ps
docker compose logs -f
```

---

## 4. Environment Variables Reference
See `.env.example` for the complete list of configurable variables:
- `SECRET_KEY`: Secret string used for signing JWTs and HMAC webhook payloads.
- `DATABASE_URL`: SQLAlchemy connection URI (`sqlite+aiosqlite:///./dubai_businessone.db` or PostgreSQL `postgresql+asyncpg://...`).
- `REDIS_URL`: Optional Redis endpoint for multi-node Layer 1 cache scaling.
- `DEFAULT_LLM_PROVIDER`: Model provider selector (`hybrid`, `vllm`, `gemini`, `rule_deterministic`).
