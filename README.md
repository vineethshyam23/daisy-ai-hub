# DAISY AI Hub

Production AI productivity platform I built at a SaaS company — deployed on GCP Cloud Run, used by 129 internal users across 4 companies before being decommissioned in favour of Anthropic Claude and Google Workspace AI.

Built with a 2-person team. I owned product direction, GCP infrastructure, and architecture. Code written by the team under my technical leadership.

---

## Why this exists in my portfolio

DAISY started as a simple question: can non-engineers use Gemini for real work without needing a GCP account or knowing how to write prompts? The answer turned out to be yes, if you wrap the API in task-specific forms rather than a generic chat window.

129 users, 3 months in production, then decommissioned when Anthropic Claude rolled out org-wide. That's not a failure — that was always the exit condition. I open-sourced a sanitized version because the architecture is worth sharing even if the product isn't running anymore.

---

## AI Tools Shipped

| Tool | What it does |
|---|---|
| Email Assistant | Reply, improve, or reformat any email with tone and length controls |
| Meeting Summarizer | Paste a transcript, get structured minutes (decisions, actions, open items) |
| Social Media Post | Generate platform-tuned posts from a topic and tone brief |
| Image Generator | Vertex AI Imagen 4 with safety filter controls |
| Shopping Assistant | Gift recommendation engine with budget awareness |
| Learning Path | Personalised multi-week learning plan for any skill |
| Interview Questions | Fetches a job posting by ID and generates targeted interview prep |
| Job Description Generator | Structured JD from a brief, following a configurable template |
| Document Analyzer | Multi-modal: upload PDFs/images, ask questions, get cited answers |
| Invoice Validator | Cross-reference Excel invoices against a Jira export, flag mismatches |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| AI | Vertex AI Gemini 2.5 Flash Lite, Imagen 4 |
| Auth (backend) | Google Secret Manager (API token loaded at startup) |
| Auth (frontend) | Firebase Authentication (Email/Password + Google OAuth) |
| Session storage | Firestore |
| Frontend | Nuxt 3, Vue 3, TypeScript, Tailwind CSS 4, Pinia |
| Deployment | GCP Cloud Run (backend + frontend as separate services) |
| CI/CD | Cloud Build |
| Registry | Artifact Registry |

---

## Repository Layout

```
daisy-ai-hub/
├── README.md
├── BUSINESS_CASE.md        # problem statement and impact
├── ARCHITECTURE.md         # Mermaid system diagram
├── DATA_FLOW.md            # request paths and auth flow
├── backend/                # FastAPI backend
│   ├── app.py              # FastAPI app, CORS, routers
│   ├── models.py           # Pydantic request/response models
│   ├── middleware/auth.py  # Bearer token verification (Secret Manager)
│   ├── modules/            # llm.py, image_generation.py, helper.py, invoice_validator.py
│   ├── routes/             # one router per feature domain
│   ├── services/           # business logic layer
│   ├── config/             # gcp.yml, prompt.yml, para.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Nuxt 3 frontend
│   ├── pages/              # ai/, search/, admin/, login.vue, index.vue
│   ├── components/         # AIHeader, GlobalFooter
│   ├── composables/        # useAdobeTracking, useAuth
│   ├── stores/             # auth, roles (Pinia)
│   ├── nuxt.config.ts
│   ├── package.json
│   └── Dockerfile
└── docs/
    ├── SETUP.md            # step-by-step environment rebuild guide
    ├── SANITIZATION.md     # what was changed from the production version
    └── LESSONS_LEARNED.md  # production insights
```

---

## Documentation

- [Business Case](BUSINESS_CASE.md) — why this was built and what it solved
- [Architecture](ARCHITECTURE.md) — system diagram and component breakdown
- [Data Flow](DATA_FLOW.md) — request paths, auth flow, multi-modal pipeline
- [Setup Guide](docs/SETUP.md) — rebuild from scratch in a new GCP project
- [Sanitization Notes](docs/SANITIZATION.md) — what changed from production
- [Lessons Learned](docs/LESSONS_LEARNED.md) — production insights and gotchas
