# Vercel Deployment Guide
## Dubai BusinessOne AI — Intelligent Digital Operations Agent

This repository is optimized for deployment on [Vercel](https://vercel.com) with **zero extra configuration**.

---

## 1. Quick Deploy via Vercel Dashboard (Recommended)

1. **Log in to Vercel**:
   Go to [https://vercel.com/new](https://vercel.com/new).

2. **Import Repository**:
   Select your GitHub repository: `Rupesh4113/Dubai-BusinessOne-AI`.

3. **Configure Project**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Select `frontend` (or leave as root; the included root `vercel.json` will automatically build the `frontend` directory).
   - **Build Command**: `npm run build` (or automatic)
   - **Output Directory**: `.next` (or automatic)

4. **Environment Variables (Optional)**:
   - If you want the frontend to communicate with an external Python FastAPI backend, set:
     `NEXT_PUBLIC_API_URL` = `https://your-backend-domain.com/api/v1`
   - If `NEXT_PUBLIC_API_URL` is omitted, the application uses the included **Vercel Serverless API routes** (`/api/v1/...`), ensuring the entire agent, deterministic calculators, human approval gate, and multilingual chat function **100% self-contained out of the box**!

5. **Click "Deploy"**:
   Vercel will build the Next.js app and provide an instant live URL (e.g., `https://dubai-businessone-ai.vercel.app`).

---

## 2. Deploy via Vercel CLI

If you have the Vercel CLI installed:
```bash
# Navigate to frontend
cd frontend

# Deploy to preview
npx vercel

# Deploy to production
npx vercel --prod
```

---

## 3. Features Live on Vercel

- **Operations Agent Chat**: Natural language business inquiry evaluation, safety checks, and evidence-backed recommendations in 6 languages.
- **Deterministic Calculators**: UAE VAT (5%), UAE Corporate Tax (0% up to 375k, 9% above, SBR), Dubai DET setup fees, and Dubai Chamber membership tariffs.
- **Human Approval Center**: Interactive review and one-click authorization of high-risk actions (e.g. trade name reservation).
- **Invoice Reconciler**: 15-digit UAE FTA TRN format verification and line-item arithmetic audit.
- **Multilingual Support**: English, Arabic (`ar` - RTL), Hindi, Urdu (`ur` - RTL), Filipino, and Malayalam with dynamic bidirectional layouts.
- **Telemetry & Zero-Inference Cache**: Real-time stats on tokens saved and cache hit ratio.
