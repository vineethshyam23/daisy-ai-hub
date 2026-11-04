# Sanitization Notes

This documents what was changed from the production version of the codebase before open-sourcing.

## What was removed or replaced

### GCP project identifiers

| Original | Replaced with |
|---|---|
| Hardcoded GCP project ID in `modules/llm.py` | `os.environ.get("GCP_PROJECT")` |
| Hardcoded GCP project number in `middleware/auth.py` | Removed fallback; config must be explicit |
| Hardcoded GCP project ID in `nuxt.config.ts` | Empty string (env var required) |
| `config/gcp.yml` project_id and project_number | `your-gcp-project-id` / `your-gcp-project-number` |

### Firebase project IDs

| File | Change |
|---|---|
| `.firebaserc` | Real project IDs replaced with `your-firebase-project-dev` / `your-firebase-project-prod` |

### Company domain references

| File | Change |
|---|---|
| `frontend/pages/login.vue` | Hardcoded domain allowlist (`@company.com`, `@partner.com`) replaced with configurable `NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS` env var |
| `frontend/composables/useAdobeTracking.ts` | Company email domain mappings removed; replaced with comment explaining how to configure |
| `frontend/pages/index.vue` | Domain-based feature gating (`@partner.nl` restricted from Search) removed; all authenticated users now get full access |

### Internal URLs and identifiers

| File | Change |
|---|---|
| `backend/app.py` | CORS origins replaced with localhost placeholders + comments |
| `backend/services/career_service.py` | Personio job feed URL (`https://company.jobs.personio.de/xml`) replaced with `CAREER_PORTAL_XML_FEED_URL` env var |
| `frontend/pages/ai/approved-metro-tools.vue` | Partner-specific tool URLs replaced with `example.com` placeholders |
| `frontend/components/GlobalFooter.vue` | Internal Microsoft Forms links retained (generic format); company name and AUP PDF path generalized |

### Product-specific references

| File | Change |
|---|---|
| `backend/config/para.py` | Proprietary product codes kept; brand names on two line items removed |
| `backend/config/prompt.yml` | Social media and job description prompts de-branded; HoReCa-specific business context replaced with generic company context |
| `backend/models.py` | Field descriptions referencing internal career portal updated to generic wording |

### Personnel references

| File | Change |
|---|---|
| `frontend/pages/terms-of-service.vue` | Named legal contact replaced with `legal@yourcompany.com` placeholder |

### Debug artifacts

| File | Action |
|---|---|
| `frontend/composables/useApiTokenDebug.ts` | Not copied from source (debug-only file, not part of production flow) |

---

## What was preserved

- All architecture patterns and design decisions
- Error handling and production resilience patterns (retries, fallback, logging)
- Multi-modal document processing logic (Gemini Parts assembly)
- Auth middleware pattern (Secret Manager + startup load)
- Prompt engineering templates (business context generalized but structure intact)
- Full invoice validator logic (product code mapping generalized)
- Firebase Auth and Firestore integration patterns
- Cloud Run Dockerfile for both services

---

## Bug fixes applied during sanitization

These were real bugs found during the sanitization pass. Worth calling out separately from sanitization changes.

1. **`modules/helper.py`**: `raise logger.error(e)` raised `TypeError` (logger.error returns None). Fixed to `logger.error(e); raise`.
2. **`config/prompt.yml`**: Removed unfilled placeholder text (`[e.g., Project Phoenix]`) from meeting-minutes-daily-weekly and meeting-minutes-presentation prompt templates.
