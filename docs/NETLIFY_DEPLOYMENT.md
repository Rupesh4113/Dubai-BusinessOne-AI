# Netlify Deployment Guide — Dubai BusinessOne AI

**Dubai BusinessOne AI** is pre-configured for direct, zero-friction deployment on **[Netlify](https://www.netlify.com)** using the official Next.js 14 Runtime (`@netlify/plugin-nextjs`).

All deterministic calculations, official citations, 4-tier memory models, and multilingual interfaces (English, Arabic, Hindi, Urdu, Filipino, Malayalam) are served through standalone Next.js serverless route handlers on Netlify's high-performance edge network.

---

## 1. Quick Deploy via Netlify Web UI (Recommended)

1. **Log in to Netlify**:
   Go to [app.netlify.com](https://app.netlify.com) and sign in with GitHub.

2. **Import Project**:
   Click **"Add new site"** → **"Import an existing project"** → Select **GitHub**.

3. **Select Repository**:
   Choose `Rupesh4113/Dubai-BusinessOne-AI`.

4. **Verify Build Configuration**:
   The included [`netlify.toml`](../netlify.toml) automatically pre-fills all required settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
   - **Node.js Version**: `20` (configured via `NODE_VERSION = "20"`)

5. **Deploy Site**:
   Click **"Deploy Dubai-BusinessOne-AI"**.
   Netlify will build the Next.js app, package serverless functions, and generate a live URL (e.g. `https://dubai-businessone-ai.netlify.app`).

---

## 2. Deploy via Netlify CLI

If you prefer using the command line:

```bash
# 1. Install Netlify CLI
npm install -g netlify-cli

# 2. Authenticate
netlify login

# 3. Deploy from the repository root
netlify deploy --build --prod
```

---

## 3. Configuration Details

### Repository `netlify.toml`
Located at the root of the repository:
```toml
[build]
  base = "frontend"
  publish = ".next"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "20"
  NPM_FLAGS = "--legacy-peer-deps"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Optional Environment Variables
In **Site configuration** → **Environment variables**:
- `BACKEND_URL` *(Optional)*: If you are running the FastAPI backend on an external service (e.g., Render, Railway, AWS), set `BACKEND_URL` to route requests there. If left unset, the application runs **100% self-contained** using the built-in Next.js serverless route handlers.

---

## 4. Features Live on Netlify

| Feature | Description | Architecture |
|---|---|---|
| **Operations Agent** | Conversational business AI with prompt injection defense | Serverless Route Handler (`/api/v1/agent/chat`) |
| **Deterministic Calculators** | UAE VAT (5%), Corporate Tax (9%), DET & Chamber Fees | Route Handlers (`/api/v1/calculate/...`) |
| **Human Approvals** | High-risk action interceptor and review queue | Route Handlers (`/api/v1/approvals/...`) |
| **Legal Knowledge Base** | Full-text verified search of UAE Federal & Dubai decrees | Route Handlers (`/api/v1/knowledge/...`) |
| **Multilingual UI (6 Languages)** | Instant translation with full RTL support (Arabic, Urdu) | Client-side reactive i18n engine |
