# Lessons Learned

Production insights from running DAISY with 129 users across 3 months.

---

## 1. Secret Manager startup load beats per-request calls

Loading the API token from Secret Manager once at process startup (in `auth.py.__init__`) was the right call. The alternative — calling Secret Manager on every request — would add ~100ms of latency to every API call and create a failure mode where Secret Manager throttling brings down the whole service.

The tradeoff: rotating the token requires a service restart. Acceptable for a low-rotation internal secret.

**Pattern worth keeping**: load expensive config once at startup, store in memory, validate cheaply per-request.

---

## 2. Per-request service instantiation worked fine at this scale

`EmailService()` is instantiated per-request in the route handler, not injected. This is technically wasteful (creates a new LLM client per call), but at ~10-20 RPM it was never a bottleneck. At higher scale, inject services at app startup instead.

**Not worth fixing** at this scale. Know the tradeoff.

---

## 3. Inline document upload is simpler than GCS but has a ceiling

For the Document Analyzer, files are read into memory and sent directly to Gemini as inline `Part.from_data()`. No GCS storage. This kept the architecture simple and eliminated upload latency.

The ceiling: Gemini's inline document limit is 20MB per request. For larger files, GCS URI (`Part.from_uri()`) is the right path.

**Pattern**: start with inline, migrate to GCS URI only when you hit the size limit.

---

## 4. Firebase Auth + separate backend token is cleaner than it looks

Using Firebase ID tokens for user auth and a separate shared Bearer token for backend service auth sounds redundant, but it kept the concerns clean:

- Firebase handles: login, session, password reset, Google OAuth
- Backend handles: who is allowed to call the API (service-level, not user-level)

If per-user rate limiting or audit logging had been needed, we would have added Firebase Admin SDK verification at the backend layer. The current pattern works for a trusted internal service.

---

## 5. Nuxt 3 SSR off saves complexity on Cloud Run

`ssr: false` means the frontend is a pure SPA. No server-side rendering, no Node.js hydration issues. The Cloud Run container just runs `node server.js` which serves the pre-built static assets. Simpler Dockerfile, no hydration mismatches.

The tradeoff: SEO is worse. For an internal tool, that is not a concern.

---

## 6. Adobe DataLayer integration is optional but adds real value at scale

The `useAdobeTracking.ts` composable pushes structured events to `window.adobeDataLayer` for every tool interaction, button click, login, and error. This was not strictly necessary but proved very useful for understanding which tools were actually used vs. which ones we thought would be popular.

**Insight from data**: Email Assistant and Meeting Summarizer were the top two tools by far. Image Generator had the most individual sessions but shortest sessions. Document Analyzer had the highest user satisfaction based on follow-up feedback.

---

## 7. Gemini response latency is the dominant UX variable

Backend median response time was under 200ms excluding the Gemini call. The Gemini call itself ranged from 1.5s (short email) to 15s (long document analysis). Streaming would have improved perceived latency significantly — buffering the full response before returning is a noticeable UX penalty on longer generations.

**Next iteration**: implement streaming with Server-Sent Events for text generation endpoints.

---

## 8. The email domain gating saved support overhead

Restricting registration to specific company email domains (now configurable via `NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS`) prevented random external signups and kept the user base manageable. Without this, Firebase Auth would accept any email address.

The validation happens client-side (a motivated person could bypass it) but was sufficient for an internal tool. For stronger enforcement, verify the domain server-side during registration via Firebase Auth triggers.

---

## 9. CORS needs updating at every new Cloud Run URL

Cloud Run assigns a new URL on each service deployment unless a custom domain is mapped. Every new backend URL needs to be added to the CORS `origins` list in `app.py`. We learned this the hard way on the first deploy.

**Solution applied**: use a custom domain with Cloud Run domain mapping. After that, the CORS list is stable.

---

## 10. Invoice Validator was the most surprising use case

The Invoice Validator (cross-referencing Excel invoices against a Jira export) was not in the original plan — it was a one-day spike by a team member who had a recurring manual task. It became one of the most used tools because it solved a real, painful, weekly problem.

**Takeaway**: give the team time to build for their own pain points. The best tools often come from the people doing the work, not from top-down product decisions.
