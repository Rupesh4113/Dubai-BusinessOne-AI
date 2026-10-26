# Streamlit Deployment Guide — Dubai BusinessOne AI

**Dubai BusinessOne AI** is engineered as a unified, production-grade Python application ready for immediate deployment on **Streamlit Community Cloud** (free, 100% managed hosting), Docker containers, or any cloud VM (AWS EC2, Google Cloud Run, Azure Container Apps).

---

## 1. Deploy on Streamlit Community Cloud (Recommended & Free)

Streamlit Community Cloud deploys directly from your GitHub repository in 1 click with automatic SSL and continuous deployment on git push.

### Step-by-Step Instructions:
1. **Log in to Streamlit**:
   Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

2. **Create New App**:
   Click **"Create app"** (or **"New app"**).

3. **Configure Deployment Settings**:
   - **Repository**: `Rupesh4113/Dubai-BusinessOne-AI`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py` (or `app.py`)
   - **App URL**: `dubai-businessone-ai.streamlit.app` (or custom subdomain of choice)

4. **Advanced Settings (Optional Secrets)**:
   Click **Advanced settings...** and specify Python **3.12** or **3.11**.
   Under **Secrets** (TOML format), you can optionally add:
   ```toml
   APP_ENV = "production"
   DEFAULT_TENANT_ID = "tenant_dubai_chamber_01"
   # Optional LLM fallback (Deterministic engine runs with 0 tokens even without keys)
   # OPENAI_API_KEY = "sk-..."
   ```

5. **Deploy**:
   Click **"Deploy!"**.
   Streamlit Cloud will read `requirements.txt`, install dependencies, load the Dubai Chamber Gold theme from `.streamlit/config.toml`, and launch the app in seconds.

---

## 2. Local Development & Testing

To run the Streamlit app locally on your workstation:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Streamlit
streamlit run streamlit_app.py
```

The app will open automatically in your browser at:
`http://localhost:8501`

---

## 3. Docker Deployment

To build and run as a standalone container:

```bash
# Build image
docker build -t dubai-businessone-ai:latest .

# Run container
docker run -p 8501:8501 -e APP_ENV=production dubai-businessone-ai:latest
```

Access the application at `http://localhost:8501`.

---

## 4. Key Features in the Streamlit App

| Module | Capability | Implementation |
|---|---|---|
| **Operations Agent** | Multi-turn chat, prompt injection defense, quick scenarios | `backend/app/agent/orchestrator.py` |
| **Zero-Inference Memory** | Hash-matched L1 cache, token counter, latency metrics | `backend/app/memory/` |
| **Deterministic Calculators** | UAE VAT (5%), Corporate Tax (9%), DET & Chamber fees, invoice reconciliation | `backend/app/calculator/` (Python `Decimal`) |
| **Human Approvals** | High-risk action interceptor & one-click approve/reject gate | `backend/app/agent/approval_gate.py` |
| **Official Regulations** | Searchable UAE Federal Decrees & official portal citations | `backend/app/knowledge/` |
| **Multilingual UI** | English, Arabic (RTL), Hindi, Urdu (RTL), Filipino, Malayalam | Built-in UI dictionary |
