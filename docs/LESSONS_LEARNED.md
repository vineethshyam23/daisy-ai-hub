# Lessons Learned

Things I'd do differently, things I wouldn't change, and a few things that surprised me.

---

## Load expensive config once at startup

The auth middleware reads the API token from Secret Manager once when the process starts, stores it in memory, and validates cheaply on every request. The obvious alternative was calling Secret Manager per-request — I'm glad we didn't. It would have added ~100ms to every call and created a dependency on Secret Manager uptime for every API request.

The tradeoff: rotating the token requires restarting the Cloud Run instance. That's fine for an internal secret that changes rarely.

## Per-request service instantiation is fine until it isn't

`EmailService()` gets instantiated fresh on every route call. Not ideal — it means a new LLM client per request. At the volume we were running (maybe 20 RPM peak) it was never a problem. At 10x that it would be. I left it because fixing it was refactoring for a scale we hadn't hit, and the risk of introducing a subtle shared-state bug wasn't worth it.

If this were going to production at higher load: inject services at app startup, don't create them per-call.

## Inline document upload hits a ceiling at 20MB

For the Document Analyzer, files go straight to Gemini as inline `Part.from_data()` — no GCS involved. This kept things simple and avoided the latency of uploading to storage first. It worked for everything we threw at it. The limit is 20MB per request; we never hit it in practice because our users were uploading meeting notes and invoices, not engineering specs.

For anything larger, GCS URI is the right path.

## Firebase + a separate backend token looks redundant but isn't

Firebase handles login, session management, password reset, and Google OAuth. The backend just validates a shared Bearer token — it has no idea who the user is. When someone asked why I wasn't just using Firebase ID tokens at the backend layer too, my answer was: the backend is a service, not a user-facing API. Per-user auth at the backend would mean calling Firebase Admin SDK on every request. The shared token was simpler and the security model was acceptable for an internal tool.

If I'd needed per-user rate limiting or audit logging, that answer changes.

## Nuxt SSR off saved a lot of pain

`ssr: false` means the frontend is a pure SPA. No hydration issues, no server-side rendering complexity. The Cloud Run container just serves static assets. I had to remind myself a few times that this was the right call even though it felt like I was "doing less" — for an internal tool with no SEO requirements, it was the right call every time.

## Streaming would have changed the UX significantly

The backend buffers the full Gemini response before returning it. This means users wait 2-15 seconds staring at a spinner before anything appears. For short email replies that's tolerable. For long document analyses it felt slow. We lived with it because streaming with Server-Sent Events would have needed frontend changes too and we were a 2-person team.

If I was building this again, streaming goes in from day one. The first thing users notice about an AI tool is perceived latency.

## The invoice validator came from a team member, not the roadmap

The Invoice Validator wasn't planned. A team member had a weekly task — cross-referencing Excel invoices against a Jira export — that took 2 hours every Friday. They built it in a day. It became one of the most-used tools in the whole thing.

I keep thinking about this one. The best tool in the product wasn't in my roadmap. It came from someone who was annoyed enough to fix their own problem.

## CORS will break you on the first deploy

Cloud Run assigns a new URL every time you deploy a new service revision unless you've set up a custom domain. We hadn't, and the first production deploy broke the frontend because the new backend URL wasn't in the CORS allowlist. Obvious in hindsight. The fix is a custom domain — after that the CORS list is stable and you stop thinking about it.
