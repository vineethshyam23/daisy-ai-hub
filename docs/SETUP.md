# Setup Guide

Step-by-step guide to rebuild AI Hub from scratch in a new GCP + Firebase project.

---

## Prerequisites

- GCP account with billing enabled
- Firebase account (linked to same Google account)
- `gcloud` CLI installed and authenticated (`gcloud auth login`)
- `firebase` CLI installed (`npm install -g firebase-tools`)
- Node.js 20+ and Python 3.11+
- Docker (for local container builds)

---

## Step 1 — GCP Project Setup

```bash
# Create a new GCP project
gcloud projects create YOUR_PROJECT_ID --name="AI Hub"
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  artifactregistry.googleapis.com

# Set region (adjust to your preferred region)
gcloud config set compute/region europe-west3
```

---

## Step 2 — Vertex AI Access

The backend calls Gemini via the Vertex AI API. No model deployment is needed — it uses Google's hosted endpoints.

```bash
# Verify Vertex AI is accessible
gcloud ai models list --region=europe-west3
```

If you get a permission error, enable the Vertex AI API and ensure your project has billing enabled.

---

## Step 3 — API Token in Secret Manager

The backend reads a shared Bearer token from Secret Manager at startup. Create it:

```bash
# Generate a random token (keep this — you'll need it in the frontend env too)
TOKEN=$(openssl rand -hex 32)
echo "Your API token: $TOKEN"

# Store in Secret Manager
echo -n "$TOKEN" | gcloud secrets create ai-hub-api-token \
  --data-file=- \
  --replication-policy=automatic
```

The secret name `ai-hub-api-token` matches the default in `backend/config/gcp.yml`. Change it there if you use a different name.

---

## Step 4 — Firebase Project Setup

1. Go to [console.firebase.google.com](https://console.firebase.google.com)
2. Add project → select the same GCP project created in Step 1
3. Enable **Authentication** → Sign-in methods → Email/Password (and optionally Google)
4. Enable **Firestore Database** → Start in production mode → Region: `europe-west3`
5. Register a **Web App** → copy the config object (you'll use it in Step 7)

```bash
# Log in to Firebase CLI
firebase login
firebase use YOUR_PROJECT_ID
```

---

## Step 5 — Backend Local Setup

```bash
cd backend/

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Update config/gcp.yml with your project details
# Or set environment variables (env vars take priority over the yml file):
export GCP_PROJECT=YOUR_PROJECT_ID
export GCP_REGION=europe-west3

# Authenticate locally (uses your personal GCP credentials)
gcloud auth application-default login

# Run locally
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

Verify: `curl http://127.0.0.1:8001/health` should return `{"status": "healthy", "message": "AI Hub Backend is running"}`.

---

## Step 6 — Backend Cloud Run Deployment

```bash
cd backend/

# Create Artifact Registry repository
gcloud artifacts repositories create ai-hub \
  --repository-format=docker \
  --location=europe-west3

# Create a service account for Cloud Run
gcloud iam service-accounts create ai-hub-backend \
  --display-name="AI Hub Backend"

SA="ai-hub-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com"

# Grant required permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:$SA" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:$SA" \
  --role="roles/aiplatform.user"

# Build and push Docker image
gcloud builds submit \
  --tag europe-west3-docker.pkg.dev/YOUR_PROJECT_ID/ai-hub/backend:latest .

# Deploy to Cloud Run
gcloud run deploy ai-hub-backend \
  --image europe-west3-docker.pkg.dev/YOUR_PROJECT_ID/ai-hub/backend:latest \
  --platform managed \
  --region europe-west3 \
  --allow-unauthenticated \
  --service-account $SA \
  --set-env-vars GCP_PROJECT=YOUR_PROJECT_ID,GCP_REGION=europe-west3
```

Note the backend URL printed at the end — you need it for the frontend.

---

## Step 7 — Frontend Local Setup

```bash
cd frontend/

# Install dependencies
npm install

# Create .env file (never commit this)
cat > .env <<EOF
NUXT_PUBLIC_API_BASE_URL=http://localhost:8001
NUXT_PUBLIC_API_TOKEN=YOUR_TOKEN_FROM_STEP_3

# Firebase config (from Firebase console → Project settings → Your apps → Web app)
NUXT_PUBLIC_FIREBASE_DEV_API_KEY=your_firebase_api_key
NUXT_PUBLIC_FIREBASE_DEV_AUTH_DOMAIN=YOUR_PROJECT_ID.firebaseapp.com
NUXT_PUBLIC_FIREBASE_DEV_PROJECT_ID=YOUR_PROJECT_ID
NUXT_PUBLIC_FIREBASE_DEV_STORAGE_BUCKET=YOUR_PROJECT_ID.appspot.com
NUXT_PUBLIC_FIREBASE_DEV_MESSAGING_SENDER_ID=your_sender_id
NUXT_PUBLIC_FIREBASE_DEV_APP_ID=your_app_id

# Optional: restrict registration to specific email domains
# NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS=yourcompany.com,partner.com
# Leave empty to allow any email domain
EOF

# Run dev server
npm run dev
# App available at http://localhost:3000
```

---

## Step 8 — Frontend Cloud Run Deployment

Before deploying, add the frontend Cloud Run URL to the CORS origins in `backend/app.py`, then redeploy the backend.

```bash
cd frontend/

# Build image
gcloud builds submit \
  --tag europe-west3-docker.pkg.dev/YOUR_PROJECT_ID/ai-hub/frontend:latest .

# Deploy to Cloud Run
gcloud run deploy ai-hub-frontend \
  --image europe-west3-docker.pkg.dev/YOUR_PROJECT_ID/ai-hub/frontend:latest \
  --platform managed \
  --region europe-west3 \
  --allow-unauthenticated \
  --set-env-vars \
NUXT_PUBLIC_API_BASE_URL=https://YOUR_BACKEND_CLOUD_RUN_URL,\
NUXT_PUBLIC_API_TOKEN=YOUR_TOKEN_FROM_STEP_3,\
NUXT_PUBLIC_FIREBASE_DEV_API_KEY=your_firebase_api_key,\
NUXT_PUBLIC_FIREBASE_DEV_AUTH_DOMAIN=YOUR_PROJECT_ID.firebaseapp.com,\
NUXT_PUBLIC_FIREBASE_DEV_PROJECT_ID=YOUR_PROJECT_ID,\
NUXT_PUBLIC_FIREBASE_DEV_STORAGE_BUCKET=YOUR_PROJECT_ID.appspot.com,\
NUXT_PUBLIC_FIREBASE_DEV_MESSAGING_SENDER_ID=your_sender_id,\
NUXT_PUBLIC_FIREBASE_DEV_APP_ID=your_app_id
```

---

## Step 9 — Custom Domain (optional)

```bash
# Map a custom domain to the frontend service
gcloud run domain-mappings create \
  --service ai-hub-frontend \
  --domain yourdomain.com \
  --region europe-west3
```

Follow the DNS verification steps that the CLI outputs. After DNS propagation, add `https://yourdomain.com` to the CORS origins in `backend/app.py` and redeploy the backend.

---

## Step 10 — Verify End-to-End

- Open the frontend URL → login page loads
- Register with your email → Firebase Auth user created (check Firebase console)
- Try Email Assistant → submit a sample email → Gemini-generated reply appears
- Try Document Analyzer → upload a PDF → analysis returned
- Backend health check: `curl https://YOUR_BACKEND_URL/health`

---

## Environment Variables Reference

### Backend

| Variable | Required | Description |
|---|---|---|
| `GCP_PROJECT` | Yes | GCP project ID |
| `GCP_REGION` | No | GCP region (default: `europe-west3`) |
| `CAREER_PORTAL_XML_FEED_URL` | No | Personio XML feed base URL for career tools |

Backend also reads `config/gcp.yml` for model names, secret name, and BigQuery settings. Environment variables override the yml file.

### Frontend

| Variable | Required | Description |
|---|---|---|
| `NUXT_PUBLIC_API_BASE_URL` | Yes | Backend Cloud Run URL |
| `NUXT_PUBLIC_API_TOKEN` | Yes | Bearer token (must match Secret Manager value) |
| `NUXT_PUBLIC_FIREBASE_DEV_*` | Yes | Firebase web app config keys |
| `NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS` | No | Comma-separated list of allowed registration domains (empty = allow all) |
| `ENV` | No | `production` or `development` (used for Adobe Analytics) |
