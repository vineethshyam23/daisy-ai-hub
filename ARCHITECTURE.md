# Architecture

## System Diagram

```mermaid
graph TB
    subgraph Client
        Browser["Browser"]
    end

    subgraph Firebase
        FirebaseAuth["Firebase Auth\n(Email/Password + Google OAuth)"]
        Firestore["Firestore\n(session/chat history)"]
    end

    subgraph CloudRun["GCP Cloud Run"]
        Frontend["Nuxt 3 Frontend\n(SSR off, served as SPA)"]
        Backend["FastAPI Backend\n(Python 3.11)"]
    end

    subgraph VertexAI["GCP Vertex AI"]
        Gemini["Gemini 2.5 Flash Lite\n(text + multi-modal)"]
        Imagen["Imagen 4\n(image generation)"]
    end

    subgraph GCPServices["GCP Platform Services"]
        SecretManager["Secret Manager\n(API token)"]
        ArtifactRegistry["Artifact Registry\n(Docker images)"]
        CloudBuild["Cloud Build\n(CI/CD)"]
    end

    Browser -->|"1. Firebase ID token (login)"| FirebaseAuth
    Browser -->|"2. HTTPS requests"| Frontend
    Frontend -->|"3. Bearer token + payload"| Backend
    Backend -->|"4. Token validation at startup"| SecretManager
    Backend -->|"5. AI inference"| Gemini
    Backend -->|"6. Image generation"| Imagen
    Frontend -->|"7. Chat history"| Firestore
    CloudBuild -->|"Build + push"| ArtifactRegistry
    ArtifactRegistry -->|"Deploy"| Frontend
    ArtifactRegistry -->|"Deploy"| Backend
```

## Component Breakdown

### Frontend (Nuxt 3)

- **SPA mode** (`ssr: false`): entire app rendered client-side, deployed to Cloud Run as a Node.js container
- **Firebase Auth**: handles login/register/OAuth; ID token stored in Pinia `auth` store
- **Pinia stores**: `auth` (user, token, roles), `roles` (admin/user permissions)
- **Composables**: `useAuth`, `useAdobeTracking` (Adobe Analytics DataLayer integration)
- **Pages**: `/ai/*` for tools, `/search/*` for internal knowledge search, `/admin/*` for user management
- **API calls**: every backend request carries a Bearer token (read from `nuxt.config.ts` runtimeConfig, injected at deploy)

### Backend (FastAPI)

- **Auth middleware**: reads API token from Secret Manager **once at startup**, validates incoming `Authorization: Bearer` headers on every protected route
- **Router per domain**: `email`, `shopping`, `images`, `social_media`, `career`, `productivity`, `llm`, `invoice_validator`
- **Service layer**: business logic lives in `services/`, routes stay thin
- **LLM module** (`modules/llm.py`): wraps `google-cloud-aiplatform`, handles `vertexai.init()`, text prediction, and multi-modal document assembly
- **Config**: `config/gcp.yml` for GCP/model settings, `config/prompt.yml` for all LLM prompt templates, `config/para.py` for hardware product code mapping (invoice tool)

### Auth Flow

```
User → Firebase (login) → ID token (browser only)
                                    ↓
Frontend → Backend Bearer token (from Secret Manager via nuxt.config runtimeConfig)
                                    ↓
Backend startup → Secret Manager → token cached in memory → validate on each request
```

The frontend Bearer token and Firebase ID token are separate concerns:
- Firebase ID token: identifies the user to Firebase/Firestore
- Backend Bearer token: a shared secret that authenticates the frontend service to the backend API (not per-user)

This is intentional — the backend is a service-to-service call, not a user-impersonation pattern. Per-user quota tracking was tracked separately in BigQuery (optional, see `gcp.yml`).

### Deployment

Both services deploy to Cloud Run via Cloud Build:

1. `git push` to main triggers Cloud Build pipeline
2. Cloud Build runs `docker build` and pushes to Artifact Registry
3. Cloud Run pulls the new image and deploys with zero-downtime traffic migration

Environment variables are injected at Cloud Run deploy time (not baked into the image). Firebase config, GCP project ID, and the API token name are all passed as `--set-env-vars` flags.

## Design Decisions

Frontend and backend are separate repos deploying to separate Cloud Run services. This wasn't a strong architectural opinion — it was practical. Frontend changes were iterative and fast, backend changes were slower and involved model config. Coupling the deploys would have meant every CSS tweak waiting on a backend image build. The downside is two Dockerfiles, two CI pipelines, and two sets of env vars to manage. At this team size that's fine.

Secret Manager for the API token was about rotation. An env var baked into the Cloud Run config means a redeploy to rotate. Secret Manager means update the secret, restart the instance. For an internal tool that might be a 2am decision if something leaks, that matters.

Pinia over Vuex: Nuxt 3 is Pinia-native and the TypeScript support is significantly cleaner. No real tradeoffs at this scale.

The backend doesn't verify Firebase ID tokens — it only checks a shared Bearer token. Someone will read this and think it's a security hole. It's not for a service-to-service pattern at this scale: the frontend is the authenticated surface, Firebase handles that, and the backend just needs to know the request came from the frontend, not from random internet traffic. If we'd needed per-user rate limiting or audit logs at the backend layer, we would have added Firebase Admin SDK verification. We didn't need it.
